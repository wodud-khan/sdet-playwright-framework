# Repository Audit

## Audit snapshot

- Date: 2026-07-26
- Branch: `refactor/sdet-framework-modernization`
- Baseline commit: `24cb706` (`sdet-portfolio-baseline-v1`)
- Scope: Phase 0 repository audit only
- Inventory: 57 tracked files, including 44 Python files
- Safety: no network access, dependency installation, external authentication, push, merge,
  release, pull request, repository rename, or GitHub setting change was performed
- Private local context was read as required but is not reproduced here

## Executive assessment

The repository is a useful prototype, not yet a demonstrated quality-engineering
portfolio. It contains recognizable UI and API test patterns, but the runtime is not
reproducible from the tracked files and several prominent README claims exceed the
available evidence.

The recommended path is **B: replace selected internals while preserving useful code,
concepts, Git history, and the public repository**. A ground-up rewrite is not justified:
the page-object flow, API-client boundary, JSON Schema example, mock-service concept,
markers, and CI/container starting points are worth retaining or adapting. The execution
model, dependency management, controlled system under test, diagnostics, data isolation,
and documentation need substantial refactoring.

No implementation was performed during this audit.

## Evidence and limitations

### Demonstrated during this audit

- Repository root, non-main branch, clean starting state, and public `origin` were verified.
- All 44 tracked Python files parsed successfully with the Python standard library.
- Both tracked JSON documents parsed successfully.
- The GitHub Actions, Kubernetes, and ownership YAML files parsed as YAML.
- Both required private local files are untracked and excluded by `.git/info/exclude`.
- The current branch points to the same baseline commit as `main`; modernization work has
  not begun.

### Execution limitation

The audit host has no installed project dependencies. `pytest`, Playwright, Requests,
FastAPI, Uvicorn, JSON Schema, Ruff/Flake8, Black, and Mypy are unavailable. Docker,
Docker Compose, Java, Allure CLI, and `kubectl` are also unavailable. The repository has
no virtual environment.

The bootstrap safety boundary requires approval before dependency installation or
network access. Therefore dependency and browser installation were not attempted.
Runtime test results must not be inferred from the static audit.

## Command audit

Results below distinguish an observed failure from a command that was deliberately not
run because approval or a missing prerequisite blocked it.

| Exact command | Result | Failure or blocker | Likely root cause | Recommended correction |
|---|---|---|---|---|
| `python --version` | Failed: command not found | README assumes a `python` alias | This macOS installation exposes `python3` only | Document `python3` for environment creation and `.venv/bin/python` thereafter |
| `python -m venv venv` | Failed: command not found | Virtual environment was not created | Same missing `python` alias | Standardize on Python 3.12 and use `python3.12 -m venv .venv` |
| `pip install -r requirements.txt` | Not run | New dependency installation requires approval | Bootstrap safety boundary; requirements are also unpinned and incomplete | Approve a controlled install only after dependency metadata is corrected |
| `playwright install` | Not run | Browser download requires approval/network | Bootstrap safety boundary | Pin Playwright and document an approved browser-install step |
| `pytest --collect-only -q` | Failed: command not found | Test discovery unavailable | Pytest is not installed | Install the approved development dependencies, then make collection the first gate |
| `pytest` | Failed: command not found | Full suite unavailable | Pytest is not installed | Run only after collection and local services pass readiness checks |
| `pytest tests/api` | Failed: command not found | API suite unavailable | Pytest and Requests are not installed | Add complete dependencies and start the controlled API before execution |
| `pytest tests/ui` | Failed: command not found | UI suite unavailable | Pytest/Playwright and browsers are not installed | Install pinned tooling and browsers; remove third-party UI dependency |
| `pytest tests/api/integration` | Failed: command not found | Integration suite unavailable; directory has no tests | Pytest is absent and the tracked directory is decorative | Implement a real service-level integration test or remove the empty directory |
| `pytest tests/ui/test_e2e_checkout.py` | Failed: command not found | UI E2E unavailable | Pytest/Playwright/browser unavailable; test depends on a public site | Migrate the workflow to the controlled local demo application |
| `pytest -n auto` | Failed: command not found | Parallel execution unavailable | Pytest-xdist is not installed | Validate serially first; then use bounded workers and isolated data |
| `pytest --alluredir=allure-results` | Failed: command not found | GitHub Actions-equivalent test command unavailable | Test dependencies are absent | Replace or simplify reporting and upload artifacts with `if: always()` |
| `pytest -m smoke -n auto` | Failed: command not found | Jenkins-equivalent command unavailable | Pytest/xdist are absent | Make Jenkins optional or remove it until its execution can be demonstrated |
| `flake8 .` | Failed: command not found | Lint check unavailable | Flake8 is not installed | Consolidate linting and formatting on pinned Ruff |
| `black --check .` | Failed: command not found | Format check unavailable | Black is not installed | Consolidate on Ruff format, or pin Black if retained |
| `mypy .` | Failed: command not found | Type check unavailable and undocumented | Mypy is not installed and is not declared | Add Mypy only after defining a typed target package |
| `uvicorn mock_services.auth_service.main:app --port 8001` | Failed: command not found | Local service cannot start | FastAPI/Uvicorn are used by code but missing from `requirements.txt` | Declare runtime dependencies and provide a readiness endpoint |
| `docker build -t sdet-playwright .` | Failed: command not found | Image could not be built | Docker is not installed | Re-run after Docker is available and build-context privacy is fixed |
| `docker compose up --build` | Failed: command not found | Compose execution unavailable; no Compose file exists | Docker/Compose absent and orchestration was never implemented | Add a small app/database Compose stack and validate `docker compose config` first |
| `kubectl apply --dry-run=client -f k8s/test-job.yaml` | Failed: command not found | Kubernetes manifest not validated by Kubernetes tooling | `kubectl` is absent; Kubernetes is out of portfolio scope | Remove this decorative manifest unless explicit learning scope is approved |
| `python3 -c 'import ast,pathlib,subprocess; paths=[pathlib.Path(p) for p in subprocess.run(["git","ls-files"],check=True,capture_output=True,text=True).stdout.splitlines() if p.endswith(".py")]; [ast.parse(p.read_text(encoding="utf-8"),filename=str(p)) for p in paths]; print(f"PASS: {len(paths)} Python files")'` | Passed: 44 files | Syntax only; imports/runtime were not exercised | None | Keep as a fast pre-test check, but do not treat it as test evidence |
| `python3 -c 'import json,pathlib; paths=[pathlib.Path("contracts/user_schema.json"),pathlib.Path("tests/data/users.json")]; [json.loads(p.read_text(encoding="utf-8")) for p in paths]; print(f"PASS: {len(paths)} JSON files")'` | Passed: 2 files | Syntax only | None | Add semantic contract/data tests |
| `ruby -e 'require "yaml"; %w[.github/workflows/playwright-tests.yml k8s/test-job.yaml ownership/test_ownership.yaml].each { \|f\| YAML.load_file(f) }; puts "PASS: 3 YAML files"'` | Passed: 3 files | Syntax only; platform semantics were not validated | None | Add action/container-specific validation in CI |
| `curl --fail http://127.0.0.1:8001/health` | Not run | Service did not start and no health route exists | Uvicorn missing; mock app exposes only `/auth/login` | Add `/health`, bounded readiness polling, and an actionable failure message |

### Test categories

| Category | Tracked evidence | Audit result |
|---|---|---|
| Unit | No `tests/unit` directory or unit tests | Absent |
| API | Four test functions across auth, user, and contract files | Implemented but not executed |
| Database | No driver, fixture, schema, database service, or test | Absent |
| Integration | Empty package only | Documentation only |
| UI | Three functions; parameterization expands the negative login test to five cases, for seven UI cases total | Implemented but not executed; all use a public site |
| End-to-end | One browser-only checkout flow | Not a UI-to-API-to-database workflow |
| Parallel | `-n auto` is globally enabled | Not demonstrated and unsafe with current artifact cleanup |
| Cross-browser | Playwright is present in dependency metadata | Not implemented; the custom fixture always launches Chromium |

## Architecture findings

### Pytest and Playwright lifecycle

- `conftest.py` replaces the pytest-playwright `page` fixture and launches Playwright and
  Chromium for every test. This defeats the plugin's browser selection and standard
  lifecycle features.
- Browser and context scope are function-level, which is isolation-friendly but expensive.
  There is no tested strategy for session reuse, authentication state, or browser matrix
  selection.
- `pytest_sessionstart` deletes and recreates shared artifact directories. With xdist,
  workers can race to remove paths while other workers use them.
- Cleanup is not protected by a comprehensive `try/finally`; a screenshot, video, or
  teardown error can prevent later cleanup.
- Video is recorded for every UI test, not only retained for failures.
- The failure hook tries to resolve the video path before the context is closed, while a
  Playwright video is finalized on page/context closure.
- The configuration defaults every invocation—including collection and API-only runs—to
  `-n auto`, which can oversubscribe a laptop or CI runner.
- `pytest.ini` repeats `--reruns 2 --reruns-delay 1` on consecutive lines. Blanket retries
  can hide deterministic defects and contradict the stated reliability standard.

### Base URL, authentication, locators, and assertions

- UI navigation is hard-coded in `pages/login_page.py`; `config/env.py` is unused.
- API URLs are split between a hard-coded public JSONPlaceholder URL and a hard-coded
  localhost auth URL. There is no single validated settings object.
- `AUTH_TOKEN` exists but is unused. No authentication-state fixture is implemented.
- Page objects are a useful separation boundary, but they mix CSS, ID, and brittle XPath
  selectors based on visible text and ancestor structure.
- Tests primarily use raw Python `assert` and `is_visible()` rather than Playwright's
  auto-retrying `expect` assertions.
- The checkout total uses binary floating-point equality for currency. Decimal parsing or
  integer cents would be safer.
- The mock invalid-login path returns HTTP 200, so the negative test demonstrates content
  matching but not conventional error-status behavior.

### Test data, cleanup, parallelism, retries, and flakiness

- UI credentials, API credentials, email addresses, names, and checkout data are
  hard-coded. They are public demo values, not secrets, but are not generated or isolated.
- `tests/data/users.json` and several factory/helper modules are unused.
- JSONPlaceholder simulates writes without persistence. The create-user test cannot prove
  storage, read-after-write behavior, or cleanup.
- There is no database state, per-test namespace, unique ID strategy, cleanup fixture, or
  post-test cleanup assertion.
- Parallel safety is claimed but not demonstrated. Shared output directories and external
  systems make the current default especially risky.
- Two automatic reruns are globally applied instead of diagnosing or quarantining a
  specific flaky test with evidence.

### Diagnostics and reporting

- A rotating logger and failure screenshot/video attempt are useful starts.
- Logs are shared across xdist workers and are not attached by the CI workflow.
- No Playwright trace, console error, page error, failed-request, or response evidence is
  captured.
- The API client logs only method, URL, and status. It does not provide safe, redacted
  request/response diagnostics or correlation IDs.
- `failure_intel.py` is an unused string classifier and cannot support the README's failure
  intelligence claims.
- Allure Python integration is configured, but the CLI and Java runtime are absent and the
  workflow uploads only raw results. No rendered report is demonstrated.
- The workflow artifact upload does not use an unconditional step, so earlier failure may
  prevent useful evidence from being retained.

### API, contract, database, and integration design

- The Requests `Session` wrapper and endpoint class are reasonable seeds.
- Sessions are never explicitly closed, dependency injection is absent, and response
  handling is minimal.
- `requirements.txt` omits packages directly imported by tracked code: `fastapi`,
  `uvicorn`, and `jsonschema` (with Pydantic arriving only transitively if FastAPI is
  installed).
- Dependencies have no versions or lock/constraints file, so installs are not reproducible.
- `api/schemas/user_schema.py` and `contracts/user_schema.json` define incompatible user
  shapes; the Python version is unused.
- The contract test is located under `tests/api/orders` but validates a JSONPlaceholder
  user, which obscures ownership and intent.
- No response schema validation covers create-user or auth responses.
- There is no database implementation or database validation.
- There is no test that crosses UI, API, and database boundaries.

### External dependencies

- All UI tests use SauceDemo, and two API tests use JSONPlaceholder. Availability, data,
  behavior, throttling, and change control belong to third parties.
- The local auth mock controls only two small API tests and is not integrated with the UI
  or a database.
- This contradicts claims of deterministic, environment-agnostic execution.

### GitHub Actions

- The workflow is syntactically valid and uses current major versions of checkout,
  setup-python, and artifact upload.
- It has no top-level least-privilege `permissions`, concurrency cancellation, dependency
  cache, job timeout, service readiness check, test matrix, or explicit browser scope.
- It installs unpinned dependencies and browsers but does not start the mock auth service.
  The auth tests would therefore be expected to fail by connection refusal.
- `playwright install` does not explicitly install Linux system dependencies.
- Only raw Allure results are uploaded; logs, screenshots, videos, traces, JUnit, and
  container logs are omitted.
- The displayed README "Build Passing" badge is static and is not tied to this workflow.

### Jenkins, Docker, Compose, Kubernetes, and health checks

- The Jenkinsfile is a plausible sketch, but uses an unqualified agent, global package
  installation, no virtual environment, no timeout, no service startup/readiness, and only
  a narrow smoke command. It cannot be called demonstrated.
- The Dockerfile is a plausible start but uses unpinned dependencies, a root user, no
  health check, no explicit test target, and no reproducible lock data.
- `.dockerignore` does not exclude local-only Markdown files. A local Docker build would
  copy untracked private local files into the image because `COPY . .` includes the build
  context. This must be corrected before any build.
- No Docker Compose file exists, so the repository cannot orchestrate an API and database.
- The Kubernetes job refers to a local `:latest` image and provides no registry, pull
  policy, configuration, secret strategy, resources, or artifact transport. Kubernetes is
  unnecessary for the focused portfolio.
- No service provides a health endpoint and no command waits for readiness.

### Secrets and repository hygiene

- No tracked private local file or obvious real credential was found.
- Demo passwords and tokens are clearly hard-coded test values, but should be labeled as
  such and kept out of logs.
- The two required private local files are currently protected only by this clone's
  `.git/info/exclude`. A tracked ignore pattern would provide defense in depth without
  naming or publishing either file.
- Docker build-context exclusions need the same defense.
- No least-privilege workflow permissions are declared.

### README accuracy and unsupported claims

The README is detailed, but much of it describes an intended architecture rather than
the tracked implementation.

Claims requiring removal or qualification include:

- static "Build Passing"
- production-style, enterprise-ready, and production-ready positioning
- deterministic and environment-agnostic execution
- safe parallel execution
- complete UI/API/integration coverage
- centralized and context-rich API logging
- failure diagnosis without reruns
- screenshot/video/trace artifact linkage in CI
- externalized configuration
- scalable governance, ownership, and team adoption

The README should lead with a small, verifiable demo, exact setup commands, expected test
counts, architecture boundaries, limitations, and evidence links. Career claims should
not be presented as repository capabilities unless the repository demonstrates them.

## Feature classification

| Major feature | Classification | Evidence |
|---|---|---|
| Tracked Python/JSON/YAML syntax | Working and demonstrated | 44 Python, 2 JSON, and 3 YAML files parsed |
| Page-object separation | Implemented but not demonstrated | Seven page modules support three UI test functions |
| UI login and checkout tests | Implemented but not demonstrated | Static test code exists; dependencies/browser unavailable |
| Public JSONPlaceholder API tests | Implemented but not demonstrated | Two tests and a Requests client exist |
| Local auth mock and tests | Partially implemented | Code exists; undeclared runtime dependencies and no health check |
| API schema validation | Partially implemented | One contract test; duplicate incompatible schema is unused |
| Unified configuration | Broken | Multiple hard-coded URLs; settings module empty; environment class unused |
| Deterministic test data and cleanup | Documentation only | No owned persistent data or cleanup lifecycle |
| Database validation | Recommended learning target | No database code or tests exist |
| Service integration tests | Documentation only | Integration directory contains only `__init__.py` |
| UI-to-API-to-database workflow | Recommended learning target | No such workflow exists |
| Cross-browser smoke execution | Documentation only | Custom fixture always launches Chromium |
| Parallel execution | Broken | Enabled by default without shared-artifact or data isolation |
| Retry strategy | Unnecessary for this portfolio | Duplicate global retries can conceal failures |
| Screenshot and video diagnostics | Partially implemented | Failure hook exists but lifecycle and CI retention are unreliable |
| Traces, console/page/network evidence | Documentation only | No implementation |
| Logging | Partially implemented | Shared rotating log; limited API logging; no CI publication |
| Allure reporting | Partially implemented | Plugin config exists; CLI/Java/report publication absent |
| GitHub Actions | Partially implemented | Syntax valid; services, safety controls, caching, and full artifacts absent |
| Jenkins | Partially implemented | Declarative sketch only; not validated |
| Docker image | Partially implemented | Dockerfile exists; build unavailable and privacy/reproducibility issues exist |
| Docker Compose | Recommended learning target | Required for target outcome but no file exists |
| Kubernetes job | Unnecessary for this portfolio | Decorative, unvalidated, and outside the focused outcome |
| Ownership mapping | Redundant | Two entries, no loader or CI integration |
| Observability metadata/failure classifier | Redundant | Unused modules supporting unsupported claims |
| External test-data JSON | Redundant | Valid JSON but no consumer |

## Modernization alternatives

| Option | Advantages | Disadvantages | Decision |
|---|---|---|---|
| A. Refactor current architecture | Maximum path continuity; smallest file movement | Hard-coded external systems, lifecycle design, missing DB, and decorative layers would force extensive patching around weak foundations | Not preferred |
| B. Replace selected internals while preserving useful code and Git history | Keeps recognizable assets and evolution history while establishing a controlled app, fixtures, diagnostics, and evidence | Requires deliberate migration and temporary duplication at checkpoints | **Recommended** |
| C. Build a new architecture temporarily and migrate selectively | Clean experimentation boundary | Encourages a parallel project, increases review burden, and can obscure useful history | Use only if an approved spike proves a risky design question |

This is not a rewrite for convenience. The migration should retain concepts and selected
code only when tests prove they still serve the target architecture.

## Repository naming review

`sdet-playwright-framework` remains understandable while Playwright is the primary UI
automation tool. It becomes narrower than the intended final evidence once API,
PostgreSQL, integration, diagnostics, and CI orchestration are equally visible.

### Keep `sdet-playwright-framework`

Advantages:

- preserves all existing links, clones, badges, bookmarks, and recruiter references
- retains current search recognition and continuity
- accurately names the UI automation engine

Disadvantages:

- can make API/database/integration work look secondary
- describes a tool-centric framework rather than a broader quality-engineering portfolio

### Consider `sdet-quality-engineering-portfolio` after implementation

Advantages:

- describes the multi-layer outcome without over-centering one tool
- supports accurate UI, API, database, integration, and CI storytelling

Disadvantages:

- is longer and less specific about Playwright
- requires updating clone URLs, local remotes, badges, documentation links, résumé links,
  bookmarks, and any external references
- old links may redirect on GitHub, but redirects can be disrupted if the old name is reused

Recommendation: **do not rename now**. Keep the current public name through
modernization, verify that the broader scope is genuinely demonstrated, and request
explicit approval before any later rename.

## Phase 0 conclusion

### What currently works

- repository safety and local-only file exclusion
- parseable Python, JSON, and YAML source
- a coherent page-object and API-client starting shape
- small UI/API examples, a mock auth concept, and basic logging/artifact intent
- syntactically valid GitHub Actions, Jenkins, Docker, and Kubernetes starting files

### What is broken, incomplete, redundant, or documentation-only

- reproducible setup and all runtime evidence
- complete dependencies and version pinning
- controlled UI/API/database system, database validation, and real integration coverage
- parallel safety, retry policy, cross-browser execution, and deterministic cleanup
- diagnostics lifecycle and CI artifact publishing
- CI service orchestration and health checks
- README claims that exceed implementation evidence
- decorative Kubernetes, ownership, observability, empty integration, and unused data/schema
  assets

Proceed only after the approval decisions in
`docs/FRAMEWORK_MODERNIZATION_PLAN.md` are resolved.
