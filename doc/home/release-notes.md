
# Release Notes

## v0.5.0 | *13-10-2026*

### Added

* Document the optimization configuration file `optim-config.yml` ([PR77](https://github.com/AntaresSimulatorTeam/GEMS/pull/226))

* Document integer strategy, heuristics and the `lower_bound` / `upper_bound` variable bound operators, available in GemsPy only ([#251](https://github.com/AntaresSimulatorTeam/GEMS/pull/251))

* Add a CI link checker for the documentation ([PR80](https://github.com/AntaresSimulatorTeam/GEMS/pull/236))

### Changed

* Bump GemsPy to v0.2.0 ([#251](https://github.com/AntaresSimulatorTeam/GEMS/pull/251))

* Rework the PyPSA-Eur tutorial notebook to run with GemsPy and the PyPSA-to-GEMS converter v0.0.2 ([#238](https://github.com/AntaresSimulatorTeam/GEMS/pull/238))

* Align the taxonomy, catalog, view config and Views output documentation with GEMS ViewsBuilder v0.0.1 ([#242](https://github.com/AntaresSimulatorTeam/GEMS/pull/242), [#248](https://github.com/AntaresSimulatorTeam/GEMS/pull/248))

* Remove `playlist-file` from the `scenario-scope` documentation of the optimization configuration file ([#239](https://github.com/AntaresSimulatorTeam/GEMS/pull/239))

* Bump basic_models_library to v1.0.1 ([#243](https://github.com/AntaresSimulatorTeam/GEMS/pull/243))

* Bump Antares Legacy Library to v2.2.0: `min_up_duration` and `min_down_duration` of the `thermal` model are now time- and scenario-independent ([#255](https://github.com/AntaresSimulatorTeam/GEMS/pull/255))

### Fixed

* Use the official "Generic Energy systems Modelling Schema" spelling of GEMS ([#233](https://github.com/AntaresSimulatorTeam/GEMS/pull/233))

* Fix links to the reorganized Antares Simulator documentation ([#245](https://github.com/AntaresSimulatorTeam/GEMS/pull/245))

* Fix `time-dependant` typo in basic_models_library ([#243](https://github.com/AntaresSimulatorTeam/GEMS/pull/243))

## v0.4.0 | *21-08-2026*

### Added

* Document Views : new section integrated in the user guide ([PR65](https://github.com/AntaresSimulatorTeam/GEMS/pull/191))

* Document thermal connection in hybrid studies ([PR75](https://github.com/AntaresSimulatorTeam/GEMS/pull/204))

* Add a public roadmap in the Home chapter ([#221](https://github.com/AntaresSimulatorTeam/GEMS/pull/221))

### Changed

* Bump GemsPy to v0.1.3 : update notebooks and document new GemsPy release ([PR76](https://github.com/AntaresSimulatorTeam/GEMS/pull/209))

* Clarify time-index notation and extra-output comparisons in syntax reference ([#212](https://github.com/AntaresSimulatorTeam/GEMS/pull/212))

* Refactor Quick Start Examples presentation page ([PR78](https://github.com/AntaresSimulatorTeam/GEMS/pull/230))

### Fixed

* Remove duplicated blocks and fix broken links ([#224](https://github.com/AntaresSimulatorTeam/GEMS/pull/224))

## v0.3.5 | *24-07-2026*

### Changed

* Bump Antares Simulator version to v10.1.1 ([PR73](https://github.com/AntaresSimulatorTeam/GEMS/pull/190))

* Bump Antares Legacy Library to v2.1.2 ([PR72](https://github.com/AntaresSimulatorTeam/GEMS/pull/188))

* Refactoring of documentation based on general comments ([PR64](https://github.com/AntaresSimulatorTeam/GEMS/pull/171))

* Update developer guide — branching model, CI table, workflows and release process ([PR62](https://github.com/AntaresSimulatorTeam/GEMS/pull/166))

### Fixed

* Fix picture paths and UV lock usage in tutorials ([#197](https://github.com/AntaresSimulatorTeam/GEMS/pull/197))

* Fix PyPSA-eur tutorial e2e tests ([#198](https://github.com/AntaresSimulatorTeam/GEMS/pull/198))

## v0.3.4 | *25-06-2026*

### Added

* Add a tutorial using the [PyPSA-eur dataset](https://pypsa-eur.readthedocs.io/en/latest/) ([PR37](https://github.com/AntaresSimulatorTeam/GEMS/pull/94))

* Add an investment jupyter notebook ([PR51](https://github.com/AntaresSimulatorTeam/GEMS/pull/135))

### Changed

* Bump Antares Simulator version to v10.1.0 ([#160](https://github.com/AntaresSimulatorTeam/GEMS/pull/160))

* Replace requirements txt file with uv lock ([#163](https://github.com/AntaresSimulatorTeam/GEMS/pull/163))

* Chore CICD - Path Blocker ([#169](https://github.com/AntaresSimulatorTeam/GEMS/pull/169))

* Rename sha256 files to follow `<library>.yml.sha256` convention ([#165](https://github.com/AntaresSimulatorTeam/GEMS/pull/165))

* Bump documentation on GemsPy from v0.10 to v0.12 ([#161](https://github.com/AntaresSimulatorTeam/GEMS/pull/161))

* Improve formatting ([#151](https://github.com/AntaresSimulatorTeam/GEMS/pull/151))

## v0.3.3 | *10-06-2026*

### Added

* Add e2e Test for jupyter notebook tutorial on unit commitment ([PR49](https://github.com/AntaresSimulatorTeam/GEMS/pull/132))

* Write Guidelines for Squash and Merge Commits ([PR54](https://github.com/AntaresSimulatorTeam/GEMS/pull/140))

### Changed

* Update PyPSA-to-GEMS converter guide and Fix some syntax issues ([PR53](https://github.com/AntaresSimulatorTeam/GEMS/pull/139))

* Align dependency pinning policy across all repos ([PR52](https://github.com/AntaresSimulatorTeam/GEMS/pull/138))

* Update pypsa-models library to v2.0.1 ([PR55](https://github.com/AntaresSimulatorTeam/GEMS/pull/142))

* Update antares-legacy library to v2.0.0 ([PR57](https://github.com/AntaresSimulatorTeam/GEMS/pull/155))

* Refactor README file by adding badges, rewrite hypergraph and modeler installation pages ([PR56](https://github.com/AntaresSimulatorTeam/GEMS/pull/153))


## v0.3.2 | *13-05-2026*

### Added

* GemsPy Unit Commitment Jupyter Notebook Tutorial ([PR33](https://github.com/AntaresSimulatorTeam/GEMS/pull/67))

* Add documentation about the Antares-Legacy to GEMS converter ([PR45](https://github.com/AntaresSimulatorTeam/GEMS/pull/115))

* Add documentation about how to verify SHA GEMS official libraries ([PR48](https://github.com/AntaresSimulatorTeam/GEMS/pull/125))


### Changed

* Rename all "scheme" mentions by "schema" ([PR46](https://github.com/AntaresSimulatorTeam/GEMS/pull/123))

* Workflow Fix and Developer Guide Update ([PR47](https://github.com/AntaresSimulatorTeam/GEMS/pull/124))

* Change warning message inside the Quick Start section ([PR50](https://github.com/AntaresSimulatorTeam/GEMS/pull/128))

## v0.3.1 | *05-05-2026*

### Added

* Add Governance Layer ([PR40](https://github.com/AntaresSimulatorTeam/GEMS/pull/99))

## v0.3.0 | *22-04-2026*

### Added

* Add the raw YAML files in the Overview section ([PR36](https://github.com/AntaresSimulatorTeam/GEMS/pull/93))
* Add GitHub Action for automatically verifying the latest released antares-simulator version ([PR36-bis](https://github.com/AntaresSimulatorTeam/GEMS/pull/85))

### Changed

* Upgrade SEO ([PR38](https://github.com/AntaresSimulatorTeam/GEMS/pull/97))
* Use the newest version of Antares-Legacy-Models Library for Quick Start Example 2 ([PR35](https://github.com/AntaresSimulatorTeam/GEMS/pull/86))
* Update the documentation area-connection part in Hybrid Studies ([PR34](https://github.com/AntaresSimulatorTeam/GEMS/pull/84))

## v0.2.0 | *26-03-2026*

### Added

* Document floor, ceil, max, min operators ([PR30](https://github.com/AntaresSimulatorTeam/GEMS/pull/62))
* Dynamic visualization of libraries ([PR31](https://github.com/AntaresSimulatorTeam/GEMS/pull/63))

### Changed

* Update the appearance of the documentation ([PR32](https://github.com/AntaresSimulatorTeam/GEMS/pull/66))
* Clarify the distinction between Antares Modeler and Antares Solver ([PR32](https://github.com/AntaresSimulatorTeam/GEMS/pull/66))

## v0.1.0 | *22-01-2026*

### Added

* Initialization of the documentation
