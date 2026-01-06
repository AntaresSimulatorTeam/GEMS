<div style="display: flex; justify-content: space-between; align-items: center;">
  <div style="text-align: left;">
    <a href="../../../..">Main Section</a>
  </div>
  <div style="text-align: right;">
    <img src="../../assets/gemsV2.png" alt="GEMS Logo" width="150"/>
  </div>
</div>

# Simulation and Optimization Parameters

Global simulation and optimization parameters are defined in the `parameters.yml` file located at the **root of the study directory**.

The `parameters.yml` file is only required when using the **Antares Modeler interpreter**.  
When other interpreters or programmatic APIs are used, these parameters may be provided through alternative configuration mechanisms or default settings.

This file controls:

- solver selection and behaviour
- simulation horizon definition
- output generation options

---

## Solver Configuration

### `solver`

| Field | Description |
|-----|------------|
| **Type** | String |
| **Expected values** | `sirius` (LP only), `scip` (MIP only), `coin`, `xpress`, `glpk` (Linux only), `highs`, `pdlp` (LP only) |
| **Required** | No |
| **Default** | `sirius` |
| **Usage** | Selects the optimisation solver used to solve the generated problem |

---

### `solver-logs`

| Field | Description |
|-----|------------|
| **Type** | Boolean |
| **Expected values** | `true` / `false` |
| **Required** | No |
| **Default** | `false` |
| **Usage** | Enables solver output in logs (useful for debugging and convergence analysis) |

---

### `solver-parameters`

| Field | Description |
|-----|------------|
| **Type** | String |
| **Required** | No |
| **Default** | Empty |
| **Usage** | Solver-specific parameters passed to the underlying [OR-Tools MPSolver](https://developers.google.com/optimization/lp/mpsolver) |

| Supported Solvers | Notes |
|------------------|------|
| `scip` | Supported |
| `xpress` | Supported |
| `pdlp` | Supported |
| Others | Not supported |

**Examples**

| Solver | Example |
|------|--------|
| XPRESS | `THREADS 1 PRESOLVE 1` |
| SCIP | `parallel/maxnthreads 1, lp/presolving TRUE` |

Incorrect or unsupported parameter syntax may be ignored or cause solver errors.

---

## Simulation Horizon

The simulation horizon defines the time steps included in the optimisation.

Both parameters must be consistent with time-dependent data series definitions.

---

### `first-time-step`

| Field | Description |
|-----|------------|
| **Type** | Integer |
| **Expected values** | Non-negative integer (`0` allowed) |
| **Required** | Yes |
| **Usage** | Index of the first time step included in the simulation |

---

### `last-time-step`

| Field | Description |
|-----|------------|
| **Type** | Integer |
| **Expected values** | Non-negative integer (`0` allowed) |
| **Required** | Yes |
| **Usage** | Index of the last time step included in the simulation |

| Horizon Rule |
|-------------|
| Simulation includes all time steps in the interval **[`first-time-step`, `last-time-step`]** |

---

## Output Control

### `no-output`

| Field | Description |
|-----|------------|
| **Type** | Boolean |
| **Expected values** | `true` / `false` |
| **Required** | No |
| **Default** | `false` |
| **Usage** | Controls whether output files are generated at the end of the simulation |

| Value | Effect |
|------|--------|
| `false` | Generate all standard output files |
| `true` | Suppress output generation |

---

## Full Example

```yaml
solver: xpress
solver-logs: false
solver-parameters: THREADS 1

first-time-step: 0
last-time-step: 2

no-output: false
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