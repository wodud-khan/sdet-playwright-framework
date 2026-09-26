"""Cross-layer fixtures for controlled service tests."""

from __future__ import annotations

from collections.abc import Generator

import pytest
from playwright.sync_api import Page

from test_framework.api.client import ApiClient
from test_framework.config import Settings
from test_framework.data_factory import OrderFactory
from test_framework.db.client import PostgresOrderClient
from test_framework.diagnostics import BrowserEvidence, evidence_path, write_json_evidence
from test_framework.order_manager import OrderManager


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--allow-sqlite-ui-fallback",
        action="store_true",
        default=False,
        help="Allow focused UI tests against the explicitly configured SQLite fallback",
    )


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(
    item: pytest.Item,
    call: pytest.CallInfo[object],
) -> Generator[None, None, None]:
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)
    if report.when != "teardown":
        return

    failed = any(
        getattr(item, f"rep_{phase}", None) is not None and getattr(item, f"rep_{phase}").failed
        for phase in ("setup", "call", "teardown")
    )
    api_client = getattr(item, "_evidence_api_client", None)
    browser = getattr(item, "_browser_evidence", None)
    evidence_to_write: list[tuple[str, dict[str, object]]] = []
    if api_client is not None and failed:
        evidence_to_write.append(
            (
                "api",
                {
                    "exchanges": [
                        {
                            "method": exchange.method,
                            "url": exchange.url,
                            "status_code": exchange.status_code,
                            "elapsed_milliseconds": exchange.elapsed_milliseconds,
                            "error_category": exchange.error_category,
                        }
                        for exchange in api_client.exchanges
                    ]
                },
            )
        )
    if browser is not None and (failed or any(browser.as_dict().values())):
        evidence_to_write.append(("browser", browser.as_dict()))
    if not evidence_to_write:
        return

    settings = Settings.from_environment()
    write_errors: list[str] = []
    for kind, payload in evidence_to_write:
        path = evidence_path(settings.artifacts_dir, settings.test_run_id, kind, item.nodeid)
        try:
            write_json_evidence(path, payload)
        except Exception as error:
            write_errors.append(
                f"Evidence writing failed ({kind}): {type(error).__name__}: {error}"
            )
    if write_errors:
        report.outcome = "failed"
        report.longrepr = "\n".join(write_errors)


@pytest.fixture(scope="session")
def runtime_settings() -> Settings:
    """Require an explicit controlled application URL for service tests."""
    settings = Settings.from_environment()
    if not settings.app_base_url:
        pytest.fail(
            "APP_BASE_URL is required for service tests; start the controlled app first",
            pytrace=False,
        )
    return settings


@pytest.fixture(scope="session")
def service_settings(runtime_settings: Settings) -> Settings:
    """Require PostgreSQL for API, database, integration, and E2E evidence."""
    settings = runtime_settings
    if not settings.database_url.startswith(("postgresql://", "postgres://")):
        pytest.fail(
            "Service tests require the primary PostgreSQL runtime",
            pytrace=False,
        )
    return settings


@pytest.fixture(scope="session")
def ui_settings(runtime_settings: Settings, request: pytest.FixtureRequest) -> Settings:
    """Allow SQLite only through an explicit focused-UI development flag."""
    settings = runtime_settings
    if settings.database_url.startswith(("postgresql://", "postgres://")):
        return settings
    if settings.database_url.startswith("sqlite:///") and request.config.getoption(
        "--allow-sqlite-ui-fallback"
    ):
        return settings
    pytest.fail(
        "UI tests require PostgreSQL unless --allow-sqlite-ui-fallback is explicit",
        pytrace=False,
    )


@pytest.fixture
def api_client(
    service_settings: Settings,
    request: pytest.FixtureRequest,
) -> Generator[ApiClient, None, None]:
    client = ApiClient(
        service_settings.api_base_url,
        service_settings.api_timeout_seconds,
    )
    request.node._evidence_api_client = client
    try:
        yield client
    finally:
        client.close()


@pytest.fixture
def postgres_client(service_settings: Settings) -> PostgresOrderClient:
    return PostgresOrderClient(service_settings.database_url)


@pytest.fixture
def order_factory(service_settings: Settings, worker_id: str) -> OrderFactory:
    return OrderFactory(service_settings.test_run_id, worker_id)


@pytest.fixture
def order_manager(
    api_client: ApiClient,
    order_factory: OrderFactory,
) -> Generator[OrderManager, None, None]:
    """Create uniquely owned orders and guarantee targeted API cleanup."""
    manager = OrderManager(api_client, order_factory)
    yield manager
    manager.cleanup()


@pytest.fixture(autouse=True)
def browser_evidence(
    request: pytest.FixtureRequest,
) -> Generator[BrowserEvidence | None, None, None]:
    """Capture browser events only when a test requests `page`."""
    if "page" not in request.fixturenames:
        yield None
        return

    page: Page = request.getfixturevalue("page")
    evidence = BrowserEvidence()
    evidence.attach(page)
    request.node._browser_evidence = evidence
    yield evidence
    unexpected = evidence.unexpected_errors()
    if unexpected and not any(
        getattr(request.node, f"rep_{phase}", None) is not None
        and getattr(request.node, f"rep_{phase}").failed
        for phase in ("setup", "call")
    ):
        pytest.fail("Unexpected browser errors: " + "; ".join(unexpected), pytrace=False)
