"""Persistence operations for the controlled order workflow."""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from demo_app.database import Database
from demo_app.schemas import OrderCreate, OrderResponse


class OrderRepository:
    """Store and retrieve orders without exposing database details to routes."""

    def __init__(self, database: Database) -> None:
        self.database = database

    def create(self, payload: OrderCreate) -> OrderResponse:
        """Persist one unique order and return its API representation."""
        order_id = str(uuid4())
        created_at = datetime.now(UTC).isoformat()
        self.database.execute(
            """
            INSERT INTO orders (
                id,
                customer_name,
                item_name,
                quantity,
                unit_price_cents,
                status,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                order_id,
                payload.customer_name,
                payload.item_name,
                payload.quantity,
                payload.unit_price_cents,
                "created",
                created_at,
            ),
        )
        order = self.get(order_id)
        if order is None:
            raise RuntimeError("Created order could not be read")
        return order

    def get(self, order_id: str) -> OrderResponse | None:
        """Return one order by exact identifier."""
        row = self.database.fetch_one(
            """
            SELECT
                id,
                customer_name,
                item_name,
                quantity,
                unit_price_cents,
                status,
                created_at
            FROM orders
            WHERE id = ?
            """,
            (order_id,),
        )
        return OrderResponse.from_record(row) if row is not None else None

    def delete(self, order_id: str) -> bool:
        """Delete only the identified order."""
        affected_rows = self.database.execute(
            "DELETE FROM orders WHERE id = ?",
            (order_id,),
        )
        return affected_rows == 1
