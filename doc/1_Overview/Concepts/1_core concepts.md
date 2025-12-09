<div style="display: flex; justify-content: space-between; align-items: center;">
    <div style="text-align: left;">
        <a href="../../../index.md">Main Section</a>
    </div>
    <div style="text-align: right;">
        <img src="../../../assets/gemsV2.png" alt="GEMS Logo" width="150"/>
    </div>
</div>

**GEMS** is a graph-based algebraic modelling language for building, managing, and solving optimization problems that describe energy systems.

Unlike traditional algebraic modelling languages such as **AMPL or GAMS**, GEMS adopts an **object-oriented** and **graph-oriented** approach. Abstract **models** of components are defined in **Libraries** and can then be **instantiated, assembled, and interconnected** to form concrete **Systems**. Systems are graphs of components, that can be translated into an optimization problem.

# Inputs

## Models definition

**Models** are abstract mathematical configurations representing the general features of a category of energy system element. Users can then specify any instance of this model to create each simulated system element.  

They are defined by *variables*, *parameters*, *ports*, and *constraints*. [Examples are provided in the User Guide section.](../../3_User%20Guide/1_syntax.md#model%20definition%20%28from%20system.yml%29)  

- **Variables ¹** are abstract mathematical variables of a model, whose values are optimized by the solver. The optimization problem is to find the best set of variables based on their configuration. Their settings are shared across all model instances and defined in a library file.  

- **Parameters (configuration) ¹** are input data declared in the model, but their values, specific for each component, are set in the system.yml file.  

- **Expression** is a mathematical formula used to specify a model's behavior, constraints, and contribution to the overall optimization problem.  

- **Constraints ¹** are mathematical conditions that restrict the values of variables.  

- **Binding Constraints ¹** are constraints that link expressions shared between components through ports.  

### Ports  

**Ports** are communication interfaces for exchanging several expressions between different components, called **fields**. Thus, they let components share information between each other.

### Component specification

As mentioned before, **components** are instantiations of different **models**. In the system file, their [parameters and connections](../../3_User%20Guide/1_syntax.md#components%20specification%20%28from%20system.yml%29) are defined.

*One single model can be referenced by several components; however, one component can only reference one single model.*

Their configuration consists of:

- **Model ID** is the reference to the model that the component uses.
- **Parameter value ¹** is set inside the system.yml file but must be previously declared inside the library.yml file.
- **Connections** are the links between two components' ports.


## Dataseries

Parameters can be **dependent on the scenario and/or over time**. In this case, **dataseries** are needed for specific data. [Their structure depends on the system.](../../3_User%20Guide/1_syntax.md#dataseries)

## Illustration with an example

To get familiar with these concepts, see the table below for a correspondence between theoretical concepts and examples from a thermal plant use case:

|Concept|Example|
|-|-|
|Library|`basis-models-library` |
|Model | `generator`, `storage` models |
|Component|A specific thermal, like a 300MW CCGT Thermal plant from `generator` model|
|Variable|Actual dispatched power ; `generation` from *generator model* |
|Parameter|Maximum Power Capacity `p_max` (specific for each thermal plant, to be entered by the users)|
|Field|The field `flow` is exchanged through *injection_port*|
|Port|The `injection_port` let the injection *flow* be transfered|
|Connection|A link between a generation unit and a node representing the injection from the plant to the energy system's node|
|Constraint|Value interval accepted for power generation|
|Binding Constraints|Energy balance inside an area|
|Time dependency|`load` is a time dependent parameter|
|Scenario dependency|`fix_startup_cost` can depend on the scenario chosen by the users|




¹: Parameters, Variables, and Constraints can be either scenario-dependent or time-dependent.

---

**Navigation**

<div style="display: flex; justify-content: space-between;">
    <div style="text-align: left;">
    <button type="button" style="background-color:#CCCCCC; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
        <a href="1_architecture.md" style="text-decoration:none; color: #000000">⬅️ Previous page</a>
    </button>
    </div>
    <button type="button" style="background-color:#AAAAFF; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
        <a href="../../../index.md" style="text-decoration:none; color: #FFFFFF">Index</a>
    </button>
    <div style="text-align: right;">
    <button type="button" style="background-color:#CCCCCC; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
        <a href="3_features.md" style="text-decoration:none; color: #000000">Next page ➡️</a>
    </button>
    </div>
</div>

---

© GEMS (LICENSE)