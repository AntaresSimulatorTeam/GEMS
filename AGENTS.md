# AGENTS.md

This file provides guidance to AI coding agents (LLMs, copilots, code assistants) when working with this repository. It is tool-agnostic and should be read by any AI agent before making changes.

---

## Project Overview

**GEMS** (Generic Energy system Modelling Scheme) is a high-level algebraic modeling language for energy system optimization and foresight studies. This repository contains:

- **YAML model libraries** — reusable energy component models (`libraries/*.yml`)
- **Documentation site** — built with MkDocs + Material theme (`doc/`, `mkdocs.yml`)
- **Python test suite** — end-to-end tests validating models against the Antares Simulator interpreter (`tests/`)
- **Study examples** — reference studies used by tests and documentation (`resources/`)

Repository: `AntaresSimulatorTeam/GEMS` — License: MPL 2.0

---

## Directory Layout

```
.github/
  workflows/                  # GitHub Actions CI workflows
  ISSUE_TEMPLATE/             # Issue templates (antares-update, process-change)
  PULL_REQUEST_TEMPLATE.md    # PR template with process ID and checklist
doc/                          # MkDocs documentation source (sections 0-6)
libraries/                    # Shared YAML model libraries (4 files)
  CHANGELOG-<library>.md      # Per-library changelogs
resources/
  Documentation_Examples/     # Quick-start example studies
  e2e_studies/                # End-to-end test studies with reference data
tests/
  e2e_tests/                  # pytest e2e tests (require Antares binary)
  unit_tests/                 # pytest unit tests for Python utilities (no binary required)
versions/                     # Version tracking files (antares-simulator, libraries, gems-language)
CHANGELOG-gems-language.md    # GEMS Language changelog
COMPATIBILITY.md              # GEMS Language ↔ Antares ↔ GemsPy version matrix
mkdocs.yml                    # Documentation site config
pyproject.toml                # Tool configuration (ruff, mypy) — not a package descriptor
requirements.txt              # Python runtime dependencies
requirements-dev.txt          # Developer dependencies (ruff, mypy, yamllint)
requirements-doc.txt          # Documentation build dependencies
.yamllint.yml                 # yamllint configuration
```

---

## GEMS Language Essentials

### Model Libraries (`libraries/*.yml`)

Each library YAML file defines `port-types` and `models` under a top-level `library` key. Understanding this structure is critical before editing any library file.

```yaml
library:
  id: <library_id>
  description: <text>

  port-types:
    - id: <port_type_id>
      fields:
        - id: <field_id>

  models:
    - id: <model_id>
      parameters:          # inputs to the model
        - id: <param_id>
          time-dependent: true|false     # optional, default false
          scenario-dependent: true|false # optional, default false
      variables:           # decision variables
        - id: <var_id>
          lower-bound: <expression>
          upper-bound: <expression>
          variable-type: continuous|integer|binary
      ports:               # connection points
        - id: <port_id>
          type: <port_type_id>   # must reference a port-type in the same library
      port-field-definitions:
        - port: <port_id>
          field: <field_id>
          definition: <math_expression>
      binding-constraints:
        - id: <constraint_id>
          expression: <math_expression>  # must contain exactly one =, <=, or >=
      constraints:
        - id: <constraint_id>
          expression: <math_expression>
      objective-contributions:
        - id: <id>
          expression: <math_expression>
```

### Mathematical Expression Syntax

- Arithmetic operators: `+`, `-`, `*`, `/`
- Comparison operators (one per constraint): `=`, `<=`, `>=`
- Aggregation: `sum(expr)` sums over time, `sum_connections(port.field)` sums across connections
- Time indexing: `var[t-1]`, `var[t+1]`, `var[0]`
- Functions: `min()`, `max()`, `ceil()`
- Linearity required: no `variable * variable` or `constant / variable`

### Study Structure

```
Study/
├── input/
│   ├── system.yml              # components + connections
│   ├── data-series/            # time-series CSV files (one value per line)
│   └── model-libraries/        # library YAML files (or symlinks to libraries/)
├── parameters.yml              # solver configuration
└── scenario_builder.yml        # optional scenario definitions
```

**system.yml** defines:
- `components` — each references a model as `library_id.model_id` and provides parameter values
- `connections` — each links two components via their port IDs

**Critical rule:** The number of parameters in a component's `system.yml` definition must exactly match the number of parameters in the referenced model. A mismatch will cause the Antares modeler to fail silently.

---

## Running Tests

### Prerequisites

Tests require the **Antares Simulator binary**. The version is tracked in `versions/antares-simulator.txt`. CI downloads it automatically. For local runs, extract the binary at the repo root:

```
antares-<version>-Ubuntu-22.04/bin/antares-solver
antares-<version>-Ubuntu-22.04/bin/antares-modeler
```

The expected path is resolved in `tests/e2e_tests/env.py`.

### Commands

```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Run all e2e tests
python -m pytest tests/e2e_tests -v

# Run a single test
python -m pytest tests/e2e_tests -v -k "test_doc_qse_examples[QSE_1_Adequacy"

# Run one test file
python -m pytest tests/e2e_tests/test_doc_qse_examples.py -v
```

### Test Architecture

| File | Purpose |
|------|---------|
| `conftest.py` | Session-scoped fixtures: `paths`, `tmp_root`, `clean_tmp` |
| `env.py` | `EnvironmentPaths` dataclass with all repo/binary paths; `OBJECTIVE_ATOL = 1e-4` |
| `utils.py` | Helpers: copy studies, run binaries, extract objective values from output |
| `test_doc_qse_examples.py` | Parametrized: runs modeler on Quick Start Examples, asserts objective |
| `test_antares_legacy_models_equivalence.py` | Parametrized: compares GEMS modeler vs Antares solver objectives |

### How Objective Comparison Works

- `test_doc_qse_examples` compares against hardcoded expected values with `abs=OBJECTIVE_ATOL`
- `test_antares_legacy_models_equivalence` compares GEMS vs Antares at runtime with `rel=0.01` (1% relative tolerance, accounting for LP relaxation vs MIP differences in the thermal model)

---

## Building Documentation

```bash
python3 -m venv documentation_env && source documentation_env/bin/activate
pip install -r requirements-doc.txt
mkdocs serve          # http://127.0.0.1:8000
mkdocs build          # builds static site to site/
```

Docs hosted at: https://gems-energy.readthedocs.io/

---

## CI/CD Workflows

| Workflow | File | Trigger | What It Does |
|----------|------|---------|--------------|
| End-to-End Tests | `e2e-tests.yml` | PR, manual | Runs YAML validation first, then downloads Antares binary and runs e2e tests; uploads artifacts on failure |
| Lint and Format | `lint-and-format.yml` | PR, manual | ruff lint/format check, mypy strict type check, yamllint |
| Check Antares Update | `check-antares-update.yml` | Daily 06:00 UTC, manual | Fetches latest Antares release, creates issue if new version found |

---

## Git & Branching Model

- **`main`** — stable releases
- **`develop`** — active development integration
- Feature branches from `develop`, PRs back to `develop`
- No direct pushes to `main` or `develop`
- CI runs on every PR

---

## Coding Conventions

### Python

- Type hints everywhere; `pathlib.Path` for file paths
- `@dataclass(frozen=True)` for structured data
- Logging via `logging.getLogger(__name__)` — no bare `print()`
- Not a Python package — `pyproject.toml` exists only for tool configuration (`[tool.ruff]`, `[tool.mypy]`); do not add `[project]` or `[build-system]` sections

### YAML

- Library IDs use lowercase with underscores: `antares_legacy_models`
- Model IDs use lowercase with hyphens or underscores: `short-term-storage`, `thermal`
- Indentation: 2 spaces

---

## Critical Rules for AI Agents

1. **Never edit `libraries/*.yml` without understanding downstream impact.** These files are shared across all studies and tests. A parameter rename or addition breaks every study that references the affected model.

2. **After editing a library, check all studies.** Grep for the model ID across `resources/**/system.yml` to find affected studies. Verify parameter counts match.

3. **Test studies use symlinks.** Files in `resources/**/model-libraries/` may be symlinks to `libraries/`. Some symlinks point to absolute paths from other machines and are broken. The test infrastructure handles this via `copy_model_library()` which replaces dangling symlinks with real files.

4. **The Antares modeler fails silently.** `subprocess.run` in `utils.py` uses `check=False` and `capture_output=True`. If the modeler fails, no output directory is created and the test fails with `FileNotFoundError` on the output path. To debug, run the modeler directly and check stderr.

5. **Do not commit** `venv/`, `documentation_env/`, `site/`, `tmp/`, or extracted Antares binary directories.

6. **Version tracking.** The Antares Simulator version is tracked in `versions/antares-simulator.txt`. It is the single source of truth — `tests/e2e_tests/env.py` reads it dynamically and the workflow reads it via a shell step. Updating the file is sufficient; no other files need to be edited.

7. **Floating-point comparisons.** Always use `pytest.approx()` for objective value assertions. Never use `==` for floating-point comparison.

8. **Preserve existing test structure.** Tests are parametrized. To add a new study test, add an entry to the `@pytest.mark.parametrize` decorator — do not create new test functions.

---

## Governance Context

This repository is part of the GEMS Ecosystem governed by a formal process framework. Key process IDs relevant to this repo:

| Process | Trigger | Scope |
|---------|---------|-------|
| DOC-01 | Antares Simulator/Modeler evolution | Update GEMS Language docs, validate examples |
| DOC-02 | Internal documentation improvement | Website updates, fix inconsistencies |
| LT-01 | GEMS Language / Antares evolution | Update libraries and taxonomies |
| LT-02 | Internal library development | Modify existing models, verify no unintended changes |
| LT-03 | New library or taxonomy | Design phase, proof-of-concept study, full E2E validation |

Every change should follow: Issue creation → Impact analysis → Implementation → Testing → Review → Versioning → Documentation update.
