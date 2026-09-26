"""Creation and exact cleanup for test-owned orders."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from uuid import UUID

import requests

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
        self._owned_order_ids: dict[str, None] = {}

    def create(self) -> CreatedOrder:
        payload = self.order_factory.build()
        response = self.api_client.post("/orders", payload.as_payload())
        if response.status_code != 201:
            self._register_confirmed_creation(payload, response)
            raise AssertionError(
                f"Expected order creation status 201, got {response.status_code}: {response.text}"
            )
        response_body: dict[str, Any] = response.json()
        order_id = str(response_body["id"])
        self.register_owned(order_id)
        return CreatedOrder(payload=payload, response_body=response_body)

    def _register_confirmed_creation(self, payload: OrderData, response: requests.Response) -> None:
        """Retain an unexpected response's ID only after an exact API read proves ownership."""
        try:
            body = response.json()
            if not isinstance(body, dict):
                return
            candidate = body.get("id")
            if not isinstance(candidate, str) or str(UUID(candidate)) != candidate:
                return
            observed_response = self.api_client.get(f"/orders/{candidate}")
            if observed_response.status_code != 200:
                return
            observed = observed_response.json()
        except (ValueError, TypeError, requests.RequestException):
            return
        if (
            isinstance(observed, dict)
            and observed.get("id") == candidate
            and all(observed.get(field) == value for field, value in payload.as_payload().items())
        ):
            self.register_owned(candidate)

    def mark_cleaned(self, order_id: str) -> None:
        """Release an order after a test explicitly proves its deletion."""
        self._owned_order_ids.pop(order_id)

    def register_owned(self, order_id: str) -> None:
        """Register state created outside the API helper, such as through the UI."""
        if not order_id:
            raise ValueError("An owned order must have an ID")
        self._owned_order_ids[order_id] = None

    def cleanup(self) -> None:
        """Delete every remaining owned order and prove API absence."""
        errors: list[str] = []
        for order_id in reversed(tuple(self._owned_order_ids)):
            try:
                delete_response = self.api_client.delete(f"/orders/{order_id}")
                if delete_response.status_code not in (204, 404):
                    raise AssertionError(
                        f"DELETE returned {delete_response.status_code}: {delete_response.text}"
                    )
                verify_response = self.api_client.get(f"/orders/{order_id}")
                if verify_response.status_code != 404:
                    raise AssertionError(
                        f"GET returned {verify_response.status_code}: {verify_response.text}"
                    )
            except Exception as error:
                errors.append(f"{order_id}: {type(error).__name__}: {error}")
            else:
                del self._owned_order_ids[order_id]
        if errors:
            raise AssertionError("Order cleanup failed:\n" + "\n".join(errors))
