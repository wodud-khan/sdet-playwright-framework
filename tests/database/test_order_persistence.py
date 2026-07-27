"""Direct PostgreSQL verification independent of application repositories."""

from __future__ import annotations

import pytest

from test_framework.db.client import PostgresOrderClient
from test_framework.order_manager import OrderManager


@pytest.mark.database
def test_created_order_is_persisted_with_exact_values(
    order_manager: OrderManager,
    postgres_client: PostgresOrderClient,
) -> None:
    created = order_manager.create()

    row = postgres_client.fetch_order(created.id)

    assert row is not None
    assert row["id"] == created.id
    assert row["customer_name"] == created.payload.customer_name
    assert row["item_name"] == created.payload.item_name
    assert row["quantity"] == created.payload.quantity
    assert row["unit_price_cents"] == created.payload.unit_price_cents
    assert row["status"] == "created"
