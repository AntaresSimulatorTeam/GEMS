---
description: Reference for GEMS mathematical expression syntax — operators, variables, parameters, port fields, linearity conditions, and time and scenario indexing mechanisms.
---

<div style="display: flex; justify-content: flex-end;">
  <a href="../../../..">
    <img src="../../assets/gemsV2.png" alt="GEMS Logo" width="150"/>
  </a>
</div>

# GEMS Mathematical Expression Syntax

[GEMS](../index.md) includes a **Mathematical Expression Syntax** that allows users to write equations for optimization problems in a clear, math-like syntax within specific configuration files. **Mathematical Expression Syntax** is independent of any programming code – model equations are specified as human-readable text, which [GEMS](../index.md) interprets to build the mathematical optimization problem.

This section provides a description of the supported operators, linearity condition, the usage of parameters, variables, and ports in mathematical expressions, and the mechanisms for time and scenario indexing and aggregation.

## Basic Operators

Basic operators can be divided into two groups:

- **Arithmetic Operators**
- **Comparison Operators**

### Arithmetic Operators

Mathematical expressions use standard arithmetic notation. The following binary arithmetic operators are supported:

| Operator | Example |
|------|--------------------------|
| Addition| ```generation + storage``` |
| Subtraction | ```generation - load``` |
| Multiplication | ```generation * generation_cost``` |
| Division |  ```generation / 2``` |

These operate with conventional precedence (multiplication and division bind tighter than addition and subtraction). Parentheses (…) can be used to group parts of an expression to improve readability or to override the normal order of operations.

### Comparison Operators

Comparison operators are used to form constraints (equations or inequalities).

| Operator | Description | Example|
|------|--------------------------| ---------------|
| `=`| Used in constraint definitions to enforce equality  | `expression_1 = expression_2` |
| `<=` | Used in constraints to require `LHS ≤ RHS` |`expression_1 <= expression_2`|
| `>=` | Used in constraints to require `LHS ≥ RHS` | `expression_1 >= expression_2`|

**Important:** Comparison operators are only allowed in constraint expressions (not in general arithmetic expressions). Each constraint expression must contain exactly one comparison operator (`=`, `<=`, or `>=`)
 dividing the expression into a left-hand side (LHS) and right-hand side (RHS). Chained comparisons (e.g. `A <= B <= C`) are not permitted; if needed, break them into separate constraints.

[**GEMS framework**](../index.md) **Mathematical Expression Syntax** does not support certain operations common in programming or math notation. For example, non-linear functions (log, sin, etc.) are not part of the expression syntax. If a mathematical relationship is non-linear, it must be linearized or reformulated.

---

## Numeric Constants (Literals)

Numeric constants can be used anywhere in an expression. Literals may be written as integers or floats (use . for a decimal point). For example, all of the following are valid constants: `42`, `0.5`, `3.14`, `100.0`.

**Example:**

```yaml
expression: 3 * 66.32 - 5 / 3.14
```

## Parameters

Parameters represent fixed input data values that can be referenced by their `id` as a simbol to include it's value in expressions. For example:

```yaml
expression: 3 * parameter_1 + 6.345 / parameter_2
```

This would use the numeric value of `parameter_1` and `parameter_2` as provided in the system input data.

Parameters can be time-dependent (having a separate value for each time step of the simulation horizon) or scenario-dependent (having different values under different scenario cases), or both. If a parameter is time-dependent, think of it as a series $p(t)$ over time; if scenario-dependent, as $p(s)$ varying by scenario; it can even be $p(t,s)$ if varying across both dimensions.

Parameters can be used freely in arithmetic operations. Since parameters are constants from the solver’s perspective (their values are fixed input), they may appear in linear or non-linear positions without violating linearity rules. For instance, multiplying two parameters or dividing by a parameter is allowed. However, dividing by a parameter that could be zero should be avoided, as this would create an undefined expression in some cases.

## Variables

Variables correspond to the decision variables of an optimization problem. All variables are referenced by their `id` in expressions, just like parameters. For example, if a model defines a variable with `id: generation`, it can be used  in an expression as:

```yaml
expression: generation * generation_cost
```

In such use, `generation` represents the variable’s value, and `generation_cost` is a parameter.

Variables can be **continuous**, **integer** or **binary**.

A crucial rule is that all expressions must be linear. This means non-linear combinations of variables are not allowed. Each term in an expression can be at most a variable multiplied by a constant or parameter. The expression cannot include products or divisions where a variable appears in a non-linear way. Violating this will result in an invalid model definition.
Some examples of prohibited expressions (non-linear in variables):

- `variable_a * variable_b` – product of two variables

- `3 / variable_a` – a variable in the denominator (non-linear reciprocal)

- `binary_var * continuous_var` – product of two variables, even if one is binary (still nonlinear)

### Time and Scenario Dependence of Variables

Variables inherently can have a value for each time step (and scenario) unless defined or used in a way that makes them constant. If a variable is time-dependent, it means conceptually there is a vector of that variable across the simulation timeline (e.g. $x_t$ for each hour $t$). Likewise, a scenario-dependent variable has independent values per scenario $s$. The **Mathematical Expression Syntax** does not require writing an index for a time-dependent variable in most cases; instead, the context of the constraint or objective will determine how it’s applied (explained under [**Time Operators**](#time-operators-and-indexing)).

If a variable is time-dependent (or scenario-dependent), it can only be used in a constraint that is also time-dependent (or scenario-dependent), or else aggregated appropriately. In practice, this means if a time-indexed variable is included in an expression, that expression is treated as a separate equation at each time step by default (the interpreter *unfolds* the equation over time). Similarly, scenario-indexed variables lead to constraints unfolding per scenario.

## Ports

Ports are the mechanism by which models exchange mathematical expressions. A port has one or more fields with each field carrying an expression. **Mathematical Expression Syntax**  allows users to reference port fields in expressions using the notation `port_id.field_id`. This is essentially a way to use expressions coming from other connected models.

When using a port field in an expression, the same dependency rules apply: if the expression of a port varies by time or scenario (which is deduced from how it’s defined – typically depending on time-dependent variables or parameters), then it can only be used in time-dependent or scenario-dependent constraints respectively.

If a port’s expressions need to be used in a time-independent manner (for example, when calculating a sum over the full time horizon), an aggregator must be applied to remove the time index. See the section on the [**Time Summation Operator**](#time-summation-full-horizon-sumx) for details. A practical implementation is provided in [`basic_models_library.yml`](https://github.com/AntaresSimulatorTeam/GEMS/blob/main/libraries/basic_models_library.yml) where the `emission_port` is used to support pollutant-related constraints.

### Port Operator

A single port on a model can have multiple connections feeding into it (multiple components can connect to the same port of this component). To aggregate all incoming values of a port field, **Mathematical Expression Syntax**  provides a special operator:

- `sum_connections(port.field)` – this returns the sum of the specified field across all incoming connections to the given port. It effectively adds up the values of that field from every other component connected to the port. The result of `sum_connections` can be used like any other term in an expression. If there are no incoming connections, the sum is simply 0.

Use `sum_connections` in constraints that need the combined effect of multiple inputs. For example, a balance node model might require that the sum of all power flows equals zero (First Kirchhoff Law). Assuming the port is injections and the field is flow, the model’s constraint could be:

```yaml
expression: sum_connections(injections.flow) = 0
```

This constraint will enforce that the total of flow from all connected components on port injections is zero.

### Direct port field usage

Direct usage of a port’s field (e.g. `balance_port.flow`) inside a constraint is not permitted in [GEMS](../index.md). Any attempt to reference a port field directly in a constraint will result in an error. Even when a port has only a single incoming connection, the `sum_connections` operator must be used to include that port’s field in constraint expressions. Direct references to port fields are allowed exclusively in the **extra-output** section of a model. This rule enforces proper modeling practices by making all port contributions explicit and avoids errors in systems with multiple connections.

**Example**: Instead of writing a constraint like `balance_port.flow = 0` (which will cause an error), use the operator to sum the port’s value:

```yaml
# Incorrect usage (will cause an error):
expression: balance_port.flow = 0
 
# Correct usage (using sum_connections):
expression: sum_connections(balance_port.flow) = 0
```

## Time Operators and Indexing

**Mathematical Expression Syntax**  provides convenient time operators to refer to specific time-indexed values or to aggregate over time. These operators apply to time-dependent parameters, variables, or port fields.  Note that time indices are 0-based (typically, 0 = first time step).

### **Current time step** `[t]`

This optional suffix denotes the value at the current time index. It is implied by default, meaning if a time-dependent element is used in a time-indexed constraint, there is no need to explicitly write `[t]` – the system assumes the current time step’s value. However, it can be included for clarity.

For example:

```yaml
expression: generation[t] * 0.5
expression: generation * 0.5
```

In the first expression, `generation[t]` explicitly refers to the generation at time `t`, and is equivalent to the second expression, `generation`, when used in a time-dependent context.

### **Explicit index** `[N]`

Using an integer expression *N* in square brackets accesses the value at the *N-th* time step. For instance, `X[5]` refers to the value of time-dependent element *X* at the *6th* time period. The index *N* can itself be an expression involving only scalars and parameters (no variables) that resolves to an integer. This allows flexible indexing; e.g., `X[parameter_idx]` if `parameter_idx` is an integer parameter. This is useful for referring to specific periods (like a particular hour or year) in an equation.

### **Relative shift** `[t+N] / [t-N]`

This allows shifting the time index forward or backward by *N* steps. For example, `X[t+1]` is the value of *X* at the next time step, and `X[t-1]` is the previous time step. The offset *N* can be an expression (using scalars and parameters) that evaluates to an integer. Depending on the study time semantics, shifted indices (e.g. `[t+1]` at the last timestep) may wrap around to keep the horizon periodic.
This is commonly used for cyclic constraints such as storage dynamics.

```yaml
expression: levels[t+1] = levels + injection - withdrawal
```

Now, it can be concluded that terms `levels[T+1]` and `levels[0]` are reffering to the same variable.

### **Time summation (full horizon)** `sum(X)`

Denotes the sum of the time-dependent operand *X* over the entire optimization horizon. If *X* is defined for each time step from *0* to *T-1*, then `sum(X)` produces a single scalar equal to $\sum_{t=0}^{T-1} X_t$.

### **Time summation (range)** `sum(S .. E, X)`

Sums the operand X from time *S* to time *E*.

Here *S* and *E* can be either:

- A constant or parameter expression that resolves to a time index

- A relative expression involving *t*. For example, `sum(t-3 .. t, X)` would sum *X* from 3 periods ago up to the current period *t*. Both *S* and *E* are evaluated as integers. This form allows moving window calculations (e.g., sum over a rolling horizon up to the current time)

Using these time operators, advanced temporal constraints can be created. For example:

```yaml
# Enforce that each period's production <= average of next 3 periods
expression: production[t] <= (1/3) * sum(t .. t+3, production)
```

## Custom Sets and Indexing (Proposed)

!!! warning "Design proposal — not yet implemented"
    This section describes a **proposed** extension to the Mathematical Expression Syntax. It is not
    yet implemented in [GemsPy](../index.md) — no model library or study can use this syntax today.
    It is documented here to gather feedback on the design before implementation begins.

In addition to the built-in [time](#time-operators-and-indexing) and [scenario](#scenario-operator)
dimensions, a model may declare arbitrary **custom sets** — user-defined discrete index domains (e.g.
the price segments of a storage's marginal-value curve, a list of fuels, a set of sub-technologies)
— and index parameters, variables, and expressions over them.

Custom-set indexing reuses the same square brackets `[ ]` already used for [time
indexing](#time-operators-and-indexing) — there is no second bracket delimiter to learn. A set's own
`id` doubles as its index variable inside `[ ]`: used bare (`X[fuel]`) it means "the current
element"; used with an explicit `set_id=value` keyword form (`X[fuel=2]`) it means "this specific
element." See [Indexing expressions](#indexing-expressions) below for the full grammar, including how
a custom-set index composes with a time index in the same brackets (`X[t+1, fuel]`).

Custom sets come in two scopes, and the right choice depends on whether the set ever needs to be
shared across connected components (through a port) or stays purely internal to one model:

- **Local sets** — declared at [model level](#declaring-a-local-model-level-set); may vary per
  component; never visible outside the model that declares them.
- **Global sets** — declared once at [library level](#declaring-a-global-library-level-set); visible
  to every model and port-type field in that library; **required** whenever a set needs to cross a
  port, since every component connecting through that port must agree on the exact same index domain.

**Both scopes follow the same rule for where a set's concrete contents live: never in the library.** A
model or library only ever declares that a set exists (its `id` and **kind** — `ordinal` or
`enumerated`); the concrete `cardinality`/`elements` are always assigned in `system.yml` — once,
study-wide, for a global set, or per component, for a local set. **`cardinality` is itself never a
literal, for either scope** — it always names a parameter (a model parameter for a local set, a
[global parameter](file-structure/library.md#global-parameters) for a global set), whose value is
what `system.yml` actually assigns (see [Declaring a local (model-level)
set](#declaring-a-local-model-level-set) and [Declaring a global (library-level)
set](#declaring-a-global-library-level-set) below). This mirrors exactly how GEMS already treats
parameters and properties (declared in the library, valued in the system file), applied to sets too,
and it means named-element access (`X[fuel=gas]`) is never valid in library expressions for *any* set
— see [Indexing expressions](#indexing-expressions) below.

### Why the distinction matters

Time and scenario are *global* dimensions: every component in a study shares the same time horizon
and scenario count, which is exactly why results can be laid out on one shared array indexed by
(component, time, scenario) in [GemsPy](../index.md)'s solver implementation. A **local** set is
inherently *ragged*: different components of the same model can have a
different cardinality or different named elements. A ragged dimension cannot be safely combined
across components — there is no well-defined meaning to summing "element 0" of one component's list
against "element 0" of a different component's list if the lists don't actually agree. That is why
local sets may only be used internally, within the model that declares them, and why anything that
needs to cross a port must use a **global** set instead — a global set is guaranteed identical for
every component that can ever connect through it, so it behaves like time/scenario: uniform, not
ragged.

### Declaring a local (model-level) set

A model declares its local custom sets in a `sets` collection, alongside `parameters` and `variables`.
Every local set states its **kind** (`ordinal` or `enumerated`) — its concrete contents are never
given here, exactly like a global set (see below):

- **Ordinal (range) set** (`kind: ordinal`) — 0-based integer positions `0 .. cardinality-1`
  (consistent with time's 0-based convention). `cardinality` names a scalar parameter of this model —
  never a literal — whose *value* (assigned per component, via the ordinary parameter-assignment
  mechanism in `system.yml`, exactly like any other parameter) gives that component's set size. This
  is how a local ordinal set varies per component: no new mechanism beyond the one parameters already
  use. The referenced parameter must itself be scalar (non-time/scenario-dependent) and must not
  itself be `indexed-by` anything, to avoid a circular "set size depends on another set" dependency.
- **Enumerated (named) set** (`kind: enumerated`) — named, ordered elements. The concrete `elements`
  list is always supplied per component in `system.yml`'s `sets:` list (never in the model), mirroring
  how [Properties](file-structure/system.md#properties) values are supplied per component while their
  keys are declared in the model — see [System — Local Sets](file-structure/system.md#local-sets).

```yaml
models:
  - id: multi_segment_storage
    parameters:
      - id: segment_count
        time-dependent: false
        scenario-dependent: false
    sets:
      - id: segment
        description: "Price segments of the storage's marginal-value curve"
        kind: ordinal
        cardinality: segment_count   # names a scalar parameter; its value is assigned per component
      - id: operating_mode
        kind: enumerated             # elements are supplied per component in system.yml
```

### Declaring a global (library-level) set

A library declares its global custom sets in a `sets` collection, a sibling of `parameters`,
`port-types`, and `models` — not nested inside any one of them, since a global set may be shared by
several models and port types at once. **A global set's concrete size or contents are never given in
the library** — only its `id`, `description`, and **kind** (`ordinal` or `enumerated`), matching
GEMS's existing pattern of the library declaring structure while the system file assigns concrete
values (the same way a model declares that a parameter exists, but only `system.yml` gives it a
value). For `kind: enumerated`, the concrete `elements` are supplied exactly once, study-wide, in
`system.yml`'s new top-level [`sets`](file-structure/system.md#global-sets) section. For
`kind: ordinal`, there is no concrete value in the `sets:` section at all — instead the library's
`sets` entry names a **[global parameter](file-structure/library.md#global-parameters)** as its
`cardinality`, exactly as a local set's `cardinality` names a *model* parameter, and that global
parameter's value is what `system.yml`'s new top-level
[`parameters`](file-structure/system.md#global-parameters) section supplies, once, study-wide. Either
way, a global set's concrete contents are never given in the library, and never per-component (see
[Why the distinction matters](#why-the-distinction-matters) above for why a per-component override
would defeat the purpose of a global set):

```yaml
library:
  id: example_library
  parameters:
    - id: segment_count
  sets:
    - id: fuel
      kind: enumerated
    - id: segment_count_set
      kind: ordinal
      cardinality: segment_count   # names a global parameter; its value is assigned once, study-wide
  port-types:
    - id: multi_fuel_port
      fields:
        - id: flow
        # see "Port fields and custom sets" below
  models:
    - id: multi_fuel_generator
      parameters:
        - id: gen_capacity
          indexed-by: fuel   # references the global set directly, no local declaration needed
          time-dependent: false
          scenario-dependent: false
```

Because a global set's `elements` are never known at library-authoring time, **bare named-element
access (e.g. `X[fuel=gas]`) is never valid against a global set inside library expressions** — a model
may only use ordinal-style access against a global set: the bare set-id for the current position
(`X[fuel]`), a relative shift (`X[fuel+1]`), or an explicit integer position given via the keyword
form (`X[fuel=0]`). This holds regardless of `kind` — `enumerated` still means "named, ordered
elements" once `system.yml` resolves it, it just means library expressions can only reach those
elements by position, never by name. This is not actually specific to global sets: since **local**
sets now follow the identical rule (concrete contents always assigned in `system.yml`, never given in
the model — see [Declaring a local (model-level) set](#declaring-a-local-model-level-set) above),
named-element access is never valid against *any* set inside library expressions, local or global.

**Recommended practice** (a `system.yml`-level concern now, since that's the only place a global set's
concrete contents ever exist): instantiate each study's global sets as *universal* — the superset of
every element that could ever be relevant across the whole system (e.g. `elements: [gas, coal, oil,
biomass, hydrogen]` even if a given generator only burns two of them) — and express per-component
variation through the *data* (e.g. a capacity/bound of `0` for unused elements) rather than through
differing set membership. This keeps the set's dimension uniform across every component, exactly like
time and scenario already are, which is what makes cross-component aggregation (`sum_connections`,
binding constraints — see [Port fields and custom sets](#port-fields-and-custom-sets)) well-defined
without any extra runtime validation.

No locally-declared identifier in a model — not just a local set, but also a parameter, variable,
port, constraint, or any other model-level `id` — may collide with a global set's `id`, or a [global
parameter's](file-structure/library.md#global-parameters) `id`, visible in the same library, since all
of these are resolved through the same bare-identifier / `indexed-by` lookup; see [Rules for id
naming](file-structure/library.md#rules-for-id-naming) for the complete rule.

### Marking a parameter or variable as set-indexed

A new `indexed-by` field, alongside the existing `time-dependent` / `scenario-dependent` booleans,
declares that a parameter or variable carries one or more custom-set dimensions. It resolves against
the model's own local sets, plus every global set declared in the library:

```yaml
parameters:
  - id: segment_capacity
    indexed-by: segment
    time-dependent: false
    scenario-dependent: false
variables:
  - id: segment_level
    indexed-by: segment
    lower-bound: 0
    upper-bound: segment_capacity[segment]
    variable-type: continuous
```

`indexed-by` also accepts a list (`indexed-by: [segment, fuel]`) for a parameter or variable indexed
by more than one custom set at once — see [Multiple indexing sets](#multiple-indexing-sets) below.

### Port fields and custom sets

A port-type field may declare `indexed-by` directly, exactly like a parameter or variable — including
a list for a field indexed by more than one set (`indexed-by: [fuel, region]`, using the same
comma-list `[...]` syntax as [Multiple indexing sets](#multiple-indexing-sets)) — but it may only
reference **global** sets, never a local one, since port types are declared independently of any
model and have no visibility into a model's local sets:

```yaml
port-types:
  - id: multi_fuel_port
    fields:
      - id: flow
        indexed-by: fuel
```

A [`port-field-definition`](file-structure/library.md#port-field-definition)'s expression must produce
a value whose inferred indexing matches the field's declared `indexed-by` exactly — the same kind of
consistency check already required to keep a variable's declared time/scenario structure consistent
with its defining expression, extended to this new dimension:

```yaml
port-field-definitions:
  - port: injection_port
    field: flow
    definition: p_generation[fuel]   # must be `fuel`-indexed to match flow's declared indexed-by
```

**Multidimensional port fields** — a field's `indexed-by` list can name more than one set, exactly
like a parameter or variable's can (see [Multiple indexing sets](#multiple-indexing-sets)):

```yaml
port-types:
  - id: multi_fuel_multi_region_port
    fields:
      - id: flow
        indexed-by: [fuel, region]

port-field-definitions:
  - port: injection_port
    field: flow
    definition: p_generation[fuel, region]   # must match flow's declared indexed-by exactly
```

Because a port field may only ever reference global sets in the first place, this holds dimension by
dimension: **every** set in a multidimensional port field's `indexed-by` must be global — there is no
partial or mixed case where some dimensions are global and others local.

Because a port field's `indexed-by` can only name a global set, and every component connecting through
that port type necessarily shares that exact global set, [`sum_connections`](#port-operator) and any
[binding constraint](file-structure/library.md#binding-constraints) built on top of it are well-defined
by construction — no additional runtime guard is needed beyond this schema-level restriction.

**Escape hatch, and its limit:** if a model genuinely needs a port-facing global set *and* a
related-but-different, per-component-flexible local set, `sum_over` only helps in the degenerate case
where the port field itself ends up **unindexed** — i.e. the field is a plain aggregate total, not
broken down by element (`sum_over(local_set, internal_var)` fully collapses `local_set` to a scalar,
per the [dimension-selectivity rule](#aggregating-over-a-custom-set) below). It **cannot** produce a
value still indexed by the global set (e.g. `flow[fuel]`) out of a differently-shaped local set —
`sum_over` reduces a dimension to a scalar, it does not remap one set's index space onto another's.
If the port field must genuinely stay broken down by global-set element, and the model's internal
detail lives on a different, differently-shaped local set, **this proposal has no solution**: it would
require a true set-to-set mapping/index-alignment primitive, which does not exist here and would be
future work.

### Indexing expressions

Custom-set indexing extends the same `[ ]` operator already defined in [Time Operators and
Indexing](#time-operators-and-indexing), rather than introducing a second bracket. A single pair of
brackets can carry any number of comma-separated **index terms**, one per dimension being indexed
(time and/or one or more custom sets):

```
index-list  := index-term (',' index-term)*
index-term  := int-expr                                # legacy form — always means the time dimension
             | identifier (('+' | '-') int-expr)?       # current position, or relative shift
             | identifier '=' int-expr                  # explicit position (keyword form)
identifier  := 't' | <declared set id>                  # a local set, or a global set visible in this library
```

| Form | Meaning | Notes |
|---|---|---|
| `X[t]` / `X` (no brackets) | current time step | unchanged from today |
| `X[5]` | explicit time step 5 | a **bare integer term always means time** — see rule below |
| `X[t+1]` / `X[t-1]` | relative time shift | unchanged from today |
| `X[fuel]` | current element of set `fuel` | the `[ ]` analogue of `X[t]` |
| `X[fuel+1]` / `X[fuel-1]` | relative shift by position on `fuel` | ordinal sets only |
| `X[fuel=2]` | explicit position 2 on set `fuel` | keyword form — see rule below |
| `X[t+1, fuel]` | compose a time shift with current-`fuel` | any mix of dimensions, comma-separated |
| `X[segment=2, fuel=1]` | explicit positions on two sets at once | order-independent — see [Multiple indexing sets](#multiple-indexing-sets) |
| `(expr)[fuel]` | index an arbitrary parenthesized **expression**, not just a bare identifier | as for time today |

Two rules keep this grammar unambiguous and fully backward compatible:

- **A bare integer index term always and only means the time dimension** (`X[5]` ≡ `X[t=5]`), never
  inferred as a position on some other dimension of `X`, even when `X` has no time dimension at all
  (in which case it is simply invalid, exactly as it is today). This is what keeps every existing
  `X[t]`, `X[5]`, `X[t+1]`, `X[t-1]` example valid, unchanged, with zero new ambiguity — a small
  trade of brevity for a rule with no exceptions.
- **An explicit position on a custom set always uses the keyword form** (`X[fuel=2]`), never a bare
  integer (`X[2]` would mean time). This also removes the old proposal's fragile "positional,
  declaration-order-dependent" multi-index form — see [Multiple indexing sets](#multiple-indexing-sets)
  below.

Because a set's `id` is an ordinary identifier — not a reserved keyword the way `t` is — standard
arithmetic precedence already parses `segment+1`, `2*segment - 1`, etc. correctly on the right-hand
side of a shift or keyword term; no dedicated "shift" grammar beyond time's is required for custom
sets.

**No implicit brackets needed for the common case:** exactly as a bare `generation` (no brackets)
today implicitly means `generation[t]`, a set-indexed parameter or variable used with **no brackets
at all** implicitly means "current position on every one of its declared dimensions" — time, and
every set in its `indexed-by`. Brackets are needed only to *deviate* from "current" on one or more
dimensions; any dimension left out of the bracket list simply stays at its current position (exactly
as `X[t+1]` today shifts only time and leaves every other dimension, if any existed, untouched).

**Note:** there is deliberately no "bare named-element" form (e.g. `X[fuel=gas]`) in this grammar — a
set's concrete elements are never known at library-authoring time (see [Declaring a global
(library-level) set](#declaring-a-global-library-level-set) above), so named access is not part of
this syntax at all; the keyword form's right-hand side is always an integer position.

### Aggregating over a custom set

A new operator, `sum_over(<set_id>, <expr>)`, aggregates an expression across every element of a
custom set, mirroring the pattern where each new dimension gets its own aggregator name (`sum` for
time, `expec` for [scenario](#scenario-operator)) rather than overloading `sum`:

```yaml
constraints:
  - id: total_level
    expression: level = sum_over(segment, segment_level)
```

`sum_over(set_id, expr)` collapses only the named set's dimension; every other dimension the operand
carries — time, scenario, or another custom set — is preserved, exactly as `sum(X)` collapses time
alone and leaves scenario untouched.

### Multiple indexing sets

A parameter or variable can be indexed by more than one custom set. Indices are comma-separated
inside a single pair of square brackets, exactly like combining a time shift with a set index —
`indexed-by`'s declaration order has no bearing on how a multi-index expression must be written,
since every dimension is named explicitly:

```yaml
sets:
  - id: segment
    kind: ordinal
    cardinality: segment_count
  - id: fuel
    kind: enumerated   # elements supplied per component in system.yml

parameters:
  - id: segment_fuel_cost
    indexed-by: [segment, fuel]
    time-dependent: false
    scenario-dependent: false
```

| Form | Meaning |
|---|---|
| `X[segment, fuel]` | current element of both (implicit/unfolded on both dimensions) |
| `X[segment+1, fuel]` | shift `segment` by +1, keep `fuel` at its current element |
| `X[segment=2, fuel=1]` | explicit position 2 on `segment`, explicit position 1 on `fuel` |

Both `segment` and `fuel` here are **local** sets, but the same multi-set syntax applies identically
to global sets, or a mix of the two — `indexed-by` doesn't care about scope, only about which sets are
named. As always, every explicit position is integer-only, never a named element — `X[segment=2,
fuel=1]`, never `X[segment=2, fuel=gas]` — since neither set's concrete elements are known at
library-authoring time (see [Declaring a local (model-level) set](#declaring-a-local-model-level-set)
and [Declaring a global (library-level) set](#declaring-a-global-library-level-set)). Unlike a
positional scheme, the keyword form `set_id=value` is **order-independent**: `X[fuel=1, segment=2]`
and `X[segment=2, fuel=1]` are the same expression, since each term names the dimension it applies to
rather than relying on matching `indexed-by`'s declaration order.

Aggregation stays single-set per call and nests for multi-set reduction, rather than introducing a
second aggregation form:

```yaml
expression: total = sum_over(fuel, sum_over(segment, segment_fuel_cost))
```

### Implicit unfolding

A constraint unfolds over a custom set whenever it contains, anywhere in its expression, **either**
of two things:

- a set-indexed variable/parameter — used bare (no brackets at all), or with the explicit "current
  element" form `X[segment]` — exactly like today's time/scenario unfolding rule (see
  [Time-Dependent Constraints vs. Aggregation](#time-dependent-constraints-vs-aggregation)), extended
  to a third dimension; or
- a **bare reference to the set's own `id`, used as a scalar value** — e.g. plain `segment` in
  `base_price + segment * price_step` — even when no parameter or variable in the expression is
  itself declared `indexed-by` that set. Referencing a set's index value only ever makes sense within
  a context unfolding over that set, so this occurrence is itself enough to trigger unfolding — see
  [Referencing a set's index value](#referencing-a-sets-index-value) below.

Because these two conditions cover every way an expression can possibly depend on a custom set, this
detection is always automatic — there is no scenario left where a constraint needs to unfold over a
set without either condition holding (an expression containing neither would be N identical,
non-varying copies of the same equation, which has no modeling purpose).

**Cross-product unfolding:** a constraint whose terms carry more than one dimension — two different
custom sets, or a custom set alongside time and/or scenario — unfolds over the **cross-product** of
all of them, generalizing the time+scenario dual-unfolding rule the base doc already establishes (a
term that is both time- and scenario-dependent already unfolds per `(t, s)` pair today; a term that is
also `segment`-indexed, or that bare-references `segment`, unfolds per `(t, s, segment)` triple, and
so on for any further set).

### Referencing a set's index value

Used bare, outside `[ ]`, a set's own `id` evaluates to the current element's 0-based integer
position within whichever set-indexed context it is unfolding in — e.g. plain `segment` below is a
plain number (0, 1, 2, …), not a subscript operator. This holds uniformly for both ordinal and
enumerated sets, since even an enumerated set has a well-defined order once `system.yml` resolves it
(`fuel` bare = 0 for `gas`, 1 for `coal`, 2 for `oil`, given a resolved `elements: [gas, coal, oil]`).

As established in [Implicit unfolding](#implicit-unfolding) above, this bare reference is on its own
enough to make a constraint unfold over that set — no separate tag is needed, even when nothing else
in the expression is set-indexed:

```yaml
extra-outputs:
  - id: segment_number
    expression: segment
```

Here `segment` is the *only* thing in the expression connected to the `segment` set — no parameter or
variable is indexed by it — yet this alone unfolds the output into one row per segment element,
reporting that element's position.

This is exactly why the naming rules forbid a set's `id` from colliding with a parameter/variable `id`
or the reserved literal `t` (a local set), or with any locally-declared identifier at all (a global
set) — see [Rules for id naming](file-structure/library.md#rules-for-id-naming) for the complete rule
— otherwise a bare reference to that name would be ambiguous between "current index position", a
parameter/variable lookup, or the built-in time index.

This also covers the case of a constraint that carries *several* set dimensions at once — some
inferred from a set-indexed term, others from a bare index-value reference like `segment` above: per
[Cross-product unfolding](#implicit-unfolding) above, the constraint simply unfolds over the
union/cross-product of all of them, exactly as it would for any other combination of dimensions.

### Collision check

- `[ ]` is no longer time-only: it becomes the single reserved indexing delimiter for every
  dimension — time and custom sets alike. `{ }` is dropped from this proposal entirely and stays
  fully unused/reserved.
- Every existing time-only form (`X[t]`, `X[5]`, `X[t+1]`, `X[t-1]`) keeps its exact current meaning
  — see the [bare-integer-always-means-time rule](#indexing-expressions) — so this change is
  additive, not breaking, for anything written against today's syntax.
- The `=` introduced by the keyword form (`X[fuel=2]`) does not collide with the "exactly one
  comparison operator" rule for constraints (see [Comparison Operators](#comparison-operators)):
  that rule counts `=`/`<=`/`>=` at the **top level** of a constraint expression, outside all
  bracket/paren nesting. A parser that respects bracket nesting (as it already must, to parse
  `sum(t .. t+3, production)` correctly today) scopes a keyword-form `=` to its enclosing `[ ]` and
  never surfaces it to top-level comparison-operator counting.
- The `,` introduced for multi-dimensional indexing (`X[segment, fuel]`) does not collide with the
  pre-existing use of `,` inside `sum(S..E, X)` or `min(u, v, ...)`/`max(u, v, ...)` — those are
  function-call parentheses `()`, a different delimiter from the index brackets `[ ]`.
- `indexed-by: [fuel, region]` (a YAML list, parsed by the YAML loader before any expression string
  is handed to the math-expression parser) and `X[fuel, region]` (inside an `expression:` string,
  parsed by the math-expression grammar above) are visually similar but live in two entirely
  different layers — no actual collision, but worth calling out explicitly since both use `[ ]`.
- `.` stays reserved for [ports](#ports).
- `sum_over` is a new name, distinct from `sum`, `sum(S..E,X)`, `sum_connections`, `expec`.

## Constraints

A constraint is described by a single expression containing a comparison operator (`=`, `<=`, or `>=`). The left and right sides must be a linear expressions. Here are the key points about constraints:

- A constraint must have exactly one comparison operator dividing the expression. For example: `generation <= capacity` or `supply = demand`.
- The expression on each side of operators `=/<=/>=` can include any allowed terms: constants, parameters, variables, port fields (subject to the linearity and dependency rules).

**Example:** In the generator model example below, an internal constraint ensures the generator’s minimum output when it’s on:

```yaml
expression: active_power >= is_on * min_active_power
```

### Time-Dependent Constraints vs. Aggregation

If a constraint expression includes any time-indexed element (e.g. a time-dependent variable), that constraint implicitly applies at each time step across the horizon. In other words, the model interpreter *unfolds* it into a series of constraints, one per period `t`. To instead enforce a single aggregate constraint across time, `sum(...)` aggregator should be used in constraint expression.

|  Constraint | Functionality  |
| -----------  | ----------  |
|`x[t] <= 100`| For each time-step apply constraint|
|`sum(x) <= 100`| Single constrant over entire time horizon|

## Objective Function

Objective function is described by an expression which should be a linear expression of variables, parameters, and scalars.

**Example:** A generator might have an objective term for its production cost:

```yaml
expression: sum(generation * generation_cost)
```

## Additional Operators

### Scenario Operator

[GEMS](../index.md) can handle multiple scenarios  for data and variables. These scenarios are independent or coupled for two-stage stochastic optimization. Scenario-dependent parameters or variables have values that differ by scenario (similar to having an extra scenario index s). **Mathematical Expression Syntax**  currently provides an operator to aggregate across the scenario dimension:

- **expec(X)** aggregator: where `X` is the scenario-dependent operand, this operator computes its expected value (i.e. its scenario-wise average).

### Dual Operators

In some cases, there is a  need to access dual results of variables or constraints of the linear problem. Depending on the case, the dual unary operator is :

- dual result of a variable whose id is `my_var` is accessed by `-reduced_cost(variable_id)`
- dual result of a constraint whose if is `my_constraint` is accessed by `dual(constraint_id)`

### Power Operator

This binary operator `^` is used within any expression, but with following restrictions.

In the context of a linear problem construction, its operands can only be literals or parameters.

```yaml
expression: parameter_1^(1 + parameter_2)
```

 In the context of a extracting results, its operands can be literals, parameters or variables.

```yaml
expression: variable_1^(1 + parameter_1)
```

### Min/Max Operators

These n-ary operators `max(u, v, ...)`/`min(u, v, ...)` are used within any expression, but with following restrictions.

 In the context of a linear problem construction, its operands can only be literals or parameters.

```yaml
expression: parameter_1 < max(parameter_2, 100)
```

 In the context of a extracting results, its operands can be literals, parameters or variables.

```yaml
expression: min(variable_1, parameter_1)
```

### Floor/Ceil/Abs/Round Operators

These unary operators `floor(X)`, `ceil(X)`, `abs(X)`, and `round(X)` (round-half-to-even) are used within any expression, but with the following restrictions:

  When `X` is time-dependent (a parameter, variable, or port field with time dimension), the operators apply pointwise on the underlying time-series.

  In the context of a linear problem construction (any context but **extra-output**), the argument of `floor`, `ceil`, `abs`, or `round` must not depend on decision variables.

```yaml
expression: floor(parameter_1 * 2)

expression: ceil(parameter_1 / 2)

expression: abs(parameter_1 - parameter_2)

expression: round(parameter_1 / 3)
```

In the context of **extra-output**, the argument can include decision variables since they are evaluated after solving.

```yaml
expression: abs(variable_1 - parameter_1)

expression: round(variable_1 / parameter_1)
```

`round(X)` uses round-half-to-even (banker's rounding), consistent with Python 3 and NumPy behaviour.

