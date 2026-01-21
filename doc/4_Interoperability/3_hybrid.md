<div style="display: flex; justify-content: space-between; align-items: center;">
  <div style="text-align: left;">
    <a href="../../../..">Main Section</a>
  </div>
  <div style="text-align: right;">
    <img src="../../../assets/gemsV2.png" alt="GEMS Logo" width="150"/>
  </div>
</div>


# Hybrid studies

This page aims to explain how to run a study made with Modeler part and Legacy part with Antares Simulator.

# Definition

To define a hybrid study, it's a solver study, with modeler files and directories in the input directory.    
The parameter.yml file from modeler studies is not needed (if it exists, it will be ignored). The solver parameters are used, since hybrid studies are conducted using antares-solver

```yaml
solver-study/
├── input/                    <-- Modeler files go here
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

A connection must be established between the GEMS component and the Legacy area on which the component refers to.

Connecting GEMS Generator component to Antares area user is adding variable generation to the area balance constraint of Antares area.

The following steps describe how to connect the modeler-study (GEMS framework) with the solver-study (Legacy framework):

### Define the connections (in the system.yml file)

The connection between GEMS component `generator1` and Legacy area `area1` needs to be defined through the **system.yml** file in the `area-connections` section :

```yaml
area-connections:
 - component: generator1  # the ID of the component to connect to the area, as defined in the components section
  port: injection        # the ID of the component's port to connect to the area. This port must be of a type that defines an area-connection injection field.
  area: area1            # the ID of the area to connect the component to, as defined in the antares-solver input files
 - component: generator2
   port: injection
   area: area1
```
### Define the area-connection fields (in the library.yml file)

As it mentions above, the port field needs to be defined in order to specify what data will be exchanged between the component and the area.

This area-connection field is defined inside the port type definition inside the library file:

```yaml 
port-type:
  id: ac_link
  fields:
    - id: flow
    - id: angle
  # area-connection is the name of the optional section to use.
  # It is mandatory if you want to use such a port type to connect modeler components to solver areas.
  area-connection:
    # injection-field: the field to use when adding the contribution of this port bearer to a connected area
    - injection-field: flow
```

## How to run a hybrid study

After following the [previous instructions](#how-to-connect-the-modeler-part-and-the-solver-part), the study is able to be run by Antares Simulator

# Example

This section presents a simple example of a hybrid study findable in the [resources folder](https://github.com/AntaresSimulatorTeam/GEMS/tree/main/resources/Documentation_Examples).

This example is depicted by the following scheme :

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

GEMS Time-Series size must be compliant with Antares Simulator optimization and simulation horizon.
If GEMS model introduce integer or binary variables, Antares Simulator must use MILP unit commitment mode.


---
**Navigation**
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