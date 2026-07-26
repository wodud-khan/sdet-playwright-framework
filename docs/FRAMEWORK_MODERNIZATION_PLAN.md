# Framework Modernization Plan

## Status and decision gate

Phase 0 auditing completed before implementation began. The modernization direction was
approved after the audit, and an approval message was interpreted as authorization to
begin implementation on `refactor/sdet-framework-modernization`. Publication and
repository administration remain out of scope.

Implementation status:

- Phase 0 repository audit: completed; no implementation occurred during that audit
- Modernization direction: approved
- Checkpoint 0: approved
- Checkpoint 1: partially implemented and partially validated
- Checkpoint 2: partially implemented and incomplete
- Checkpoints 3–7: pending
- Docker and PostgreSQL runtime validation: blocked because Docker is not installed

Observed evidence for the partial candidate:

- Python 3.12.11 environment created through uv
- 49 installed packages passed `uv pip check`
- six unit tests collected and passed
- Ruff lint and formatting checks passed
- Mypy passed for the current source and readiness script
- a local SQLite-backed health/create/read/delete flow returned expected HTTP statuses
- Compose YAML parsed successfully

Incomplete or blocked evidence:

- the documented pip-based commands do not work in the current uv environment because it
  intentionally has no pip module
- a fresh-clone install has not yet been replayed from an empty environment
- no PostgreSQL runtime, Docker build, or Docker Compose command has executed
- API, contract, direct PostgreSQL, integration, browser, E2E, parallel, cross-browser,
  diagnostics, reporting, and CI validation remain pending

No implementation checkpoint is complete merely because files were created. A capability
is public evidence only after its required runtime validation passes.

Recommended strategy: **selectively rebuild the internals while preserving useful code,
concepts, public repository continuity, and Git history (Option B).**

This recommendation is proportional to the evidence:

- a focused page-object/API-client/test skeleton is worth preserving
- the current runtime, external dependencies, lifecycle, data strategy, diagnostics, and
  claims are not a safe foundation to expand in place
- a separate replacement repository would discard useful history and make review harder

## Desired outcome

Deliver a small local order application backed by PostgreSQL and a test framework that
demonstrates:

- Python, Pytest, and Playwright
- focused UI testing
- REST API behavior and schema testing
- direct database validation
- API/database integration tests
- one complete UI-to-API-to-database workflow
- unique data and targeted cleanup
- reliable serial and bounded parallel execution
- Chromium, Firefox, and WebKit smoke coverage
- failure traces, screenshots, browser/API/database evidence, logs, and reports
- GitHub Actions and Docker Compose
- accurate, evidence-based documentation

The result remains an independent portfolio system. It must not imply employer code,
production scale, or unproven infrastructure expertise.

## Change disposition

### Reconciled disposition of baseline deletions

The 51 deleted tracked files were reviewed against the baseline. Their final disposition
is grouped below; Git history and the retained local safety stash preserve the original
content.

| Deleted baseline area | Final disposition | Rationale or migration target |
|---|---|---|
| `.flake8` | Remain deleted | Ruff configuration in `pyproject.toml` is the stronger equivalent |
| `Jenkinsfile` | Remain deleted | Unvalidated secondary CI inflated scope; GitHub Actions is the approved public path |
| `api/client/*` and `api/endpoints/*` | Legacy files remain deleted; migrate useful client/session concepts | A typed, injected client under `src/test_framework/api/` will replace hard-coded external URLs |
| `api/config/api_capabilities.py` | Remain deleted | It documented a removed third-party API rather than executable capability |
| `api/schemas/*` | Remain deleted | The unused Python user schema conflicted with the tracked JSON contract |
| `config/env.py` and empty `config/settings.py` | Remain deleted | `src/test_framework/config.py` is the validated replacement |
| legacy `conftest.py` | Remain deleted; replace | A new fixture layer will use official pytest-playwright fixtures and safe finalizers |
| `k8s/test-job.yaml` | Remain deleted | Kubernetes is outside the focused portfolio |
| `mock_services/auth_service/*` | Remain deleted | The controlled order application is a stronger owned system under test |
| `observability/metadata.py` and `ownership/test_ownership.yaml` | Remain deleted | Both were decorative and had no consuming workflow |
| `pages/*` | Legacy files remain deleted; migrate the page-object concept | New semantic page/component objects will target the controlled UI |
| `pytest.ini` | Remain deleted | Pytest configuration moves to `pyproject.toml`; blanket reruns and implicit parallelism stay removed |
| `requirements.txt` | Remain deleted | One uv-based locked workflow will replace unbounded incomplete requirements |
| legacy `tests/api/*` | Remain deleted; replace | New API, contract, database, and integration tests will use the controlled app and PostgreSQL |
| legacy `tests/ui/*` | Remain deleted; replace | New Playwright tests will use semantic locators and the controlled UI |
| `tests/data/users.json` | Remain deleted | Worker-aware factories will replace unused shared static data |
| `utils/api_helpers.py` and `utils/schema_validator.py` | Migrate only useful behavior | JSON response and schema checks belong in typed clients/contract helpers |
| `utils/data_factory.py` | Replace | A unique run- and worker-aware factory will replace shared credentials |
| `utils/failure_intel.py` | Remain deleted | String matching did not provide actionable diagnostics |
| `utils/logger.py` | Replace | Structured, redacted, test-scoped evidence will replace a shared rotating file |
| empty package files under removed legacy directories | Remain deleted | No empty directories are retained for appearance |

`README.md` remains from the baseline until executable evidence is mature enough to
replace its unsupported claims accurately.

The still-tracked `contracts/user_schema.json` is not part of the deletion count. It will
be replaced by one canonical order contract when the contract suite is implemented.

### Database priority

PostgreSQL is the primary persistent integration runtime. Direct database, integration,
UI-to-API-to-database, Docker Compose, CI, résumé, and LinkedIn claims must be supported by
executed PostgreSQL evidence.

SQLite is allowed only for isolated unit tests and an optional lightweight application
check. It is not an equal primary architecture and must not be the default for any public
integration or end-to-end command.

### Retain

| Asset or idea | Retention approach |
|---|---|
| Git history and current repository | Keep all evolution visible on the existing branch/repository |
| Page-object separation | Preserve the intent; migrate useful behavior behind semantic locators |
| Requests API-client boundary | Preserve a synchronous typed client concept with injected settings and safe diagnostics |
| JSON Schema validation | Keep one canonical contract per response and expand meaningful coverage |
| Pytest markers and layered test organization | Keep only markers backed by real tests |
| Local mock/controlled-service idea | Evolve into a small owned demo app with health/readiness behavior |
| Failure screenshot/logging intent | Rebuild around supported Playwright lifecycle and per-test evidence |
| GitHub Actions and Dockerfile starting points | Replace contents incrementally and preserve history |
| Login/checkout test intent | Use as migration references where the local workflow has equivalent value |

### Refactor

| Current area | Required refactor |
|---|---|
| `conftest.py` | Use official pytest-playwright fixtures, typed settings, safe finalizers, worker-specific artifacts, and service fixtures |
| `pages/` | Move to the target package, inject base URL, use roles/labels/test IDs and Playwright `expect` |
| `api/` | Consolidate clients/config/schemas, close sessions, standardize timeouts/errors, redact diagnostics |
| `config/` | Replace unused/empty modules with one validated settings object |
| `tests/api` | Point to the controlled app, align filenames with intent, add negative and contract checks |
| `tests/ui` | Point to the controlled UI and separate smoke, behavior, and full E2E intent |
| `utils/logger.py` | Use run/test context, worker-safe output, and CI attachment integration |
| `pytest.ini` | Move configuration to `pyproject.toml`, remove duplicate/global reruns and default `-n auto` |
| `requirements.txt` | Replace unpinned/incomplete metadata with declared bounded dependencies and a reproducible lock/constraints path |
| `.github/workflows/playwright-tests.yml` | Replace with explicit quality gates, service lifecycle, least permissions, timeouts, caching, matrix, and always-uploaded artifacts |
| `Dockerfile` and `.dockerignore` | Use reproducible dependencies, non-root runtime where practical, explicit target, and private-file exclusions |
| `README.md` | Replace aspirational claims with verified setup, architecture, commands, results, limitations, and artifact examples |

### Remove

Removal means deletion in an implementation commit; Git history will retain prior content.

| Asset | Reason |
|---|---|
| `k8s/test-job.yaml` and empty `k8s/` | Unvalidated and unnecessary for the focused portfolio |
| `ownership/test_ownership.yaml` | Decorative; no consuming code or credible team workflow |
| `observability/metadata.py` | Unused Allure labeling does not demonstrate observability |
| `utils/failure_intel.py` | Unused string matching supports an overstated claim |
| `utils/api_helpers.py` | Trivial unused helper |
| `tests/data/users.json` | Unused shared static data |
| Duplicate/unused `api/schemas/user_schema.py` | Conflicts with the tracked JSON contract |
| Empty `config/settings.py` and empty test-category packages | Decorative until real behavior exists |
| Blanket `pytest-rerunfailures` defaults | Retries must not conceal instability |
| Primary Allure dependency/configuration | Java/CLI adds friction without a demonstrated report; use HTML/JUnit and native traces |
| Jenkinsfile from the primary outcome | GitHub Actions is sufficient; retain only if explicitly approved and validated |
| Third-party SauceDemo/JSONPlaceholder dependencies | Core portfolio evidence must use the controlled local system |

### Add

| Addition | Purpose |
|---|---|
| `pyproject.toml` plus reproducible dependency lock/constraints | One source for package, Pytest, Ruff, and Mypy configuration |
| `src/demo_app/` | Minimal FastAPI UI/API under test |
| `src/test_framework/` | Typed reusable config, clients, pages, diagnostics, and factories |
| `compose.yaml` | Start the app and PostgreSQL with explicit health checks |
| PostgreSQL schema/model | Provide genuine persistent state and database evidence |
| `/health` and readiness polling | Replace startup sleeps with bounded state checks |
| `.env.example` | Document safe local configuration names/defaults |
| Unit, contract, database, integration, UI, and E2E tests | Back every advertised test layer with executable evidence |
| Unique run/worker data factories and cleanup registry | Make state-changing tests repeatable and parallel-safe |
| Native Playwright traces/screenshots and browser event capture | Make UI failures diagnosable |
| Redacted API and labeled database evidence | Make non-UI failures diagnosable without leaking data |
| HTML and JUnit reports | Provide low-friction human/CI outputs |
| `docs/TEST_STRATEGY.md` and `docs/TROUBLESHOOTING.md` | Explain risk coverage, commands, evidence, and common failure recovery |
| GitHub Actions quality workflow | Demonstrate reproducible gates and artifact retention |

## Proposed directory structure

```text
.
├── .github/workflows/quality.yml
├── contracts/order.schema.json
├── docs/
├── scripts/wait_for_services.py
├── src/
│   ├── demo_app/
│   │   ├── api/
│   │   ├── static/
│   │   ├── database.py
│   │   ├── main.py
│   │   ├── models.py
│   │   └── schemas.py
│   └── test_framework/
│       ├── api/client.py
│       ├── db/client.py
│       ├── pages/orders_page.py
│       ├── config.py
│       ├── data_factory.py
│       └── diagnostics.py
├── tests/
│   ├── unit/
│   ├── api/
│   ├── contract/
│   ├── database/
│   ├── integration/
│   ├── ui/
│   └── e2e/
├── .dockerignore
├── .env.example
├── .gitignore
├── compose.yaml
├── conftest.py
├── Dockerfile
├── pyproject.toml
└── README.md
```

Do not create an empty directory simply to match this proposal.

## Proposed tools

Exact versions will be chosen and validated during approved implementation.

| Tool | Why needed |
|---|---|
| Python 3.12 | Stable common runtime aligned with the current CI intent |
| Pytest | Unified fixtures, markers, selection, and reporting |
| pytest-playwright and Playwright | Supported browser lifecycle, cross-browser execution, and native evidence |
| Requests | Clear synchronous black-box REST client |
| FastAPI, Uvicorn, and Pydantic | Small controlled API/UI host with explicit contracts |
| PostgreSQL and psycopg 3 | Real persistence plus independent SQL validation |
| JSON Schema | Black-box response validation separate from app models |
| pytest-xdist | Bounded parallel proof after isolation is established |
| Ruff | One deterministic lint/format tool replacing overlap |
| Mypy | Focused type checking for framework and app boundaries |
| pytest-html and JUnit XML | Portable local/CI reports without Java |
| Docker and Docker Compose | Repeatable app/database orchestration |
| GitHub Actions | Automated public evidence and artifact retention |

Tools intentionally not proposed for the primary path: Kubernetes, paid/cloud services,
performance tools, security scanners presented as expertise, production observability
platforms, and default Allure/Jenkins requirements.

## Implementation checkpoints

Complexity is relative to this repository:

- **S**: small, isolated change with limited interaction risk
- **M**: several files or one cross-cutting boundary
- **L**: multiple components and runtime validation

### Checkpoint 0 — Approval and baseline

Complexity: **S**

Deliverables:

- owner answers all approval questions below
- branch/root/safety checks are repeated
- clean baseline status and audit commit boundary are recorded
- dependency/network and Docker availability are explicitly authorized or deferred

Validation:

```bash
pwd
git branch --show-current
git status --short --branch
git diff --check
```

Exit criterion: implementation scope and allowed installation/network actions are explicit.

### Checkpoint 1 — Project metadata, safety, and honest skeleton

Complexity: **M**

Deliverables:

- add tracked ignore defenses for private local files and Docker build context
- introduce `pyproject.toml` and an agreed lock/constraints mechanism
- establish Python 3.12, Ruff, Mypy, Pytest, and marker configuration
- remove blanket reruns and implicit `-n auto`
- add `.env.example`
- delete only approved decorative/unused files
- make test collection pass before application behavior is added

Validation:

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -e ".[dev]"
.venv/bin/python -m pytest --collect-only -q
.venv/bin/ruff check .
.venv/bin/ruff format --check .
.venv/bin/mypy src
git status --short --ignored
git diff --check
```

Exit criterion: dependencies install reproducibly, safety checks pass, and every remaining
directory has a purpose.

### Checkpoint 2 — Controlled app and PostgreSQL orchestration

Complexity: **L**

Deliverables:

- implement minimal order API and static UI
- implement PostgreSQL persistence and narrowly scoped schema initialization
- add app/database health checks
- add Compose services and a multi-stage/non-root Dockerfile where practical
- add bounded readiness polling with actionable failures
- add unit tests for app validation and framework-free helpers

Validation:

```bash
docker compose config
docker compose build
docker compose up -d
.venv/bin/python scripts/wait_for_services.py
curl --fail --silent http://127.0.0.1:8000/health
.venv/bin/python -m pytest tests/unit -q
docker compose ps
```

Exit criterion: the owned UI/API/database system starts reliably and reports healthy
without arbitrary sleeps.

### Checkpoint 3 — Framework core and isolated API/database tests

Complexity: **L**

Deliverables:

- implement immutable validated settings
- implement typed API and database clients with explicit lifecycles
- add redacted diagnostics
- implement unique run/worker-aware data factories
- add API, contract, database, and API-to-database integration tests
- guarantee targeted cleanup through finalizers

Validation:

```bash
.venv/bin/python -m pytest tests/api -q
.venv/bin/python -m pytest tests/contract -q
.venv/bin/python -m pytest tests/database -q
.venv/bin/python -m pytest tests/integration -q
.venv/bin/python -m pytest -m "api or contract or database or integration" -n 2
.venv/bin/ruff check .
.venv/bin/mypy src
```

Exit criterion: service/data tests pass serially and in a bounded two-worker run with no
residual records.

### Checkpoint 4 — UI framework and complete E2E workflow

Complexity: **L**

Deliverables:

- use pytest-playwright's fixtures without shadowing `page`
- implement semantic page/component objects and web-first assertions
- add focused UI validation and one critical smoke flow
- implement the UI-create → API-read → database-verify → API-delete → database-absence E2E
  test
- prove cleanup even when an intermediate assertion fails

Validation:

```bash
.venv/bin/python -m playwright install chromium
.venv/bin/python -m pytest tests/ui --browser chromium -q
.venv/bin/python -m pytest tests/e2e --browser chromium -q
.venv/bin/python -m pytest -m smoke --browser chromium -q
```

Exit criterion: the full controlled workflow passes repeatedly and leaves no owned state.

### Checkpoint 5 — Failure evidence, cross-browser smoke, and parallel proof

Complexity: **M**

Deliverables:

- retain failure-only traces/screenshots and selected video
- record browser console errors, page errors, failed requests, and safe response metadata
- publish safe API/database/app/Compose diagnostics
- generate HTML and JUnit reports
- prove a small Chromium/Firefox/WebKit smoke matrix
- prove bounded parallel execution without shared-path collisions
- document one intentional local failure drill, then revert the failure

Validation:

```bash
.venv/bin/python -m playwright install chromium firefox webkit
.venv/bin/python -m pytest -m smoke --browser chromium --browser firefox --browser webkit
.venv/bin/python -m pytest -m "not ui and not e2e" -n 2
.venv/bin/python -m pytest tests/ui -n 2 --browser chromium
.venv/bin/python -m pytest --html=artifacts/report.html --self-contained-html \
  --junitxml=artifacts/junit.xml
```

Exit criterion: supported browsers pass smoke coverage and a first failure produces the
documented, private-data-safe evidence bundle.

### Checkpoint 6 — GitHub Actions and container execution

Complexity: **L**

Deliverables:

- implement least-privilege workflow permissions, concurrency, and timeouts
- cache against lock/browser inputs
- run lint, format, types, unit, service-layer tests, Chromium E2E, and browser smoke
- use the same Compose lifecycle as local execution
- upload reports, browser artifacts, app logs, and Compose logs under `if: always()`
- validate the containerized test command

Validation:

```bash
docker compose run --rm tests .venv/bin/python -m pytest -m smoke --browser chromium
docker compose logs --no-color
.venv/bin/ruff check .
.venv/bin/ruff format --check .
.venv/bin/mypy src
.venv/bin/python -m pytest -q
git diff --check
```

The container command may be adjusted to the image's internal Python path; the final
README and workflow must use the exact validated form.

Exit criterion: local commands and CI commands agree, all required jobs pass, and failure
artifacts are retained.

### Checkpoint 7 — Documentation and final claim audit

Complexity: **M**

Deliverables:

- rewrite README quick start, structure, test strategy, expected results, and limitations
- add troubleshooting and artifact guides
- remove static success badges and unsupported enterprise/production claims
- document human review of AI-assisted work without overstating language mastery
- classify all public capabilities from final execution evidence
- revisit—but do not perform—the repository naming decision

Validation:

```bash
.venv/bin/python -m pytest --collect-only -q
.venv/bin/python -m pytest -q
.venv/bin/ruff check .
.venv/bin/ruff format --check .
.venv/bin/mypy src
docker compose config
git diff --check
git status --short --branch
```

Exit criterion: every README command is copied from a passing validation log and every
claim maps to implementation evidence.

## Validation matrix

These are the final named commands the implementation should converge on. A small
`Makefile` or script may provide aliases, but the underlying commands must remain visible.

| Gate | Proposed command |
|---|---|
| Discovery | `.venv/bin/python -m pytest --collect-only -q` |
| Unit | `.venv/bin/python -m pytest tests/unit -q` |
| API | `.venv/bin/python -m pytest tests/api -q` |
| Contract | `.venv/bin/python -m pytest tests/contract -q` |
| Database | `.venv/bin/python -m pytest tests/database -q` |
| Integration | `.venv/bin/python -m pytest tests/integration -q` |
| UI | `.venv/bin/python -m pytest tests/ui --browser chromium -q` |
| End-to-end | `.venv/bin/python -m pytest tests/e2e --browser chromium -q` |
| Cross-browser smoke | `.venv/bin/python -m pytest -m smoke --browser chromium --browser firefox --browser webkit` |
| Parallel service tests | `.venv/bin/python -m pytest -m "not ui and not e2e" -n 2` |
| Lint | `.venv/bin/ruff check .` |
| Format | `.venv/bin/ruff format --check .` |
| Types | `.venv/bin/mypy src` |
| Compose validity | `docker compose config` |
| Compose health | `docker compose up -d && .venv/bin/python scripts/wait_for_services.py` |
| Container smoke | `docker compose run --rm tests python -m pytest -m smoke --browser chromium` |
| Whitespace | `git diff --check` |

No destructive volume removal should be embedded in the ordinary validation command.
When an explicitly approved clean reset is needed, it must target only the named Compose
project volumes.

## Risks and mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Local Docker/Compose is unavailable | Controlled stack cannot be validated locally | Obtain explicit installation approval or use an already approved environment; do not claim success from CI alone |
| Python 3.14 differs from proposed 3.12 | Package/runtime divergence | Make 3.12 explicit in local setup, Docker, and CI |
| Dependency installation requires network | Phase 1 cannot start safely | Request one scoped approval after metadata is reviewed |
| Demo app consumes portfolio effort | Framework work becomes diluted | Enforce one workflow, minimal UI, and no product roadmap |
| Existing tests lose recognizable history | Reviewers may see a rewrite | Migrate in checkpoints, preserve concepts, and explain replacements in commits/docs |
| Parallel execution corrupts artifacts/state | Flaky or misleading results | Worker-specific paths, unique IDs, targeted cleanup, bounded workers, serial-first gates |
| Cleanup removes unrelated data | Data loss or cross-test interference | Query/delete by exact generated ID; forbid global cleanup |
| Diagnostics expose secrets/private files | Privacy/security incident | Redaction tests, allowlisted metadata, artifact review, build-context exclusions |
| Browser matrix lengthens feedback | Slow or costly CI | Full E2E on Chromium; only a small smoke test across three browsers |
| Allure/Jenkins/Kubernetes inflate claims | Shallow, unvalidated portfolio | Remove from primary path; add later only with an approved learning goal and evidence |
| README drifts from code | Unsupported public claims recur | Treat documented commands and claim classification as final release gates |
| Repository rename breaks references | Recruiter/user friction | Keep the current name until implementation is complete and approval is explicit |

## Approval questions

Implementation requires explicit answers to these decisions:

1. Approve Option B: selective internal rebuild on
   `refactor/sdet-framework-modernization`, preserving Git history?
2. Approve the controlled local order UI + FastAPI REST API + PostgreSQL system under test?
3. Approve Python 3.12 as the project runtime and a later scoped network/dependency install
   after version bounds/lock metadata are reviewed?
4. Approve replacing primary Allure reporting with native Playwright artifacts, HTML, and
   JUnit reports?
5. Approve removing Kubernetes, the current Jenkinsfile, decorative ownership/
   observability modules, unused data/schema/helpers, blanket retries, and third-party
   SauceDemo/JSONPlaceholder dependencies?
6. Docker and Docker Compose are not installed locally. Should implementation wait for a
   locally available Docker environment, or proceed through non-container checkpoints
   while marking Compose validation blocked?
7. Approve keeping `sdet-playwright-framework` during modernization and revisiting
   `sdet-quality-engineering-portfolio` only after the broader scope is demonstrated?

No repository rename, push, publication, merge, release, pull request, or GitHub settings
change is included in any approval above. Each would require separate explicit authority;
the current task expressly forbids them.

## Phase 0 stop record

Phase 0 ended with the original plan and required owner review. That boundary was honored:
implementation began only after the audit, following an approval message interpreted as
authorization to modernize. The current implementation status is governed by the
reconciliation record at the top of this document.
