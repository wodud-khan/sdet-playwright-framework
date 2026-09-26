# SDET Playwright Framework

This repository tests a small order form and REST API backed by PostgreSQL. The application is controlled by the project so browser, API, JSON contract, and database checks can observe the same order. Python 3.12, pytest, synchronous Playwright with pytest-playwright fixtures, Requests, uv, Ruff, and Mypy form the test toolchain.

## Why these test layers

- Unit tests cover input rules, the SQLite repository path, cleanup, and diagnostics without a service.
- API tests check exact REST statuses and bodies. Contract tests validate response JSON against `contracts/order.schema.json`, independently of Pydantic models.
- Database tests query PostgreSQL directly; integration tests compare API and persisted state.
- Focused UI tests check browser controls and feedback. Chromium E2E tests follow UI creation through API and PostgreSQL, then delete the exact owned order. A page smoke test runs on Chromium, Firefox, and WebKit; it is not full E2E coverage on three engines.

Each registered ID belongs to one test. Teardown attempts cleanup for every owned ID and verifies absence. A 404 during cleanup is acceptable only after an exact-ID read confirms absence. Product tests still require 204 for DELETE and 404 for missing records. The UI fixes unit price at 2499 cents; tests supply independent expected totals for different quantities.

## Prerequisites and setup

Install [uv](https://docs.astral.sh/uv/), Docker with Compose, and the Playwright browsers. From the repository root:

```bash
uv sync --extra dev --locked --python 3.12
uv run --frozen playwright install chromium firefox webkit
uv lock --check
```

Start the PostgreSQL stack and confirm readiness:

```bash
docker compose config
docker compose up --detach --build --wait
uv run --frozen python scripts/wait_for_services.py --timeout 30
```

If ports 8000 or 5432 are occupied, use `APP_PORT` and `POSTGRES_PORT` Compose overrides and set the matching URLs below. Do not stop unrelated processes.

```bash
export APP_BASE_URL=http://127.0.0.1:8000
export DATABASE_URL=postgresql://portfolio:local-demo-password@127.0.0.1:5432/portfolio
export ARTIFACTS_DIR=artifacts
export TEST_RUN_ID=local-review

uv run --frozen pytest tests/unit -q
uv run --frozen pytest tests/api tests/contract tests/database tests/integration -q
uv run --frozen pytest tests/ui tests/e2e -q --browser chromium
uv run --frozen pytest -m 'api or contract or database or integration' -q -n 2
uv run --frozen pytest tests/ui -q -n 2 --browser chromium
uv run --frozen pytest -m smoke -q --browser chromium --browser firefox --browser webkit
```

Static checks are `uv run --frozen ruff check .`, `uv run --frozen ruff format --check .`, and `uv run --frozen mypy src scripts`. Mypy checks `src` and `scripts`, not all tests. Stop only this project's stack with `docker compose down`; retain the named database volume.

SQLite supports isolated repository tests and an explicit focused UI development path (`--allow-sqlite-ui-fallback`). It does not establish PostgreSQL integration or E2E correctness.

## Debugging failures

Use pytest's failure output, optional HTML/JUnit reports, and `--tracing retain-on-failure --screenshot only-on-failure --video retain-on-failure --output artifacts/playwright` for browser runs. Custom JSON records API method, URL, elapsed time, status or transport category, and browser error events. Its structured URL fields omit credentials, query strings, and fragments, but retain path segments; it does not record request or response bodies, headers, or cookies as separate fields. Console message text and page error names remain raw and can contain URLs or sensitive values. Native Playwright traces, screenshots, and videos, as well as pytest output and Compose logs, are not comprehensively redacted. Review evidence before sharing it and use synthetic test data.

The installed pytest-playwright recorder retains native failure artifacts based on the call report. A failure arising only during teardown may have custom JSON without retained native trace, screenshot, or video. An unexpected API creation status still fails. If its response contains a canonical UUID, an exact API read must match both that ID and every uniquely generated payload field before the manager registers it for cleanup. A timeout, missing or malformed ID, or failed verification leaves no safe exact ID to clean automatically.

## Validation record (September 2026)

On September 23, before this correction pass, a locked sync and lock check passed; pytest collected 54 cases, Ruff lint/format and Mypy passed, and 40 unit cases passed. The PostgreSQL Compose app built and became healthy. Service tests passed serially (7) and with two workers (7). Chromium UI/E2E passed (7), focused UI passed with two workers (4), and three-engine smoke passed (3). Those results preceded the final code changes.

For the current working tree, pytest collected 59 cases, the 25 focused unit cases and all 45 unit cases passed, and Ruff lint/format and Mypy passed. Four Chromium UI cases passed serially and with two workers against the explicit SQLite fallback. On September 25, the PostgreSQL Compose app built and became healthy; service tests passed serially (7) and with two workers (7), the repeatable failure cleanup regression passed (1), Chromium E2E passed (3), focused Chromium UI passed with two workers (4), and Chromium/Firefox/WebKit smoke passed (3). The project stack was stopped without deleting its named database volume. Remote CI results for later commits must be checked in GitHub Actions.

## CI and history

`.github/workflows/quality.yml` runs locked static/unit checks, the PostgreSQL service layers, bounded two-worker checks, Chromium UI/E2E, and three-engine smoke. It uploads reports and diagnostics and stops its Compose stack. CI validates quality; it does not deploy. Historical runs for the July 2026 version are linked in [the validation record](docs/FINAL_VALIDATION_REPORT.md); those results do not validate later edits.

Additional details: [architecture](docs/ARCHITECTURE.md), [design decisions](docs/DESIGN_DECISIONS.md), [test strategy](docs/TEST_STRATEGY.md), [CI guide](docs/CI_CD_GUIDE.md), [flaky-test policy](docs/FLAKY_TEST_POLICY.md), and [troubleshooting](docs/TROUBLESHOOTING.md).
