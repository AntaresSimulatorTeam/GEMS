---
description: Overview of the Legacy-to-GEMS Converter — an open-source Python package that exports Antares Legacy networks as GEMS study folders, supporting linear OPF and stochastic optimisation.
---

<div style="display: flex; justify-content: flex-end;">
  <a href="../..">
    <img src="../../../assets/gemsV2.png" alt="GEMS Logo" width="150"/>
  </a>
</div>

# About

The [Legacy-to-GEMS Converter](https://github.com/AntaresSimulatorTeam/AntaresLegacyModels-to-GEMS-Converter) is an open-source Python package that transforms an Antares Legacy study folder into a GEMS study folder. A tutorial explainign how to use this converter is present through the [README](https://github.com/AntaresSimulatorTeam/AntaresLegacyModels-to-GEMS-Converter/blob/main/README.md) file inside this repo.

It relies on the [`antares_legacy_models` library](https://github.com/AntaresSimulatorTeam/AntaresLegacyModels-to-GEMS-Converter/blob/main/src/antares_gems_converter/libs/antares_historic/antares_legacy_models.yml), which defines the Antares Legacy elements to convert, such as :

- **area**, representing the *legacy* node
- **load**, representing the *legacy* load element
- **link**, representing the *legacy* link element
- **renewable**, representing the *legacy* renewable cluster
- **thermal**, representing the *legacy* thermal cluster
- **short-term-storage**, representing the *legacy* short-term-storage cluster
