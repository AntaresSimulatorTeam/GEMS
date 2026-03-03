<div style="display: flex; justify-content: space-between; align-items: center;">
    <div style="text-align: left;">
        <a href="../../../..">Main Section</a>
    </div>
    <div style="text-align: right;">
        <img src="../../../assets/gemsV2.png" alt="GEMS Logo" width="150"/>
    </div>
</div>

# Optimization Problem MPS File

One can expect from any [GEMS](../../index.md) interpreter to export the fully assembled optimisation problem in a **standard mathematical programming format** [**MPS**](https://lpsolve.sourceforge.net/5.5/mps-format.htm?utm_source=chatgpt.com). The exported file contains the complete linear or mixed-integer formulation constructed from the system configuration, model libraries, and input data.

This export is primarily intended for **verification, debugging, and external analysis** of the optimisation problem.

A **GEMS interpreter** generates a MPS file in the study **output directory**. This functionality is available only in the [Antares Modeler interpreter](../../1_Overview/4_GEMS%20Interpreters/2_antares_simulator_modeler.md). The [GemsPy interpreter](../../1_Overview/4_GEMS%20Interpreters/1_gemspy.md) does not currently have a native function for this purpose; using the dedicated method of the underlying `OR-Tools` object that represents the optimisation problem is one possible way to export the MPS file.

For example, the file `1-1.mps` is automatically created in the output folder and represents the exact optimisation problem solved during the execution.

The file is typically overwritten each time the study is executed.

