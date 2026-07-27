# AI-Assisted Engineering

## Working model

AI assistance may draft plans, code, tests, fixes, commands, and documentation. Those
drafts are not evidence by themselves. The SDET remains responsible for requirements,
architecture, test intent, risk coverage, execution, review, debugging, claim accuracy,
and release judgment.

For this modernization, AI-assisted work included repository analysis, implementation
drafts, test-framework structure, CI configuration, and documentation. Human direction
defined the approved architecture, PostgreSQL priority, removal scope, safety boundaries,
runtime constraints, reporting direction, and publication restrictions.

## Required human review

The SDET reviews:

- whether each test represents a meaningful risk
- selectors and page-object responsibilities
- exact statuses, schemas, database values, and expected outcomes
- unique test-data ownership and cleanup behavior
- timeout and error handling
- failure evidence for usefulness and privacy
- dependency and action versions
- Docker and CI behavior after actual execution
- every résumé, LinkedIn, README, and interview claim

Generated code is held to the same lint, formatting, type, test, and runtime gates as
human-written code.

## Evidence rule

The repository distinguishes:

- **implemented**: code or configuration exists and has passed relevant static checks
- **demonstrated**: the required runtime command executed successfully with recorded
  evidence
- **blocked**: implementation exists, but a missing runtime or approval boundary prevents
  the required execution
- **planned**: the capability is not implemented

AI output cannot move a capability from implemented to demonstrated. Only executable
evidence can.

## Privacy and safety

AI-assisted work must not place local context, personal paths, credentials, employer or
client information, environment dumps, or private files in code, logs, prompts intended
for publication, reports, Docker contexts, or commits.

Repository-local private Markdown files, real `.env` files, environments, caches, and
generated evidence are ignored. Failure diagnostics retain allowlisted metadata rather
than bodies, headers, cookies, or authorization values.

## Direct versus assisted implementation

Git history records engineering outcomes, not authorship percentages. A truthful summary
is:

- project scope and approval boundaries were human-directed
- implementation and documentation were AI-assisted
- commands and results were reviewed against the repository state
- isolated execution was demonstrated locally
- Docker/PostgreSQL and CI results remain unclaimed until a human-authorized runtime
  validation occurs

This is evidence of supervised AI-assisted engineering, not a claim that automation
replaced SDET reasoning.
