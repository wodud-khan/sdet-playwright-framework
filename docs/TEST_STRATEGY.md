# Test Strategy

| Layer | Main assertion | Runtime |
|---|---|---|
| Unit | Input rules, cleanup, diagnostics, SQLite behavior | Python |
| API | Exact REST status and payload | App + PostgreSQL |
| Contract | Public response against standalone JSON Schema | App + PostgreSQL |
| Database | Exact persisted row through psycopg | PostgreSQL |
| Integration | API deletion reflected in SQL | App + PostgreSQL |
| UI | Form controls and feedback, including mocked 503 recovery | App + browser |
| E2E | UI creation through API/SQL and exact-ID cleanup | App + PostgreSQL + Chromium |

Run serial suites before the existing two-worker and three-browser smoke commands in the [README](../README.md). Do not treat the SQLite repository checks or focused SQLite UI run as PostgreSQL evidence. The controlled child E2E test intentionally fails after UI creation and then verifies exact-ID absence; the outer test passes only when cleanup succeeds.

Unexpected browser console, page, request, and HTTP errors fail a test. A test may declare an exact method/path/status/count before an expected HTTP error; repeated identical responses use one declaration with `count`, and duplicate declarations are rejected. Other events remain failures. Negative API tests inspect non-2xx responses directly. The JSON contract is independent of application model classes.
