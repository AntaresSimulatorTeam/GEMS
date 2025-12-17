<div style="display: flex; justify-content: space-between; align-items: center;">
  <div style="text-align: left;">
    <a href="../../../..">Main Section</a>
  </div>
  <div style="text-align: right;">
    <img src="../../assets/gemsV2.png" alt="GEMS Logo" width="150"/>
  </div>
</div>

# QSE 2: Unit Commitment - Week-Long Optimization

## Overview
This tutorial demonstrates unit commitment optimization over a one-week time horizon. Unit commitment determines which generators should be online (committed) at each time period while respecting technical constraints like minimum up/down times and ramping limits.

The study folder is on the [GEMS Github repository](https://github.com/AntaresSimulatorTeam/GEMS/tree/main/doc/5_Examples/QSE/QSE_2_Unit_Commitment).

### Unit Commitment Definition

**Unit Commitment** is the problem of determining the optimal schedule of power generation units over a planning horizon while satisfying:
- Load demand at each time step
- Generator technical constraints (min/max power, ramping rates, minimum up/down times)
- Network transmission limits
- System reserve requirements

Region A:                    Region B:
- Coal Plant (200 MW)        - Nuclear Plant (300 MW)
- Gas Plant (150 MW)         - Peaker Plant (100 MW)
- Wind Farm (100 MW)         - Solar Farm (80 MW)
- Load (80-180 MW)           - Load (120-250 MW)
         \                    /
          \--- Link 100MW ---/

          
## Files Structure
```
tutorial_QSE_unit_commitment/
├── input/
│   ├── library.yml
│   ├── system.yml
│   └── data-series/
│       ├── load_ts.csv
│       ├── wind_generation_ts.csv
│       └── solar_generation_ts.csv
└── parameters.yml
```

## Problem Description

### System Overview

**Components:**
- 2 Buses (Region A and Region B)
- 1 Link (connecting the two regions)
- 4 Thermal Generators (with commitment variables and technical constraints)
- 2 Renewable Sources (wind and solar with variable profiles)
- 2 Loads (variable demand over the week)

**Time Horizon:** 168 hours (1 week) with hourly resolution

![QSE Unit Commitment Scheme](../assets/3_QSE_UC_scheme.png)

### Key Unit Commitment Features

This example introduces:
1. **Binary commitment variables** - Generators can be ON or OFF
2. **Minimum up/down times** - Once started, generators must run for minimum duration
3. **Start-up costs** - Cost incurred when starting a generator
4. **Ramping constraints** - Limited rate of power change between hours
5. **Minimum stable generation** - Generators have minimum output when running

# Mathematical Representation

This section presents the mathematical formulation of the unit commitment problem. The notation is adapted from the [Antares Simulator Wiki](https://xwiki.antares-simulator.org/xwiki/bin/view/Reference%20guide/4.%20Active%20windows/5.Optimization%20problem/).

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
| $u_{g,t}$ | Commitment status of generator $g$ at time $t$ (binary) | - |
| $v_{g,t}$ | Start-up indicator for generator $g$ at time $t$ (binary) | - |
| $w_{g,t}$ | Shut-down indicator for generator $g$ at time $t$ (binary) | - |
| $P_{g,t}$ | Power output from generator $g$ at time $t$ | MW |
| $F_{l,t}$ | Net power flow through link $l$ at time $t$ | MW |
| $U_{b,t}$ | Unsupplied power at bus $b$ at time $t$ | MW |
| $S_{b,t}$ | Spilled power at bus $b$ at time $t$ | MW |

### Parameters - Generator Technical Constraints

| Symbol | Description | Unit |
|--------|-------------|------|
| $\underline{P}_g$ | Minimum stable power output when online | MW |
| $\overline{P}_g$ | Maximum power output | MW |
| $RU_g$ | Ramp-up rate limit | MW/h |
| $RD_g$ | Ramp-down rate limit | MW/h |
| $UT_g$ | Minimum up time (hours generator must stay on) | hours |
| $DT_g$ | Minimum down time (hours generator must stay off) | hours |

### Parameters - Economic

| Symbol | Description | Unit |
|--------|-------------|------|
| $\chi_g$ | Variable generation cost | \$/MWh |
| $\kappa_g$ | Start-up cost | \$ |
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
\Omega_{\text{total}} = \Omega_{\text{generation}} + \Omega_{\text{startup}} + \Omega_{\text{unsupplied}} + \Omega_{\text{spillage}}
$$

## Objective Function Components

### Generation Cost

Variable cost of running committed generators:

$$
\Omega_{\text{generation}} = \sum_{t \in T} \sum_{b \in B} \sum_{g \in G_b} \chi_g \cdot P_{g,t}
$$

### Start-up Cost

Cost incurred when starting generators:

$$
\Omega_{\text{startup}} = \sum_{t \in T} \sum_{b \in B} \sum_{g \in G_b} \kappa_g \cdot v_{g,t}
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

Power output must respect commitment status and capacity:

$$
\forall g \in G, \forall t \in T: \quad \underline{P}_g \cdot u_{g,t} \leq P_{g,t} \leq \overline{P}_g \cdot u_{g,t}
$$

### Start-up and Shut-down Logic

Link commitment status changes to start-up and shut-down variables:

$$
\forall g \in G, \forall t \in T: \quad v_{g,t} - w_{g,t} = u_{g,t} - u_{g,t-1}
$$

where $v_{g,t}, w_{g,t} \in \{0,1\}$ and $v_{g,t} + w_{g,t} \leq 1$ (cannot start and stop simultaneously).

### Minimum Up Time

Generator must stay online for minimum duration after start-up:

$$
\forall g \in G, \forall t \in T: \quad \sum_{\tau=t}^{\min(t+UT_g-1, |T|)} u_{g,\tau} \geq UT_g \cdot v_{g,t}
$$

### Minimum Down Time

Generator must stay offline for minimum duration after shut-down:

$$
\forall g \in G, \forall t \in T: \quad \sum_{\tau=t}^{\min(t+DT_g-1, |T|)} (1 - u_{g,\tau}) \geq DT_g \cdot w_{g,t}
$$

### Ramping Constraints

Power output changes are limited by ramp rates:

**Ramp-up limit:**
$$
\forall g \in G, \forall t \in T: \quad P_{g,t} - P_{g,t-1} \leq RU_g
$$

**Ramp-down limit:**
$$
\forall g \in G, \forall t \in T: \quad P_{g,t-1} - P_{g,t} \leq RD_g
$$

### Transmission Constraints

Power flows are limited by line capacity:

$$
\forall l \in L, \forall t \in T: \quad -\overline{F}_l \leq F_{l,t} \leq \overline{F}_l
$$

# YAML Block Description

## Library File

The library file must include models with binary commitment variables and technical constraints.

![Unit Commitment Library YAML](../../assets/3_QSE_UC_library.png)

### Thermal Generator with Commitment Model

```yaml
models:
  - id: thermal_generator_uc
    parameters:
      - id: p_min
        description: Minimum stable generation
      - id: p_max
        description: Maximum generation capacity
      - id: generation_cost
        description: Variable cost
      - id: startup_cost
        description: Cost to start the unit
      - id: ramp_up_rate
        description: Maximum increase per hour
      - id: ramp_down_rate
        description: Maximum decrease per hour
      - id: min_up_time
        description: Minimum hours online
      - id: min_down_time
        description: Minimum hours offline
    
    variables:
      - id: commitment
        lower-bound: 0
        upper-bound: 1
        variable-type: integer  # Binary: 0 or 1
      
      - id: startup
        lower-bound: 0
        upper-bound: 1
        variable-type: integer
      
      - id: shutdown
        lower-bound: 0
        upper-bound: 1
        variable-type: integer
      
      - id: generation
        lower-bound: 0
        upper-bound: p_max
        variable-type: continuous
    
    constraints:
      - id: min_generation
        expression: generation >= p_min * commitment
      
      - id: max_generation
        expression: generation <= p_max * commitment
      
      - id: commitment_logic
        expression: startup - shutdown = commitment - commitment[t-1]
      
      - id: no_simultaneous_start_stop
        expression: startup + shutdown <= 1
      
      - id: ramp_up
        expression: generation - generation[t-1] <= ramp_up_rate
      
      - id: ramp_down
        expression: generation[t-1] - generation <= ramp_down_rate
      
      - id: min_up_time_constraint
        expression: sum_window(commitment, min_up_time) >= min_up_time * startup
      
      - id: min_down_time_constraint
        expression: sum_window(1 - commitment, min_down_time) >= min_down_time * shutdown
    
    ports:
      - id: balance_port
        type: flow
    
    port-field-definitions:
      - port: balance_port
        field: flow
        definition: generation
    
    objective-contributions:
      - id: variable_cost
        expression: sum(generation_cost * generation)
      
      - id: startup_cost
        expression: sum(startup_cost * startup)
```

## System File

### System Configuration

Create `system.yml` with the following characteristics:

**Region A:**
- Generator A1: Coal, 200 MW, high start-up cost (12 hours min up-time)
- Generator A2: Gas, 150 MW, medium start-up cost (4 hours min up-time)
- Wind farm: 100 MW installed capacity
- Load: Variable 80-180 MW

**Region B:**
- Generator B1: Nuclear, 300 MW, very high start-up cost (24 hours min up-time)
- Generator B2: Gas peaker, 100 MW, low start-up cost (1 hour min up-time)
- Solar farm: 80 MW installed capacity
- Load: Variable 120-250 MW

**Transmission:**
- Link A-B: 100 MW bidirectional capacity

![System YAML Configuration](../../assets/3_QSE_UC_system.png)

### Example System YAML

```yaml
system:
  id: unit_commitment_week
  description: Week-long unit commitment with 4 thermal generators
  
  required-model-libraries:
    - unit_commitment_library
  
  components:
    # === BUSES ===
    - id: bus_region_a
      model: unit_commitment_library.bus
      parameters:
        spillage_cost: 100
        unsupplied_energy_cost: 10000
    
    - id: bus_region_b
      model: unit_commitment_library.bus
      parameters:
        spillage_cost: 100
        unsupplied_energy_cost: 10000
    
    # === THERMAL GENERATORS ===
    - id: coal_plant_a
      model: unit_commitment_library.thermal_generator_uc
      parameters:
        p_min: 80           # Must run at least 80 MW when on
        p_max: 200
        generation_cost: 35
        startup_cost: 5000  # Expensive to start
        ramp_up_rate: 30
        ramp_down_rate: 30
        min_up_time: 12     # Must run 12 hours minimum
        min_down_time: 8
    
    - id: gas_plant_a
      model: unit_commitment_library.thermal_generator_uc
      parameters:
        p_min: 30
        p_max: 150
        generation_cost: 50
        startup_cost: 1500
        ramp_up_rate: 50
        ramp_down_rate: 50
        min_up_time: 4
        min_down_time: 2
    
    - id: nuclear_plant_b
      model: unit_commitment_library.thermal_generator_uc
      parameters:
        p_min: 250          # Nuclear runs at high minimum load
        p_max: 300
        generation_cost: 15 # Cheap operation
        startup_cost: 50000 # Very expensive to start
        ramp_up_rate: 15    # Slow ramping
        ramp_down_rate: 15
        min_up_time: 24     # Must run full day
        min_down_time: 48
    
    - id: peaker_plant_b
      model: unit_commitment_library.thermal_generator_uc
      parameters:
        p_min: 10           # Flexible peaker
        p_max: 100
        generation_cost: 80 # Expensive to run
        startup_cost: 200   # Quick start
        ramp_up_rate: 100   # Fast ramping
        ramp_down_rate: 100
        min_up_time: 1
        min_down_time: 1
    
    # === RENEWABLES ===
    - id: wind_farm_a
      model: unit_commitment_library.renewable
      parameters:
        generation:
          timeseries: wind_generation_ts.csv
          scenario: 1
    
    - id: solar_farm_b
      model: unit_commitment_library.renewable
      parameters:
        generation:
          timeseries: solar_generation_ts.csv
          scenario: 1
    
    # === LOADS ===
    - id: load_region_a
      model: unit_commitment_library.load
      parameters:
        load:
          timeseries: load_region_a_ts.csv
          scenario: 1
    
    - id: load_region_b
      model: unit_commitment_library.load
      parameters:
        load:
          timeseries: load_region_b_ts.csv
          scenario: 1
    
    # === TRANSMISSION ===
    - id: transmission_ab
      model: unit_commitment_library.link
      parameters:
        capacity_direct: 100
        capacity_indirect: 100
  
  connections:
    # Region A
    - port-from: coal_plant_a.balance_port
      port-to: bus_region_a.balance_port
    - port-from: gas_plant_a.balance_port
      port-to: bus_region_a.balance_port
    - port-from: wind_farm_a.balance_port
      port-to: bus_region_a.balance_port
    - port-from: load_region_a.balance_port
      port-to: bus_region_a.balance_port
    - port-from: transmission_ab.out_port
      port-to: bus_region_a.balance_port
    
    # Region B
    - port-from: nuclear_plant_b.balance_port
      port-to: bus_region_b.balance_port
    - port-from: peaker_plant_b.balance_port
      port-to: bus_region_b.balance_port
    - port-from: solar_farm_b.balance_port
      port-to: bus_region_b.balance_port
    - port-from: load_region_b.balance_port
      port-to: bus_region_b.balance_port
    - port-from: transmission_ab.in_port
      port-to: bus_region_b.balance_port
```

# Time Series Data

## Load Profiles

Weekly load profiles with typical daily patterns and weekend variations.

**data-series/load_region_a_ts.csv** (168 values):
```csv
ts-name,load_region_a
0,120
1,110
2,100
3,95
4,90
5,100
6,130
7,160
8,180
9,175
...
```

**Pattern characteristics:**
- Daily peak around 8-9 AM and 6-7 PM
- Weekend demand 20% lower than weekdays
- Night valley demand (3-5 AM)

## Renewable Generation Profiles

**data-series/wind_generation_ts.csv:**
- Variable wind with occasional high production periods
- Average capacity factor ~35%
- Some periods with near-zero wind

**data-series/solar_generation_ts.csv:**
- Zero generation at night (hours 0-6, 20-24)
- Peak generation midday (hours 11-14)
- Clear pattern repeating daily

# Expected Dispatch Strategy

## Baseload Operation

**Nuclear Plant B:**
- Likely runs continuously (168 hours) due to:
  - Very high start-up cost (\$50,000)
  - Long minimum up time (24 hours)
  - Lowest variable cost (\$15/MWh)
  - High minimum generation (250 MW)
- Provides baseload for Region B

## Mid-Merit Operation

**Coal Plant A:**
- Runs during weekdays, potentially off on weekends
- Start-up cost (\$5,000) and 12-hour minimum up time make it commit for longer periods
- Medium variable cost (\$35/MWh)

**Gas Plant A:**
- More flexible operation (4-hour minimum up time)
- Starts/stops more frequently to follow load variations
- Medium-high variable cost (\$50/MWh)

## Peaking Operation

**Gas Peaker B:**
- Only runs during high-demand periods
- Very flexible (1-hour min up/down time)
- Fast ramping (100 MW/hour)
- High variable cost (\$80/MWh) means used sparingly
- Quick start (\$200) allows frequent cycling

## Renewable Integration

**Wind and Solar:**
- Used whenever available (zero marginal cost)
- May cause spillage during low-demand periods if generation exceeds demand and minimum generator constraints
- Solar helps reduce peaker use during afternoon peaks

## Weekly Pattern

**Typical Week:**
- **Monday-Friday:** All units except peaker likely committed, peaker for evening peaks
- **Weekend:** Lower demand may allow coal plant shutdown, nuclear continues
- **Monday morning:** Potential restart costs for coal plant
- **Night hours:** Minimum generation constraints may cause renewable spillage

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
solver.load_system("system.yml")
solver.load_library("library.yml")
solver.solve()

# Extract results
results = solver.get_results()

# Generator commitment status
coal_commitment = results['coal_plant_a']['commitment']
gas_a_commitment = results['gas_plant_a']['commitment']
nuclear_commitment = results['nuclear_plant_b']['commitment']
peaker_commitment = results['peaker_plant_b']['commitment']

# Generator power output
coal_gen = results['coal_plant_a']['generation']
gas_a_gen = results['gas_plant_a']['generation']
nuclear_gen = results['nuclear_plant_b']['generation']
peaker_gen = results['peaker_plant_b']['generation']

# Print summary
print(f"=== Week Summary ===")
print(f"Nuclear operating hours: {sum(nuclear_commitment)}")
print(f"Coal operating hours: {sum(coal_commitment)}")
print(f"Gas A operating hours: {sum(gas_a_commitment)}")
print(f"Peaker operating hours: {sum(peaker_commitment)}")
print(f"\nTotal generation cost: ${results['total_generation_cost']:,.0f}")
print(f"Total start-up cost: ${results['total_startup_cost']:,.0f}")
print(f"Total cost: ${results['total_cost']:,.0f}")
```

## Outputs

### Commitment Schedule

The commitment schedule shows when each generator is ON (1) or OFF (0):

![Generator Commitment Schedule](../../assets/3_QSE_UC_out_commitment.png)

### Generation Dispatch

Stacked generation showing how different units serve load throughout the week:

![Generation Dispatch](../../assets/3_QSE_UC_out_generation.png)

### Cost Breakdown

Analysis of generation costs vs start-up costs:

![Cost Analysis](../../assets/3_QSE_UC_out_costs.png)

### Key Observations

1. **Nuclear baseload:** Runs continuously at high capacity factor
2. **Weekend effect:** Reduced generation and potentially fewer committed units
3. **Renewable integration:** Wind and solar reduce thermal generation when available
4. **Peak periods:** Peaker plant only operates during high-demand hours
5. **Start-up events:** Limited due to minimum up-time constraints and high start-up costs

# Key Differences: Unit Commitment vs Economic Dispatch

## Economic Dispatch (Tutorial QSE 1)

- **Continuous variables only**
- Generators can produce any level within [Pmin, Pmax]
- No start-up costs or minimum runtime constraints
- Instantaneous response
- Linear Programming (LP) problem
- Faster to solve

## Unit Commitment (This Tutorial)

- **Binary commitment variables** (ON/OFF decisions)
- Minimum stable generation when running
- Start-up and shut-down costs
- Minimum up/down time constraints
- Ramping rate limits
- Mixed Integer Linear Programming (MILP) problem
- More realistic but computationally intensive

# Computational Considerations

## Problem Size

- **Variables:** ~7,000 (168 hours × ~40 variables per hour)
- **Binary variables:** ~700 (4 generators × 3 binary vars × 168 hours)
- **Constraints:** ~10,000

## Solving Time

- Economic dispatch: seconds
- Unit commitment: minutes to hours depending on solver and system size

## Solver Settings

For large problems, consider:
- MIP gap tolerance (e.g., 1% optimality)
- Time limits
- Heuristic methods for initial solutions
- Decomposition techniques for multi-week problems

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
