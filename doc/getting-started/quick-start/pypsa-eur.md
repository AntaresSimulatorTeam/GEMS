# How to run a PyPSA-Eur study on a server with GEMS

This tutorial is a workflow to run a [PyPSA-Eur](https://github.com/PyPSA/pypsa-eur) study on a remote Linux server using GEMS. [PyPSA-Eur](https://github.com/PyPSA/pypsa-eur) is an open-source energy system model covering the European power grid coded in PyPSA format whose native format is not compatible with Antares Modeler. The package [PyPSA-to-GEMS-Converter](https://github.com/AntaresSimulatorTeam/PyPSA-to-GEMS-Converter) converts PyPSA format studies into GEMS readable studies.

1. **Configure a simple PyPSA-Eur study** with minimal settings (one area only, 3 days), download the data.
2. **Convert to GEMS format** using the Python package [PyPSA-to-GEMS-Converter](https://github.com/AntaresSimulatorTeam/PyPSA-to-GEMS-Converter) inside a Jupyter notebook.
3. **Run the simulation** with [GemsPy](../installation/gemspy-installation.md) from within the same notebook.

The Jupyter notebook runs in a Python virtual environment on the remote server and is accessed locally via VS Code Remote SSH.

## Requirements

- A remote Linux server with Python 3.11 or later installed
- [VS Code](https://code.visualstudio.com/) with the [Remote - SSH](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-ssh) extension installed locally

## Part 1 - Clone the GEMS repository

These steps are run **on the remote server** (connect via SSH first).

The GEMS repository contains the Jupyter notebook needed for the conversion step and run the GEMS simulation of the converted study.

```bash
git clone https://github.com/AntaresSimulatorTeam/GEMS.git
cd GEMS
```

## Part 2 - Set up and run PyPSA-Eur

These steps are run **on the remote server**.

This part focuses on setting up a simple PyPSA-Eur study (France only, 3 days) on the server.

### 2.1 Install Pixi

[Pixi](https://pixi.sh) is the package manager used by PyPSA-Eur.

```bash
curl -fsSL https://pixi.sh/install.sh | bash
source ~/.bashrc  # or restart the terminal
```

### 2.2 Clone PyPSA-Eur

```bash
git clone https://github.com/PyPSA/pypsa-eur.git
cd pypsa-eur
```

### 2.3 Install the environment

```bash
pixi install
```

This reads `pixi.toml` and installs all dependencies into `.pixi/envs/default/`. The first run takes a few minutes.

### 2.4 Configure the study

This part is important because it determines the amount of data downloaded from PyPSA-Eur open data. In this example, to create a small study easy to convert, the study only contains the FR node and data for 3 days.

First, copy the default config:

```bash
cp config/config.default.yaml config/config.yaml
```

Then edit `config/config.yaml` to set the target countries, number of clusters, planning horizon, and other study parameters.

??? info "Example config file with only FR node"

    ```yaml
    # PyPSA-Eur: simple one-year electricity study (runs on a normal PC)
    #
    # Use with:  snakemake -call solve_elec_networks --configfile config/config.regional.yaml -j 2
    # Resume after crash:  add  --rerun-incomplete
    benchmark:
      enabled: false

    countries:
      - FR

    scenario:
      clusters: [1]
      opts: [""]
      sector_opts: [""]
      planning_horizons: [2050]

    snapshots:
      start: "2013-01-01"
      end: "2013-01-03"
      inclusive: left

    solving:
      solver:
        name: highs
        options: "highs-default"
      mem_mb: 10000

    atlite:
      nprocesses: 2

    sector:
      hydrogen_underground_storage_locations:
        - onshore
      regional_co2_sequestration_potential:
        enable: false
      district_heating:
        supply_temperature_approximation:
          rolling_window_ambient_temperature: 48

    plotting:
      costs_threshold: 0.001
      energy_threshold: 0.1
    ```

### 2.5 Run the workflow

Now, we can download data from PyPSA-Eur.

!!! warning

    This download can last for 10 minutes for only one node.

```bash
pixi run snakemake -c all all -j 4
```

To resume after an interrupted run:

```bash
pixi run snakemake -c all all -j 4 --rerun-incomplete
```


## Part 3 - Install the Python environment and open the Jupyter notebook

We have everything needed to convert and run the study:

- PyPSA-Eur data
- GEMS repo with the Jupyter notebook

We can now create the Python environment on the server and open the notebook:

1. In VS Code, open the **Command Palette** (`Ctrl+Shift+P`) and select **Remote-SSH: Connect to Host**.
2. Access to ```/home/ubuntu/GEMS/doc/examples/notebooks/tutorial-two-pypsa-eur/```
3. Create a virtual environment and install the packages used by the notebook

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install jupyter matplotlib netcdf4 xarray pypsa pypsa-to-gems-converter==0.0.2 gemspy==0.3.0
    ```

4. Copy the network generated in Part 2 next to the notebook (a pre-generated copy is already shipped with the tutorial, so this step is optional)

    ```bash
    mkdir -p pypsa-eur/resources/networks
    cp /home/ubuntu/GEMS/pypsa-eur/resources/networks/base_s_1_elec.nc pypsa-eur/resources/networks/
    ```

5. Open `tutorial_pypsa_eur_gemspy.ipynb` in VS Code, select the `.venv` interpreter as kernel and run the cells in order to convert the PyPSA-Eur network into a GEMS study, run it with GemsPy and analyse the results.
