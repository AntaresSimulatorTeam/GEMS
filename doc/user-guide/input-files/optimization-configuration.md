# Optimization Configuration File

The `optim-config.yml` file defines the resolution strategy and execution scope of a GEMS study. It is placed at `input/optim-config.yml` inside the study directory.

This file is **optional**. If users don't mention it, default values apply and the study runs in frontal mode over scenario `0`.

It controls:

- the **time scope** and **scenario scope** of the simulation
- the **solver** used to solve the optimisation problem
- the **resolution strategy**: how the optimisation horizon is decomposed (frontal, sequential blocks, parallel blocks, or Benders decomposition for investment studies)
- **per-model settings**: out-of-bounds time handling and decomposition assignment



## Structure of the Optimisation Configuration File

### (optional) Time Scope

The `time-scope` section determines which time indices are considered in the simulation. 

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `first-time-step` | Integer | `0` | First time step index |
| `last-time-step` | Integer | `0` | Last time step index  |


### (optional) Scenario Scope

The `scenario-scope` key defines which Monte Carlo scenarios are executed. When absent, only scenario `0` is run. Two forms are mutually exclusive:

**Inline form** — list scenario indices directly:

| Field | Type | Description |
|-------|------|-------------|
| `scenario-scope.include` | List of integers or ranges (e.g. `"0-9"`) | Scenarios to run |
| `scenario-scope.exclude` | List of integers | (optional) Scenarios to remove from `include` |

**Playlist-file form** — reference an external JSON file (flat array of indices):

| Field | Type | Description |
|-------|------|-------------|
| `scenario-scope.playlist-file` | Path | JSON file containing scenario indices |
| `scenario-scope.exclude` | List of integers | (optional) Scenarios to further filter from the playlist |

Example of scenario-scope configuration
```yaml
scenario-scope:
  playlist-file: mc_playlist.json
  exclude:
    - 1
    - "3-4"
```
Example of `mc_playlist.json`
```yaml
[0, 1, 2, 3, 4, 5]
```


### (optional) Resolution Strategy

This section sets the resolution mode of the optimisation.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `resolution-mode` | String | `frontal` | Decomposition strategy: `frontal`, `sequential-subproblems`, `parallel-subproblems`, `benders-decomposition` |
| `block-length` | Integer | None | Number of time steps per optimisation block (not required for `frontal mode`) |
| `block-overlap` | Integer | `0` | Overlap time steps between consecutive blocks |

Explanations of the different resolution modes:
| Mode | Description |
|------|-------------|
| `frontal` | Entire horizon solved as a single LP |
| `sequential-subproblems` | Consecutive windows solved sequentially; state carried over between blocks |
| `parallel-subproblems` | Independent blocks that can be solved in parallel |
| `benders-decomposition` | Investment (master) separated from operation (subproblems) — required for investment studies |

### (optional) Solver

The `solver` section allows you to select the (MI)LP used for the resolution and declare its settings.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `solver.name` | String | `highs` | Solver name between :`highs`, `xpress`, `gurobi` |
| `solver.logs` | Boolean | `false` | Enable solver output in logs |
| `solver.parameters` | String | None | Space-separated `key=value` pairs passed to the solver |

### (optional) Per-Model Configuration

The `models` section is dedicated to advanced settings of models. For a list of models designated by their `id`, the following collections can be declared:
- `out-of-bounds-processing`: management of temporal block boundaries for time shift operators,
- `decomposition`: management the master/subproblem partition for Benders decomposition,
- `heuristics.integer-strategy`: declaration of the integer resolution mode.

#### Out-of-Bounds Processing 

This section declares how temporal block boundaries are handled:

| Field | Type | Default | Description | 
|-------|------|---------|-------------| 
| `out-of-bounds-processing.constraints[].mode` | String | `cyclic` | How to handle time-shifted references at block boundaries: `cyclic` (wrap around) or `drop` (skip constraint) | 
 
- **`cyclic`** : the out-of-range index is wrapped to the opposite end of the block (e.g. `t-1` at step `0` becomes the last step)

- **`drop`** : the constraint is omitted entirely for the affected time step. 

#### Decomposition 

(Benders resolution mode only) This section specifies how a model's variables, constraints, and objective contributions are dispatched among subproblems, master, and master-and-subproblems.

| Field | Type | Default | Description | 
|-------|------|---------|-------------| 
| `decomposition` | String | `subproblems` | Benders partition: `subproblems`, `master`, `master-and-subproblems` | 

- **`subproblems`** : the model's variables and constraints appear only in the operational subproblems (e.g. a dispatchable generator). 

- **`master`** : the model appears only in the investment master problem (e.g. a candidate generation cluster). 

- **`master-and-subproblems`** : the model is replicated in both levels, with coupling constraints linking the two. 

#### Integer Strategy 

It sets how integer variables are treated :

| Field | Type | Default | Description | 
|-------|------|---------|-------------| 
| `heuristics.integer-strategy` | String | `exact` | Integer handling: `exact` (MILP), `relaxed` (continuous), `heuristic` (relax then refine) | 

- **`exact`** : integer constraints are enforced strictly (MILP). Produces optimal integer solutions at the cost of higher computational time. 

- **`relaxed`** : integer variables are treated as continuous. 

- **`heuristic`** : the problem is first solved relaxed, then integer variables are fixed to rounded values and the problem is re-solved. 

## Example

This code describes a minimal configuration for a frontal simulation run:

```yaml
# Time range matching a typical weekly optimisation (168 h, 0-based)
first-time-step: 0
last-time-step: 167

# Run over 3 Monte Carlo scenarios
scenario-scope:
  include:
    - "0-2"

solver:
  name: highs
  logs: false

resolution-mode: frontal

# short_term_storage.level_equation references level[t-1].
# At t=0 that is out of bounds; cyclic wraps it to level[167],
# which is pinned by the library's initial_level_constraint.
models:
  - id: antares_legacy_models.short_term_storage
    out-of-bounds-processing:
      constraints:
        - id: level_equation
          mode: cyclic 
```
