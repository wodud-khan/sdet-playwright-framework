"""Black-box REST behavior for the controlled order API."""

from __future__ import annotations

import pytest

from test_framework.api.client import ApiClient
from test_framework.data_factory import OrderFactory
from test_framework.order_manager import OrderManager


@pytest.mark.api
def test_create_and_read_order(order_manager: OrderManager, api_client: ApiClient) -> None:
    created = order_manager.create()

    assert created.response_body["customer_name"] == created.payload.customer_name
    assert created.response_body["item_name"] == created.payload.item_name
    assert created.response_body["total_cents"] == 4998

    response = api_client.get(f"/orders/{created.id}")

    assert response.status_code == 200
    assert response.json() == created.response_body


@pytest.mark.api
def test_create_order_rejects_invalid_quantity(
    api_client: ApiClient,
    order_factory: OrderFactory,
) -> None:
    payload = order_factory.build().as_payload()
    payload["quantity"] = 0

    response = api_client.post("/orders", payload)

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "quantity"]


@pytest.mark.api
def test_unknown_order_returns_not_found(api_client: ApiClient) -> None:
    response = api_client.get("/orders/00000000-0000-0000-0000-000000000000")

    assert response.status_code == 404
    assert response.json() == {"detail": "Order not found"}


@pytest.mark.api
def test_delete_unknown_order_returns_not_found(api_client: ApiClient) -> None:
    response = api_client.delete("/orders/00000000-0000-0000-0000-000000000000")

    assert response.status_code == 404
    assert response.json() == {"detail": "Order not found"}
