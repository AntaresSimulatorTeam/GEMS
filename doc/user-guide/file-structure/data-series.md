---
description: Reference for the GEMS data series file — how to supply time-varying input data (load profiles, availability factors, costs) to parameterise energy system models.
tags:
  - Algebraic Modelling Language
  - Energy Modelling
---

<div style="display: flex; justify-content: flex-end;">
  <a href="../../../..">
    <img src="../../../assets/gemsV2.png" alt="GEMS Logo" width="150"/>
  </a>
</div>

# Data Series

Data series provide the numerical input data for time-varying and scenario-varying parameters and they are stored in `csv` files.

The filename (without extension) serves as the `id` of the data series. For instance, a file named `demand_profile.csv` defines a data series with the `id` `demand_profile`. This `id` is what users would use in the system file’s to instantiate parameter values.

## Time-dependent series

Represent a value that changes over time but is the same across all scenarios. The file should contain one column of numbers, where each row is the value at a consecutive timestamp. There should be as many rows as the number of time steps in your simulation horizon. For example, a demand_profile.tsv for a one-day simulation with hourly time steps (24 hours) would have 24 rows of data. A short example (with, say, 4 time steps) might look like:

```text
10.4
23.1
34
45
```

Each line is the demand at a given time (with the first line corresponding to time step 0, and so on).

## Scenario-dependent series

Represent a value that varies by scenario, but is constant in time. The file should contain one row of numbers, with each column representing the value for one scenario. For example, if you have 4 scenarios defined, a scenario-dependent series file might contain a single line with 4 values:

```text
10 22 55 42
```

This would indicate the parameter’s value in scenario 1 is 10, scenario 2 is 60, 22.

## Time-and-scenario-dependent series

Represent data that varies across both time and scenarios (a different time series for each scenario). The file in this case would be a matrix with rows corresponding to time steps and columns corresponding to scenarios. For example, if there are 3 scenarios and 2 time steps (for simplicity), a file could look like:

```text
10 22 55
45 89 33
```

Here, the first row contains the values at time-step 0 for scenarios 1, 2, 3 respectively, and the second row contains the values at time-step 1 for scenarios 1, 2, 3.

