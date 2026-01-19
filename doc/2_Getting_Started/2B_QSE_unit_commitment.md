<div style="display: flex; justify-content: space-between; align-items: center;">
  <div style="text-align: left;">
    <a href="../../../..">Main Section</a>
  </div>
  <div style="text-align: right;">
    <img src="../../assets/gemsV2.png" alt="GEMS Logo" width="150"/>
  </div>
</div>

# QSE 2: Unit Commitment - Simple Example

## Overview

This tutorial demonstrates a simple example of a **unit commitment** problem stated with GEMS. Unit commitment involves determining the optimal number of dispatchable generating units at each time period in order to meet residual demand at the lowest possible cost. This example is intended to illustrate modelling concepts and should not be interpreted as representing a realistic system.

The study folder is on the [GEMS Github repository](https://github.com/AntaresSimulatorTeam/GEMS/tree/main/resources/Documentation_Examples/QSE/QSE_2_Unit_Commitment).

### Files Structure

The diagram below describe the file structure of the [study](https://github.com/AntaresSimulatorTeam/GEMS/tree/main/resources/Documentation_Examples/QSE/QSE_2_Unit_Commitment).

```text
QSE_2_Unit_Commitment/
├── input/
│   ├── system.yml
│   ├── model-libraries/
│   │   └── antares_legacy_models.yml
│   └── data-series/
│       ├── load.csv
│       ├── solar.csv
│       └── wind.csv
└── parameters.yml
```

### Problem Description

![QSE_2 system description diagram](../../assets/2_Scheme_QSE2_Unit_Com_System.png)

The *Unit Commitment* problem here involves determining the on/off scheme and dispatch of thermal units required to ensure adequate production and load balancing, given the intermittent nature of solar and wind generation. Modelling the thermal units takes into account dynamic constraints and non-proportional costs, such as start-up and fixed costs.

<details>
  <summary><strong>System Overview</strong></summary>

  <ul>
    <li>
      <strong>Bus</strong> (central node for power balance)
      <ul>
        <li><code>spillage_cost</code>: 1000 €/MWh</li>
        <li><code>unsupplied_energy_cost</code>: 10000 €/MWh</li>
      </ul>
    </li>
    <li>
      <strong>Thermal cluster</strong> (dispatchable)
      <ul>
        <li>10 units, each 10 MW (100 MW total capacity)</li>
        <li>All parameters (min/max power, costs, min up/down, number of units) are set in <code>system.yml</code></li>
      </ul>
    </li>
    <li>
      <strong>Solar plant</strong>
      <ul>
        <li>Generation profile from <code>solar.csv</code> timeseries :</li>
        <li><img src="../../assets/2_QSE2_UC_ts_solar.png" alt="solar profile"/></li>
      </ul>
    </li>
    <li>
      <strong>Wind plant</strong>
      <ul>
        <li>Generation profile from <code>wind.csv</code> timeseries :</li>
        <li><img src="../../assets/2_QSE2_UC_ts_wind.png" alt="wind profile"/></li>
      </ul>
    </li>
    <li>
      <strong>Load</strong>
      <ul>
        <li>Variable demand (35–125 MW) from <code>load.csv</code> timeseries :</li>
        <li><img src="../../assets/2_QSE2_UC_ts_load.png" alt="load profile"/></li>
      </ul>
    </li>
  </ul>
  <ul>
    <li><strong>Time Horizon:</strong> 1 week, hourly resolution (168 hours)</li>
    <li>The diagram above shows the connections between these components.</li>
  </ul>
</details>

## Running the GEMS study with Antares Modeler

Instructions to run this GEMS study with [Antares Simulator](https://github.com/AntaresSimulatorTeam/Antares_Simulator/releases) are available below.

<details>
  <summary><strong>Detailed steps for running GEMS study with Antares Modeler</strong></summary>
  <ol>
    <li>Download <a href="https://github.com/AntaresSimulatorTeam/GEMS/tree/documentation/get_started_quick_examples/resources/Documentation_Examples/QSE/QSE_2_unit_commitment">QSE_2_unit_commitment</a></li>
    <li>Copy <a href="https://github.com/AntaresSimulatorTeam/GEMS/blob/f5c772ab6cbfd7d6de9861478a1d70a25edf339d/libraries/antares_legacy_models.yml"><code>antares_legacy_models.yml</code></a> into the <code>QSE_2_unit_commitment/input/model-libraries/</code></li>
    <li>Get Antares Modeler installed through this <a href="../1_installation">tutorial</a></li>
    <li>Locate <strong>bin</strong> folder</li>
    <li>Open the terminal</li>
    <li>Run these command lines:
      <p><strong>Windows</strong></p>
      <pre><code>antares-modeler.exe &lt;path-to-study&gt;</code></pre>
      <p><strong>Linux</strong></p>
      <pre><code>./antares-modeler &lt;path-to-study&gt;</code></pre>
    </li>
  </ol>
  <p>The results will be available in the folder <code>&lt;study_folder&gt;/output</code>.</p>
</details>

## Outputs

This graph illustrates how the number of thermal units generating power changes over the simulation week, reflecting the **unit commitment** feature. At night, when solar generation is unavailable, more thermal units are solicited to meet demand. Around midday, increased solar output often reduces the need for thermal generation, resulting in fewer thermal units operating.

![nb units on profile](../../assets/2_QSE2_UC_ts_units.png)

Focus on the flows of all components:

![flows of all components](../../assets/2_QSE2_UC_outputs.png)

<details>
  <summary><strong>Key outputs variables in the Simulation Table</strong></summary>
  <p>
    The simulation outputs are saved in <code>output/simulation_table--&lt;timestamp&gt;.csv</code>. This table gives the key to understand the different output variables relevant to this example of unit commitment.
  </p>
  <table>
    <tr>
      <th>Variable</th>
      <th>Description</th>
    </tr>
    <tr>
      <td><code>thermal,nb_units_on</code></td>
      <td><strong>Number of units currently ON</strong> (0-10). This is the key output showing how many thermal units are committed at each hour.</td>
    </tr>
    <tr>
      <td><code>thermal,nb_starting</code></td>
      <td>Number of units starting up at this hour</td>
    </tr>
    <tr>
      <td><code>thermal,nb_stopping</code></td>
      <td>Number of units shutting down at this hour</td>
    </tr>
    <tr>
      <td><code>thermal,generation</code></td>
      <td>Total power output from the thermal cluster (MW)</td>
    </tr>
  </table>
</details>

## Further in-depth explanations

### Mathematical formulation

The mathematical modelling used for this study case is inspired from Antares Simulator legacy approach: [Antares Simulator documentation](https://xwiki.antares-simulator.org/xwiki/bin/view/Reference%20guide/4.%20Active%20windows/5.Optimization%20problem/).

### Library File

The library file [**antares_legacy_models.yml**](https://github.com/AntaresSimulatorTeam/GEMS/blob/main/libraries/antares_legacy_models.yml) defines the main component [models](../3_User_Guide/3_GEMS_File_Structure/2_library.md#models) used in this example:

- **bus**: Central node with power balance constraint, spillage, and unsupplied energy variables.
- **load**: Consumes power (negative flow into the bus).
- **thermal**: Dispatchable thermal cluster with unit commitment logic (integer variables for units ON/starting/stopping).
- **renewable**: Non-dispatchable generation for solar and wind plants.

### System File

The description of an energy system is the combination of a model library and a graph of components (instantiation of models) described in the system file. This part contains an extract of this **system file**.

<details>
  <summary><strong>Details of the <code>system.yml</code> File</strong></summary>

The next lines are an extract of the whole system file of this study:

```yaml
system:
  id: system
  components:
    - id: bus1
      model: antares_legacy_models.area

      parameters:
        - id: spillage_cost
          time-dependent: false
          scenario-dependent: false
          value: 1000
        - id: ens_cost
          time-dependent: false
          scenario-dependent: false
          value: 10000
          
    - id: load_bus
      model: antares_legacy_models.load

      parameters:
        - id: load
          time-dependent: true
          scenario-dependent: true
          value: load

    - id: gas_plant
      model: antares_legacy_models.thermal
      parameters:
        - id: p_min_unit
          time-dependent: false
          scenario-dependent: false
          value: 3
        - id: p_max_unit
          time-dependent: false
          scenario-dependent: false
          value: 10
        - id: generation_cost
          time-dependent: false
          scenario-dependent: false
          value: 30
        - id: startup_cost
          time-dependent: false
          scenario-dependent: false
          value: 1000
        - id: fixed_cost
          time-dependent: false
          scenario-dependent: false
          value: 100
        - id: d_min_up
          time-dependent: false
          scenario-dependent: false
          value: 12
        - id: d_min_down
          time-dependent: false
          scenario-dependent: false
          value: 12
        - id: p_min_cluster
          time-dependent: false
          scenario-dependent: false
          value: 0
        - id: p_max_cluster
          time-dependent: false
          scenario-dependent: false
          value: 100
        - id: nb_units_max
          time-dependent: false
          scenario-dependent: false
          value: 10
        - id: nb_units_min
          time-dependent: false
          scenario-dependent: false
          value: 0
        - id: nb_units_max_variation_forward
          time-dependent: false
          scenario-dependent: false
          value: 0
        - id: nb_units_max_variation_backward
          time-dependent: false
          scenario-dependent: false
          value: 0

    - id: solar_farm
      model: antares_legacy_models.renewable
      parameters:
        - id: nominal_capacity
          time-dependent: false
          scenario-dependent: false
          value: 50
        - id: unit_count
          time-dependent: false
          scenario-dependent: false
          value: 1
        - id: generation
          time-dependent: true
          scenario-dependent: true
          value: solar

    - id: wind_farm
      model: antares_legacy_models.renewable
      parameters:
        - id: nominal_capacity
          time-dependent: false
          scenario-dependent: false
          value: 35
        - id: unit_count
          time-dependent: false
          scenario-dependent: false
          value: 1
        - id: generation
          time-dependent: true
          scenario-dependent: true
          value: wind

  connections:

    - component1: bus1
      component2: load_bus
      port1: balance_port
      port2: balance_port
    - component1: bus1
      component2: gas_plant
      port1: balance_port
      port2: balance_port
    - component1: bus1
      component2: solar_farm
      port1: balance_port
      port2: balance_port
    - component1: bus1
      component2: wind_farm
      port1: balance_port
      port2: balance_port
```

</details>

---

**Navigation**
<div style="display: flex; justify-content: space-between;">
  <div style="text-align: left;">
  <button type="button" style="background-color:#CCCCCC; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
    <a href="../2A_QSE_adequacy_math_model" style="text-decoration:none; color: #000000">⬅️ Previous page</a>
  </button>
  </div>
  <button type="button" style="background-color:#AAAAFF; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
    <a href="../../../.." style="text-decoration:none; color: #FFFFFF">Home</a>
  </button>
  <div style="text-align: right;">
  <button type="button" style="background-color:#CCCCCC; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
    <a href="../../3_User_Guide/1_introduction" style="text-decoration:none; color: #000000">Next page ➡️</a>
  </button>
  </div>
</div>

---

© GEMS (LICENSE)
