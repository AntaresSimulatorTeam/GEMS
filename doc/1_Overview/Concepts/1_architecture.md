<div style="display: flex; justify-content: space-between; align-items: center;">
  <div style="text-align: left;">
    <a href="../index.md">Main Section</a>
  </div>
  <div style="text-align: right;">
    <img src="../../assets/gemsV2.png" alt="GEMS Logo" width="150"/>
  </div>
</div>

# GEMS Architecture

## Architectural Breakthrough

This architecture represents a fundamental change from classical OOME architectures, where problem definition is typically located inside the *Problem builder* and the tool itself.

<div style="text-align: center;">
  <img src="../../assets/3_Scheme_Classical_GEMS_OOME.png" alt="Architecture Breakthrough of GEMS comparing to Classical OOME" />
</div>


By configuring the entire optimization problem using these **external YAML files**, the architecture achieves its key principles:

- **Versatile Modelling**: Optimization problem can be configured easily ***without* rewriting the core code**
- **Interoperability**: The GEMS format facilitates seamless interaction with external tools, demonstrated, for example, by the conversion and simulation of PyPSA studies using GemsPy

## Input Files

The GEMS architecture enforces a structured approach, separating modeling logic, system configuration, optimization workflow, and business intelligence into four distinct "bounded domains".

The core inputs for defining the optimization problem are external configuration files:

| Component | File | Description & Role |
| :--- | :--- | :--- |
| **Model Libraries** | `library.yml` | Define the **Models**, which are **abstract representation of a type of object** that will be simulated inside our own study. This file includes optimization **variables**, **mathematical constraints**, **objective contributions**, **parameters**, and **ports**. |
| **System** | `system.yml` | Defines the **Components**, which are **numerical instantiation of models**. It links to a specific model ID and defines the numerical values for its parameters. It also defines the **connections** between components via ports, forming the system graph. |
| **Timeseries** | `timeseries.tsv` | Contains the numerical data for parameters that are dependent on time and scenario. |


## Files Interaction

The following scheme shows the interaction of the different core concepts presented previously. It is based on the *basic-model-library* present inside this documentation.

<p align="center">
    <img src="../../assets/6_GEMS_architecture.png" alt="GEMS Architecture Diagram">
</p>

---

**Navigation**

<div style="display: flex; justify-content: space-between;">
  <div style="text-align: left;">
  <button type="button" style="background-color:#CCCCCC; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
    <a href="../Home/Main_Home/2_release_notes.md" style="text-decoration:none; color: #000000">⬅️ Previous page</a>
  </button>
  </div>
  <button type="button" style="background-color:#AAAAFF; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
    <a href="../../index.md" style="text-decoration:none; color: #FFFFFF">Index</a>
  </button>
  <div style="text-align: right;">
  <button type="button" style="background-color:#CCCCCC; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
    <a href="2_core concepts.md" style="text-decoration:none; color: #000000">Next page ➡️</a>
  </button>
  </div>
</div>

---

© GEMS (LICENSE)