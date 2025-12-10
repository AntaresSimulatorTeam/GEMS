![Template Banner](../assets/template_banner.svg)
<div style="display: flex; justify-content: space-between; align-items: center;">
  <div style="text-align: left;">
    <a href="../../../..">Main Section</a>
  </div>
  <div style="text-align: right;">
    <img src="../../assets/gemsV2.png" alt="GEMS Logo" width="150"/>
  </div>
</div>


# QSE 1 : Three-Bus Adequacy System

## Overview
This tutorial demonstrates adequacy modeling in a meshed three-bus network. Unlike the previous two-bus example, a three-bus system allows us to illustrate **Kirchhoff's Second Law** (loop flows) and network effects that cannot be shown with only two nodes.

## Problem Description

### Network
**Components:**

- 3 Buses (Regions 1, 2, 3 forming a triangle)
- 3 Links (connecting each pair of regions)
- 3 Generators (different capacities and costs)
- 3 Loads (varying demands)

**Time Horizon:** 1 hour is used for this example

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

## Step 1: Library File

- Use `basic-model-library.yml` from [libraries folder](../../libraries/basic_models_library.yml)

## Step 2: System File

- Creation of `system.yml` [file](../2_Getting%20Started/QSE_Study/input/system.yml)

This system models a three-bus network with the following characteristics:

**Network Topology:**

- 3 interconnected buses forming a triangular mesh network
- 3 bidirectional transmission links connecting each pair of buses

**Generation:**

- Generator 1 (Bus 1): 70-100 MW capacity, 35 $/MWh cost
- Generator 2 (Bus 2): 50-90 MW capacity, 25 $/MWh cost (cheapest)
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

## How to run the study 

### With Modeler

1. Get Modeler installed through this [tutorial](../2_Getting%20Started/1_installation.md)
2. Go to the GEMS study folder, open the terminal
3. Type in the terminal `antares-modeler QSE_Study/`

The results will be available in the folder `QSE_Study/output`


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