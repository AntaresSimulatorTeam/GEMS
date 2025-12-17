# GEMS Framework Syntax

The **GEMS framework** relies on a well-defined, declarative syntax to describe optimisation problems in a clear, solver-independent, and reproducible way.

From a user and documentation perspective, the GEMS syntax can be explicitly separated into **two complementary layers**, each serving a distinct purpose:

- **Mathematical Syntax** — describes *what is being modeled*
- **Configuration Syntax** — describes *how it is declared and structured*

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

!!! note
    Mathematical syntax focuses exclusively on *equations and rules*.
    It does not describe where variables come from or how models are wired together.

➡️ See: **Mathematical Syntax and Rules**

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

!!! note
    Although YAML is used as the file format, the Configuration Syntax is
    **GEMS-specific** and goes far beyond generic YAML rules.

➡️ See: **Configuration Syntax (YAML)**

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