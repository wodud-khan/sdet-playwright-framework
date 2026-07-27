# Repository Working Agreement

## Scope and safety

- Work only in this repository and only on a non-main branch.
- Never commit or expose local-only context, environment, or pull-request files.
- Do not push, merge, publish, release, open pull requests, rename the repository, or
  change GitHub settings without explicit authority.
- Do not add real credentials, employer/client material, or private data.
- Keep generated reports, browser artifacts, environments, and local databases ignored.
- Do not use destructive Git commands or broad filesystem deletion.

## Architecture

- Python 3.12 is the supported runtime.
- PostgreSQL is the primary integration runtime. SQLite is limited to isolated unit tests
  or an explicitly labeled lightweight application check.
- Test code uses Pytest and official pytest-playwright fixtures.
- Keep UI, API, database, integration, and end-to-end intent in distinct test directories.
- Core tests must not depend on third-party websites or services.

## Test policy

- Run serially by default; parallel execution is an explicit validation command.
- Never add blanket retries or weaken an assertion to make a test pass.
- Create unique state per test and clean up only records owned by that test.
- Prefer Playwright web-first assertions and semantic locators.
- Capture failure evidence without logging credentials, cookies, authorization headers, or
  private files.

## Quality gates

Use the locked uv workflow:

```bash
uv sync --extra dev --locked --python 3.12
```

Run the applicable gates before handing off a checkpoint:

```bash
.venv/bin/python -m pytest --collect-only -q
.venv/bin/ruff check .
.venv/bin/ruff format --check .
.venv/bin/mypy src scripts
.venv/bin/python -m pytest -q
git diff --check
```

Docker-dependent changes also require:

```bash
docker compose config
docker compose up -d --build
```

If a required tool is unavailable, report the exact blocker rather than claiming success.

## Documentation and claims

- Keep README commands copied from validated execution.
- Describe only implemented and demonstrated capabilities.
- Avoid claims such as enterprise-grade, production-ready, complete, or guaranteed.
- Treat AI output as draft engineering work subject to human requirements, review,
  debugging, and release judgment.
