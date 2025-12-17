<div style="display: flex; justify-content: space-between; align-items: center;">
  <div style="text-align: left;">
    <a href="folder1/home1.md">Main Section</a>
  </div>
  <div style="text-align: right;">
    <img src="../../assets/gemsV2.png" alt="GEMS Logo" width="150"/>
  </div>
</div>

*This section coms from Overview.concepts file*

# GEMS Mathematical Expression Syntax

GEMS includes a **Mathematical Expression Syntax** that allows modelers to write equations for optimization models in a clear, math-like syntax within configuration files
. This language is independent of any programming code – model equations are specified as human-readable text, which GEMS interprets to build the mathematical optimization problem.

In this section, we detail the **Mathematical Expression Syntax**, supported operators, linearity requirements, use of parameters/variables/ports, time and scenario indexing, aggregation functions, constraint forms, naming rules, and some modeling best practices.


## Operators

Operators can be divided into three groups:

- **Arithmetic Operators**
- **Comparison Operators**
- **Advance Operators**

### Arithmetic Operators
Mathematical expressions use standard arithmetic notation. The following binary arithmetic operators are supported:


| Operator | Example |
|------|--------------------------|
| Addition| A + B |
| Subtraction | A - B |
| Multiplication | A * B |
| Division | A / B |

These operate with conventional precedence (multiplication and division bind tighter than addition and subtraction). You may use parentheses (...) to group sub-expressions as needed for clarity or to override precedence.

### Comparison Operators

Comparison operators are used to form constraints (equations or inequalities).

| Operator | Description | Example|
|------|--------------------------| ---------------|
| Equality `=`| Used in constraint definitions to enforce that left-hand side equals right-hand side | `var1 = var2` |
| Less-than-or-equal `<=` | Used in constraints to require `LHS ≤ RHS` | `var 1 <= var2`|
| Greater-than-or-equal `>=` | Used in constraints to require `LHS ≥ RHS` | `var 1 >= var2`|

Important: Comparison operators are only allowed in constraint expressions (not in general arithmetic expressions). Each constraint expression must contain exactly one comparison operator (`=`, `<=`, or `>=`)
 dividing the expression into a left-hand side (LHS) and right-hand side (RHS). Chained comparisons (e.g. `A <= B <= C`) are not permitted; if needed, break them into separate constraints.

### Advance Operators

TODO : dual, reduced_cost, pow, min, max


GEMS framework **Mathematical Expression Syntax** does not support certain operations common in programming or math notation. For example, exponentiation (^ or **), modul, and non-linear functions (log, sin, etc.) are not part of the expression syntax. Only the operators listed above can be used. If a mathematical relationship is non-linear, it must be linearized or reformulated.

# Dataseries
Currently, the framework supports defining **dataseries** using tab-seperated-values files. Values must be separated using tabs, and the character `.` represents the floating point.

## Scenario / Time Dependency
Inside the YAML files, **Parameters, Variables, and Constraints** can be dependent on the scenario and/or over time.
- A **scenario dependency** means, for instance, that the *parameter* `fixed_cost` for starting up a plant can depend on the chosen scenario.

    A simulation with 4 scenarios will get :
    `54 67.5 23.652 253`
- A **time dependent** *parameter* can be for instance `max_active_power_set_point` dependending on plant maintenancy. A time dependency needs a dataserie for getting data

    A simulation with 4 timestamps will get :
    ```
    54 
    67.5 
    23.652 
    253```

# Outputs

## Taxonomy 

![Taxonomy scheme](../assets/6_taxonomy.png)

The outputs of GEMS contain the results of the modelisation, in a LP format (**Optimization Problem**) and for hybrid and pure modeler studies in CSV format (**simulation table**), there are also **extra-outputs**. Their structure is detailed inside UserGuide section.

- **Optimization Problem**
    The optimization model solved by Antares modeler is written in the human-readable LP format, under output/problem.lp. It is only meant to be used for debugging.

- **Simulation Table**
    Antares Simulator (hybrid and modeler modes) produces detailed optimization results for the modeler's components, in the "simulation table", in CSV format

    - **Extra Outputs**
        Extra-Outputs computed after optimization (using optimal variable values). These appear in the output files alongside variable and port values inside the simulation table.

- **Business Views**
    Output files with metrics specifically designed for users purposes. It made from the simulation table.
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