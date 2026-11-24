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

## 6. Other findings worth knowing

* **Real files that fail the schemas** are recorded one by one in `conformance/real-examples-known.yml`
  with their class (upstream data bug, documented divergence, intentional negative test).
* **GEMS' own libraries do not follow GEMS' own naming rule** (L08), and `GEMS/doc` contradicts
  `GEMS/AGENTS.md` on hyphens in model ids.
