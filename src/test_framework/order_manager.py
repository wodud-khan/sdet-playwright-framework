"""Creation and exact cleanup for test-owned orders."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from test_framework.api.client import ApiClient
from test_framework.data_factory import OrderData, OrderFactory


@dataclass(frozen=True, slots=True)
class CreatedOrder:
    """Payload and response data for one test-owned order."""

    payload: OrderData
    response_body: dict[str, Any]

    @property
    def id(self) -> str:
        return str(self.response_body["id"])


class OrderManager:
    """Create unique orders and delete only records owned by this test."""

    def __init__(self, api_client: ApiClient, order_factory: OrderFactory) -> None:
        self.api_client = api_client
        self.order_factory = order_factory
        self._owned_order_ids: list[str] = []

    def create(self) -> CreatedOrder:
        payload = self.order_factory.build()
        response = self.api_client.post("/orders", payload.as_payload())
        if response.status_code != 201:
            raise AssertionError(
                f"Expected order creation status 201, got {response.status_code}: {response.text}"
            )
        response_body: dict[str, Any] = response.json()
        order_id = str(response_body["id"])
        self._owned_order_ids.append(order_id)
        return CreatedOrder(payload=payload, response_body=response_body)

    def mark_cleaned(self, order_id: str) -> None:
        """Release an order after a test explicitly proves its deletion."""
        self._owned_order_ids.remove(order_id)

    def cleanup(self) -> None:
        """Delete every remaining owned order and prove API absence."""
        for order_id in reversed(self._owned_order_ids):
            delete_response = self.api_client.delete(f"/orders/{order_id}")
            if delete_response.status_code != 204:
                raise AssertionError(
                    f"Cleanup expected status 204 for {order_id}, "
                    f"got {delete_response.status_code}: {delete_response.text}"
                )
            verify_response = self.api_client.get(f"/orders/{order_id}")
            if verify_response.status_code != 404:
                raise AssertionError(
                    f"Cleanup expected {order_id} to return 404, "
                    f"got {verify_response.status_code}: {verify_response.text}"
                )
        self._owned_order_ids.clear()
