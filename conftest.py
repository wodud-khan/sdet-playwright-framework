"""Cross-layer fixtures for controlled service tests."""

from __future__ import annotations

from collections.abc import Generator
from pathlib import Path

import pytest
from playwright.sync_api import Page

from test_framework.api.client import ApiClient
from test_framework.config import Settings
from test_framework.data_factory import OrderFactory
from test_framework.db.client import PostgresOrderClient
from test_framework.diagnostics import BrowserEvidence, safe_test_name, write_json_evidence
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
    yield client
    report = getattr(request.node, "rep_call", None)
    if report is not None and report.failed:
        output_path = (
            service_settings.artifacts_dir / "api" / f"{safe_test_name(request.node.nodeid)}.json"
        )
        write_json_evidence(
            output_path,
            {
                "test": request.node.nodeid,
                "exchanges": [
                    {
                        "method": exchange.method,
                        "url": exchange.url,
                        "status_code": exchange.status_code,
                        "elapsed_milliseconds": exchange.elapsed_milliseconds,
                    }
                    for exchange in client.exchanges
                ],
            },
        )
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
) -> Generator[None, None, None]:
    """Capture body-free browser events only when a test requests `page`."""
    if "page" not in request.fixturenames:
        yield
        return

    page: Page = request.getfixturevalue("page")
    evidence = BrowserEvidence()
    evidence.attach(page)
    yield

    report = getattr(request.node, "rep_call", None)
    if report is None:
        return

    settings = Settings.from_environment()
    output_path = (
        Path(settings.artifacts_dir) / "browser" / f"{safe_test_name(request.node.nodeid)}.json"
    )
    evidence_payload = {
        "test": request.node.nodeid,
        **evidence.as_dict(),
    }
    has_browser_errors = any(
        (
            evidence.console_errors,
            evidence.page_errors,
            evidence.failed_requests,
            evidence.error_responses,
        )
    )
    if report.failed or has_browser_errors:
        write_json_evidence(output_path, evidence_payload)
    if report.passed and has_browser_errors:
        pytest.fail(
            f"Unexpected browser errors were captured in {output_path}",
            pytrace=False,
        )
