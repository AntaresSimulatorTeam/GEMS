# Roadmap

This page gives a high-level view of where the GEMS language and its ecosystem are heading. It is grouped into three horizons: **Now**, **Next**, and **Later**.

Looking for what has already shipped? Check the Release Notes for [the GEMS language](release-notes.md) and its two interpreters, [Antares Simulator](https://github.com/AntaresSimulatorTeam/Antares_Simulator/releases) and [GemsPy](https://github.com/AntaresSimulatorTeam/GemsPy/releases). If you have a feature you'd like to see prioritized, or a use case we should know about, open an issue or start a discussion on the [GitHub repository](https://github.com/AntaresSimulatorTeam/GEMS).

## Now

*In progress, or about to start.*

<div class="grid cards" markdown>

-   :material-shape-outline:{ .lg .middle } **Custom sets and dimensions**

    ---

    Let users define their own sets and dimensions, enabling (among other things) multi-horizon investment studies, specific demand-response constraints, advanced processes modelling, reserve modelling, and piecewise-linear costs.

    `Language`

-   :material-view-dashboard-outline:{ .lg .middle } **[ViewsBuilder](https://github.com/AntaresSimulatorTeam/GEMS-ViewsBuilder) integration with Antares Simulator & GemsPy**

    ---

    Connect the ViewsBuilder tool directly to Antares Simulator and GemsPy outputs.

    `Outputs & UI`

-   :material-speedometer:{ .lg .middle } **Warm start in GemsPy**

    ---

    Reuse a previous solution as a warm start to speed up GemsPy optimisation, matching a capability already available in Antares Simulator.

    `Performance`

</div>

## Next

*Planned after the Now items.*

<div class="grid cards" markdown>

-   :material-vector-line:{ .lg .middle } **Weighted connections**

    ---

    Allow connections between components to hold weights, enabling flow-based constraints and the modelling of advanced processes.

    `Language`

-   :material-ruler-square-compass:{ .lg .middle } **Units and dimensional analysis**

    ---

    Attach physical and monetary units (MW, MWh, €...) to variables and parameters, with automatic consistency checks.

    `Language`

-   :material-link-variant:{ .lg .middle } **Inter-block constraints and dynamics**

    ---

    Operators to declare dynamics and constraints across blocks, enabling policy constraints — such as security of supply or CO2 targets — to be handled inside decomposed investment problems.

    `Language`

-   :material-database-outline:{ .lg .middle } **Parquet data series**

    ---

    Support the Parquet file format for input data series, for faster loading and smaller files on large studies.

    `Language`


</div>

## Later

*Longer-term or exploratory.*

<div class="grid cards" markdown>

-   :material-monitor-dashboard:{ .lg .middle } **Graphical interface for studies**

    ---

    A graphical interface to browse, edit, and run GEMS studies, with dashboards and maps to visualize outputs.

    `UI`

-   :material-waves:{ .lg .middle } **Hydro pre-processing heuristics**

    ---

    Built-in heuristics for hydro reservoir management, including water value computation.

    `Language`

-   :material-chart-scatter-plot:{ .lg .middle } **Pareto fronts and sensitivity analysis**

    ---

    Native support for multi-objective Pareto front generation and sensitivity analysis on study parameters.

    `Language`

-   :material-source-branch:{ .lg .middle } **Cross-scenario operators**

    ---

    New language operators to work across scenarios, such as CVaR constraints and equality constraints between variables across scenarios.

    `Language`

</div>

??? note "This roadmap is a plan, not a promise"
    Items reflect current thinking, not a delivery commitment. Priorities can change based on community feedback, available effort, and technical findings along the way.
