<div style="display: flex; justify-content: space-between; align-items: center;">
    <div style="text-align: left;">
        <a href="../../../..">Main Section</a>
    </div>
    <div style="text-align: right;">
        <img src="../../../assets/gemsV2.png" alt="GEMS Logo" width="150"/>
    </div>
</div>

# Simulation Table: abstract definition

The **Simulation Table** is a structured table that contains the values of all 

- [Variables](../3_GEMS_File_Structure/2_library.md/#variables)
- [Constraints](../3_GEMS_File_Structure/2_library.md/#constraints)
- [Port Fields](../3_GEMS_File_Structure/2_library.md/#port-field-definition)
- [Extra Outputs](../3_GEMS_File_Structure/2_library.md/#extra-output)

from the solved [optimization problem](2_optimization_problem.md). It essentially provides a flat table of the optimization solution, with enough information to identify each value’s context (which component, which variable or other output, which time and scenario). This is the most granular output data that we can think of – it’s meant for analysts or developers who want to examine the full solution or feed it into further processing.

**Contents and Structure**: Each row of the simulation table corresponds to a specific model output at a specific index. The table includes the following columns (as `csv` header):

| Column | Description |
|------|--------------------------|
| `block`| The time block number (if the simulation was run in chunks or rolling horizon blocks; otherwise often 1 for the whole horizon).|
| `component` | The component `id` to which this result pertains. Currently, all variables and constraints from all components are exported.|
|`output`| The name of the output within that component. Typically this is the `id` of a decision variable, constraint identifiers and extra outputs with their values or status.|
|`absolute_time_index`|The time step index (1-indexed) from the start of the simulation period. For example, 1 = first hour, 24 = 24th hour, etc.|
|`block_time_index`| The time index within the current block (if using multi-block simulation). In a single-block (full horizon) run, this will be the same as the absolute index|
|`scenario_index`| The scenario number for this entry. If multiple Monte Carlo scenarios were run, this distinguishes them.|
|`value`|The value of the output (variable). None for constraints.|
|`basis_status`| The status in the solver basis for this variable or constraint. Possible values are, *Free*, *At lower bound*, *At upper bound*, *Fixed value*, *Basic*, *None (not available or not applicable)*|

# Simulation Table exported by [Antares Simulator](../../1_Overview/GEMS_Interpreters/2_antares_simulator_modeler.md)

[Antares Simulator](../../1_Overview/GEMS_Interpreters/2_antares_simulator_modeler.md) exports the **Simulation Table** as a .csv file. The `csv` file is named `simulation_table_{timestamp}.csv` (e.g. `simulation_table_20251223-1015.csv`) to distinguish runs. By default, the file will reside in the study’s output directory (`outputs/simulation_table_{timestamp}.csv`).

**Example:** To illustrate, here are a couple of rows from a simulation table:

```csv
block,component,output,absolute_time_index,block_time_index,scenario_index,value,basis_status
1,GENERATOR,max_p,1,1,1,5900,Basic
1,GENERATOR,constraint_1,1,1,1,,At lower bound
```

**Navigation**

<div style="display: flex; justify-content: space-between;">
  <div style="text-align: left;">
  <button type="button" style="background-color:#CCCCCC; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
    <a href="../../1_Overview/References/4_Users" style="text-decoration:none; color: #000000">⬅️ Previous page</a>
  </button>
  </div>
  <button type="button" style="background-color:#AAAAFF; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
    <a href="../../../.." style="text-decoration:none; color: #FFFFFF">Index</a>
  </button>
  <div style="text-align: right;">
  <button type="button" style="background-color:#CCCCCC; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
    <a href="../1B_gemspy_installation" style="text-decoration:none; color: #000000">Next page ➡️</a>
  </button>
  </div>
</div>

---


© GEMS (LICENSE)