# CI Guide

`.github/workflows/quality.yml` has two jobs. `static-and-unit` installs the locked Python 3.12 environment, checks the lock, collects tests, runs Ruff and Mypy, and runs unit tests with two workers. `postgres-and-browser` builds the Compose stack, waits for health, runs serial and two-worker service suites, Chromium UI/E2E, and Chromium/Firefox/WebKit smoke. It captures Compose logs, stops the stack without deleting the volume, and uploads reports under `if: always()`.

The workflow has read-only repository permissions, non-persisted checkout credentials, job timeouts, concurrency cancellation, and SHA-pinned actions. It runs on pull requests, pushes to `main`, and manual dispatch. It validates quality; it does not deploy, publish, or release. Local commands and port overrides are in the [README](../README.md). Historical run links are in the [validation record](FINAL_VALIDATION_REPORT.md).
