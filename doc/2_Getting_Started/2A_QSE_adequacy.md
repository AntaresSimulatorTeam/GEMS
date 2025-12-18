<div style="display: flex; justify-content: space-between; align-items: center;">
  <div style="text-align: left;">
    <a href="../../../..">Main Section</a>
  </div>
  <div style="text-align: right;">
    <img src="../assets/gemsV2.png" alt="GEMS Logo" width="150"/>
  </div>
</div>


# QSE 1 : Three-Bus Adequacy System

## Overview
This tutorial demonstrates adequacy modeling in a meshed three-bus network.

The study folder is on the [GEMS Github repository](https://github.com/AntaresSimulatorTeam/GEMS/tree/f5c772ab6cbfd7d6de9861478a1d70a25edf339d/doc/5_Examples/QSE/QSE_1_Adequacy).

### Adequacy definition

**Adequacy** is the ability of the electric grid to satisfy the end-user power demand at all times. The main challenge is to get the balance between the electric **Production** (generator, storage) and **Consumption** (load, spillage) while respecting the **limitations of the grid**.

![Adequacy Scheme](../assets/2_adequacy_scheme.png)

## Files Structure
```
tutorial_QSE_adequacy/
├── input/
│   ├── library.yml
│   ├── system.yml
│   └── data-series/
│       └──  ...
└── parameters.yml
```
## Problem Description

### Network
**Components:**

- 3 Buses (Regions 1, 2, 3 forming a triangle)
- 3 Links (connecting each pair of regions)
- 3 Generators (different capacities and costs)
- 3 Loads (fixed demands)

**Time Horizon:** 1 hour is used for this example

![QSE_Adequacy scheme](../assets/2_QSE_Adequacy_scheme.png)

In this example, the `power flows` on the links are only constrained by thermal capacities.

# Mathematical representation

This part presents the mathematical representations of the problem. The notations mainly come from the [Wiki - Antares Simulator](https://xwiki.antares-simulator.org/xwiki/bin/view/Reference%20guide/4.%20Active%20windows/5.Optimization%20problem/).

## Glossary of Mathematical Symbols

### General notation

| Symbol | Description |
|--------|-------------|
| $L$ | Set of transmission links (edges of the power system graph) |
| $B$ | Set of buses, ordered set |
| $G_b$ | Set of generators installed at bus $b$ |
| $L_b^+$ | Set of links for which $b$ is the upstream vertex |
| $L_b^-$ | Set of links for which $b$ is the downstream vertex |

### Decision Variables

| Symbol | Description | Unit |
|--------|-------------|------|
| $F_l$ | Net power flow through link $l$ | MW |
| $F_l^+$ | Power flow through link $l$, from upstream to downstream | MW |
| $F_l^-$ | Power flow through link $l$, from downstream to upstream | MW |
| $P_g$ | Power output from generator $g$ | MW |
| $U_b$ | Unsupplied power at bus $b$ (in nominal state) | MW |
| $S_b$ | Spilled power at bus $b$ (in nominal state) | MW |
| $x_l$ | Transmission capacity investment level for link $l$ (binary) | - |

### Parameters

| Symbol | Description | Unit |
|--------|-------------|------|
| $\Omega_{\text{dispatch}}$ | Total dispatch cost | \$ |
| $\Omega_{\text{transmission}}$ | Transmission cost component | \$ |
| $\Omega_{\text{generator}}$ | Thermal generation cost component | \$ |
| $\Omega_{\text{unsupplied}}$ | Unsupplied energy cost component | \$ |
| $\Omega_{\text{spillage}}$ | Spillage cost component | \$ |
| $\overline{C_l^+}$ | Maximum transmission capacity (upstream to downstream) | MW |
| $\overline{C_l^-}$ | Maximum transmission capacity (downstream to upstream) | MW |
| $\underline{P}_g$ | Minimum power output from generator $g$ | MW |
| $\overline{P}_g$ | Maximum power output from generator $g$ | MW |
| $\chi_g$ | Output cost from generator $g$ | \$/MWh |
| $\delta_b^+$ | Normative unsupplied energy cost at bus $b$ (value of lost load) | \$/MWh |
| $\delta_b^-$ | Normative spilled energy cost at bus $b$ (value of wasted energy) | \$/MWh |
| $D_b$ | Net power demand at bus $b$ | MW |

## Optimization Problem

The objective function to minimize the total dispatch cost for the three-bus system is:

$$
\min(\Omega_{\text{dispatch}})
$$

where $\Omega_{\text{dispatch}}$ is composed of the following cost components:

$$
\Omega_{\text{dispatch}} = \Omega_{\text{generator}} + \Omega_{\text{unsupplied}} + \Omega_{\text{spillage}}
$$

## Objective function for each component

### Thermal Generation Cost

For the generators in the system:

$$
\Omega_{\text{generator}} = \sum_{b \in B} \sum_{g \in G_b}   \chi_{g} \cdot P_{g} 
$$

### Unsupplied Energy Cost

For the three buses in the system:

$$
\Omega_{\text{unsupplied}} = \sum_{b \in B} \delta_{b}^+ \cdot U_{b} 
$$

where $U_b$ represents unsupplied energy at bus $b$.

### Spillage Cost

For the three buses in the system:

$$
\Omega_{\text{spillage}} = \sum_{b \in B} \delta_{b}^- \cdot S_{b} 
$$

where $S_b$ represents spilled energy at bus $b$.

## Balance Constraints

### First Kirchhoff's Law (Power Balance):

$$
\forall b \in B, \sum_{g \in G_b} P_g - D_b + \sum_{l \in L_b^+} F_l - \sum_{l \in L_b^-} F_l = S_b - U_b
$$

## Flow Capacity Constraints

### Flow Definition Constraint:

$$
\forall l \in L, \quad F_l = F_l^+ - F_l^-
$$

## Thermal Units
### Power Output Constraints

Power output is bounded by must-run commitments and power availability:

$$
\forall b \in B, \forall g \in G_b, \quad \underline{P}_g \leq P_g \leq \overline{P}_g
$$

# GEMS Representation

In following sections it will be represented how mathematical model is translated, how user can instantiate components from models and how optimization graph is been built into the GEMS Framework specific files.

## Library File

This section shows how mathematical model is implemented for every power system element that figures in optimization problem. File in which models are defined is called `library file`. **TODO: create a link to the library file docs file, we don't still have it, create it in different PR**

![YAML Block description with mathematical equations](../assets/2_QSE_Adequacy_maths.png)

## System File

### Overview

- Creation of `system.yml` file

This system models a three-bus network with the following characteristics:

**Network Topology:**

- 3 interconnected buses forming a triangular mesh network
- 3 bidirectional transmission links connecting each pair of buses

**Generation:**

- Generator 1 (Bus 1): 70-100 MW capacity, 35 $/MWh cost
- Generator 2 (Bus 2): 50-90 MW capacity, 25 $/MWh cost
- Generator 3 (Bus 3): 50-200 MW capacity, 42 $/MWh cost

**Demand:**

- Bus 1: 50 MW
- Bus 2: 40 MW
- Bus 3: 150 MW
- **Total Load: 240 MW**

**Transmission Capacities:**

- Link 1-2: 40 MW (bidirectional)
- Link 2-3: 30 MW (bidirectional)
- Link 3-1: 50 MW (bidirectional)

**Economic Parameters:**

- Spillage cost: 1000 $/MWh (penalty for wasted energy)
- Unsupplied energy cost: 10000 $/MWh (high penalty for unmet demand)

**Expected Dispatch:**

Given the generator costs (Generator 2 is cheapest at 25 $/MWh), the optimizer will prioritize Generator 2, then Generator 1, and finally Generator 3 as needed to meet the total demand of 170 MW while respecting transmission constraints.

## System file and Optimization Graph

Following diagrams represents part of the `system.yml` where user is able to instantiate components (buses, links, generators etc.) and connect them via ports into the optimization graph.

Instantiation of components `bus_1`, `bus_load_1`, `generator_1` and `link_12` is represented as well as connection between `bus_1` and `bus_load_1` components. Entire system file can be found [in this repo](https://github.com/AntaresSimulatorTeam/GEMS/blob/15b4821113a09a417b73d00b3bc24f819ef44c99/doc/5_Examples/QSE/QSE_1_Adequacy/input/system.yml).

![system yaml file explanations](../assets/2_QSE_Adequacy_system.png)

Based on the connection via components from `connections` section in `system.yml` file, optimization graph can be build. Following graph represents optimization graph of **Three-bus Adequacy example**.

![complete diagram with ports](../../assets/2_QSE_1_system_complete.png)

# How to run the study 

## By using Modeler

1. Get Modeler installed through this [tutorial](../1_installation)
2. Go to the Parent folder of `rte-antares-9.3.2-installer-64bits/`
3. Open the terminal
4. Run these command lines :

```bash
# Windows
rte-antares-9.3.2-installer-64bits\bin\antares-9.3-modeler.exe <path-to-study>

# Linux
./rte-antares-9.3.2-installer-64bits/bin/antares-9.3-modeler <path-to-study>
```

The results will be available in the folder `<study_folder>/output`

## Outputs

In `output` folder, the simulation table csv file represents the results of the simulation.

The simulation outputs contain the optimized value of marginal price for each bus. The power flows between buses can be visualized as follows:

![outputs diagram](../../assets/2_QSE_1_out_scheme.png)

- bus_1 : **35 €/MW**, as bus_1 consumes its own power produced at 35 €/MW
- bus_2 : **35 €/MW**, as generator_2 is at its maximum rate, so the next produced 1MWh will be generated by bus_1 and the power will be transferred by link12. Therefore, the marginal price for bus_2 is 35€/MW.
- bus_3 : **42 €/MW**, because bus_3 produces its own power produced at 42 €/MW


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