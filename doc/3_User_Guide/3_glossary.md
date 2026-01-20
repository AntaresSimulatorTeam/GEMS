<div style="display: flex; justify-content: space-between; align-items: center;">
  <div style="text-align: left;">
    <a href="../../../..">Main Section</a>
  </div>
  <div style="text-align: right;">
    <img src="../../../assets/gemsV2.png" alt="GEMS Logo" width="150"/>
  </div>
</div>

# Glossary

This section is a glossary of the main concepts used by GEMS.

## Input Files

| Term    | Definition    |
|---------|---------------|
| [Library](./3_GEMS_File_Structure/2_library.md) | A file listing all the models representing general unspecified elements of a study. These models are used as "template" for creating their instances, called components|
| [System](./3_GEMS_File_Structure/3_system.md)  | A file listing all the "components", the instances of models defined by the system yaml file, representing all the specified elements of the simulated grid. This file also contains all the connections between the components|
| [Dataseries](./3_GEMS_File_Structure/4_data_series.md) | A table containing all the data through time. It is used by time/scenario dependent components|

## Concepts

### Models and Components

| Concept     | Definition    |
|-------------|---------------|
|[Model](./3_GEMS_File_Structure/2_library.md#models)| An abstract mathematical configuration representing the general features of a category of grid element. Users can specify any instance of this model for creating each simulated grid's element  |
|[Component](./3_GEMS_File_Structure/3_system.md#components)| An instance using a model as a template. Each component is a specific detailed instance of a model representing a real object. Multiple components can use the same model within a system, each with different parameter values |

### Abstract modelling: Optimization 

| Concept              | Definition        |
|----------------------|-------------------|
| [Variable](./2_mathematical_syntax.md#variables)             | An abstract mathematical variable of a model, whose value is optimized by the solver. The optimization problem is to find the best set of variables based on the variable's configuration, shared across all model instances. |
| [Parameter](./2_mathematical_syntax.md#parameters)            | An input data declared in the model, with a value specific to each component (set in the system.yml file). The optimization problem seeks the best set of variables according to these parameters.               |
| [Objective function](./2_mathematical_syntax.md#objective-function)   | The mathematical expression optimized by the solver. Variables are selected to achieve its global minimum based on the input parameters. |

### Interfaces and Relationships

| Concept            | Definition        |
|--------------------|-------------------|
| [Port](./3_GEMS_File_Structure/2_library.md#ports)| A communication interface for exchanging expressions, called "fields"     |
| [Field](./3_GEMS_File_Structure/2_library.md#ports) | An expression exchanged by a port    |
| [Constraint](./3_GEMS_File_Structure/2_library.md#constraints)| A mathematical relationship or condition that restricts the values of variables |
| [Binding Constraint](./3_GEMS_File_Structure/2_library.md#binding-constraints) | A constraint that links variables or ports across different models or components |
| [Connection](./3_GEMS_File_Structure/3_system.md#connections)| A link between two components' ports |

### Time and Scenario Dependency

| Concept            | Definition            |
|--------------------|-----------------------|
| Time dependent     | A parameter depending on time. In this case, the parameters are represented as a dataseries|
| Scenario dependent | A parameter or variable depending on the scenario. In this case, the parameter is instantiated as as a dataseries. |

---
**Navigation**
<div style="display: flex; justify-content: space-between;">
  <div style="text-align: left;">
  <button type="button" style="background-color:#CCCCCC; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
    <a href="../5_Outputs/3_business_view" style="text-decoration:none; color: #000000">⬅️ Previous page</a>
  </button>
  </div>
  <button type="button" style="background-color:#AAAAFF; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
    <a href="../../../.." style="text-decoration:none; color: #FFFFFF">Index</a>
  </button>
  <div style="text-align: right;">
  <button type="button" style="background-color:#CCCCCC; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
    <a href="../../4_Interoperability/1_pypsa" style="text-decoration:none; color: #000000">Next page ➡️</a>
  </button>
  </div>
</div>

---

© GEMS (LICENSE)
