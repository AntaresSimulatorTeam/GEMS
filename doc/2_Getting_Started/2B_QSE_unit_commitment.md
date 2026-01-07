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
This tutorial demonstrates a simple **unit commitment optimization**. Unit commitment determines the **optimal number of units generating power** from **one single generator** at each time period to meet demand at minimum cost.

The study folder is on the [GEMS Github repository](https://github.com/AntaresSimulatorTeam/GEMS/tree/main/resources/Documentation_Examples/QSE/QSE_2_Unit_Commitment).

### Files Structure

```
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

<details>
  <summary><strong>Unit Commitment example description in details</strong></summary>
  <p>
    The diagram above shows the connections between the main components:
  </p>
  <ul>
    <li><strong>1 Bus:</strong> Central node for power balance</li>
    <li><strong>1 Thermal cluster:</strong> 10 units of 3 MW each (30 MW total capacity)</li>
    <li><strong>1 Solar Plant</strong></li>
    <li><strong>1 Wind Plant</strong></li>
    <li><strong>1 Load:</strong> Variable demand (35-125 MW)</li>
  </ul>
  <p>
    <strong>Time Horizon:</strong> 1 week with hourly resolution (168 hours)
  </p>
</details>

## Running the GEMS study with Antares Modeler

1. Download [QSE_2_unit_commitment](https://github.com/AntaresSimulatorTeam/GEMS/tree/documentation/get_started_quick_examples/resources/Documentation_Examples/QSE/QSE_2_unit_commitment)
2. Copy [`basic_models_library.yml`](https://github.com/AntaresSimulatorTeam/GEMS/blob/f5c772ab6cbfd7d6de9861478a1d70a25edf339d/libraries/basic_models_library.yml) into the `QSE_2_unit_commitment/input/model-libraries/`
3. Get Antares Modeler installed through this [tutorial](../1_installation)
4. Locate **bin** folder
5. Open the terminal
6. Run these command lines :

```bash
# Windows
antares-modeler.exe <path-to-study>

# Linux
./antares-modeler <path-to-study>
```

The results will be available in the folder `<study_folder>/output`.

## Outputs

## Output Variables

This graph illustrates how the number of thermal units generating power changes over the simulation week, reflecting the **unit commitment** feature. At night, when solar generation is unavailable, more thermal units are solicited to meet demand. Around midday, increased solar output often reduces the need for thermal generation, resulting in fewer thermal units operating.

![nb units on profile](../assets/2_QSE2_UC_ts_units.png)

<details>
  <summary><strong>Key outputs variables in details</strong></summary>
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

### Library File

<details>
  <summary><strong>Details of the <code>antares_legacy_models.yml</code> Library File</strong></summary>
  <ul>
    <li><strong>bus:</strong> Central node with power balance constraint, spillage and unsupplied energy variables</li>
    <li><strong>load:</strong> Consumes power (negative flow into the bus)</li>
    <li><strong>thermal:</strong> Dispatchable thermal cluster with unit commitment logic (integer variables for units ON/starting/stopping)</li>
    <li><strong>renewable:</strong> Non-dispatchable generation for solar and wind plants</li>
  </ul>
</details>

### System File
<details>
  <summary><strong>Details of the <code>system.yml</code> File</strong></summary>
  <p>
    <strong>Bus:</strong>
  </p>
  <ul>
    <li><code>spillage_cost</code> = 1000 $/MWh</li>
    <li><code>unsupplied_energy_cost</code> = 10000 $/MWh</li>
  </ul>
  <p>
    <strong>Thermal Cluster (10 units of 1 MW):</strong>
  </p>
  <ul>
    <li>All thermal parameters (min/max power, costs, min up/down, number of units) are set directly in <code>system.yml</code>.</li>
  </ul>
  <p>
    <strong>Renewables:</strong>
  <ul>
    <li><strong>Solar:</strong> generation from <code>solar.csv</code> timeseries</li>
  </ul>
  <div>
    <img src="../../assets/2_QSE2_UC_ts_solar.png" alt="solar profile"/>
  </div>
  <ul>
    <li><strong>Wind:</strong> generation from <code>wind.csv</code> timeseries</li>
  </ul>
  <div>
    <img src="../../assets/2_QSE2_UC_ts_wind.png" alt="wind profile"/>
  </div>
    <strong>Load:</strong>
  </p>
  <ul>
    <li>Variable demand from <code>load.csv</code> timeseries</li>
  </ul>
  <p>
    <img src="../../assets/2_QSE2_UC_ts_load.png" alt="load profile"/>
  </p>
</details>

---

**Navigation**
<div style="display: flex; justify-content: space-between;">
  <div style="text-align: left;">
  <button type="button" style="background-color:#CCCCCC; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
    <a href="../2A_QSE_adequacy" style="text-decoration:none; color: #000000">⬅️ Previous: Adequacy</a>
  </button>
  </div>
  <button type="button" style="background-color:#AAAAFF; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
    <a href="../../../.." style="text-decoration:none; color: #FFFFFF">Index</a>
  </button>
  <div style="text-align: right;">
  <button type="button" style="background-color:#CCCCCC; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
    <a href="../4_QSE_Investment" style="text-decoration:none; color: #000000">Next: Investment ➡️</a>
  </button>
  </div>
</div>

---

© GEMS (LICENSE)
