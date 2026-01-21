<div style="display: flex; justify-content: space-between; align-items: center;">
  <div style="text-align: left;">
    <a href="../../../..">Main Section</a>
  </div>
  <div style="text-align: right;">
    <img src="../../../assets/gemsV2.png" alt="GEMS Logo" width="150"/>
  </div>
</div>


# Hybrid studies

This page explains how to configure and run a **hybrid study** that combines the Modeler part (GEMS components) with the Legacy part (standard Antares solver) in Antares Simulator. In a hybrid study, the GEMS modeler files are integrated into a solver study’s directory structure, allowing the Antares solver to incorporate custom model components defined by GEMS.

# Definition

A **hybrid study** is essentially a **solver-based Antares** study that includes **additional GEMS** modeler data in its input folder. It uses the regular Antares solver (antares-solver) to run the simulation, but the input directory contains GEMS-specific files (such as system.yml, model libraries, etc.) describing custom components. 
The usual *parameter.yml from a pure modeler study is not used in this mode* – if it exists, it will be ignored. Instead, the study relies on the standard solver configuration (the *study.antares* file and other solver parameters) for simulation settings. In summary, the hybrid study’s input directory merges the modeler files with the typical Antares files, and the Antares solver’s built-in GEMS interpreter handles the GEMS part during the simulation.

```yaml
solver-study/
```text
│   ├── areas/
│   ├── bindingconstraints/
│   ├── ...
│   ├── model-libraries/ # Modeler libraries folder
│   ├── system.yml       # Modeler system file
│   └── data-series/     # Modeler dataseries folder
├── layers/
├── logs/
├── output/
├── settings/
├── user/
├── Desktop.ini
├── Logs.log
└── study.antares
```

# Running a hybrid study

## How to connect the modeler part and the solver part

In a hybrid study, it is crucial to **connect each GEMS component to an appropriate Antares area** so that the component’s variables participate in the simulation. Establishing this connection ensures that, for example, a GEMS generator’s output is included in the power balance of a specific Antares area. 
In practical terms, connecting a GEMS Generator component to an Antares area injects the generator’s power output into that area’s balance equation (the supply-demand constraint). *Without this connection, the modeler component would remain isolated and not influence the solver’s optimization problem*. The following steps describe how to **link the modeler part to the solver part**:

### Define the connections (in the system.yml file)

The `area-connections` section of the **system.yml** is to declare each link between a GEMS component and a legacy Antares area. For every component that should supply or interact with an area, an entry adds specifying the component, the port through which it connects, and the target area name. The port must be one that supports area injection (we’ll ensure that in the library definition). For example, to connect a component `wind_farm` to a legacy area `area1` through `wind_farm`’s port named injection, the following configuration is used:

```yaml
area-connections:
 - component: wind_farm # the ID of the component to connect to the area, as defined in the components section
  port: balance_port # the ID of the component's port to connect to the area. This port must be of a type that defines an area-connection injection field.
  area: area1 # the ID of the area to connect the component to, as defined in the antares-solver input files
```

### Define the area-connection fields (in the library.yml file)

For a GEMS component’s port to successfully inject into an Antares area, the port’s type must declare which field represents the power injection. This is configured in the model library YAML (e.g., a **library.yml** in the *model-libraries* folder). Within the port type definition, an `area-connection` specifies an `injection-field`. The `injection-field` designates which field of that port will be added to the connected area’s balance equation. For example, considering a port type that carries power flow, it's defined in the library as follows:

```yaml 
  port-types:
    - id: flow
      description: A port that transfers a power flow.
      fields:
        - id: flow
  # area-connection is the name of the optional section to use.
  # It is mandatory to use such a port type to connect modeler components to solver areas.
  area-connection:
    # injection-field: the field to use when adding the contribution of this port bearer to a connected area
    - injection-field: flow
```

## How to run a hybrid study

After setting up the connections as described above, running a hybrid study is done in the same way as running a standard Antares simulation. The study can be opened or launched with Antares Simulator (using the GUI or the command-line solver). The presence of system.yml and modeler libraries in the input folder will trigger the Antares solver’s GEMS interpreter to load those components. The solver will then construct a combined optimization problem that includes both the legacy elements (areas, thermal plants, hydro, etc.) and the new GEMS modeler components defined by the user.

From the user’s perspective, the simulation is executed as usual (for example, by clicking Run in the Antares interface or using antares-solver on the study folder). The solver will read the hybrid study configuration and automatically integrate the modeler part. Once the run starts, it will simulate with the combined model. Results for the GEMS components (e.g., generation output of a custom component) will appear alongside the usual Antares results for areas, provided that output has been configured for those components (the GEMS framework will handle output storage in the study results).

# Example

This section presents a simple example of a hybrid study findable in the [resources folder](https://github.com/AntaresSimulatorTeam/GEMS/tree/main/resources/Documentation_Examples).

![Hybrid Study Scheme](../assets/4_hybrid_study_scheme.png)

<details>
<summary>Hybrid Study Example Details</summary>

<p>This consists of an area from Solver framework with a constant load of 1000 MW and a wind farm component made from the <em>renewable</em> <strong>model</strong> from the <a href="https://github.com/AntaresSimulatorTeam/GEMS/blob/main/libraries/basic_models_library.yml"><strong>basic-models-library</strong></a>.</p>

<p>Concerning the connection between the area and the renewable component, it's configured by these yaml files:</p>

<p><strong>library.yml :</strong></p>

<pre><code class="language-yaml">  port-types:
  - id: flow
    description: A port that transfers a power flow.
    fields:
    - id: flow
    area-connection:
    - injection-field: flow
...
  - id: renewable
    parameters:
    - id: generation
      time-dependent: true
      scenario-dependent: true
    ports:
    - id: balance_port
      type: flow
    port-field-definitions:
    - port: balance_port
      field: flow
      definition: generation
</code></pre>

<p><strong>system.yml :</strong></p>

<pre><code class="language-yaml">...
  area-connections:
  - component: wind_farm
    port: balance_port
    area: Area
</code></pre>

</details>

# Limitation

When constructing hybrid studies, the following important constraints should be considered:

Time Series Length: The time series data used in GEMS modeler components (for example, the generation profile of a renewable) must align with the Antares simulation horizon and resolution. In practice, this means the number of time steps and the granularity of GEMS time-dependent inputs should match the solver’s expectations (e.g., 8760 hourly values for a yearly hourly simulation). The hybrid solver will not accept a modeler time series that doesn’t fit the configured simulation timeframe.

Integer/Binary Decision Variables: If any GEMS component introduces integer or binary decision variables (for instance, a component that has an on/off state or unit commitment logic), Antares must be run in MILP mode. Antares Simulator’s solver has to be set to Mixed-Integer Linear Programming (the unit commitment MILP option) to handle discrete variables. In hybrid mode, the solver will incorporate those binary/integer variables into the optimization, but only if the MILP solver is enabled. If running with continuous (LP) mode while using components that require integer decisions, the simulation will not handle them correctly. Thus, the study’s optimization settings must be configured for MILP (unit commitment) when needed.

<div style="display: flex; justify-content: space-between;">
  <div style="text-align: left;">
  <button type="button" style="background-color:#CCCCCC; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
    <a href="../2_antares_legacy" style="text-decoration:none; color: #000000">⬅️ Previous page</a>
  </button>
  </div>
  <button type="button" style="background-color:#AAAAFF; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
    <a href="../../../.." style="text-decoration:none; color: #FFFFFF">Home</a>
  </button>
  <div style="text-align: right;">
  <button type="button" style="background-color:#CCCCCC; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
    <a href="../../5_Examples/1_optimization_problem" style="text-decoration:none; color: #000000">Next page ➡️</a>
  </button>
  </div>
</div>

---

© GEMS (LICENSE)