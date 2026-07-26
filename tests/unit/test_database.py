"""Unit tests for the SQLite database and order repository path."""

from __future__ import annotations

from pathlib import Path

import pytest

from demo_app.database import Database
from demo_app.repository import OrderRepository
from demo_app.schemas import OrderCreate


@pytest.mark.unit
def test_repository_round_trip_uses_exact_order_id(tmp_path: Path) -> None:
    database = Database(f"sqlite:///{tmp_path / 'orders.db'}")
    database.initialize()
    repository = OrderRepository(database)
    payload = OrderCreate(
        customer_name="  Ada Lovelace  ",
        item_name="Quality Notebook",
        quantity=2,
        unit_price_cents=2499,
    )

    created = repository.create(payload)

    assert created.customer_name == "Ada Lovelace"
    assert created.total_cents == 4998
    assert repository.get(created.id) == created
    assert repository.delete(created.id) is True
    assert repository.get(created.id) is None
    assert repository.delete(created.id) is False


@pytest.mark.unit
def test_database_rejects_unsupported_url() -> None:
    with pytest.raises(ValueError, match="DATABASE_URL"):
        Database("mysql://localhost/example")
