"""Unit tests for private-data-safe diagnostic file handling."""

from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from test_framework.api.client import safe_url
from test_framework.diagnostics import (
    BrowserEvidence,
    evidence_path,
    safe_test_name,
    write_json_evidence,
)


@pytest.mark.unit
def test_safe_test_name_removes_path_and_parameter_separators() -> None:
    name = safe_test_name("tests/ui/test_order.py::test_name[value / private]")

    assert "/" not in name
    assert "::" not in name
    assert len(name) <= 180


@pytest.mark.unit
def test_evidence_names_distinguish_truncated_ids_and_repeated_runs(tmp_path: Path) -> None:
    prefix = "test_" + "x" * 200
    assert safe_test_name(prefix + "a") != safe_test_name(prefix + "b")
    first = evidence_path(tmp_path, "run", "api", prefix)
    second = evidence_path(tmp_path, "run", "api", prefix)
    assert first != second


@pytest.mark.unit
def test_json_evidence_is_written_under_requested_artifact_root(tmp_path: Path) -> None:
    output = tmp_path / "browser" / "test.json"

    write_json_evidence(output, {"status": "failed", "events": []})

    assert json.loads(output.read_text(encoding="utf-8")) == {
        "events": [],
        "status": "failed",
    }


@pytest.mark.unit
def test_safe_url_removes_credentials_query_and_fragment() -> None:
    assert safe_url("https://user:secret@example.invalid:8443/api/orders?token=private#part") == (
        "https://example.invalid:8443/api/orders"
    )
    assert safe_url("http://[invalid") == "<invalid URL>"


@pytest.mark.unit
def test_structured_browser_url_is_safe_but_event_text_is_raw() -> None:
    evidence = BrowserEvidence()
    message = Mock(
        type="error",
        text="Failed at https://user:secret@example.invalid/orders?token=private#debug",
        location={"url": "https://user:secret@example.invalid/app?token=private"},
    )
    evidence._on_console(message)
    evidence._on_page_error(
        SimpleNamespace(
            name="Error at https://user:secret@example.invalid/fail?token=private#debug"
        )
    )  # type: ignore[arg-type]

    assert evidence.console_errors == [{"text": message.text, "url": "https://example.invalid/app"}]
    assert evidence.page_errors == [
        "Error at https://user:secret@example.invalid/fail?token=private#debug"
    ]


@pytest.mark.unit
def test_expected_http_error_is_scoped_and_counted() -> None:
    evidence = BrowserEvidence()
    evidence.expect_http_error("POST", "/api/orders", 503)
    evidence.error_responses.append(
        {"method": "POST", "url": "http://localhost/api/orders", "status": 503}
    )
    assert evidence.unexpected_errors() == []
    evidence.error_responses.append(
        {"method": "GET", "url": "http://localhost/api/unrelated", "status": 500}
    )
    assert "unrelated" in str(evidence.unexpected_errors())


@pytest.mark.unit
def test_expected_http_error_must_occur() -> None:
    evidence = BrowserEvidence()
    evidence.expect_http_error("POST", "/api/orders", 503)
    assert "observed 0" in str(evidence.unexpected_errors())


@pytest.mark.unit
def test_expected_http_error_must_be_registered_before_request() -> None:
    evidence = BrowserEvidence()
    evidence._started_requests.add(("POST", "/api/orders"))
    with pytest.raises(ValueError, match="before starting"):
        evidence.expect_http_error("POST", "/api/orders", 503)


@pytest.mark.unit
def test_extra_identical_http_error_is_not_suppressed() -> None:
    evidence = BrowserEvidence()
    evidence.expect_http_error("POST", "/api/orders", 503)
    event = {"method": "POST", "url": "http://localhost/api/orders", "status": 503}
    evidence.error_responses.extend((event.copy(), event.copy()))
    assert "observed 2" in str(evidence.unexpected_errors())
    assert "HTTP error" in str(evidence.unexpected_errors())


@pytest.mark.unit
def test_duplicate_expectations_require_explicit_count() -> None:
    evidence = BrowserEvidence()
    evidence.expect_http_error("POST", "/api/orders", 503)
    with pytest.raises(ValueError, match="use count"):
        evidence.expect_http_error("POST", "/api/orders", 503)


@pytest.mark.unit
def test_repeated_http_errors_require_each_expected_occurrence() -> None:
    evidence = BrowserEvidence()
    evidence.expect_http_error("POST", "/api/orders", 503, count=2)
    event = {"method": "POST", "url": "http://localhost/api/orders", "status": 503}
    evidence.error_responses.append(event.copy())

    assert "observed 1" in str(evidence.unexpected_errors())

    evidence.error_responses.append(event.copy())
    assert evidence.unexpected_errors() == []

    evidence.error_responses.append(event.copy())
    assert "observed 3" in str(evidence.unexpected_errors())
    assert "HTTP error" in str(evidence.unexpected_errors())
