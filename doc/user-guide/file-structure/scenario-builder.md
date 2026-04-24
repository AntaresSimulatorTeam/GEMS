---
description: Reference for the GEMS scenario builder file — how to define multiple scenarios for probabilistic or stochastic energy system optimisation studies.
tags:
  - Algebraic Modelling Language
  - Optimisation
---

<div style="display: flex; justify-content: flex-end;">
  <a href="../../../..">
    <img src="../../../assets/gemsV2.png" alt="GEMS Logo" width="150"/>
  </a>
</div>

# Scenario Builder

The `modeler-scenariobuilder.dat` file, located in the `data-series` directory, is used to map simulation scenarios to columns of data series. Each line defines an association between a [**scenario group**](system.md#components) name and a **Monte Carlo scenario** (referred to as *scenario*) with a **data series column identifier** (referred to as *time series index*).

## Purpose

The scenario builder associates:

- **scenario group ID**
- **Monte Carlo scenario** (referred to as *scenario*)
- **time series index**

allowing the model to select which data series column is used for a given [**scenario group**](system.md#components) and simulation scenario.

## File Format

Each line in the `modeler-scenariobuilder.dat` file defines a single mapping using the following format:

```text
scenario_group_id, scenario = time_series_index
```

## Example

```text
thermal_group, 0 = 1
thermal_group, 1 = 5
hydro_group, 2 = 7
```

