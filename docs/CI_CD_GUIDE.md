# CI/CD Guide

## Workflow scope

`.github/workflows/quality.yml` defines validation, not deployment. It triggers
automatically for pushes to `main`, for pull requests, and through manual dispatch. It
does not publish packages, deploy infrastructure, create releases, modify repository
settings, or write back to the repository.

Restricting push execution to `main` avoids duplicate push and pull-request runs on
feature branches. Pull requests provide feature-branch validation, the `main` push
validates the integrated result, and manual dispatch preserves an explicit path for
branch validation when required. This is the intended long-term trigger strategy rather
than a temporary modernization exception.

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

The pins were reviewed against the official action repositories on 2026-07-26:

| Action | Pin |
|---|---|
| `actions/checkout` v7.0.1 | `3d3c42e5aac5ba805825da76410c181273ba90b1` |
| `astral-sh/setup-uv` v8.1.0 | `08807647e7069bb48b6ef5acd8ec9567f424441b` |
| `actions/cache` v6.1.0 | `55cc8345863c7cc4c66a329aec7e433d2d1c52a9` |
| `actions/upload-artifact` v7.0.1 | `043fb46d1a93c77aae656e7c1c64a875d1fc6a0a` |

`actions/checkout` moved from v7.0.0 to the compatible v7.0.1 patch release because
v7.0.1 supersedes the existing release and its exact commit was verified in the official
repository. The setup-uv, cache, and upload-artifact pins remain unchanged: their exact
commits are official and compatible with this workflow, and no requirement justifies
additional dependency churn. Pins should continue to be reviewed through official
release and security notices.

## Container runtime selection

The controlled database uses `postgres:17.10-bookworm`. PostgreSQL 17.10 is the current
supported patch release in the approved PostgreSQL 17 major line. The versioned Debian
Bookworm tag is published by the Docker Official Image for both AMD64 and ARM64, including
Apple Silicon hosts through Docker Desktop's Linux ARM64 runtime. The configuration does
not use `latest`, an unversioned tag, a beta release, or a different PostgreSQL major
version.

## Local parity

The CI service lifecycle is represented locally by:

```bash
uv sync --extra dev --locked --python 3.12
uv run playwright install chromium firefox webkit
docker compose config
docker compose build --no-cache
docker compose up --detach --wait
.venv/bin/python scripts/wait_for_services.py --timeout 30
```

Tests run from the host against `127.0.0.1:8000` and `127.0.0.1:5432` in both
environments. The app and database run inside Compose.

Local parity was demonstrated on Apple Silicon with Docker Desktop 4.83.0, Engine 29.6.2,
Compose 5.3.1, and PostgreSQL 17.10 Bookworm. The no-cache build, Compose health,
readiness, and safe shutdown passed. The workflow-equivalent test intent passed locally:

- 28 tests collected; Ruff, formatting, and Mypy passed
- 18 unit tests passed
- API 4, contract 1, database 1, and integration 1 passed independently
- 7 service cases passed with two workers
- focused Chromium UI 2 and full Chromium E2E 1 passed
- 3 smoke cases passed across Chromium, Firefox, and WebKit
- the failure-evidence bundle and exact-ID cleanup were demonstrated

## Hosted validation evidence

The workflow passed in both integration stages:

- Pull-request run
  [`30236883963`](https://github.com/wodud-khan/sdet-playwright-framework/actions/runs/30236883963)
  validated `bab0f08a59c6423e08c80fa38635cf217d93d6c4`.
- Post-merge `main` run
  [`30237237422`](https://github.com/wodud-khan/sdet-playwright-framework/actions/runs/30237237422)
  validated merge commit `0a2fbf927893ccacb56365214e8e5371c0434e39`.

In both runs, `static-and-unit` and `postgres-and-browser` passed. Each run uploaded
`unit-reports` and `service-browser-evidence`. The hosted results confirmed:

- 28-test collection, Ruff, formatting, Mypy, and 18 unit tests
- 7 serial service tests and the same 7 cases with two workers
- 3 Chromium UI/E2E tests
- 3 smoke cases across Chromium, Firefox, and WebKit, with 31 cases deselected
- Compose build, health, readiness, diagnostic capture, artifact upload, and shutdown

These results demonstrate the committed quality-validation workflow on GitHub-hosted
Ubuntu runners. They do not demonstrate deployment, release automation, package
publication, production operations, or infrastructure ownership. Local Docker evidence
and hosted workflow evidence remain distinct and are both recorded in
`FINAL_VALIDATION_REPORT.md`.

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
