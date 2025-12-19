<div style="display: flex; justify-content: space-between; align-items: center;">
  <div style="text-align: left;">
    <a href="../../../..">Main Section</a>
  </div>
  <div style="text-align: right;">
    <img src="../../../assets/gemsV2.png" alt="GEMS Logo" width="150"/>
  </div>
</div>

# GEMS Mathematical Expression Syntax

GEMS includes a **Mathematical Expression Syntax** that allows modelers to write equations for optimization problems in a clear, math-like syntax within configuration files. **Mathematical Expression Syntax** is independent of any programming code – model equations are specified as human-readable text, which GEMS interprets to build the mathematical optimization problem.

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

These operate with conventional precedence (multiplication and division bind tighter than addition and subtraction). You may use parentheses (...) to group sub-expressions as needed for clarity or to override precedence.

### Comparison Operators

Comparison operators are used to form constraints (equations or inequalities).

| Operator | Description | Example|
|------|--------------------------| ---------------|
| `=`| Used in constraint definitions to enforce equality  | `var1 = var2` |
| `<=` | Used in constraints to require `LHS ≤ RHS` |`var 1 <= var2`|
| `>=` | Used in constraints to require `LHS ≥ RHS` | `var 1 >= var2`|

**Important:** Comparison operators are only allowed in constraint expressions (not in general arithmetic expressions). Each constraint expression must contain exactly one comparison operator (`=`, `<=`, or `>=`)
 dividing the expression into a left-hand side (LHS) and right-hand side (RHS). Chained comparisons (e.g. `A <= B <= C`) are not permitted; if needed, break them into separate constraints.

GEMS framework **Mathematical Expression Syntax** does not support certain operations common in programming or math notation. For example, non-linear functions (log, sin, etc.) are not part of the expression syntax. If a mathematical relationship is non-linear, it must be linearized or reformulated.

Throughout the following sections several advanced operators that will be referenced as they become relevant to each topic.

## Numeric Constants (Literals)

Numeric constants can be used anywhere in an expression. Literals may be written as integers or floats (use . for a decimal point). For example, all of the following are valid constants: `42`, `0.5`, `3.14`, `100.0`.

**Example:**

```yaml
expression: 3 * 66.32 - 5 / 3.14
```

This expression uses literal constants (`67.43`, `5`, `3.14`) in a valid way. Constants can appear in any part of an expression, either standalone or multiplied/divided with other terms.

## Parameters

**Parameters** represent fixed input data values (not decision variables) that can be referenced by their `ID` as a simbol to include it's value in expressions. For example:

```yaml
expression: 3 * parameter_1 + 6.345 / parameter_2
```
This would use the numeric value of `parameter_1` and `parameter_2` as provided in the system input data.

Parameters can be time-dependent (having a separate value for each time step of the simulation horizon) or scenario-dependent (having different values under different scenario cases), or both. If a parameter is time-dependent, think of it as a series **`p(t)`** over time; if scenario-dependent, as **`p(s)`** varying by scenario; it can even be **`p(t,s)`** if varying across both dimensions.

You can use parameters freely in arithmetic operations. Since parameters are constants from the solver’s perspective (their values are fixed input), they may appear in linear or non-linear positions without violating linearity rules. For instance, multiplying two parameters or dividing by a parameter is allowed. However, dividing by a parameter that could be zero should be avoided, as this would create an undefined expression in some cases (ensure your data never gives zero for such parameters).

## Variables

Variables correspond to the decision variables of the optimization. All variables are referenced by their `ID` in expressions, just like parameters. For example, if a model defines a variable with `id: generation`, you can use `generation` in an expression:
```yaml
expression: generation * generation_cost
```
In such use, `generation` represents the variable’s value, and `cost_per_unit` is a parameter.

Variables can be **continuous**, **integer** or **binary**.

A crucial rule is that all expressions must be linear. This means non-linear combinations of variables are not allowed. Each term in an expression can be at most a variable multiplied by a constant or parameter. The expression cannot include products or divisions where a variable appears in a non-linear way. Violating this will result in an invalid model definition.


Some examples of prohibited expressions (non-linear in variables):

- `variable_a * variable_b` – product of two variables

- `3 / variable_a` – a variable in the denominator (non-linear reciprocal)

- `binary_var * continuous_var` – product of two variables, even if one is binary (still nonlinear)


### Time and Scenario Dependence of Variables 
In GEMS, variables inherently can have a value for each time step (and scenario) unless defined or used in a way that makes them constant. If a variable is time-dependent, it means conceptually there is a vector of that variable across the simulation timeline (e.g. x<sub>t</sub> for each hour t). Likewise, a scenario-dependent variable has independent values per scenario s. The **Mathematical Expression Syntax** does not require writing an index for a time-dependent variable in most cases; instead, the context of the constraint or objective will determine how it’s applied (explained under **Time Operators**).

If a variable is time-dependent (or scenario-dependent), it can only be used in a constraint that is also time-dependent (or scenario-dependent), or else aggregated appropriately. In practice, this means if you include a time-indexed variable in an expression, that expression is treated as a separate equation at each time step by default (the model interpreter "unfolds" the equation over time). Similarly, scenario-indexed variables lead to constraints unfolding per scenario.

## Ports

In GEMS, ports are the mechanism by which models/components exchange values. A port has one or more fields (each field carrying a numeric value, e.g. a power flow, a voltage, etc.). **Mathematical Expression Syntax**  allows you to reference port fields in expressions using the notation `port_id.field_id`. This is essentially a way to use values coming from other connected components or to define the values sent out via this model’s ports.

When using a port field in an expression, the same dependency rules apply: if the port’s value varies by time or scenario (which is deduced from how it’s defined – typically depending on time-dependent variables or parameters), then it can only be used in time-dependent or scenario-dependent constraints respectively. If you need to use a port’s value in a time-constant way (e.g. summing over time), you must apply an aggregator to remove the time index.

### Port Operator

A single port on a model can have multiple connections feeding into it (multiple components can connect to the same port of this component). To aggregate all incoming values of a port field, **Mathematical Expression Syntax**  provides a special operator:

- `sum_connections(port.field)` – this returns the sum of the specified field across all incoming connections to the given port. It effectively adds up the values of that field from every other component connected to the port. The result of sum_connections can be used like any other term in an expression. If there are no incoming connections, the sum is simply 0.

Use `sum_connections` in constraints that need the combined effect of multiple inputs. For example, a balance node model might require that the sum of all power flows equals zero (First Kirchhoff Law). Assuming the port is injections and the field is flow, the model’s constraint could be:

```yaml
expression: sum_connections(injections.flow) = 0
```
This single constraint will enforce that the total of flow from all connected components on port injections is zero.

### Direct port.field usage
If you know a port has exactly one connection (or you want to treat a single connection's value), you could reference `port_id.field_id` directly in an expression. However, for generality and clarity, it is recommended to use `sum_connections` even for single-connection cases – it makes the intent clear and will also handle multiple connections if the model is extended.

Similar to variables, port field values must enter expressions linearly. Since a port field ultimately either comes from another model’s variable or is defined by a linear expression in this model, using `port.field` in linear combinations is fine, but you cannot, for example, multiply two port fields together or divide by a port field (these would imply non-linear relationships and are not allowed, just as with variables).

## Time Operators and Indexing

Many model quantities in GEMS vary over a timeline (e.g., hourly production over a year). **Mathematical Expression Syntax**  provides convenient time operators to refer to specific time-indexed values or to aggregate over time. These operators apply to time-dependent parameters, variables, or port fields:

###  **Current time step** `[t]`: 
This optional suffix denotes the value at the current time index. It is implied by default, meaning if you use a time-dependent element in a time-indexed constraint, you need not explicitly write [t] – the system assumes the current time step’s value.However, you can include it for clarity. For example, `demand[t]` explicitly refers to the demand at time t, and is equivalent to just demand when used in a time-dependent context.

###  **Explicit index** `[N]`: 
Using an integer expression N in square brackets accesses the value at the N-th time step. For instance, `X[5]` refers to the value of time-dependent element *X* at the *5th* time period. The index N can itself be an expression involving only scalars and parameters (no variables) that resolves to an integer. This allows flexible indexing; e.g., `X[parameter_idx]` if `parameter_idx` is an integer parameter. This is useful for referring to specific periods (like a particular hour or year) in an equation. Note that time indices are 1-based (typically, 1 = first time step).

###  **Relative shift** `[t+N] / [t-N]`: 
This allows shifting the time index forward or backward by N steps. For example, `X[t+1]` is the value of `X` at the next time step, and `X[t-1]` is the previous time step. The offset N can be an expression (using scalars/parameters) that evaluates to an integer. Depending on the study time semantics, shifted indices (e.g. `[t+1]` at the last timestep) may wrap around to keep the horizon periodic.
This is commonly used for cyclic constraints such as storage dynamics.
```yaml
expression: levels[t+1] = levels + injection - withdrwal
```
Now, it can be concluded that expression `levels[T+1]` is equal to `levels[0]`.

### **Time summation (full horizon)** `sum(X)`:

Denotes the sum of the time-dependent operand X over the entire optimization horizon. If X is defined for each time step from 0 to T-1, then sum(X) produces a single scalar equal to $\sum_{t=0}^{T-1} X_t$. This is useful for objectives or constraints involving total amounts (e.g., total annual production).

### **Time summation (range)** `sum(S .. E, X)`:

Sums the operand X from time S to time E.

Here `S` and `E` can be either:

- A constant or parameter expression that resolves to a time index

- A relative expression involving t. For example, `sum(t-3 .. t, X)` would sum X from 3 periods ago up to the current period t. Both `S` and `E` are evaluated as integers. This form allows moving window calculations (e.g., sum over a rolling horizon up to the current time).

Using these time operators, you can create advanced temporal constraints. For example:

```yaml
# Enforce that each period's production <= average of next 3 periods
expression: production[t] <= (1/3) * sum(t+1 .. t+3, production)
```

## Constraints

A constraint is described by a single expression containing a comparison (`=`, `<=`, or `>=`). The left and right sides of that comparison are linear expressions as discussed above. Here are the key points about constraints:

- A constraint must have exactly one comparison operator dividing the expression. For example: `generation <= capacity` or `supply = demand`.
- The expression on each side of operators `=/<=/>=` can include any allowed terms: constants, parameters, variables, port fields (subject to the linearity and dependency rules). Both sides of the comparator are evaluated and the inequality/equality enforced by the solver.

**Example:** In the generator model example below, an internal constraint ensures the generator’s minimum output when it’s on:

```yaml
expression: active_power >= is_on * min_active_power
```

### Time-Dependent Constraints vs. Aggregation

If a constraint expression includes any time-indexed element (e.g. a time-dependent variable), that constraint implicitly applies at each time step across the horizon. In other words, the model interpreter "unfolds" it into a series of constraints, one per period `t`. To instead enforce a single aggregate constraint across time, you must eliminate the free t index by using a `sum(...)` aggregator. For example, `x[t] <= 100` in a constraint would apply for every time step `t`. But `sum(x) <= 100` applies once, to the total sum over time.



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

GEMS can handle multiple scenarios (two stage stochastic) for data and variables. Scenario-dependent parameters or variables have values that differ by scenario (similar to having an extra scenario index s). **Mathematical Expression Syntax**  currently provides an operator to aggregate across the scenario dimension:

- **expec(X)** aggregator: where `X` is the scenario-dependent operand, this operator computes its expected value (i.e. its scenario-wise average).


### Dual Operators

In some cases, there is a  need to access dual results of variables / constraints of the linear problem. Depending on the case, the dual unary operator is :

- dual result of a variable whose id is my_var is accessed by `-reduced_cost(variable_id)`
- dual result of a constraint whose if is my_constraint is accessed by `dual(constraint_id)`

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
expression: paramter_1 < max(parameter_2, 100)
```

 In the context of a extracting results, its operands can be literals, parameters or varibles.
```yaml
expression: min(variable_1, parameter_1)
```

---
**Navigation**
<div style="display: flex; justify-content: space-between;">
  <div style="text-align: left;">
  <button type="button" style="background-color:#CCCCCC; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
    <a href="previous.md" style="text-decoration:none; color: #000000">⬅️ Previous page</a>
  </button>
  </div>
  <button type="button" style="background-color:#AAAAFF; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
    <a href="Home/Main_Home/1_context_GEMS.md" style="text-decoration:none; color: #FFFFFF">Index</a>
  </button>
  <div style="text-align: right;">
  <button type="button" style="background-color:#CCCCCC; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
    <a href="next.md" style="text-decoration:none; color: #000000">Next page ➡️</a>
  </button>
  </div>
</div>

---

© GEMS (LICENSE)