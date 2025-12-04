<div style="display: flex; justify-content: space-between; align-items: center;">
    <div style="text-align: left;">
        <a href="../../../index.md">Main Section</a>
    </div>
    <div style="text-align: right;">
        <img src="../../../assets/gemsV2.png" alt="GEMS Logo" width="150"/>
    </div>
</div>

# Inputs
## YAML files
GEMS uses mainly YAML files for defining optimization problem :

- **Library.yml** is a file listing all the **models** representing general unspecified elements of a study. These models are used as “template” for creating their instances, called **components**.

- **System.yml** is a file listing all the **components**, the instances of **models** defined by the system yaml file, representing all the specified elements of the simulated energy system. Besides, this file contains all the connections between the components, defining how they interact. 

### Models definition (from library.yml)

As seen before, library defines the **models**. They are abstract mathematical configurations representing the general features of a category of energy system element, then, users can specify any instance of this model for creating each simulated grid’s element. 

They are defined by *variables*, *parameters*, *ports*, *constraints*, [examples are provided in UserGuide section](../../3_User%20Guide/1_syntax.md#model%20definition%20%28from%20system.yml%29).

- **Variables [^1]** are abstract mathematical variables of a model, whose value is optimized by the solver. The optimization problem is to find the best set of variables based on their configuration. Their settings is shared across all model instances and defined in a library file.

- **Parameters (configuration) [^1]** is an input data declared in the model, but its value specific for each component is set in system.yml file.

- **Expression** is a mathematical formula used to specify a models's behavior, constraints, and contribution to the overall optimization problem

- **Constraints [^1]** are mathematical conditions that restricts the values of variables 

- **Port** is  communication interface for exchanging several expressions, called **fields** (expressions only exchanged by a port).

- **Binding Constraints [^1]** are constraints that link expressions shared between components through ports

### Component specification (from system.yml)

As mentionned before, **components** are instantiations of different **models**. In the system file, their [parameters and connections](../../3_User%20Guide/1_syntax.md#components%20specification%20%28from%20system.yml%29) are defined.

*One singe model can be referenced by several components, however, one component can only reference to one single model.*

Their configuration consist of :

- **Model ID** is the reference of the model of which the component used. 
- **Parameter value [^1]** is set inside the system.yml file but it was previously declared inside the library.yml file
- **Connections** are the links between two components' ports 


## Dataseries

Inside the YAML files, Parameters, Variables, and Constraints can be **dependent on the scenario and/or over time**, in this case, **dataseries** are needed for specified data. [Their structure depends of the system.](../../3_User%20Guide/1_syntax.md#dataseries).

## Illustration with an example

For getting familiar with these concepts, you can see below a corresponding table between theorical concepts and example from a thermal plant usecase :

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
|Time dependency|`max_active_power_setpoint` is a time dependent parameter|
|Scenario dependency|`fix_startup_cost` can depend on the scenario chosen by the users|

# Outputs

The outputs of GEMS consit of the results of the modelisation, in two main files; **Optimization Problem** and **Business Views**. Their structure are detailed inside [UserGuide section](../../3_User%20Guide/1_syntax.md#outputs).

- Optimization Problem contains all the global results of the simulation
- Business Views consits of the results of the simulation but according to users' [specific needs](../../3_User%20Guide/1_syntax.md#outputs).



[^1]: Parameters, Variables, and Constraints can be either scenario-dependent or time-dependent.

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