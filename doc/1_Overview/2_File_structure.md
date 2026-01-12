<div style="display: flex; justify-content: space-between; align-items: center;">
  <div style="text-align: left;">
    <a href="../../index.md">Main Section</a>
  </div>
  <div style="text-align: right;">
    <img src="../../../assets/gemsV2.png" alt="GEMS Logo" width="150"/>
  </div>
</div>


# File Overview : Model, System, Optimization, Business

The GEMS architecture enforces a structured approach, separating modelling logic, system configuration, optimization workflow, and business intelligence into four distinct "bounded domains" (see the following definition diagram):

Users primarily interact with GEMS by defining the **system to be simulated or optimized** through external configuration files that describe components, constraints, and operating conditions.
During execution, an internal process may automatically construct an optimization problem from this system description and pass it to an external solver when required, but this remains an implementation detail rather than the primary user concern.


<div style="display: flex; justify-content: center; align-items: center; height: 500px; overflow: hidden;">
  <img src="../../assets/domains.png" alt="File structure" style="height: 100%; object-fit: contain;"/>
</div>

<br>

# Role of each File Type

These inputs are external files to the core software and consist of:

| **Type of File**   | **Domain**  | **File**        | **Description & Role**  |
|---------------------|-------------|-----------------|-------------------------|
| **Model Libraries** | <span style="display:inline-block; width:12px; height:12px; background-color:#17A2B8; border-radius:50%; margin-right:5px;"></span>Abstract modelling | YAML (e.g., `basic-models-library.yml`, `antares-models-library.yml`)  |**Defines Models:** Abstract representations of system components to be simulated. **Models are defined in a library file** and specifies its ports, parameters, and internal behavior.These definitions can also include optional constraint and objective contributions used in simulation. |
| **System**  | <span style="display:inline-block; width:12px; height:12px; background-color:#D63384; border-radius:50%; margin-right:5px;"></span>System  | YAML  (`system.yml`) | **Defines Components:** Numerical instantiation of models, linking to model IDs (e.g., `example_library_id.example_model_id`). Specifies parameter values and connections between components via ports, forming the system graph. |
| **Timeseries**  | <span style="display:inline-block; width:12px; height:12px; background-color:#D63384; border-radius:50%; margin-right:5px;"></span>System  | Dataseries (e.g., `wind_generation.csv`, `solar_generation.csv`)  | **Time-dependent Data:** Numerical data for parameters varying by time and scenario. Stored as `.csv` or `.tsv` files, typically in a data-series folder.  |
| **Taxonomy**             | <span style="display:inline-block; width:12px; height:12px; background-color:#17A2B8; border-radius:50%; margin-right:5px;"></span>Abstract modelling        | YAML (e.g., `taxonomy.yml`)                | **Model Structure & Categories:** Specifies mandatory parameters, variables, ports, or extra outputs per category. Useful for structuring the UI (user interface) and simulation outputs.                             |
| **Solution Workflow**    | <span style="display:inline-block; width:12px; height:12px; background-color:#F8A055; border-radius:50%; margin-right:5px;"></span>Solution Workflow        | YAML (`optim-config.yml`)            | **Workflow Definition:** Describes calculation block processing (sequential, parallel, Xpansion frontale, Benders decomposition) and master problem constraints, especially for investment variables.                   |
| **Business Views Configurations**       | <span style="display:inline-block; width:12px; height:12px; background-color:#8B5FB5; border-radius:50%; margin-right:5px;"></span>Business Intelligence    | YAML (e.g., `business-view-def.yml`, `business-metric.yml`) | **Business Metrics Logic:** Calculates business metrics from simulation results in two phases: Step 1 (component scope, complex arithmetic), Step 2 (global scope, aggregation/filtering).                             |
| **Parameters**           | <span style="display:inline-block; width:12px; height:12px; background-color:#F8A055; border-radius:50%; margin-right:5px;"></span>Solution Workflow                | YAML (`parameters.yml`)              | **Solver & Configuration Settings:** Contains solver parameters and configuration required for running Modeler.                                                                                                |

# Files Interaction

The following scheme shows the interaction of the different core concepts presented previously. It is based on the [*basic-model-library*](../../../libraries/basic_models_library.yml) included in this documentation.

<p align="center">
    <img src="../../../assets/6_GEMS_architecture.png" alt="GEMS Architecture Diagram">
</p>

<br/>
<br/>

# Outputs File (generated by a Gems interpreter)

The outputs of GEMS consist of three main categories of objects: **Optimization Problem**, **Simulation Table** and **Business Views**. Their structure is detailed in the [User Guide section](../../3_User%20Guide/1_syntax.md#outputs).

- **Optimization Problem** represents the global mathematical formulation of the energy system simulation/optimization.
- **Simulation Table** contains the raw results of the simulation or optimization, including the optimal values of decision variables and the values of expressions computed from them.
- **Business Views** provide curated representations of the simulation or optimization results from a business-intelligence perspective, tailored to users [specific needs](../../3_User%20Guide/1_syntax.md#outputs).

---

**Navigation**

<div style="display: flex; justify-content: space-between;">
  <div style="text-align: left;">
  <button type="button" style="background-color:#CCCCCC; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
    <a href="../1_core concepts" style="text-decoration:none; color: #000000">⬅️ Previous page</a>
  </button>
  </div>
  <button type="button" style="background-color:#AAAAFF; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
    <a href="../../../../.." style="text-decoration:none; color: #FFFFFF">Index</a>
  </button>
  <div style="text-align: right;">
  <button type="button" style="background-color:#CCCCCC; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
    <a href="../3_features_usecase" style="text-decoration:none; color: #000000">Next page ➡️</a>
  </button>
  </div>
</div>