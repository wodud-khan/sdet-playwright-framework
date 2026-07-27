"""Black-box JSON Schema checks for order responses."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from test_framework.api.client import ApiClient
from test_framework.contracts import validate_contract
from test_framework.order_manager import OrderManager

ORDER_SCHEMA = json.loads(Path("contracts/order.schema.json").read_text(encoding="utf-8"))


@pytest.mark.contract
def test_create_and_read_responses_match_order_contract(
    create_order: OrderManager,
    api_client: ApiClient,
) -> None:
    created = create_order.create()
    validate_contract(created.response_body, ORDER_SCHEMA)

    read_response = api_client.get(f"/orders/{created.id}")

    assert read_response.status_code == 200
    validate_contract(read_response.json(), ORDER_SCHEMA)
