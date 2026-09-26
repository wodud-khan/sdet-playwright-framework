"""Unit tests for the SQLite database and order repository path."""

from __future__ import annotations

import sqlite3
from pathlib import Path
from unittest.mock import patch

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


@pytest.mark.unit
@pytest.mark.parametrize("operation", ["execute", "fetch_one"])
@pytest.mark.parametrize("fails", [False, True])
def test_sqlite_connection_closes_on_success_and_error(
    tmp_path: Path, operation: str, fails: bool
) -> None:
    database = Database(f"sqlite:///{tmp_path / 'orders.db'}")
    real_connect = sqlite3.connect
    connections: list[sqlite3.Connection] = []

    def tracking_connect(path: Path) -> sqlite3.Connection:
        connection = real_connect(path)
        connections.append(connection)
        return connection

    with patch("demo_app.database.sqlite3.connect", side_effect=tracking_connect):
        if fails:
            with pytest.raises(sqlite3.OperationalError):
                getattr(database, operation)("SELECT * FROM missing_table")
        elif operation == "execute":
            database.execute("CREATE TABLE sample (value INTEGER)")
        else:
            assert database.fetch_one("SELECT 1 AS value") == {"value": 1}

    assert len(connections) == 1
    with pytest.raises(sqlite3.ProgrammingError, match="closed database"):
        connections[0].execute("SELECT 1")


@pytest.mark.unit
def test_sqlite_failed_write_rolls_back(tmp_path: Path) -> None:
    database = Database(f"sqlite:///{tmp_path / 'orders.db'}")
    database.execute("CREATE TABLE sample (value INTEGER UNIQUE)")
    database.execute("INSERT INTO sample VALUES (?)", (1,))
    with pytest.raises(sqlite3.IntegrityError):
        database.execute("INSERT INTO sample VALUES (?)", (1,))
    assert database.fetch_one("SELECT count(*) AS total FROM sample") == {"total": 1}
