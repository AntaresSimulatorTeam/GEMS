# Changelog — pypsa_models

All notable changes to this library are documented here.

## [2.0.1] — 2026-05-21

- **Changed** `emission_factor` to `scenario-dependent: true` for `generator`, `storage_unit`, and `store` — enables per-scenario CO2 emission factors (PyPSA 1.2.0)
## [2.0.0] — 2026-05-14

- **Added** `line` model — DC LOPF line with extendable and modular capacity support
- **Added** `transformer` model — DC LOPF transformer with extendable and modular capacity support
- **Added** `theta` variable and `theta_min`/`theta_max` parameters to `bus` model
- **Added** port definition in `bus` model for `angle` field of `flow` port type
- **Changed** `flow` port-type field renamed from `flow` to `power`; `angle` field added
- **Fixed** `storage_unit` model — `spill` variable now correctly bounded by `inflow` parameter

## [1.0.0] — 2025-01-26

Initial baseline release.

Supported component models: generators (basic, extendable, p_min/p_max, with emissions),
links (basic, extendable), storage units, stores.

Validated against PyPSA 1.0.0 and Antares-Simulator 9.3.7.
