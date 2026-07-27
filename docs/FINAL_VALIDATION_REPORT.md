# Final Validation Report

Report date: 2026-07-26

## Executive summary

The repository has been selectively rebuilt into a focused Python/Pytest/Playwright
quality-engineering portfolio while preserving Git history and repository identity. The
baseline's third-party tests, decorative Jenkins/Kubernetes/Allure paths, blanket
retries, and unsupported claims were removed or replaced.

The primary local runtime is now demonstrated. An official Apple Silicon Docker Desktop
installation built the non-root application image without cache, pulled PostgreSQL
17.10 Bookworm for ARM64, started both services to healthy state, and supported every
unit, API, contract, direct-database, integration, Chromium UI, full E2E, bounded
parallel, and three-browser smoke command required by the validation plan.

Exact-ID cleanup was proven after a deliberate intermediate assertion failure. A
separate PostgreSQL-backed Chromium failure drill produced the complete diagnostic
bundle and was privacy-audited. Both temporary failing tests were removed, the committed
E2E passed again, the orders table contained zero rows, the containers were stopped, and
the named PostgreSQL volume was retained.

The only major execution boundary left is hosted GitHub Actions. The workflow is
committed and locally aligned, but it has not been pushed or run; this report does not
claim hosted CI success.

## Safety and scope record

- Workspace: local `sdet-playwright-framework` repository
- Branch: `refactor/sdet-framework-modernization`
- Baseline tag and original candidate HEAD: `sdet-portfolio-baseline-v1` / `24cb706`
- Retained safety stash:
  `SDET framework modernization candidate before PostgreSQL reconciliation`
- Publication: no push, merge, pull request, release, repository rename, or settings
  change
- Docker scope: official Docker Desktop only; no alternate runtime, account, sign-in,
  subscription, cloud service, storage relocation, internal-settings edit, or symlink
- Privacy: local `*.local.md` files remained ignored and excluded from Git, Docker
  context, retained reports, and public documentation

## Validation environment

| Item | Observed value |
|---|---|
| Host | macOS 15.7.4, Apple Silicon ARM64 |
| uv | 0.11.8 |
| Project Python | 3.12.11 |
| Locked development packages | 49 installed; lock check passed |
| Playwright | 1.61.0 with Chromium, Firefox, and WebKit |
| Docker Desktop | 4.83.0, build 234302 |
| Docker Engine | 29.6.2, Linux ARM64 |
| Docker Compose | 5.3.1 |
| PostgreSQL image | `postgres:17.10-bookworm` |
| PostgreSQL server | 17.10, Debian `17.10-1.pgdg12+1` |
| PostgreSQL image digest | `sha256:4f736ae292687621d4dbe0d499ffd024a36bd2ee7d8ca6f2ccd4c800f047b394` |
| Application image | Linux ARM64, configured user `portfolio` |

`docker version`, `docker compose version`, `docker info`, and
`docker run --rm hello-world` all passed. The `hello-world` pull selected ARM64.

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

The project containers and network are stopped. The named volume
`sdet-playwright-framework_portfolio_database` remains present; `down -v` was not used.

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

The retained evidence was scanned directly, including decompressed trace contents. It
contains no authorization headers, cookies, request bodies with private data,
environment-variable dumps, local-only Markdown, passwords, or personal Mac paths.
Playwright trace stack metadata initially contained absolute repository paths; those
metadata strings were replaced with `<repository>`, the archive was rebuilt, and
`unzip -t` plus a second privacy scan passed.

## Capability classification

| Major capability | Classification | Evidence |
|---|---|---|
| Python 3.12 locked uv workflow | Implemented and demonstrated | Sync, lock, collection, and tools passed |
| Pytest discovery and markers | Implemented and demonstrated | 28 tests collected |
| Ruff and Mypy gates | Implemented and demonstrated | All static gates passed |
| Isolated unit tests | Implemented and demonstrated | 18 passed |
| Controlled FastAPI/PostgreSQL app | Implemented and demonstrated | Build, health, readiness, and logs passed |
| REST API suite | Implemented and demonstrated | 4 passed |
| JSON contract suite | Implemented and demonstrated | 1 passed |
| Direct PostgreSQL suite | Implemented and demonstrated | 1 passed |
| API/database integration | Implemented and demonstrated | 1 passed |
| Focused Playwright UI | Implemented and demonstrated | 2 Chromium cases passed |
| UI/API/PostgreSQL E2E | Implemented and demonstrated | Full workflow and restoration runs passed |
| Unique run/worker data | Implemented and demonstrated | Serial/parallel runs and source review |
| Exact targeted cleanup | Implemented and demonstrated | E2E and intentional-failure absence proofs |
| Bounded parallelism | Implemented and demonstrated | 7 service and 2 UI cases passed with two workers |
| Three-browser smoke | Implemented and demonstrated | Chromium, Firefox, WebKit passed on primary stack |
| Failure evidence and reports | Implemented and demonstrated | Complete privacy-audited bundle retained locally |
| Compose stack and non-root app image | Implemented and demonstrated | No-cache build and healthy lifecycle passed |
| GitHub Actions quality pipeline | Implemented; hosted run not executed | Exact workflow pins reviewed; no hosted run |
| Kubernetes/Jenkins/Allure primary paths | Removed | Outside focused portfolio scope |

## CI validation boundary

The workflow uses read-only permissions, non-persisted checkout credentials, bounded
timeouts, concurrency cancellation, exact action SHAs, the same locked dependencies, and
the same Compose/test commands demonstrated locally.

Local Docker success proves the committed build and service lifecycle on this Mac. It
does not prove GitHub-hosted runner behavior, action execution, caching, or artifact
upload. Do not claim a passing GitHub Actions pipeline until an authorized hosted run
passes and its run ID and artifacts are recorded here.

## Known limitations

- No GitHub-hosted workflow result or uploaded CI artifact
- Positive order schema coverage only; a dedicated error-response schema is deferred
- App startup initializes the small schema directly; migration tooling is outside scope
- No authentication, cloud, performance, security, accessibility, or visual-regression
  program
- Docker validation was performed on Apple Silicon; the official PostgreSQL tag is
  multi-architecture, but this run does not independently test an AMD64 host

## Meaningful local commit history

The modernization uses coherent Conventional Commits:

1. `docs: record repository audit and modernization strategy`
2. `refactor: remove unsupported legacy framework components`
3. `chore: establish reproducible Python project configuration`
4. `feat: add controlled order application foundation`
5. `chore: define PostgreSQL Compose configuration`
6. `test: add PostgreSQL service-layer coverage`
7. `test: add Playwright UI workflow and failure diagnostics`
8. `ci: add reproducible GitHub Actions quality pipeline`
9. `docs: document architecture execution and portfolio evidence`
10. `chore: update container and workflow validation dependencies`

No commit was pushed.

## Final pre-push checklist

- [x] Official Docker Desktop installation and runtime checks passed.
- [x] Compose config, no-cache build, startup, health, logs, and shutdown passed.
- [x] API, contract, database, integration, UI, and E2E suites passed independently.
- [x] Full UI-to-API-to-PostgreSQL cleanup was proven.
- [x] Intentional-failure teardown deleted only its exact owned ID.
- [x] Two-worker PostgreSQL service and focused UI execution passed.
- [x] Three-browser smoke passed against the PostgreSQL stack.
- [x] Failure reports and logs were privacy-audited.
- [x] Local-only files remain ignored and absent from Git and Docker context.
- [x] The safety stash remains available.
- [ ] GitHub Actions was authorized to run, passed, and retained expected artifacts.
- [ ] Push or pull-request authority was granted.

## Completion decision

Status: **local Docker/PostgreSQL modernization validation complete**.

The repository is ready for an authorized push to validate the hosted GitHub Actions
workflow. This work stops before push, pull request, hosted execution, merge, release,
publication, repository settings changes, or safety-stash deletion.
