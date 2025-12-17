<div style="display: flex; justify-content: space-between; align-items: center;">
  <div style="text-align: left;">
    <a href="../../../..">Main Section</a>
  </div>
  <div style="text-align: right;">
    <img src="../../../assets/gemsV2.png" alt="GEMS Logo" width="150"/>
  </div>
</div>

# GEMS Framework Syntax

The **GEMS framework** relies on a well-defined, declarative syntax to describe optimisation problems in a clear, solver-independent, and reproducible way.

From a user and documentation perspective, the GEMS syntax can be explicitly separated into **two complementary layers**, each serving a distinct purpose:

- **Mathematical Syntax** — [describes *what is being modeled*](../2_mathematical_syntax)
- **Configuration Syntax** — [describes *how it is declared and structured*](../3_configuration_syntax)

This separation is fundamental to understanding how GEMS models are written, interpreted, and validated.

---

## Overview

GEMS models are not written as imperative programs.  
Instead, they are defined using **structured configuration files** combined with **mathematical expressions**.

Each layer plays a different role:

| Layer | Purpose | Typical Content |
|------|--------|----------------|
| Mathematical Syntax | Express optimisation logic | Equations, constraints, objectives |
| Configuration Syntax | Declare and organize models and system | YAML structure, keywords, sections |

Keeping these concerns separate improves readability, validation, and long-term maintainability of models.

---

## 1. Mathematical Syntax

The **GEMS Framework Mathematical Syntax** is used to express the mathematical formulation of an optimisation problem.

It defines:

- Arithmetic and comparison operators
- Linear expressions involving parameters, variables, and port fields
- Constraint and objective expressions
- Time and scenario operators
- Aggregation operators
- Linearity and dimensionality rules

Mathematical syntax is **solver-agnostic** and intentionally restricted to ensure that all models remain linear (LP/MILP) and unambiguous.

> Mathematical syntax focuses exclusively on *equations and rules*. It does not describe where variables come from or how models are wired together.

➡️ See: [**Mathematical Syntax and Rules**](../2_mathematical_syntax)

---

## 2. Configuration Syntax

The **GEMS Framework Configuration Syntax** defines how optimisation models are **declared, structured, and connected** using YAML files.

It specifies:

- How models are defined in libraries
- How variables, parameters, ports, and constraints are declared
- How components are instantiated and connected in the system file
- How parameters are provided and referenced
- How optimisation options are configured

This syntax governs the **structure and semantics** of all GEMS YAML files.

### Configuration Files Covered

The Configuration Syntax applies to all GEMS configuration files, including:

- **Model libraries**
- **System file**
- **Parameter files**
- **Optimization configuration**

Each file type has:
- A well-defined structure
- Allowed keywords and sections
- Validation rules

> Although YAML is used as the file format, the Configuration Syntax is **GEMS-specific** and goes far beyond generic YAML rules.

➡️ See: [**Configuration Syntax (YAML)**](../3_configuration_syntax)

---

## Why This Separation Matters

Separating mathematical and configuration syntax provides several benefits:

- Clarifies the distinction between *model logic* and *model declaration*
- Makes documentation easier to navigate
- Helps users reason about errors (math vs structure)
- Supports long-term extensibility of the framework

!!! tip
    When debugging a model, first ask:
    *Is this a mathematical formulation issue, or a configuration issue?*

---

## Summary

The GEMS Framework syntax consists of two tightly integrated but clearly distinct layers:

- **Mathematical Syntax**  
  Defines the optimisation problem itself

- **Configuration Syntax**  
  Defines how the problem is described, structured, and assembled

Together, they allow GEMS to combine expressive mathematical modeling with a clean, declarative configuration approach.

---
**Navigation**
<div style="display: flex; justify-content: space-between;">
  <div style="text-align: left;">
  <button type="button" style="background-color:#CCCCCC; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
    <a href="../2_Getting_Started/2_quick_start_examples" style="text-decoration:none; color: #000000">⬅️ Previous page</a>
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