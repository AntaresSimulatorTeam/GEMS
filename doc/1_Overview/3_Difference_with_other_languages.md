<div style="display: flex; justify-content: space-between; align-items: center;">
  <div style="text-align: left;">
    <a href="../../../..">Main Section</a>
  </div>
  <div style="text-align: right;">
    <img src="../../assets/gemsV2.png" alt="GEMS Logo" width="150"/>
  </div>
</div>

# Differences with other modelling languages and tools

## <img src="../../assets/1_modelica_logo.png" alt="Modelica Logo" width="60" style="vertical-align: middle;"/> MODELICA Language

[Modelica](https://modelica.org/) is a language designed for modelling physical systems based **on differential and algebraic equations**, with a strong focus on dynamic behaviour and simulation.
In contrast, [GEMS](../index.md) is dedicated to the formulation of **mathematical optimisation problems**, making it better suited for long-term energy system studies.
While [Modelica](https://modelica.org/) excels at component-level dynamics, [GEMS](../index.md) focuses on system-wide decision-making, planning, and optimisation.

<br>

## <img src="../../assets/1_gams_logo.png" alt="GAMS Logo" width="60" style="vertical-align: middle;"/> GAMS - General Algebraic Modeling System

[GAMS](https://www.gams.com/) is a powerful language for expressing mathematical optimisation problems in an algebraic form.
However, it does **not provide a native object-oriented or graph-based modelling paradigm**.
[GEMS](../index.md) object and graph-oriented approach is particularly well suited for modelling interconnected energy systems, where similar components (generators, batteries, loads) are replicated across multiple nodes.

<br>

## <img src="../../assets/1_linopy_logo.webp" alt="Linopy Logo" width="60" style="vertical-align: middle;"/> Linopy - Python Package -  Linear optimization with n-dimensional labeled variables
Although both [Linopy](https://linopy.readthedocs.io/en/latest/index.html) and [GEMS](../index.md) are used to formulate optimisation problems, they do not fulfil the same functions. [Linopy](https://linopy.readthedocs.io/en/latest/index.html) is a Python-based modelling multisolver interface whereas [GEMS](../index.md) is conceived as a modelling language to explicitly formulate the energy systems, their components, and their behaviour independently of any particular implementation. [GEMS](../index.md) plays at the level of the system (there it is graph-oriented) whereas [Linopy](https://linopy.readthedocs.io/en/latest/index.html) plays at the level of the linear problem (it is vector-oriented, and one should build a layer on top of that to manage the system graphs). [GEMS](../index.md) interpreters may be built on top of multisolver interfaces, such as [Linopy](https://linopy.readthedocs.io/en/latest/index.html) or [Google OR-Tools](https://developers.google.com/optimization?hl=fr). 
<br> 


## <img src="../../assets/5_antares_sim_logo.webp" alt="Antares Logo" width="60" style="vertical-align: middle;"/> Antares Simulator (Legacy)

Historically, [Antares Simulator](https://antares-simulator.readthedocs.io/en/latest/), an open-source tool for long-term energy system studies, relies on a **fixed file tree structure** as its main input format.
This structure is hard-coded in the tool, which limits flexibility and extensibility.
Introducing new objects or behaviours typically requires **modifying the C++ source code**, whereas [GEMS](../index.md) allows such extensions directly at the modelling language level.

<br>

## <img src="../../assets/1_pypsa_logo.png" alt="PyPSA Logo" width="60" style="vertical-align: middle;"/> PyPSA – Python for Power System Analysis

[PyPSA](https://pypsa.org/) enables the generation of energy system studies using flexible configuration files and **produces a NetCDF** representation of the resulting model.
However, **the component models themselves are hard-coded** in the [PyPSA](https://pypsa.org/) core, which limits extensibility.
Adding new component formulations or behaviours requires **Python development skills**, while [GEMS](../index.md) allows users to define and extend models declaratively.

<br>

## <img src="../../assets/1_plexos_logo.webp" alt="PLEXOS Logo" width="60" style="vertical-align: middle;"/> PLEXOS® Energy Modeling Software

[PLEXOS®](https://www.energyexemplar.com/plexos) follows a philosophy similar to [Antares Simulator](https://antares-simulator.readthedocs.io/en/latest/), relying on a fixed and **predefined file-based structure** to describe studies.
While powerful, this approach offers limited flexibility when adapting or extending model structures.
[GEMS](../index.md), by contrast, provides a fully configurable modelling language where system structure and component behaviour can evolve without modifying the solver core.

<br/>
<br/>

---

**Navigation**

<div style="display: flex; justify-content: space-between;">
  <div style="text-align: left;">
  <button type="button" style="background-color:#CCCCCC; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
    <a href="../2_File_structure" style="text-decoration:none; color: #000000">⬅️ Previous page</a>
  </button>
  </div>
  <button type="button" style="background-color:#AAAAFF; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
    <a href="../../index" style="text-decoration:none; color: #FFFFFF">Home</a>
  </button>
  <div style="text-align: right;">
  <button type="button" style="background-color:#CCCCCC; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
    <a href="../4_GEMS Interpreters/1_gemspy" style="text-decoration:none; color: #000000">Next page ➡️</a>
  </button>
  </div>
</div>

---
