# Data Series

Data series provide the numerical input data for time-varying and scenario-varying parameters and they are stored in `csv` files (or, as [proposed](#parquet-data-series-proposed), in Parquet files).

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


## Parquet data series (Proposed)

!!! warning "Design proposal — not yet implemented"
    This section is a **placeholder** for a proposed extension. It sketches a direction only, and
    most of the design is still open (see the questions below). It is not yet implemented in
    [GemsPy](../../index.md) or Antares Simulator.

Large studies make CSV slow to read and heavy to store. This applies to hourly series over many
scenarios, and above all to [set-indexed series](#set-indexed-series), which can hold hundreds of
millions of values. The idea is to let any data series be stored as an
[Apache Parquet](https://parquet.apache.org/) file instead: a compressed, typed, columnar format,
already used for GEMS outputs. This is the roadmap item
[Parquet data series](../../home/roadmap.md#next).

**Starting point.**

- A data series may be a file `<id>.parquet` instead of `<id>.csv`. It is referenced by the same
  `id` in the [system file](system.md), so a study can switch format without changing `system.yml`.
- Its content follows the long layout of [set-indexed series](#set-indexed-series): one column per
  set in `indexed-by` order, then `time`, `scenario` and `value`, with only the columns that apply
  (see [below](#set-indexed-series-in-parquet)).
- CSV stays fully supported. Parquet is an additional option, never a requirement.

### Set-indexed series in Parquet

[Custom sets](../syntax.md#custom-sets-and-indexing-proposed) are the main reason for this proposal.
The series of a set-indexed parameter has one row per combination of set elements, time step and
scenario, and Parquet compresses such repeated keys well. The rules of
[set-indexed series](#set-indexed-series) carry over:

- **Set columns.** There is one column per set, named after the set `id`, in `indexed-by` order,
  before `time` and `scenario`.
- **Element values.**
  - A column holds the set's **elements as instantiated in `system.yml`**, never their positions.
  - A set instantiated with a range (`0..4`, `2020..2024`) gives an integer column.
  - A set instantiated with names (`[gas, coal, oil]`) gives a string column. Parquet's dictionary
    encoding stores repeated names compactly.
- **Local and global sets.**
  - For a [local set](system.md#local-sets), the rows cover the elements of each component that uses
    the series. Components that instantiate the set differently therefore need different series,
    possibly of different sizes. This holds for CSV as well.
  - For a [global set](system.md#global-sets), every file uses the same study-wide elements.
- **Validation.** As in CSV, element values must match the instantiation exactly. Whether every
  combination must appear exactly once is [open](#open-questions) (question 9).

```text
data-series/
  segment_fuel_cost.parquet   # columns:
                              #   segment: int32    (local set instantiated as 0..2)
                              #   fuel:    string   (global set instantiated as [gas, coal, oil])
                              #   time:    int32
                              #   value:   float64
  load_fr.csv                 # unchanged headerless series
```

### Open questions

1. **Layout.** Should Parquet use only the long layout, or also a wide layout mirroring the
   headerless matrices (one row per time step, one column per scenario)? Wide mirrors the
   existing matrices; long is uniform with set-indexed series. Which is smaller depends on
   compression.
2. **One series per file, or several?** One file per series keeps the `id` = file name rule. A
   multi-series file, with one column per series or a `series` key column, would cut the number of
   files in large studies, but needs a referencing syntax (e.g. `file:column`).
3. **Same `id` in two formats.** If both `<id>.csv` and `<id>.parquet` exist, is that an error, or
   does one take precedence?
4. **Column types.** Which types are accepted for `time` (integer) and `value` (float or integer)?
   Are nulls forbidden, as missing rows already are?
5. **Set element types.** For a set instantiated with an explicit list of numbers
   (`[10, 20, 30]`), should the column be integer or string? Must the column type match the way the
   set is instantiated, or may an interpreter convert it?
6. **Several components in one file.** A `component` key column would let one file hold a parameter
   for all the components of a model, including components that instantiate a local set
   differently. Is this worth a new referencing rule? (This is related to question 2.)
7. **Set instantiations from files.** Large sets, such as a thousand CNEC names, are tedious to list
   in `system.yml`. Should a set's `elements` also be readable from a (Parquet) file?
8. **Scenario column.** Does `scenario` hold the data-series column index used by the
   [scenario builder](scenario-builder.md), as the matrix columns do today? This question is
   inherited from the [set-indexed](#set-indexed-series) CSV format, which does not define it
   either. It should be settled there, for both formats.
9. **Row order and density.** Must every combination of keys appear exactly once? Should rows be
   required in canonical order, so they can be read without sorting? If so, are set columns sorted
   by position in the set or by element value?
10. **Physical options.** Should compression, row-group size or partitioning (for example one file
    per scenario, or per set element) be prescribed, recommended or left free?
11. **Scope.** Should the same format later cover other inputs (for example the scenario builder,
    or connection-weight tables if that proposal is adopted)? Should interpreters be required to
    support it, or may support be optional?
