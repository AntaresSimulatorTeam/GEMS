<div style="display: flex; justify-content: flex-end;">
  <a href="../../../..">
    <img src="../../../assets/gemsV2.png" alt="GEMS Logo" width="150"/>
  </a>
</div>

# Data Series

Data series provide the numerical input data for time-varying and scenario-varying parameters and they are stored in `csv` files.

The filename (without extension) serves as the `id` of the data series. For instance, a file named `demand_profile.csv` defines a data series with the `id` `demand_profile`. This `id` is what users would use in the system file to instantiate parameter values.

All cell values are **floating-point numbers**. Values are whitespace-separated (spaces or tabs); no header row should be present.

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

This would indicate the parameter’s value in scenario 1 is 10, scenario 2 is 22, and scenario 3 is 55.

## Time-and-scenario-dependent series

Represent data that varies across both time and scenarios (a different time series for each scenario). The file in this case would be a matrix with rows corresponding to time steps and columns corresponding to scenarios. For example, if there are 3 scenarios and 2 time steps (for simplicity), a file could look like:

```text
10 22 55
45 89 33
```

Here, the first row contains the values at time-step 0 for scenarios 1, 2, 3 respectively, and the second row contains the values at time-step 1 for scenarios 1, 2, 3.

## Set-indexed series

!!! warning "Design proposal — not yet implemented"
    This section describes a **proposed** extension to the data-series format, part of the
    [Custom Sets and Indexing](../mathematical-syntax.md#custom-sets-and-indexing-proposed) proposal.
    It is not yet implemented in [GemsPy](../../index.md).

A parameter declared `indexed-by` a [custom set](./library.md#sets) — whether a local (model-level)
or [global (library-level)](./library.md#library-level-sets) set — cannot use the positional matrix
formats above: a third (or later) dimension cannot be expressed by shape alone without an arbitrary
stacking convention, and an enumerated set's elements are *named*, not positional, so a plain matrix
cannot carry their names. Such parameters instead use a **tidy/long CSV format, with a header row**
— unlike every other data series, which has no header:

```csv
segment,time,scenario,value
0,0,0,10.4
0,0,1,11.0
1,0,0,20.0
```

Only the columns that actually apply to the parameter appear. A `segment`-indexed parameter that is
neither time- nor scenario-dependent is simply:

```csv
segment,value
0,10.0
1,25.0
2,60.0
```

For a parameter indexed by an enumerated set, the column holds element names instead of integer
positions:

```csv
fuel,value
gas,42.0
coal,55.0
```

For a parameter indexed by more than one set (`indexed-by: [segment, fuel]`), one column per set
appears, each named after its set `id`:

```csv
segment,fuel,value
0,gas,10.0
0,coal,12.0
1,gas,20.0
```

