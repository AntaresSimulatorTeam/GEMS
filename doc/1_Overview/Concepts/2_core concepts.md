<<<<<<< HEAD
<div style="display: flex; justify-content: space-between; align-items: center;">
    <div style="text-align: left;">
        <a href="../../index.md">Main Section</a>
    </div>
    <div style="text-align: right;">
        <img src="../../assets/gemsV2.png" alt="GEMS Logo" width="150"/>
    </div>
</div>

# Inputs
## YAML files
GEMS uses mainly YAML files for defining optimization problem :

- **Library.yml** is a file listing all the **models** representing general unspecified elements of a study. These models are used as “template” for creating their instances, called **components**.

- **System.yml** is a file listing all the **components**, the instances of **models** defined by the system yaml file, representing all the specified elements of the simulated grid. Besides, this file contains all the connections between the components, defining how they interact. 

### Models definition (from library.yml)

As seen before, library defines the **models**. They are abstract mathematical configurations representing the general features of a category of grid element, then, users can specify any instance of this model for creating each simulated grid’s element. 

They are defined by *variables*, *parameters*, *ports*, *constraints* :

- **Variables [^1]** are abstract mathematical variables of a model, whose value is optimized by the solver. The optimization problem is to find the best set of variables based on their configuration. Their settings is shared across all model instances and defined in a library file.

- **Parameters (configuration) [^1]** is an input data declared in the model, but its value specific for each component is set in system.yml file.

- **Port** is  communication interface for exchanging several expressions, called **fields** (expressions only exchanged by a port).

- **Constraints [^1]** are mathematical conditions that restricts the values of variables 

- **Binding Constraints [^1]** are constraint that links variables or ports across different models or components

### Components specification (from system.yml)

As mentionned before, **components** are instantiations of different **models**. In the system file, their parameters and connections are defined.

*One singe model can be referenced by several components, however, one component can only reference to one single model.*

- **Model ID** is the reference of the model of which the component used. 
- **Parameter value [^1]** is set inside the system.yml file but it was previously declared inside the library.yml file
- **Connections** are the links between two components' ports 

## Dataseries

**Data series** are needed by the system description to define component parameter values are set in dedicated input files. Currently, the framework supports defining data-series using tab-seperated-values files. Values must be separated using tabs, and the character `.` represents the floating point.

### Scenario / Time Dependency
Inside the YAML files, **Parameters, Variables, and Constraints** can be dependent on the scenario and/or over time.
- A **scenario dependency** means, for instance, that the *parameter* `fixed_cost` for starting up a plant can depend on the chosen scenario.

    A simulation with 4 scenarios will get :
    `54 67.5 23.652 253`
- A **time dependent** *parameter* can be for instance `max_active_power_set_point` dependending on plant maintenancy. A time dependency needs a dataserie for getting data

    A simulation with 4 timestamps will get :
    ```
    54 
    67.5 
    23.652 
    253```

## Illustration with an example

For getting familiar with these concepts, you can see below a corresponding table between theorical concepts and example from a thermal plant usecase :

|concept|example|
|-|-|
|Library|List of global concepts such as a thermal plant|
|Model | A thermal plant model|
|Component|A specific theraml, like a 300MW CCGT Thermal plant|
|Variable|Actual dispatched power|
|Parameter|Maximum Power Capacity (specfic for each thermal plant, to be entered by the users)|
|Field|The field Injection flow is exchanged through injection_port|
|Port|The injection_port let the injection_flow be transfered|
|Connection|A link between a generation unit and a node representing the injection from the plant to the grid’s node|
|Constraint|Value interval accepted for power generation|
|Binding Constraints|Specific example with an area 
model (not a GU model) - Energy balance inside an area|
|Time dependency|Max_active_power_setpoint is a time dependent parameter|
|Scenario dependency|fix_startup_cost can depend on the scenario chosen by the users|

# Outputs

The outputs of GEMS contain the results of the modelisation, in a LP format (**Optimization Model**) and for hybrid and pure modeler studies in CSV format (**simulation table**), there are also **extra-outputs**.

- **Optimization Model**
    The optimization model solved by Antares modeler is written in the human-readable LP format, under output/problem.lp. It is only meant to be used for debugging.

- **Simulation Table**
    Antares Simulator (hybrid and modeler modes) produces detailed optimization results for the modeler's components, in the "simulation table", in CSV format

- **Extra Outputs**
    Extra-Outputs computed after optimization (using optimal variable values). These appear in the output files alongside variable and port values.

- **Business Views**
    Output files with metrics specifically designed for users purposes. It made from the simulation table.

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
        <a href="../../index.md" style="text-decoration:none; color: #FFFFFF">Index</a>
    </button>
    <div style="text-align: right;">
    <button type="button" style="background-color:#CCCCCC; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
        <a href="3_features.md" style="text-decoration:none; color: #000000">Next page ➡️</a>
    </button>
    </div>
=======
![Template Banner](../../assets/template_banner.svg)
<div style="display: flex; justify-content: space-between; align-items: center;">
  <div style="text-align: left;">
    <a href="folder1/home1.md">Main Section</a>
  </div>
  <div style="text-align: right;">
    <img src="assets/gemsV2.png" alt="GEMS Logo" width="150"/>
  </div>
</div>


# Title 1

<div style="display: flex; flex-direction: column; align-items: center; gap: 10px;">
  <div style="display: flex; justify-content: center; align-items: flex-end; gap: 40px;">
    <div style="display: flex; flex-direction: column; align-items: center;">
      <img src="assets/4_RTE_logo.svg.png" alt="RTE Logo" style="height: 80"/>
      <div style="font-size: 0.9em; color: #555; margin-top: 8px;"><em>RTE - French Transmission System Operator</em></div>
    </div>
    <div style="display: flex; flex-direction: column; align-items: center;">
      <img src="assets/5_antares_sim_logo.webp" alt="Antares Simulator Logo" style="height: 80"/>
      <div style="font-size: 0.9em; color: #555; margin-top: 8px;"><em>Antares Simulator Team</em></div>
    </div>
  </div>
</div>

## Sub-Title 2
Content or text here.

**Code block example (YAML):**
```yaml
connections:
  - component1: generator1
    port1: injection_port
    component2: node1
    port2: injection_port
  - component1: generator2
    port1: injection_port
    component2: node1
    port2: injection_port
  - component1: demand
    port1: injection_port
    component2: node1
    port2: injection_port
```

**Code block example (Python):**
```python
print("Hello World")
```
**Note Example:**

<div style="border:1px solid #ccc; padding:10px; background:#f9f9f9;">
<strong>🖊️ Note :</strong> This is an important note
</div>


**Simple Equation example:**

 > $3 * parameter_1 * variable_a + variable_b + 56.4 <= variable_4 * 439$ 

**LATEC equation example:**
$$
3 \cdot \text{parameter\_1} \cdot \text{variable\_a} + \text{variable\_b} + 56.4 \leq \text{variable\_4} \cdot 439
$$

---
**Navigation**
<div style="display: flex; justify-content: space-between;">
  <div style="text-align: left;">
  <button type="button" style="background-color:#CCCCCC; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
    <a href="previous.md" style="text-decoration:none; color: #000000">⬅️ Previous page</a>
  </button>
  </div>
  <button type="button" style="background-color:#AAAAFF; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
    <a href="Home/Main_Home/1_context_GEMS.md" style="text-decoration:none; color: #FFFFFF">Index</a>
  </button>
  <div style="text-align: right;">
  <button type="button" style="background-color:#CCCCCC; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
    <a href="next.md" style="text-decoration:none; color: #000000">Next page ➡️</a>
  </button>
  </div>
>>>>>>> main
</div>

---

© GEMS (LICENSE)