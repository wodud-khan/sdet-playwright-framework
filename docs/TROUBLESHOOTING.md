# Troubleshooting

## Confirm the environment first

```bash
git branch --show-current
uv --version
.venv/bin/python --version
.venv/bin/python -m pytest --collect-only -q
```

The supported branch for the current modernization is
`refactor/sdet-framework-modernization`, and the supported Python line is 3.12.

## `uv` cannot use its cache

In a restricted sandbox, uv may fail while accessing a user-level cache outside the
repository. The installed `.venv` tools can still run:

```bash
.venv/bin/ruff check .
.venv/bin/python -m pytest tests/unit -q
```

For a normal local terminal, rerun the locked sync:

```bash
uv sync --extra dev --locked --python 3.12
```

Do not replace the lock file or introduce a second primary pip workflow to bypass an
unexplained cache error.

## `APP_BASE_URL is required`

Service/browser tests intentionally fail instead of skipping when no controlled app is
configured:

```bash
export APP_BASE_URL=http://127.0.0.1:8000
```

Then confirm:

```bash
.venv/bin/python scripts/wait_for_services.py --timeout 30
```

## `Service tests require the primary PostgreSQL runtime`

API, contract, database, integration, and E2E evidence require a PostgreSQL URL:

```bash
export DATABASE_URL=postgresql://portfolio:local-demo-password@127.0.0.1:5432/portfolio
```

SQLite is accepted only by isolated unit logic and focused UI tests with the explicit
`--allow-sqlite-ui-fallback` flag.

## Docker command not found

Docker is a system-level dependency and is not automatically installed by this project.
Install it only with the machine owner's approval. Until it is available, run isolated
gates and classify PostgreSQL/Compose/service/E2E checks as blocked.

After Docker becomes available:

```bash
docker version
docker compose version
docker compose config
docker compose up --detach --build --wait
docker compose ps
```

If startup fails, retain:

```bash
docker compose ps --all
docker compose logs --no-color
```

Then stop the stack safely:

```bash
docker compose down
```

## Browser executable missing

Install the declared browser binaries:

```bash
uv run playwright install chromium firefox webkit
```

On a Linux CI runner, system dependencies are installed with:

```bash
uv run playwright install --with-deps chromium firefox webkit
```

Browser installation requires network access and should not be mistaken for application
or test validation.

## A browser test passes but evidence reports errors

The diagnostics fixture deliberately fails a passing test when it observes console
errors, uncaught page errors, failed requests, or HTTP error responses. Inspect the
structured JSON in `artifacts/browser`, then the Playwright trace:

```bash
uv run playwright show-trace artifacts/playwright/path/to/trace.zip
```

Fix the browser or application error; do not suppress the evidence hook.

## Cleanup failed

`OrderManager` deletes only IDs created or registered by the current test. A cleanup
failure can indicate:

- the app/database became unavailable during teardown
- the test deleted a record but did not call `mark_cleaned`
- the record was changed by another actor
- the API returned an unexpected result

Inspect the exact order ID and API exchange evidence. Never replace the cleanup with a
table-wide delete.

## Parallel-only failures

Rerun the exact failing node serially, then with two workers:

```bash
.venv/bin/python -m pytest path/to/test.py::test_name -q
.venv/bin/python -m pytest path/to/test.py::test_name -q -n 2
```

Check run/worker IDs, exact record ownership, port use, and artifact paths. Do not switch
to `-n auto` or add retries.

## Reports are missing

Reports are generated only when their options are present:

```bash
.venv/bin/python -m pytest tests/unit -q \
  --html=artifacts/unit-report.html \
  --self-contained-html \
  --junitxml=artifacts/unit-junit.xml
```

`artifacts/` is ignored by design. GitHub Actions uploads it under `if: always()` but that
behavior remains unverified until the workflow runs.
