<div style="display: flex; justify-content: space-between; align-items: center;">
  <div style="text-align: left;">
    <a href="../../../..">Main Section</a>
  </div>
  <div style="text-align: right;">
    <img src="../../assets/gemsV2.png" alt="GEMS Logo" width="150"/>
  </div>
</div>

# QSE 2: Unit Commitment - Mathematical Representation

This part represents the optimization problem formulation of the example [QSE_Unit_Commitment](2B_QSE_unit_commitment.md) that is built up from [`antares-legacy-models.yml`](https://github.com/AntaresSimulatorTeam/GEMS/blob/main/libraries/antares_legacy_models.yml) library. The referenced library includes additional models that are not used in the example and are therefore not included in the optimization problem formulation.

## Glossary of Mathematical Symbols

### General notation

| Symbol | Description |
|--------|-------------|
| $T$ | Set of time periods (hours), $t \in \{1, 2, ..., 168\}$ |
| $b$ | The single bus in the system |
| $N$ | Number of thermal units (10) |

### Decision Variables - Thermal

| Symbol | Description | Unit | Type |
|--------|-------------|------|------|
| $P_{t}$ | Total power output from thermal cluster at time $t$ | MW | Continuous |
| $n^{on}_{t}$ | Number of units ON at time $t$ | - | Integer |
| $n^{start}_{t}$ | Number of units starting at time $t$ | - | Integer |
| $n^{stop}_{t}$ | Number of units stopping at time $t$ | - | Integer |

### Decision Variables - System

| Symbol | Description | Unit |
|--------|-------------|------|
| $U_{t}$ | Unsupplied power at time $t$ | MW |
| $S_{t}$ | Spilled power at time $t$ | MW |

### Parameters - Thermal

| Symbol | Description | Value | Unit |
|--------|-------------|-------|------|
| $\underline{P}^{unit}$ | Minimum power per unit | 0 | MW |
| $\overline{P}^{unit}$ | Maximum power per unit | 1 | MW |
| $\chi^{gen}$ | Variable generation cost | 50 | €/MWh |
| $\chi^{start}$ | Startup cost | 100 | $ |
| $\chi^{fix}$ | Fixed cost (per unit ON) | 10 | $/h |
| $\tau^{up}$ | Minimum up time | 2 | hours |
| $\tau^{down}$ | Minimum down time | 2 | hours |

### Parameters - Renewables

| Symbol | Description | Unit |
|--------|-------------|------|
| $R^{solar}_{t}$ | Solar generation at time $t$ | MW |
| $R^{wind}_{t}$ | Wind generation at time $t$ | MW |

### Parameters - System

| Symbol | Description | Value | Unit |
|--------|-------------|-------|------|
| $D_{t}$ | Load demand at time $t$ | 35-125 | MW |
| $\delta^+$ | Unsupplied energy cost | 10000 | €/MWh |
| $\delta^-$ | Spillage cost | 1000 | €/MWh |

## Optimization Problem

The objective function minimizes total system cost:

$$
\min(\Omega_{\text{total}})
$$

where:

$$
\Omega_{\text{total}} = \Omega_{\text{thermal}} + \Omega_{\text{unsupplied}} + \Omega_{\text{spillage}}
$$

## Objective Function Components

### Thermal Generation Cost

$$
\Omega_{\text{thermal}} = \sum_{t \in T} \left( \chi^{gen} \cdot P_{t} + \chi^{start} \cdot n^{start}_{t} + \chi^{fix} \cdot n^{on}_{t} \right)
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

For each time period, generation must equal demand plus spillage minus unsupplied:

$$
\forall t \in T: \quad P_{t} + R^{solar}_{t} + R^{wind}_{t} - D_{t} = S_{t} - U_{t}
$$

### Thermal Generation Limits

The thermal output is bounded by the number of units ON:

$$
\forall t \in T: \quad n^{on}_{t} \cdot \underline{P}^{unit} \leq P_{t} \leq n^{on}_{t} \cdot \overline{P}^{unit}
$$

### Unit Dynamics

The number of units ON follows the commitment dynamics:

$$
\forall t \in T: \quad n^{on}_{t} = n^{on}_{t-1} + n^{start}_{t} - n^{stop}_{t}
$$

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
