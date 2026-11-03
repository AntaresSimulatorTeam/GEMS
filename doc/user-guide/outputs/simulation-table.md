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
| `block`| The time block index, starting at 0 (if the simulation was run in chunks or rolling horizon blocks; otherwise 0 for the whole horizon).|
| `component` | The component `id` to which this result pertains. Currently, all variables and constraints from all components are exported.|
|`output`| The name of the output within that component. Typically this is the `id` of a decision variable, constraint identifiers and extra outputs with their values or status.|
|`absolute_time_index`|The time step index (0-indexed) from the start of the simulation period. For example, 0 = first hour, 23 = 24th hour, etc. This is the same indexing as input data series files (first row = time step 0).|
|`block_time_index`| The time index within the current block, starting at 0 (if using multi-block simulation). In a single-block (full horizon) run, this will be the same as the absolute index|
|`scenario_index`| The scenario number for this entry. If multiple Monte Carlo scenarios were run, this distinguishes them.|
|`value`|The value of the output (variable). None for constraints.|
|`basis_status`| The status in the solver basis for this variable or constraint. Possible values are, *Free*, *At lower bound*, *At upper bound*, *Fixed value*, *Basic*, *None (not available or not applicable)*|

??? note "Example of a simulation table"
    Here are a couple of rows from a simulation table:
    ```csv
    block,component,output,absolute_time_index,block_time_index,scenario_index,value,basis_status
    0,generator1,generation,0,0,0,80,Basic
    0,bus_1,balance,0,0,0,None,Fixed value
    ```

## Detailed of the structure

To explore in depth the details of the structure of the simulation table, please see directly the dedicated documentation of the main GEMS interpreters :

* Simulation Table exported by [Antares Simulator](https://antares-simulator.readthedocs.io/en/latest/reference/modeler/03-outputs/#simulation-table)

* Simulation Table exported by [GemsPy](https://gemspy.readthedocs.io/en/latest/user-guide/outputs/)

