# GEMS Compatibility Matrix

This table maps GEMS Language versions to the interpreter and library versions they are compatible with.

| GEMS Language | Antares-Simulator | antares-modeler (GemsPy) | Notes |
|---------------|-------------------|--------------------------|-------|
| 1.0.0         | 9.3.2             | —                        | Initial release |

## Versioning Policy

- **GEMS Language** — version in `versions/gems-language.txt`. Bumped when the language specification changes (new keywords, syntax changes, removed features).
- **Antares-Simulator** — tracked version in `versions/antares-simulator.txt`. The version against which E2E tests are run.
- **antares-modeler (GemsPy)** — the Antares GEMS interpreter version. Updated when interpreter-specific behavior changes.

## Compatibility Rules

- A GEMS study written for Language version `X.Y.Z` is compatible with all interpreter versions that support `X.Y.Z`.
- Patch versions (`Z`) are always backward-compatible.
- Minor versions (`Y`) may add new features; older interpreters may not support them.
- Major versions (`X`) may contain breaking changes.

## Library Versions

| Library | Current Version | Version File |
|---------|----------------|--------------|
| `basic_models_library` | 1.0.0 | `versions/basic_models_library.txt` |
| `antares_legacy_models` | 1.0.0 | `versions/antares_legacy_models.txt` |
| `pypsa_models` | 1.0.0 | `versions/pypsa_models.txt` |
| `andromede_models` | 1.0.0 | `versions/andromede_models.txt` |
