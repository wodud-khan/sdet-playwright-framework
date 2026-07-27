"""Unit tests for private-data-safe diagnostic file handling."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from test_framework.diagnostics import safe_test_name, write_json_evidence


@pytest.mark.unit
def test_safe_test_name_removes_path_and_parameter_separators() -> None:
    name = safe_test_name("tests/ui/test_order.py::test_name[value / private]")

    assert "/" not in name
    assert "::" not in name
    assert len(name) <= 180


@pytest.mark.unit
def test_json_evidence_is_written_under_requested_artifact_root(tmp_path: Path) -> None:
    output = tmp_path / "browser" / "test.json"

    write_json_evidence(output, {"status": "failed", "events": []})

    assert json.loads(output.read_text(encoding="utf-8")) == {
        "events": [],
        "status": "failed",
    }
