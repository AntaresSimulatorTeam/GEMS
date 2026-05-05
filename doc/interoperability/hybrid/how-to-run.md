<div style="display: flex; justify-content: flex-end;">
  <a href="../..">
    <img src="../../../assets/gemsV2.png" alt="GEMS Logo" width="150"/>
  </a>
</div>

# Run a Hybrid Study

After setting up the connections as described above, **running a hybrid study** is done in the same way as [running a standard Antares simulation](https://antares-simulator.readthedocs.io/en/latest/user-guide/solver/10-command-line/). The study can be opened or launched with Antares Simulator (using the GUI or the command-line solver). The presence of the file `system.yml` and the folder `model-libraries` in the input folder will trigger the Antares solver's GEMS interpreter to load those components. The solver will then construct a combined optimization problem that includes both the Legacy elements (areas, thermal plants, hydro, etc.) and the GEMS components defined by the user.

Once the run starts, it will simulate with the combined model. Results for the GEMS components (e.g., generation output of a custom component) will appear alongside the usual Antares results for areas, provided that output has been configured for those components (the GEMS framework will handle output storage in the study results).
