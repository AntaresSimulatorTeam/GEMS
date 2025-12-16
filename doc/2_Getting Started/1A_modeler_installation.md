<div style="display: flex; justify-content: space-between; align-items: center;">
  <div style="text-align: left;">
    <a href="../../../..">Main Section</a>
  </div>
  <div style="text-align: right;">
    <img src="../../assets/gemsV2.png" alt="GEMS Logo" width="150"/>
  </div>
</div>

# Antares Simulator's GEMS interpreter

This section outlines the approach for configuring and utilizing the **Antares Modeler**, the interpreter for the **GEMS language** inside [Antares Simulator](https://github.com/AntaresSimulatorTeam/Antares_Simulator).

## Installation

Note that the current **last stable version** of Antares Simulator is [**9.3.2**](https://github.com/AntaresSimulatorTeam/Antares_Simulator/releases/tag/v9.3.2).

### Download and Extract

1. Go to the [**Antares Simulator releases page**](https://github.com/AntaresSimulatorTeam/Antares_Simulator/releases)
2. Download the appropriate archive for your platform:
    - **Windows**: `rte-antares-<simulator-version>-installer-64bits.zip`
    - **Linux**: `rte-antares-<simulator-version>-Ubuntu-<ubuntu-version>tar.gz`
3. Extract the archive to your desired location:
    - **Windows**: Right-click and select "Extraction"
    - **Linux**: `tar -xzf rte-antares-<simulator-version>-Ubuntu-<ubuntu-version>tar.gz`

<div style="height: 500px; overflow: hidden;">
  <img src="../../assets/2_Modeler_download.png" alt="Download Page" style="height: 100%; object-fit: contain;"/>
</div>

### Locate the Executables

After extraction, navigate to the `bin` folder inside the extracted directory. You will find:

- **Antares Modeler executable** (`antares-modeler` or `antares-modeler.exe`)
- **Antares Solver executable** (`antares-solver` or `antares-solver.exe`)

**Antares Modeler** is currently a command-line–only tool with no graphical interface yet. It is used for launching studies with full GEMS syntax.
**Antares Solver** is designed for running Antares legacy study and hybrid studies comprising a mix of legacy and Gems models.

<div style="height: 200px; overflow: hidden;">
  <img src="../../assets/2_Modeler_bin.png" alt="ScreenShoot of bin folder" style="height: 100%; object-fit: contain;"/>
</div>

### Launch the resolution of a GEMS study

**Opening a terminal:**

- **Windows**: Press `Win + R`, type `cmd` or `powershell`, and press Enter
- **Linux**: Press `Ctrl + Alt + T` or search for "Terminal" in your applications menu

#### Antares Modeler

**Run Antares Modeler:**

In the parent directory of `rte-antares-9.3.2-installer-64bits/` (or the extracted folder).
```bash
# Windows
rte-antares-9.3.2-installer-64bits\bin\antares-modeler.exe <path-to-study>

# Linux
./rte-antares-9.3.2-installer-64bits/bin/antares-modeler <path-to-study>
```

**Test the installation:**

Let’s check if Modeler is installed correctly.

1. **Download the example study:**

   Download the [first Quick Start Example (QSE_1_Adequacy)](https://github.com/AntaresSimulatorTeam/GEMS/tree/documentation/get_started_quick_examples/doc/5_Examples/QSE/QSE_1_Adequacy) and save the "QSE_1_Adequacy" folder.

2. **Place the folder:**

   Move the "QSE_1_Adequacy" folder into your `rte-antares-9.3.2-installer-64bits` directory.

3. **Run the test:**

   Open a command line in the parent folder of "QSE_1_Adequacy" and run:

   ```bash
   # On Windows:
   .\bin\antares-modeler.exe .\QSE_1_Adequacy
   (Press Enter)

   # On Linux:
   ./bin/antares-modeler <path-to-study> QSE_1_Adequacy/
   (Press Enter)
   ```

4. **Check for success:**

   If you see logs like these, your installation is complete !
   
   Especially, `[yyyy-mm-dd HH:MM:SS][modeler][infos] Simulation table is written in: QSE_1_Adequacy/output/simulation_table--yyyymmdd HHMMSS.csv
`

   ![Modeler installation logs](../../assets/2_Modeler_logs.png)


#### Antares Solver

**Run Antares Solver:**
```bash
# Windows
rte-antares-9.3.2-installer-64bits\bin\antares-solver.exe <path-to-study>

# Linux
./rte-antares-9.3.2-installer-64bits/bin/antares-solver  <path-to-study>
```

Replace `<path-to-study>` with the path to your Antares study directory.

## Requirements

The complete installation, documentation is available on the [official documentation website](https://antares-simulator.readthedocs.io/en/latest/user-guide/02-install/).

In addition, Antares Modeler requires inside, the study folder, a `parameters.yml` file to run a GEMS study , and the process for creating this file is detailed in [this section](../3_User%20Guide/2_inputs.md). Unlike the GEMSPy interpreter, Modeler depends on this configuration file.


## Additional Resources

| Resource                | Link                                                                 |
|-------------------------|----------------------------------------------------------------------|
| Antares Simulator GitHub | [Antares Simulator on GitHub](https://github.com/AntaresSimulatorTeam/Antares_Simulator) |
| Online Documentation     | [Antares Simulator Docs](https://antares-simulator.readthedocs.io/en/latest/) |
| Modeler Documentation    | [GEMS Modeler Docs](https://antares-simulator.readthedocs.io/en/latest/user-guide/modeler/01-overview-modeler/) |
| Examples                 | See the repository's `examples/` directory                           |
| FAQ                      | [FAQ](../../6_Support%20&%20Contributing/1_faq.md)                   |
| GitHub Issues            | [Antares Simulator Issues](https://github.com/AntaresSimulatorTeam/Antares_Simulator/issues) |
| Contact Support          | [Contact support](../../6_Support%20&%20Contributing/2_contact.md)   |

---

**Navigation**

<div style="display: flex; justify-content: space-between;">
  <div style="text-align: left;">
  <button type="button" style="background-color:#CCCCCC; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
    <a href="../../1_Overview/References/4_Users" style="text-decoration:none; color: #000000">⬅️ Previous page</a>
  </button>
  </div>
  <button type="button" style="background-color:#AAAAFF; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
    <a href="../../../.." style="text-decoration:none; color: #FFFFFF">Index</a>
  </button>
  <div style="text-align: right;">
  <button type="button" style="background-color:#CCCCCC; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
    <a href="../1B_gemspy_installation" style="text-decoration:none; color: #000000">Next page ➡️</a>
  </button>
  </div>
</div>

---


© GEMS (LICENSE)