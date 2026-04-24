---
description: GEMS glossary — definitions of core concepts including libraries, models, components, ports, connections, system files, and data series used in the GEMS framework.
tags:
  - Algebraic Modelling Language
  - Graph-based Modelling
---

<div style="display: flex; justify-content: flex-end;">
  <a href="../../../..">
    <img src="../../assets/gemsV2.png" alt="GEMS Logo" width="150"/>
  </a>
</div>

# Glossary

This section is a glossary of the main concepts used by GEMS.

## Input Files

| Term    | Definition    |
|---------|---------------|
| [Library](../user-guide/file-structure/library.md) | A file listing all the models representing general unspecified elements of a study. These models are used as "template" for creating their instances, called components|
| [System](../user-guide/file-structure/system.md)  | A file listing all the "components", the instances of models defined by the system yaml file, representing all the specified elements of the simulated grid. This file also contains all the connections between the components|
| [Dataseries](../user-guide/file-structure/data-series.md) | A table containing all the data through time. It is used by time/scenario dependent components|

## Concepts

### Models and Components

| Concept     | Definition    |
|-------------|---------------|
|[Model](../user-guide/file-structure/library.md#models)| An abstract mathematical configuration representing the general features of a category of grid element. Users can specify any instance of this model for creating each simulated grid's element  |
|[Component](../user-guide/file-structure/system.md#components)| An instance using a model as a template. Each component is a specific detailed instance of a model representing a real object. Multiple components can use the same model within a system, each with different parameter values |

### Abstract modelling: Optimization

| Concept              | Definition        |
|----------------------|-------------------|
| [Variable](../user-guide/file-structure/library.md#variables)             | An abstract mathematical variable of a model, whose value is optimized by the solver. The optimization problem is to find the best set of variables based on the variable's configuration, shared across all model instances. |
| [Parameter](../user-guide/file-structure/library.md#parameters)            | An input data declared in the model, with a value specific to each component (set in the system.yml file). The optimization problem seeks the best set of variables according to these parameters.               |
| [Objective function](../user-guide/file-structure/library.md#objective-contribution)   | The mathematical expression optimized by the solver. Variables are selected to achieve its global minimum based on the input parameters. |
| [Constraint](../user-guide/file-structure/library.md#constraints)| A mathematical relationship or condition that restricts the values of variables |
| [Binding Constraint](../user-guide/file-structure/library.md#binding-constraints) | A constraint that links variables or ports across different models or components |

### Interfaces and Relationships

| Concept            | Definition        |
|--------------------|-------------------|
| [Port](../user-guide/file-structure/library.md#ports)| A communication interface for exchanging expressions, called "fields"     |
| [Field](../user-guide/file-structure/library.md#ports) | An expression exchanged by a port    |
| [Connection](../user-guide/file-structure/system.md#connections)| A link between two components' ports |

### Time and Scenario Dependency

| Concept            | Definition            |
|--------------------|-----------------------|
| [Time dependent](../user-guide/mathematical-syntax.md#time-operators-and-indexing)     |  A parameter or variable depending on time. In this case, the parameter is instantiated as a dataseries. |
| [Scenario dependent](../user-guide/mathematical-syntax.md#scenario-operator) | A parameter or variable depending on the scenario. In this case, the parameter is instantiated as a dataseries. |


