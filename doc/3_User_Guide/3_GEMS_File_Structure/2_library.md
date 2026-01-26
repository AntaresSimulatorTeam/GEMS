<div style="display: flex; justify-content: space-between; align-items: center;">
  <div style="text-align: left;">
    <a href="../../../..">Main Section</a>
  </div>
  <div style="text-align: right;">
    <img src="../../../assets/gemsV2.png" alt="GEMS Logo" width="150"/>
  </div>
</div>

# Library File

A library file defines a library of two collections of abstract objects:

- [Models](#models) - Contains the mathematical formulation for component type
- [Ports Types](#port-types) - Describe the kinds of connections models can have

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

The equation `sum_connections(injection.flow) = 0` follows the GEMS [**Mathematical Expression Syntax**](../2_mathematical_syntax.md#ports).

## Rules for id naming

All `id's` in the model library and system file must respect the following:

- Alphanumeric characters are allowed, as well as the underscore _ character
- All other characters are prohibited
- Only lower-case is allowed

## Collections and key fields in library file

Every library file must begin with the following header with optional `description`:

```yaml
library:
  id: example_library
  description: "Example model library"
```

| Element | Description |
|------|--------------------------|
| `id`| A unique identifier for the library. This `id` is used by system files to reference models from this library. It must be unique across all libraries that are used to build a system and must follow standard [naming rules](#rules-for-id-naming).|
| `description` | *(Optional)* A human-readable description of the library’s content or purpose.|

### Port Types

The `port-types` collection defines the set of port types available within a library. These port types can be used by models/components to communicate with each other by exchanging linear expressions.

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

| Element | Description |
|------|--------------------------|
|`port-types`| A list of port types definitions that models can use for connecting to other models.|
| `id`| Unique `id` for the port type within this library (must follow the naming rules and not conflict with other port type `id's` in the same library).|
| `description` | *(Optional)* A human-readable description of the library’s content or purpose.|
|`fields`| A list of fields carried by this port. Each field has an `id` (unique within the port type) that identifies a quantity carried by the port (e.g. a field might be power flow). A field holds a single floating number.|

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

| Element | Description |
|------|--------------------------|
|`id`| A unique identifier for the model within a library. It must follow standard [naming rules](#rules-for-id-naming). System files reference the model by combining the library `id` and the model `id`.|
| `description`| *(Optional)* Text description of the model.|

#### Parameters

A list of parameters that this model takes. Each parameter defines a configurable value for the model when it’s used in a system. For each parameter user can specify specify:

| Element | Description |
|------|--------------------------|
|`id`| Unique parameter identifier within the model. It must follow standard [naming rules](#rules-for-id-naming).|
| `time-dependent`| `true` or `false`. If `true`, this parameter can vary over the simulation timeline (meaning it will be associated with a time series input). If `false`, it’s treated as constant in time.|
|`scenario-dependent`|`true` or `false`. If `true`, the parameter can have different values in different scenarios (i.e., it requires scenario-specific data). If `false`, it does not vary between scenarios.|

Together, these flags define how the parameter can be provided — as a single value, a time series, scenario-based data, or a matrix. For details on how parameter data is stored and referenced, see the [data-series](./4_data_series.md).

#### Variables

A list of decision variables introduced by this model for the optimization problem. Each variable includes:

| Element | Description |
|------|--------------------------|
|`id`| Unique variable name within the model. It must follow standard [naming rules](#rules-for-id-naming).|
| `variable-type`| The type of variable: `continuous`, `integer`, or `binary`. This influences how the solver treats the variable (`continuous` vs. `integer programming`).|
|`lower-bound`|*(Optional)* A mathematical expression for the variable’s lower bound (if not provided, defaults to -∞ for continuous/integer, or 0 for binary).|
|`upper-bound`|*(Optional)* A mathematical expression for the variable’s upper bound (if not provided, defaults to +∞ for continuous/integer, or 1 for binary).|

Any expression used for bounds must use only constants or models parameters.

For example, variable `p_injection` in the `storage` model is defined as a continuous variable with upper bound set up by parameters `injection_nominal_capacity` and lower bound set up by 0.

```yaml
variables:
  - id: p_injection
    lower-bound: 0
    upper-bound: injection_nominal_capacity
    variable-type: continuous
```

#### Ports

A list of ports that model exposes to connect with other models. Each port has:

| Element | Description |
|------|--------------------------|
|`id`| Unique port name within the model. It must follow standard [naming rules](#rules-for-id-naming).|
| `type`| The port type (by `id`) that this port conforms to.|

The port `type` must be one of those defined in the [port-types](#port-types) collection of a library included in the system.

#### Port Field Definition

A collection of definitions describing the ports **emitted** by a model. Each entry associates one of the model’s variables, parameters, or linear expressions with a specific field of a port. When a model defines a port, it must provide definitions for all fields of that port.

| Element | Description |
|------|--------------------------|
|`port`| The `id` of a port (as listed in the [ports section](#ports) of this model).|
| `field`| The field `id` (as defined in the [port types](#port-types)) that is intended to be defined for this port.|
|`definition`| An expression for the value of that field, using the model’s variables/parameters.|

#### Constraints

A list of internal constraints of a model. These are equations or inequalities that involve the model’s own variables, parameters. Each constraint has:

| Element | Description |
|------|--------------------------|
|`id`| Unique `id` for the constraint within the model. It must follow standard [naming rules](#rules-for-id-naming).|
| `expression`| A mathematical expression representing the constraint.|

An explicit example is provided by the `storage` model constraint defining the initial reservoir level:

```yaml
constraints:
  - id: initial_level_constraint
    expression: level[0] = initial_level * reservoir_capacity
```

Constraint **expression** must comply with the [**Mathematical Expression Syntax**](../2_mathematical_syntax.md#constraints) to ensure it is interpreted correctly during model evaluation.

#### Binding-Constraints

A list of external constraints that involve model’s ports (i.e., constraints that will bind this model’s behavior to other models when connected).

| Element | Description |
|------|--------------------------|
|`id`| Unique `id` for the constraint within the model. It must follow standard [naming rules](#rules-for-id-naming).|
| `expression`| A mathematical expression representing the constraint.|

Binding constraints are defined in the same manner as internal constraints, but they may include [port operators](../2_mathematical_syntax.md#port-operator), which aggregate linear expressions emitted through a port.

An explicit example is provided by the `bus` model implementing the energy balance constraint (**First Kirchhoff Law**):

```yaml
binding-constraints:
  - id: balance
    expression: sum_connections(balance_port.flow) = spillage - unsupplied_energy
```

A detailed, step-by-step illustration of how binding constraints are constructed from ports and port-field definitions is provided in [Hypergraph Structure](../4_Theoretical_Concepts/1_hypergraph_structure.md) section.

#### Objective Contribution

An `objective contribution` is a linear expression that represents a cost or penalty associated with a model component. During model assembly, all objective contributions defined across all instantiated components are **automatically aggregated** to form the **global objective function** of the optimisation problem. By convention, the optimisation problem is assumed to be a **minimisation** problem.

| Element | Description |
|------|--------------------------|
|`id`| Unique `id` for the constraint within the model. It must follow standard [naming rules](#rules-for-id-naming).|
| `expression`| A mathematical expression representing the constraint.|

```yaml
objective-contributions:
  - id: objective
    expression: sum(spillage_cost * spillage + unsupplied_energy_cost * unsupplied_energy)
```

Note that a model may define multiple objective contributions, each identified by its own `id`. This enables advanced formulations such as [two-stage stochastic](../4_Theoretical_Concepts/2_optimization_problem.md) optimisation, where different objective terms belong to different optimisation stages (e.g. investment vs. operation).

#### Extra Output

The `extra-outputs` section allows each model to define additional calculated outputs that are **evaluated after optimization**.

Each entry under `extra-outputs` must contain:

| Field | Description |
|--------------|-----------------|
| `id` | Unique identifier for the extra output within the model. Must follow standard ID rules (lowercase, alphanumeric, underscores). |
| `expression` | A mathematical expression computed after optimization. Can use variables, parameters, and port fields. Must be linear and evaluable from optimal values. |

Unlike in constraints, [direct port field usage](../2_mathematical_syntax.md#direct-port-field-usage) **is allowed** in `extra-outputs`.

**Navigation**

<div style="display: flex; justify-content: space-between;">
    <div style="text-align: left;">
    <button type="button" style="background-color:#CCCCCC; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
        <a href="../1_overview" style="text-decoration:none; color: #000000">⬅️ Previous page</a>
    </button>
    </div>
    <button type="button" style="background-color:#AAAAFF; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
        <a href="../../../.." style="text-decoration:none; color: #FFFFFF">Home</a>
    </button>
    <div style="text-align: right;">
    <button type="button" style="background-color:#CCCCCC; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
        <a href="../3_system" style="text-decoration:none; color: #000000">Next page ➡️</a>
    </button>
    </div>
</div>

---

