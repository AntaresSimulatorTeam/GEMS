---
description: Simple example of a GEMS hybrid study — a walkthrough of a minimal Antares Simulator study combining GEMS components with Antares Legacy areas.
tags:
  - Getting Started
  - Hybrid Studies
  - Interoperability
---

<div style="display: flex; justify-content: flex-end;">
  <a href="../..">
    <img src="../../../assets/gemsV2.png" alt="GEMS Logo" width="150"/>
  </a>
</div>

# Simple example of a [hybrid study](https://github.com/AntaresSimulatorTeam/GEMS/tree/main/resources/Documentation_Examples/Hybrid_Study)

This section represents a simple example of a hybrid study that demonstrates how to integrate GEMS models into Antares Simulator. The example can be found in the [resources folder](https://github.com/AntaresSimulatorTeam/GEMS/tree/main/resources/Documentation_Examples) and covers a one-week time horizon.

![Hybrid Study Scheme](../../assets/4_hybrid_study_scheme.png)

<details>
<summary>Hybrid Study Example Details</summary>

<p>This consists of an area from Solver framework with a constant demand of 60 MW throughout one week and a wind farm component made from the <em>renewable</em> <strong>model</strong> from the <a href="https://github.com/AntaresSimulatorTeam/GEMS/blob/main/libraries/basic_models_library.yml"><strong>basic-models-library</strong></a>.</p>

<p>Concerning the connection between the area and the renewable component, it's configured by these yaml files:</p>

<p><strong>library.yml :</strong></p>

<pre><code class="language-yaml">
library:
  id: example_library

  port-types:
    - id: flow_port
      description: A port that transfers a power flow.
      fields:
        - id: flow_field
      area-connection:
        injection-to-balance: flow_field
        spillage-bound:
        unsupplied-energy-bound:

  models:
    - id: renewable
      parameters:
        - id: generation
          time-dependent: true
          scenario-dependent: true
      ports:
        - id: balance_port
          type: flow_port
      port-field-definitions:
        - port: balance_port
          field: flow_field
          definition: generation
</code></pre>

<p><strong>system.yml :</strong></p>

<pre><code class="language-yaml">
system:
  id: system

  components:
    - id: wind_farm
      model: example_library.renewable
      parameters:
        - id: generation
          time-dependent: true
          scenario-dependent: true
          value: wind

  area-connections:
    - component: wind_farm
      port: balance_port
      area: Area
</code></pre>

</details>

Since the wind farm does not produce enough energy to fully cover the demand, the results include **Energy Not Served (ENS)**.

This example is intended solely to demonstrate how the **GEMS component**, when connected to an **Antares Simulator area**, emits a linear expression that is incorporated into the area's balance constraint.

In this specific case, wind generation during the first hour is 20MW and demand is 60MW. As a result, the Antares area reports an ENS of 40MW, which is consistent with the balance shown in the simulation results.
