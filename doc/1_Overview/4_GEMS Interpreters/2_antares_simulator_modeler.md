<div style="display: flex; justify-content: flex-end;">
    <a href="../../../..">
        <img src="../../../assets/gemsV2.png" alt="GEMS Logo" width="150"/>
    </a>
</div>

# Antares Simulator's GEMS interpreter

<div style="text-align: center;">
  <img src="../../../assets/5_antares_sim_logo.webp" alt="Antares Simulator logo" style="height: 70px;"/>
</div>

[Antares Simulator](https://antares-simulator.readthedocs.io/en/latest/) includes a GEMS interpreter. This piece of code is a graph-based optimization problem builder that provides a comprehensive environment for constructing, configuring, and solving LP, MIP, and MILP problems. Its design emphasizes flexibility, enabling users to tailor mathematical formulations, data structures, and model components to suit the specific requirements of their studies.

Integrated alongside the **Antares Simulator [^1]**, this GEMS interpreter introduces new possibilities for extending legacy optimization structures directly within Antares studies. This integration enables users to broaden the standard simulation framework by creating new models and exploring enhanced problem formulations, all while remaining fully compatible with the Antares Simulator ecosystem.
Two different usage mode of the GEMS interpreter are available with [Antares Simulator](https://antares-simulator.readthedocs.io/en/latest/) :

- **Hybrid mode**: allows the construction of studies that combine Antares’ legacy components with GEMS components. In terms of temporal and uncertainty modeling, this mode follows the historical approach of [Antares Simulator](https://antares-simulator.readthedocs.io/en/latest/). It is executed using `antares-solver`, the traditional Antares Simulator executable.  
- **Full modeler mode**: exclusively supports GEMS components and provides greater flexibility, as it is not constrained by [Antares Simulator](https://antares-simulator.readthedocs.io/en/latest/)’s temporal and uncertainty structures. It is executed using `antares-modeler`.

For detailed usage and examples of [Antares Simulator](https://antares-simulator.readthedocs.io/en/latest/) and its GEMS interpreter, see:

- [Installation Guide](../../2_Getting_Started/1A_modeler_installation.md)
- [Examples section](../../5_Examples/1_adequacy_example.md)
- [The official Antares Simulator Documentation - Modeler section](https://antares-simulator.readthedocs.io/en/latest/user-guide/modeler/01-overview-modeler/)

[^1]: **Antares Simulator** is an open-source power system simulator designed to quantify the adequacy and economic performance of interconnected energy systems in the long term. It is used by transmission system operators for probabilistic simulations of energy consumption, generation, and transportation.