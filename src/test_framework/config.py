"""Validated runtime configuration shared by test layers."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse


def _validated_http_url(value: str, variable_name: str) -> str:
    normalized = value.rstrip("/")
    if not normalized:
        return ""

    parsed = urlparse(normalized)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError(f"{variable_name} must be an absolute HTTP(S) URL")
    return normalized


@dataclass(frozen=True, slots=True)
class Settings:
    """Immutable configuration with safe local defaults."""

    app_base_url: str
    database_url: str
    api_timeout_seconds: float
    artifacts_dir: Path
    test_run_id: str

    @property
    def api_base_url(self) -> str:
        """Return the demo application's API root."""
        return f"{self.app_base_url}/api" if self.app_base_url else ""

    @classmethod
    def from_environment(cls) -> Settings:
        """Build settings from environment variables and fail early on invalid input."""
        app_base_url = _validated_http_url(os.getenv("APP_BASE_URL", ""), "APP_BASE_URL")
        database_url = os.getenv(
            "DATABASE_URL",
            "postgresql://portfolio:local-demo-password@127.0.0.1:5432/portfolio",
        )
        timeout = float(os.getenv("API_TIMEOUT_SECONDS", "5"))
        if timeout <= 0:
            raise ValueError("API_TIMEOUT_SECONDS must be greater than zero")

        artifacts_dir = Path(os.getenv("ARTIFACTS_DIR", "artifacts"))
        test_run_id = os.getenv("TEST_RUN_ID", "local")
        if not test_run_id.strip():
            raise ValueError("TEST_RUN_ID must not be empty")

        return cls(
            app_base_url=app_base_url,
            database_url=database_url,
            api_timeout_seconds=timeout,
            artifacts_dir=artifacts_dir,
            test_run_id=test_run_id,
        )
