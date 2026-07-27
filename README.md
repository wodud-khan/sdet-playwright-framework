# SDET Playwright Framework

A focused quality-engineering portfolio built around a deliberately small order
application. The repository demonstrates test architecture and engineering decisions
across Python, Pytest, Playwright, REST, JSON Schema, PostgreSQL, diagnostics, reporting,
Docker Compose, and GitHub Actions configuration.

The primary local stack is demonstrated end to end: Docker Compose builds and starts the
FastAPI application and PostgreSQL 17, all service and browser layers pass, bounded
parallel runs do not collide, all three supported browser engines pass smoke coverage,
and exact-ID cleanup works even after an intentional assertion failure.

## What the project contains

- A minimal FastAPI order UI and REST API under `src/demo_app`
- PostgreSQL as the primary integration and end-to-end persistence runtime
- Typed API and direct PostgreSQL clients
- Run- and worker-aware test data with exact-record cleanup
- Separate unit, API, contract, database, integration, UI, and E2E suites
- Official pytest-playwright browser fixtures, semantic locators, and web-first assertions
- Failure-only browser/API evidence plus HTML, JUnit, trace, screenshot, video, and logs
- Locked Python 3.12 dependencies through uv
- A non-root application image and health-checked Docker Compose stack
- A least-privilege, SHA-pinned GitHub Actions workflow ready for hosted validation

## Demonstrated evidence

| Capability | Result |
|---|---|
| Locked Python 3.12 installation and 28-test collection | Passed |
| Ruff lint/format and strict Mypy | Passed |
| Unit | 18 passed |
| API | 4 passed |
| JSON contract | 1 passed |
| Direct PostgreSQL | 1 passed |
| API-to-PostgreSQL integration | 1 passed |
| Focused Chromium UI | 2 passed |
| Chromium UI-to-API-to-PostgreSQL E2E | 1 passed |
| Two-worker service layer | 7 passed |
| Two-worker Chromium UI | 2 passed |
| PostgreSQL-backed Chromium/Firefox/WebKit smoke | 3 passed |
| Docker no-cache build and Compose health lifecycle | Passed |
| Intentional-failure cleanup and diagnostic evidence drills | Passed |
| Hosted GitHub Actions execution | Not executed |

See [FINAL_VALIDATION_REPORT.md](docs/FINAL_VALIDATION_REPORT.md) for exact commands,
runtime versions, evidence boundaries, and remaining limitations.

## Prerequisites

- macOS or Linux
- [uv](https://docs.astral.sh/uv/) available on `PATH`
- Docker with the Compose plugin

Python 3.12 is the supported project runtime. uv may obtain it when needed.

## Install

From the repository root:

```bash
uv sync --extra dev --locked --python 3.12
uv run playwright install chromium firefox webkit
```

The committed `uv.lock` is the dependency source for local setup and CI.

## Fast checks

These commands do not need Docker:

```bash
.venv/bin/python -m pytest --collect-only -q
.venv/bin/ruff check .
.venv/bin/ruff format --check .
.venv/bin/mypy src scripts
.venv/bin/python -m pytest tests/unit -q
```

## Primary PostgreSQL workflow

Build and start the controlled stack:

```bash
docker compose config
docker compose build --no-cache
docker compose up --detach --wait
docker compose ps
.venv/bin/python scripts/wait_for_services.py --timeout 30
curl --fail --silent http://127.0.0.1:8000/health
```

Configure host-side tests:

```bash
export APP_BASE_URL=http://127.0.0.1:8000
export DATABASE_URL=postgresql://portfolio:local-demo-password@127.0.0.1:5432/portfolio
export API_TIMEOUT_SECONDS=5
export ARTIFACTS_DIR=artifacts
export TEST_RUN_ID=local
```

Run each layer independently:

```bash
.venv/bin/python -m pytest tests/api -q
.venv/bin/python -m pytest tests/contract -q
.venv/bin/python -m pytest tests/database -q
.venv/bin/python -m pytest tests/integration -q
.venv/bin/python -m pytest tests/ui --browser chromium -q
.venv/bin/python -m pytest tests/e2e --browser chromium -q
```

Run bounded parallel and browser proofs:

```bash
.venv/bin/python -m pytest \
  -m "api or contract or database or integration" -n 2 -q

.venv/bin/python -m pytest tests/ui -n 2 --browser chromium -q

.venv/bin/python -m pytest -m smoke \
  --browser chromium --browser firefox --browser webkit -q
```

Stop the containers and network without deleting the named database volume:

```bash
docker compose logs --no-color
docker compose down
```

Do not add `-v` to ordinary shutdown.

## Failure evidence

For browser tests, enable native Playwright and portable report output:

```bash
.venv/bin/python -m pytest tests/ui --browser chromium \
  --tracing=retain-on-failure \
  --screenshot=only-on-failure \
  --video=retain-on-failure \
  --output=artifacts/playwright \
  --html=artifacts/browser-report.html \
  --self-contained-html \
  --junitxml=artifacts/browser-junit.xml
```

Failure evidence can include:

- Playwright trace, screenshot, and video
- console, page, failed-request, and error-response metadata
- body-free API method/URL/status/duration metadata
- Pytest HTML and JUnit reports
- application, PostgreSQL, and Compose logs

Generated evidence stays under ignored paths. Authorization headers, cookies, request
bodies with private data, environment dumps, private local files, and personal paths are
excluded.

## Optional lightweight development path

SQLite is available only for isolated logic and quick focused-UI development when the
primary stack is intentionally not running. It is not an integration or E2E substitute.

```bash
mkdir -p artifacts
DATABASE_URL=sqlite:///artifacts/ui-fallback.sqlite3 \
  .venv/bin/python -m uvicorn demo_app.main:app --host 127.0.0.1 --port 8000
```

In another terminal:

```bash
APP_BASE_URL=http://127.0.0.1:8000 \
DATABASE_URL=sqlite:///artifacts/ui-fallback.sqlite3 \
  .venv/bin/python -m pytest tests/ui \
  --allow-sqlite-ui-fallback --browser chromium -q
```

## Test structure

```text
tests/
├── unit/          # isolated framework and application logic
├── api/           # black-box REST behavior
├── contract/      # JSON Schema validation
├── database/      # direct PostgreSQL verification
├── integration/   # API-to-PostgreSQL lifecycle
├── ui/            # focused browser behavior
└── e2e/           # UI-to-API-to-PostgreSQL workflow
```

The controlled application is intentionally smaller than the test framework. Core tests
do not call public websites or require external accounts.

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Test strategy](docs/TEST_STRATEGY.md)
- [CI/CD guide](docs/CI_CD_GUIDE.md)
- [Flaky-test policy](docs/FLAKY_TEST_POLICY.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)
- [AI-assisted engineering](docs/AI_ASSISTED_ENGINEERING.md)
- [Final validation report](docs/FINAL_VALIDATION_REPORT.md)
- [Interview walkthrough](docs/INTERVIEW_WALKTHROUGH.md)
- [Résumé and LinkedIn claims](docs/RESUME_AND_LINKEDIN_CLAIMS.md)

## Limitations

- The GitHub Actions workflow has not been pushed or executed; local success is not a
  hosted-CI result.
- Positive order schema coverage is present; a dedicated error-response schema is not.
- The demo app initializes its small schema directly; migration tooling is outside scope.
- Authentication, cloud deployment, performance, security, accessibility, and visual
  regression programs are intentionally outside scope.
- This is a portfolio system, not a production application or enterprise framework.
