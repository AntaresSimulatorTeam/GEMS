# What the schemas do NOT cover

JSON Schema validates the shape of one parsed document. The rules below need more than that. They are
not faked in the schemas; a consumer that needs them must keep (or write) code for them. The IDs are
referenced from the schema descriptions.

## Not expressible in JSON Schema

| ID | Rule | Where it lives today | Notes |
|---|---|---|---|
| N01 | **Expression syntax and semantics**: `expression`, `definition`, `lower-bound`, `upper-bound` hold the GEMS expression language (operators, `sum`, `[t-1]`, `sum_connections(port.field)`, linearity, port operators only in binding constraints, ...). The schemas only check "string, or a number read as a literal". | GemsPy ANTLR grammar and `gems_craft.expression`; Antares_Simulator `modeler` expression parser; GEMS `doc/user-guide/syntax.md` | A regex would be a fake: the language is not regular. |
| N02 | **Cross-reference resolution**: port `type` -> a port type of some library in the system; `port-field-definitions[].port/field` -> ports/fields of the model; identifiers used in expressions -> parameters, variables, ports of the model; component `model` -> `<library>.<model>` in the loaded libraries; `connections[].component1/2` and `port1/2` -> components and ports; both ends of a connection share a port type; `area-connections` / `thermal-capacity-connections` -> component, port whose type declares the matching `*-connection`; optim-config `models[].id` and `constraints/variables/objective-contributions[].id` -> the system's models; heuristic element `id` -> a parameter or variable of the model, with the right time dependence; `integer-strategy` heuristic -> an entry in optim-config `heuristics`. | `gems_craft.model.resolve_library`, `gems_craft.study.resolve_components`, `gems_craft.optim_config.validation`; Simulator `model-converter` | Needs several files at once. |
| N03 | **Time-series dimension and data-series checks**: a series named by `value` exists in `data-series/` (`.csv` / `.tsv`), covers `time-scope`, has the columns the scenario builder expects, is used with consistent `time-dependent` / `scenario-dependent` flags, `value` of a dependent parameter is only allowed if the model parameter is declared dependent (`system.md:65-66`). | GemsPy `study.data`, `study.scenario_builder`; AntaREST `_resolve_data_series_file`; Simulator data-series importer | Depends on files outside the YAML. The doc's "Cannot be set to true if the model parameter is not declared time-dependent" is a library-vs-system rule (N02 family). |
| N04 | **Defaults being applied**: `time-dependent` / `scenario-dependent` default to `true` in libraries and `false` in systems, `variable-type` to `continuous`, `resolution.mode` to `frontal` (Simulator: `sequential-subproblems`), `carry-over-length` to `block-overlap`, `integer-strategy.id` to `exact`, `scenario-scope` to scenario 0, `model-decomposition.location` to `subproblems`, `out-of-bounds` to `cyclic`. The `default` keyword is only an annotation; validators do not insert it. | each interpreter | The schemas state defaults in `description` text only. Note that the same word is true/false depending on the file kind. |
| N05 | **Cross-field, cross-entry and ordering constraints**: `first-time-step <= last-time-step`; `block-overlap < block-length`; `carry-over-length <= block-overlap`; range `a-b` with `a <= b`; the scenario set is non-empty after `exclude`; unique ids inside a list (library ids, model ids, port ids, parameter ids, component ids, a model at most once in optim-config `models`, a heuristic at most once); `exclude` entries outside `include` only warn. (`dependentRequired`, `if/then/else`, `contains` and `maxItems` *are* used where they can express something, e.g. block-length required for windowed modes, heuristic element sets.) | `gems_craft.optim_config.parsing` validators, resolvers | JSON Schema cannot compare two numbers, and `uniqueItems` compares whole items, not one key. |
| N06 | **Solver option strings**: `solver-options.parameters` is `KEY VALUE ...` with an even token count; names and values are solver specific. | `SolverOptionsConfig.parsed_parameters` | A pattern would wrongly accept or reject solver-specific values. |
| N07 | **Taxonomy rules**: a model's `taxonomy-category` exists in the taxonomy named by `library.taxonomy` and the model exposes the variables, parameters, ports, ... the category requires; every property declared by a model is set on each component of that model (`library.md:317`); no property declared twice. | `gems_craft.model.validation`, ViewsBuilder `validation/` | Needs the taxonomy file and the system. |
| N08 | **Semantics of the optimization problem**: master/subproblem placement rules (master variables time-independent, master constraints only reference master variables, integer variables in `master`), heuristics not combined with Benders, linearity of objective contributions. | `gems_craft.optim_config.validation` | Need the resolved model. |
| N09 | **YAML-level facts that survive parsing only partly**: duplicate keys (PyYAML keeps the last one silently; Antares_Simulator reports "Duplicated field", `checkFields.cpp:132-139`), YAML 1.1 vs 1.2 scalar typing (`yes`, `1e-3` without a dot are strings or booleans depending on the parser), anchors/aliases, tags. | the YAML parser in each project | The runner uses `yaml.safe_load` (YAML 1.1). A consumer using a YAML 1.2 parser can see different types for the same file. |
| N10 | **Files that are not one of the seven kinds**: `parameters.yml`, `modeler-scenariobuilder.dat`, the calendar CSV (`absolute_time_index,block,granular_date`, constant step), data-series CSV/TSV. | - | Out of scope of this draft. |

## Not covered because no project specifies it

* **`optim-config`** exists in two incompatible dialects (DISCREPANCIES O01-O07). Only the DOC/GemsPy one
  is described; the Simulator one is rejected on purpose. It is provisional.
* **Whether a missing optional file is an error** (optim-config absent or empty, O07) is a rule about the
  study folder, not about a document.

## Where the schemas are intentionally looser than the doc

* Ids follow the relaxed `Identifier`, not the doc's `[a-z0-9_]+` rule (L08).
* `system.id`, `system.components` are optional (GemsPy), not mandatory (AntaREST / doc wording).
* Parameter `time-dependent` / `scenario-dependent` are optional with default `false` in a system (GemsPy, Simulator), not mandatory (doc, AntaREST).
* An empty optim-config document (null) is accepted, as in the Simulator and AntaREST; GemsPy rejects it (O07, decided by the maintainer).

## Where the schemas are intentionally stricter than a reference implementation

* Unknown root keys next to `system` / `library` are rejected (GemsPy ignores them next to `system`, S11).
* snake_case spellings are rejected (GemsPy and AntaREST accept them, L10 / S13).
* A constant system parameter must carry a number and a dependent one a string (GemsPy does not check at
  parse time, S05).
* Heuristic element sets and output types are enforced in the schema (GemsPy enforces them in code).
