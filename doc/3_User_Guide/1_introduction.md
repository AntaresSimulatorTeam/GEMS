<div style="display: flex; justify-content: space-between; align-items: center;">
  <div style="text-align: left;">
    <a href="../../../..">Main Section</a>
  </div>
  <div style="text-align: right;">
    <img src="../../../assets/gemsV2.png" alt="GEMS Logo" width="150"/>
  </div>
</div>

# GEMS Framework Introduction

The **GEMS framework** provides a declarative way to describe energy systems — and more generally, graph-based optimisation problems — in a clear, stand-alone, solver-independent, and reproducible manner.

Rather than writing imperative code, users define a study through **structured configuration files**, **mathematical expressions**, and **well-defined concepts** that together allow GEMS to:

- interpret a system as a connected graph of components,
- construct the corresponding optimisation problem,
- solve it with a selected backend,
- and expose results in consistent output formats.

From a documentation perspective, the User Guide is organized into **four complementary sections**, each serving a distinct purpose:

- [**Mathematical Syntax**](#mathematical-syntax) — rules for writing mathematical expressions used in constraints and objectives  

- [**Data Structure**](#data-structure) — rules for configuring GEMS YAML files and how they reference each other  

- [**Theoretical Concepts**](#theoretical-concepts) — core ideas behind the system representation and optimisation formulation

- [**Outputs**](#outputs) — produced result formats and how to interpret them  

This separation is fundamental to understanding how GEMS models are written, interpreted, validated, and analysed.

---

## Mathematical Syntax

The **GEMS Framework Mathematical Syntax** represents set of rules for creating mathematical expression which will be used in building an optimization problem.

It defines:

- Arithmetic and comparison operators
- Linear expressions involving parameters, variables, and port fields, constraints and objective function
- Time and scenario operators
- Aggregation operators
- Linearity rules
- Additional Operators

Mathematical syntax is **solver-agnostic** and intentionally restricted to ensure that all models remain linear (LP/MILP) and unambiguous.

> Mathematical syntax focuses exclusively on *equations and rules*. It does not describe where variables come from or how models are wired together.

➡️ See: [**Mathematical Syntax and Rules**](../2_mathematical_syntax)

---

## Data Structure

The **GEMS Framework Data Structure** defines how optimisation models are **declared, structured, and connected** using YAML files.

It specifies:

- How models and ports are defined in libraries
- How variables, parameters, ports, constraints and objective function are declared in a model
- How components are instantiated
- How parameters are defined in a component
- How to use ports to connect components to form a system graph
- How optimisation options are configured
- (When applicable) How to create Business View configuration file

These rules governs the **structure and semantics** of all GEMS YAML files.

➡️ See: [**Data Structure**](../3_configuration_syntax)

## Theoretical Concepts

The **Theoretical Concepts** section explains the core ideas behind how GEMS represents a system and builds an optimisation model.

It introduces:

- The **hypergraph representation** of a system (components + ports + connections)
- The distinction between **models** (templates) and **components** (instances)
- How constraints and objectives are assembled into a global optimisation problem
- How time and scenarios unfold into a larger deterministic or stochastic formulation
- (When applicable) concepts behind **two-stage** stochastic modelling

> This section is conceptual: it explains *why* the file structure and syntax are designed the way they are.

➡️ See: [**Theoretical Concepts**](../4_theoretical_concepts)


## Outputs

The **Outputs** section describes what GEMS produces after interpretation and solving, and how to consume results.

It covers:

- The **Simulation Table** (standard structured results)
- The exported **optimization problem**
- **Business View**: configured aggregations and indicators for analysis/reporting

> Outputs depend on the selected interpreter and run configuration, but the documentation provides a consistent way to locate and interpret results.

➡️ See: [**Outputs and Result Formats**](../5_outputs)


---
**Navigation**
<div style="display: flex; justify-content: space-between;">
  <div style="text-align: left;">
  <button type="button" style="background-color:#CCCCCC; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
    <a href="../../2_Getting_Started/2_quick_start_examples" style="text-decoration:none; color: #000000">⬅️ Previous page</a>
  </button>
  </div>
  <button type="button" style="background-color:#AAAAFF; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
    <a href="../../../.." style="text-decoration:none; color: #FFFFFF">Index</a>
  </button>
  <div style="text-align: right;">
  <button type="button" style="background-color:#CCCCCC; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
    <a href="../2_mathematical_syntax" style="text-decoration:none; color: #000000">Next page ➡️</a>
  </button>
  </div>
</div>

---

© GEMS (LICENSE)