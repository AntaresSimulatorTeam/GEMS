# Validation Tests

These tests live in `tests/validation_tests/` and require **no Antares binary**. They run in under a second and serve as a fast gate on every PR before the e2e tests.

---

## Overview

| File | What it checks | Scope |
|------|----------------|-------|
| `test_yaml_syntax.py` | All YAML files are syntactically valid | `libraries/`, `resources/` |
| `test_library_schema.py` | Library files have the required top-level structure | `libraries/` |
| `test_port_type_consistency.py` | Port references in models resolve to defined port-types | `libraries/` |
| `test_study_system_validation.py` | Component/connection references in studies resolve | `resources/**/system.yml` |
| `test_parameter_completeness.py` | Parameters in studies match the model definition | `resources/**/system.yml` |
| `test_data_series_integrity.py` | Time-series CSV files referenced in studies exist | `resources/**/system.yml` |
| `test_expression_syntax.py` | Mathematical expressions in models are well-formed | `libraries/` |
| `test_library_versioning.py` | Each library has a version file and a changelog | `libraries/`, `versions/` |

---

## test_yaml_syntax.py

**What:** Parses every `.yml` and `.yaml` file under `libraries/` and `resources/` with PyYAML.

**Catches:** Malformed YAML — bad indentation, unclosed brackets, invalid characters, duplicate keys.

**Does not catch:** Correct YAML that is semantically wrong (e.g. a model missing its `id`).

**Note:** Dangling symlinks (files in `model-libraries/` pointing to paths on other machines) are skipped automatically and do not cause failures.

**Example failure:**
```
libraries/antares_legacy_models.yml: mapping values are not allowed here
  in "<unicode string>", line 18, column 7
```

---

## test_library_schema.py

**What:** Validates the top-level structure of each library YAML file against the `LibraryFile` Pydantic schema.

**Checks:**
- The file has a top-level `library` key
- `library.id` exists and is non-empty
- `library.models` is a list where each entry has a non-empty `id`
- `library.port-types` is a list where each entry has a non-empty `id`

**Catches:** Libraries missing required fields, wrong nesting (e.g. `models` at the wrong level), empty IDs.

**Does not catch:** Whether model references or port-type references are valid (those are checked in subsequent tests).

**Example failure:**
```
antares_legacy_models.yml: model is missing its id
```

---

## test_port_type_consistency.py

**What:** For every port declared in every model, checks that its `type` field references a port-type that is defined in the same library.

**Catches:** Typos in port-type names, port-types that were renamed or removed while model ports still reference the old name.

**Example failure:**
```
antares_legacy_models.yml: model 'thermal' port 'balance_port' references
undefined port-type 'flows'. Defined port-types: ['flow']
```

---

## test_study_system_validation.py

**What:** Three separate tests run on every `system.yml` under `resources/`:

### test_component_model_references
Checks that every `component.model` value (`library_id.model_id`) resolves to a real model in a known library.

- The format must be `library_id.model_id` (exactly one dot)
- `library_id` must match the `id` of a file in `libraries/`
- `model_id` must match a model defined in that library

**Catches:** Typos in model references, models that were renamed in the library but not updated in studies.

**Example failure:**
```
resources/.../system.yml: component 'th1' references unknown model
'therml' in library 'antares_legacy_models'. Known models: ['area', 'load', 'thermal', ...]
```

### test_connection_component_references
Checks that `component1` and `component2` in every connection refer to components that are declared in the same system.

**Catches:** Connections referencing components that were renamed or removed.

**Example failure:**
```
resources/.../system.yml: connection references unknown component1
'bus_old'. Known components: ['bus1', 'load_bus', 'th1', 'th2']
```

### test_connection_port_references
Checks that `port1` and `port2` in every connection refer to ports that are defined on the respective component's model.

**Catches:** Connections using port names that don't exist on the model, port renames in the library not reflected in studies.

**Example failure:**
```
resources/.../system.yml: connection references port 'injection_port'
on component 'bus1', but that model only defines ports: ['balance_port']
```

---

## test_parameter_completeness.py

**What:** For every component in every `system.yml`, checks that every parameter it declares actually exists in the referenced model's parameter list.

**Catches:** Parameters that were renamed or removed from a library model but are still referenced in study files. This is the exact class of bug encountered during the v10.0.0 migration, where `nb_units_max`, `nb_units_min`, etc. were removed from the thermal model but studies still declared them.

**Does not check:** Whether all required parameters are provided (only that provided parameters are valid). This is intentional — the modeler handles missing parameters.

**Example failure:**
```
resources/.../system.yml: component 'th1' sets parameter 'nb_units_max'
which is not defined in model 'antares_legacy_models.thermal'.
Defined parameters: ['minimum_generation_modulation', 'p_max_cluster', ...]
```

---

## test_data_series_integrity.py

**What:** For every `time-dependent: true` parameter in a `system.yml` that has a string value (i.e. a filename reference rather than an inline scalar), checks that the corresponding `.csv` file exists in the study's `data-series/` directory.

**Catches:** Broken references to time-series files — renames, deletions, or missing files.

**Does not check:** The content of the CSV (whether it has the right number of rows, valid numbers, etc.). Only existence is verified.

**Example failure:**
```
resources/.../system.yml: component 'load_bus' parameter 'load'
references data series 'demand', but
'resources/.../input/data-series/demand.csv' does not exist
```

---

## test_expression_syntax.py

**What:** Six separate tests validate the mathematical expressions embedded in library model definitions.

### test_constraint_has_single_comparison
Every `constraints` and `binding-constraints` expression must contain exactly one comparison operator (`=`, `<=`, or `>=`).

**Catches:** Expressions with no comparison (not a valid constraint), two comparisons (chained inequalities are not supported), or accidental `==` (Python-style equality).

**Example failure:**
```
antares_legacy_models.yml / model 'thermal' / constraint 'max_generation':
expected exactly 1 comparison operator (=, <=, >=), found 0
in: 'generation * p_max_unit'
```

### test_expression_identifiers_are_defined
Every identifier appearing in a constraint, objective contribution, or port-field definition must be declared as either a parameter or a variable in the same model.

Identifiers inside `sum_connections(port.field)` are excluded — ports and fields are validated separately. Built-in keywords (`sum`, `sum_connections`, `min`, `max`, `ceil`, `floor`, `expec`, `t`) are also excluded.

**Does not cover:** Variable bounds — those are checked by `test_variable_bound_uses_only_parameters` with a stricter rule.

**Catches:** Typos in variable or parameter names, identifiers left over from a rename, references to identifiers from a different model.

**Example failure:**
```
antares_legacy_models.yml / model 'thermal' / constraints[max_generation]:
undefined identifier(s) ['p_max_units'] in expression: 'generation <= nb_units_on * p_max_units'
Declared identifiers: ['d_min_down', 'd_min_up', 'generation', ..., 'p_max_unit', ...]
```

### test_variable_bound_uses_only_parameters

Every `lower-bound` and `upper-bound` expression on a variable must only reference parameters, not decision variables.

Bounds are fixed at problem-construction time before the solver runs, so they cannot depend on the values of decision variables.

**Does not check:** Whether the bound identifier is actually declared (that is covered by `test_expression_identifiers_are_defined` for the same expression scope).

**Catches:** Bounds that accidentally reference a variable instead of the intended parameter, especially after a parameter is promoted to a variable during model refactoring.

**Example failure:**
```
antares_legacy_models.yml / model 'thermal' / variables[generation].upper-bound:
bound expression may only reference parameters, but found non-parameter
identifier(s) ['nb_units_on'] in: 'nb_units_on * p_max_unit'.
Declared parameters: ['p_max_unit', 'p_min_unit', ...]
```

### test_no_direct_port_field_in_constraints

No constraint or binding-constraint expression may reference a port field directly (e.g. `balance_port.flow`). The `sum_connections(port.field)` operator must always be used, even when only a single component is connected to the port.

**Catches:** Direct port field usage that would cause the Antares modeler to reject the model at runtime.

**Example failure:**
```
basic_models_library.yml / model 'bus' / binding-constraints[balance]:
direct port field reference(s) ['balance_port.flow'] are not allowed in
constraint expressions. Use sum_connections() instead.
```

### test_port_field_definition_references_valid_port_and_field
Every `port-field-definition` entry must:
- Reference a `port` that is declared in the model's `ports` list
- Reference a `field` that is declared on that port's type in the library's `port-types`

**Catches:** Port-field definitions pointing to non-existent ports or fields, renames of port-types not propagated to port-field definitions.

**Example failure:**
```
antares_legacy_models.yml / model 'thermal': port-field-definition
on port 'balance_port' references field 'power', but valid fields
for this port type are: ['flow']
```

### test_sum_connections_references_valid_port_and_field
Every `sum_connections(port.field)` call in a constraint expression must:
- Reference a `port` that is declared in the model's `ports` list
- Reference a `field` that is declared on that port's type

**Catches:** `sum_connections()` calls with wrong port or field names.

**Example failure:**
```
basic_models_library.yml / model 'bus' / constraint 'balance':
sum_connections() references field 'power' on port 'balance_port',
but valid fields for this port type are: ['flow']
```

---

## test_library_versioning.py

**What:** Two tests per library file enforce the governance requirement that every library is independently versioned and has a changelog.

### test_library_has_version_file
Checks that a corresponding version tracking file exists at `versions/<library_name>.txt` and is non-empty.

**Catches:** New library files added to `libraries/` without a corresponding version entry.

**Example failure:**
```
Missing version file for library 'new_models.yml':
expected 'versions/new_models.txt'
```

### test_library_has_changelog
Checks that a changelog file exists at `libraries/CHANGELOG-<library_name>.md` and is non-empty.

**Catches:** Library files modified without a changelog, new libraries added without documentation of what they contain.

**Example failure:**
```
Missing changelog for library 'new_models.yml':
expected 'libraries/CHANGELOG-new_models.md'
```

---

## Running the validation tests

```bash
python -m pytest tests/validation_tests -v
```

To run a single file:

```bash
python -m pytest tests/validation_tests/test_expression_syntax.py -v
```

To run a single test function:

```bash
python -m pytest tests/validation_tests/test_expression_syntax.py::test_constraint_has_single_comparison -v
```
