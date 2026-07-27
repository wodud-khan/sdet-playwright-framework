"""Redacted browser and API evidence helpers."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

from playwright.sync_api import ConsoleMessage, Error, Page, Request, Response


def safe_test_name(node_id: str) -> str:
    """Create a bounded filename from a Pytest node ID."""
    normalized = re.sub(r"[^a-zA-Z0-9_.-]+", "-", node_id).strip("-")
    return normalized[:180] or "unknown-test"


def write_json_evidence(path: Path, payload: dict[str, object]) -> None:
    """Write structured evidence beneath an already configured artifact root."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True),
        encoding="utf-8",
    )


@dataclass
class BrowserEvidence:
    """Body-free browser events useful for diagnosing a failed test."""

    console_errors: list[str] = field(default_factory=list)
    page_errors: list[str] = field(default_factory=list)
    failed_requests: list[dict[str, object]] = field(default_factory=list)
    error_responses: list[dict[str, object]] = field(default_factory=list)

    def attach(self, page: Page) -> None:
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
        }

    def _on_console(self, message: ConsoleMessage) -> None:
        if message.type == "error":
            self.console_errors.append(message.text)

    def _on_page_error(self, error: Error) -> None:
        self.page_errors.append(str(error))

    def _on_request_failed(self, request: Request) -> None:
        self.failed_requests.append(
            {
                "method": request.method,
                "url": request.url,
                "failure": request.failure,
            }
        )

    def _on_response(self, response: Response) -> None:
        if response.status >= 400:
            self.error_responses.append(
                {
                    "method": response.request.method,
                    "url": response.url,
                    "status": response.status,
                }
            )
