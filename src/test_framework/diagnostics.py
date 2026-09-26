"""Custom browser and API evidence helpers."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from hashlib import sha256
from pathlib import Path
from urllib.parse import urlsplit
from uuid import uuid4

from playwright.sync_api import ConsoleMessage, Error, Page, Request, Response

from test_framework.api.client import safe_url


def safe_test_name(node_id: str) -> str:
    """Create a bounded filename from a Pytest node ID."""
    normalized = re.sub(r"[^a-zA-Z0-9_.-]+", "-", node_id).strip("-")
    digest = sha256(node_id.encode()).hexdigest()[:10]
    return f"{normalized[:150] or 'unknown-test'}-{digest}"


def evidence_path(root: Path, run_id: str, kind: str, node_id: str) -> Path:
    return (
        root / safe_test_name(run_id) / kind / f"{safe_test_name(node_id)}-{uuid4().hex[:8]}.json"
    )


def write_json_evidence(path: Path, payload: dict[str, object]) -> None:
    """Write structured evidence beneath an already configured artifact root."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True),
        encoding="utf-8",
    )


@dataclass
class BrowserEvidence:
    """Browser events useful for diagnosing a failed test."""

    console_errors: list[dict[str, str]] = field(default_factory=list)
    page_errors: list[str] = field(default_factory=list)
    failed_requests: list[dict[str, object]] = field(default_factory=list)
    error_responses: list[dict[str, object]] = field(default_factory=list)
    expected_http_errors: list[dict[str, object]] = field(default_factory=list)
    _started_requests: set[tuple[str, str]] = field(default_factory=set, repr=False)

    def expect_http_error(self, method: str, path: str, status: int, count: int = 1) -> None:
        if not path.startswith("/") or count < 1:
            raise ValueError("Expected HTTP errors require an exact path and positive count")
        if (method, path) in self._started_requests:
            raise ValueError("Register an expected HTTP error before starting its request")
        if any(
            expected["method"] == method
            and expected["path"] == path
            and expected["status"] == status
            for expected in self.expected_http_errors
        ):
            raise ValueError("Duplicate HTTP error expectation; use count for repeated responses")
        self.expected_http_errors.append(
            {"method": method, "path": path, "status": status, "count": count}
        )

    def unexpected_errors(self) -> list[str]:
        errors = [f"page error: {error}" for error in self.page_errors]
        errors += [f"request failure: {event}" for event in self.failed_requests]
        matched_indices: set[int] = set()
        for expected in self.expected_http_errors:
            events = [
                index
                for index, event in enumerate(self.error_responses)
                if event["method"] == expected["method"]
                and urlsplit(str(event["url"])).path == expected["path"]
                and event["status"] == expected["status"]
            ]
            if len(events) != expected["count"]:
                errors.append(f"expected HTTP {expected}, observed {len(events)}")
            count = expected["count"]
            assert isinstance(count, int)
            matched_indices.update(events[:count])
        errors += [
            f"HTTP error: {event}"
            for index, event in enumerate(self.error_responses)
            if index not in matched_indices
        ]
        for event in self.console_errors:
            if not any(
                self._matches_console(event, expected) for expected in self.expected_http_errors
            ):
                errors.append(f"console error: {event['text']}")
        return errors

    @staticmethod
    def _matches_console(event: dict[str, str], expected: dict[str, object]) -> bool:
        return (
            urlsplit(event["url"]).path == expected["path"]
            and f"{expected['status']}" in event["text"]
            and "Failed to load resource" in event["text"]
        )

    def attach(self, page: Page) -> None:
        page.on("request", self._on_request)
        page.on("console", self._on_console)
        page.on("pageerror", self._on_page_error)
        page.on("requestfailed", self._on_request_failed)
        page.on("response", self._on_response)

    def as_dict(self) -> dict[str, object]:
        return {
            "console_errors": self.console_errors,
            "page_errors": self.page_errors,
            "failed_requests": self.failed_requests,
            "error_responses": self.error_responses,
            "expected_http_errors": self.expected_http_errors,
        }

    def _on_console(self, message: ConsoleMessage) -> None:
        if message.type == "error":
            self.console_errors.append(
                {"text": message.text, "url": safe_url(message.location.get("url", ""))}
            )

    def _on_request(self, request: Request) -> None:
        self._started_requests.add((request.method, urlsplit(request.url).path))

    def _on_page_error(self, error: Error) -> None:
        self.page_errors.append(error.name or "Error")

    def _on_request_failed(self, request: Request) -> None:
        self.failed_requests.append(
            {
                "method": request.method,
                "url": safe_url(request.url),
                "failure": "request failed",
            }
        )

    def _on_response(self, response: Response) -> None:
        if response.status >= 400:
            self.error_responses.append(
                {
                    "method": response.request.method,
                    "url": safe_url(response.url),
                    "status": response.status,
                }
            )
