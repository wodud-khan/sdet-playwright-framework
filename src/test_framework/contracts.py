"""JSON Schema validation independent of application model classes."""

from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ORDER_SCHEMA_PATH = Path(__file__).resolve().parents[2] / "contracts" / "order.schema.json"


def load_order_schema() -> dict[str, object]:
    schema: dict[str, object] = json.loads(ORDER_SCHEMA_PATH.read_text(encoding="utf-8"))
    return schema


def validate_contract(instance: object, schema: dict[str, object]) -> None:
    """Validate one response and raise a detailed schema error on mismatch."""
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(
        schema,
        format_checker=FormatChecker(),
    )
    validator.validate(instance)
