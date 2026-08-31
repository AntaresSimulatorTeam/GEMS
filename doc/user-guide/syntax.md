---
description: Reference for GEMS expression syntax — operators, variables, parameters, port fields, linearity conditions, and time and scenario indexing mechanisms.
---

# GEMS Syntax

[GEMS](../index.md) includes an **Expression Syntax** that allows users to write equations for optimization problems in a clear, math-like syntax within specific configuration files. This syntax is independent of any programming code – model equations are specified as human-readable text, which [GEMS](../index.md) interprets to build the mathematical optimization problem.

This section provides a description of the supported operators, linearity condition, the usage of parameters, variables, and ports in expressions, and the mechanisms for time and scenario indexing and aggregation.

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

**Important:** Comparison operators are only allowed in constraint expressions (not in general arithmetic expressions), with one exception: in [`extra-outputs`](input-files/library.md#extra-output), a comparison operator evaluates to a boolean (`0`/`1`) instead of forming a constraint — e.g. `unsupplied_energy >= 0.000001` to flag loss of load. Each constraint expression must contain exactly one comparison operator (`=`, `<=`, or `>=`)
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

Parameters represent fixed input data values that can be referenced by their `id` as a symbol to include its value in expressions. For example:

```yaml
expression: 3 * parameter_1 + 6.345 / parameter_2
```

This would use the numeric value of `parameter_1` and `parameter_2` as provided in the system input data.

Parameters can be time-dependent (having a separate value for each time step of the simulation horizon) or scenario-dependent (having different values under different scenario cases), or both. If a parameter is time-dependent, think of it as a series $p(t)$ over time; if scenario-dependent, as $p(s)$ varying by scenario; it can even be $p(t,s)$ if varying across both dimensions. See [Time Operators and Indexing](#time-operators-and-indexing) and [Scenario Operator](#scenario-operator) for how to write expressions involving such parameters.

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

!!! warning "Design proposal — not yet implemented"
    The same inference applies to a third dimension, too: if a port field's defining expression is
    indexed by a [custom set](#custom-sets-and-indexing-proposed) (deduced the same way, from the
    parameters/variables the expression depends on), the field carries that dimension — no separate
    declaration is needed, exactly like time and scenario. See [Port fields and custom
    sets](#port-fields-and-custom-sets) for the two rules this inference must additionally satisfy
    before a field can be aggregated across connections. Not yet implemented in [GemsPy](../index.md).

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

Here, when `t` corresponds to the last time step, `levels[t+1]` is the same as `levels[0]`.

### **Time summation (full horizon)** `sum(X)`

Denotes the sum of the time-dependent operand *X* over the entire optimization horizon. `sum(X)` produces a single scalar equal to the sum of *X* over every time step from `0` to the [`last-time-step`](input-files/solver-optimization.md#simulation-horizon) (inclusive).

!!! note "Difference `sum` from `sum_connections`"
    - `sum(X)` : aggregate a time-dependent quantity **across time steps** (temporal summation).
    - `sum_connections(port.field)` : aggregates a port field **across connected components** (structural summation). See [Port Operator](#port-operator).

    For the full specification of these operators, see the [Antares Modeler Expressions reference](https://antares-simulator.readthedocs.io/en/latest/user-guide/modeler/09-expressions/#time-operators).

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
indexing](#time-operators-and-indexing). A set's own
`id` doubles as its index variable inside `[ ]`: used bare (`X[fuel]`) it means "the current
element"; used with an explicit `set_id=value` keyword form (`X[fuel=2]`) it means "this specific
element." See [Indexing expressions](#indexing-expressions) below for the full grammar, including how
a custom-set index composes with a time index in the same brackets (`X[t+1, fuel]`).

Custom sets come in two scopes, and the right choice depends on whether the set ever needs to be
shared across connected components (through a port) or stays purely internal to one model:

- **Local sets** — declared at [model level](input-files/library.md#sets); may vary per
  component; never visible outside the model that declares them.
- **Global sets** — declared once at [library level](input-files/library.md#library-level-sets); visible
  to every model and port-type field in that library; **required** whenever a set needs to cross a
  port, since every component connecting through that port must agree on the exact same index domain.

### Why the distinction matters

Time and scenario are *global* dimensions: every component in a study shares the same time horizon
and scenario count, which is exactly why results can be laid out on one shared array indexed by
(component, time, scenario) in [GemsPy](../index.md)'s solver implementation. A **local** set is
inherently *ragged*: different components of the same model can have a
different number of elements, or the same number under different names. A ragged dimension cannot be safely combined
across components — there is no well-defined meaning to summing "element 0" of one component's list
against "element 0" of a different component's list if the lists don't actually agree. That is why
local sets may only be used internally, within the model that declares them, and why anything that
needs to cross a port must use a **global** set instead — a global set is guaranteed identical for
every component that can ever connect through it, so it behaves like time/scenario: uniform, not
ragged.

### Port fields and custom sets

Exactly like time/scenario dependence for ports (see [the base Ports
section](#ports) above), a port-type field declares nothing new for custom sets: a field's custom-set
indexing is inferred purely from how connected models define it — e.g. if `p_generation` is
`indexed-by: fuel`, then

```yaml
port-field-definitions:
  - port: injection_port
    field: flow
    definition: p_generation[fuel]   # must be `fuel`-indexed to match flow's declared indexed-by
```

infers that `flow` is fuel-indexed too.

The only restriction on this inference: **a `port-field-definition`'s expression may only be indexed by
global sets, never a local one** — local sets are per-component/ragged (see [Why the distinction
matters](#why-the-distinction-matters) above), so letting one cross a port would silently break
aggregation the moment two connected components' local sets disagree in size or content. This is
checked on every model's `definition` on its own.

Different models connecting to the same port type do **not** need to agree on which global set(s) they
use for the same field — one model's definition can be `fuel`-indexed, another's `region`-indexed,
another's unindexed, all for the same field of the same port type. `sum_connections` and any binding
constraint combining them unfolds over the **union** of every global set involved, exactly like today's
[cross-product unfolding](#implicit-unfolding) of mixed time/scenario-dependent terms: each model's
contribution is broadcast — replicated — across whichever of those dimensions its own definition
doesn't carry, then summed element-wise. This is the same mechanism that already combines a purely
time-dependent term with a purely scenario-dependent one; custom sets just add further dimensions to
the same cross-product.

A definition indexed by more than one set at once (`p_generation[fuel, region]`) is simply inferred as
such, exactly as for a parameter or variable (see [Multiple indexing sets](#multiple-indexing-sets)) —
the global-only restriction then applies dimension by dimension (every set in the tuple must be global,
never a mix).

**Escape hatch, and its limit:** `sum_over` can bridge a port-facing global set and a related local set
only in the degenerate case where the port field ends up **unindexed** — `sum_over(local_set,
internal_var)` fully collapses the local set to a scalar (see [Aggregating over a custom
set](#aggregating-over-a-custom-set) below). It cannot remap a local set's index space onto a global
set's: if the port field must stay broken down by global-set element while the model's internal detail
lives on a differently-shaped local set, **this proposal has no solution** — that would require a true
set-to-set mapping primitive, left as future work.

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
  integer (`X[2]` would mean time) — see [Multiple indexing sets](#multiple-indexing-sets) below.

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

**Note:** there is deliberately no "bare named-element" form (e.g. `X[fuel=gas]`) in this grammar. A
set's `elements` are never known at library-authoring time — only once `system.yml`
[instantiates them](input-files/system.md#global-sets) (for a global set) or per component (for a
local one) — so a model may only ever access a set positionally: the bare set-id for the current
position (`X[fuel]`), a relative shift (`X[fuel+1]`), or an explicit integer position via the keyword
form (`X[fuel=0]`). This holds no matter how `system.yml` ends up instantiating the set's elements — a
name list still only reaches its elements by position from inside the library, never by name. This
applies identically to local and global sets.

**Position and label are not the same thing once a range doesn't start at 0.** With a 0-based range
(`0..4`), position and value happen to coincide — but nothing requires a range to start there. Given
`elements: 2020..2024` (e.g. a `vintage` set of years) in `system.yml`, `X[vintage=0]` still means
"the first declared element" — here, the element whose value is `2020` — not "the element whose value
is 0." Positional indexing (`X[segment]`, `X[segment=2]`, `X[segment+1]`) always addresses *position
within the declared list*, never the element's value, whether that list came from an explicit list or
a range.

**On meaningfulness, not validity:** every form above is well-defined for any set — `system.yml`
always resolves a set to an ordered list, whether it came from a range or a name list, and `[ ]` only
ever operates on that order positionally. But `X[segment+1]`-style relative shift only makes
*modeling* sense when the set's declared order itself carries meaning — price tiers, vintage years,
dispatch priority. For a set whose order is incidental (e.g. `fuel: [gas, coal, oil]`, listed in no
particular order), `X[fuel+1]` is syntactically legal but likely a modeling mistake, not a real "next
fuel" relationship. Unlike time, whose order is always chronological, GEMS doesn't distinguish the two
cases in the schema — it's on the library author to only rely on relative shift where the declared
order is deliberate.

**Getting data associated with each element:** there is no way to use a set's index position as a bare
arithmetic value (e.g. `segment * price_step`, using `segment` as a raw number) — only the forms above
are supported. If a model needs per-element data — a price step per segment, a conversion factor per
fuel — declare an ordinary parameter `indexed-by` that set and supply its values via the [set-indexed
data series](input-files/data-series.md#set-indexed-series) format, the same way a time-dependent
parameter's values come from a time series rather than from any implicit function of `t`:

```yaml
parameters:
  - id: segment_price_step
    indexed-by: segment
    time-dependent: false
    scenario-dependent: false

constraints:
  - id: segment_marginal_cost
    expression: segment_price[segment] = base_price + segment_price_step[segment]
```

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

**Getting a set's size:** there is no dedicated operator for this — `t`'s own count (`T`) isn't
exposed to expressions either, so a set doesn't get special treatment here. `sum_over(set_id, 1)`
already gives it for free: summing the constant `1` once per element yields the set's cardinality,
with no new syntax needed.

```yaml
expression: average_level = sum_over(segment, segment_level) / sum_over(segment, 1)
```

### Multiple indexing sets

A parameter or variable can be indexed by more than one custom set. Indices are comma-separated
inside a single pair of square brackets, exactly like combining a time shift with a set index —
`indexed-by`'s declaration order has no bearing on how a multi-index expression must be written,
since every dimension is named explicitly:

```yaml
sets:
  - id: segment
  - id: fuel

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
library-authoring time (see [Local sets](input-files/library.md#sets) and [Library-Level
Sets](input-files/library.md#library-level-sets)). Unlike a positional scheme, the keyword form
`set_id=value` is **order-independent**: `X[fuel=1, segment=2]` and `X[segment=2, fuel=1]` are the
same expression, since each term names the dimension it applies to rather than relying on matching
`indexed-by`'s declaration order.

Aggregation stays single-set per call and nests for multi-set reduction, rather than introducing a
second aggregation form:

```yaml
expression: total = sum_over(fuel, sum_over(segment, segment_fuel_cost))
```

### Implicit unfolding

A constraint containing a set-indexed variable/parameter — without an explicit index, or with the
"current element" form `X[segment]` — implicitly unfolds into one constraint per set element, exactly
like today's time/scenario unfolding rule (see [Time-Dependent Constraints vs. Aggregation](#time-dependent-constraints-vs-aggregation)), extended to a third dimension.

**Cross-product unfolding:** a constraint whose terms carry more than one dimension — two different
custom sets, or a custom set alongside time and/or scenario — unfolds over the **cross-product** of
all of them, generalizing the time+scenario dual-unfolding rule the base doc already establishes (a
term that is both time- and scenario-dependent already unfolds per `(t, s)` pair today; a term that is
also `segment`-indexed unfolds per `(t, s, segment)` triple, and so on for any further set).

Unfolding over a custom set is driven entirely by set-indexed parameter/variable terms appearing in the
expression, exactly like time/scenario unfolding today — there is no mechanism to force-unfold a
constraint over a set with no set-indexed term in it. This follows from `indexed-by` [existing only on
parameters and variables](input-files/library.md#sets) (see [Indexing
expressions](#indexing-expressions) above for the replacement pattern when a constraint needs data
associated with each element).

### Collision check

- `[ ]` is no longer time-only: it becomes the single reserved indexing delimiter for every
  dimension — time and custom sets alike.
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
|`sum(x) <= 100`| Single constraint over entire time horizon|

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
- dual result of a constraint whose id is `my_constraint` is accessed by `dual(constraint_id)`

### Power Operator

This binary operator `^` is used within any expression, but with following restrictions.

In the context of a linear problem construction, its operands can only be literals or parameters.

```yaml
expression: parameter_1^(1 + parameter_2)
```

 In the context of extracting results, its operands can be literals, parameters or variables.

```yaml
expression: variable_1^(1 + parameter_1)
```

### Min/Max Operators

These n-ary operators `max(u, v, ...)`/`min(u, v, ...)` are used within any expression, but with following restrictions.

 In the context of a linear problem construction, its operands can only be literals or parameters.

```yaml
expression: parameter_1 < max(parameter_2, 100)
```

 In the context of extracting results, its operands can be literals, parameters or variables.

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

