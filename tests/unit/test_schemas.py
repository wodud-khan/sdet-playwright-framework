"""Unit tests for order request and response rules."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from demo_app.schemas import OrderCreate


@pytest.mark.unit
def test_order_input_normalizes_human_text() -> None:
    order = OrderCreate(
        customer_name="  Grace Hopper ",
        item_name="  Test Journal ",
        quantity=1,
        unit_price_cents=2499,
    )

    assert order.customer_name == "Grace Hopper"
    assert order.item_name == "Test Journal"


@pytest.mark.unit
@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("customer_name", " "),
        ("item_name", "x"),
        ("quantity", 0),
        ("quantity", 101),
        ("unit_price_cents", 0),
        ("unit_price_cents", 1_000_001),
        ("extra", "unrecognized"),
    ],
)
def test_order_input_rejects_invalid_business_values(field: str, value: object) -> None:
    payload: dict[str, object] = {
        "customer_name": "Grace Hopper",
        "item_name": "Test Journal",
        "quantity": 1,
        "unit_price_cents": 2499,
    }
    payload[field] = value

    with pytest.raises(ValidationError):
        OrderCreate.model_validate(payload)
