---
description: Reference for GEMS business view configuration files — how to define aggregated output views and reporting structures for energy system simulation results.
tags:
  - Energy Modelling
---

<div style="display: flex; justify-content: flex-end;">
    <a href="../../../..">
        <img src="../../../assets/gemsV2.png" alt="GEMS Logo" width="150"/>
    </a>
</div>

# Business Views Configuration Files

 **[Business Views](../outputs/business-view.md)** are result tables designed to meet business-user expectations.  
Each Business View exposes a set of Business Variables, which define the columns of the resulting tables.  
These numerical values are computed exclusively from:

- the data contained in the **[Simulation Table](../outputs/simulation-table.md)**,
- the hypergraph representation of the [system](../file-structure/system.md).
The algorithmic process to compute a Business View from this data is made explicit in a **Business View Configuration File**.

**The configuration and capabilities of Business Outputs are still under active development.**


