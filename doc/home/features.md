---
description: What the GEMS language supports today - graph-based modelling, native time and scenario dimensions, LP/MIP/MILP and two-stage stochastic optimisation, granular outputs.
---

# Features 

This page summarises what the GEMS language and format support **today**, and the kinds of studies they were designed for.

For what is being worked on next, see the [Roadmap](roadmap.md). For the history of changes, see the [Release Notes](release-notes.md).


<div class="grid cards" markdown>

-   :material-graph-outline:{ .lg .middle } **Systems as graphs of connected components**

    ---

    Define abstract models once in a library, instantiate them as components, and connect them through typed ports. 

    `Language`

    [:octicons-arrow-right-24: Library file](../user-guide/file-structure/library.md)

-   :material-function-variant:{ .lg .middle } **Readable, math-like expression syntax**

    ---

    Write equations as text close to the mathematics, to encode your own models with custom constraints, or use reference libraries of models.

    `Language`

    [:octicons-arrow-right-24: GEMS syntax](../user-guide/syntax.md)

-   :material-vector-polyline:{ .lg .middle } **LP, MIP and MILP problems**

    ---

    Variables can be continuous, integer or binary, with bounds given by parameters or expressions. Discrete operational decisions (e.g. unit commitment, start-up and shut-down logic) are expressed directly in the model.

    `Solving`

    [:octicons-arrow-right-24: Variables](../user-guide/file-structure/library.md#variables)


-   :material-swap-horizontal:{ .lg .middle } **Solver-agnostic by design**

    ---

    Model equations live in YAML files, never in software code, and are interpreted at run time. The optimisation solver is a configuration choice with solver-specific options passed through.

    `Solving`

    [:octicons-arrow-right-24: Solver configuration](../user-guide/file-structure/solver-optimization.md)


-   :material-clock-outline:{ .lg .middle } **Time as a native dimension**

    ---

    No index sets to declare for time: refer to the current time step, shift it forward or backward for storage and ramping dynamics, and aggregate over the full horizon or a moving window. 

    `Language`

    [:octicons-arrow-right-24: Time operators and indexing](../user-guide/syntax.md#time-operators-and-indexing)

-   :material-dice-multiple-outline:{ .lg .middle } **Uncertainty as a native dimension**

    ---

    Parameters and variables can vary by scenario alongside time, and the expectation operator aggregates across the scenario dimension: the basis for Monte Carlo studies and for coupling scenarios through 2-stage stochastic formulations.

    `Language`

    [:octicons-arrow-right-24: Scenario operator](../user-guide/syntax.md#scenario-operator)


-   :material-trending-up:{ .lg .middle } **Investment and two-stage stochastic optimisation**

    ---

    A model can declare several objective contributions belonging to different optimisation stages, separating investment (here-and-now) from operation (recourse). This is what makes capacity-expansion studies and Benders-style decomposition expressible in the language.

    `Solving`

    [:octicons-arrow-right-24: Objective contributions](../user-guide/file-structure/library.md#objective-contribution)

-   :material-view-week-outline:{ .lg .middle } **Block decomposition of the horizon**

    ---

    A long horizon can be solved in successive blocks rather than as one monolithic problem, the basis for rolling-horizon resolution. Every result carries the block it came from. 

    `Solving`

    [:octicons-arrow-right-24: The `block` column](../user-guide/outputs/simulation-table.md)
    
-   :material-file-table-outline:{ .lg .middle } **Scenario building from data series**

    ---

    Time-dependent, scenario-dependent and time × scenario data live in plain CSV files. The scenario builder maps each Monte Carlo scenario to a data series column per scenario group, so the same system can be replayed against different datasets.

    `Data`

    [:octicons-arrow-right-24: Scenario builder](../user-guide/file-structure/scenario-builder.md)
    
-   :material-tag-outline:{ .lg .middle } **Component properties and metadata**

    ---

    Attach arbitrary key/value properties to components (e.g. carrier, technology, operator) either declared by the model or added freely. They are available downstream for filtering, aggregation and visualisation.

    `Data`

    [:octicons-arrow-right-24: Component properties](../user-guide/file-structure/system.md#properties)



-   :material-table-large:{ .lg .middle } **Full, granular results**

    ---

    One flat table holds the value of every variable, constraint, port field and extra output, identified by component, time step and scenario. It includes duals and reduced costs for marginal prices, and user-defined extra outputs evaluated after the solve.

    `Outputs`

    [:octicons-arrow-right-24: Simulation table](../user-guide/outputs/simulation-table.md)


</div>

