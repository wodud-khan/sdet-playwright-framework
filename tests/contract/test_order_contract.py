"""Black-box JSON Schema checks for order responses."""

from __future__ import annotations

import pytest

from test_framework.api.client import ApiClient
from test_framework.contracts import load_order_schema, validate_contract
from test_framework.order_manager import OrderManager


@pytest.mark.contract
def test_create_and_read_responses_match_order_contract(
    order_manager: OrderManager,
    api_client: ApiClient,
) -> None:
    created = order_manager.create()
    validate_contract(created.response_body, load_order_schema())

    read_response = api_client.get(f"/orders/{created.id}")

    assert read_response.status_code == 200
    validate_contract(read_response.json(), load_order_schema())
