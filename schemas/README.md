# GEMS JSON Schemas

JSON Schemas (draft 2020-12) for the GEMS YAML files. They check structure only; semantic rules
(references between models, ports, parameters, expression syntax) are checked by the interpreters.

| Schema | File |
|---|---|
| `gems-library.schema.json` | `model-libraries/*.yml` |
| `gems-system.schema.json` | `input/system.yml` |
| `gems-parameters.schema.json` | `parameters.yml` |
| `gems-optim-config.schema.json` | `input/optim-config.yml` |
| `gems-taxonomy.schema.json` | taxonomy files |
| `gems-catalog.schema.json` | catalog files |
| `gems-view-config.schema.json` | views configuration files |

They follow the documentation in `doc/user-guide/input-files/` and the GemsPy parsers
(unknown keys are rejected, keys are kebab-case, defaults are not required).
Identifier naming (lowercase, underscores) is documented but not enforced by GemsPy, so it is not enforced here.

Editor use (VS Code, YAML extension):

```json
{ "yaml.schemas": { "schemas/gems-library.schema.json": "**/model-libraries/*.yml",
                    "schemas/gems-system.schema.json": "**/system.yml" } }
```

`tests/unit_tests/test_json_schemas.py` validates the repository's own YAML files against them.

`gems-relationships.json` lists the cross-file references of a study (which key of which file must match which key of another),
with cardinality and the rule applied. It is documentation/tooling input, not a JSON Schema.

## Checking a study folder

```bash
python schemas/check_study.py path/to/study                 # JSON Schema validation + cross-file checks
python schemas/check_study.py path/to/study --libs libraries  # libraries kept outside the study
python schemas/check_study.py path/to/study --json --no-schema
```

Each finding names the relationship id from `gems-relationships.json`. The exit status is 1 when there is at least one
error. Relationships marked `derived` (expression names, time-scope coverage of data series) are not checked.
Data series are looked up as `.csv`, `.txt` or `.tsv`. With `--libs`, only libraries used by the system are taken from
those folders, and the study's own copy of a library wins.
