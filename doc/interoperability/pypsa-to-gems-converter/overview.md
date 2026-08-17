---
description: Overview of the PyPSA-to-GEMS Converter - an open-source Python package that exports PyPSA networks as GEMS study folders, supporting linear OPF and stochastic optimisation.
---

# Overview

The [PyPSA-to-GEMS](https://github.com/AntaresSimulatorTeam/PyPSA-to-GEMS-Converter) Converter 
is an open-source & standalone python package that enables the conversion of studies conducted in PyPSA into the GEMS format: it exports a [PyPSA Network](https://docs.pypsa.org/latest/api/networks/network) as a [GEMS](https://gems-energy.readthedocs.io/en/latest/user-guide/file-structure/overview/) folder.

This converter is based on the representation of the PyPSA models of components as a GEMS library of models: [pypsa_models.yml](https://github.com/AntaresSimulatorTeam/GEMS/blob/main/libraries/pypsa_models.yml).

### Key Features

- **Conversion of linear optimal power flow & economical dispatch studies**
- **Conversion of two-stage stochastic optimization studies**

## Table of Contents

- [How the Converter Works](./how-the-converter-works.md)
- [Input and Output of the Converter](./input-and-output.md)
- [Current Limitations of the Converter](./current-limitations.md)
- [Step-by-Step Guide: Manually Executing a Simulation in GEMS Modeler](./step-by-step-guide.md)
- [Comparing Results Between GEMS Modeler and PyPSA](./comparing-results.md)