"""JSON Schema validation independent of application model classes."""

from __future__ import annotations

from jsonschema import Draft202012Validator, FormatChecker


def validate_contract(instance: object, schema: dict[str, object]) -> None:
    """Validate one response and raise a detailed schema error on mismatch."""
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(
        schema,
        format_checker=FormatChecker(),
    )
    validator.validate(instance)
