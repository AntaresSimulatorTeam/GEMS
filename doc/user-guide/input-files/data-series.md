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

## Set-indexed series

!!! warning "Design proposal — not yet implemented"
    This section describes a **proposed** extension to the data-series format, part of the
    [Custom Sets and Indexing](../syntax.md#custom-sets-and-indexing-proposed) proposal.
    It is not yet implemented in [GemsPy](../../index.md).

**Backward compatibility:** this section is purely additive. A parameter that does not declare
`indexed-by` is entirely unaffected — it continues to use one of the three existing headerless matrix
formats above ([Time-dependent](#time-dependent-series), [Scenario-dependent](#scenario-dependent-series),
or [Time-and-scenario-dependent](#time-and-scenario-dependent-series) series), completely unchanged.
The new tidy/long, headered CSV format below applies exclusively to parameters that declare
`indexed-by`; it is never a replacement for the existing formats, only a new option alongside them.

A parameter declared `indexed-by` a [custom set](./library.md#sets) — whether a local (model-level)
or [global (library-level)](./library.md#library-level-sets) set — cannot use the positional matrix
formats above: a third (or later) dimension cannot be expressed by shape alone without an arbitrary
stacking convention, and a set instantiated with named elements in `system.yml` has *named*, not
positional, elements, so a plain matrix cannot carry their names. Such parameters instead use a
**tidy/long CSV format, with a header row** — unlike every other data series, which has no header:

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

For a parameter indexed by a set `system.yml` instantiated with named elements (an explicit list, e.g.
`elements: [gas, coal, oil]`), the column holds those names instead of integer positions:

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

**Column order:** in the general case — any number of sets, combined with time and/or scenario — the
canonical column order is: sets, in the same order as declared in `indexed-by`, followed by `time`,
then `scenario`, then `value`:

```csv
segment,fuel,time,scenario,value
0,gas,0,0,10.4
0,gas,0,1,11.0
0,coal,0,0,9.2
```

A data-series column's values must match exactly whatever `system.yml` declares for that set —
[Global Sets](./system.md#global-sets) or [Local Sets](./system.md#local-sets) — whether that
instantiation was an explicit list or a range shorthand (a range-instantiated set's column simply
holds the resulting integers); the library/model alone never tells a data-series author the concrete
element list to use, since neither ever gives a set's concrete `elements` itself (see
[library.md's Sets](./library.md#sets)).

