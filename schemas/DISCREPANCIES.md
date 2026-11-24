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

## 1. Model library

| ID | Field / structure | DOC | GemsPy | ASim (develop) | AntaREST | Others | Schema |
|---|---|---|---|---|---|---|---|
| L01 | `library.version`, `library.taxonomy`, model `taxonomy-category`, model `properties` | documented, optional (`DOC/library.md:47-61`, `:315-341`) | accepted (`GP/model/parsing.py:107-123`, `:126-133`) | **rejected** as unrecognised: `libraryFields` has none of them (`CPP/yml-model/parser.cpp:19-54`), yet `GEMS/libraries/antares_legacy_models.yml:15-16,33,68` uses all four | accepted (`AR/library.py:118-146`) | ASim `decoders.cpp:175-204` does not read them | accepted |
| L02 | `variable-type` value and requiredness | enum `continuous`, `integer`, `binary`, no default stated (`DOC/library.md:207`) | free `str`, default `continuous` (`GP/model/parsing.py:47`); only the three values resolve (`GP/model/resolve_library.py:433-440`) | spelled **`boolean`**, not `binary`; default continuous (`CPP/yml-model/decoders.cpp:99-115,128-129`); five real Simulator test libraries use `boolean` (e.g. `Antares_Simulator/resources/modeler/1_4/input/model-libraries/lib_example_1_4.yml`) | `binary`, and the key is **mandatory** (`type: VariableType = Field(alias="variable-type")`, no default: `AR/library.py:74-77,113`) | - | enum of the three doc values, optional. `boolean` rejected |
| L03 | variable `time-dependent` / `scenario-dependent` | documented, default true (`DOC/library.md:210-211`) | accepted (`GP/model/parsing.py:44-45`) | accepted (`CPP/yml-model/decoders.cpp:130-131`) | **rejected**: not a field of `_GemsModelVariables`, `extra="forbid"` (`AR/library.py:109-115`) | - | accepted |
| L04 | `location` on variables, constraints, objective-contributions | not in library doc (placement lives in optim-config `model-decomposition`, `DOC/optimization-configuration.md:402-460`) | **rejected** (no such field) | accepted, default `subproblems` (`CPP/yml-model/decoders.cpp:132,156,171`, `parser.cpp:15-17,48`) | rejected | - | rejected |
| L05 | `library.dependencies` | undocumented | accepted, list of str (`GP/model/parsing.py:128`) | rejected (`parser.cpp:19-54`) | rejected | - | accepted, flagged |
| L06 | `constraints[].lower-bound` / `upper-bound` | undocumented (`DOC/library.md:246-263`) | accepted (`GP/model/parsing.py:50-54`, used at `GP/model/resolve_library.py:445-455`) | rejected (`expressionFields`, `parser.cpp:15-17`) | rejected (`AR/library.py:80-83`) | - | accepted, flagged |
| L07 | `area-connection` keys | "all three keys must be present ... even if some values are left empty"; at least one with a value (`GEMS/doc/interoperability/hybrid/hybrid-connections.md:13,34,106`) | all optional (`GP/model/parsing.py:61-66`) but GemsPy's hybrid writer calls them "mandatory keys, as null when unused" (`GemsPy/src/gems_craft_hybrid/model/parsing.py:21-39`) | the first three **required**, `price` optional (`CPP/yml-model/parser.cpp:27-33`) | three optional, **no `price`** (`AR/library.py:29-34`) | PC writes nothing (no hybrid) | three keys required (nullable), at least one non-null, `price` optional |
| L08 | id naming rule | "alphanumeric and underscore, lower-case only" for all ids of libraries and system (`DOC/library.md:37-43`). Yet the same docs show `port-to-area`, `to-area-bound` (`hybrid-connections.md:17-21`) and `AGENTS.md:125` says "model IDs ... lowercase with hyphens or underscores: `short-term-storage`" | not enforced (no pattern anywhere in `GP/`) | not enforced | enforced for port-type, model, variable, constraint, objective ids only: `^[a-z0-9_]+$` (`antarest/core/model.py:30-31`, used at `AR/library.py:46,82,88,112,121`), not for parameter, port or property ids (`:62,70`) | - | **relaxed to non-empty string** (`Identifier`); the doc rule is kept as unused `StrictIdentifier`. Applying it would reject real files of GEMS itself (`libraries/andromede_models.yml` library id `andromede-v1-models`, `libraries/basic_models_library.yml` constraint `Level equation`, ...): measured as files whose first error is the pattern, at least 6 in GEMS, 35 in GemsPy, 26 in Antares_Simulator, 2 in AntaREST, 1 in ViewsBuilder |
| L09 | numbers in expression fields | bounds "Number or Expression" (`DOC/library.md:208-209`) | any YAML number is read as its literal for bounds, `definition`, `expression` (`coerce_numbers_to_str`, `GP/model/parsing.py:29-38`) | `as<string>` on any scalar (`CPP/yml-model/decoders.cpp:25-35`) | bounds `str \| float`, `expression: str` strict (`AR/library.py:92-115,80-90`) | - | bounds and `definition`: string or number; `expression`: string only |
| L10 | snake_case spelling of keys | kebab only | **both** accepted (`populate_by_name`, `utils.py:86-89`) | kebab only | both accepted | PC writes snake_case (S13) | kebab only |
| L11 | `binding-constraints`, `extra-outputs`, `port-field-definitions` | documented in full | typed | typed | **opaque `Any`**, "not used in the current implementation" (`AR/library.py:131-136`) | - | typed (GemsPy) |
| L12 | `null` for a collection (`models:` with nothing after it) | not stated | rejected (`List[...]`, no `None`) | treated as absent (`as_fallback_default`, `CPP/yml-model/decoders.cpp:179-199`, `checkFields.cpp:184-187`) | rejected | - | rejected |
| L13 | `extra-outputs` strictness in GemsPy | - | `ExtraOutputSchema` is a stdlib `@dataclass` (`GP/model/parsing.py:101-104`), not a `ModifiedBaseModel`; I could not verify without running GemsPy that unknown keys are rejected there | rejects unknown keys | rejects | - | rejects unknown keys (unverified in GemsPy) |
| L14 | which collections are optional | "All fields, unless explicitly marked as optional, must be present" (`DOC/library.md:8`), but `parameters`, `variables`, `ports`, `constraints`, `fields`... are not marked optional | all default to empty lists (`GP/model/parsing.py:73-78,107-123`) | all default to empty (`decoders.cpp:179-191`); only `id` mandatory, plus per-entry required keys (`parser.cpp:19-54`) | all default to empty (`AR/library.py:138-146`) | - | only `library.id`, `model.id` and per-entry required keys are mandatory (DOC and code disagree; code wins) |

## 2. System

| ID | Field / structure | DOC | GemsPy | ASim (develop) | AntaREST | Others | Schema |
|---|---|---|---|---|---|---|---|
| S01 | `system.description` | documented, optional (`DOC/system.md:5,41`) | **rejected**: `SystemSchema` has no such field, `extra="forbid"` (`GemsPy/src/gems_craft/study/parsing.py:88-92`) | accepted (`CPP/yml-system/parser.cpp:17`) | accepted (`AR/system.py:149`) | - | accepted. A DOC-conformant file therefore fails in GemsPy |
| S02 | `system.id` | "A unique identifier" (`DOC/system.md:40`), no "optional" tag | optional (`parsing.py:89`) | optional, default `""` (`CPP/yml-system/decoders.cpp:81`, `parser.cpp:16`) | **mandatory** (`AR/system.py:148`) | VB falls back to `"study"` (`GEMS-ViewsBuilder/.../input/system.py:66`) | optional |
| S03 | `system.components` | listed without "optional" (`DOC/system.md:43`) | default empty (`parsing.py:91`) | default empty (`decoders.cpp:82`) | **mandatory** (`AR/system.py:150`) | - | optional |
| S04 | parameter `time-dependent` / `scenario-dependent` | "the following fields must be provided" (`DOC/system.md:60-67`) | default `false` (`GP/study/parsing.py:32-37`) | default `false` (`CPP/yml-system/decoders.cpp:17-21`, `parser.cpp:26`) | **mandatory** (`AR/system.py:31-32`) | PC default `false` (`PyPSA-to-GEMS-Converter/src/models/gems_system_yml_schema/gems_component_parameter.py:20-21`) | optional, default false |
| S05 | parameter `value` typing | number if both flags false, else data-series id (`DOC/system.md:69-73`) | `float \| str`, no cross-check (`GP/study/parsing.py:35`) | always read as a string (`CPP/yml-system/decoders.cpp:22`) | enforced: dependent -> str, constant -> number (`AR/system.py:38-45`) | the Simulator's own test 1.5 expects failure for a series id on a constant parameter (`Antares_Simulator/src/tests/cucumber/features/modeler-features/test_launcher_1.feature:49-53`) | enforced (DOC + AntaREST) |
| S06 | parameter `scenario-group` | not documented at parameter level (only on components, `DOC/system.md:54`) | accepted (`GP/study/parsing.py:37`) | rejected (`parser.cpp:24-26`) | rejected (`AR/system.py:27-33`) | PC's own model accepts it (`gems_component_parameter.py:23`) | accepted, flagged |
| S07 | component `integer-strategy` | documented, "Only available in GemsPy ... Antares modeler ... ignores this field" (`DOC/system.md:98-102`) | accepted (`GP/study/parsing.py:61-85`) | **rejected** (not in `systemFields`, `parser.cpp:15-36`), contradicting the doc's "ignores" | accepted (`AR/system.py:68-104`) | - | accepted |
| S08 | `system.model-libraries` | "Comma-separated list of library IDs" (`DOC/system.md:42`) | `Optional[str]`, "Parsed but unused for now" (`GP/study/parsing.py:90`) | accepted, not read (`parser.cpp:18`, `decoders.cpp:79-89`) | passes through (`extra="allow"`, `AR/system.py:146`) | VB never reads it | optional string, content not checked |
| S09 | `area-connections`, `thermal-capacity-connections` | documented only in the hybrid pages (`hybrid-connections.md:90-140`), not in `system.md` | accepted **only by `HybridSystemSchema`** (`GemsPy/src/gems_craft_hybrid/study/parsing.py:36-38`); the plain `SystemSchema` rejects them | accepted (`CPP/yml-system/parser.cpp:31-36`) | accepted; area lower-cased (`AR/system.py:116-143`) | PC omits them when empty because plain GemsPy rejects them (`PyPSA-to-GEMS-Converter/src/models/gems_system_yml_schema/gems_system.py:74-84`) | accepted |
| S10 | unknown keys in `system` | - | rejected | rejected | **allowed** (`extra="allow"`, `AR/system.py:146`) | - | rejected |
| S11 | keys next to the root `system` | "exactly one top-level `system` entry" (`DOC/system.md:5`) | `parse_yaml_system` reads `tree["system"]` and **ignores siblings** (`GP/study/parsing.py:116-120`); the unused `load_input_system` expects a headerless document (`:102-110`) | rejected (`CPP/yml-system/parser.cpp:42`) | reads `["system"]` only (`file_study_gems_system_dao.py:95`) | - | rejected |
| S12 | property `value` type | String (`DOC/system.md:79-84`) | `str`, YAML ints rejected (`GP/study/parsing.py:40-42`) | any scalar, read as string (`CPP/yml-system/decoders.cpp:26-31`) | `str` (`AR/system.py:61-65`) | - | string |
| S13 | `model_libraries` / `area_connections` in snake_case | kebab only | accepted | rejected | accepted for known fields, passed through otherwise | PC writes `model_libraries` and `area_connections` (`PyPSA-to-GEMS-Converter/src/models/gems_system_yml_schema/gems_system.py:62,81`); four GemsPy test studies and `GEMS-ViewsBuilder/resources/tests_inputs/test_3/system.yml:6` do the same | kebab only; these 6 files are recorded as known failures |
| S14 | property ids | "key name" (`DOC/system.md:83`) | free string | free string | free string | ASim writes `district_<name>` with the raw district name, e.g. `district_all areas` (`Antares_Simulator/src/view-builder/generateSystemForView.cpp:38`; AntaREST fixture `.../system-for-views.yml`) | free string |

## 3. Optimization configuration

The two dialects barely overlap. DOC and GemsPy describe the same file; ASim reads a different, smaller one;
PC writes the ASim one.

| ID | Field / structure | DOC | GemsPy | ASim (develop) | Others | Schema |
|---|---|---|---|---|---|---|
| O01 | resolution mode | `resolution.mode`, 4 values, default `frontal`, plus `block-length`, `block-overlap`, `carry-over-length` (`DOC/optimization-configuration.md:170-186`) | same (`GP/optim_config/parsing.py:144-228`) | top-level **`resolution-mode`** string, only `benders-decomposition` and `sequential-subproblems` accepted, default `sequential-subproblems` (`CPP/yml-optim-config/parser.cpp:30`, `decoders.cpp:126-130`, `OptimConfig.h:58-59`, `Antares_Simulator/src/modeler/loadFiles/readLibraries.cpp:196-204`) | PC writes `resolution-mode: benders-decomposition` (`PyPSA-to-GEMS-Converter/resources/optim-config.yml:12`); Simulator test studies 13_1 and 13_2 too | DOC/GemsPy dialect only (provisional) |
| O02 | `time-scope`, `solver-options` | documented (`DOC/optimization-configuration.md:76-166`) | `TimeScopeConfig`, `SolverOptionsConfig` (`parsing.py:231-271`) | **not in `optimConfigFields`**, rejected (`parser.cpp:16-31`) | in the Simulator the equivalent settings live in `parameters.yml`, outside this task's four kinds | accepted |
| O03 | `models[].model-decomposition` | optional (`DOC/...:324-329`) | optional (`parsing.py:139`) | **mandatory** (`required` = true at `CPP/yml-optim-config/parser.cpp:21`) | - | optional |
| O04 | `out-of-bounds-processing.constraints[].mode` | "mandatory for every listed constraint" (`DOC/...:365`) | mandatory (`parsing.py:54-56`) | optional, default `cyclic` (`parser.cpp:28`, `decoders.cpp:35`) | - | mandatory |
| O05 | `models[].heuristics` | documented, "Only available in GemsPy ... Antares modeler ... ignores this section" (`DOC/...:464-466`) | accepted; element names hard-coded in `_HEURISTIC_SCHEMA` (`parsing.py:76-134`) | **rejected** (not in `optimConfigFields`), contradicting "ignores" | - | accepted; element names copied into the schema |
| O06 | heuristic element `type` | optional, default `parameter` (`DOC/...:515`); the doc's own example omits it (`:481-489`) | **mandatory** (`type: ModelElementAccessType`, no default, `parsing.py:70-73`) | n/a | - | mandatory (follows GemsPy) |
| O07 | file absent / empty | "The file itself is optional" (`DOC/...:25`); examples write `models: []` "Antares Modeler (from v10.2.0) requires this file in every study" (`GEMS/resources/.../Hybrid_Study/input/optim-config.yml:2`) | absent -> defaults (`parsing.py:386-392`); **empty file -> error** (`safe_load` gives `None`, `model_validate(None)` fails, `:394-397`) | file **required** when `system.yml` exists (`Antares_Simulator/src/modeler/loadFiles/readOptimConfig.cpp:58-64`); empty content accepted (`:70-74`) | AntaREST creates an **empty** `optim-config.yml` with `touch()` (`antarest/study/dao/file/file_study_gems_system_dao.py:152-157`); 44 real Simulator test studies carry comment-only files | **decided: empty document accepted** (null or `{}`); GemsPy must be fixed to accept it |
| O08 | `scenario-scope` entries | int, quoted int, quoted range (`DOC/...:111-117`) | `Union[int, str]`, booleans rejected, `exclude` needs `include` (`parsing.py:310-349`) | any scalar, stored as string (`CPP/yml-optim-config/decoders.cpp:77-120`) | - | int >= 0 or string `a-b`; `exclude` needs `include` |
| O09 | model `id` format | "fully qualified model id, `<library-id>.<model-id>`" (`DOC/...:326`) | free `str` (`parsing.py:138`) | split on `.`, uses the first two parts (`readLibraries.cpp:102-107`) | - | exactly one dot |

## 5. Views inputs (taxonomy, catalog, view-config)

| ID | Observation | Evidence |
|---|---|---|
| W01 | **ViewsBuilder accepts snake_case spellings of every key** (`time_granularity`, `location_port`, ...) because its base model sets `validate_by_name=True` next to the kebab-case alias; the GEMS doc only documents kebab-case, and the schemas reject snake_case (as for L10 / S13). Two of ViewsBuilder's own test inputs write `time_granularity`. | `GEMS-ViewsBuilder/gems_views_builder/base_model.py`; `resources/tests_inputs/test_3/view_config.yml`, `resources/tests_inputs/filtering_and_breakdown/view_config.yml` |
| W02 | **Id patterns exist in code only**: the view `id` and aggregation pattern `id` are `[A-Za-z0-9_]+`, a metric reference is `<catalog>.<metric>` with `[A-Za-z0-9_-]` on both sides. The doc states none of them. The schema follows the code. | `GEMS-ViewsBuilder/gems_views_builder/input/view_config.py:37-52` |
| W03 | The doc says "at least one" pattern / metric; ViewsBuilder enforces it (`min_length=1`), while `metrics-definition`, `terms` and taxonomy `categories` may be empty. The schema mirrors this. | `view_config.py:53-58`, `input/catalog.py` |

## 6. Other findings worth knowing

* **Real files that fail the schemas** are recorded one by one in `conformance/real-examples-known.yml`
  with their class (upstream data bug, documented divergence, intentional negative test).
* **GEMS' own libraries do not follow GEMS' own naming rule** (L08), and `GEMS/doc` contradicts
  `GEMS/AGENTS.md` on hyphens in model ids.
* **GemsPy rejects `description` on `system`** although the GEMS doc documents it (S01) and two other
  consumers accept it.
* **AntaREST writes a file GemsPy cannot read** (empty `optim-config.yml`, O07): resolved on the schema side (empty is valid), GemsPy still needs the fix.
* **The PyPSA converter writes two things GemsPy's own schemas or the doc reject**: snake_case
  `model_libraries` (S13) and the Simulator-dialect `resolution-mode` (O01).
