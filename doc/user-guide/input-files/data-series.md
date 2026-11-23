# Data Series

Data series provide the numerical input data for time-varying and scenario-varying parameters and they are stored in `csv` files.

The filename (without extension) serves as the `id` of the data series. For instance, a file named `demand_profile.csv` defines a data series with the `id` `demand_profile`. This `id` is what users would use in the [system file](system.md) to instantiate parameter values.

## Time-dependent series

Represent a value that changes over time but is the same across all scenarios. The file should contain one column of numbers, where each row is the value at a consecutive timestamp. There should be as many rows as the number of time steps in your simulation horizon. For example, a demand_profile.csv for a one-day simulation with hourly time steps (24 hours) would have 24 rows of data. A short example (with, say, 4 time steps) might look like:

```text
10.4
23.1
34
45
```

Each line is the demand at a given time (with the first line corresponding to time step 0, and so on).

## Scenario-dependent series

Represent a value that varies by scenario, but is constant in time. The file should contain one row of numbers, with each column representing the value for one scenario. The mapping from simulation scenarios to column indices is controlled by the [scenario builder](scenario-builder.md). For example, if you have 4 scenarios defined, a scenario-dependent series file might contain a single line with 4 values:

```text
10, 22, 55, 42
```

This would indicate the parameter's value in scenario 1 is 10, scenario 2 is 22, scenario 3 is 55, and scenario 4 is 42.

## Time-and-scenario-dependent series

Represent data that varies across both time and scenarios (a different time series for each scenario). The file in this case would be a matrix with rows corresponding to time steps and columns corresponding to scenarios. For example, if there are 3 scenarios and 2 time steps (for simplicity), a file could look like:

```text
10, 22, 55
45, 89, 33
```

Here, the first row contains the values at time-step 0 for scenarios 1, 2, 3 respectively, and the second row contains the values at time-step 1 for scenarios 1, 2, 3.

## Connection-weight tables (Proposed)

!!! warning "Design proposal — not yet implemented"
    Part of the [Weighted connections](../syntax.md#weighted-connections-proposed) proposal.

A [connection-weight table](system.md#connection-weights) gives one weight of one port for all the
port's connections. Unlike the series above, it has a **header row**. Its columns are, in order: one
per set in `indexed-by` (see the [custom sets proposal](https://github.com/AntaresSimulatorTeam/GEMS/pull/207)),
one named after the **port** holding the connection keys, `time` and `scenario` if the weight
depends on them, and `value`. The table is dense: each combination of keys appears exactly once.
Column naming and scenario mapping are [open questions 3 and 4](../syntax.md#open-questions-on-weighted-connections).

First rows of `core_ptdf_zones.csv`:

```csv
cnec,zones,time,value
0,fr,0,0.112
0,be,0,-0.231
1,fr,0,0.008
```
