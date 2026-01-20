<div align="center">
    <img src="../../assets/gemsV2.png" alt="GEMS Logo" width="800"/>
</div>

# Context of GEMS

The framework **GEMS** (Generic Energy Systems Modelling Scheme) was developed by the [Antares Simulator Team](https://antares-simulator.org/) at [RTE](https://www.rte-france.com/), the French Transmission System Operator (TSO). Its goal is to advance tools and communities for **long-term power system adequacy** and **investment planning** studies.

<div style="display: flex; flex-direction: column; align-items: center; gap: 10px;">
  <div style="display: flex; justify-content: center; align-items: flex-end; gap: 40px;">
    <div style="display: flex; flex-direction: column; align-items: center;">
      <img src="../../assets/4_RTE_logo.svg.png" alt="RTE Logo" style="height: 80px"/>
      <div style="font-size: 0.9em; color: #555; margin-top: 8px;"><em>RTE - French Transmission System Operator</em></div>
    </div>
    <div style="display: flex; flex-direction: column; align-items: center;">
      <img src="../../assets/5_antares_sim_logo.webp" alt="Antares Simulator Logo" style="height: 80px"/>
      <div style="font-size: 0.9em; color: #555; margin-top: 8px;"><em>Antares Simulator Team</em></div>
    </div>
  </div>
</div>

It provides a high-level Modelling language, close to mathematical syntax, and a data structure for describing energy systems.

<br>

# Vision and Ambitions for GEMS

The ambition behind the GEMS language is to **build and support a community of energy modellers and energy foresight practitioners** who can easily share models, assumptions, and studies.
This approach is particularly important as future energy systems — strategic by nature — are increasingly conceived in a **multi-energy, multi-actor landscape**, characterised by rising systemic complexity and tightly coupled interactions across scales.

<div align="center">
    <img src="../../assets/Communaute.jpg" alt="GEMS Logo" width="150px"/>
</div>

GEMS has the key attributes required to support and sustain such a community.

- **Versatility**
<br>
GEMS is a generic optimisation language capable of representing a wide range of energy systems and use cases, from operational studies to long-term planning, across multiple energy carriers and scales.

- **Code Stability and Maintainability**
<br>
By clearly **separating model definition from problem resolution**, GEMS promotes robust, modular, and maintainable code that can evolve over time without breaking existing models.

- **Interoperability/Interpretability**
<br>
GEMS relies on a **self-contained** and exhaustive mathematical formulation, ensuring that all modelling assumptions, variables, and constraints are explicitly defined. This guarantees unambiguous interpretability of models, which is a key enabler for true interoperability between tools, solvers, and modelling frameworks.

<div align="center">
    <img src="../../assets/Context_Gems_Example_Model.png" alt="GEMS Logo" width="500"/>
</div>

<br>

# Resources

The **GEMS documentation, pre-defined model libraries and quick-start examples** are hosted in the GitHub repository: [GEMS](https://github.com/AntaresSimulatorTeam/Gems)

The following **interpreters** can be used to run Gems modelling language :

- [Antares Simulator](https://github.com/AntaresSimulatorTeam/Antares_Simulator), an open-source power system simulator
- [GemsPy](https://github.com/AntaresSimulatorTeam/GemsPy), a stand-alone Python package, maintained for prototyping purposes

**Converters** are available to translate existing studies into the GEMS modelling language:

- [Antares Legacy Models to GEMS Converter](https://github.com/AntaresSimulatorTeam/AntaresLegacyModels-to-GEMS-Converter) : a Python package that enables the migration of Antares Legacy Models to GEMS.
- [PyPSA to Gems Converter](https://github.com/AntaresSimulatorTeam/PyPSA-to-GEMS-Converter), a stand-alone Python package to export PyPSA [Networks](https://docs.pypsa.org/v1.0.2/user-guide/design/#network-object) as [GEMS system](./3_User_Guide/3_GEMS_File_Structure/3_system.md). This converter supports [PyPSA two-stage stochastic optimization problems](https://docs.pypsa.org/v1.0.2/user-guide/optimization/stochastic/): such problems can be addressed by GEMS [interpreters](./1_Overview/1_Architecture.md) and solved with [Antares Xpansion's Benders decomposition algorithm](https://antares-xpansion.readthedocs.io/en/stable/).

<br>

# Documentation Highlights

## Quick Links

<div class="grid cards" markdown>

-   :material-clock-fast:{ .lg .middle } **Getting Started**

    ---

    How to **install** GEMS interpreters and create 2 **simples studies** (*Adequacy problem* and *Unit Commitment*).

    [:octicons-arrow-right-24: Installation](2_Getting_Started/1A_modeler_installation.md)

    [:octicons-arrow-right-24: Quick Start Examples](2_Getting_Started/2A_QSE_adequacy.md)

-   :material-view-list:{ .lg .middle } **Overview**

    ---

    **Understand** about GEMS framework and its interpreters.

    [:octicons-arrow-right-24: Architecture](1_Overview/1_Architecture.md)

    [:octicons-arrow-right-24: Interpreters](../doc/1_Overview/4_GEMS%20Interpreters/1_gemspy.md)

-   :material-new-box:{ .lg .middle } **Release Notes**

    ---

    Check out the latest features, bug fixes and improvements in the release notes.

    [:octicons-arrow-right-24: What's new](0_Home/4_release_notes.md)

</div>

## Sections

<div class="grid cards" markdown>

-   :material-bookshelf:{ .lg .middle } **User Guide**

    ---

    Detailed presentation of GEMS **syntax**, **file structure**, and how to configure **optimization studies**.

    [:octicons-arrow-right-24: User Guide](3_User_Guide/1_introduction.md)

-   :material-notebook-multiple:{ .lg .middle } **Examples**

    ---

    Examples can be found here from the **first steps with GEMS** to handling **hybrid studies**.

    [:octicons-arrow-right-24: Examples](5_Examples/1_optimization_problem.md)

-   :material-swap-horizontal:{ .lg .middle } **Interoperability**

    ---

    How to export **PyPSA** and **Antares Legacy** study cases in GEMS format and run them with GEMS interpreters.

    [:octicons-arrow-right-24: Interoperability](4_Interoperability/1_pypsa.md)

-   :fontawesome-solid-users:{ .lg .middle } **Support and Contributing**

    ---

    Find here **Support** for using GEMS. How to **Contribute** to GEMS.

    [:octicons-arrow-right-24: Support](../doc/0_Home/5_support.md)

    [:octicons-arrow-right-24: Contributing](6_Support_Contributing/3_contributing.md)

</div>

---
**Navigation**
<div style="display: flex; justify-content: flex-end;">
  <button type="button" style="background-color:#CCCCCC; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
  <a href="../0_Home/2_core_concepts" style="text-decoration:none; color: #000000">Next page ➡️</a>
  </button>
</div>

---

© GEMS (LICENSE)