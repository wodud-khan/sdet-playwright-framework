"""Cross-layer fixtures for controlled service tests."""

from __future__ import annotations

from collections.abc import Generator

import pytest

from test_framework.api.client import ApiClient
from test_framework.config import Settings
from test_framework.data_factory import OrderFactory
from test_framework.db.client import PostgresOrderClient
from test_framework.order_manager import OrderManager


@pytest.fixture(scope="session")
def service_settings() -> Settings:
    """Require explicit service URLs and PostgreSQL for non-unit test layers."""
    settings = Settings.from_environment()
    if not settings.app_base_url:
        pytest.fail(
            "APP_BASE_URL is required for service tests; start the controlled app first",
            pytrace=False,
        )
    if not settings.database_url.startswith(("postgresql://", "postgres://")):
        pytest.fail(
            "Service tests require the primary PostgreSQL runtime",
            pytrace=False,
        )
    return settings


@pytest.fixture
def api_client(service_settings: Settings) -> Generator[ApiClient, None, None]:
    client = ApiClient(
        service_settings.api_base_url,
        service_settings.api_timeout_seconds,
    )
    yield client
    client.close()


@pytest.fixture
def postgres_client(service_settings: Settings) -> PostgresOrderClient:
    return PostgresOrderClient(service_settings.database_url)


@pytest.fixture
def order_factory(service_settings: Settings, worker_id: str) -> OrderFactory:
    return OrderFactory(service_settings.test_run_id, worker_id)


@pytest.fixture
def create_order(
    api_client: ApiClient,
    order_factory: OrderFactory,
) -> Generator[OrderManager, None, None]:
    """Create uniquely owned orders and guarantee targeted API cleanup."""
    manager = OrderManager(api_client, order_factory)
    yield manager
    manager.cleanup()
