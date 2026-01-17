<div style="display: flex; justify-content: space-between; align-items: center;">
  <div style="text-align: left;">
    <a href="../../../..">Main Section</a>
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

# Types of files and roles

These inputs are external files to the core software and consist of:

| **Type of File**   | **Domain**  | **File**        | **Description & Role**  |
|---------------------|-------------|-----------------|-------------------------|
| **[Model Libraries](../../3_User_Guide/3_GEMS_File_Structure/2_library.md)** | <span style="display:inline-block; width:12px; height:12px; background-color:#17A2B8; border-radius:50%; margin-right:5px;"></span>Abstract modelling | YAML (e.g., `basic-models-library.yml`, `antares-models-library.yml`)  |**Defines Models:** Abstract representations of system components to be simulated. **Models are defined in a library file** and specifies its ports, parameters, and internal behavior.These definitions can also include optional constraint and objective contributions used in simulation.|
| **[Taxonomy](../../3_User_Guide/3_GEMS_File_Structure/7_taxonomy.md)**| <span style="display:inline-block; width:12px; height:12px; background-color:#17A2B8; border-radius:50%; margin-right:5px;"></span>Abstract modelling| YAML (e.g., `taxonomy.yml`)| **Model Structure & Categories:** Specifies mandatory parameters, variables, ports, or extra outputs per category. Useful for structuring the UI (user interface) and simulation outputs.|
| **[System](../../3_User_Guide/3_GEMS_File_Structure/3_system.md)**  | <span style="display:inline-block; width:12px; height:12px; background-color:#D63384; border-radius:50%; margin-right:5px;"></span>System  | YAML  (`system.yml`) | **Defines Components:** Numerical instantiation of models, linking to model IDs (e.g., `example_library_id.example_model_id`). Specifies parameter values and connections between components via ports, forming the system graph.|
| **[Timeseries](../../3_User_Guide/3_GEMS_File_Structure/4_data_series.md)**  | <span style="display:inline-block; width:12px; height:12px; background-color:#D63384; border-radius:50%; margin-right:5px;"></span>System  | Dataseries (e.g., `wind_generation.csv`, `solar_generation.csv`)  | **Time-dependent Data:** Numerical data for parameters varying by time and scenario. Stored as `.csv` or `.tsv` files, typically in a data-series folder.|
| **Solution Workflow**| <span style="display:inline-block; width:12px; height:12px; background-color:#F8A055; border-radius:50%; margin-right:5px;"></span>Solution Workflow| YAML (`optim-config.yml`)| **Workflow Definition:** Describes calculation block processing (sequential, parallel, Xpansion frontale, Benders decomposition) and master problem constraints, especially for investment variables.|
|**[Optimization Parameters](../3_User_Guide/3_GEMS_File_Structure/6_solver_optimization.md)**| <span style="display:inline-block; width:12px; height:12px; background-color:#F8A055; border-radius:50%; margin-right:5px;"></span>Solution Workflow| YAML (`parameters.yml`)| **Solver & Configuration Settings:** Contains solver parameters and configuration required for running Modeler.|
| **[Business Views Configurations](../3_User_Guide/3_GEMS_File_Structure/8_business_view_configuration.md)**| <span style="display:inline-block; width:12px; height:12px; background-color:#8B5FB5; border-radius:50%; margin-right:5px;"></span>Business Intelligence| YAML (e.g., `business-view-def.yml`, `business-metric.yml`) | **Business Metrics Logic:** Calculates business metrics from simulation results in two phases: Step 1 (component scope, complex arithmetic), Step 2 (global scope, aggregation/filtering).|

# Files Interaction

The following scheme shows the interaction of the different core concepts presented previously. It is based on the [*basic-model-library*](https://github.com/AntaresSimulatorTeam/GEMS/blob/main/libraries/basic_models_library.yml) included in this documentation.

<p align="center">
    <img src="../../../assets/6_GEMS_architecture.png" alt="GEMS Architecture Diagram">
</p>

<br/>
<br/>

## Illustration with an example

To get familiar with these concepts, see the table below for a correspondence between theoretical concepts and examples from a thermal plant use case from the [basic_models_library](https://github.com/AntaresSimulatorTeam/GEMS/blob/main/libraries/basic_models_library.yml):

|Concept|Example|
|-|-|
|Library|Library (`basic_models_library`) where generator model is defined|
|Model |The `generator` model |
|Component|A specific thermal plant, like a 300MW CCGT Thermal plant from `generator` model|
|Variable|Actual dispatched power ; `generation` from *generator model* |
|Parameter|The `generation_cost` (specific for each thermal plant, to be entered by the users)|
|Field|The field `flow` is exchanged through *balance_port*|
|Port|The `balance_port` let the power *flow* be transferred|
|Connection|A link between a generation unit and a node representing the injection from the plant to the energy system's node|
|Constraint|Value interval accepted for power generation|
|Binding Constraints|Energy balance inside an area|
|Scenario dependency| The maximum power output `p_max` can depend on the scenario chosen by the users (and also depends on the time)|
|Time dependency|`p_max` is a time dependent parameter (and also depends on the scenario)|

# Outputs File (generated by a Gems interpreter)

The outputs of GEMS consist of three main categories of objects: **Optimization Problem**, **Simulation Table** and **Business Views**. Their structure is detailed in the [User Guide section](../../3_User_Guide/1_syntax.md#outputs).

- **Optimization Problem** represents the global mathematical formulation of the energy system simulation/optimization.
- **Simulation Table** contains the raw results of the simulation or optimization, including the optimal values of decision variables and the values of expressions computed from them.
- **Business Views** provide curated representations of the simulation or optimization results from a business-intelligence perspective, tailored to users [specific needs](../../3_User_Guide/1_syntax.md#outputs).

---

**Navigation**

<div style="display: flex; justify-content: space-between;">
  <div style="text-align: left;">
  <button type="button" style="background-color:#CCCCCC; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
    <a href="../1_Architecture" style="text-decoration:none; color: #000000">⬅️ Previous page</a>
  </button>
  </div>
  <button type="button" style="background-color:#AAAAFF; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
    <a href="../../../.." style="text-decoration:none; color: #FFFFFF">Home</a>
  </button>
  <div style="text-align: right;">
  <button type="button" style="background-color:#CCCCCC; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
    <a href="../3_Difference_with_other_languages" style="text-decoration:none; color: #000000">Next page ➡️</a>
  </button>
  </div>
</div>