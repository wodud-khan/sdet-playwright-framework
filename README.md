# SDET Playwright Framework

A focused quality-engineering portfolio built around a deliberately small order
application. The repository demonstrates test architecture and engineering decisions
across Python, Pytest, Playwright, REST, contracts, persistence, diagnostics, reporting,
Docker Compose, and GitHub Actions.

This modernization is still in progress. The isolated framework, unit tests, lightweight
UI path, cross-browser smoke path, bounded parallel checks, and controlled failure
diagnostics have run locally. PostgreSQL, Docker Compose, the PostgreSQL-backed service
suites, the full UI-to-API-to-database workflow, and the GitHub-hosted workflow are
implemented but not yet runtime-validated because Docker is not installed locally.

## What the project contains

- A minimal FastAPI order UI and REST API under `src/demo_app`
- PostgreSQL as the primary integration and end-to-end persistence runtime
- A narrow SQLite adapter used only for isolated tests and an explicit UI fallback
- Typed API and direct PostgreSQL clients
- Run- and worker-aware test data with exact-record cleanup
- Separate unit, API, contract, database, integration, UI, and E2E suites
- Official pytest-playwright browser fixtures, semantic locators, and web-first assertions
- Failure-only browser/API evidence plus HTML, JUnit, trace, screenshot, and video output
- Locked Python 3.12 dependencies through uv
- A two-job GitHub Actions workflow and a health-checked Compose stack

## Current evidence

| Capability | Current status |
|---|---|
| Fresh locked Python 3.12 installation | Demonstrated |
| 28-test collection | Demonstrated |
| Ruff lint/format and strict Mypy | Demonstrated |
| 18 isolated unit tests | Demonstrated |
| Focused Chromium UI through explicit SQLite fallback | Demonstrated |
| Chromium, Firefox, and WebKit fallback smoke | Demonstrated |
| Bounded two-worker unit and focused UI runs | Demonstrated |
| HTML/JUnit and intentional browser-failure evidence | Demonstrated |
| PostgreSQL app and direct database behavior | Implemented; runtime blocked |
| API, contract, database, and integration suites | Implemented; runtime blocked |
| Full UI-to-API-to-PostgreSQL E2E | Implemented; runtime blocked |
| Docker image and Compose lifecycle | Implemented; runtime blocked |
| GitHub Actions execution | Implemented; not yet executed |

See [FINAL_VALIDATION_REPORT.md](docs/FINAL_VALIDATION_REPORT.md) for exact evidence and
claim boundaries.

## Prerequisites

- macOS or Linux
- [uv](https://docs.astral.sh/uv/) available on `PATH`
- Docker with the Compose plugin for the primary PostgreSQL workflow

Python 3.12 is the supported runtime. uv may obtain that runtime when needed.

## Install

From the repository root:

```bash
uv sync --extra dev --locked --python 3.12
uv run playwright install chromium firefox webkit
```

The committed `uv.lock` is the single dependency source for local setup and CI. The
absence of `pip` inside a uv-managed environment is intentional.

## Fast validated checks

These commands do not need Docker:

```bash
.venv/bin/python -m pytest --collect-only -q
.venv/bin/ruff check .
.venv/bin/ruff format --check .
.venv/bin/mypy src scripts
.venv/bin/python -m pytest tests/unit -q
```

Generate portable unit reports:

```bash
.venv/bin/python -m pytest tests/unit -q -n 2 \
  --html=artifacts/unit-report.html \
  --self-contained-html \
  --junitxml=artifacts/unit-junit.xml
```

## Primary PostgreSQL workflow

The following is the intended local workflow, but it remains unvalidated on this machine
until Docker is installed:

```bash
docker compose config
docker compose up --detach --build --wait
.venv/bin/python scripts/wait_for_services.py --timeout 30

export APP_BASE_URL=http://127.0.0.1:8000
export DATABASE_URL=postgresql://portfolio:local-demo-password@127.0.0.1:5432/portfolio
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

Run the isolation and browser proofs:

```bash
.venv/bin/python -m pytest \
  -m "api or contract or database or integration" -n 2 -q

.venv/bin/python -m pytest -m smoke \
  --browser chromium --browser firefox --browser webkit -q
```

Stop the stack without deleting its named database volume:

```bash
docker compose down
```

Do not interpret these PostgreSQL and Compose commands as passing evidence until their
results are recorded in the final validation report.

## Explicit lightweight UI fallback

SQLite is not the primary database. This fallback exists only for quick UI development
when PostgreSQL is unavailable.

In one terminal:

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

This command cannot support PostgreSQL, database-integration, Docker, or full E2E claims.

## Failure evidence

For browser tests, enable native Playwright evidence:

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

Failure evidence may include:

- trace archives, screenshots, and video from Playwright
- console, page, failed-request, and error-response metadata
- body-free API exchange metadata
- Pytest HTML and JUnit reports
- application and Compose logs in CI

Generated evidence stays under ignored paths. Authorization headers, cookies, request
bodies, environment dumps, and private local files are not collected.

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

The demo application is intentionally smaller than the test framework. Core tests do not
call public websites or require external accounts.

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

- Docker and PostgreSQL execution are currently blocked by the missing local Docker
  runtime.
- The GitHub Actions workflow is committed but has not been pushed or executed.
- Authentication, cloud deployment, performance, security, accessibility, and visual
  regression programs are intentionally outside the current scope.
- The database schema is initialized by the demo app; production migration tooling is not
  represented.
- This is a portfolio system, not a production application or enterprise framework.
