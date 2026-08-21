# Simulation Table: abstract definition

The **Simulation Table** is a structured table that contains the values of all 

- [Variables](../input-files/library.md#variables)
- [Constraints](../input-files/library.md#constraints)
- [Port Fields](../input-files/library.md#port-field-definition)
- [Extra Outputs](../input-files/library.md#extra-output)

from the solved [optimization problem](./optimization-problem-files.md). It essentially provides a flat table of the optimization solution, with enough information to identify each value’s context (which component, which variable or other output, which time and scenario). This is the most granular output data that we can think of – it’s meant for analysts or developers who want to examine the full solution or feed it into further processing.

**Contents and Structure**: Each row of the simulation table corresponds to a specific model output at a specific index. The table includes the following columns (as `csv` header):

| Column | Description |
|------|--------------------------|
| `block`| The time block number (if the simulation was run in chunks or rolling horizon blocks; otherwise often 1 for the whole horizon).|
| `component` | The component `id` to which this result pertains. Currently, all variables and constraints from all components are exported.|
|`output`| The name of the output within that component. Typically this is the `id` of a decision variable, constraint identifiers and extra outputs with their values or status.|
|`absolute_time_index`|The time step index (1-indexed) from the start of the simulation period. For example, 1 = first hour, 24 = 24th hour, etc. Note: this is 1-based, whereas time indexing in input data series files is 0-based (first row = time step 0).|
|`block_time_index`| The time index within the current block (if using multi-block simulation). In a single-block (full horizon) run, this will be the same as the absolute index|
|`scenario_index`| The scenario number for this entry. If multiple Monte Carlo scenarios were run, this distinguishes them.|
|`value`|The value of the output (variable). None for constraints.|
|`basis_status`| The status in the solver basis for this variable or constraint. Possible values are, *Free*, *At lower bound*, *At upper bound*, *Fixed value*, *Basic*, *None (not available or not applicable)*|

!!! warning "Design proposal — not yet implemented"
    The two columns below are part of the
    [Custom Sets and Indexing](../mathematical-syntax.md#custom-sets-and-indexing-proposed) design
    proposal. They are not yet implemented in [GemsPy](../../index.md).

| Column | Description |
|------|--------------------------|
|`set_id`| Blank for outputs with no [custom-set](../file-structure/library.md#sets) dimension. Otherwise, the `id` of the set this output is indexed by — a local (model-level) or [global (library-level)](../file-structure/library.md#library-level-sets) set, encoded identically either way. For an output indexed by more than one set (e.g. `X{segment, fuel}`), a pipe-joined list in declaration order, e.g. `segment\|fuel`.|
|`set_index`| Blank when `set_id` is blank. Otherwise, the element value for that row, exactly as instantiated in `system.yml` — an integer position for a range-instantiated set, or the element name for a name-instantiated set. For a multi-set output, a pipe-joined list in the same order as `set_id`, e.g. `1\|gas`.|

!!! warning "Design proposal — not yet implemented"
    The two columns below are part of the
    [Custom Sets and Indexing](../mathematical-syntax.md#custom-sets-and-indexing-proposed) design
    proposal. They are not yet implemented in [GemsPy](../../index.md).

| Column | Description |
|------|--------------------------|
|`set_id`| Blank for outputs with no [custom-set](../file-structure/library.md#sets) dimension. Otherwise, the `id` of the set this output is indexed by — a local (model-level) or [global (library-level)](../file-structure/library.md#library-level-sets) set, encoded identically either way. For an output indexed by more than one set (e.g. `X{segment, fuel}`), a pipe-joined list in declaration order, e.g. `segment\|fuel`.|
|`set_index`| Blank when `set_id` is blank. Otherwise, the element value for that row, exactly as instantiated in `system.yml` — an integer position for a range-instantiated set, or the element name for a name-instantiated set. For a multi-set output, a pipe-joined list in the same order as `set_id`, e.g. `1\|gas`.|

## Simulation Table exported by [Antares Simulator](../../overview/gems-interpreters/antares-simulator.md)

[Antares Simulator](../../overview/gems-interpreters/antares-simulator.md) exports the **Simulation Table** as a .csv file. The `csv` file is named `simulation_table--{timestamp}.csv` (e.g. `simulation_table--20251223-1015.csv`) to distinguish runs. By default, the file will reside in the study’s output directory (`outputs/simulation_table--{timestamp}.csv`).

**Example:** To illustrate, here are a couple of rows from a simulation table:

```csv
block,component,output,absolute_time_index,block_time_index,scenario_index,value,basis_status
1,GENERATOR,max_p,1,1,1,5900,Basic
1,GENERATOR,constraint_1,1,1,1,,At lower bound
```

Once [Custom Sets and Indexing](../mathematical-syntax.md#custom-sets-and-indexing-proposed) is
implemented, a set-indexed output would add the two proposed columns, e.g.:

```csv
block,component,output,absolute_time_index,block_time_index,scenario_index,set_id,set_index,value,basis_status
1,STORAGE,segment_level,1,1,1,segment,1,120.0,Basic
```

An output indexed by more than one set pipe-joins both `set_id` and `set_index`, e.g. a
`segment_fuel_cost` output indexed by `{segment, fuel}`:

```csv
block,component,output,absolute_time_index,block_time_index,scenario_index,set_id,set_index,value,basis_status
1,GENERATOR,segment_fuel_cost,1,1,1,segment|fuel,1|gas,55.0,Basic
```

