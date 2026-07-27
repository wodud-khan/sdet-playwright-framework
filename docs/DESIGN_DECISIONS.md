# Design Decisions

## Controlled application boundary

The framework tests a small FastAPI order application owned by the repository. This
replaces public demo sites whose data, availability, selectors, and rate limits are
outside the test suite's control. The owned boundary makes failures reproducible and
allows UI, API, contract, and persistence assertions to observe the same workflow.

## PostgreSQL as the primary runtime

PostgreSQL is the primary service, integration, and end-to-end runtime. Docker Compose
provides the same database topology for local and hosted validation, including health
checks and direct SQL verification. SQLite is limited to isolated repository logic and
an explicitly enabled lightweight UI-development path; it does not substitute for
PostgreSQL evidence.

## Separate test intent

The suite separates concerns by layer:

- unit tests cover configuration, schemas, data generation, cleanup, diagnostics, and
  isolated repository behavior
- API tests verify exact REST status and payload behavior
- contract tests validate public JSON independently of application models
- database tests query PostgreSQL directly by exact ID
- integration tests compare API behavior with persisted state
- UI tests cover focused browser behavior
- E2E tests connect UI creation, API observation, contract validation, PostgreSQL
  verification, API deletion, and database absence

This structure keeps failures attributable and lets each layer run independently.

## Owned data and cleanup

Every state-changing test creates run-, worker-, and UUID-aware data. The manager tracks
only IDs created by that test, deletes those exact IDs through the public API, and
verifies absence. Table-wide deletion, truncation, and wildcard cleanup are excluded so
parallel workers cannot erase one another's state.

## Bounded parallel execution

Serial execution remains the default diagnostic baseline. Two-worker runs explicitly
prove isolation without making resource use unbounded or obscuring ordering and cleanup
defects. The workflow does not use automatic worker counts.

## Browser scope

The full UI-to-API-to-PostgreSQL E2E workflow is Chromium-focused to keep the deepest
path deterministic and economical. A small smoke marker runs on Chromium, Firefox, and
WebKit to cover browser-engine differences without multiplying the full E2E matrix.

## Focused toolchain

Automatic retries are excluded because they can conceal deterministic defects.
Kubernetes, Jenkins, Allure, and other decorative infrastructure were removed because
the repository does not deploy or operate a production service. Portable HTML/JUnit
reports, native Playwright evidence, Docker Compose, and GitHub Actions directly support
the demonstrated quality workflow.

## Known limitations

- The order schema has positive-response coverage but no dedicated error-response
  contract.
- The application initializes its small schema at startup; migration tooling is outside
  scope.
- Authentication, deployment, cloud operations, performance, security, accessibility,
  and visual-regression programs are outside scope.
- The application is intentionally small and does not model production scaling or
  operational concerns.
