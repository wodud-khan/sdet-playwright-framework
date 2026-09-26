"""Typed synchronous API client with structured exchange metadata."""

from __future__ import annotations

from dataclasses import dataclass
from time import monotonic
from typing import Any
from urllib.parse import urlsplit, urlunsplit

import requests


@dataclass(frozen=True, slots=True)
class ApiExchange:
    """Structured request metadata retained for failure evidence."""

    method: str
    url: str
    status_code: int | None
    elapsed_milliseconds: int
    error_category: str | None = None


def safe_url(url: str) -> str:
    """Retain only scheme, host, port, and path in custom evidence."""
    try:
        parsed = urlsplit(url)
        host = parsed.hostname or ""
        if ":" in host:
            host = f"[{host}]"
        if parsed.port is not None:
            host = f"{host}:{parsed.port}"
        return urlunsplit((parsed.scheme, host, parsed.path, "", ""))
    except ValueError:
        return "<invalid URL>"


class ApiClient:
    """Manage one Requests session and explicit timeout for the demo API."""

    def __init__(self, base_url: str, timeout_seconds: float) -> None:
        if not base_url.startswith(("http://", "https://")):
            raise ValueError("API base URL must be absolute")
        if timeout_seconds <= 0:
            raise ValueError("API timeout must be greater than zero")

        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = timeout_seconds
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
        )
        self._exchanges: list[ApiExchange] = []

    @property
    def exchanges(self) -> tuple[ApiExchange, ...]:
        """Return immutable, body-free request metadata."""
        return tuple(self._exchanges)

    def get(self, endpoint: str) -> requests.Response:
        return self._request("GET", endpoint)

    def post(self, endpoint: str, payload: dict[str, object]) -> requests.Response:
        return self._request("POST", endpoint, json=payload)

    def delete(self, endpoint: str) -> requests.Response:
        return self._request("DELETE", endpoint)

    def close(self) -> None:
        """Close pooled HTTP connections deterministically."""
        self.session.close()

    def _request(
        self,
        method: str,
        endpoint: str,
        **kwargs: Any,
    ) -> requests.Response:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        started = monotonic()
        try:
            response = self.session.request(
                method,
                url,
                timeout=self.timeout_seconds,
                **kwargs,
            )
        except requests.RequestException as error:
            self._exchanges.append(
                ApiExchange(
                    method,
                    safe_url(url),
                    None,
                    round((monotonic() - started) * 1000),
                    type(error).__name__,
                )
            )
            raise
        elapsed = round((monotonic() - started) * 1000)
        self._exchanges.append(
            ApiExchange(
                method=method,
                url=safe_url(response.url),
                status_code=response.status_code,
                elapsed_milliseconds=elapsed,
            )
        )
        return response
