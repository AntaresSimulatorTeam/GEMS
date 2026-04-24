# GEMS Compatibility Matrix

This table maps GEMS Language versions to the interpreter and library versions they are compatible with.

| GEMS Language | Antares-Simulator | antares-modeler (GemsPy) | Notes |
|---------------|-------------------|--------------------------|-------|
| 1.0.0         | 9.3.2             | —                        | Initial release |

## Versioning Policy

- **GEMS Language** — `gems_language_version` in `dependencies.json`. Bumped when the language specification changes (new keywords, syntax changes, removed features).
- **Antares-Simulator** — `antares_simulator_version` in `dependencies.json`. The version against which E2E tests are run.
- **antares-modeler (GemsPy)** — the Antares GEMS interpreter version. Updated when interpreter-specific behavior changes.

## Compatibility Rules

- A GEMS study written for Language version `X.Y.Z` is compatible with all interpreter versions that support `X.Y.Z`.
- Patch versions (`Z`) are always backward-compatible.
- Minor versions (`Y`) may add new features; older interpreters may not support them.
- Major versions (`X`) may contain breaking changes.

## Library Versions

| Library | Current Version | Key in `dependencies.json` |
|---------|----------------|----------------------------|
| `basic_models_library` | 1.0.0 | `basic_models_library_version` |
| `antares_legacy_models` | 1.0.0 | `antares_legacy_models_version` |
| `pypsa_models` | 1.0.0 | `pypsa_models_version` |
| `andromede_models` | 1.0.0 | `andromede_models_version` |
