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

# Ressources

The **GEMS documentation, pre-defined model libraries and quick-start examples** are hosted in the Github repository :  [GEMS](https://github.com/AntaresSimulatorTeam/Gems)

The following **interpreters** can be used to run Gems modelling language :

- [Antares Simulator](https://github.com/AntaresSimulatorTeam/Antares_Simulator), an open-source power system simulator
- [GEMSPy](https://github.com/AntaresSimulatorTeam/GemsPy), a stand-alone Python package, maintained for prototyping purposes

**Converters** are available to translate existing studies into the GEMS modelling language:

- [Antares Legacy Models to Gems Converter](https://github.com/AntaresSimulatorTeam/PyPSA-to-GEMS-Converter) : an open-source power system simulator that enables the migration of Antares legacy models to GEMS
- [PyPSA to Gems Converter](https://github.com/AntaresSimulatorTeam/AntaresLegacyModels-to-GEMS-Converter), a stand-alone Python package, maintained for prototyping purposes

<br>


# Documentation Highlights

<div style="display: flex; flex-wrap: wrap; gap: 20px; justify-content: space-between;">
  <!-- Card Overview -->
  <div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 12px; margin: 10px 0; background-color: #f9f9f9; width: 190px;">
    <div style="font-size: 1.2em; margin-bottom: 8px;">
      📖 <strong>Overview</strong>
    </div>
    <div style="margin-left: 10px;">
      <div style="margin-bottom: 5px;">
        <a href="../1_Overview/1_Architecture" style="background-color: #1e3a8a; color: #FFFFFF; text-decoration: none; padding: 6px 12px; border-radius: 4px; font-weight: bold; display: block; width: 100%; max-width: 150px;">🔍 Architecture</a>
      </div>
      <div style="margin-bottom: 5px;">
        <a href="../1_Overview/4_GEMS Interpreters/1_gemspy" style="background-color: #1e3a8a; color: #FFFFFF; text-decoration: none; padding: 6px 12px; border-radius: 4px; font-weight: bold; display: block; width: 100%; max-width: 150px;">🤖 Interpreters</a>
      </div>
      <div style="margin-bottom: 5px;">
        <a href="../1_Overview/5_References/1_Classification_Configuration" style="background-color: #1e3a8a; color: #FFFFFF; text-decoration: none; padding: 6px 12px; border-radius: 4px; font-weight: bold; display: block; width: 100%; max-width: 150px;">📄 References</a>
      </div>
    </div>
  </div>

  <!-- Card Getting Started -->
  <div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 12px; margin: 10px 0; background-color: #f9f9f9; width: 190px;">
    <div style="font-size: 1.2em; margin-bottom: 8px;">
      🚀 <strong>Getting Started</strong>
    </div>
    <div style="margin-left: 10px;">
      <div style="margin-bottom: 5px;">
        <a href="../2_Getting Started/1A_modeler_installation" style="background-color: #1e3a8a; color: #FFFFFF; text-decoration: none; padding: 6px 12px; border-radius: 4px; font-weight: bold; display: block; width: 100%; max-width: 150px;">💿 Installation</a>
      </div>
      <div style="margin-bottom: 5px;">
        <a href="../2_Getting Started/2A_adequacy" style="background-color: #1e3a8a; color: #FFFFFF; text-decoration: none; padding: 6px 12px; border-radius: 4px; font-weight: bold; display: block; width: 100%; max-width: 150px;">🏁 Quick Start</a>
      </div>
    </div>
  </div>

  <!-- Card User Guide -->
  <div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 12px; margin: 10px 0; background-color: #f9f9f9; width: 190px;">
    <div style="font-size: 1.2em; margin-bottom: 8px;">
      🧑‍🏫 <strong>User Guide</strong>
    </div>
    <div style="margin-left: 10px;">
      <div style="margin-bottom: 5px;">
        <a href="../3_User Guide/1_syntax" style="background-color: #1e3a8a; color: #FFFFFF; text-decoration: none; padding: 6px 12px; border-radius: 4px; font-weight: bold; display: block; width: 100%; max-width: 150px;">📝 Syntax</a>
      </div>
      <div style="margin-bottom: 5px;">
        <a href="../3_User Guide/2_inputs" style="background-color: #1e3a8a; color: #FFFFFF; text-decoration: none; padding: 6px 12px; border-radius: 4px; font-weight: bold; display: block; width: 100%; max-width: 150px;">↘️ Inputs</a>
      </div>
      <div style="margin-bottom: 5px;">
        <a href="../3_User Guide/4_outputs" style="background-color: #1e3a8a; color: #FFFFFF; text-decoration: none; padding: 6px 12px; border-radius: 4px; font-weight: bold; display: block; width: 100%; max-width: 150px;">↗️ Outputs</a>
      </div>
    </div>
  </div>

  <!-- Card Interoperability -->
  <div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 12px; margin: 10px 0; background-color: #f9f9f9; width: 190px;">
    <div style="font-size: 1.2em; margin-bottom: 8px;">
      ↕️ <strong>Interoperability</strong>
    </div>
    <div style="margin-left: 10px;">
      <div style="margin-bottom: 5px;">
        <a href="../4_Interoperability/1_pypsa" style="background-color: #1e3a8a; color: #FFFFFF; text-decoration: none; padding: 6px 12px; border-radius: 4px; font-weight: bold; display: block; width: 100%; max-width: 150px;">🔄 PyPSA</a>
      </div>
      <div style="margin-bottom: 5px;">
        <a href="../4_Interoperability/2_antares legacy" style="background-color: #1e3a8a; color: #FFFFFF; text-decoration: none; padding: 6px 12px; border-radius: 4px; font-weight: bold; display: block; width: 100%; max-width: 150px;">📜 Antares Legacy</a>
      </div>
      <div style="margin-bottom: 5px;">
        <a href="../4_Interoperability/3_hybrid" style="background-color: #1e3a8a; color: #FFFFFF; text-decoration: none; padding: 6px 12px; border-radius: 4px; font-weight: bold; display: block; width: 100%; max-width: 150px;">🔰 Hybrid</a>
      </div>
    </div>
  </div>

  <!-- Card Examples -->
  <div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 12px; margin: 10px 0; background-color: #f9f9f9; width: 190px;">
    <div style="font-size: 1.2em; margin-bottom: 8px;">
      ✏️ <strong>Examples</strong>
    </div>
    <div style="margin-left: 10px;">
      <div style="margin-bottom: 5px;">
        <a href="../5_Examples/1_optimization_problem" style="background-color: #1e3a8a; color: #FFFFFF; text-decoration: none; padding: 6px 12px; border-radius: 4px; font-weight: bold; display: block; width: 100%; max-width: 150px;">📚 Tutorial</a>
      </div>
      <div style="margin-bottom: 5px;">
        <a href="../5_Examples/2_hybrid" style="background-color: #1e3a8a; color: #FFFFFF; text-decoration: none; padding: 6px 12px; border-radius: 4px; font-weight: bold; display: block; width: 100%; max-width: 150px;">🔰 Hybrid Examples</a>
      </div>
    </div>
  </div>
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