<div style="display: flex; justify-content: space-between; align-items: center;">
  <div style="text-align: left;">
    <a href="../../../index.md">Main Section</a>
  </div>
  <div style="text-align: right;">
    <img src="../../../assets/gemsV2.png" alt="GEMS Logo" width="150"/>
  </div>
</div>

# GEMS Features

## Main Functionalities

- **Mixed Integer Linear Programming (MILP)**: GEMS is designed to handle mathematical problems requiring Mixed Integer Linear Programming.
- **Time × Scenario Optimization**: Problems over a time × scenario grid can be solved.

## Energy System Modelling

- **Multi-Energy Modelling**: Multi-energy systems can be modeled by GEMS. While ANTARES mainly focuses on the electric grid, GEMS can handle multi-energy systems.
- **Antares Legacy Integration (Hybrid Mode)**: A study can be composed of a "hybrid" simulation made of two simulation parts, one from Legacy and the other from GEMS.
- **Model Taxonomy**: The framework uses a `taxonomy.yml` file to define model categories and ensure mandatory fields (parameters, variables, ports, extra outputs) for each category.

## Architecture

- **Versatility**: Users can easily integrate new component models without rewriting core code by editing their own library and system YAML files.
- **Input Separation**: Input data is separated into self-contained external files:
  - `library file`
  - `system file`
  - `dataseries`
- **Interpreters**: Different interpreters can be used for solving problems, including the Modeler (GEMS interpreter in Antares Simulator) and GemsPy (Python interpreter [available on GitHub](https://github.com/AntaresSimulatorTeam/GemsPy)).
- **Code Stability**: GEMS was developed to ensure code stability and maintainability.
- **Interoperability**: GEMS aims to emphasize interoperability and the ability to run studies from different formats.

---

**Navigation**

<div style="display: flex; justify-content: space-between;">
  <div style="text-align: left;">
  <button type="button" style="background-color:#CCCCCC; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
  <a href="2_core concepts.md" style="text-decoration:none; color: #000000">⬅️ Previous page</a>
  </button>
  </div>
  <button type="button" style="background-color:#AAAAFF; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
  <a href="../../../index.md" style="text-decoration:none; color: #FFFFFF">Index</a>
  </button>
  <div style="text-align: right;">
  <button type="button" style="background-color:#CCCCCC; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
  <a href="xxx" style="text-decoration:none; color: #000000">Next page ➡️</a>
  </button>
  </div>
</div>

---

© GEMS (LICENSE)
