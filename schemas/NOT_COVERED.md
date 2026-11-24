# What the schemas do NOT cover

JSON Schema validates the shape of one parsed document. The rules below need more than that. They are
not faked in the schemas; a consumer that needs them must keep (or write) code for them. The IDs are
referenced from the schema descriptions.

## Not expressible in JSON Schema

| ID | Rule | Where it lives today | Notes |
|---|---|---|---|
| N01 | **Expression syntax and semantics**: `expression`, `definition`, `lower-bound`, `upper-bound` hold the GEMS expression language (operators, `sum`, `[t-1]`, `sum_connections(port.field)`, linearity, port operators only in binding constraints, ...). The schemas only check "string, or a number read as a literal". | GemsPy ANTLR grammar and `gems_craft.expression`; Antares_Simulator `modeler` expression parser; GEMS `doc/user-guide/syntax.md` | A regex would be a fake: the language is not regular. |
| N02 | **Cross-reference resolution**: port `type` -> a port type of some library in the system; `port-field-definitions[].port/field` -> ports/fields of the model; identifiers used in expressions -> parameters, variables, ports of the model; component `model` -> `<library>.<model>` in the loaded libraries; `connections[].component1/2` and `port1/2` -> components and ports; both ends of a connection share a port type; `area-connections` / `thermal-capacity-connections` -> component, port whose type declares the matching `*-connection`; optim-config `models[].id` and `constraints/variables/objective-contributions[].id` -> the system's models; heuristic element `id` -> a parameter or variable of the model, with the right time dependence; `integer-strategy` heuristic -> an entry in optim-config `heuristics`. | `gems_craft.model.resolve_library`, `gems_craft.study.resolve_components`, `gems_craft.optim_config.validation`; Simulator `model-converter` | Needs several files at once. |
| N07 | **Taxonomy rules**: a model's `taxonomy-category` exists in the taxonomy named by `library.taxonomy` and the model exposes the variables, parameters, ports, ... the category requires; every property declared by a model is set on each component of that model (`library.md:317`); no property declared twice. | `gems_craft.model.validation`, ViewsBuilder `validation/` | Needs the taxonomy file and the system. |
| N09 | **YAML-level facts that survive parsing only partly**: duplicate keys (PyYAML keeps the last one silently; Antares_Simulator reports "Duplicated field", `checkFields.cpp:132-139`), YAML 1.1 vs 1.2 scalar typing (`yes`, `1e-3` without a dot are strings or booleans depending on the parser), anchors/aliases, tags. | the YAML parser in each project | The runner uses `yaml.safe_load` (YAML 1.1). A consumer using a YAML 1.2 parser can see different types for the same file. |
| N10 | **Files that are not one of the seven kinds**: `parameters.yml`, `modeler-scenariobuilder.dat`, the calendar CSV (`absolute_time_index,block,granular_date`, constant step), data-series CSV/TSV. | - | Out of scope of this draft. |

## Where the schemas are intentionally looser than the doc

* Ids follow the relaxed `Identifier`, not the doc's `[a-z0-9_]+` rule (L08).

## Where the schemas are intentionally stricter than a reference implementation

* Unknown root keys next to `system` / `library` are rejected (GemsPy ignores them next to `system`, S11).
* snake_case spellings are rejected (GemsPy and AntaREST accept them, L10 / S13).
