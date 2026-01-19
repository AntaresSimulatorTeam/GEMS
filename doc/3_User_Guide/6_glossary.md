
<div style="display: flex; justify-content: space-between; align-items: center;">
  <div style="text-align: left;">
    <a href="../../../..">Main Section</a>
  </div>
  <div style="text-align: right;">
    <img src="../../../assets/gemsV2.png" alt="GEMS Logo" width="150"/>
  </div>
</div>

# Glossary

## Input Files

| Term    | Definition    |
|---------|---------------|
| Library | A file listing all the models representing general unspecified elements of a study. These models are used as "template" for creating their instances, called components|
| System  | A file listing all the "components", the instances of models defined by the system yaml file, representing all the specified elements of the simulated grid. This file also contains all the connections between the components|
| Dataseries | A table containing all the data throught the time, it's used by time/scenario dependent components|


## Concepts

### Models and Components

| Concept     | Definition    |
|-------------|---------------|
| Model       | An abstract mathematical configuration representing the general features of a category of grid element. Users can specify any instance of this model for creating each simulated grid's element  |
| Component   | An instance using a model as a template. Each component is a specific detailed instance of a model representing a real object. Multiple components can use the same model within a system, each with different parameter values |

## Optimization configuration

| Concept              | Definition        |
|----------------------|-------------------|
| Variable             | An abstract mathematical variable of a model, whose value is optimized by the solver. The optimization problem is to find the best set of variables based on the variable's configuration, shared across all model instances. |
| Parameter            | An input data declared in the model, with a value specific to each component (set in the system.yml file). The optimization problem seeks the best set of variables according to these parameters.               |
| Objective function   | The mathematical expression optimized by the solver. Variables are selected to achieve its global minimum based on the input parameters. |

### Interfaces and Relationships

| Concept            | Definition        |
|--------------------|-------------------|
| Port               | A communication interface for exchanging expressions, called "fields"     |
| Field              | An expression exchanged by a port    |
| Constraint         | A mathematical relationship or condition that restricts the values of variables |
| Binding Constraint | A constraint that links variables or ports across different models or components |
| Connection         | A link between two components' ports |

### Time and Scenario dependency Configuration

| Concept            | Definition            |
|--------------------|-----------------------|
| Time dependent     | A parameter depending on time. In this case, the parameters are represented as a dataseries|
| Scenario dependent | A parameter depending on the scenario type. In this case, the parameters are represented as a dataseries |

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
