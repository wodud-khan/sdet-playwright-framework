# Historical Validation Report

Report date: 2026-07-27

This report records the repository and environment validated on that date. Its local
and hosted results do not validate later working-tree changes. Use the current
[README](../README.md) for present-day commands and results.

## Executive summary

The repository has been selectively rebuilt into a focused Python/Pytest/Playwright
quality-engineering portfolio while preserving Git history and repository identity. The
baseline's third-party tests, decorative Jenkins/Kubernetes/Allure paths, blanket
retries, and unsupported claims were removed or replaced.

The primary local runtime is demonstrated. The non-root application image built without
cache, the official PostgreSQL 17.10 Bookworm image started healthy, and every unit,
API, contract, direct-database, integration, Chromium UI, full E2E, bounded-parallel,
and three-browser smoke command passed against the controlled stack.

Exact-ID cleanup was proven after a deliberate intermediate assertion failure. A
separate PostgreSQL-backed Chromium failure drill produced the complete diagnostic
bundle and was privacy-audited. Both temporary failing tests were removed, the committed
E2E passed again, the orders table contained zero rows, the containers were stopped, and
the named PostgreSQL volume was retained.

GitHub Actions then passed twice: once for pull request #1 and once for the merge commit
on `main`. Both hosted runs completed static/unit and PostgreSQL/browser jobs, uploaded
the expected artifacts, stopped their Compose stacks, and produced no failure, error,
or warning annotations.

## Reproducibility and privacy scope

- Git history and repository identity were preserved.
- Locked Python dependencies, Dockerfile, Compose configuration, and the official
  PostgreSQL image define the reproducible runtime.
- Local configuration, private-note patterns, reports, logs, browser evidence, caches,
  virtual environments, and local databases are excluded by Git and Docker-context
  safeguards.
- Local failure evidence and both hosted artifact sets were scanned for credentials,
  private request data, personal paths, and local-only material.
- Kubernetes, Jenkins, Allure, public demo sites, blanket retries, deployment, and
  production-operations claims remain outside the focused scope.

## Validation environment

| Item | Observed value |
|---|---|
| uv | 0.11.8 |
| Project Python | 3.12.11 |
| Locked development packages | 49 installed; lock check passed |
| Playwright | 1.61.0 with Chromium, Firefox, and WebKit |
| Local container architecture | Linux ARM64 |
| Hosted runner | GitHub-hosted Ubuntu |
| PostgreSQL image | `postgres:17.10-bookworm` |
| PostgreSQL server | 17.10, Debian `17.10-1.pgdg12+1` |
| PostgreSQL image digest | `sha256:4f736ae292687621d4dbe0d499ffd024a36bd2ee7d8ca6f2ccd4c800f047b394` |
| Application image | Non-root user `portfolio` |

Local Docker engine, Compose, information, and `hello-world` checks passed before stack
validation. The hosted workflow independently exercised the committed Linux build and
Compose lifecycle on GitHub runners.

## Build and Compose results

Ports 5432 and 8000 were available, so no overrides were required.

```bash
docker compose config
docker compose build --no-cache
docker compose up --detach --wait
docker compose ps
.venv/bin/python scripts/wait_for_services.py --timeout 30
curl --fail --silent http://127.0.0.1:8000/health
```

Results:

- Compose configuration rendered successfully.
- The no-cache application build passed.
- PostgreSQL and the application both became healthy.
- The readiness probe passed.
- `/health` returned `{"status":"ok","database":"ok"}`.
- PostgreSQL reported 17.10 on `aarch64-unknown-linux-gnu`.
- Startup and runtime logs contained no unexpected startup, health, permission, schema,
  secret, or private-path errors.
- The normal PostgreSQL initialization shutdown/restart sequence was expected.

Final cleanup used:

```bash
docker compose logs --no-color
docker compose down
```

At the end of that run, the project containers and network were stopped. The named volume
`sdet-playwright-framework_portfolio_database` was retained; `down -v` was not used.

## Primary test results

The primary environment was:

```bash
export APP_BASE_URL=http://127.0.0.1:8000
export DATABASE_URL=postgresql://portfolio:local-demo-password@127.0.0.1:5432/portfolio
export API_TIMEOUT_SECONDS=5
export ARTIFACTS_DIR=artifacts
export TEST_RUN_ID=local-docker-validation
```

No primary command used `--allow-sqlite-ui-fallback`.

| Layer or gate | Command summary | Result |
|---|---|---|
| Collection | `pytest --collect-only -q` | 28 collected |
| Ruff lint | `ruff check .` | Passed |
| Ruff format | `ruff format --check .` | 44 files formatted |
| Mypy | `mypy src scripts` | 18 source files clean |
| Unit | `pytest tests/unit -q` | 18 passed |
| API | `pytest tests/api -q` | 4 passed |
| Contract | `pytest tests/contract -q` | 1 passed |
| Direct PostgreSQL | `pytest tests/database -q` | 1 passed |
| API/PostgreSQL integration | `pytest tests/integration -q` | 1 passed |
| Focused Chromium UI | `pytest tests/ui --browser chromium -q` | 2 passed |
| Full Chromium E2E | `pytest tests/e2e --browser chromium -q` | 1 passed |
| Two-worker service intent | service marker expression with `-n 2` | 7 passed |
| Two-worker Chromium UI | `pytest tests/ui -n 2 --browser chromium -q` | 2 passed |
| Three-browser smoke | Chromium, Firefox, WebKit | 3 passed, 31 deselected |
| Post-drill E2E restoration | committed Chromium E2E | 1 passed |

## Hosted GitHub Actions evidence

Pull-request validation:

- Run: [`30236883963`](https://github.com/wodud-khan/sdet-playwright-framework/actions/runs/30236883963)
- Validated commit: `bab0f08a59c6423e08c80fa38635cf217d93d6c4`
- `static-and-unit`: passed
- `postgres-and-browser`: passed
- Artifacts: `unit-reports`, `service-browser-evidence`

Post-merge `main` validation:

- Run: [`30237237422`](https://github.com/wodud-khan/sdet-playwright-framework/actions/runs/30237237422)
- Merge commit: `0a2fbf927893ccacb56365214e8e5371c0434e39`
- `static-and-unit`: passed
- `postgres-and-browser`: passed
- Artifacts: `unit-reports`, `service-browser-evidence`

The `main` run reproduced the expected summaries:

- 28 tests collected
- Ruff lint and formatting passed; Mypy found no issues in 18 source files
- 18 unit tests passed
- 7 serial service tests passed
- 7 service tests passed with two workers
- 3 Chromium UI/E2E tests passed
- 3 Chromium/Firefox/WebKit smoke cases passed, with 31 deselected
- Compose build, health, readiness, diagnostics, artifact upload, and shutdown passed

Neither run produced a failure, error, or warning annotation. The downloaded artifact
sets contained only the expected HTML/JUnit reports and Compose state/log files. A
content scan found no credentials, personal paths or identities, private local material,
authorization/cookie/session data, environment secrets, or request-body literals. The
temporary audit copies were deleted; hosted artifacts were retained.

## Data isolation and cleanup proof

Implementation review confirmed:

- every payload combines the run ID, xdist worker ID, and a random UUID suffix
- the manager records only order IDs owned by the current test
- cleanup calls the public API for each exact ID and verifies a `404`
- direct SQL deletion is scoped by `WHERE id = ?`
- no table-wide `DELETE`, `TRUNCATE`, wildcard, drop-table, or global cleanup exists

The committed E2E demonstrated:

1. create through the UI
2. validate the returned JSON contract
3. read the exact order through the API
4. verify exact values directly in PostgreSQL
5. delete through the API
6. prove PostgreSQL absence

A temporary two-test drill created and directly verified one order, intentionally failed,
then allowed fixture teardown to run. The following test checked that same captured ID
and passed because it was absent: one expected failure and one cleanup-proof pass. The
table count was zero afterward. The temporary test was removed and never committed.

## PostgreSQL-backed failure evidence

A separate temporary Chromium test:

1. created an order through the API manager
2. verified its presence directly in PostgreSQL
3. opened the live UI
4. intentionally asserted a nonexistent heading

The expected single failure retained:

- Playwright trace archive
- failure screenshot
- video
- browser console/page/failed-request/error-response JSON
- body-free API method/URL/status/duration JSON
- self-contained HTML report
- JUnit XML report
- application log
- PostgreSQL log
- combined Compose log and Compose state

Fixture teardown deleted the exact order and verified API absence. The PostgreSQL table
count was zero. The temporary test was removed, and the committed E2E passed afterward.

The evidence retained for that run was scanned directly, including decompressed trace
contents. The scan found no authorization headers, cookies, request bodies with private data,
environment-variable dumps, local-only Markdown, passwords, or personal Mac paths.
Playwright trace stack metadata initially contained absolute repository paths; those
metadata strings were replaced with `<repository>`, the archive was rebuilt, and
`unzip -t` plus a second privacy scan passed.

## CI evidence boundary

The workflow uses read-only permissions, non-persisted checkout credentials, bounded
timeouts, concurrency cancellation, exact action SHAs, locked dependencies, and the
same Compose/test commands demonstrated locally. The two successful hosted runs prove
quality-gate execution, runner setup, container lifecycle, test behavior, and artifact
upload for the validated commits.

The workflow does not deploy an application, publish a package, create a release, or
operate production infrastructure. A passing quality workflow is not evidence of those
capabilities.

## Known limitations

- Positive order schema coverage only; a dedicated error-response schema is deferred
- App startup initializes the small schema directly; migration tooling is outside scope
- No authentication, cloud, performance, security, accessibility, or visual-regression
  program
- Hosted CI performs quality validation only; deployment and production operations are
  outside scope
- Local container validation exercised ARM64 and hosted validation exercised the GitHub
  Ubuntu environment; no broader platform matrix is claimed

## Completion decision

Status: **local and hosted quality validation demonstrated**.

The demonstrated evidence covers the controlled application, PostgreSQL integration,
layered test architecture, exact cleanup, bounded parallelism, three-browser smoke,
failure diagnostics, Compose lifecycle, and GitHub-hosted quality workflow. It does not
claim production readiness, deployment, enterprise scale, or zero flakiness.
