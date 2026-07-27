# Troubleshooting

## Confirm the environment first

```bash
git branch --show-current
uv --version
.venv/bin/python --version
.venv/bin/python -m pytest --collect-only -q
docker version
docker compose version
```

The supported branch for this modernization is
`refactor/sdet-framework-modernization`, and the supported project Python line is 3.12.

## Virtual-environment launchers reference an old repository path

Moving or renaming a parent folder can leave absolute shebangs in installed console
scripts. Refresh all entry points from the existing lock without changing versions:

```bash
uv sync --extra dev --locked --python 3.12 --reinstall
uv lock --check
```

Do not hand-edit scripts under `.venv/bin`.

## `uv` cannot use its cache

In a restricted environment, uv may fail while accessing a user-level cache outside the
repository. Installed `.venv` tools can still run:

```bash
.venv/bin/ruff check .
.venv/bin/python -m pytest tests/unit -q
```

In a normal local terminal, rerun the locked sync. Do not replace `uv.lock` or introduce
a second primary pip workflow to bypass an unexplained cache error.

## `APP_BASE_URL is required`

Service and browser tests intentionally fail instead of skipping when no controlled app
is configured:

```bash
export APP_BASE_URL=http://127.0.0.1:8000
.venv/bin/python scripts/wait_for_services.py --timeout 30
```

## `Service tests require the primary PostgreSQL runtime`

API, contract, database, integration, and E2E evidence require PostgreSQL:

```bash
export DATABASE_URL=postgresql://portfolio:local-demo-password@127.0.0.1:5432/portfolio
```

SQLite is accepted only for isolated logic and focused UI development with the explicit
`--allow-sqlite-ui-fallback` flag.

## Docker is unavailable

Docker is a system-level dependency and is not installed by repository scripts. Use only
an owner-approved official Docker distribution for the host architecture. After Docker
is available, verify the runtime before starting the project:

```bash
docker version
docker compose version
docker info
docker run --rm hello-world
```

The repository remains reproducible through its committed Dockerfile, Compose file,
Python metadata, and lock file; no Docker Desktop internal settings are required.

## Port 5432 or 8000 is occupied

Identify listeners without terminating unrelated processes:

```bash
lsof -nP -iTCP:5432 -sTCP:LISTEN
lsof -nP -iTCP:8000 -sTCP:LISTEN
```

Use supported overrides:

```bash
POSTGRES_PORT=55432 APP_PORT=8080 docker compose up --detach --wait

export APP_BASE_URL=http://127.0.0.1:8080
export DATABASE_URL=postgresql://portfolio:local-demo-password@127.0.0.1:55432/portfolio
```

## Compose does not become healthy

Separate configuration, build, and runtime diagnosis:

```bash
docker compose config
docker compose build --no-cache
docker compose up --detach --wait
docker compose ps --all
docker compose logs --no-color
```

Look for image-pull, startup, health-check, permission, schema, and port-binding errors.
Do not treat a successful `docker compose config` as runtime validation.

Stop the stack safely:

```bash
docker compose down
```

Ordinary cleanup must not use `docker compose down -v`. A named-volume reset requires a
specific technical reason and explicit approval.

## Browser executable missing

Install the declared browser binaries:

```bash
uv run playwright install chromium firefox webkit
```

On a Linux CI runner:

```bash
uv run playwright install --with-deps chromium firefox webkit
```

Browser installation is setup, not application or test evidence.

## A browser test passes but evidence reports errors

The diagnostics fixture deliberately fails a passing test when it observes console
errors, uncaught page errors, failed requests, or HTTP error responses. Inspect the
structured JSON and Playwright trace:

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

Inspect the exact order ID and body-free API exchange evidence. Never replace cleanup
with table-wide `DELETE`, `TRUNCATE`, wildcard, or global cleanup.

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

`artifacts/` is ignored by design. The workflow is configured to upload evidence under
`if: always()`, but that behavior becomes evidence only after a hosted run.

## Evidence contains a personal path or sensitive field

Inspect ordinary files and compressed trace contents before sharing:

```bash
rg -a -n '/Users/|authorization|set-cookie|cookie:' artifacts
unzip -p path/to/trace.zip | rg -a -n '/Users/|authorization|set-cookie|cookie:'
```

Do not publish an unsafe bundle. Regenerate or sanitize only the offending metadata,
validate the rebuilt archive with `unzip -t`, and scan it again. Never include local-only
Markdown, request bodies with private data, passwords, or environment-variable dumps.
