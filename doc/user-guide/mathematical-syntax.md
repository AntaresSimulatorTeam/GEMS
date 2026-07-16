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

Custom-set indexing uses curly braces `{ }`, a delimiter distinct from the square brackets `[ ]`
reserved for time, so the two never collide. A set's own `id` doubles as its index variable: used
bare inside `{ }` it means "the current element"; used with an explicit value it means "this specific
element."

Custom sets come in two scopes, and the right choice depends on whether the set ever needs to be
shared across connected components (through a port) or stays purely internal to one model:

- **Local sets** — declared at [model level](#declaring-a-local-model-level-set); may vary per
  component; never visible outside the model that declares them.
- **Global sets** — declared once at [library level](#declaring-a-global-library-level-set); visible
  to every model and port-type field in that library; **required** whenever a set needs to cross a
  port, since every component connecting through that port must agree on the exact same index domain.

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
Two kinds of sets are supported:

- **Ordinal (range) set** — `cardinality: <integer-literal-or-scalar-parameter-id>` gives 0-based
  integer positions `0 .. cardinality-1` (consistent with time's 0-based convention). Pointing
  `cardinality` at a scalar parameter id lets different components of the same model have different
  set sizes, using the same per-component parameter-assignment mechanism already used for any other
  parameter — no new mechanism is needed for this. The referenced parameter must itself be scalar
  (non-time/scenario-dependent, as already required of any `cardinality` parameter) and must not
  itself be set-indexed, to avoid a circular "set size depends on another set" dependency.
- **Enumerated (named) set** — `elements: [id1, id2, ...]` gives named, ordered elements. If every
  component instantiating the model shares the same list, declare it directly at model level (as
  below). If different components need different lists, declare only the set's `id` at model level
  (no `elements`) and supply the concrete list per component in `system.yml`, using the same
  `sets:` mechanism `system.yml` already uses for [Properties](file-structure/system.md#properties).

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
        cardinality: segment_count   # integer literal, or the id of a scalar parameter
```

### Declaring a global (library-level) set

A library declares its global custom sets in a `sets` collection, a sibling of `port-types` and
`models` — not nested inside any one of them, since a global set may be shared by several models and
port types at once:

```yaml
library:
  id: example_library
  sets:
    - id: fuel
      elements: [gas, coal, oil]   # fixed once and for all in the library, or...
    - id: technology
      # ...left unresolved here, to be instantiated per-study —
      # see System — Global Sets in file-structure/system.md
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

A global set's `cardinality`, unlike a local set's, must be an integer **literal** — a library isn't
owned by any one component, so it has no scalar parameter to point at. `elements` may likewise be
given directly, or left unresolved in the library and instantiated once for the whole study in
`system.yml`'s new top-level [`sets`](file-structure/system.md#global-sets) section (never
per-component — see [Why the distinction matters](#why-the-distinction-matters) above for why a
per-component override would defeat the purpose of a global set).

**Recommended practice:** make global sets *universal* — the superset of every element that could
ever be relevant across the library (e.g. `elements: [gas, coal, oil, biomass, hydrogen]` even if a
given generator only burns two of them) — and express per-component variation through the *data*
(e.g. a capacity/bound of `0` for unused elements) rather than through differing set membership. This
keeps the set's dimension uniform across every component, exactly like time and scenario already are,
which is what makes cross-component aggregation (`sum_connections`, binding constraints — see
[Port fields and custom sets](#port-fields-and-custom-sets)) well-defined without any extra runtime
validation.

A model's own local set `id`s must not collide with any global set `id` visible in the same library
(in addition to the naming rules in [Indexing a constraint explicitly](#indexing-a-constraint-explicitly-and-referencing-the-index-value-itself)
below) — since both are resolved through the same `indexed-by` lookup.

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
    upper-bound: segment_capacity{segment}
    variable-type: continuous
```

`indexed-by` also accepts a list (`indexed-by: [segment, fuel]`) for a parameter or variable indexed
by more than one custom set at once — see [Multiple indexing sets](#multiple-indexing-sets) below.

### Port fields and custom sets

A port-type field may declare `indexed-by` directly, exactly like a parameter or variable — but it
may only reference a **global** set, never a local one, since port types are declared independently
of any model and have no visibility into a model's local sets:

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
    definition: p_generation{fuel}   # must be `fuel`-indexed to match flow's declared indexed-by
```

Because a port field's `indexed-by` can only name a global set, and every component connecting through
that port type necessarily shares that exact global set, [`sum_connections`](#port-operator) and any
[binding constraint](file-structure/library.md#binding-constraints) built on top of it are well-defined
by construction — no additional runtime guard is needed beyond this schema-level restriction.

**Escape hatch:** if a model genuinely needs a port-facing global set *and* a related-but-different,
per-component-flexible local set, keep them as two distinctly-named sets and have the
`port-field-definition` reduce explicitly from the local set to the global one (e.g. via `sum_over`,
with the model author writing the correspondence by hand). There is no generic set-to-set mapping
primitive in this proposal — a true index-alignment/mapping feature would be future work.

### Indexing expressions

| Form | Meaning | Time analogue |
|---|---|---|
| `X{segment}` | current element (implicit within an unfolded/aggregated context) | `X[t]` |
| `X{2}` | explicit element at position 2 (ordinal sets, 0-based) | `X[5]` |
| `X{segment+1}` / `X{segment-1}` | relative shift by position (ordinal sets only) | `X[t+1]` / `X[t-1]` |
| `X{gas}` | explicit named-element access (enumerated sets) | *(no time equivalent)* |
| `(expr){segment}` | index an arbitrary parenthesized **expression**, not just a bare identifier | `(expr)[t+1]` |
| `X{segment}[t+1]` | compose set- and time-indexing on the same term | — |

Because a set's `id` is an ordinary identifier — not a reserved keyword the way `t` is — standard
arithmetic precedence already parses `segment+1`, `2*segment - 1`, etc. correctly; no dedicated
"shift" grammar (like time's) is required for custom sets.

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
inside a single pair of braces, in the same order as declared in `indexed-by`:

```yaml
sets:
  - id: segment
    cardinality: segment_count
  - id: fuel
    elements: [gas, coal, oil]

parameters:
  - id: segment_fuel_cost
    indexed-by: [segment, fuel]
    time-dependent: false
    scenario-dependent: false
```

| Form | Meaning |
|---|---|
| `X{segment, fuel}` | current element of both (implicit/unfolded on both dimensions) |
| `X{segment+1, fuel}` | shift `segment` by +1, keep `fuel` at its current element |
| `X{2, gas}` | explicit position 2 on `segment`, explicit element `gas` on `fuel` |

Aggregation stays single-set per call and nests for multi-set reduction, rather than introducing a
second aggregation form:

```yaml
expression: total = sum_over(fuel, sum_over(segment, segment_fuel_cost))
```

### Implicit unfolding

A constraint containing a set-indexed variable/parameter — without an explicit index, or with the
"current element" form `X{segment}` — implicitly unfolds into one constraint per set element, exactly
like today's time/scenario unfolding rule (see [Time-Dependent Constraints vs. Aggregation](#time-dependent-constraints-vs-aggregation)), extended to a third dimension.

!!! note "Open question"
    What happens when a constraint's *implicit* set dimension (inferred from one of its own terms)
    differs from an *explicitly* declared `indexed-by` naming a different set on that same constraint
    (see below)? This proposal does not yet specify whether the constraint should unfold over the
    union/product of both, or how such a mismatch should be reported. Flagged here as unresolved —
    left for a follow-up refinement rather than the initial proposal.

### Indexing a constraint explicitly, and referencing the index value itself

Implicit unfolding only fires when the constraint contains a term that is itself `indexed-by` the
set. To unfold a constraint over a set even when none of its terms are set-indexed — typically
because the constraint only needs the *index value* itself, not a subscript into anything — add an
explicit `indexed-by` field on the constraint (this field applies identically to
`binding-constraints`, `objective-contributions`, and `extra-outputs`):

```yaml
constraints:
  - id: segment_marginal_cost
    indexed-by: segment
    expression: segment_price{segment} = base_price + segment * price_step
```

Used bare, outside `{ }`, a set's own `id` evaluates to the current element's 0-based integer
position within whichever set-indexed context it is unfolding in — e.g. bare `segment` above is a
plain number (0, 1, 2, …), not a subscript operator. This holds uniformly for both ordinal and
enumerated sets, since even an enumerated set has a well-defined declaration order (`fuel` bare = 0
for `gas`, 1 for `coal`, 2 for `oil` given `elements: [gas, coal, oil]`).

A set's `id` must not collide with (see [Rules for id naming](file-structure/library.md#rules-for-id-naming)):

- any parameter or variable `id` in the same model,
- any global set `id` visible in the same library (for a local set),
- the reserved literal `t`,

or a bare reference to that name would be ambiguous between "current index position", a
parameter/variable lookup, or the built-in time index.

### Collision check

- `[ ]` stays 100% reserved for time; never touched.
- `{ }` is currently unused anywhere in the grammar — zero syntactic overlap.
- `.` stays reserved for [ports](#ports).
- `sum_over` is a new name, distinct from `sum`, `sum(S..E,X)`, `sum_connections`, `expec`.
- `{` only ever appears immediately after an identifier (`X{...}`), never as the first character of
  the expression string, so it can't be misparsed as a YAML flow mapping.

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

