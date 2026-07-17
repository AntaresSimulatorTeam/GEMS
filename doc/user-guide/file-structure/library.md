<div style="display: flex; justify-content: flex-end;">
  <a href="../../../..">
    <img src="../../../assets/gemsV2.png" alt="GEMS Logo" width="150"/>
  </a>
</div>

# Library File

A library file defines a library of two collections of abstract objects:

- [Models](#models) - Contains the mathematical formulation for component type
- [Ports Types](#port-types) - Describe the kinds of connections models can have

!!! warning "Design proposal — not yet implemented"
    A proposed third collection, [Library-Level Sets](#library-level-sets), declares global custom
    index sets shared across `port-types` and `models`. Not yet implemented in
    [GemsPy](../../index.md).

The library file is a YAML file with a single root key, `library`. Under this root, the library’s identifier, an optional description, and the collections of `port-types` and `models` are defined. All fields, unless explicitly marked as optional, must be present for the library to be considered valid. The following example illustrates the structure of a simple library file:

```yaml
library:

  id: example_library
  description: "Example model library"

  port-types:
    - id: flow_port
      description: "Power flow port"
      fields:
        - id: flow

  models:
    - id: bus
      description: "A simple balance node model"
      ports:
        - id: balance_port
          type: flow_port
      binding-constraints:
        - id: balance
          expression: sum_connections(flow_port.flow) = 0
```

In this example, one port type `flow_port` and one model `bus` are defined. The model contains a port named `balance_port` of type `flow_port`, along with a binding constraint equation that enforces **First Kirchhoff Law**.

The equation `sum_connections(injection.flow) = 0` follows the GEMS [**Mathematical Expression Syntax**](../mathematical-syntax.md#ports).

## Rules for id naming

All `id's` in the model library and system file must respect the following:

- Alphanumeric characters are allowed, as well as the underscore _ character
- All other characters are prohibited
- Only lower-case is allowed

!!! warning "Design proposal — not yet implemented"
    A local [set](#sets)'s `id` must not collide with any parameter or variable `id` within the same
    model, or with the reserved literal `t`. **A global (library-level) set's `id` must likewise never
    be the reserved literal `t`** — it is just as usable bare, in any model in the library, as a local
    set's id is, so the same ambiguity applies.

    More generally: **no locally-declared identifier in a model — a parameter, variable, local set,
    port, constraint, binding-constraint, objective-contribution, or extra-output `id` — may collide
    with any [global (library-level) set](#library-level-sets) `id` visible in that library.** A
    global set's `id` is usable bare from inside any model in the library (via `indexed-by`, or as a
    bare current-position reference) without that model declaring anything locally, so any local `id`
    that happens to match one creates the same kind of ambiguity a local-set/parameter collision would.

    These rules are part of the
    [Custom Sets and Indexing](../mathematical-syntax.md#custom-sets-and-indexing-proposed) proposal —
    not yet implemented in [GemsPy](../../index.md).

## Collections and key fields in library file

Every library file must begin with the following header with optional `description` and `version`:

```yaml
library:
  id: example_library
  description: "Example model library"
  version: "1.0.0"
```

| Element | Type | Description |
|------|------|--------------------------|
| `id`| String | A unique identifier for the library. This `id` is used by [system files](../system.md) to reference models from this library via the `model-libraries` field. It must be unique across all libraries that are used to build a system and must follow standard [naming rules](#rules-for-id-naming).|
| `description` | String | *(Optional)* A human-readable description of the library’s content or purpose.|
| `version` | String | *(Optional)* A version string for the library (e.g. `"1.0.0"`). Should be bumped whenever the library changes; see the corresponding `CHANGELOG` file.|

### Library-Level Sets

!!! warning "Design proposal — not yet implemented"
    This section describes a **proposed** extension to the library file schema. It is not yet
    implemented in [GemsPy](../../index.md). See
    [Custom Sets and Indexing](../mathematical-syntax.md#custom-sets-and-indexing-proposed) for the
    full expression-syntax proposal this schema supports.

The `sets` collection, a sibling of `port-types` and `models`, declares **global** custom index sets
— shared by every model and port-type field in this library that references them. This is the only
kind of custom set that may cross a port: a [port-type field](#port-types)'s `indexed-by` may only
name a global set, and the argument passed to `sum_connections` inside a
[binding constraint](#binding-constraints) may only be indexed by one, since every component
connecting through a port must agree on the exact same index domain (see
[Why the distinction matters](../mathematical-syntax.md#why-the-distinction-matters)). This does
**not** restrict a binding constraint as a whole — it may still freely reference the model's own local
sets in parts of its expression that don't cross the port. Model-level, per-component-varying sets are
declared separately — see [Sets](#sets) under Models below.

This collection is **optional**.

A global set's concrete size or contents are **never** given in the library — only its `id`,
`description`, and **kind** (`ordinal` or `enumerated`). This mirrors GEMS's existing pattern of the
library declaring structure while the system file assigns concrete values (the same way a model
declares that a parameter exists, but only `system.yml` gives it a value). The concrete `cardinality`
(ordinal) or `elements` (enumerated) are always supplied exactly once, study-wide, in
[`system.yml`'s Global Sets section](../system.md#global-sets) — see below.

```yaml
library:
  id: example_library
  sets:
    - id: fuel
      kind: enumerated
    - id: segment_count_set
      kind: ordinal
```

| Element | Type | Description |
|------|------|--------------------------|
|`id`| String | Unique set identifier within the library. Must follow the [naming rules](#rules-for-id-naming).|
| `description`| String | *(Optional)* A human-readable description of the set's purpose.|
|`kind`| Enum | `ordinal` or `enumerated`. Determines which indexing forms are valid against this set in expressions (see below) — the concrete size/elements are resolved later, in `system.yml`, so this is the only thing the library itself needs to know.|

Because a global set's `elements` are never known at library-authoring time, **bare named-element
access (e.g. `X{gas}`) is never valid against a global set inside library expressions** — a model may
only use ordinal-style access against a global set: the bare set-id for the current position
(`X{fuel}`), a relative shift (`X{fuel+1}`), or an explicit integer position (`X{0}`). This holds
regardless of `kind`: `enumerated` still means "named, ordered elements" once `system.yml` resolves it,
it just means library expressions can only reach those elements by position, never by name. Contrast
with a **local** set whose `elements` are given directly in the model (see [Sets](#sets) under Models
below) — there, named access is fully available, since the names are known at library-authoring time.

**Recommended practice** (a `system.yml`-level concern now, since that's the only place a global set's
concrete contents ever exist): make each study's instantiation *universal* — the superset of every
element that could ever be relevant across the whole system — and express per-component variation
through data (e.g. a `0` capacity/bound for unused elements) rather than through differing membership.

### Port Types

The `port-types` collection defines the set of port types available within a library. These port types can be used by models/components to communicate with each other by exchanging linear expressions through [connections](../system#connections).

This collection is **optional**. A library may define no port types, although such a library has limited practical use, as its models cannot interact through ports. Alternatively, a library may rely on port types defined in another library, enabling reuse and interoperability across libraries.

```yaml
port-types:
    - id: flow_port
      description: "Power flow port"
      fields:
        - id: flow
    - id: example_port
      fields:
        - id: field_1
        - id: field_2
```

| Element | Type | Description |
|------|------|--------------------------|
|`port-types`| List | A list of port type definitions that models can use for connecting to other models.|
| `id`| String | Unique `id` for the port type within this library. Must follow the [naming rules](#rules-for-id-naming) and must not conflict with other port type `id`s in the same library.|
| `description` | String | *(Optional)* A human-readable description of the port type’s purpose.|
|`fields`| List | A list of fields carried by this port. Each field has an `id` (unique within the port type) that identifies a scalar floating-point quantity exchanged through the port (e.g. a power flow value).|

!!! warning "Design proposal — not yet implemented"
    A field may declare `indexed-by`, referencing one or more [library-level set](#library-level-sets)
    `id`s (a single `id`, or a list for a field indexed by more than one set), to mark the field as
    carrying a custom-set dimension (never a model-level set — see
    [Port fields and custom sets](../mathematical-syntax.md#port-fields-and-custom-sets)):
    ```yaml
    port-types:
      - id: multi_fuel_port
        fields:
          - id: flow
            indexed-by: fuel
    ```
    Not yet implemented in [GemsPy](../../index.md).

### Models

The `models` collection defines all model types that can be instantiated within a system. In the following YAML file, two models are defined: `bus` and `storage`.

```yaml
  models:
    - id: bus
      parameters:
        - id: spillage_cost
          time-dependent: false
          scenario-dependent: false
        - id: unsupplied_energy_cost
          time-dependent: false
          scenario-dependent: false
      variables:
        - id: spillage
          lower-bound: 0
          variable-type: continuous
        - id: unsupplied_energy
          lower-bound: 0
          variable-type: continuous
      ports:
        - id: balance_port
          type: flow
      binding-constraints:
        - id: balance
          expression: sum_connections(balance_port.flow) = spillage - unsupplied_energy
      objective-contributions:
        - id: objective
          expression: sum(spillage_cost * spillage + unsupplied_energy_cost * unsupplied_energy)
      extra-outputs:
        - id: marginal_price
          expression: dual(balance)

    - id: storage
      parameters:
        - id: reservoir_capacity
          time-dependent: false
          scenario-dependent: false
        - id: injection_nominal_capacity
          time-dependent: false
          scenario-dependent: false
        - id: withdrawal_nominal_capacity
          time-dependent: false
          scenario-dependent: false
        - id: efficiency_injection
          time-dependent: false
          scenario-dependent: false
        - id: efficiency_withdrawal
          time-dependent: false
          scenario-dependent: false
        - id: initial_level
          time-dependent: false
          scenario-dependent: true
      variables:
        - id: p_injection
          lower-bound: 0
          upper-bound: injection_nominal_capacity
          variable-type: continuous
        - id: p_withdrawal
          lower-bound: 0
          upper-bound: withdrawal_nominal_capacity
          variable-type: continuous
        - id: level
          lower-bound: 0
          upper-bound: reservoir_capacity
          variable-type: continuous
      ports:
        - id: injection_port
          type: flow
      port-field-definitions:
        - port: injection_port
          field: flow
          definition: p_withdrawal - p_injection
      constraints:
        - id: initial_level_constraint
          expression: level[0] = initial_level * reservoir_capacity
        - id: level_dynamic_constraint
          expression: level[t+1] = level + efficiency_injection * p_injection - efficiency_withdrawal * p_withdrawal

```

A model is an abstract object, that will be instantiated once or several times in a system and is defined by:

#### Unique Identifier and Description

| Element | Type | Description |
|------|------|--------------------------|
|`id`| String | A unique identifier for the model within a library. Must follow the [naming rules](#rules-for-id-naming). [System files](../system#components) reference the model by combining the library `id` and the model `id`.|
| `description`| String | *(Optional)* Text description of the model.|

#### Parameters

A list of parameters that this model takes. Each parameter defines a configurable value for the model when it’s used in a system. For each parameter user can specify specify:

| Element | Type | Description |
|------|------|--------------------------|
|`id`| String | Unique parameter identifier within the model. Must follow the [naming rules](#rules-for-id-naming).|
| `time-dependent`| Boolean | `true` or `false`. If `true`, this parameter can vary over the simulation timeline (meaning it will be associated with a time series input). If `false`, it is treated as constant in time.|
|`scenario-dependent`| Boolean | `true` or `false`. If `true`, the parameter can have different values in different scenarios (i.e., it requires scenario-specific data). If `false`, it does not vary between scenarios.|

Together, these flags define how the parameter can be provided — as a single value, a time series, scenario-based data, or a matrix. For details on how parameter data is stored and referenced, see the [data-series](./data-series.md). For how parameter values are assigned in the system file, see [System — Parameters](../system#parameters).

#### Variables

A list of decision variables introduced by this model for the optimization problem. Each variable includes:

| Element | Type | Description |
|------|------|--------------------------|
|`id`| String | Unique variable name within the model. Must follow the [naming rules](#rules-for-id-naming).|
| `variable-type`| Enum | The type of variable: `continuous`, `integer`, or `binary`. This determines how the solver treats the variable.|
|`lower-bound`| Number or Expression | *(Optional)* Lower bound for the variable. Can be a numeric literal or an expression using only model parameters and constants. Defaults to −∞ for `continuous`/`integer`, or `0` for `binary`.|
|`upper-bound`| Number or Expression | *(Optional)* Upper bound for the variable. Can be a numeric literal or an expression using only model parameters and constants. Defaults to +∞ for `continuous`/`integer`, or `1` for `binary`.|

Any expression used for bounds must use only constants or models parameters.

For example, variable `p_injection` in the `storage` model is defined as a continuous variable with upper bound set up by parameters `injection_nominal_capacity` and lower bound set up by 0.

```yaml
variables:
  - id: p_injection
    lower-bound: 0
    upper-bound: injection_nominal_capacity
    variable-type: continuous
```

#### Sets

!!! warning "Design proposal — not yet implemented"
    This section describes a **proposed** extension to the library file schema. It is not yet
    implemented in [GemsPy](../../index.md). See
    [Custom Sets and Indexing](../mathematical-syntax.md#custom-sets-and-indexing-proposed) for the
    full expression-syntax proposal this schema supports.

(Optional) A list of **local** custom index sets declared by this model — usable to index this
model's own `parameters` and `variables` (via the new `indexed-by` field described below) and to
index its `constraints`, `binding-constraints`, `objective-contributions`, and `extra-outputs`. Local
sets may vary per component (see `cardinality` below) but are not visible outside this model. A model
may also use a [library-level set](#library-level-sets) directly via `indexed-by`, without declaring
anything here — declare a local set only when the index genuinely needs to vary per component or stay
internal to this model; see
[Why the distinction matters](../mathematical-syntax.md#why-the-distinction-matters).

| Element | Type | Description |
|------|------|--------------------------|
|`id`| String | Unique set identifier within the model. Must follow the [naming rules](#rules-for-id-naming) (including the naming-collision constraints against parameters/variables/`t`/global sets described there).|
| `description`| String | *(Optional)* A human-readable description of the set's purpose.|
|`cardinality`| Integer or parameter `id` | *(Ordinal sets)* Either an integer literal or the `id` of a scalar, non-time/scenario-dependent, non-set-indexed parameter of this model. Defines 0-based integer positions `0 .. cardinality-1`. Referencing a parameter lets different components instantiating this model have different set sizes, using the ordinary per-component parameter-assignment mechanism (see [System — Parameters](../system.md#parameters)).|
|`elements`| List of strings | *(Enumerated sets)* An ordered list of named elements. If omitted, the set's concrete elements must instead be supplied per component in the [system file](../system.md#local-sets).|

Exactly one of `cardinality` or `elements` must be given, unless `elements` is intentionally omitted
to defer the concrete list to each component (see [System — Local Sets](../system.md#local-sets)).

```yaml
models:
  - id: multi_segment_storage
    parameters:
      - id: segment_count
        time-dependent: false
        scenario-dependent: false
    sets:
      - id: segment
        description: "Price segments of the storage's marginal-value curve"
        cardinality: segment_count
      - id: operating_mode
        elements: [off, standby, full]
```

To mark a parameter or variable as indexed by one (or more) of these sets, add an `indexed-by`
field, analogous to `time-dependent`/`scenario-dependent`. It resolves against this model's own local
sets, plus every [library-level set](#library-level-sets) visible in this library:

| Element | Type | Description |
|------|------|--------------------------|
|`indexed-by`| Set `id`, or list of set `id`s | *(Optional)* Declares that this parameter/variable carries one or more custom-set dimensions (local, global, or a mix). Referenced in expressions via `{...}` — e.g. `X{segment}` or `X{segment, fuel}` for multiple sets. See [Custom Sets and Indexing](../mathematical-syntax.md#custom-sets-and-indexing-proposed).|

```yaml
parameters:
  - id: segment_capacity
    indexed-by: segment
    time-dependent: false
    scenario-dependent: false
variables:
  - id: segment_level
    indexed-by: segment
    lower-bound: 0
    upper-bound: segment_capacity{segment}
    variable-type: continuous
```

The same `indexed-by` field applies to `constraints`, `binding-constraints`,
`objective-contributions`, and `extra-outputs`, to force unfolding over a set even when none of the
constraint's own terms are set-indexed — see
[Indexing a constraint explicitly](../mathematical-syntax.md#indexing-a-constraint-explicitly-and-referencing-the-index-value-itself).

#### Ports

A list of ports that model exposes to connect with other models. Each port has:

| Element | Type | Description |
|------|------|--------------------------|
|`id`| String | Unique port name within the model. Must follow the [naming rules](#rules-for-id-naming).|
| `type`| String | The port type `id` that this port conforms to. Must match a port type defined in the [port-types](#port-types) collection of a library included in the system.|

The port `type` must be one of those defined in the [port-types](#port-types) collection of a library included in the system.

#### Port Field Definition

A collection of definitions describing the ports **emitted** by a model. Each entry associates one of the model’s variables, parameters, or linear expressions with a specific field of a port. When a model defines a port, it must provide definitions for all fields of that port.

| Element | Type | Description |
|------|------|--------------------------|
|`port`| String | The `id` of a port listed in the [ports section](#ports) of this model.|
| `field`| String | The field `id` as defined in the corresponding [port type](#port-types).|
|`definition`| [Mathematical Expression](../mathematical-syntax.md) | A linear expression giving the value of that port field, using the model’s variables and/or parameters.|

!!! warning "Design proposal — not yet implemented"
    If the port field declares `indexed-by` (see [Port Types](#port-types)), this `definition`'s
    expression must produce a value whose inferred indexing matches it exactly — see
    [Port fields and custom sets](../mathematical-syntax.md#port-fields-and-custom-sets). Not yet
    implemented in [GemsPy](../../index.md).

#### Constraints

A list of internal constraints of a model. These are equations or inequalities that involve the model’s own variables, parameters. Each constraint has:

| Element | Type | Description |
|------|------|--------------------------|
|`id`| String | Unique `id` for the constraint within the model. Must follow the [naming rules](#rules-for-id-naming).|
| `expression`| [Mathematical Expression](../mathematical-syntax.md#constraints) | An equation or inequality using the model’s variables and parameters.|

An explicit example is provided by the `storage` model constraint defining the initial reservoir level:

```yaml
constraints:
  - id: initial_level_constraint
    expression: level[0] = initial_level * reservoir_capacity
```

Constraint **expression** must comply with the [**Mathematical Expression Syntax**](../mathematical-syntax.md#constraints) to ensure it is interpreted correctly during model evaluation.

#### Binding-Constraints

A list of external constraints that involve model’s ports (i.e., constraints that will bind this model’s behavior to other models when connected).

| Element | Type | Description |
|------|------|--------------------------|
|`id`| String | Unique `id` for the binding constraint within the model. Must follow the [naming rules](#rules-for-id-naming).|
| `expression`| [Mathematical Expression](../mathematical-syntax.md#constraints) | An equation or inequality that may use [port operators](../mathematical-syntax.md#port-operator) to aggregate expressions from connected components.|

Binding constraints are defined in the same manner as internal constraints, but they may include [port operators](../mathematical-syntax.md#port-operator), which aggregate linear expressions emitted through a port.

!!! warning "Design proposal — not yet implemented"
    `sum_connections(port.field{s})` is well-defined for any custom set `s`, because a port field can
    only be `indexed-by` a [library-level (global) set](#library-level-sets) — every component
    connecting through that port type necessarily shares the exact same set, so no additional runtime
    guard is needed beyond that schema-level restriction. See
    [Port fields and custom sets](../mathematical-syntax.md#port-fields-and-custom-sets). Not yet
    implemented in [GemsPy](../../index.md).

An explicit example is provided by the `bus` model implementing the energy balance constraint (**First Kirchhoff Law**):

```yaml
binding-constraints:
  - id: balance
    expression: sum_connections(balance_port.flow) = spillage - unsupplied_energy
```


#### Objective Contribution

An `objective contribution` is a linear expression that represents a cost or penalty associated with a model component. During model assembly, all objective contributions defined across all instantiated components are **automatically aggregated** to form the **global objective function** of the optimisation problem. By convention, the optimisation problem is assumed to be a **minimisation** problem.

| Element | Type | Description |
|------|------|--------------------------|
|`id`| String | Unique `id` for the objective contribution within the model. Must follow the [naming rules](#rules-for-id-naming).|
| `expression`| [Mathematical Expression](../mathematical-syntax.md) | A linear expression representing a cost or penalty term. All contributions across all components are summed to form the global minimisation objective.|

```yaml
objective-contributions:
  - id: objective
    expression: sum(spillage_cost * spillage + unsupplied_energy_cost * unsupplied_energy)
```

Note that a model may define multiple objective contributions, each identified by its own `id`. This enables advanced formulations such as [two-stage stochastic](../theoretical-concepts/optimization-problem.md) optimisation, where different objective terms belong to different optimisation stages (e.g. investment vs. operation).

#### Extra Output

The `extra-outputs` section allows each model to define additional calculated outputs that are **evaluated after optimization**.

Each entry under `extra-outputs` must contain:

| Field | Type | Description |
|------|------|-----------------|
| `id` | String | Unique identifier for the extra output within the model. Must follow the [naming rules](#rules-for-id-naming). |
| `expression` | [Mathematical Expression](../mathematical-syntax.md) | A linear expression evaluated from optimal variable values after the solve. May use variables, parameters, and [direct port field access](../mathematical-syntax.md#direct-port-field-usage) (unlike constraints). |

Unlike in constraints, [direct port field usage](../mathematical-syntax.md#direct-port-field-usage) **is allowed** in `extra-outputs`.

#### Properties 

(Optional) If `properties` keys are declared in the model, the declaration of  such keys and their values are mandatory for the components that instantiate the model.

In the library file, each entry only declares the key name, they are specified by a value for each component within the [system file](../system#properties).

| Element | Type | Description |
|------|------|--------------------------|
| `id` | String | Unique property key name within the model. |

```yaml
models:
  - id: thermal
    properties:
      - id: carrier
      - id: company
```

#### Taxonomy

(Optional) A string that assigns the model to a category within a classification taxonomy. 

```yaml
  models:
    - id: generator
      taxonomy-category: production
```