<div style="display: flex; justify-content: space-between; align-items: center;">
    <div style="text-align: left;">
        <a href="../../../..">Main Section</a>
    </div>
    <div style="text-align: right;">
        <img src="../../assets/gemsV2.png" alt="GEMS Logo" width="150"/>
    </div>
</div>

# An Optimisation Language Tailored for Energy System Modelling

**GEMS** is a graph-based [algebraic modelling language](https://en.wikipedia.org/wiki/Algebraic_modeling_language) for building, managing, and solving optimization problems that describe energy systems.

This language **differs from traditional optimization languages** in several ways by natively accounting for the specific needs of energy system modelling. Its underlying motivation is to provide essential features for advanced energy modelling: **a readable and user-friendly syntax, strong flexibility, and a tool-agnostic design.**

<div style="height: 500px; overflow: hidden;">
  <img src="../../assets/Gems_core_concepts.png" alt="Core Concepts" style="height: 100%; object-fit: contain;"/>
</div>

<br>

# Key Design Principles and Capabilities

## Separating Model Definition from Solver Execution

<div style="display: flex; align-items: flex-start; gap: 15px; margin-bottom: 25px;">
  <img src="../../assets/Core_concept_solver_modeler.png"
       width="40"
       alt="Graph oriented icon"/>

  <p style="margin: 0;">
    GEMS as a modelling language adopts an approach that clearly distinguishes <strong>model definition</strong> from <strong>numerical computations</strong>. This allows users to focus on the structure and behavior of energy systems without being immediately concerned with optimization details. Mathematical equations ruling energy system components are not hard-coded in a software code, they are dynamically interpreted: they remain independent from the simulation tool and from the underlying optimization solver (independence from the optimisation solver is admittedly more standard). This separation <strong> facilitates reuse, experimentation, and maintenance of models </strong>, while making it easy to test different solvers or resolution settings as needed.
  </p>
</div>

## Model Energy Systems as Connected Objects (Hypergraphs)

<div style="display: flex; align-items: flex-start; gap: 15px; margin-bottom: 25px;">
  <img src="../../assets/Core_concept_graph_oriented.png"
       width="40"
       alt="Graph oriented icon"/>

  <p style="margin: 0;">
    Unlike traditional algebraic modelling languages such as
    <strong>AMPL or GAMS</strong>, GEMS adopts an
    <strong>object-oriented</strong> and
    <strong>graph-oriented</strong> approach.
    Abstract <strong>models</strong> of components are defined in
    <strong>Libraries</strong> and can then be
    <strong>instantiated, assembled, and interconnected</strong>
    to form concrete <strong>Systems</strong>.
    Systems are graphs of components, that can be translated into an optimization problem.
  </p>
</div>

## Integrated Time and Uncertainty Dimensions

<div style="display: flex; align-items: flex-start; gap: 15px; margin-bottom: 25px;">
  <img src="../../assets/Core_concept_time_scenario.png" width="40" alt="Time Scenario icon"/>

  <p style="margin: 0;">
  GEMS natively incorporates <strong> time and scenario dimensions</strong> into its modelling framework.
  <strong>Temporal </strong> and <strong>scenarios </strong> indices are natively available in the language, either in an implicit or explicit form. This allows users to easly define <strong>dynamic behaviours, inter-temporal constraints, and scenario-based analyses</strong> in a clear and structured way, while ensuring consistency and scalability of the resulting optimisation problems.
  </p>
</div>

## Supported Optimisation Problem Classes

<div style="display: flex; align-items: flex-start; gap: 15px; margin-bottom: 25px;">
  <img src="../../assets/Core_concept_optimisation_problems.png" width="40" alt="Optimisation icon"/>

  <div>
    <p style="margin: 0 0 8px 0;">
      GEMS supports a wide range of optimisation formulations commonly used in energy system studies.
      It is designed to handle:
    </p>

    <ul style="margin: 0; padding-left: 20px;">
      <li>
        <strong> <a href="https://en.wikipedia.org/wiki/Integer_programming">Mixed Integer Linear Programming (MILP)</a> </strong> problems, enabling the representation
        of discrete operational or investment decisions alongside continuous operational variables.
      </li>
      <li>
        <strong> <a href="https://en.wikipedia.org/wiki/Stochastic_programming">Two-stage stochastic optimisation </a> </strong> problems, where first-stage (here-and-now)
        decisions are coupled with second-stage (recourse) decisions, providing a robust
        framework for decision-making under uncertainty.
      </li>
    </ul>
  </div>
</div>

## YAML-Based, User-Friendly Model Definition

<div style="display: flex; align-items: flex-start; gap: 15px; margin-bottom: 25px;">
  <img src="../../assets/Core_concept_yaml_file.png" width="40" alt="YAML file icon"/>
  <p style="margin: 0;">
  GEMS relies on <strong> YAML configuration files </strong> to provide a user-friendly and transparent
  modelling interface.
  YAML enables readable, structured, and easily editable model definitions,
  lowering the barrier for new users while remaining expressive enough for advanced use cases.
  This approach facilitates <strong> model versioning, collaboration, and integration with external tools </strong>,
  while clearly separating model structure, data, and assumptions from the underlying optimisation engine.
   </p>
</div>

**Navigation**

<div style="display: flex; justify-content: space-between;">
    <div style="text-align: left;">
    <button type="button" style="background-color:#CCCCCC; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
        <a href="../../../.." style="text-decoration:none; color: #000000">⬅️ Previous page</a>
    </button>
    </div>
    <button type="button" style="background-color:#AAAAFF; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
        <a href="../../../.." style="text-decoration:none; color: #FFFFFF">Home</a>
    </button>
    <div style="text-align: right;">
    <button type="button" style="background-color:#CCCCCC; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
        <a href="../3_use_cases" style="text-decoration:none; color: #000000">Next page ➡️</a>
    </button>
    </div>
</div>

---
