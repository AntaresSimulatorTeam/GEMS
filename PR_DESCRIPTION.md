## Summary

This PR introduces CI/CD governance infrastructure for the GEMS repository: structured GitHub issue templates aligned with the formal process framework, automated Antares update detection with integrated E2E test validation, and a complete linting/type-checking pipeline.

---

## Changes

### 1. GitHub Issue Templates (new)

Five dedicated issue templates — one per governance process — replacing the previous generic `process-change.yml` template. Each template includes a full Steps 1–10 checklist with process-specific deviations.

- **`doc-01.yml`** — Antares Simulator evolution impact on GEMS Language documentation
  - Captures: previous/new Antares version, trigger, impact on GEMS Language, interpreter support status, validation strategy
  - Full checklist Steps 1–10; deviation: Step 4 documentation update precedes implementation
- **`doc-02.yml`** — Internal documentation improvement
  - Captures: change type (new content / correction / restructuring / translation), description, affected doc sections
  - Full checklist Steps 1–10; deviation: Step 8 versioning may be patch-only
- **`lt-01.yml`** — Antares Simulator evolution impact on model libraries and taxonomies
  - Captures: Antares versions, affected libraries (free-text, reads from `libraries/`), validation strategy
  - Full checklist Steps 1–10; deviation: Step 4 enforces alignment with GEMS Language semantics
- **`lt-02.yml`** — Internal library or taxonomy development
  - Captures: affected library, change type (major/minor/patch), whether optimization results are impacted
  - Full checklist Steps 1–10; deviation: Step 5 validates no unintended changes to optimization results
- **`lt-03.yml`** — New library or taxonomy
  - Captures: library name, description, design overview, use cases, proof-of-concept plan
  - Full checklist Steps 1–10 with mandatory design phase before implementation; full E2E validation required before release

### 2. Scheduled Antares Update Workflow (`check-antares-update.yml`) — new

Daily (06:00 UTC) automated check for a new stable Antares Simulator release.

- **`check-update` job** — Fetches all GitHub tags, filters pre-releases (rc/alpha/beta/nightly), compares with `antares_simulator_version` in `dependencies.json`; if a new version is found, fetches release notes from the GitHub API and creates a triage issue containing: version table, release notes, triage checklist (DOC-01 / LT-01 routing), and detailed task checklists (Validation, Compatibility, Documentation, Decision)
- **`e2e-new-version` job** — Calls the reusable `run-e2e-tests.yml` workflow against the new Antares version (no repo change); exposes `test_outcome` as output
- **`post-results` job** — Runs `if: always()`; posts E2E test result (pass/fail + run link) as a comment on the triage issue

### 3. Reusable E2E Workflow (`run-e2e-tests.yml`) — new

Extracts all E2E test steps into a reusable `workflow_call` workflow to avoid duplication between `e2e-tests.yml` and `check-antares-update.yml`.

- Inputs: `antares_version` (required), `artifact_name` (optional, default `e2e-test-failures`)
- Output: `test_outcome` (success or failure) — available to callers even when the job fails
- Steps: checkout, Python setup, install dependencies, override `antares_simulator_version` in `dependencies.json`, download binary, extract, run tests (`continue-on-error: true`), upload artifacts on failure, cleanup, fail if tests failed

### 4. E2E Tests Workflow (`e2e-tests.yml`) — updated

- Reads Antares version dynamically from `dependencies.json` in a `read-version` job (was hardcoded as `9.3.2`)
- Calls the reusable `run-e2e-tests.yml` workflow — E2E logic no longer duplicated
- Updated action versions: `actions/checkout@v6`, `actions/setup-python@v6`

### 5. Lint, Format and Tests Workflow (`lint-format-and-tests.yml`) — new

Two jobs:

- **`lint` job** — runs all checks in sequence:
  - `ruff check tests/` and `ruff format --check tests/`
  - `mypy` (configuration driven by `pyproject.toml`)
  - `yamllint -c .yamllint.yml libraries/ resources/ .github/workflows/`
- **`unit-tests` job** — runs `pytest tests/unit_tests -v`

### 6. Tool Configuration (`pyproject.toml`) — new

- Ruff configuration: Python 3.11 target, 100-char line length, rules E/W/F/I/UP/B/C4/RUF, E501 ignored (handled by formatter), isort first-party set to `tests`
- Mypy strict mode: covers `tests/` directory; excludes `tests/e2e_tests/test_*` and `tests/e2e_tests/conftest.py` (pytest fixture injection is not mypy-compatible); utility modules `env.py` and `utils.py` are fully type-checked

---

## Version Tracking — `dependencies.json`

`dependencies.json` at the repo root is the single source of truth for all component versions. All workflows read from it dynamically — no version is hardcoded anywhere in CI:

```json
{
    "antares_simulator_version": "10.0.0",
    "gems_language_version": "1.0.0",
    "basic_models_library_version": "1.0.0",
    "antares_legacy_models_version": "1.0.0",
    "pypsa_models_version": "1.0.0",
    "andromede_models_version": "1.0.0"
}
```

---

## Testing

- All unit and E2E tests pass locally on the branch (`python -m pytest tests/ -v`)
- `ruff check tests/` and `ruff format --check tests/` pass with no violations
- `mypy` (strict) passes on `tests/e2e_tests/env.py`, `tests/e2e_tests/utils.py`, and all unit tests
- `yamllint` passes on all YAML files in `libraries/`, `resources/`, and `.github/workflows/`

---

## Process Reference

| Process | Template | Trigger |
|---------|----------|---------|
| DOC-01  | `doc-01.yml` | Manually opened from triage issue created by `check-antares-update.yml` |
| DOC-02  | `doc-02.yml` | Manual |
| LT-01   | `lt-01.yml` | Manually opened from triage issue created by `check-antares-update.yml` |
| LT-02   | `lt-02.yml` | Manual |
| LT-03   | `lt-03.yml` | Manual |
| Antares version detection | — | `check-antares-update.yml` (daily cron, auto-creates triage issue) |
