# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**GEMS** (Generic Energy system Modelling Scheme) is a high-level algebraic modeling language for energy system optimization and foresight studies. This repo contains YAML model libraries, a MkDocs documentation site, and a Python test suite that validates models against the Antares Simulator interpreter.

Repository: `AntaresSimulatorTeam/GEMS` — License: MPL 2.0

## Running Tests

Tests require **Antares Simulator v9.3.2** binaries. CI downloads them automatically; locally they must be extracted at the repo root as `antares-9.3.2-Ubuntu-22.04/` (paths resolved in `tests/e2e_tests/env.py`).

```bash
# Setup
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Run all e2e tests
python -m pytest tests/e2e_tests -v

# Run a single test by name
python -m pytest tests/e2e_tests -v -k "test_doc_qse_examples[QSE_1_Adequacy"

# Run one test file
python -m pytest tests/e2e_tests/test_doc_qse_examples.py -v
```

Tests compare objective function values using `pytest.approx()` with `abs=1e-4` (defined as `OBJECTIVE_ATOL` in `tests/e2e_tests/env.py`).

### Test Architecture

- `conftest.py` — session-scoped fixtures: `paths` (all env paths), `tmp_root` (temp directory, cleaned per test)
- `env.py` — `EnvironmentPaths` dataclass centralizing repo, study, and binary paths
- `utils.py` — helpers for copying studies, running binaries (`antares-solver` and `antares-modeler`), and extracting objective values from output files
- `test_doc_qse_examples.py` — parametrized: runs GEMS modeler on Quick Start Examples, checks objective vs expected value
- `test_antares_legacy_models_equivalence.py` — parametrized: runs both GEMS modeler and Antares solver on paired studies, asserts their objectives match

## Building Documentation

```bash
python3 -m venv documentation_env && source documentation_env/bin/activate
pip install -r requirements-doc.txt
mkdocs serve          # http://127.0.0.1:8000
mkdocs build          # static site to site/
```

Docs source is `doc/`, config in `mkdocs.yml`. Uses Material theme with MathJax and a custom YAML dynamic loader (`doc/javascripts/yaml-loader.js`).

## YAML Model & Study Structure

### Model Libraries (`libraries/*.yml`)

Each library file defines `port-types` and `models`. A model contains:

- `parameters` — input values (optionally `time-dependent` / `scenario-dependent`)
- `variables` — decision variables with bounds and type (`continuous`, `integer`, `binary`)
- `ports` — typed connection points (e.g., `flow`, `energy`, `emission`)
- `port-field-definitions` — algebraic expressions defining port field values
- `binding-constraints` — algebraic equality/inequality constraints
- `objective-contributions` — expressions summed into the objective function

Key syntax: `sum_connections(port.field)` aggregates across all connections to a port; `sum(expr)` sums over time steps.

### Study Structure

```text
Study/
├── input/
│   ├── system.yml              # components (referencing library.model) + connections
│   ├── data-series/            # time-series CSVs
│   └── model-libraries/        # library YAML files (or symlinks to libraries/)
├── parameters.yml              # solver config (solver, time steps, output flags)
└── scenario_builder.yml        # optional scenario definitions
```

`system.yml` has two top-level sections under `system`:
- `components` — each references a model as `library_id.model_id` and provides parameter values
- `connections` — each links two components by specifying `component1`/`component2` and their respective `port1`/`port2` names, forming the energy system graph

## Git & CI Workflow

- Development on `develop`, releases merge to `main`. Feature branches from `develop`, PRs back to `develop`.
- CI (`.github/workflows/e2e-tests.yml`) runs `pytest tests/e2e_tests` on every PR.
- A daily cron job (`.github/workflows/check-antares-update.yml`) checks for new Antares Simulator releases and opens a GitHub issue when one is found. The tracked version lives in `versions/antares-simulator.txt`.

## Python Conventions

- Type hints everywhere; `pathlib.Path` for file paths.
- `@dataclass(frozen=True)` for structured data.
- Logging via `logging.getLogger(__name__)` — no bare `print()`.
- This is not a Python package (no setup.py / pyproject.toml).

## Important Constraints

- `libraries/*.yml` are shared across studies and tests — edits propagate to all downstream.
- Do not commit `venv/`, `documentation_env/`, or `site/`.
- Test studies in `resources/` use symlinks for model libraries; some operations must preserve them (`preserve_symlinks=True`).
