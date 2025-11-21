---
title: "Core concepts"
author: "Guillaume MAISTRE - RTEi"
date: "19/11/2025"
logo: "../../assets/gemsV2.png"
---

<div style="display: flex; justify-content: space-between; align-items: center;">
    <div style="text-align: left;">
        <a href="../../index.md">Main Section</a>
    </div>
    <div style="text-align: right;">
        <img src="../../assets/gemsV2.png" alt="GEMS Logo" width="150"/>
    </div>
</div>

# YAML files
GEMS uses mainly YAML files for defining optimisation problem :

- **Library.yml** is a file listing all the **models** representing general unspecified elements of a study. These models are used as “template” for creating their instances, called **components**.

- **System.yml** is a file listing all the **components**, the instances of **models** defined by the system yaml file, representing all the specified elements of the simulated grid. Besides, this file contains all the connections between the components, defining how they interact. 

## Models definition (from library.yml)

As seen before, library defines the **models**. They are abstract mathematical configurations representing the general features of a category of grid element, then, users can specify any instance of this model for creating each simulated grid’s element. 

They are defined by *variables*, *parameters*, *ports*, *constraints* :

- **Variables [^1]** are abstract mathematical variables of a model, whose value is optimized by the solver. The optimization problem is to find the best set of variables based on their configuration. Their settings is shared across all model instances and defined in a library file.

- **Parameters (configuration) [^1]** is an input data declared in the model, but its value specific for each component is set in system.yml file.

- **Port** is  communication interface for exchanging several expressions, called **fields** (expressions only exchanged by a port).

- **Constraints [^1]** are mathematical conditions that restricts the values of variables 

## Components specification (from system.yml)

As mentionned before, **components** are instantiations of different **models**. In the system file, their parameters and connections are defined.

*One singe model can be referenced by several components, however, one component can only reference to one single model.*

- **Model ID** is the reference of the model of which the component used. 
- **Parameter value [^1]** is set inside the system.yml file but it was previously declared inside the library.yml file
- **Connections** are the links between two components' ports 

# Dataseries

The **data series** are set of data throughout the all the optimisation problem time specific for each input.

## Scenario / Time Dependency

Inside the YAML files, **Parameters, Variables, Constraints** can be dependent on the scenario or/and over the time.
- A **scenario dependency** means for instance that the *parameter* `fixed_cost` for strating up a plant can depends on the scenario we chose.
- A **time dependent** *parameter* can be for instance `max_active_power_set_point` dependending on plant maintenancy. A time dependency needs a dataserie for getting data

# Illustration with an example

ADD EXAMPLE FROM GLOSSARY WITH THERMAL PLANT


[^1]: Parameters, Variables, Constraints can be either scenario dependent or time dependent
---
**Navigation**

<div style="display: flex; justify-content: space-between;">
    <div style="text-align: left;">
        <a href="../Main_Home/3_release_notes.md">Previous Section</a>
    </div>
    <div style="text-align: center;">
        <a href="../../index.md">Back to Home</a>
    </div>
  <div style="text-align: right;">
    <a href="2_GEMS_architecture.md">Next Section</a>
  </div>
</div>

---

© GEMS (LICENSE)