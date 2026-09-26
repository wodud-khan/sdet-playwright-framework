"""PostgreSQL persistence with a narrow SQLite adapter for isolated tests."""

from __future__ import annotations

import sqlite3
from contextlib import closing
from pathlib import Path

import psycopg
from psycopg.rows import dict_row

CREATE_ORDERS_TABLE = """
CREATE TABLE IF NOT EXISTS orders (
    id VARCHAR(36) PRIMARY KEY,
    customer_name VARCHAR(80) NOT NULL,
    item_name VARCHAR(80) NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity BETWEEN 1 AND 100),
    unit_price_cents INTEGER NOT NULL CHECK (unit_price_cents BETWEEN 1 AND 1000000),
    status VARCHAR(20) NOT NULL CHECK (status = 'created'),
    created_at VARCHAR(40) NOT NULL
)
"""

Parameters = tuple[object, ...]


class Database:
    """Execute the small SQL surface needed by the portfolio application."""

    def __init__(self, url: str) -> None:
        if not url.startswith(("sqlite:///", "postgresql://", "postgres://")):
            raise ValueError("DATABASE_URL must use sqlite, postgresql, or postgres")
        self.url = url
        self.backend = "sqlite" if url.startswith("sqlite:///") else "postgresql"

    def initialize(self) -> None:
        """Create the application table when it does not exist."""
        self.execute(CREATE_ORDERS_TABLE)

    def execute(self, statement: str, parameters: Parameters = ()) -> int:
        """Execute a state-changing statement and return its affected-row count."""
        if self.backend == "sqlite":
            path = self._sqlite_path()
            path.parent.mkdir(parents=True, exist_ok=True)
            with closing(sqlite3.connect(path)) as sqlite_connection, sqlite_connection:
                sqlite_cursor = sqlite_connection.execute(statement, parameters)
                return sqlite_cursor.rowcount

        with (
            psycopg.connect(self.url) as postgres_connection,
            postgres_connection.cursor() as postgres_cursor,
        ):
            postgres_cursor.execute(self._postgres_statement(statement), parameters)
            return postgres_cursor.rowcount

    def fetch_one(
        self,
        statement: str,
        parameters: Parameters = (),
    ) -> dict[str, object] | None:
        """Return one row as a mapping, or `None` when no row matches."""
        if self.backend == "sqlite":
            path = self._sqlite_path()
            path.parent.mkdir(parents=True, exist_ok=True)
            with closing(sqlite3.connect(path)) as sqlite_connection, sqlite_connection:
                sqlite_connection.row_factory = sqlite3.Row
                row = sqlite_connection.execute(statement, parameters).fetchone()
                return dict(row) if row is not None else None

        with (
            psycopg.connect(self.url, row_factory=dict_row) as postgres_connection,
            postgres_connection.cursor() as postgres_cursor,
        ):
            postgres_cursor.execute(self._postgres_statement(statement), parameters)
            row = postgres_cursor.fetchone()
            return dict(row) if row is not None else None

    def is_healthy(self) -> bool:
        """Return whether the configured database accepts a simple query."""
        try:
            row = self.fetch_one("SELECT 1 AS healthy")
        except (OSError, sqlite3.Error, psycopg.Error):
            return False
        return row is not None and row.get("healthy") == 1

    def _sqlite_path(self) -> Path:
        raw_path = self.url.removeprefix("sqlite:///")
        if not raw_path or raw_path == ":memory:":
            raise ValueError("SQLite must use a persistent file path")
        return Path(raw_path)

    @staticmethod
    def _postgres_statement(statement: str) -> str:
        return statement.replace("?", "%s")
