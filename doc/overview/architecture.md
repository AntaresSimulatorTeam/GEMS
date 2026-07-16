---
description: Learn how GEMS architecture differs from classical OOME architectures by externalising model definitions into YAML files, enabling solver-agnostic and reusable energy system models.
---

# GEMS Architecture Breakthrough

GEMS represents a fundamental change from classical **OOME architectures (Object-Oriented Modelling Environment)**, where mathematical models are typically **hard-coded** in the software itself.

![Architecture Breakthrough of GEMS comparing to Classical OOME](../../assets/Architecture_OOME.png)

This architecture of GEMS aims to export the definition of component models and system configuration from the core software, by relying on **external YAML files**, which enables:

- **Flexible modelling:** Models and system configurations can be defined, extended, or modified directly in configuration files-no changes to the core code are required.
- **Interoperability:** The GEMS file format supports seamless integration with external tools and workflows, such as converting and simulating PyPSA studies using [GemsPy](gems-interpreters/gemspy.md).

![Architecture Breakthrough of GEMS comparing to Classical OOME](../../assets/Architecture_GEMS.png)