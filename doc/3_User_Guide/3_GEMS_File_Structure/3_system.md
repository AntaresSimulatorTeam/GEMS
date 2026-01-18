<div style="display: flex; justify-content: space-between; align-items: center;">
  <div style="text-align: left;">
    <a href="../../../..">Main Section</a>
  </div>
  <div style="text-align: right;">
    <img src="../../../assets/gemsV2.png" alt="GEMS Logo" width="150"/>
  </div>
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

The `connections` section specifies how components are linked. In this case, the `balance_port` port of `load_1` is connected to the `balance_port` port of `bus_1`, indicating that the load is connected to the node

## Components

The system file describes the energy system to be simulated. Each component defined in the system represents a concrete instantiation of a model from one of the referenced libraries. For every component, the following fields are specified:

| Element | Description |
|------|--------------------------|
|`id`| Unique identifier for the component within this system.|
| `model` | Specifies which model this component instantiates The format is `library_id.model_id`.|
|`scenario-group`|The `id` of the scenario group this component belongs to. |
|`parameters`|Collection of values assigned to the model’s parameters. All parameters defined by the model must be assigned a value.|

For each parameter definition, the following fields must be provided:

| Element | Description |
|------|--------------------------|
| `id`| The `id` of the parameter, as defined by the model.|
| `time-dependent` | `true` or `false`, indicates whether the parameter depends on time or is constant across the whole simulation horizon. If the model parameter is not time-dependent, this can't be set to true.|
|`scenario-dependent`|`true` or `false`, indicates whether the parameter changes depending on the simulated scenario, or is the same for all scenarios. If the model parameter is not scenario-dependent, this can't be set to true. |
|`value`|Value assigned to the parameter.|

The `value` field is interpreted as follows:

- For `constant parameters`, a numeric value must be provided (data series `id's` are not allowed).

- For `time-dependent` parameters, the value must be the `id` of a time-dependent data series.

- For `scenario-dependent` parameters, the value must be the `id` of a scenario-dependent data series.

- For `time-and-scenario-dependent` parameters, the value must be the `id` of a data series that varies across both dimensions.

## Connections

A list of connections between component ports. Each connection entry defines a link between two components’ ports, allowing them to interact.

 Element | Description |
|------|--------------------------|
| `component1`| The `id` of the first component being connected.|
| `component2` | The `id` of the second component being connected.|
|`port1`| The port `id` on `component1`. |
|`port2`|The port `id` on `component2`.|

The two ports being connected must be of the same port type.

Port `connections` determine how linear expressions are exchanged between components. If a model defines a port only in the ports section, it acts as a **receiver** for that port and collects linear expressions emitted by connected components. A typical example is a **bus** model, which receives flow expressions from connected components (generators, load etc.).

If a model additionally defines **port-field-definitions**, it acts as an **emitter** for that port. In this case, the model exposes linear expressions through the port, allowing connected receiver component to consume them. A common example is a generator model, which emits it's `generation` variable to connected bus component.

**Navigation**

<div style="display: flex; justify-content: space-between;">
    <div style="text-align: left;">
    <button type="button" style="background-color:#CCCCCC; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
        <a href="../2_library" style="text-decoration:none; color: #000000">⬅️ Previous page</a>
    </button>
    </div>
    <button type="button" style="background-color:#AAAAFF; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
        <a href="../../../.." style="text-decoration:none; color: #FFFFFF">Home</a>
    </button>
    <div style="text-align: right;">
    <button type="button" style="background-color:#CCCCCC; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
        <a href="../4_data_series" style="text-decoration:none; color: #000000">Next page ➡️</a>
    </button>
    </div>
</div>

---

© GEMS (LICENSE)