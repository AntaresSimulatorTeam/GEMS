# Antares Legacy Models Library — Changelog

All notable changes to the Antares Legacy models library (`src/antares_gems_converter/libs/`) are documented here.

Versioning follows the rules defined in `COMPATIBILITY.md`:

- **Major** — New legacy model added
- **Minor** — Bug fix or improvement to an existing model
- **Patch** — Non-functional change (rename variable/parameter, internal refactor)

---

## [2.1.2]

- `area` model: added `is_significant_loss_of_load` extra-output (`unsupplied_energy >= 0.5`); `is_loss_of_load` now captures any non-zero unsupplied energy (`unsupplied_energy >= 1e-6`).

---

## [2.1.1]

- Added `carrier` property to `link`, `short_term_storage`, and `long_term_storage` models.
- Added `miscellaneous_type` property to `miscellaneous_generation` model.

---

## [2.1.0]

- `thermal` model: added `market_bid_cost` parameter; objective contribution now uses `market_bid_cost` instead of `generation_cost`.
- `link` model: simplified congestion expressions (`is_directly_congested`, `is_indirectly_congested`) to use `flow` directly, removing dependency on `loop_flow`.
- `short_term_storage` model: added overflow support (`overflow` variable, `is_overflow_allowed`, `overflow_cost`) and variation penalties (`injection_variation`, `withdrawal_variation` variables with associated parameters and constraints).
- `long_term_storage` model: fixed objective expression to add a small regularization term (`-0.000001*level`) to avoid degenerate solutions.

---

## [2.0.0]

- Added models `miscellaneous_generation` and `long_term_storage`
- Renamed taxonomy categories to use `generation` in place of `production`:
    - `dispatchable_production` → `dispatchable_generation`
    - `renewable_fatal_production` → `renewable_fatal_generation`
    - `miscellaneous_fatal_production` → `miscellaneous_fatal_generation`
    - Parent category `production` → `generation`
- Updated the `thermal`, `renewable`, and `miscellaneous_generation` models accordingly.
- Catalog files (`antares_legacy_area_catalog.yml`, `antares_legacy_thermal_cluster_catalog.yml`) and the taxonomy (`antares_legacy_taxonomy.yml`) updated consistently.

---

## [1.1.0]

- Renaming to match naming conventions.
- New extra-outputs to be able to reproduce legacy output metrics.
- New parameter on link model : loop flow.

---

## [1.0.0] — 2026-04-19

- Initial baseline release.
- Supported model types: area, thermal, link, short-term storage (STS), load, renewables.
HYBRID and FULL conversion modes supported.
- Validated against Antares-Simulator 10.0.0, antares-craft 0.3.0, GemsPy 0.0.2.