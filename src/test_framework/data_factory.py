"""Run- and worker-aware unique test-data generation."""

from __future__ import annotations

import re
from dataclasses import dataclass
from uuid import uuid4


def _safe_fragment(value: str) -> str:
    normalized = re.sub(r"[^a-zA-Z0-9_-]+", "-", value).strip("-")
    return normalized[:24] or "local"


@dataclass(frozen=True, slots=True)
class OrderData:
    """One unique order payload owned by a test."""

    customer_name: str
    item_name: str
    quantity: int
    unit_price_cents: int

    def as_payload(self) -> dict[str, object]:
        return {
            "customer_name": self.customer_name,
            "item_name": self.item_name,
            "quantity": self.quantity,
            "unit_price_cents": self.unit_price_cents,
        }


class OrderFactory:
    """Generate unique payloads without shared mutable state."""

    def __init__(self, run_id: str, worker_id: str) -> None:
        self.run_id = _safe_fragment(run_id)
        self.worker_id = _safe_fragment(worker_id)

    def build(self) -> OrderData:
        unique_suffix = uuid4().hex[:10]
        owner = f"{self.run_id}-{self.worker_id}-{unique_suffix}"
        return OrderData(
            customer_name=f"Test {owner}",
            item_name=f"Quality Notebook {unique_suffix}",
            quantity=2,
            unit_price_cents=2499,
        )
