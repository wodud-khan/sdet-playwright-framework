# Test Strategy

## Quality risks

The framework targets a small set of risks that can be demonstrated deeply:

- invalid order input crosses the API boundary
- create/read/delete behavior returns exact HTTP outcomes
- response shape drifts from the public JSON contract
- API state differs from persisted PostgreSQL state
- browser controls or feedback become unusable
- a full user-created order cannot be observed consistently through UI, API, and database
- tests leak records, collide under parallelism, or conceal browser failures

## Test layers

| Layer | Intent | Runtime | Current evidence |
|---|---|---|---|
| Unit | Settings, schemas, data, cleanup, diagnostics, SQLite repository logic | Python only | 18 passing |
| API | Exact REST status and body behavior | App + PostgreSQL | Implemented; blocked |
| Contract | JSON Schema for create/read order responses | App + PostgreSQL | Implemented; blocked |
| Database | Independent row verification by exact ID | App + PostgreSQL | Implemented; blocked |
| Integration | API create/delete reflected in PostgreSQL | App + PostgreSQL | Implemented; blocked |
| UI | Focused form controls and client validation | App; fallback allowed explicitly | Chromium fallback passing |
| E2E | UI create, API read, DB verify, exact cleanup | App + PostgreSQL + Chromium | Implemented; blocked |

SQLite results never substitute for PostgreSQL evidence.

## Assertion policy

- Assert one exact expected status, not a broad accepted range.
- Use full response equality when the stable payload is known.
- Validate public response structure with JSON Schema, independently of application
  Pydantic models.
- Query PostgreSQL through a dedicated test client rather than the application repository.
- Use Playwright `expect` assertions, accessible roles, labels, and stable test IDs.
- Treat unexpected console errors, page errors, failed requests, or HTTP error responses
  as failures even if the visible assertion passed.

## Data and teardown

State-changing tests use `OrderFactory` data containing:

- the test run identifier
- the xdist worker identifier
- a random per-record suffix

`OrderManager` records exact IDs and runs cleanup during fixture teardown, including after
test failures. Cleanup calls the public delete endpoint and verifies API absence. There is
no global fixture record, blanket deletion, table truncation, or shared static user.

## Execution order

Run serially first:

```bash
.venv/bin/python -m pytest tests/unit -q
.venv/bin/python -m pytest tests/api tests/contract tests/database tests/integration -q
.venv/bin/python -m pytest tests/ui tests/e2e --browser chromium -q
```

Then prove bounded isolation:

```bash
.venv/bin/python -m pytest \
  -m "api or contract or database or integration" -n 2 -q

.venv/bin/python -m pytest tests/ui -n 2 --browser chromium -q
```

Keep cross-browser coverage small:

```bash
.venv/bin/python -m pytest -m smoke \
  --browser chromium --browser firefox --browser webkit -q
```

The full E2E workflow runs on Chromium only. A broad E2E browser matrix would add cost
without improving the portfolio's current risk evidence.

## Reporting and diagnostics

HTML and JUnit provide portable human and CI results. Browser failures can retain native
trace, screenshot, and video output. The framework adds structured browser and API
metadata without request/response bodies or sensitive headers.

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

An intentional closed-port drill demonstrated that JSON browser events, a screenshot,
trace, and video are retained on failure. Compose/app/PostgreSQL log capture is configured
in CI but has not yet run.

## Exit criteria

The modernization cannot be classified as complete until:

- Docker Compose starts the app and PostgreSQL as healthy
- every service and browser layer passes independently
- the complete E2E case proves its cleanup
- the PostgreSQL-backed suite passes with two workers
- three-browser smoke passes against the primary stack
- the GitHub-hosted workflow passes and retains its artifacts
- the final report is updated with exact runtime evidence
