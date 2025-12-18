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
This tutorial demonstrates a simple unit commitment optimization. Unit commitment determines the optimal power output from a generator at each time period to meet demand at minimum cost.

The study folder is on the [GEMS Github repository](https://github.com/AntaresSimulatorTeam/GEMS/tree/main/doc/5_Examples/QSE/QSE_2_Unit_Commitment).

## Files Structure

```
QSE_2_Unit_Commitment/
├── input/
│   ├── system.yml
│   ├── model-libraries/
│   │   └── unit_commitment_library.yml
│   └── data-series/
│       ├── solar.csv
│       ├── wind.csv
│       └── load.csv
└── parameters.yml
```

## Problem Description

**Components:**

  - 1 Bus
  - 1 Generator (10 MW capacity) with 10 units of 1 MW
  - 1 Solar Plant
  - 1 Wind Plant
  - 1 Load (variable demand)

**Time Horizon:** 1 week with hourly resolution

![QSE_2 system description diagram](../assets/2_Scheme_QSE2_Unit_Com_System.png)

# Mathematical Representation

This section presents the mathematical formulation of the unit commitment problem.

## Glossary of Mathematical Symbols

### General notation

| Symbol | Description |
|--------|-------------|
| $T$ | Set of time periods (hours), $t \in \{1, 2, ..., 12\}$ |
| $b$ | The single bus in the system |

### Decision Variables

| Symbol | Description | Unit |
|--------|-------------|------|
| $P_{t}$ | Power output from generator at time $t$ | MW |
| $U_{t}$ | Unsupplied power at time $t$ | MW |
| $S_{t}$ | Spilled power at time $t$ | MW |

### Parameters - Generator

| Symbol | Description | Unit |
|--------|-------------|------|
| $\underline{P}$ | Minimum power output (0 MW) | MW |
| $\overline{P}$ | Maximum power output (10 MW) | MW |
| $\chi$ | Variable generation cost (50 $/MWh) | $/MWh |

### Parameters - System

| Symbol | Description | Unit |
|--------|-------------|------|
| $D_{t}$ | Load demand at time $t$ | MW |
| $\delta^+$ | Unsupplied energy cost (10000 $/MWh) | $/MWh |
| $\delta^-$ | Spillage cost (1000 $/MWh) | $/MWh |

## Optimization Problem

The objective function minimizes total system cost:

$$
\min(\Omega_{\text{dispatch}})
$$

where:

$$
\Omega_{\text{dispatch}} = \Omega_{\text{generation}} + \Omega_{\text{unsupplied}} + \Omega_{\text{spillage}}
$$

## Objective Function Components

### Generation Cost

$$
\Omega_{\text{generation}} = \sum_{t \in T} \chi \cdot P_{t}
$$

### Unsupplied Energy Cost

$$
\Omega_{\text{unsupplied}} = \sum_{t \in T} \delta^+ \cdot U_{t}
$$

### Spillage Cost

$$
\Omega_{\text{spillage}} = \sum_{t \in T} \delta^- \cdot S_{t}
$$

## Constraints

### Power Balance (Kirchhoff's Law)

For each time period:

$$
\forall t \in T: \quad P_{t} - D_{t} = S_{t} - U_{t}
$$

### Generator Output Limits

$$
\forall t \in T: \quad \underline{P} \leq P_{t} \leq \overline{P}
$$

# YAML Block Description

## Library File

The library file defines the models for bus, load, and generator.

## System File

### System Configuration

- Create `system.yml` with the following characteristics:

**Single Area:**

- Bus: spillage_cost = 1000 $/MWh, unsupplied_energy_cost = 10000 $/MWh
- Generator: 10 MW max, 0 MW min, $50/MWh, CO2 factor 0.4
- Load: Variable demand from timeseries (5-10 MW range)

# How to Run the Study

## By Using Modeler

1. Get Modeler installed through this [tutorial](./1_installation.md)
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
