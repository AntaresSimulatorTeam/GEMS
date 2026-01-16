<div style="display: flex; justify-content: space-between; align-items: center;">
  <div style="text-align: left;">
    <a href="../../../..">Main Section</a>
  </div>
  <div style="text-align: right;">
    <img src="../../assets/gemsV2.png" alt="GEMS Logo" width="150"/>
  </div>
</div>

# Differences with other modelling languages and tools
## MODELICA Language 

Modelica is a language designed for modelling physical systems based **on differential and algebraic equations**, with a strong focus on dynamic behaviour and simulation.
In contrast, GEMS is dedicated to the formulation of **mathematical optimisation problems**, making it better suited for long-term energy system studies.
While Modelica excels at component-level dynamics, GEMS focuses on system-wide decision-making, planning, and optimisation.

<br>

## GAMS - General Algebraic Modeling System

GAMS is a powerful language for expressing mathematical optimisation problems in an algebraic form.
However, it does **not provide a native object-oriented or graph-based modelling paradigm**.
GEMS’ object and graph-oriented approach is particularly well suited for modelling interconnected energy systems, where similar components (generators, batteries, loads) are replicated across multiple nodes.

<br>

## Linopy - Python Package -  Linear optimization with n-dimensional labeled variables
While both Linopy and GEMS are used to formulate optimisation problems, they serve fundamentally different purposes. Linopy is a Python-based modelling library designed to conveniently express and solve optimisation problems within a **specific software ecosystem, closely tied to Python workflows** and solver interfaces. In contrast, GEMS is conceived as a generic, self-contained optimisation language that explicitly formultes the energy system, its components, and their behaviour independently of any particular implementation or solver. 
<br> <br>
**By separating model definition from problem resolution**, GEMS prioritises interpretability, interoperability, and long-term maintainability, enabling models to be shared, reused, and understood across tools, institutions, and time horizons—an essential requirement for long-term energy system studies and collaborative modelling communities.

<br>

## Antares Simulator (Legacy)

Historically, Antares Simulator, an open-source tool for long-term energy system studies, relies on a **fixed file tree structure** as its main input format.
This structure is hard-coded in the tool, which limits flexibility and extensibility.
Introducing new objects or behaviours typically requires **modifying the C++ source code**, whereas GEMS allows such extensions directly at the modelling language level.

<br>

## PyPSA – Python for Power System Analysis

PyPSA enables the generation of energy system studies using flexible configuration files and **produces a NetCDF** representation of the resulting model.
However, **the component models themselves are hard-coded** in the PyPSA core, which limits extensibility.
Adding new component formulations or behaviours requires **Python development skills**, while GEMS allows users to define and extend models declaratively.

<br>

## PLEXOS® Energy Modeling Software

PLEXOS follows a philosophy similar to Antares Simulator, relying on a fixed and **predefined file-based structure** to describe studies.
While powerful, this approach offers limited flexibility when adapting or extending model structures.
GEMS, by contrast, provides a fully configurable modelling language where system structure and component behaviour can evolve without modifying the solver core.

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

