# Discrepancies between projects

What each project treats as mandatory, optional, or spells differently, for the four GEMS input
kinds. Every row cites file and line in the clones under `upstream/` (read-only, shallow, taken on
2026-11-19). The schemas refer to these rows through `x-discrepancy: [ID]`.

**Where projects disagree the schemas follow GemsPy (the reference implementation named in the brief)
and say so in the row's last column. That is a provisional default, not a decision: the open
questions at the end of the README/report list the ones that need a human choice.**

## Sources and how to read the tables

| Short name | Source | Commit |
|---|---|---|
| **DOC** | `GEMS/doc/user-guide/input-files/*.md`, `GEMS/doc/interoperability/hybrid/*.md`, `GEMS/AGENTS.md` | GEMS `9c52d63` |
| **GemsPy** | `GemsPy/src/gems_craft/**/parsing.py` (pydantic; `gems_craft_hybrid` for the hybrid sections) | GemsPy `b197a14` |
| **ASim** | Antares_Simulator `develop`: `src/io/inputs/yml-*/parser.cpp` + `decoders.cpp` + `yml-utils/checkFields.cpp` | `6744889` |
| **AntaREST** | `AntaREST/antarest/study/business/model/gems/{library,system}.py`, `antarest/core/model.py` | `cf5852e` |
| **VB** | GEMS-ViewsBuilder `gems_views_builder/input/system.py` | `975baab` |
| **PC** | PyPSA-to-GEMS-Converter `src/models/gems_system_yml_schema/*`, `src/gems_study_writer.py`, `resources/optim-config.yml` | `4f2c92e` |

Path prefixes used below: `GP/` = `GemsPy/src/gems_craft/`, `DOC/` = `GEMS/doc/user-guide/input-files/`,
`CPP/` = `Antares_Simulator/src/io/inputs/`, `AR/` = `AntaREST/antarest/study/business/model/gems/`.

**antares-datamanager-front, antares-datamanager-generator and antares-doc: no evidence.** At the
cloned commits none of them reads, writes or validates a GEMS library, system, optim-config or
system-for-view file (`grep -ri gems` over `src/` of the two datamanager repos finds nothing;
antares-doc only mentions GEMS in prose and links, and has no input-file reference). They are listed in
the rollout plan because the brief names them, but they contribute no rows here.

**Antares_Simulator strictness depends on the version.** `develop` validates every key of
libraries, systems and optim-configs with a whitelist (`CPP/yml-utils/checkFields.cpp:129-139`,
message `Unrecognised field` at `:61`) and rejects what is not listed. At tag `v10.2.0` (the version in
`GEMS/dependencies.json`) that file does not exist and `yml-model/parser.cpp` only tags nodes; I did
not investigate whether 10.2.0 rejects unknown keys by another route. Rows marked "ASim develop"
therefore describe the unreleased behaviour.

**Key spelling.** GemsPy and AntaREST build their pydantic models with `populate_by_name=True`
(`GemsPy/src/gems_craft/utils.py:86-89`, `AR/library.py:44`, `AR/system.py:28`), so they accept both
`time-dependent` and `time_dependent`. DOC, ASim and the schemas only know the kebab-case spelling.
See L10 / S13.

---

