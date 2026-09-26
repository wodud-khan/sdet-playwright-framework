"""Verify evidence after pytest setup, call, and teardown reporting."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest


@pytest.mark.unit
def test_api_evidence_lifecycle_and_session_closure(tmp_path: Path) -> None:
    child = tmp_path / "test_lifecycle_child.py"
    child.write_text(
        """
from pathlib import Path
import os
import pytest
import conftest
import requests

@pytest.fixture
def setup_failure(api_client):
    raise RuntimeError('setup sentinel')

def test_setup_failure(setup_failure):
    pass

def test_teardown_failure(order_manager, api_client):
    order_manager.register_owned('owned')
    def failed_delete(method, url, **kwargs):
        response = requests.Response()
        response.status_code = 500
        response._content = b'{"detail":"test error"}'
        response.url = url
        return response
    api_client.session.request = failed_delete

def test_writer_failure_keeps_original_and_closes_session(api_client):
    def close():
        Path(os.environ['CLOSED_FILE']).write_text('closed', encoding='utf-8')
    api_client.session.close = close
    def broken_writer(path, payload):
        raise OSError('writer sentinel')
    conftest.write_json_evidence = broken_writer
    raise AssertionError('original sentinel')
""",
        encoding="utf-8",
    )
    artifacts = tmp_path / "artifacts"
    closed_file = tmp_path / "closed.txt"
    env = {
        **os.environ,
        "APP_BASE_URL": "http://127.0.0.1:8000",
        "ARTIFACTS_DIR": str(artifacts),
        "TEST_RUN_ID": "lifecycle",
        "CLOSED_FILE": str(closed_file),
    }
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-p", "conftest", str(child), "-q"],
        cwd=Path(__file__).resolve().parents[2],
        env=env,
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    assert result.returncode == 1, result.stdout + result.stderr
    assert "setup sentinel" in result.stdout
    assert "Order cleanup failed" in result.stdout
    assert "original sentinel" in result.stdout
    assert "writer sentinel" in result.stdout
    assert closed_file.exists(), result.stdout + result.stderr
    assert closed_file.read_text(encoding="utf-8") == "closed"
    evidence_files = list(artifacts.rglob("*.json"))
    assert len(evidence_files) == 2
    assert any('"status_code": 500' in path.read_text(encoding="utf-8") for path in evidence_files)
