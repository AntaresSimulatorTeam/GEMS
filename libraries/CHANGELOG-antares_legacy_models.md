# Changelog — antares_legacy_models

All notable changes to this library are documented here.

## [2.0.0]

### Added
- Added models `miscellaneous_generation` and `long_term_storage`

### Changed
- Renamed taxonomy categories to use `generation` in place of `production`:
    - `dispatchable_production` → `dispatchable_generation`
    - `renewable_fatal_production` → `renewable_fatal_generation`
    - `miscellaneous_fatal_production` → `miscellaneous_fatal_generation`
    - Parent category `production` → `generation`
- Updated the `thermal`, `renewable`, and `miscellaneous_generation` models accordingly.
- Catalog files (`antares_legacy_area_catalog.yml`, `antares_legacy_thermal_cluster_catalog.yml`) and the taxonomy (`antares_legacy_taxonomy.yml`) updated consistently.

## [1.1.0]

### Added
- `extra-outputs` on existing models to reproduce legacy output metrics.
- `loop_flow` parameter on the `link` model.

### Changed
- Parameter and variable renaming across models to align with naming conventions.

## [1.0.0] — 2025-01-26

### Added
- Initial release of `antares_legacy_models`.
- Models: `area`, `load`, `thermal`, `renewable`, `short_term_storage`, `link`.
- Port-types: `flow`.
