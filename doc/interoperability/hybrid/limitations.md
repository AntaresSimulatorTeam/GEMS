---
description: Known limitations of the GEMS hybrid mode in Antares Simulator — current restrictions on component types, connections, and features in hybrid studies.
tags:
  - Interoperability
  - Hybrid Studies
---

<div style="display: flex; justify-content: flex-end;">
  <a href="../..">
    <img src="../../../assets/gemsV2.png" alt="GEMS Logo" width="150"/>
  </a>
</div>

# Limitations

When constructing hybrid studies, the following important constraints should be considered:

**Time Series Length:**

The time series data used in GEMS modeler components (for example, the generation profile of a renewable) must align with the Antares simulation horizon and resolution. In practice, this means the number of time steps and the granularity of GEMS time-dependent inputs should match the solver's expectations (e.g., 8760 hourly values for a yearly hourly simulation). The hybrid solver will not accept a modeler time series that doesn't fit the configured simulation timeframe.

**Integer/Binary Decision Variables:**

If any GEMS component introduces integer or binary decision variables (for instance, a component that has an on/off state or unit commitment logic), Antares must be run in MILP mode. Antares Simulator's solver has to be set to Mixed-Integer Linear Programming (the unit commitment MILP option) to handle discrete variables. In hybrid mode, the solver will incorporate those binary/integer variables into the optimization, but only if the MILP solver is enabled. If running with continuous (LP) mode while using components that require integer decisions, the simulation will not handle them correctly. Thus, the study's optimization settings must be configured for MILP (unit commitment) when needed.

**Scenario dependency of Variables**:
In Antares Simulator Legacy mode, each MC scenario is optimized separately. Thus, hybrid studies cannot contain scenario-independent variables. If you try to use such a variable in hybrid mode, the solver will fail.
