<div style="display: flex; justify-content: flex-end;">
  <a href="../../../..">
    <img src="../../../assets/gemsV2.png" alt="GEMS Logo" width="150"/>
  </a>
</div>

# System File

The **system file** defines the concrete energy system to be simulated. It instantiates components from models provided by the libraries, assigns parameter values, and specifies how components are connected to each other. In practice, the system file answers questions such as which components are included, how they are linked, what parameter values they use (fixed, time-dependent, or scenario-dependent), and which model libraries are required. It acts as the central configuration that brings together models, data, and connections for a simulation run.

The system file is a YAML file with a single root key `system`. The system contains fields for an `id`, `description`, a list of `model-libraries` to use, the list of `components` in the system, and the list of `connections` definitions between components. Every system file must have exactly one top-level `system` entry containing these sections. Below is an example snippet of a system file:

```yaml
system:
  id: my_system
  description: "An example system with one load and one node"
  model-libraries: my_library_1, my_library_2
  components:
    - id: load_1
      model: my_library_1.load
      scenario-group: load_group
      parameters:
        - id: load
          time-dependent: true
          scenario-dependent: false
          value: demand_profile
    - id: bus_1
      model: my_library_2.bus
  connections:
    - component1: bus_1
      component2: load_1
      port1: balance_port
      port2: balance_port
```

In this example, the system file defines a system with two model libraries, `my_library_1` and `my_library_2`. These libraries provide the model definitions used to instantiate the system components.

The system `my_system` instantiates two components: `load_1`, which is an instance of the `load` model defined in `my_library_1`, and `bus_1`, which is an instance of the `bus` model defined in `my_library_2`. The `load_1` component assigns a time-dependent parameter `load`, whose value is provided by the data series identified as `demand_profile`.

The `connections` section specifies how components are linked. In this case, the `balance_port` port of `load_1` is connected to the `balance_port` port of `bus_1`, indicating that the load is connected to the node.

The top-level fields of a system file are:

| Element | Type | Description |
|------|------|--------------------------|
| `id` | String | A unique identifier for the system. Must follow the [naming rules](library.md#rules-for-id-naming).|
| `description` | String | *(Optional)* A human-readable description of the system.|
| `model-libraries` | String | *(Optional)* Comma-separated list of library IDs whose models are used in this system (e.g. `my_library_1, my_library_2`). Must match the `id` fields of the library files available to the simulation.|
| `components` | List | The list of component instantiations in the system.|
| `connections` | List | The list of port connections between components.|

## Components

The system file describes the energy system to be simulated. Each component defined in the system represents a concrete instantiation of a model from one of the referenced libraries. For every component, the following fields are specified:

| Element | Type | Description |
|------|------|--------------------------|
|`id`| String | Unique identifier for the component within this system. Must follow the [naming rules](library.md#rules-for-id-naming).|
| `model` | String | Specifies which model this component instantiates. The format is `library_id.model_id`.|
|`scenario-group`| String | *(Optional)* The `id` of the scenario group this component belongs to. Used to map Monte Carlo scenarios to data series columns via the [scenario builder](scenario-builder.md).|
|`parameters`| List | *(Optional)* Collection of values assigned to the model’s parameters. All parameters defined by the model must be assigned a value.|

### Parameters

For each parameter definition, the following fields must be provided:

| Element | Type | Description |
|------|------|--------------------------|
| `id`| String | The `id` of the parameter, as defined by the model.|
| `time-dependent` | Boolean | `true` or `false`. Indicates whether the parameter varies over time. Cannot be set to `true` if the corresponding model parameter is not declared time-dependent.|
|`scenario-dependent`| Boolean | `true` or `false`. Indicates whether the parameter changes across scenarios. Cannot be set to `true` if the corresponding model parameter is not declared scenario-dependent.|
|`value`| Number or String | Value assigned to the parameter (see below).|

For each parameter, the `value` field should be defined as follows:

- If `time-dependent: false` and `scenario-dependent: false`, the numerical value of the parameter (`float` or `integer`).

- Otherwise (when at least one of `time-dependent` or `scenario-dependent` is `true`), the `id` of a data series stored in the `data-series` directory. See [data series](./data-series.md) for file format details.

## Connections

A list of connections between component ports. Each connection entry defines a link between two components’ ports, allowing them to interact.

|Element | Type | Description |
|------|------|--------------------------|
| `component1`| String | The `id` of the first component being connected.|
| `component2` | String | The `id` of the second component being connected.|
|`port1`| String | The port `id` on `component1`.|
|`port2`| String | The port `id` on `component2`.|

The two ports being connected must be of the same port type.

Port `connections` determine how linear expressions are exchanged between components. If a model defines a port only in the ports section, it acts as a **receiver** for that port and collects linear expressions emitted by connected components. A typical example is a **bus** model, which receives flow expressions from connected components (generators, load etc.).

If a model additionally defines **port-field-definitions**, it acts as an **emitter** for that port. In this case, the model exposes linear expressions through the port, allowing connected receiver component to consume them. A common example is a generator model, which emits it's `generation` variable to connected bus component.

## Properties 

(Optional) These `properties` add extra-information for users linked to components not used by the solver.

```yaml
system:
  components:
    - id: nuclear_1
      model: basic.generator
      properties:
        - id: technology
          value: nuclear
        - id: company
          value: frenchpower
```