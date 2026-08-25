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

The `time-scope` section configures the time index. If it's unconfigured, default values are taken into account.

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

### (optional) Solver

This `solver` part chooses the solver parameters.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `solver.name` | String | `highs` | Solver name between :`highs`, `xpress`, `gurobi` |
| `solver.logs` | Boolean | `false` | Enable solver output in logs |
| `solver.parameters` | String | None | Space-separated `key=value` pairs passed to the solver |


### (optional) Resolution Strategy

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


### (optional) Per-Model Configuration

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `out-of-bounds-processing.constraints[].mode` | String | `cyclic` | How to handle time-shifted references at block boundaries: `cyclic` (wrap around) or `drop` (skip constraint) |
| `decomposition` | String | `subproblems` | Benders partition: `subproblems`, `master`, `master-and-subproblems` |
| `heuristics.integer-strategy` | String | `exact` | Integer handling: `exact` (MILP), `relaxed` (continuous), `heuristic` (relax then refine) |

## Example

This code describe a minimal configuration for a frontal simulation run:

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