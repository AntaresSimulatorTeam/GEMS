---
description: Step-by-step installation guide for Antares Simulator's GEMS interpreter (Antares Modeler) - download, extract, and configure the GEMS interpreter within Antares Simulator.
---

# Antares Simulator's GEMS interpreter

This section outlines the approach for configuring and utilizing the **Antares Modeler**, the interpreter for the **GEMS language** inside [Antares Simulator](https://github.com/AntaresSimulatorTeam/Antares_Simulator).

## Installation

The following link provides access to the most recent stable version of the [Antares Simulator](https://github.com/AntaresSimulatorTeam/Antares_Simulator/releases).

### Download and Extract

1. Go to the [**Antares Simulator releases page**](https://github.com/AntaresSimulatorTeam/Antares_Simulator/releases)

2. Download the appropriate archive for your platform:

    === "Windows"
        `rte-antares-<simulator-version>-installer-64bits.zip`

    === "Linux"
        `rte-antares-<simulator-version>-Ubuntu-<ubuntu-version>.tar.gz`

3. Extract the archive to your desired location:

    === "Windows"
        Right-click the archive and select "Extract All"

    === "Linux"
        ```bash
        tar -xzf rte-antares-<simulator-version>-Ubuntu-<ubuntu-version>.tar.gz
        ```

### Locate the Executables

After extraction, navigate to the `bin` folder inside the extracted directory. You will find:

- **Antares Modeler executable** (`antares-modeler` or `antares-modeler.exe`)
- **Antares Solver executable** (`antares-solver` or `antares-solver.exe`)

**Antares Modeler** is currently a command-line–only tool with no graphical interface yet. It is used for launching studies with full GEMS syntax.
**Antares Solver** is designed for running Antares legacy study and hybrid studies comprising a mix of legacy and Gems models.

```txt
cmake\
pkgconfig\
antares-batchrun.exe
antares-config.exe
antares-modeler         # GEMS studies
antares-solver          # hybrid and legacy studies
antares-study-finder
```

### Launch the resolution of a GEMS study

**Opening a terminal:**

=== "Windows"
    Press `Win + R`, type `cmd` or `powershell`, and press Enter

=== "Linux"
    Press `Ctrl + Alt + T` or search for "Terminal" in your applications menu

#### Antares Modeler

**First study simulation with Modeler:**

Let’s check if Modeler is working correctly.

- **Download the example study:**

    Download the [first Quick Start Example (QSE_1_Adequacy)](https://github.com/AntaresSimulatorTeam/GEMS/tree/main/resources/Documentation_Examples/QSE/QSE_1_Adequacy) and save the "QSE_1_Adequacy" folder.

- **Run simulation:**

    === "Windows"
        ```bash
        .\bin\antares-modeler.exe .\<absolute path to QSE_1_Adequacy study folder>
        ```

    === "Linux"
        ```bash
        ./bin/antares-modeler ./<absolute path to QSE_1_Adequacy study folder>
        ```

- **Check for success:**

    If you see logs like these, Modeler works correctly !

    Especially, `[yyyy-mm-dd HH:MM:SS][modeler][infos] Simulation table of scenario 0 is written in: QSE_1_Adequacy/output/yyyymmdd-HHMM/simulation-table-0.csv`

    ```txt
    [2026-10-13 17:12:01][modeler][infos] Study path: QSE_1_Adequacy/
    [2026-10-13 17:12:01][modeler][infos] Output folder : QSE_1_Adequacy/output/20261013-1712
    [2026-10-13 17:12:01][modeler][infos] Parameters loaded
    [2026-10-13 17:12:01][modeler][infos] Loading modeler files...
    [2026-10-13 17:12:01][modeler][infos] Library loaded: basic_models_library
    [2026-10-13 17:12:01][modeler][infos] Libraries loaded
    [2026-10-13 17:12:01][modeler][infos] System loaded
    [2026-10-13 17:12:01][modeler][warns] Data-series could not be loaded: Not a directory: QSE_1_Adequacy/input/data-series
    [2026-10-13 17:12:01][modeler][infos] Timeseries loaded
    [2026-10-13 17:12:01][modeler][infos] No scenario builder found, skipping scenario groups loading.
    [2026-10-13 17:12:01][modeler][infos] Scenario groups loaded
    [2026-10-13 17:12:01][modeler][infos] Modeler loaded in 0.004 s
    [2026-10-13 17:12:01][modeler][infos] Locations validity OK
    [2026-10-13 17:12:01][modeler][infos] Number of Monte-Carlo scenarios to simulate: 1
    [2026-10-13 17:12:01][modeler][infos] Number of variables: 18
    [2026-10-13 17:12:01][modeler][infos] Number of constraints: 6
    [2026-10-13 17:12:01][modeler][infos] Solving scenario 0
    [2026-10-13 17:12:01][modeler][infos] Launching resolution...
    [2026-10-13 17:12:01][modeler][infos] Solved in 0.000 s
    [2026-10-13 17:12:01][modeler][infos] Simulation Table is generated in 0 ms
    [2026-10-13 17:12:01][modeler][infos] Simulation table of scenario 0 is written in: QSE_1_Adequacy/output/20261013-1712/simulation-table-0.csv
    ```

    !!! info "`optim-config.yml` is required"
        Antares Modeler (from v10.2.0) stops with the error `Missing 'optim-config.yml'` if the study has no
        [`input/optim-config.yml`](../../user-guide/input-files/optimization-configuration.md) file. The example
        studies already include one.

### Launch the resolution of an Hybrid study

#### Antares Solver

- Use the Hybrid Study tutorial :

  Refer to the tutorial inside the [Interoperability - Antares Hybrid Mode](../../interoperability/hybrid/overview.md) section

- Run the following commands:

    === "Windows"
        ```bash
        rte-antares-x.x.x-installer-64bits\bin\antares-solver.exe <path-to-study> --output all
        ```

    === "Linux"
        ```bash
        ./rte-antares-x.x.x-installer-64bits/bin/antares-solver <path-to-study> --output all
        ```

Replace `<path-to-study>` with the path to your Antares study directory. The `--output all` option writes the [simulation tables](../../user-guide/outputs/simulation-table.md) of the GEMS components in addition to the Legacy outputs: without it, Antares Solver writes the Legacy outputs only.

## Requirements

The complete installation, documentation is available on the [official documentation website](https://antares-simulator.readthedocs.io/en/latest/reference/installation/).

In addition, Antares Modeler requires inside, the study folder, a `parameters.yml` file to run a GEMS study, and the process for creating this file is detailed in [this section](../../user-guide/input-files/solver-optimization.md). Unlike the [GemsPy interpreter](gemspy-installation.md), Modeler depends on this configuration file. Modeler also requires an [`input/optim-config.yml`](../../user-guide/input-files/optimization-configuration.md) file, which may only declare `models: []`.

## Additional Resources

| Resource                | Link                                                                 |
|-------------------------|----------------------------------------------------------------------|
| Antares Simulator GitHub | [Antares Simulator on GitHub](https://github.com/AntaresSimulatorTeam/Antares_Simulator) |
| Online Documentation     | [Antares Simulator Docs](https://antares-simulator.readthedocs.io/en/latest/) |
| Modeler Documentation    | [GEMS Modeler Docs](https://antares-simulator.readthedocs.io/en/latest/reference/modeler/01-overview-modeler/) |
| Examples                 | See the repository's `examples/` directory                           |
| FAQ                      | [FAQ](../../support/faq.md)                   |
| GitHub Issues            | [Antares Simulator Issues](https://github.com/AntaresSimulatorTeam/Antares_Simulator/issues) |
| Contact Support          | [Contact support](../../support/contact.md)   |