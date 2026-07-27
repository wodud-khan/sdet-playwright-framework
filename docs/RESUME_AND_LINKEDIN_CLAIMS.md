# Résumé and LinkedIn Claims

## Claim rule

Use only claims supported by the current validation report. “Implemented” does not mean
“passed.” SQLite fallback evidence does not support a PostgreSQL claim. A committed
workflow does not support a passing-CI claim.

## Five résumé-safe bullets

- Modernized a Python 3.12/Pytest/Playwright portfolio into a 28-test layered design,
  replacing third-party test dependencies, blanket retries, and unsupported tooling with
  a controlled local system and locked uv workflow.
- Built typed API, JSON Schema, direct PostgreSQL, integration, page-object, and E2E test
  components with unique run/worker data and exact-record cleanup; PostgreSQL runtime
  validation is pending local Docker availability.
- Demonstrated 18 isolated tests in serial and two-worker modes, plus focused Chromium UI
  and Chromium/Firefox/WebKit smoke coverage through an explicitly labeled lightweight
  fallback.
- Implemented failure diagnostics that retain Playwright trace, screenshot, video,
  browser-event JSON, API exchange metadata, HTML, and JUnit evidence; verified the
  bundle with a controlled failing test.
- Configured a least-privilege, SHA-pinned GitHub Actions pipeline to build a Compose
  app/PostgreSQL stack and retain test artifacts; hosted execution remains pending.

These bullets are deliberately explicit about the blocked PostgreSQL and CI boundary.
After Docker/CI validation, they may be shortened only after the report records passing
evidence.

## LinkedIn project description

I rebuilt an existing browser-automation repository into a focused quality-engineering
portfolio around a small controlled order application. The design separates unit, REST
API, JSON contract, direct database, integration, focused UI, and end-to-end intent while
sharing typed configuration, unique run/worker-aware data, and exact cleanup.

The non-container foundation is demonstrated locally with a locked Python 3.12
environment, 28-test collection, Ruff/Mypy gates, 18 passing unit tests, bounded parallel
checks, focused Chromium UI, three-browser fallback smoke, and an intentional
failure-evidence drill. PostgreSQL persistence, Docker Compose, the full
UI-to-API-to-database workflow, and a least-privilege GitHub Actions pipeline are
implemented. Their runtime validation is still pending because Docker is not installed
on the current machine, so I am not presenting those items as passing evidence yet.

## Claims to defer

Do not currently say:

- “Built a fully validated PostgreSQL automation framework”
- “Delivered a passing CI/CD pipeline”
- “Validated Dockerized local/CI parity”
- “Completed cross-browser end-to-end coverage”
- “Production-ready” or “enterprise-grade”
- “Zero flaky tests” or “guaranteed reliable”
- “Implemented Kubernetes, observability, security, or performance engineering”

## Direct implementation versus AI assistance

A truthful authorship description is:

> Human-directed, AI-assisted modernization. I set and reviewed the requirements,
> architecture, selectors, assertions, test data, cleanup, error behavior, diagnostics,
> and evidence boundaries. AI assisted with drafts of code, tests, analysis, and
> documentation. Runtime results—not generated text—determine every public claim.

Do not assign an invented percentage of code to either human or AI work. Git history and
validation evidence are more useful than an unverifiable authorship ratio.
