# Flaky-Test Policy

## Principle

A test that passes only sometimes is a defect in the test, product, environment, or
observability. It is not a signal to enable blanket retries.

The default suite is serial and retry-free. Parallelism is opt-in and bounded at two
workers after isolation is demonstrated.

## Triage

When a test is unstable:

1. Preserve the first-failure evidence.
2. Reproduce the same test with the same browser, runtime, and data configuration.
3. Classify the cause as product behavior, test logic, data collision, environment,
   service readiness, browser behavior, or unknown.
4. Verify the root cause with evidence before changing assertions or timing.
5. Correct the responsible layer.
6. Run the focused test repeatedly, then its layer serially, then the relevant bounded
   parallel or browser matrix.
7. Document any remaining limitation.

## Prohibited fixes

- arbitrary `sleep` calls
- global or blanket retries
- broader status-code acceptance
- replacing exact assertions with presence-only checks
- CSS/XPath locators when roles, labels, or stable test IDs are available
- table-wide cleanup
- shared mutable records
- silently skipping failures when a dependency is unavailable
- deleting failure artifacts before the cause is understood

## Temporary quarantine

Quarantine is exceptional. A quarantined case must have:

- a precise reason and reproducible symptom
- an issue or public tracking reference
- an owner
- an expiry date
- a separate, visible CI result
- no effect on unrelated required gates

No quarantine mechanism is currently implemented in this repository. Adding one would be
a policy and CI change, not an ad hoc marker.

## Readiness and waiting

Use observable conditions:

- Compose service health checks
- the bounded `/health` polling helper
- Playwright web-first assertions and auto-waiting
- exact API/database state

Timeouts must be finite and should report the last observed failure. Increasing a timeout
is justified only when measured startup or operation time proves the existing bound is
unrealistic.
