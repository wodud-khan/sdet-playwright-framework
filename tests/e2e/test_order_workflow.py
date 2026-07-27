"""Complete UI-to-API-to-PostgreSQL workflow with targeted cleanup."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from playwright.sync_api import Page

from test_framework.api.client import ApiClient
from test_framework.config import Settings
from test_framework.contracts import validate_contract
from test_framework.data_factory import OrderFactory
from test_framework.db.client import PostgresOrderClient
from test_framework.order_manager import OrderManager
from test_framework.pages.order_page import OrderPage

ORDER_SCHEMA = json.loads(Path("contracts/order.schema.json").read_text(encoding="utf-8"))


@pytest.mark.e2e
def test_ui_order_is_visible_through_api_and_postgresql(
    page: Page,
    service_settings: Settings,
    order_factory: OrderFactory,
    order_manager: OrderManager,
    api_client: ApiClient,
    postgres_client: PostgresOrderClient,
) -> None:
    payload = order_factory.build()
    order_page = OrderPage(page, service_settings.app_base_url)
    order_page.open()

    response_body = order_page.create_order(payload)
    order_id = str(response_body["id"])
    order_manager.register_owned(order_id)
    validate_contract(response_body, ORDER_SCHEMA)

    api_response = api_client.get(f"/orders/{order_id}")
    assert api_response.status_code == 200
    assert api_response.json() == response_body

    row = postgres_client.fetch_order(order_id)
    assert row is not None
    assert row["customer_name"] == payload.customer_name
    assert row["item_name"] == payload.item_name
    assert row["quantity"] == payload.quantity
    assert row["unit_price_cents"] == payload.unit_price_cents

    delete_response = api_client.delete(f"/orders/{order_id}")
    assert delete_response.status_code == 204
    assert not postgres_client.order_exists(order_id)
    order_manager.mark_cleaned(order_id)
