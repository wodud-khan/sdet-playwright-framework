# Flaky-Test Policy

Preserve the first failure and reproduce it with the same runtime, browser, and test data. Check service readiness, exact IDs, browser events, and diagnostics before changing a timeout or assertion. Use Compose health, bounded readiness polling, Playwright auto-waiting, and observable state. Keep serial execution as the first diagnostic run, then rerun the relevant bounded worker or browser scope.

There are no blanket reruns or quarantine markers. A future targeted retry or quarantine needs a specific cause, visible result, and review; it is not a substitute for fixing a reproducible defect. Do not clear shared tables or erase earlier artifacts to make a run pass.
