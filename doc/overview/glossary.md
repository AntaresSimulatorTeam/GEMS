---
description: GEMS glossary - definitions of core concepts including libraries, models, components, ports, connections, system files, and data series used in the GEMS framework.
---

# Glossary

This section is a glossary of the main concepts used by GEMS. For a detailed specification of each file, see the [file structure page](file-structure.md).

## Input Files

| Term    | Definition    |
|---------|---------------|
| [Library](../user-guide/input-files/library.md) | A file listing all the **models** representing general unspecified elements of a study. These models are used as "templates" for creating their instances, called components.|
| [System](../user-guide/input-files/system.md)  | A file listing all the "**components**", the instances of models defined by the system YAML file, representing all the specified elements of the simulated grid. This file also contains all the connections between the components|
| [Dataseries](../user-guide/input-files/data-series.md) | A table containing all the data through time. It is used by time/scenario dependent components|
| [Taxonomy](../user-guide/input-files/business-view-configuration.md) | A file classifying component models into **categories**. Used to select which components contribute to a metric.|
| [Catalog](../user-guide/input-files/business-view-configuration.md) | A file defining a set of end-use **Metrics** with their aggregation rules (terms, terms-operator, time-operator).|
| [View Config](../user-guide/input-files/business-view-configuration.md) | Configure **views** by specifying scope (location, calendar), time aggregation, and the metrics from `catalog.yml` to compute.|

## Concepts

### Models and Components

| Concept     | Definition    |
|-------------|---------------|
|[Model](../user-guide/input-files/library.md#models)| An abstract mathematical configuration representing the general features of a category of grid element. Users can specify any instance of this model for creating each simulated grid's element  |
|[Component](../user-guide/input-files/system.md#components)| An instance using a model as a template. Each component is a specific detailed instance of a model representing a real object. Multiple components can use the same model within a system, each with different parameter values |

### Abstract modelling: Optimization

| Concept              | Definition        |
|----------------------|-------------------|
| [Variable](../user-guide/input-files/library.md#variables)             | An abstract mathematical variable of a model, whose value is optimized by the solver. The optimization problem is to find the best set of variables based on the variable's configuration, shared across all model instances. |
| [Parameter](../user-guide/input-files/library.md#parameters)            | An input data declared in the model, with a value specific to each component (set in the system.yml file). It can be a scalar value, a time-series, or a scenario-series. The optimization problem seeks the best set of variables according to these parameters.               |
| [Objective function](../user-guide/input-files/library.md#objective-contribution)   | The mathematical expression optimized by the solver. Variables are selected to achieve its global minimum based on the input parameters. |
| [Constraint](../user-guide/input-files/library.md#constraints)| A mathematical relationship or condition that restricts the values of variables |
| [Binding Constraint](../user-guide/input-files/library.md#binding-constraints) | A constraint that links variables or ports across different models or components |

### Interfaces and Relationships

| Concept            | Definition        |
|--------------------|-------------------|
| [Port](../user-guide/input-files/library.md#ports)| A communication interface for exchanging expressions, called "fields"     |
| [Field](../user-guide/input-files/library.md#ports) | A scalar quantity carried by a port and exchanged between connected components (e.g., a power flow value) |
| [Connection](../user-guide/input-files/system.md#connections)| A link between two components' ports |

### Time and Scenario Dependency

| Concept            | Definition            |
|--------------------|-----------------------|
| Time | Energy systems modelled and optimized within GEMS are, in most cases, inherently temporal. To make this tractable within a computational framework, GEMS represents time in a discrete rather than continuous manner.
| [Time dependent](../user-guide/syntax.md#time-operators-and-indexing)     |  A parameter or variable depending on time. In this case, the parameter is instantiated as a dataseries. |
| Scenario | Condition of the system environment (e.g., weather patterns, demand levels) over the simulation horizon. Multiple scenarios can be evaluated in a single study to capture variability or uncertainty. |
| [Scenario dependent](../user-guide/syntax.md#scenario-operator) | A parameter or variable depending on the scenario. In this case, the parameter is instantiated as a dataseries. |


## Output Files

| Term    | Definition    |
|---------|---------------|
| [Simulation table](../user-guide/outputs/simulation-table.md) | A table providing the raw optimization results|
| [Views](../user-guide/outputs/business-view.md) | They provide a representation of results as Metrics, based on users' requirements written inside the `view-config.yml`.|


