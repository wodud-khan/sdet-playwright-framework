"""Direct PostgreSQL assertions independent of application repositories."""

from __future__ import annotations

from typing import Any

import psycopg
from psycopg.rows import dict_row


class PostgresOrderClient:
    """Read order state directly from the primary PostgreSQL runtime."""

    def __init__(self, database_url: str) -> None:
        if not database_url.startswith(("postgresql://", "postgres://")):
            raise ValueError("Direct database validation requires PostgreSQL")
        self.database_url = database_url

    def fetch_order(self, order_id: str) -> dict[str, object] | None:
        """Return one exact order row without using application code."""
        with (
            psycopg.connect(self.database_url, row_factory=dict_row) as connection,
            connection.cursor() as cursor,
        ):
            cursor.execute(
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
                WHERE id = %s
                """,
                (order_id,),
            )
            row: dict[str, Any] | None = cursor.fetchone()
            return dict(row) if row is not None else None

    def order_exists(self, order_id: str) -> bool:
        return self.fetch_order(order_id) is not None
