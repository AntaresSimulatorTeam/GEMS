<div style="display: flex; justify-content: space-between; align-items: center;">
  <div style="text-align: left;">
    <a href="../../../..">Main Section</a>
  </div>
  <div style="text-align: right;">
    <img src="../../assets/gemsV2.png" alt="GEMS Logo" width="150"/>
  </div>
</div>

# QSE 2: Economic Dispatch - Week-Long Optimization

## Overview
This tutorial demonstrates economic dispatch optimization over a one-week time horizon. Economic dispatch determines the optimal power output from each generator at each time period to meet demand at minimum cost.

The study folder is on the [GEMS Github repository](https://github.com/AntaresSimulatorTeam/GEMS/tree/main/doc/5_Examples/QSE/QSE_2_Unit_Commitment).

### Economic Dispatch Definition

**Economic Dispatch** is the problem of determining the optimal power output from generation units over a 7 days horizon.

## Files Structure

```
QSE_2_Unit_Commitment/
├── input/
│   ├── system.yml
│   ├── model-libraries/
│   │   └── unit_commitment_library.yml
│   └── data-series/
│       ├── load_bus_A.csv
│       ├── load_bus_B.csv
│       ├── wind_generation.csv
│       └── solar_generation.csv
└── parameters.yml
```

## Problem Description

**Components:**
- 2 Buses (Region A and Region B)
- 1 Link (connecting the two regions)
- 4 Thermal Generators (with capacity and cost constraints)
- 2 Renewable Generators (wind and solar with variable profiles)
- 2 Loads (variable demand over the week)

**Time Horizon:** 168 hours (1 week) with hourly resolution

![QSE_2 system description diagram](../../assets/2_Scheme_QSE2_Unit_Com_System.png)

# Mathematical Representation

This section presents the mathematical formulation of the economic dispatch problem. The notation is adapted from the [Antares Simulator Wiki](https://xwiki.antares-simulator.org/xwiki/bin/view/Reference%20guide/4.%20Active%20windows/5.Optimization%20problem/).

## Glossary of Mathematical Symbols

### Sets and Indices

| Symbol | Description |
|--------|-------------|
| $T$ | Set of time periods (hours), $t \in \{1, 2, ..., 168\}$ |
| $B$ | Set of buses (regions) |
| $G_b$ | Set of thermal generators at bus $b$ |
| $R_b$ | Set of renewable generators at bus $b$ |
| $L$ | Set of transmission links |

### Decision Variables

| Symbol | Description | Unit |
|--------|-------------|------|
| $P_{g,t}$ | Power output from generator $g$ at time $t$ | MW |
| $F_{l,t}$ | Net power flow through link $l$ at time $t$ | MW |
| $U_{b,t}$ | Unsupplied power at bus $b$ at time $t$ | MW |
| $S_{b,t}$ | Spilled power at bus $b$ at time $t$ | MW |

### Parameters - Generator Technical Constraints

| Symbol | Description | Unit |
|--------|-------------|------|
| $\underline{P}_g$ | Minimum power output | MW |
| $\overline{P}_g$ | Maximum power output | MW |
| $\epsilon_g$ | CO2 emission factor | tCO2/MWh |

### Parameters - Economic

| Symbol | Description | Unit |
|--------|-------------|------|
| $\chi_g$ | Variable generation cost | \$/MWh |
| $\delta_b^+$ | Unsupplied energy cost (value of lost load) | \$/MWh |
| $\delta_b^-$ | Spillage cost | \$/MWh |

### Parameters - System

| Symbol | Description | Unit |
|--------|-------------|------|
| $D_{b,t}$ | Load demand at bus $b$ at time $t$ | MW |
| $\overline{W}_{r,t}$ | Available renewable generation from source $r$ at time $t$ | MW |
| $\overline{F}_l$ | Transmission capacity of link $l$ | MW |

## Optimization Problem

The objective function minimizes total system cost over the week:

$$
\min(\Omega_{\text{total}})
$$

where:

$$
\Omega_{\text{total}} = \Omega_{\text{generation}} + \Omega_{\text{unsupplied}} + \Omega_{\text{spillage}}
$$

## Objective Function Components

### Generation Cost

Variable cost of running generators:

$$
\Omega_{\text{generation}} = \sum_{t \in T} \sum_{b \in B} \sum_{g \in G_b} \chi_g \cdot P_{g,t}
$$

### Unsupplied Energy Cost

Penalty for not meeting demand:

$$
\Omega_{\text{unsupplied}} = \sum_{t \in T} \sum_{b \in B} \delta_b^+ \cdot U_{b,t}
$$

### Spillage Cost

Penalty for wasted renewable energy:

$$
\Omega_{\text{spillage}} = \sum_{t \in T} \sum_{b \in B} \delta_b^- \cdot S_{b,t}
$$

## Constraints

### Power Balance (First Kirchhoff's Law)

For each bus and time period:

$$
\forall b \in B, \forall t \in T: \quad \sum_{g \in G_b} P_{g,t} + \sum_{r \in R_b} \overline{W}_{r,t} - D_{b,t} + \sum_{l \in L_b^+} F_{l,t} - \sum_{l \in L_b^-} F_{l,t} = S_{b,t} - U_{b,t}
$$

### Generator Output Limits

Power output must respect capacity bounds:

$$
\forall g \in G, \forall t \in T: \quad \underline{P}_g \leq P_{g,t} \leq \overline{P}_g
$$

### Transmission Constraints

Power flows are limited by line capacity:

$$
\forall l \in L, \forall t \in T: \quad -\overline{F}_l \leq F_{l,t} \leq \overline{F}_l
$$

# YAML Block Description

## Library File

The library file defines the models for buses, loads, generators, renewables, and transmission links.

![Unit Commitment Library YAML](../../assets/3_QSE_UC_library.png)

### Generator Model

```yaml
- id: generator
  parameters:
    - id: p_min
      scenario-dependent: true
      time-dependent: true
    - id: p_max
      scenario-dependent: true
      time-dependent: true
    - id: generation_cost
      scenario-dependent: false
      time-dependent: false
    - id: co2_emission_factor
      scenario-dependent: false
      time-dependent: false
  variables:
    - id: generation
      lower-bound: p_min
      upper-bound: p_max
      variable-type: continuous
  ports:
    - id: balance_port
      type: flow_port
  port-field-definitions:
    - port: balance_port
      field: flow
      definition: generation
  objective-contributions:
    - id: objective
      expression: sum(generation_cost * generation)
```

### Renewable Model

```yaml
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
      field: flow
      definition: generation
```

## System File

### System Configuration

Create `system.yml` with the following characteristics:

**Region A:**
- Coal plant: 200 MW max, 80 MW min, $35/MWh, CO2 factor 0.9
- Gas plant: 150 MW max, 30 MW min, $50/MWh, CO2 factor 0.4
- Wind farm: Variable generation from timeseries
- Load: Variable demand from timeseries

**Region B:**
- Nuclear plant: 300 MW max, 200 MW min, $15/MWh, CO2 factor 0
- Gas plant: 100 MW max, 10 MW min, $80/MWh, CO2 factor 0.5
- Solar farm: Variable generation from timeseries
- Load: Variable demand from timeseries

**Transmission:**
- Link A-B: 100 MW bidirectional capacity

![System YAML Configuration](../../assets/3_QSE_UC_system.png)

### Example System YAML

```yaml
system:
  id: system

  components:

    # === BUSES ===
    - id: bus_A
      model: unit_commitment_library.bus

      parameters:
        - id: spillage_cost
          time-dependent: false
          scenario-dependent: false
          value: 1000
        - id: unsupplied_energy_cost
          time-dependent: false
          scenario-dependent: false
          value: 10000

    - id: bus_B
      model: unit_commitment_library.bus

      parameters:
        - id: spillage_cost
          time-dependent: false
          scenario-dependent: false
          value: 1000
        - id: unsupplied_energy_cost
          time-dependent: false
          scenario-dependent: false
          value: 10000

    # === LOADS ===
    - id: load_A
      model: unit_commitment_library.load

      parameters:
        - id: load
          time-dependent: true
          scenario-dependent: true
          value: load_bus_A

    - id: load_B
      model: unit_commitment_library.load

      parameters:
        - id: load
          time-dependent: true
          scenario-dependent: true
          value: load_bus_B

    # === THERMAL GENERATORS ===
    - id: coal_plant_A
      model: unit_commitment_library.generator

      parameters:
        - id: p_min
          time-dependent: false
          scenario-dependent: false
          value: 80
        - id: p_max
          time-dependent: false
          scenario-dependent: false
          value: 200
        - id: generation_cost
          time-dependent: false
          scenario-dependent: false
          value: 35
        - id: co2_emission_factor
          time-dependent: false
          scenario-dependent: false
          value: 0.9

    - id: gas_plant_A
      model: unit_commitment_library.generator

      parameters:
        - id: p_min
          time-dependent: false
          scenario-dependent: false
          value: 30
        - id: p_max
          time-dependent: false
          scenario-dependent: false
          value: 150
        - id: generation_cost
          time-dependent: false
          scenario-dependent: false
          value: 50
        - id: co2_emission_factor
          time-dependent: false
          scenario-dependent: false
          value: 0.4

    - id: nuclear_plant_B
      model: unit_commitment_library.generator

      parameters:
        - id: p_min
          time-dependent: false
          scenario-dependent: false
          value: 200
        - id: p_max
          time-dependent: false
          scenario-dependent: false
          value: 300
        - id: generation_cost
          time-dependent: false
          scenario-dependent: false
          value: 15
        - id: co2_emission_factor
          time-dependent: false
          scenario-dependent: false
          value: 0

    - id: gas_plant_B
      model: unit_commitment_library.generator

      parameters:
        - id: p_min
          time-dependent: false
          scenario-dependent: false
          value: 10
        - id: p_max
          time-dependent: false
          scenario-dependent: false
          value: 100
        - id: generation_cost
          time-dependent: false
          scenario-dependent: false
          value: 80
        - id: co2_emission_factor
          time-dependent: false
          scenario-dependent: false
          value: 0.5

    # === RENEWABLES ===
    - id: wind_farm_A
      model: unit_commitment_library.renewable

      parameters:
        - id: generation
          time-dependent: true
          scenario-dependent: true
          value: wind_generation

    - id: solar_farm_B
      model: unit_commitment_library.renewable

      parameters:
        - id: generation
          time-dependent: true
          scenario-dependent: true
          value: solar_generation

    # === TRANSMISSION ===
    - id: link_AB
      model: unit_commitment_library.link

      parameters:
        - id: capacity_direct
          time-dependent: false
          scenario-dependent: false
          value: 100
        - id: capacity_indirect
          time-dependent: false
          scenario-dependent: false
          value: 100

  connections:

    - component1: bus_A
      component2: load_A
      port1: balance_port
      port2: balance_port

    - component1: bus_B
      component2: load_B
      port1: balance_port
      port2: balance_port

    - component1: bus_A
      component2: coal_plant_A
      port1: balance_port
      port2: balance_port

    - component1: bus_A
      component2: gas_plant_A
      port1: balance_port
      port2: balance_port

    - component1: bus_A
      component2: wind_farm_A
      port1: balance_port
      port2: balance_port

    - component1: bus_B
      component2: nuclear_plant_B
      port1: balance_port
      port2: balance_port

    - component1: bus_B
      component2: gas_plant_B
      port1: balance_port
      port2: balance_port

    - component1: bus_B
      component2: solar_farm_B
      port1: balance_port
      port2: balance_port

    - component1: bus_A
      component2: link_AB
      port1: balance_port
      port2: out_port

    - component1: bus_B
      component2: link_AB
      port1: balance_port
      port2: in_port
```

# Time Series Data

## Load Profiles

Weekly load profiles with typical daily patterns for both regions. Each load has its own CSV file.

**data-series/load_bus_A.csv** (168 values, no header):
```csv
100
95
90
85
85
90
110
140
160
170
...
```

**data-series/load_bus_B.csv** (168 values, no header):
```csv
150
145
140
135
135
145
170
200
220
235
...
```

**Pattern characteristics:**
- Daily peak around 8-9 AM and 6-7 PM
- Night valley demand (3-5 AM)
- Region B has higher load than Region A

## Renewable Generation Profiles

**data-series/wind_generation.csv** (168 values, no header):
```csv
45
50
55
...
```
- Variable wind with occasional high production periods
- Average capacity factor ~50%

**data-series/solar_generation.csv** (168 values, no header):
```csv
0
0
...
5
15
30
...
```
- Zero generation at night (hours 0-5, 20-24)
- Peak generation midday (hours 11-14)
- Clear pattern repeating daily

# Expected Dispatch Strategy

## Merit Order

Generators are dispatched according to their variable cost (merit order):

1. **Nuclear Plant B** ($15/MWh) - Lowest cost, runs at maximum capacity when possible
2. **Coal Plant A** ($35/MWh) - Second in merit order
3. **Gas Plant A** ($50/MWh) - Mid-merit generation
4. **Gas Plant B** ($80/MWh) - Highest cost, only used for peak demand

## Baseload Operation

**Nuclear Plant B:**
- Runs at high capacity due to lowest variable cost
- Minimum generation of 200 MW ensures continuous operation
- Zero CO2 emissions

## Mid-Merit Operation

**Coal Plant A:**
- Dispatched when nuclear + renewables insufficient
- Medium variable cost ($35/MWh)
- Highest CO2 emissions (0.9 tCO2/MWh)

**Gas Plant A:**
- Flexible operation between 30-150 MW
- Medium variable cost ($50/MWh)
- Lower CO2 than coal (0.4 tCO2/MWh)

## Peaking Operation

**Gas Plant B:**
- Only dispatched during high-demand periods
- Flexible range (10-100 MW)
- High variable cost ($80/MWh)
- Used sparingly to minimize costs

## Renewable Integration

**Wind and Solar:**
- Used whenever available (zero marginal cost)
- May cause spillage during low-demand periods if generation exceeds demand and minimum generator constraints
- Solar helps reduce gas plant use during afternoon peaks

# How to Run the Study

## By Using Modeler

1. Install Modeler through the [installation tutorial](../2_Getting%20Started/1_installation.md)
2. Navigate to the parent folder of `rte-antares-9.3.2-installer-64bits/`
3. Open the terminal
4. Run these commands:

```bash
# Windows
rte-antares-9.3.2-installer-64bits\bin\antares-9.3-modeler.exe <path-to-study>

# Linux
./rte-antares-9.3.2-installer-64bits/bin/antares-9.3-modeler <path-to-study>
```

The results will be available in `<study_folder>/output`

## By Using GEMSPy

```python
from gemspy import Solver
import pandas as pd
import matplotlib.pyplot as plt

# Load and solve
solver = Solver()
solver.load_system("input/system.yml")
solver.load_library("input/model-libraries/unit_commitment_library.yml")
solver.solve()

# Extract results
results = solver.get_results()

# Generator power output
coal_gen = results['coal_plant_A']['generation']
gas_a_gen = results['gas_plant_A']['generation']
nuclear_gen = results['nuclear_plant_B']['generation']
gas_b_gen = results['gas_plant_B']['generation']

# Print summary
print(f"=== Week Summary ===")
print(f"Total coal generation: {sum(coal_gen):.0f} MWh")
print(f"Total gas A generation: {sum(gas_a_gen):.0f} MWh")
print(f"Total nuclear generation: {sum(nuclear_gen):.0f} MWh")
print(f"Total gas B generation: {sum(gas_b_gen):.0f} MWh")
print(f"\nTotal cost: ${results['total_cost']:,.0f}")
```

## Outputs

### Generation Dispatch

Stacked generation showing how different units serve load throughout the week:

![Generation Dispatch](../../assets/3_QSE_UC_out_generation.png)

### Marginal Prices

Marginal prices at each bus over the week, derived from the dual values of the balance constraints.

### CO2 Emissions

Total CO2 emissions from each generator, calculated using the emission factors.

### Key Observations

1. **Nuclear baseload:** Runs at high capacity due to lowest cost
2. **Merit order dispatch:** Generators dispatched by increasing cost
3. **Renewable integration:** Wind and solar reduce thermal generation when available
4. **Peak periods:** Gas Plant B only operates during high-demand hours
5. **Transmission flows:** Link AB balances regional supply and demand

# Key Differences: Adequacy vs Economic Dispatch

## Adequacy (Tutorial QSE 1)

- Single time step analysis
- Focus on capacity balance
- Simpler problem formulation
- Quick to solve

## Economic Dispatch (This Tutorial)

- **Multi-period optimization** (168 hours)
- Time-dependent load and renewable profiles
- Transmission network constraints
- CO2 emission tracking
- Linear Programming (LP) problem
- Merit order dispatch based on generation costs

# Computational Considerations

## Problem Size

- **Variables:** 1,848
- **Constraints:** 504
- All continuous variables (LP problem)

## Solving Time

- Typically solves in milliseconds with modern LP solvers
- COIN-OR CBC solver used in this example

## Solver Settings

From `parameters.yml`:
```yaml
solver: coin
solver-logs: false
solver-parameters: THREADS 1
no-output: false
first-time-step: 0
last-time-step: 167
```

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
