"""Unit tests for reusable client, contract, and data boundaries."""

from __future__ import annotations

from pathlib import Path

import pytest
import requests
from jsonschema import ValidationError

from test_framework.api.client import ApiClient
from test_framework.contracts import validate_contract
from test_framework.data_factory import OrderFactory
from test_framework.db.client import PostgresOrderClient
from test_framework.order_manager import OrderManager


def _response(status_code: int, body: str = "") -> requests.Response:
    response = requests.Response()
    response.status_code = status_code
    response._content = body.encode()
    response.url = "http://example.invalid/api/orders"
    return response


class _FakeOrderApi:
    def __init__(self) -> None:
        self.requested_endpoints: list[tuple[str, str]] = []

    def post(self, endpoint: str, payload: dict[str, object]) -> requests.Response:
        self.requested_endpoints.append(("POST", endpoint))
        return _response(
            201,
            (
                '{"id":"c56a4180-65aa-42ec-a945-5fd21dec0538",'
                f'"customer_name":"{payload["customer_name"]}"'
                "}"
            ),
        )

    def delete(self, endpoint: str) -> requests.Response:
        self.requested_endpoints.append(("DELETE", endpoint))
        return _response(204)

    def get(self, endpoint: str) -> requests.Response:
        self.requested_endpoints.append(("GET", endpoint))
        return _response(404, '{"detail":"Order not found"}')


@pytest.mark.unit
def test_order_factory_produces_unique_worker_owned_payloads() -> None:
    factory = OrderFactory("run 42", "gw1")

    first = factory.build()
    second = factory.build()

    assert first != second
    assert "run-42-gw1" in first.customer_name
    assert "run-42-gw1" in second.customer_name


@pytest.mark.unit
def test_clients_reject_invalid_runtime_configuration() -> None:
    with pytest.raises(ValueError, match="absolute"):
        ApiClient("localhost:8000/api", 5)

    with pytest.raises(ValueError, match="PostgreSQL"):
        PostgresOrderClient("sqlite:///orders.db")


@pytest.mark.unit
def test_order_contract_accepts_valid_response() -> None:
    schema_path = Path("contracts/order.schema.json")
    schema = __import__("json").loads(schema_path.read_text(encoding="utf-8"))
    response = {
        "id": "c56a4180-65aa-42ec-a945-5fd21dec0538",
        "customer_name": "Test Customer",
        "item_name": "Quality Notebook",
        "quantity": 2,
        "unit_price_cents": 2499,
        "status": "created",
        "total_cents": 4998,
        "created_at": "2026-07-26T12:00:00+00:00",
    }

    validate_contract(response, schema)


@pytest.mark.unit
def test_order_contract_rejects_unknown_fields() -> None:
    schema_path = Path("contracts/order.schema.json")
    schema = __import__("json").loads(schema_path.read_text(encoding="utf-8"))
    response = {
        "id": "c56a4180-65aa-42ec-a945-5fd21dec0538",
        "customer_name": "Test Customer",
        "item_name": "Quality Notebook",
        "quantity": 2,
        "unit_price_cents": 2499,
        "status": "created",
        "total_cents": 4998,
        "created_at": "2026-07-26T12:00:00+00:00",
        "unexpected": True,
    }

    with pytest.raises(ValidationError):
        validate_contract(response, schema)


@pytest.mark.unit
def test_order_manager_cleans_up_only_its_exact_order() -> None:
    api = _FakeOrderApi()
    manager = OrderManager(api, OrderFactory("run-1", "gw0"))  # type: ignore[arg-type]

    created = manager.create()
    manager.cleanup()

    assert api.requested_endpoints == [
        ("POST", "/orders"),
        ("DELETE", f"/orders/{created.id}"),
        ("GET", f"/orders/{created.id}"),
    ]
