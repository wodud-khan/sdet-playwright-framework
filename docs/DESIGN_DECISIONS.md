# Design Decisions

The small owned application makes UI, API, JSON, and SQL observations reproducible without depending on a public demo site. The full cross-layer flow runs on Chromium; a page smoke test covers Firefox and WebKit. Those are separate scopes.

The UI exposes customer, item, and quantity while fixing price at 2499 cents. Tests specify expected totals independently in cents. The page object handles interaction and display checks; test fixtures own record cleanup. API tests require exact product statuses, while teardown accepts a previously deleted owned ID only after it verifies 404 by exact ID.

Serial runs are the diagnostic default. Two-worker service and UI runs check isolation without unbounded workers. Playwright's semantic locators and observable waits are preferred for this page. Blanket reruns are absent because they can hide an initial failure; a targeted retry would need its own evidence and justification. The existing toolchain and report formats are kept small enough to explain.

See [architecture](ARCHITECTURE.md) for components and [flaky-test policy](FLAKY_TEST_POLICY.md) for triage.
