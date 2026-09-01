---
description: Overview of the AntaresLegacyModels-to-GEMS Converter - an open-source Python package that transforms Antares Legacy studies into GEMS study folders, supporting linear OPF and stochastic optimisation.
---

# About

The [AntaresLegacyModels-to-GEMS Converter](https://github.com/AntaresSimulatorTeam/AntaresLegacyModels-to-GEMS-Converter) is an open-source Python package that transforms an Antares Legacy study folder into a [GEMS study folder](../../user-guide/input-files/overview.md).

A tutorial explaining how to use the converter is available in the [README](https://github.com/AntaresSimulatorTeam/AntaresLegacyModels-to-GEMS-Converter/blob/main/README.md) of the repository.

It relies on the [`antares_legacy_models` library](https://github.com/AntaresSimulatorTeam/AntaresLegacyModels-to-GEMS-Converter/blob/main/src/antares_gems_converter/libs/antares_historic/antares_legacy_models.yml) (see also the [reference libraries](../../overview/references/libraries.md) page), which defines the Antares Legacy elements the converter recognises:

- **area** - geographic node
- **load** - load demand
- **link** - interconnection links
- **renewable** - representing renewable clusters
- **thermal** - representing thermal clusters
- **short-term-storage** - representing short-term storage clusters
