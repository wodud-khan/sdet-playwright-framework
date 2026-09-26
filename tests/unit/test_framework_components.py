"""Unit tests for reusable client, contract, and data boundaries."""

from __future__ import annotations

import json
from unittest.mock import Mock

import pytest
import requests
from jsonschema import ValidationError

from test_framework.api.client import ApiClient
from test_framework.contracts import load_order_schema, validate_contract
from test_framework.data_factory import OrderData, OrderFactory
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
            json.dumps(
                {
                    "id": "c56a4180-65aa-42ec-a945-5fd21dec0538",
                    "customer_name": payload["customer_name"],
                }
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
    schema = load_order_schema()
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
    schema = load_order_schema()
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


@pytest.mark.unit
def test_unexpected_create_status_registers_only_api_verified_order() -> None:
    order_id = "c56a4180-65aa-42ec-a945-5fd21dec0538"
    payload = OrderData("Test unique-owner", "Quality Notebook unique-owner", 2, 2499)
    factory = Mock()
    factory.build.return_value = payload
    api = Mock()
    api.post.return_value = _response(500, json.dumps({"id": order_id}))
    api.get.side_effect = [
        _response(200, json.dumps({"id": order_id, **payload.as_payload()})),
        _response(404),
    ]
    api.delete.return_value = _response(204)
    manager = OrderManager(api, factory)

    with pytest.raises(AssertionError, match="Expected order creation status 201, got 500"):
        manager.create()

    assert list(manager._owned_order_ids) == [order_id]
    manager.cleanup()
    api.delete.assert_called_once_with(f"/orders/{order_id}")
    assert not manager._owned_order_ids


@pytest.mark.unit
def test_unexpected_create_status_does_not_claim_unrelated_order() -> None:
    order_id = "c56a4180-65aa-42ec-a945-5fd21dec0538"
    payload = OrderData("Test unique-owner", "Quality Notebook unique-owner", 2, 2499)
    factory = Mock()
    factory.build.return_value = payload
    api = Mock()
    api.post.return_value = _response(500, json.dumps({"id": order_id}))
    api.get.return_value = _response(
        200, json.dumps({"id": order_id, **payload.as_payload(), "customer_name": "Other test"})
    )
    manager = OrderManager(api, factory)

    with pytest.raises(AssertionError, match="Expected order creation status 201, got 500"):
        manager.create()

    assert not manager._owned_order_ids
    manager.cleanup()
    api.delete.assert_not_called()


@pytest.mark.unit
def test_cleanup_attempts_every_owned_id_and_keeps_only_failures() -> None:
    api = Mock()
    api.delete.side_effect = [_response(204), _response(500), _response(204)]
    api.get.side_effect = [_response(404), _response(404)]
    manager = OrderManager(api, OrderFactory("run", "gw0"))  # type: ignore[arg-type]
    for order_id in ("first", "broken", "last"):
        manager.register_owned(order_id)
    manager.register_owned("last")

    with pytest.raises(AssertionError, match=r"broken.*500"):
        manager.cleanup()

    assert api.delete.call_count == 3
    assert list(manager._owned_order_ids) == ["broken"]
    api.delete.side_effect = None
    api.delete.return_value = _response(204)
    api.get.side_effect = None
    api.get.return_value = _response(404)
    manager.cleanup()
    manager.cleanup()
    assert api.delete.call_count == 4


@pytest.mark.unit
@pytest.mark.parametrize("delete_status", [204, 404])
def test_cleanup_accepts_verified_absence(delete_status: int) -> None:
    api = Mock()
    api.delete.return_value = _response(delete_status)
    api.get.return_value = _response(404)
    manager = OrderManager(api, OrderFactory("run", "gw0"))  # type: ignore[arg-type]
    manager.register_owned("owned")

    manager.cleanup()

    assert not manager._owned_order_ids
    api.get.assert_called_once_with("/orders/owned")


@pytest.mark.unit
@pytest.mark.parametrize("failure", [requests.ConnectionError("offline"), _response(200)])
def test_cleanup_retains_unverified_order(failure: object) -> None:
    api = Mock()
    api.delete.return_value = _response(204)
    if isinstance(failure, Exception):
        api.get.side_effect = failure
    else:
        api.get.return_value = failure
    manager = OrderManager(api, OrderFactory("run", "gw0"))  # type: ignore[arg-type]
    manager.register_owned("owned")

    with pytest.raises(AssertionError, match="owned"):
        manager.cleanup()

    assert list(manager._owned_order_ids) == ["owned"]


@pytest.mark.unit
def test_cleanup_continues_after_delete_transport_failure() -> None:
    api = Mock()
    api.delete.side_effect = [requests.ConnectionError("offline"), _response(204)]
    api.get.return_value = _response(404)
    manager = OrderManager(api, OrderFactory("run", "gw0"))  # type: ignore[arg-type]
    manager.register_owned("successful")
    manager.register_owned("failed")

    with pytest.raises(AssertionError, match=r"failed.*ConnectionError"):
        manager.cleanup()

    assert api.delete.call_count == 2
    assert list(manager._owned_order_ids) == ["failed"]


@pytest.mark.unit
def test_transport_failure_records_metadata_and_preserves_exception() -> None:
    client = ApiClient("https://user:secret@example.invalid/api", 5)
    failure = requests.ConnectionError("private connection detail")
    client.session.request = Mock(side_effect=failure)  # type: ignore[method-assign]

    with pytest.raises(requests.ConnectionError) as caught:
        client.get("orders/1?token=private")

    assert caught.value is failure
    exchange = client.exchanges[0]
    assert exchange.method == "GET"
    assert exchange.url == "https://example.invalid/api/orders/1"
    assert exchange.status_code is None
    assert exchange.error_category == "ConnectionError"
    assert exchange.elapsed_milliseconds >= 0
    client.close()
