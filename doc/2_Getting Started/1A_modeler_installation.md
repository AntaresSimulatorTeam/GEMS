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

**Antares Modeler** is currently a command-line–only tool with no graphical interface yet. It is able to [tackle an **hybrid** study](../3_User%20Guide/3_hybrid%20inputs.md) (made from legacy and GEMS models).

<div style="height: 200px; overflow: hidden;">
  <img src="../../assets/2_Modeler_bin.png" alt="ScreenShoot of bin folder" style="height: 100%; object-fit: contain;"/>
</div>

### Command-Line Usage Examples

**Opening a terminal:**

- **Windows**: Press `Win + R`, type `cmd` or `powershell`, and press Enter
- **Linux**: Press `Ctrl + Alt + T` or search for "Terminal" in your applications menu

**Run Antares Modeler:**

Assuming you are in the parent directory of `rte-antares-9.3.2-installer-64bits/` (or the extracted folder).
```bash
# Windows
rte-antares-9.3.2-installer-64bits\bin\antares-9.3-modeler.exe <path-to-study>

# Linux
./rte-antares-9.3.2-installer-64bits/bin/antares-9.3-modeler <path-to-study>
```

**Run Antares Solver:**
```bash
# Windows
rte-antares-9.3.2-installer-64bits\bin\antares-9.3-solver.exe -i <path-to-study>

# Linux
./rte-antares-9.3.2-installer-64bits/bin/antares-9.3-solver -i <path-to-study>
```

Replace `<path-to-study>` with the path to your Antares study directory.

## Requirements

The **Antares Modeler** is designed to function within the Antares Simulator ecosystem. Therefore, it is necessary to **install Antares Simulator**.

The complete installation, documentation is available on the [official documentation website](https://antares-simulator.readthedocs.io/en/latest/user-guide/02-install/).

In addition, Antares Modeler requires a `parameters.yml` file to run a GEMS study. , and the process for creating this file is detailed in [this section](../3_User%20Guide/2_inputs.md). Unlike the GEMSPy interpreter, Modeler depends on this configuration file.


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