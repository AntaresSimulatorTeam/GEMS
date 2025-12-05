![Template Banner](../assets/template_banner.svg)
<div style="display: flex; justify-content: space-between; align-items: center;">
  <div style="text-align: left;">
    <a href="folder1/home1.md">Main Section</a>
  </div>
  <div style="text-align: right;">
    <img src="assets/gemsV2.png" alt="GEMS Logo" width="150"/>
  </div>
</div>


# QSE 1 : Three-Bus Adequacy System

## Overview
This tutorial demonstrates adequacy modeling in a meshed three-bus network. Unlike the previous two-bus example, a three-bus system allows us to illustrate **Kirchhoff's Second Law** (loop flows) and network effects that cannot be shown with only two nodes.

## Problem Description

### Network
**Components:**
- **3 Buses** (Regions 1, 2, 3 forming a triangle)
- **3 Links** (connecting each pair of regions)
- **3 Generators** (different capacities and costs)
- **3 Loads** (varying demands)

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

Use `basic-model-library.yml` from [libraries folder](../../libraries/basic_models_library.yml)

## Step 2: System File

Creation of `system.yml` file:

```yaml
system:
  id: system

  components:

    - id: bus_1
      model: basic_models_library.bus

      parameters:
        - id: spillage_cost
          time-dependent: false
          scenario-dependent: false
          value: 1000
        - id: unsupplied_energy_cost
          time-dependent: false
          scenario-dependent: false
          value: 10000

    - id: bus_2
      model: basic_models_library.bus

      parameters:
        - id: spillage_cost
          time-dependent: false
          scenario-dependent: false
          value: 1000
        - id: unsupplied_energy_cost
          time-dependent: false
          scenario-dependent: false
          value: 10000
          
    - id: bus_3
      model: basic_models_library.bus

      parameters:
        - id: spillage_cost
          time-dependent: false
          scenario-dependent: false
          value: 1000
        - id: unsupplied_energy_cost
          time-dependent: false
          scenario-dependent: false
          value: 10000

    - id: bus_load_1
      model: basic_models_library.load

      parameters:
        - id: load_1
          value: 50 # only one value as there is only one time step

    - id: bus_load_2
      model: basic_models_library.load

      parameters:
        - id: load_2
          value: 40 # only one value as there is only one time step
          
    - id: bus_load_3
      model: basic_models_library.load

      parameters:
        - id: load_3
          value: 80 # only one value as there is only one time step
          
          
    - id: generator1
      model: basic_models_library.generator

      parameters:
        - id: p_min
          time-dependent: true
          scenario-dependent: true
          value: generator1_min_generation
        - id: p_max
          time-dependent: true
          scenario-dependent: true
          value: generator1_max_generation
        - id: generation_cost
          time-dependent: false
          scenario-dependent: false
          value: 35

    - id: generator2
      model: basic_models_library.generator

      parameters:
        - id: p_min
          time-dependent: true
          scenario-dependent: true
          value: generator2_min_generation
        - id: p_max
          time-dependent: true
          scenario-dependent: true
          value: generator2_max_generation
        - id: generation_cost
          time-dependent: false
          scenario-dependent: false
          value: 50

    - id: generator3
      model: basic_models_library.generator

      parameters:
        - id: p_min
          time-dependent: true
          scenario-dependent: true
          value: generator3_min_generation
        - id: p_max
          time-dependent: true
          scenario-dependent: true
          value: generator3_max_generation
        - id: generation_cost
          time-dependent: false
          scenario-dependent: false
          value: 42

    - id: link_12
      model: basic_models_library.link
      parameters:
        capacity_direct: 40
        capacity_indirect: 40
    
    - id: link_23
      model: basic_models_library.link
      parameters:
        capacity_direct: 30
        capacity_indirect: 30 
    
    - id: link_31
      model: basic_models_library.link
      parameters:
        capacity_direct: 50
        capacity_indirect: 50

  connections:
    # Load connections
    - component1: bus_1
      component2: bus_load_1
      port1: balance_port
      port2: balance_port

    - component1: bus_2
      component2: bus_load_2
      port1: balance_port
      port2: balance_port

    - component1: bus_3
      component2: bus_load_3
      port1: balance_port
      port2: balance_port

    # Generator connections
    - component1: bus_1
      component2: generator1
      port1: balance_port
      port2: balance_port

    - component1: bus_2
      component2: generator2
      port1: balance_port
      port2: balance_port

    - component1: bus_3
      component2: generator3
      port1: balance_port
      port2: balance_port

    # Link connections
    - component1: bus_1
      component2: link_12
      port1: balance_port
      port2: balance_port

    - component1: bus_1
      component2: link_31
      port1: balance_port
      port2: balance_port

    - component1: bus_2
      component2: link_12
      port1: balance_port
      port2: balance_port

    - component1: bus_2
      component2: link_23
      port1: balance_port
      port2: balance_port

    - component1: bus_3
      component2: link_23
      port1: balance_port
      port2: balance_port

    - component1: bus_3
      component2: link_31
      port1: balance_port
      port2: balance_port 
```

## Step 3: Kirchhoff's Law (Balance of Flows)

### Definition

**Kirchhoff's Second Law** states that the sum of voltages (or flow costs) around any closed loop must equal zero.

---
**Navigation**
<div style="display: flex; justify-content: space-between;">
  <div style="text-align: left;">
    <a href="previous.md">Previous Section</a>
  </div>
    <div style="text-align: center;">
    <a href="../../index.md">Back to Home</a>
  </div>
  <div style="text-align: right;">
    <a href="next.md">Next Section</a>
  </div>
</div>

---

© GEMS (LICENSE)