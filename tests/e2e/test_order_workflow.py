"""Complete UI-to-API-to-PostgreSQL workflow with targeted cleanup."""

from __future__ import annotations

import pytest
from playwright.sync_api import Page

from test_framework.api.client import ApiClient
from test_framework.config import Settings
from test_framework.contracts import load_order_schema, validate_contract
from test_framework.data_factory import OrderFactory
from test_framework.db.client import PostgresOrderClient
from test_framework.order_manager import OrderManager
from test_framework.pages.order_page import OrderPage


@pytest.mark.e2e
@pytest.mark.parametrize(("quantity", "expected_total_cents"), [(1, 2499), (3, 7497)])
def test_ui_order_is_visible_through_api_and_postgresql(
    page: Page,
    service_settings: Settings,
    order_factory: OrderFactory,
    order_manager: OrderManager,
    api_client: ApiClient,
    postgres_client: PostgresOrderClient,
    quantity: int,
    expected_total_cents: int,
) -> None:
    payload = order_factory.build()
    order_page = OrderPage(page, service_settings.app_base_url)
    order_page.open()

    status, response_body = order_page.submit_order(
        payload.customer_name, payload.item_name, quantity
    )
    order_id = str(response_body["id"])
    order_manager.register_owned(order_id)
    assert status == 201
    validate_contract(response_body, load_order_schema())
    assert response_body["quantity"] == quantity
    assert response_body["unit_price_cents"] == 2499  # The UI fixes this price.
    assert response_body["total_cents"] == expected_total_cents
    order_page.expect_order_saved(order_id, expected_total_cents)

    api_response = api_client.get(f"/orders/{order_id}")
    assert api_response.status_code == 200
    assert api_response.json() == response_body

    row = postgres_client.fetch_order(order_id)
    assert row is not None
    assert row["customer_name"] == payload.customer_name
    assert row["item_name"] == payload.item_name
    assert row["quantity"] == quantity
    assert row["unit_price_cents"] == 2499

    delete_response = api_client.delete(f"/orders/{order_id}")
    assert delete_response.status_code == 204
    order_manager.mark_cleaned(order_id)
    assert not postgres_client.order_exists(order_id)
