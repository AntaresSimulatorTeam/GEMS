# Antares Legacy Models Library — Changelog

All notable changes to the Antares Legacy models library (`src/antares_gems_converter/libs/`) are documented here.

Versioning follows the rules defined in `COMPATIBILITY.md`:

- **Major** — New legacy model added
- **Minor** — Bug fix or improvement to an existing model
- **Patch** — Non-functional change (rename variable/parameter, internal refactor)

---

## [2.4.0]

- `flow` port-type: new fields `spillage_bound` and `unsupplied_energy_bound`, mapped to the `spillage-bound` and `unsupplied-energy-bound` of the hybrid `area-connection` (previously `flow` and nothing). Every model with a `flow` port defines them after the legacy bounds on spilled and unsupplied energy:
    - `thermal`: `generation_power`; `renewable`, `miscellaneous_generation`: `available_power`.
    - `short_term_storage`, `long_term_storage`: `withdrawal_power` (injection and pumping no longer reduce the bound on spillage).
    - `load`: `max(0, -load)` and `max(0, load)` (the load no longer reduces the bound on spillage, and bounds the unsupplied energy).
    - `link`: `0` on both ports (imports may neither be spilled nor left unsupplied).
- Hybrid results change when a converted load has unsupplied energy (the converted study was infeasible) or imports, when an area spills the imports of a converted link, and when a converted short-term storage or hydro reservoir charges on imports.
- The bounds assume the nodal optimization options of the areas (`non-dispatchable-power`, `dispatchable-hydro-power`, `other-dispatchable-power`) are on, which is their default.
- Zero port-field definitions are plain numbers (`definition: 0`), which requires GemsPy >= 0.3.0.

---

## [2.3.0]

- Added `name` property to the `renewable` model (cluster name, used to break down GEMS-ViewsBuilder metrics). Every component of this model must now set it, including the aggregated wind, solar and run-of-river components.
- `short_term_storage` model: renamed the `group` property to `technology`, like `thermal` and `renewable`, where it also holds the Antares cluster group. The taxonomy category `short_term_storage` and the `STS_INJECTION`, `STS_WITHDRAWAL` and `STS_LEVEL` breakdowns of the area catalog are renamed accordingly.

---

## [2.2.1]

- Added `name` property to `thermal` and `short_term_storage` models (cluster name, used to break down GEMS-ViewsBuilder metrics).

---

## [2.2.0]

- `thermal` model: `min_up_duration` and `min_down_duration` are now declared `time-dependent: false` and `scenario-dependent: false`. Both are used in the bounds of the minimum up/down time sums, and GEMS requires time-sum bounds to be declared time-independent in the library. A system can no longer give them a time series or scenario-dependent values.

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
