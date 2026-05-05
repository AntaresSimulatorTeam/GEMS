# GEMS Compatibility Matrix

This table maps documentation/language versions to the interpreter and library versions they are compatible with.

| Documentation | Antares-Simulator | GemsPy | Notes |
|---------------|-------------------|--------|-------|
| v0.3.0        | 10.0.1            | —      |  |
| v0.3.1        | 10.0.1            | —      |  |

## Versioning Policy

- **GEMS Language / Documentation** — versioned together. The documentation release version (tracked in `doc/0_Home/4_release_notes.md`) is the canonical language version. Bumped whenever the language specification or documentation changes; a future distinction between language and documentation versions may be introduced.
- **Antares-Simulator** — `antares_simulator_version` in `dependencies.json`. The version against which E2E tests are run.
- **antares-modeler (GemsPy)** — the Antares GEMS interpreter version. Updated when interpreter-specific behavior changes.

## Compatibility Rules

- A GEMS study written for Language version `X.Y.Z` is compatible with all interpreter versions that support `X.Y.Z`.
- Patch versions (`Z`) are always backward-compatible.
- Minor versions (`Y`) may add new features; older interpreters may not support them.
- Major versions (`X`) may contain breaking changes.

## Library Versions

| Library | Current Version |
|---------|----------------|
| `basic_models_library` | 1.0.0 |
| `antares_legacy_models` | 1.0.0 |
| `pypsa_models` | 1.0.0 |
| `andromede_models` | 1.0.0 |
