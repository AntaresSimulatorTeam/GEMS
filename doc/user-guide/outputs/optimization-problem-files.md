<div style="display: flex; justify-content: flex-end;">
    <a href="../../../..">
        <img src="../../../assets/gemsV2.png" alt="GEMS Logo" width="150"/>
    </a>
</div>

# Optimization Problem MPS Files

One can expect from any [GEMS](../../index.md) interpreter to export the fully assembled optimisation problem in a **standard mathematical programming format** [**MPS**](https://lpsolve.sourceforge.net/5.5/mps-format.htm?utm_source=chatgpt.com). The exported file contains the complete linear or mixed-integer formulation constructed from the system configuration, model libraries, and input data.

This export is primarily intended for **verification, debugging, and external analysis** of the optimisation problem.

A **GEMS interpreter** generates a MPS file in the study **output directory**. This functionality is available only in the [Antares Modeler interpreter](../../overview/gems-interpreters/antares-simulator.md). The [GemsPy interpreter](../../overview/gems-interpreters/gemspy.md) does not currently have a native function for this purpose; using the dedicated method of the underlying `OR-Tools` object that represents the optimisation problem is one possible way to export the MPS file.

The MPS file follows the naming convention `{year}-{block}.mps`, where `year` is the Monte Carlo year number and `block` is the optimization block number. For example, `1-1.mps` corresponds to year 1, block 1.

The file is typically overwritten each time the study is executed.

