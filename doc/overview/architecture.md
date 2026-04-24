---
description: Learn how GEMS architecture differs from classical OOME architectures by externalising model definitions into YAML files, enabling solver-agnostic and reusable energy system models.
tags:
  - Energy Modelling
  - Graph-based Modelling
  - Algebraic Modelling Language
---

<div style="display: flex; justify-content: flex-end;">
  <a href="../../../..">
    <img src="../../assets/gemsV2.png" alt="GEMS Logo" width="150"/>
  </a>
</div>

# GEMS Architecture Breakthrough

GEMS represents a fundamental change from classical **OOME architectures (Object-Oriented Modelling Environment)**, where mathematical models are typically **hard-coded** in the software itself.

<div style="text-align: center;">
  <img src="../../assets/Architecture_OOME.png" alt="Architecture Breakthrough of GEMS comparing to Classical OOME" />
</div>

This architecture of GEMS aims to export the definition of component models and system configuration from the core software, by relying on **external YAML files**, which enables:

- **Flexible modelling:** Models and system configurations can be defined, extended, or modified directly in configuration files—no changes to the core code are required.
- **Interoperability:** The GEMS file format supports seamless integration with external tools and workflows, such as converting and simulating PyPSA studies using GemsPy.

<div style="text-align: center; width:1000px;">
  <img src="../../assets/Architecture_GEMS.png" alt="Architecture Breakthrough of GEMS comparing to Classical OOME" />
</div>