"""Unit tests for runtime configuration validation."""

from __future__ import annotations

import pytest

from test_framework.config import Settings


@pytest.mark.unit
def test_settings_use_safe_local_defaults(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("APP_BASE_URL", raising=False)
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.delenv("API_TIMEOUT_SECONDS", raising=False)
    monkeypatch.delenv("ARTIFACTS_DIR", raising=False)
    monkeypatch.delenv("TEST_RUN_ID", raising=False)

    settings = Settings.from_environment()

    assert settings.app_base_url == ""
    assert settings.database_url == (
        "postgresql://portfolio:local-demo-password@127.0.0.1:5432/portfolio"
    )
    assert settings.api_timeout_seconds == 5
    assert settings.test_run_id == "local"


@pytest.mark.unit
@pytest.mark.parametrize(
    ("variable", "value", "message"),
    [
        ("APP_BASE_URL", "localhost:8000", "absolute HTTP"),
        ("API_TIMEOUT_SECONDS", "0", "greater than zero"),
        ("TEST_RUN_ID", " ", "must not be empty"),
    ],
)
def test_settings_reject_invalid_values(
    monkeypatch: pytest.MonkeyPatch,
    variable: str,
    value: str,
    message: str,
) -> None:
    monkeypatch.setenv(variable, value)

    with pytest.raises(ValueError, match=message):
        Settings.from_environment()
