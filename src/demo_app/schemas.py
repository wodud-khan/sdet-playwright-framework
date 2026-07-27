"""Request and response contracts for the controlled order application."""

from __future__ import annotations

from datetime import datetime
from typing import Literal, Self

from pydantic import BaseModel, ConfigDict, Field, field_validator


def _record_integer(value: object, field_name: str) -> int:
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        return int(value)
    raise TypeError(f"{field_name} must be an integer")


class OrderCreate(BaseModel):
    """Validated order input accepted by the API."""

    model_config = ConfigDict(extra="forbid")

    customer_name: str = Field(min_length=2, max_length=80)
    item_name: str = Field(min_length=2, max_length=80)
    quantity: int = Field(ge=1, le=100)
    unit_price_cents: int = Field(ge=1, le=1_000_000)

    @field_validator("customer_name", "item_name")
    @classmethod
    def strip_text(cls, value: str) -> str:
        """Normalize surrounding whitespace while preserving meaningful content."""
        normalized = value.strip()
        if len(normalized) < 2:
            raise ValueError("must contain at least two non-whitespace characters")
        return normalized


class OrderResponse(OrderCreate):
    """Stable order representation returned by the API."""

    id: str
    status: Literal["created"]
    total_cents: int
    created_at: datetime

    @classmethod
    def from_record(cls, record: dict[str, object]) -> Self:
        """Create a response from a database row."""
        quantity = _record_integer(record["quantity"], "quantity")
        unit_price_cents = _record_integer(
            record["unit_price_cents"],
            "unit_price_cents",
        )
        return cls(
            id=str(record["id"]),
            customer_name=str(record["customer_name"]),
            item_name=str(record["item_name"]),
            quantity=quantity,
            unit_price_cents=unit_price_cents,
            status="created",
            total_cents=quantity * unit_price_cents,
            created_at=datetime.fromisoformat(str(record["created_at"])),
        )


class HealthResponse(BaseModel):
    """Readiness response for local and container orchestration."""

    status: Literal["ok"]
    database: Literal["ok"]
