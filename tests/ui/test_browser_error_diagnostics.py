"""Prove expected HTTP events do not hide unrelated browser errors."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from test_framework.config import Settings


@pytest.mark.ui
def test_unexpected_browser_error_still_fails(tmp_path: Path, ui_settings: Settings) -> None:
    child = tmp_path / "test_unexpected_browser_error.py"
    child.write_text(
        """
from playwright.sync_api import expect
from test_framework.pages.order_page import OrderPage

def test_error_events(page, ui_settings, browser_evidence):
    order_page = OrderPage(page, ui_settings.app_base_url)
    order_page.open()
    page.route('**/api/orders', lambda route: route.fulfill(
        status=503, content_type='application/json', body='{"detail":"Try again later"}'))
    browser_evidence.expect_http_error('POST', '/api/orders', 503)
    order_page.customer_name.fill('Ada Lovelace')
    order_page.item_name.fill('Quality Notebook')
    order_page.quantity.fill('1')
    order_page.submit.click()
    expect(order_page.form_status).to_have_text('Order could not be created: Try again later')
    page.goto(ui_settings.app_base_url + '/unexpected-missing-page')
""",
        encoding="utf-8",
    )
    artifacts = tmp_path / "artifacts"
    env = {**os.environ, "ARTIFACTS_DIR": str(artifacts), "TEST_RUN_ID": "error-drill"}
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "-p",
            "conftest",
            str(child),
            "-q",
            "--browser",
            "chromium",
            "--allow-sqlite-ui-fallback",
            "--tracing",
            "retain-on-failure",
            "--screenshot",
            "only-on-failure",
            "--video",
            "retain-on-failure",
            "--output",
            str(tmp_path / "playwright"),
        ],
        cwd=Path(__file__).resolve().parents[2],
        env=env,
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    assert result.returncode == 1, result.stdout + result.stderr
    assert "Unexpected browser errors" in result.stdout
    evidence_files = list(artifacts.rglob("*.json"))
    assert len(evidence_files) == 1
    evidence = json.loads(evidence_files[0].read_text(encoding="utf-8"))
    assert {event["status"] for event in evidence["error_responses"]} == {503, 404}
    assert not [
        path
        for path in (tmp_path / "playwright").rglob("*")
        if path.suffix in {".zip", ".png", ".webm"}
    ]
