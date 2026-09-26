"""Exercise ownership cleanup across a real failed browser test."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from test_framework.config import Settings
from test_framework.db.client import PostgresOrderClient


@pytest.mark.e2e
def test_ui_created_order_is_removed_after_result_assertion_fails(
    tmp_path: Path, service_settings: Settings, postgres_client: PostgresOrderClient
) -> None:
    child = tmp_path / "test_created_then_failed.py"
    order_id_file = tmp_path / "owned-id.txt"
    child.write_text(
        """
import os
from pathlib import Path
from test_framework.pages.order_page import OrderPage

def test_created_then_failed(page, service_settings, order_factory, order_manager, postgres_client):
    payload = order_factory.build()
    order_page = OrderPage(page, service_settings.app_base_url)
    order_page.open()
    status, body = order_page.submit_order(payload.customer_name, payload.item_name, 1)
    order_id = str(body['id'])
    order_manager.register_owned(order_id)
    assert status == 201
    assert postgres_client.order_exists(order_id)
    Path(os.environ['ORDER_ID_FILE']).write_text(order_id, encoding='utf-8')
    order_page.expect_order_saved(order_id, 1)
""",
        encoding="utf-8",
    )
    artifacts = tmp_path / "artifacts"
    native = tmp_path / "playwright"
    env = {
        **os.environ,
        "ORDER_ID_FILE": str(order_id_file),
        "ARTIFACTS_DIR": str(artifacts),
        "TEST_RUN_ID": "failure-cleanup-drill",
    }
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
            "--tracing",
            "retain-on-failure",
            "--screenshot",
            "only-on-failure",
            "--video",
            "retain-on-failure",
            "--output",
            str(native),
        ],
        cwd=Path(__file__).resolve().parents[2],
        env=env,
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    assert order_id_file.exists(), result.stdout + result.stderr
    order_id = order_id_file.read_text(encoding="utf-8")
    assert result.returncode == 1, result.stdout + result.stderr
    assert "$0.01" in result.stdout
    assert not postgres_client.order_exists(order_id)
    evidence_files = list(artifacts.rglob("*.json"))
    assert len(evidence_files) == 2
    api_evidence = next(path for path in evidence_files if path.parent.name == "api")
    exchanges = json.loads(api_evidence.read_text(encoding="utf-8"))["exchanges"]
    assert any(exchange["url"].endswith(f"/orders/{order_id}") for exchange in exchanges)
    assert {path.suffix for path in native.rglob("*") if path.is_file()} >= {
        ".zip",
        ".png",
        ".webm",
    }
