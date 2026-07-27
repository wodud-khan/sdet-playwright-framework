"""Typed synchronous API client with safe exchange metadata."""

from __future__ import annotations

from dataclasses import dataclass
from time import monotonic
from typing import Any

import requests


@dataclass(frozen=True, slots=True)
class ApiExchange:
    """Non-sensitive metadata retained for failure evidence."""

    method: str
    url: str
    status_code: int
    elapsed_milliseconds: int


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
        response = self.session.request(
            method,
            url,
            timeout=self.timeout_seconds,
            **kwargs,
        )
        elapsed = round((monotonic() - started) * 1000)
        self._exchanges.append(
            ApiExchange(
                method=method,
                url=response.url,
                status_code=response.status_code,
                elapsed_milliseconds=elapsed,
            )
        )
        return response
