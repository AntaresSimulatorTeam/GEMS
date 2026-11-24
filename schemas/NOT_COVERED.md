# What the schemas do NOT cover

JSON Schema validates the shape of one parsed document. The rules below need more than that. They are
not faked in the schemas; a consumer that needs them must keep (or write) code for them. The IDs are
referenced from the schema descriptions.

## Not expressible in JSON Schema

| ID | Rule | Where it lives today | Notes |
|---|---|---|---|
| N01 | **Expression syntax and semantics**: `expression`, `definition`, `lower-bound`, `upper-bound` hold the GEMS expression language (operators, `sum`, `[t-1]`, `sum_connections(port.field)`, linearity, port operators only in binding constraints, ...). The schemas only check "string, or a number read as a literal". | GemsPy ANTLR grammar and `gems_craft.expression`; Antares_Simulator `modeler` expression parser; GEMS `doc/user-guide/syntax.md` | A regex would be a fake: the language is not regular. |
| N09 | **YAML-level facts that survive parsing only partly**: duplicate keys (PyYAML keeps the last one silently; Antares_Simulator reports "Duplicated field", `checkFields.cpp:132-139`), YAML 1.1 vs 1.2 scalar typing (`yes`, `1e-3` without a dot are strings or booleans depending on the parser), anchors/aliases, tags. | the YAML parser in each project | The runner uses `yaml.safe_load` (YAML 1.1). A consumer using a YAML 1.2 parser can see different types for the same file. |
| N10 | **Files that are not one of the seven kinds**: `parameters.yml`, `modeler-scenariobuilder.dat`, the calendar CSV (`absolute_time_index,block,granular_date`, constant step), data-series CSV/TSV. | - | Out of scope of this draft. |
