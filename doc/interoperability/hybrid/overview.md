---
description: How to configure and run Antares Simulator hybrid studies — combining GEMS components with Antares Legacy areas in a single simulation for multi-model energy system studies.
tags:
  - Interoperability
  - Hybrid Studies
  - Antares Simulator
---

<div style="display: flex; justify-content: flex-end;">
  <a href="../..">
    <img src="../../../assets/gemsV2.png" alt="GEMS Logo" width="150"/>
  </a>
</div>

# Antares Simulator Hybrid studies

This page explains how to configure and run a [**hybrid study**](https://antares-simulator.readthedocs.io/en/latest/user-guide/solver/08-hybrid-studies/) i.e. a study combining **GEMS components** and **Antares Simulator's Legacy Components**. In a hybrid study, the GEMS files are integrated into a Antares Simulator study's directory structure, allowing Antares Simulator to incorporate GEMS components.

## Definition

A [**hybrid study**](https://antares-simulator.readthedocs.io/en/latest/user-guide/solver/08-hybrid-studies/) is essentially a **Antares Simulator** study that includes additional **GEMS** input data (in the `input/` folder). The Antares Simulator executable (*antares-solver*) is able to run such a simulation, although the input directory contains **GEMS-specific files** (such as system, model libraries and data-series) describing GEMS components.

In this hybrid mode, the file `parameter.yml` is not used: if it exists, it will be ignored. Instead, the study relies on the Antares Simulator simulation settings. In summary, the **hybrid study's** input directory merges the modeler files with the typical Antares files, and the Antares solver's built-in GEMS interpreter handles the GEMS components during the simulation.

```text
Antares-Simulator-Study/
├── input/
│   ├── areas/
│   ├── bindingconstraints/
│   ├── ...
│   ├── model-libraries/     # Modeler libraries folder
│   ├── system.yml           # Modeler system file
│   └── data-series/         # Modeler dataseries folder
├── layers/
├── logs/
├── output/
├── settings/
├── user/
├── Desktop.ini
├── Logs.log
└── study.antares
```

## Table of Contents

- [Coupling GEMS Components with Legacy Areas](hybrid-connections.md)
- [Run a Hybrid Study](how-to-run.md)
- [Outputs](outputs.md)
- [Simple Example](example.md)
- [Limitations](limitations.md)
