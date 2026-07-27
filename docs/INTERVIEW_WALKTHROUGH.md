# Interview Walkthrough

## 60-second explanation

I modernized a browser-test repository into a focused quality-engineering portfolio. I
removed unvalidated third-party and decorative paths, then built a deliberately small
FastAPI order system so the tests own the UI, REST API, and persistence boundary.

The framework separates unit, API, JSON contract, direct PostgreSQL, integration, focused
UI, and one full E2E workflow. Shared components provide validated configuration, typed
clients, semantic page objects, unique run/worker test data, and exact cleanup. Browser
failures retain traces, screenshots, video, and safe event metadata, while HTML and JUnit
cover portable reporting.

I have demonstrated the locked Python 3.12 setup, 28-test collection, static gates, 18
unit tests, bounded parallel checks, focused Chromium UI, three-browser fallback smoke,
and a controlled diagnostic failure. Docker is not installed locally, so I clearly label
PostgreSQL, Compose, full E2E, and hosted CI execution as implemented but not yet
validated.

## Deeper architecture explanation

The main design decision was to make the system under test controlled and smaller than
the test architecture. FastAPI serves a static order form and three REST operations.
The application repository uses one small persistence interface. PostgreSQL is the
primary runtime; SQLite exists only to keep isolated and focused UI development fast.

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
the browser captured an unexpected error.

Compose starts PostgreSQL and the non-root app with health checks. GitHub Actions is
configured to use the same Compose lifecycle, run static and layered gates, and upload
artifacts unconditionally. That last runtime path is not yet demonstrated.

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
kept only for isolated speed and an explicit fallback; it cannot support the database or
E2E claims.

### 4. Why retain a SQLite adapter at all?

It makes repository logic and focused browser mechanics testable without system
infrastructure. Its use is gated and documented so it does not become an equal primary
architecture.

### 5. How do API and database tests stay independent?

API tests use Requests against public endpoints. Database checks use a dedicated psycopg
client and exact SQL query. They do not call the application's `OrderRepository`.

### 6. How is test data isolated?

Every payload includes a run ID, xdist worker ID, and random suffix. There is no shared
mutable fixture record.

### 7. How does cleanup work after a failure?

A yield fixture owns an `OrderManager`. Teardown runs after the test body and deletes only
registered order IDs through the API, then verifies `404`. The E2E test also verifies
database absence when it performs its explicit delete.

### 8. What if cleanup itself fails?

The cleanup raises an explicit assertion with the exact record and response. It does not
hide the failure or fall back to a broad database delete.

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

Its implemented flow creates through UI, validates and reads through API, queries the
exact PostgreSQL row, deletes through API, and verifies database absence. It is not yet
runtime-demonstrated because PostgreSQL is unavailable locally.

### 13. What evidence is captured on a browser failure?

Native Playwright trace, screenshot, and video plus structured console, page-error,
failed-request, and error-response metadata. API fixtures retain safe method/URL/status/
duration metadata. Bodies and sensitive headers are excluded.

### 14. How was the diagnostics path tested?

A controlled test targeted a closed local port. It failed as expected and retained
browser JSON, screenshot, trace, and video. The deliberate failure was not committed.

### 15. What parallelism has been demonstrated?

Eighteen unit tests and the focused fallback UI passed with two workers. PostgreSQL-backed
service parallelism is implemented but remains blocked. I do not claim `-n auto` or
unbounded concurrency.

### 16. Why only smoke coverage across all three browsers?

The highest-value full workflow stays on Chromium. A small smoke matrix detects basic
browser compatibility without tripling every service/E2E test and its runtime cost.

### 17. How do local and CI commands align?

Both use uv 0.11.8, Python 3.12, `uv.lock`, the same Compose stack, readiness script, test
markers, and Playwright options. CI adds caching, timeouts, concurrency cancellation, and
artifact upload.

### 18. What is the current biggest limitation?

Docker is missing locally. Therefore PostgreSQL, Compose, service suites, full E2E, and
hosted CI cannot be described as passing. The validation report stops at that boundary.

### 19. What would you validate immediately after Docker installation?

Compose config/build/up/health, independent service layers serially, Chromium UI/E2E,
cleanup, two-worker service isolation, three-browser primary-stack smoke, failure logs,
and finally the hosted workflow after separate push authority.

### 20. How was AI used responsibly?

AI assisted with analysis, implementation, tests, and documentation drafts. Human
direction set scope and safety, and the SDET reviews assertions, selectors, cleanup,
diagnostics, commands, results, and claims. Generated text never substitutes for runtime
evidence.

## Honest closing summary

The strongest part of the project is not the number of tools. It is the traceability from
risk to test layer, data ownership, cleanup, diagnostics, reproducible command, and
truthful claim. The remaining Docker boundary should be presented openly; resolving it
is the next validation step, not something to imply away.
