<div style="display: flex; justify-content: space-between; align-items: center;">
  <div style="text-align: left;">
    <a href="../../../..">Main Section</a>
  </div>
  <div style="text-align: right;">
    <img src="../../assets/gemsV2.png" alt="GEMS Logo" width="150"/>
  </div>
</div>


# Quick-start example 1: three-bus adequacy system

## Overview and problem description
This tutorial demonstrates resource adequacy modeling using a simplified three-bus meshed network over a single time-step. The example is intended solely to illustrate modeling concepts and should not be interpreted as a realistic system representation; however, it provides a foundation for developing more detailed and realistic models.

The study folder is on the [GEMS Github repository](https://github.com/AntaresSimulatorTeam/GEMS/tree/documentation/get_started_quick_examples/resources/Documentation_Examples/QSE/QSE_1_Adequacy).

### Adequacy definition

**Resource Adequacy** is the ability of the electric grid to satisfy the end-user power demand at all times. The main challenge is to get the balance between the electric **Production** (generator, storage) and **Consumption** (load, spillage) while respecting the **limitations of the grid**.

![Adequacy Scheme](../assets/2_adequacy_scheme.png)

### Problem Description

Network Topology: Triangle connecting Buses 1, 2, and 3 :

![QSE_Adequacy scheme](../assets/2_QSE_Adequacy_scheme.png)

<details>
<summary>Problems description in details</summary>

Time Horizon: This example considers a single one-hour time step.

Network Components:
<ul>
  <li>3 Buses (Regions 1, 2, 3 forming a triangle)</li>
  <li>3 Links (connecting each pair of regions)</li>
  <li>3 Generators (different capacities and costs)</li>
  <li>3 Loads (fixed demands)</li>
</ul>

In this example, the power flows on the links are constrained only by thermal capacities.

Generation:
<ul>
  <li><code>Generator 1</code> (Bus 1): 70-100 MW capacity, 35 €/MWh cost</li>
  <li><code>Generator 2</code> (Bus 2): 50-90 MW capacity, 25 €/MWh cost</li>
  <li><code>Generator 3</code> (Bus 3): 50-200 MW capacity, 42 €/MWh cost</li>
</ul>

Demand:
<ul>
  <li>Bus 1: 50 MW</li>
  <li>Bus 2: 40 MW</li>
  <li>Bus 3: 150 MW</li>
  <li>Total Load: 240 MW</li>
</ul>

Transmission Capacities:
<ul>
  <li>Link 1-2: 40 MW (bidirectional)</li>
  <li>Link 2-3: 30 MW (bidirectional)</li>
  <li>Link 3-1: 50 MW (bidirectional)</li>
</ul>

Economic Parameters:
<ul>
  <li>Spillage cost: 1000 €/MWh (penalty for wasted energy)</li>
  <li>Unsupplied energy cost: 10000 €/MWh (high penalty for unmet demand)</li>
</ul>
</details>



## The GEMS study

### Files Structure

Following block represents GEMS Framework study folder structure.
```
QSE_1_adequacy/
├── input/
│   ├──model-libraries/
│   │  ├── basic_models_library.yml
│   │  └── ...
│   ├── system.yml
│   └── data-series/
│       └──  ...
└── parameters.yml
```
The example study makes use of models provided by the [GEMS library](https://github.com/AntaresSimulatorTeam/GEMS/tree/f5c772ab6cbfd7d6de9861478a1d70a25edf339d/libraries). For maintainability reasons, the library is stored separately in the repository and is not included directly in the example study. Consequently, users must copy the [`basic_models_library.yml`](https://github.com/AntaresSimulatorTeam/GEMS/blob/f5c772ab6cbfd7d6de9861478a1d70a25edf339d/libraries/basic_models_library.yml) file into the example study directory (`QSE_1_adequacy/input/model-libraries/`) prior to execution.

Since this example performs the simulation over a single time step, the data-series folder does not contain any time-series data.

Simulation options can be configured in the `parameters.yml` file. For more details on available simulation options, refer to the following [link](https://github.com/AntaresSimulatorTeam/Antares_Simulator/blob/develop/docs/user-guide/modeler/04-parameters.md).

### Models Library

System of the **Three-bus Adequacy** example rely on models defined in the GEMS library file [`basic_models_library.yml`](https://github.com/AntaresSimulatorTeam/GEMS/blob/f5c772ab6cbfd7d6de9861478a1d70a25edf339d/libraries/basic_models_library.yml). These models encode the decision variables, objective-function contributions, and constraints that collectively form the optimization problem.

The complete mathematical formulation corresponding to this example — including decision variables, parameters, objective function, and constraints — is detailed in the following document:

[**Mathematical representation of the Three-bus Adequacy problem**](3_QSE_adequacy_math_model.md)

### System file and Optimization Graph

Following diagrams represents part of the `system.yml` where user is able to instantiate components (buses, links, generators etc.) and connect them via ports into the optimization graph.

Instantiation of components `bus_1`, `bus_load_1`, `generator_1` and `link_12` is represented as well as connection between `bus_1` and `bus_load_1` components and connection between `bus_1` and `link_12` components. Entire system file can be found [in this repo](https://github.com/AntaresSimulatorTeam/GEMS/blob/15b4821113a09a417b73d00b3bc24f819ef44c99/doc/5_Examples/QSE/QSE_1_Adequacy/input/system.yml).

![system yaml file explanations](../assets/2_QSE_Adequacy_system_only_one.png)

<details>
<summary>System file description</summary>
<p>
  <img src="../../assets/2_QSE_Adequacy_system.png" alt="system yaml file explanations" style="max-width:100%;">
</p>
<p>
  Based on the connection via components from <code>connections</code> section in the <code>system.yml</code> file, the optimization graph can be built. The following graph represents the optimization graph of the Three-bus Adequacy example.
</p>
<p>
  <img src="../../assets/2_QSE_1_system_complete.png" alt="complete diagram with ports" style="max-width:100%;">
</p>
</details>


## Running the GEMS study with Antares Modeler

1. Download [QSE_1_Adequacy](https://github.com/AntaresSimulatorTeam/GEMS/tree/documentation/get_started_quick_examples/resources/Documentation_Examples/QSE/QSE_1_Adequacy)
2. Copy [`basic_models_library.yml`](https://github.com/AntaresSimulatorTeam/GEMS/blob/f5c772ab6cbfd7d6de9861478a1d70a25edf339d/libraries/basic_models_library.yml) into the `QSE_1_adequacy/input/model-libraries/`
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

## Outputs

The results are available in the csv file `QSE_1_Adequacy/output/simulation_table--YYYYMMDD-HHMM.csv`

The simulation outputs contain the optimized value of optimization problem variables, the status of all contraints and bounds, as well as user defined extra output, as described on the [following page](../3_User_Guide/4_outputs.md).

The power flows between buses can be visualized as follows:

![outputs diagram](../../assets/2_QSE_1_out_scheme.png)

<details class="more-details">
  <summary><strong>Description of the problem in details </strong></summary>

By utilizing the extra output feature, the marginal price is obtained as the dual value of the power balance constraint at each bus:

<ul>
  <li>
    <code>bus_1</code>: 35 €/MWh, based on the generation cost of <code>generator_1</code>.
  </li>
  <li>
    <code>bus_2</code>: 35 €/MWh, since <code>generator_2</code> is operating at its maximum capacity. The next increment of 1 MWh is therefore produced by <code>generator_1</code>.
  </li>
  <li>
    <code>bus_3</code>: 42 €/MWh, based on the generation cost of <code>generator_3</code>.
  </li>
</ul>


The following graphs show the merit order of the generator and links flows :

<div style="display: flex; justify-content: center; gap: 32px; align-items: flex-start;">
  <figure style="width:45%; margin:0;">
    <img src="../../assets/2_QSE_1_out_Generator.png" alt="Outputs Generators" style="width:100%;"/>
    <figcaption style="text-align:center; margin-top:8px;">
      This graph shows the power output of each generator in the system, illustrating how the optimizer allocates generation based on cost and capacity constraints.
    </figcaption>
  </figure>
  <figure style="width:45%; margin:0;">
    <img src="../../assets/2_QSE_1_out_Links.png" alt="Outputs Flows" style="width:100%;"/>
    <figcaption style="text-align:center; margin-top:8px;">
      Above the blue absciss axis, the flow represents import, below it's export.
    </figcaption>
  </figure>
</div>

</details>

---
**Navigation**
<div style="display: flex; justify-content: space-between;">
  <div style="text-align: left;">
  <button type="button" style="background-color:#CCCCCC; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
    <a href="../1_installation" style="text-decoration:none; color: #000000">⬅️ Previous page</a>
  </button>
  </div>
  <button type="button" style="background-color:#AAAAFF; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
    <a href="../../../.." style="text-decoration:none; color: #FFFFFF">Index</a>
  </button>
  <div style="text-align: right;">
  <button type="button" style="background-color:#CCCCCC; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
    <a href="../3_QSE_Unit_Commitment" style="text-decoration:none; color: #000000">Next page ➡️</a>
  </button>
  </div>
</div>

---

© GEMS (LICENSE) 