# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with this repository.

For full project context, conventions, YAML schema details, and critical rules, see [AGENTS.md](AGENTS.md) — read it before making any changes.

## Quick Reference

```bash
# Run tests
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python -m pytest tests/e2e_tests -v

# Build docs
python3 -m venv documentation_env && source documentation_env/bin/activate
pip install -r requirements-doc.txt
mkdocs serve
```

## Key Reminders

- Antares binary version is tracked in `versions/antares-simulator.txt` — single source of truth; `env.py` and the workflow read it dynamically, no other files need updating
- `libraries/*.yml` are shared — edits affect all studies and tests
- Test studies in `resources/` may have broken symlinks in `model-libraries/`; the test harness handles this via `copy_model_library()`
- The Antares modeler fails silently (`check=False`); run it directly to see errors
- Git workflow: feature branches from `develop`, PRs back to `develop`
