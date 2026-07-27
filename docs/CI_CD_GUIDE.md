# CI/CD Guide

## Workflow scope

`.github/workflows/quality.yml` defines validation, not deployment. It triggers on pushes,
pull requests, and manual dispatch. It does not publish packages, deploy infrastructure,
create releases, modify repository settings, or write back to the repository.

The workflow has read-only repository permissions, disables persisted checkout
credentials, cancels superseded runs for the same ref, and applies explicit job timeouts.
Third-party actions are pinned to immutable commit SHAs with version comments.

## Job 1: static analysis and unit tests

`static-and-unit`:

1. Checks out the repository without persisted credentials.
2. Installs uv 0.11.8 and Python 3.12.
3. Restores a lock-keyed uv cache.
4. Runs the locked development sync and lock check.
5. Collects all tests.
6. Runs Ruff lint, Ruff format check, and Mypy.
7. Runs unit tests with two bounded workers.
8. Uploads HTML/JUnit output even after failure.

The commands match the local uv workflow.

## Job 2: PostgreSQL and browser tests

`postgres-and-browser` runs only after the first job passes:

1. Installs the same locked environment.
2. Restores a browser cache keyed by `uv.lock`.
3. Installs Chromium, Firefox, WebKit, and required runner libraries.
4. Builds and starts the same app/PostgreSQL Compose stack used locally.
5. Waits on Compose health and the bounded HTTP readiness probe.
6. Runs API, contract, database, and integration tests serially.
7. Repeats service intent with two workers to prove isolation.
8. Runs focused UI and full E2E coverage on Chromium.
9. Runs the smoke marker on Chromium, Firefox, and WebKit.
10. Always captures Compose state/logs, stops services, and uploads reports/evidence.

Artifacts are retained for 14 days. Hidden files are not included.

## Action pins

At the time the workflow was authored:

| Action | Pin |
|---|---|
| `actions/checkout` v7.0.0 | `9c091bb21b7c1c1d1991bb908d89e4e9dddfe3e0` |
| `astral-sh/setup-uv` v8.1.0 | `08807647e7069bb48b6ef5acd8ec9567f424441b` |
| `actions/cache` v6.1.0 | `55cc8345863c7cc4c66a329aec7e433d2d1c52a9` |
| `actions/upload-artifact` v7.0.1 | `043fb46d1a93c77aae656e7c1c64a875d1fc6a0a` |

Pins should be reviewed periodically through official release and security notices.

## Local parity

The CI service lifecycle is represented locally by:

```bash
uv sync --extra dev --locked --python 3.12
uv run playwright install chromium firefox webkit
docker compose up --detach --build --wait
.venv/bin/python scripts/wait_for_services.py --timeout 30
```

Tests run from the host against `127.0.0.1:8000` and `127.0.0.1:5432` in both
environments. The app and database run inside Compose.

## Current validation boundary

The workflow file parses locally and its non-Docker commands match locally validated
commands. It has not been pushed or executed. Therefore:

- do not claim a passing GitHub Actions pipeline
- do not use the workflow file as proof that the image builds
- do not use it as proof that PostgreSQL or the E2E path passes
- record the first hosted run ID, result, and retained artifacts in
  `FINAL_VALIDATION_REPORT.md` before changing those classifications

## Failure triage

Start with the earliest failed job and inspect:

- unit HTML/JUnit output for collection or isolated failures
- service/browser JUnit and HTML reports
- `compose-ps.txt` for health state
- `compose.log` for app and PostgreSQL startup/runtime errors
- Playwright trace, screenshot, video, and structured browser JSON
- body-free API exchange JSON

Do not add retries to turn a red workflow green. Follow
[FLAKY_TEST_POLICY.md](FLAKY_TEST_POLICY.md).
