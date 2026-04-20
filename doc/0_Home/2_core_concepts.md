<div style="display: flex; justify-content: flex-end;">
  <a href="../../../..">
    <img src="../../assets/gemsV2.png" alt="GEMS Logo" width="150"/>
  </a>
</div>

# An Optimisation Language Tailored for Energy System Modelling

**GEMS** is a graph-based [algebraic modelling language](https://en.wikipedia.org/wiki/Algebraic_modeling_language) for building, managing, and solving optimization problems that describe energy systems.

This language **differs from traditional optimization languages** in several ways by natively accounting for the specific needs of energy system modelling. Its underlying motivation is to provide essential features for advanced energy modelling: **a readable and user-friendly syntax, strong flexibility, and a tool-agnostic design.**

<div style="height: 500px; overflow: hidden;">
  <img src="../../assets/Gems_core_concepts.png" alt="Core Concepts" style="height: 100%; object-fit: contain;"/>
</div>

<br>

# Defining Models and Systems as YAML Configurations
<style>
.yaml-diptych pre { white-space: pre-wrap; word-break: break-all; }
</style>
<div class="yaml-diptych" style="display: flex; gap: 1.5rem; align-items: flex-start; width: 125%">
<div style="flex: 1; min-width: 0;">

<h3> Library </h3>

A YAML file defining abstract objects called <a href="../3_User_Guide/3_GEMS_File_Structure/2_library.md#models">models</a>, which describe the mathematical formulation of a category of energy system element.

<br>
<br>
For more details, see the <a href="../3_User_Guide/3_GEMS_File_Structure/2_library.md"><b>Library</b></a> page of the user guide.

```yaml
library:

  id: example_library
  description: "Example model library"

  models:
    - id: bus
      description: "A simple balance node model"
      ports:
        - id: balance_port
          type: flow_port
      binding-constraints:
        - id: balance
          expression: sum_connections(flow_port.flow) = 0

    - id: generator
      parameters:
        - id: p_min
        - id: p_max
        - id: generation_cost
        - id: co2_emission_factor
      variables:
        - id: generation
          lower-bound: p_min
          upper-bound: p_max
          variable-type: continuous
      ports:
        - id: balance_port
          type: flow
        - id: energy_port
          type: energy
        - id: emission_port
          type: emission
      port-field-definitions:
        - port: balance_port
          field: flow
          definition: generation
        - port: energy_port
          field: cumulative_energy
          definition: sum(generation)
        - port: emission_port
          field: co2
          definition: sum(generation * co2_emission_factor)
      objective-contributions:
        - id: objective
          expression: sum(generation_cost * generation)
```

</div>
<div style="flex: 1; min-width: 0;">

<h3> System </h3>

A YAML file describing the concrete energy system to be simulated. It instantiates components from models provided by the libraries, assigns parameter values, and defines the connections between components.

<br>
For more details, see the <a href="../3_User_Guide/3_GEMS_File_Structure/3_system.md"><b>System</b></a> page of the user guide.

```yaml
system:
  id: my_system
  description: "An example system with one load, one node, one thermal generator"
  model-libraries: example_library
  components:

    - id: load_1
      model: example_library.load
      scenario-group: load_group
      parameters:
        - id: load
          time-dependent: true
          value: demand_profile

    - id: bus_1
      model: example_library.bus
      parameters:
        - id: spillage_cost
          value: 1000
        - id: unsupplied_energy_cost
          value: 10000

    - id: generator_1
      model: example_library.generator
      parameters:
        - id: p_min
          value: 70
        - id: p_max
          value: 100
        - id: generation_cost
          value: 35
        - id: co2_emission_factor
          value: 0
```

</div>
</div>

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
