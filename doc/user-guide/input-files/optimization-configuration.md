# Optimization Configuration File

The `optim-config.yml` file declares **how** a GEMS study is solved: which time steps and
Monte-Carlo scenarios are simulated, which solver is called, how the optimization horizon is
decomposed into subproblems, and how individual models behave at the boundaries of those
subproblems.

It sits next to the other input files, at `input/optim-config.yml`:

```text
my_study/
├── parameters.yml
└── input/
    ├── system.yml
    ├── optim-config.yml      ← this file
    ├── model-libraries/
    └── data-series/
```

The file describes the **resolution strategy only**. It never changes what is modeled: the
components, their parameters and their connections all live in the
[system file](system.md), and their equations in the [model libraries](library.md).
The same system can therefore be solved several ways by editing this file alone.

The file itself is optional, and so is every section within it: when a key is absent it falls
back to the default given in its table below, so a study needs to declare only what it changes.

!!! warning "Language reference, not an interpreter reference"
    This page documents `optim-config.yml` as defined by the **latest design of the GEMS
    language**. Not every feature described here is necessarily supported by every interpreter.
    Refer to the documentation of the interpreter you are running to know which features it
    supports.

## Top-level keys

| Key | Type | Purpose |
|---|---|---|
| [`time-scope`](#time-scope) | Mapping | The range of time steps to simulate |
| [`scenario-scope`](#scenario-scope) | Mapping | The Monte-Carlo scenarios to simulate |
| [`solver-options`](#solver-options) | Mapping | Which (MI)LP solver to call, and how |
| [`resolution`](#resolution) | Mapping | How the horizon is decomposed into optimization subproblems |
| [`models`](#models) | List of mappings | Per-model settings: boundary handling and Benders decomposition |

A complete file, showing every section at once:

```yaml
time-scope:
  first-time-step: 0
  last-time-step: 8759          # 8760 hourly time steps: one year

scenario-scope:
  include:
    - "0-9"                     # ten Monte-Carlo scenarios, 0 through 9

solver-options:
  name: highs
  logs: false
  parameters: "THREADS 4"

resolution:
  mode: sequential-subproblems
  block-length: 168             # one week per subproblem
  block-overlap: 24             # consecutive blocks share one day
  carry-over-length: 24         # the whole shared day is fixed to the previous block's solution

models:
  - id: antares_legacy_models.short_term_storage
    out-of-bounds-processing:
      constraints:
        - id: level_equation
          mode: cyclic
```

---

## `time-scope`

Selects the range of time steps to simulate. Both bounds are **0-based and inclusive**, so the
number of time steps solved is `last-time-step − first-time-step + 1`.

| Key | Type | Default | Description |
|---|---|---|---|
| `first-time-step` | Integer | `0` | Index of the first simulated time step |
| `last-time-step` | Integer | `0` | Index of the last simulated time step |

```yaml
time-scope:
  first-time-step: 0
  last-time-step: 167     # 168 time steps: one week at hourly resolution
```

The range must be covered by the [data series](data-series.md) feeding every time-dependent
parameter of the study.

---

## `scenario-scope`

Selects which Monte-Carlo scenarios are simulated. Scenario indices are **0-based**, matching
the convention of the [scenario builder file](scenario-builder.md).

The base set of scenarios is given by exactly one of two mutually exclusive keys — `include`
(written inline) or `playlist-file` (read from a JSON file). `exclude` is optional and can be
combined with either.

| Key | Type | Default | Description |
|---|---|---|---|
| `include` | List of entries | — | The scenarios to simulate. Mutually exclusive with `playlist-file` |
| `playlist-file` | Path | — | A JSON file listing the scenarios to simulate. Mutually exclusive with `include` |
| `exclude` | List of entries | — | Scenarios removed from the base set |

Each entry of `include` and `exclude` is one of:

| Entry form | Example | Meaning |
|---|---|---|
| Integer | `5` | Scenario 5 |
| Quoted integer | `"5"` | Scenario 5 — identical to `5` |
| Quoted range | `"0-9"` | Scenarios 0 to 9 inclusive (ten scenarios) |

### Inline form

```yaml
scenario-scope:
  include:
    - "0-19"
    - "49-59"
  exclude:
    - 9
    - 14
```

This simulates scenarios 0–19 and 49–59, minus 9 and 14 — 30 scenarios in total.

### Playlist-file form

When the scenario list is long or produced programmatically, keep it in a separate JSON file.
The path is resolved relative to `optim-config.yml`.

```yaml
scenario-scope:
  playlist-file: mc_playlist.json
  exclude:
    - 4
    - "8-10"
```

The referenced file holds a flat JSON array of non-negative integers:

```json
[0, 2, 4, 6, 8, 10, 12]
```

Combining `playlist-file` with `exclude` lets you drop a few scenarios for one run without
editing the playlist itself.

!!! info "Rules"
    - All indices must be greater than or equal to `0`.
    - Duplicates are removed and the resulting set is sorted in ascending order.
    - An `exclude` entry that is not in the base set is ignored, with a warning.
    - `exclude` cannot be used on its own: it requires `include` or `playlist-file`.
    - When `scenario-scope` is omitted, scenario `0` alone is simulated.
    - When a [scenario builder file](scenario-builder.md) is present, every selected index must
      be defined for every scenario group it declares.

---

## `solver-options`

Selects the (MI)LP solver and how it is driven.

| Key | Type | Default | Description |
|---|---|---|---|
| `name` | String | `highs` | Solver to call — for example `highs`, `xpress` or `gurobi` |
| `logs` | Boolean | `false` | Print the solver's own output |
| `parameters` | String | `""` | Solver-specific options, forwarded as-is |

`parameters` is a single string holding an **even number of whitespace-separated tokens**, read
as alternating names and values. Values that look numeric are converted to numbers; everything
else is passed through as text. Both the option names and their accepted values are defined by
the solver, not by GEMS.

```yaml
solver-options:
  name: xpress
  logs: true
  parameters: "THREADS 1 MAXTIME 300"   # THREADS = 1, MAXTIME = 300
```

---

## `resolution`

Selects how the time horizon defined by [`time-scope`](#time-scope) is turned into one or more
optimization problems. This is the single most consequential choice in the file: it governs
solving time, memory use, and whether the result is a global optimum.

| Key | Type | Default | Description |
|---|---|---|---|
| `mode` | String | `frontal` | `frontal`, `sequential-subproblems`, `parallel-subproblems` or `benders-decomposition` |
| `block-length` | Integer | — | Number of time steps per block. **Required** for `sequential-subproblems` and `parallel-subproblems`; not used by the other modes |
| `block-overlap` | Integer | `0` | Number of time steps shared by two consecutive blocks. `sequential-subproblems` only; must satisfy `0 ≤ block-overlap < block-length` |
| `carry-over-length` | Integer | `block-overlap` | How many of the shared time steps are fixed to the previous block's solution. `sequential-subproblems` only; must satisfy `0 ≤ carry-over-length ≤ block-overlap` |

`block-overlap` and `carry-over-length` describe how consecutive blocks are stitched together,
which only happens in `sequential-subproblems`. Declaring either one in any other mode is an
error rather than a silently ignored key — including an explicit `block-overlap: 0`.

### `frontal`

The whole horizon is built as a **single optimization problem** and solved in one call.

```yaml
resolution:
  mode: frontal
```

This is the only mode that gives a globally optimal solution over the full horizon with no
approximation, and the only one where inter-temporal constraints — storage cycles, minimum up
and down durations — are enforced end to end without any boundary treatment. Its cost is size:
the problem must fit in memory as a whole, which becomes the limiting factor on long horizons
with many scenarios.

### `sequential-subproblems`

The horizon is cut into blocks of `block-length` time steps, solved **one after another** in
chronological order. Each block starts `block-length − block-overlap` time steps after the
previous one, so consecutive blocks share `block-overlap` time steps. Of those shared time
steps, the first `carry-over-length` are **fixed** to the values the previous block computed for
the same absolute time steps; the rest are re-optimized freely.

```yaml
resolution:
  mode: sequential-subproblems
  block-length: 168        # one week
  block-overlap: 24        # sharing one day with the previous week
  carry-over-length: 24    # optional; defaults to block-overlap
```

The three parameters, on a small example (`block-length: 10`, `block-overlap: 4`,
`carry-over-length: 3`):

```text
absolute t   0   1   2   3   4   5   6   7   8   9   10  11  12  13  14  15

block N      0   1   2   3   4   5   6   7   8   9
             └───────────── block-length = 10 ─────┘

block N+1                            0   1   2   3   4   5   6   7   8   9
                                     └───────────── block-length = 10 ─────┘

                                     ├───────────┤  block-overlap = 4
                                                    (t = 6..9 belong to both blocks)
                                     ├───────┤      carry-over-length = 3
                                                    (t = 6..8 fixed to block N's values)
                                                 ↑  t = 9 is shared but re-optimized in N+1
```

- **`block-overlap`** gives block *N+1* real history for its lag-dependent constraints: at its
  first time steps, expressions such as `level[t-1]` or a minimum up duration spanning several
  hours have actual preceding time steps to refer to, instead of a block boundary.
- **`carry-over-length`** decides how much of that shared window block *N+1* is allowed to
  revise. Fixing all of it (the default) means the previous block's decisions are final; fixing
  none of it lets each block re-optimize the whole overlap with more look-ahead, in the spirit of
  a receding-horizon controller.

Two values deserve to be spelled out:

- **Omitting `carry-over-length`** resolves it to `block-overlap`: the entire shared window is
  fixed. This is the right default when the overlap exists only to supply history.
- **`carry-over-length: 0`** is legal and different from omitting the key: the blocks still
  overlap — so lag-dependent constraints keep their history — but nothing is fixed, and block
  *N+1* re-solves the shared window on its own.

!!! note "What carry-over does and does not do"
    Carry-over is plain variable fixing: every time-dependent variable of every model whose
    block-relative index falls in the carried-over window is fixed to the value the previous
    block gave it at the same absolute time step. It is not an initial-condition mechanism —
    block *N+1* is not handed the time step preceding its own window, so a `[t-1]` reference at
    its very first time step still resolves against that block's own boundary rule
    (see [`out-of-bounds-processing`](#out-of-bounds-processing)).

    **Time-independent variables are never carried over.** Nothing links their value from one
    block to the next, so each block would size them on its own. `sequential-subproblems` is
    therefore unsuited to investment problems; use [`frontal`](#frontal) or
    [`benders-decomposition`](#benders-decomposition) for those.

Shared time steps appear once per block in the results, tagged by block, so nothing is merged
or lost.

### `parallel-subproblems`

The horizon is cut into **independent** blocks of `block-length` time steps, which can be solved
concurrently.

```yaml
resolution:
  mode: parallel-subproblems
  block-length: 168
```

Nothing links one block to the next: no overlap, no carry-over, no shared state. This is the
fastest mode for horizons whose blocks are genuinely independent — or where the coupling between
them is weak enough to be neglected. Where inter-temporal dynamics matter across block
boundaries, `sequential-subproblems` reproduces them and this mode does not.

### `benders-decomposition`

The problem is split along a different axis: **investment decisions on one side, operation on
the other**. A *master problem* holds the time-independent investment variables; *subproblems*
hold operation, one per scenario and time block. Master and subproblems are solved alternately,
the subproblems returning Benders cuts that progressively shape the master's cost function,
until the two converge.

```yaml
resolution:
  mode: benders-decomposition
```

Use it for investment studies: it lets a single set of sizing decisions be optimized against
many operational scenarios without ever assembling all of them into one problem. Which model
element goes to which side is declared per model, in
[`model-decomposition`](#model-decomposition).

!!! warning
    Under `benders-decomposition`, subproblems must be continuous: no integer or binary variable
    may end up on the subproblem side.

---

## `models`

The `models` key holds a **list of per-model settings**. Everything above applies to the study as
a whole; this section is where individual models are given special treatment.

```yaml
models:
  - id: <library-id>.<model-id>        # which model these settings apply to
    out-of-bounds-processing: {...}    # optional
    model-decomposition: {...}         # optional
```

| Key | Type | Required | Description |
|---|---|---|---|
| `id` | String | Yes | The **fully qualified model id**, `<library-id>.<model-id>` |
| [`out-of-bounds-processing`](#out-of-bounds-processing) | Mapping | No | How the model's constraints behave at block boundaries |
| [`model-decomposition`](#model-decomposition) | Mapping | No | Where the model's elements go under Benders decomposition |

Four points about how this list is matched:

- **Entries target models, not components.** `id` is the identifier of a model defined in a
  [model library](library.md), qualified by that library's id — the same string a component uses
  in its `model:` field in the [system file](system.md). It is *not* a component id.
- **Settings apply to every component built from that model.** Declaring
  `antares_legacy_models.short_term_storage` configures all storage components of the study at
  once. There is no per-component override.
- **Each entry must name a model actually used by the system**, and every constraint, variable
  or objective contribution it refers to must exist in that model. Any mismatch — a model no
  component instantiates, a misspelled constraint id — is reported as an error before solving.
- **Everything unlisted keeps its default.** Models absent from the list, and elements absent
  from an entry, behave as described in the two sections below. A model can declare
  `out-of-bounds-processing`, `model-decomposition`, or both; the two are independent.

Order does not matter, but each model should appear at most once.

### `out-of-bounds-processing`

A constraint may refer to a time step other than the current one, through a
[relative time shift](../syntax.md#relative-shift-tn-t-n) such as `level[t-1]`, or a
[relative time sum](../syntax.md#time-summation-range-sums-e-x). Near the edges of an
optimization block, those references point **outside the block** — `level[t-1]` at the first
time step, `generation[t+1]` at the last one. This section declares what happens then.

```yaml
models:
  - id: antares_legacy_models.short_term_storage
    out-of-bounds-processing:
      constraints:
        - id: level_equation
          mode: cyclic
```

`constraints` is a list of `{id, mode}` pairs. Each `id` names a constraint of the model, and
`mode` is mandatory for every listed constraint:

| `mode` | Behavior at a boundary |
|---|---|
| `cyclic` | The out-of-range index wraps around to the other end of the block: at the first time step, `[t-1]` reads the block's last time step |
| `drop` | The constraint is not generated for the time steps whose references fall outside the block; it still applies everywhere else |

**`cyclic` is the default** — a constraint not listed here, and a model not listed in `models` at
all, wraps around. Listing a constraint with `mode: cyclic` is therefore a way of making that
choice explicit in the file.

Two aspects are worth keeping in mind:

- **The boundary is the block's, not the horizon's.** In [`frontal`](#frontal) mode the block is
  the whole horizon, so wrapping links its last time step to its first. In the windowed modes
  each block wraps or drops on its own edges, and `block-overlap` is what lets a sequential block
  reach real history instead of hitting its own boundary.
- **`drop` removes constraint instances, not the constraint.** Only the affected time steps lose
  it. It applies per component, since a shift amount may be a parameter with a different value on
  each component. For that reason, a dropped constraint's shift amounts and time-sum bounds must
  be constants or parameter references — a shift that depends on a variable cannot be checked
  against the block boundary.

Which mode to pick follows from what the constraint means:

- `cyclic` suits a quantity that is expected to return to its starting point over the block — a
  storage level over a representative week, for instance, where wrapping enforces exactly that
  closure.
- `drop` suits a constraint that has no meaning before the block starts — a start-up or minimum
  up-duration constraint whose history is genuinely unknown at the first time step, where
  wrapping would invent a spurious link between the end and the start of the block.

The model library often settles the question. `antares_legacy_models.short_term_storage`, for
example, declares both `level_equation` (`level = level[t-1] + …`) and an
`initial_level_constraint` pinning the level at the end of the week: `cyclic` on
`level_equation` closes the loop consistently with that target, whereas `drop` would leave the
first time step's level unconstrained.

### `model-decomposition`

Under [`benders-decomposition`](#benders-decomposition), each element of a model has to end up
on one side of the master/subproblem split. This section declares that placement explicitly,
overriding the defaults. It is read only in `benders-decomposition` mode.

```yaml
models:
  - id: investment_library.candidate_generator
    model-decomposition:
      variables:
        - id: p_installed
          location: master-and-subproblems
      objective-contributions:
        - id: investment_cost_installation
          location: master
        - id: expected_operating_cost
          location: subproblems
```

The mapping holds up to three lists — `variables`, `constraints` and
`objective-contributions` — each a list of `{id, location}` pairs naming an element of the model:

| Key | Type | Description |
|---|---|---|
| `variables` | List of `{id, location}` | Placement of the model's variables |
| `constraints` | List of `{id, location}` | Placement of the model's constraints and binding constraints |
| `objective-contributions` | List of `{id, location}` | Placement of the model's objective contributions |

`location` takes one of three values:

| `location` | Meaning |
|---|---|
| `subproblems` | The element exists in each operational subproblem only — the **default** for anything not listed |
| `master` | The element exists in the investment master problem only |
| `master-and-subproblems` | A **coupling** element: decided in the master problem, then used by the subproblems as a fixed input |

The typical investment model uses all three. Its sizing variable is `master-and-subproblems` —
the master chooses the installed capacity, and each subproblem operates against that value. Its
annualized investment cost is `master`, since it depends only on the sizing decision. Its
operating cost, and the operational constraints that bound generation by installed capacity, stay
in `subproblems`.

!!! info "Validation rules"
    - **A variable placed in `master` or `master-and-subproblems` must be time-independent.**
      Investment decisions are taken once for the whole horizon; a time-dependent variable cannot
      be a master variable.
    - **Constraints and objective contributions placed in `master` may only reference variables
      placed in `master` or `master-and-subproblems`.** The master problem has no access to
      operational variables.
    - Under `benders-decomposition`, no integer or binary variable may remain on the subproblem
      side.

    These rules are checked against the model libraries before solving, and every violation is
    reported at once.

---

## Examples

=== "Frontal"

    The default strategy, and the reference every other mode is approximated against: one week
    at hourly resolution, three scenarios, solved as a single problem.

    ```yaml
    time-scope:
      first-time-step: 0
      last-time-step: 167          # 168 hourly time steps

    scenario-scope:
      include:
        - "0-2"                    # scenarios 0, 1 and 2

    solver-options:
      name: highs
      logs: false

    resolution:
      mode: frontal

    # level_equation reads level[t-1]; at the first time step of the horizon that index is
    # out of bounds. Wrapping it to the last time step closes the storage cycle over the week,
    # consistently with the library's initial_level_constraint on level[167].
    models:
      - id: antares_legacy_models.short_term_storage
        out-of-bounds-processing:
          constraints:
            - id: level_equation
              mode: cyclic
    ```

=== "Sequential"

    A rolling horizon over a full year: 52 weekly blocks solved in order, each one reaching one
    day back into the previous week. The whole shared day is fixed to the previous block's
    solution, so each week's decisions are final once taken.

    ```yaml
    time-scope:
      first-time-step: 0
      last-time-step: 8759         # 8760 hourly time steps: one year

    scenario-scope:
      include:
        - 0

    resolution:
      mode: sequential-subproblems
      block-length: 168            # one week per block
      block-overlap: 24            # each block reaches one day into the previous one
      carry-over-length: 24        # that whole day is fixed to the previous block's values

    # The overlap already gives level_equation a real level[t-1] inside each block, except at
    # the very first one. Dropping the constraint at boundary time steps avoids wrapping a
    # weekly block's level onto itself, which would be meaningless mid-year.
    models:
      - id: antares_legacy_models.short_term_storage
        out-of-bounds-processing:
          constraints:
            - id: level_equation
              mode: drop
    ```

    Setting `carry-over-length: 0` instead would keep the same overlap — so the same history for
    `level[t-1]` — while letting each block re-optimize the shared day with a full week of
    look-ahead.

=== "Parallel"

    Independent blocks, solved concurrently. Here a year is cut into 52 self-contained weeks:
    each one closes its own storage cycle, which is what makes them independent in the first
    place.

    ```yaml
    time-scope:
      first-time-step: 0
      last-time-step: 8759

    scenario-scope:
      playlist-file: mc_playlist.json    # scenario list kept in a separate JSON file
      exclude:
        - 7                              # scenario 7 dropped for this run

    resolution:
      mode: parallel-subproblems
      block-length: 168                  # one independent week per block
      # block-overlap and carry-over-length do not apply here and would be rejected

    models:
      - id: antares_legacy_models.short_term_storage
        out-of-bounds-processing:
          constraints:
            - id: level_equation
              mode: cyclic               # each week closes its own storage cycle
    ```

=== "Investment (Benders)"

    An investment study over ten scenarios, using the `candidate_generator` and
    `candidate_storage` models of the
    [investment tutorial](../../examples/notebooks/tutorial-three-investment/tutorial-invest.ipynb).
    Both candidates are sized once, by the master problem, and operated in every scenario's
    subproblem.

    ```yaml
    time-scope:
      first-time-step: 0
      last-time-step: 167

    scenario-scope:
      include:
        - "0-9"                    # ten scenarios sharing one investment decision

    resolution:
      mode: benders-decomposition

    models:
      - id: investment_library.candidate_generator
        model-decomposition:
          variables:
            # Installed capacity is chosen once by the master and used by every subproblem.
            - id: p_installed
              location: master-and-subproblems
            # generation is time-dependent and stays in the subproblems (default).
          objective-contributions:
            - id: investment_cost_installation
              location: master
            - id: expected_operating_cost
              location: subproblems
          # capacity_limit (generation <= p_installed) stays in the subproblems (default):
          # it bounds an operational variable, using the capacity fixed by the master.

      - id: investment_library.candidate_storage
        model-decomposition:
          variables:
            - id: p_installed
              location: master-and-subproblems
          objective-contributions:
            - id: investment_cost_installation
              location: master
        # level_equation reads level[t+1], out of bounds at the last time step. Dropping it
        # there leaves the final level free, as intended: the level is pinned at the start of
        # the horizon by initial_level_constraint, not at its end.
        out-of-bounds-processing:
          constraints:
            - id: level_equation
              mode: drop
    ```

    Note how the two per-model sections combine on `candidate_storage`: `model-decomposition`
    splits it across the two levels, while `out-of-bounds-processing` governs its behavior at
    the horizon's edges. Both are optional and independent of each other.
