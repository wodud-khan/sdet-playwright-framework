# Interview Walkthrough

## 60-second explanation

I modernized a browser-test repository into a focused quality-engineering portfolio. I
removed third-party and decorative paths, then built a deliberately small FastAPI order
system so the tests own the UI, REST API, and persistence boundary.

The framework separates unit, API, JSON contract, direct PostgreSQL, integration, focused
UI, and one full E2E workflow. Shared components provide validated configuration, typed
clients, semantic page objects, unique run/worker data, and exact cleanup. Browser
failures retain traces, screenshots, video, and safe event metadata, while HTML, JUnit,
application, PostgreSQL, and Compose logs provide portable evidence.

I demonstrated the locked Python 3.12 setup, 28-test collection, static gates, every test
layer against the Docker/PostgreSQL stack, bounded two-worker service and UI execution,
Chromium/Firefox/WebKit smoke, exact cleanup after an intentional assertion failure, and
a privacy-audited PostgreSQL-backed browser failure bundle. The hosted GitHub Actions
workflow is the remaining execution boundary, so I do not describe it as passing.

## Deeper architecture explanation

The main design decision was to make the system under test controlled and smaller than
the test architecture. FastAPI serves a static order form and three REST operations. The
application repository uses one small persistence interface. PostgreSQL is the primary
runtime; SQLite exists only for isolated logic and optional focused-UI development.

At the framework boundary, `Settings` validates environment configuration. `ApiClient`
owns HTTP session lifecycle and records only safe exchange metadata. A separate psycopg
client queries exact order IDs, so database checks do not accidentally reuse application
repository code. `OrderFactory` combines run, xdist worker, and random IDs. `OrderManager`
tracks only records created by a test and deletes each through the public API in teardown.

The E2E test submits through Playwright, captures the order returned by the UI/API,
validates its JSON contract, reads it through the API, verifies the row directly in
PostgreSQL, deletes it through the API, and proves database absence. The UI layer uses
official pytest-playwright fixtures, roles, labels, test IDs, and web-first assertions.

Diagnostics are failure-focused. Native Playwright options retain trace, screenshot, and
video, while an autouse hook records console errors, page errors, failed requests, and
error responses without bodies or headers. A passing visible assertion still fails if
the browser captured an unexpected error. The controlled drill also retained body-free
API metadata and service logs; decompressed trace content was audited for private data.

Compose starts PostgreSQL and the non-root app with health checks. The local no-cache
build, readiness, all test layers, failure drill, logs, and safe shutdown passed. GitHub
Actions is configured to use the same lifecycle with immutable action pins and
least-privilege permissions, but hosted execution remains a separate proof.

## Twenty likely interview questions

### 1. Why replace public demo websites with a controlled app?

Public sites add outages, rate limits, changing data, and selectors outside the test
owner's control. The local app makes failures attributable and permits API/database
verification without an external account.

### 2. Why is the demo application so small?

The portfolio subject is quality engineering. One order workflow provides enough UI,
API, contract, persistence, cleanup, and failure boundaries without turning the project
into an application-development showcase.

### 3. Why PostgreSQL instead of SQLite?

PostgreSQL creates a real service boundary and independent SQL-validation path. SQLite is
kept only for isolated speed and optional focused-UI development; it does not support the
primary integration or E2E evidence.

### 4. Why retain a SQLite adapter at all?

It keeps repository logic and focused browser mechanics fast during development. Its use
is explicit so it does not become an equal primary architecture.

### 5. How do API and database tests stay independent?

API tests use Requests against public endpoints. Database checks use a dedicated psycopg
client and exact SQL query. They do not call the application's `OrderRepository`.

### 6. How is test data isolated?

Every payload includes a run ID, xdist worker ID, and random suffix. There is no shared
mutable fixture record.

### 7. How does cleanup work after a failure?

A yield fixture owns an `OrderManager`. Teardown runs after the test body and deletes only
registered order IDs through the API, then verifies `404`. I proved that with a temporary
test that failed after PostgreSQL presence; the next test verified the same captured ID
was absent, and the table count was zero.

### 8. What if cleanup itself fails?

Cleanup raises an explicit assertion with the exact record and response. It does not hide
the failure or fall back to a broad database delete.

### 9. Why no automatic retries?

Retries can turn nondeterminism into a green build and discard first-failure evidence.
The policy is to diagnose product, test, data, readiness, browser, or environment causes.

### 10. How do the UI selectors resist change?

The page object uses accessible roles, labels, and narrow stable test IDs. Tests use
Playwright web-first assertions rather than manual polling or sleep.

### 11. Why use JSON Schema when FastAPI already uses Pydantic?

Pydantic validates inside the application. JSON Schema validates the black-box response
from the test side, avoiding a contract check that merely reuses the implementation
model.

### 12. What does the complete E2E test prove?

It creates through the UI, validates the JSON contract, reads through the API, queries
the exact PostgreSQL row, deletes through the API, and verifies database absence. That
workflow passed on Chromium and passed again after the controlled failure drill.

### 13. What evidence is captured on a browser failure?

Native Playwright trace, screenshot, and video plus structured console, page-error,
failed-request, and error-response metadata. API fixtures retain safe method/URL/status/
duration metadata. HTML, JUnit, application, PostgreSQL, and Compose logs complete the
bundle.

### 14. How was the diagnostics path tested?

A temporary Chromium test created an order, verified it directly in PostgreSQL, opened
the live UI, then asserted a nonexistent heading. It produced one expected failure and
the full bundle. Cleanup left zero rows, the test was removed, and decompressed trace
content plus ordinary files were scanned for secrets and personal paths.

### 15. What parallelism has been demonstrated?

Eighteen unit tests passed with two workers during the pre-installation regression, seven
PostgreSQL service tests passed with two workers, and two PostgreSQL-backed Chromium UI
tests passed with two workers. I do not claim `-n auto` or unbounded concurrency.

### 16. Why only smoke coverage across all three browsers?

The highest-value full workflow stays on Chromium. A small PostgreSQL-backed smoke matrix
detects basic compatibility across Chromium, Firefox, and WebKit without tripling every
service/E2E test and its runtime cost.

### 17. How do local and CI commands align?

Both use uv 0.11.8, Python 3.12, `uv.lock`, the same Compose stack, readiness script, test
markers, and Playwright options. CI adds caching, timeouts, concurrency cancellation, and
artifact upload.

### 18. What is the current biggest limitation?

The workflow has not run on a GitHub-hosted runner, so action execution, hosted caching,
and artifact upload are not yet evidence. The application also intentionally omits
production migrations, authentication, and broader nonfunctional programs.

### 19. What would you validate next?

After separate push authority, I would run the hosted workflow, inspect both jobs and
retained artifacts, compare Compose health and test counts with local evidence, record
the run ID, and only then make a CI-success claim.

### 20. How was AI used responsibly?

AI assisted with analysis, implementation, tests, and documentation drafts. Human
direction set scope and safety, and the SDET reviews assertions, selectors, cleanup,
diagnostics, commands, results, and claims. Generated text never substitutes for runtime
evidence.

## Honest closing summary

The strongest part of the project is not the number of tools. It is the traceability from
risk to test layer, data ownership, cleanup, diagnostics, reproducible command, and
truthful claim. Local Docker/PostgreSQL behavior is demonstrated; hosted CI is the next
separate validation step.
