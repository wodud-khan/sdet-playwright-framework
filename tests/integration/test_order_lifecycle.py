"""API-to-PostgreSQL lifecycle with explicit absence verification."""

from __future__ import annotations

import pytest

from test_framework.api.client import ApiClient
from test_framework.db.client import PostgresOrderClient
from test_framework.order_manager import OrderManager


@pytest.mark.integration
def test_api_create_and_delete_are_reflected_in_postgresql(
    create_order: OrderManager,
    api_client: ApiClient,
    postgres_client: PostgresOrderClient,
) -> None:
    created = create_order.create()

    assert postgres_client.order_exists(created.id)

    delete_response = api_client.delete(f"/orders/{created.id}")

    assert delete_response.status_code == 204
    assert not postgres_client.order_exists(created.id)
    create_order.mark_cleaned(created.id)
