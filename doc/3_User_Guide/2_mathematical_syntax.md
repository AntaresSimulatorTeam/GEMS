<div style="display: flex; justify-content: space-between; align-items: center;">
  <div style="text-align: left;">
    <a href="../../../..">Main Section</a>
  </div>
  <div style="text-align: right;">
    <img src="../../assets/gemsV2.png" alt="GEMS Logo" width="150"/>
  </div>
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

Ports are the mechanism by which models exchange linear expressions. A port has one or more fields with each field carrying a linear expression. **Mathematical Expression Syntax**  allows users to reference port fields in expressions using the notation `port_id.field_id`. This is essentially a way to use linear expressions coming from other connected models.

When using a port field in an expression, the same dependency rules apply: if linear expressions of a port varies by time or scenario (which is deduced from how it’s defined – typically depending on time-dependent variables or parameters), then it can only be used in time-dependent or scenario-dependent constraints respectively.

If a port’s linear expressions need to be used in a time-independent manner (for example, when calculating a sum over the full time horizon), an aggregator must be applied to remove the time index. See the section on the [**Time Summation Operator**](#time-summation-full-horizon-sumx) for details. A practical implementation is provided in [`basic_models_library.yml`](https://github.com/AntaresSimulatorTeam/GEMS/blob/main/libraries/basic_models_library.yml) where the `emmision_port` is used to support pollutant-related constraints.

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
expression: levels[t+1] = levels + injection - withdrwal
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

---
**Navigation**

<div style="display: flex; justify-content: space-between;">
    <div style="text-align: left;">
    <button type="button" style="background-color:#CCCCCC; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
        <a href="../1_introduction" style="text-decoration:none; color: #000000">⬅️ Previous page</a>
    </button>
    </div>
    <button type="button" style="background-color:#AAAAFF; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
        <a href="../../../.." style="text-decoration:none; color: #FFFFFF">Home</a>
    </button>
    <div style="text-align: right;">
    <button type="button" style="background-color:#CCCCCC; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
        <a href="../3_GEMS_File_Structure/1_overview" style="text-decoration:none; color: #000000">Next page ➡️</a>
    </button>
    </div>
</div>

---

