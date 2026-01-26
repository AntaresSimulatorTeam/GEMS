<div style="display: flex; justify-content: space-between; align-items: center;">
  <div style="text-align: left;">
    <a href="../../../..">Main Section</a>
  </div>
  <div style="text-align: right;">
    <img src="../../../assets/gemsV2.png" alt="GEMS Logo" width="150"/>
  </div>
</div>

# GEMS Framework Introduction

The [**GEMS framework**](../index.md) provides a declarative way to describe energy systems — and more generally, graph-based optimization problems — in a clear, stand-alone, solver-independent, and reproducible manner.

Rather than writing imperative code, users define a study through **structured configuration files**, **mathematical expressions**, and **well-defined concepts** that together allow [GEMS](../index.md) to:

- interpret a system as a connected graph of components,
- construct the corresponding optimization problem,
- solve it with a selected solver,
- and expose results in consistent output formats.

From a documentation perspective, the User Guide is organized into **four complementary sections**, each serving a distinct purpose:

- [**Mathematical Syntax**](#mathematical-syntax) — rules for writing mathematical expressions

- [**File Structure**](#file-structure) — rules for writing [GEMS](../index.md) YAML files and how they reference each other  

- [**Theoretical Concepts**](#theoretical-concepts) — core ideas behind the system representation and optimization formulation

- [**Outputs**](#outputs) — produced result formats and how to interpret them  

This separation is fundamental to understanding how [GEMS](../index.md) systems are written, interpreted, validated, and analysed.

---

## Mathematical Syntax

The **GEMS Framework Mathematical Syntax** represents set of rules for creating mathematical expressions which will be used in building an optimization problem.

It defines:

- Arithmetic and comparison operators
- Linear expressions involving parameters, variables, and port fields, constraints and objective function
- Time and scenario operators
- Aggregation operators
- Linearity rules
- Additional Operators

Mathematical syntax is **solver-agnostic** and intentionally restricted to ensure that all optimization problems - representing systems - remain linear (LP/MILP) and unambiguous.

Mathematical syntax focuses exclusively on *equations and rules*. It does not describe where parameters and variables come from or how components are wired together as a system.

See: [**Mathematical Syntax and Rules**](./2_mathematical_syntax.md)

---

## File Structure

The **GEMS Framework File Structure** defines how components are **declared, structured, and connected**  to form a system, and how these systems can be translated as optimization problems, using YAML files.

It specifies:

- How models and ports are defined in libraries
- How variables, parameters, ports, constraints and objective function are declared in a model
- How components are instantiated
- How parameters are defined in a component
- How to use ports to connect components to form a system graph
- How optimization options are configured
- (When applicable) How to create Business View configuration file

These rules governs the **structure and semantics** of all [GEMS](../index.md) YAML files.

See: [**File Structure**](./3_GEMS_File_Structure/1_overview.md)

## Theoretical Concepts

The **Theoretical Concepts** section explains the core ideas behind how [GEMS](../index.md) represents a system and builds an optimization problem.

It introduces:

- The **hypergraph representation** of a system (components + ports + connections)
- The distinction between **models** (templates) and **components** (instances)
- How constraints and objectives are assembled into a global optimization problem
- How time and scenarios unfold into a larger deterministic or stochastic formulation
- (When applicable) concepts behind **two-stage** stochastic modelling

This section is conceptual: it explains *why* the file structure and syntax are designed the way they are.

See: [**Theoretical Concepts**](./4_Theoretical_Concepts/1_hypergraph_structure.md)

## Outputs

The **Outputs** section describes what [GEMS](../index.md) produces after interpretation and solving, and how to consume results.

It covers:

- The **Simulation Table** (standard structured results)
- The exported **optimization problem**
- **Business View**: configured aggregations and indicators for analysis/reporting

Outputs depend on the selected interpreter and run configuration, but the documentation provides a consistent way to locate and interpret results.

See: [**Outputs and Result Formats**](./5_Outputs/1_simulation_table.md)

---
**Navigation**

<div style="display: flex; justify-content: space-between;">
    <div style="text-align: left;">
    <button type="button" style="background-color:#CCCCCC; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
        <a href="../../2_Getting_Started/2B_QSE_unit_commitment" style="text-decoration:none; color: #000000">⬅️ Previous page</a>
    </button>
    </div>
    <button type="button" style="background-color:#AAAAFF; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
        <a href="../../../.." style="text-decoration:none; color: #FFFFFF">Home</a>
    </button>
    <div style="text-align: right;">
    <button type="button" style="background-color:#CCCCCC; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
        <a href="../2_mathematical_syntax" style="text-decoration:none; color: #000000">Next page ➡️</a>
    </button>
    </div>
</div>

---

