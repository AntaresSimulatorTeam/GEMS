<div style="display: flex; justify-content: flex-end;">
  <a href="../../../..">
    <img src="../../../assets/gemsV2.png" alt="GEMS Logo" width="150"/>
  </a>
</div>

# How to run a PyPSA-Eur study on a server with GEMS

## Requirements

- A remote Linux server with Docker and Docker Compose installed
- [VS Code](https://code.visualstudio.com/) with the [Remote - SSH](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-ssh) extension installed locally

The configuration of the VS Code Remote SSH linked to remote server running Jupyter docker image is detailed in this tutorial [VS Code Remote SSH + Jupyter tutorial](https://www.w3tutorials.net/blog/vscode-how-to-run-a-jupyter-notebook-in-a-docker-container-over-a-remote-server/).

## Part 1 — Clone the GEMS repository

These steps are run **on the remote server** (connect via SSH first).

The GEMS repository contains the Docker configuration and the Jupyter notebook needed for the conversion step.

```bash
git clone https://github.com/AntaresSimulatorTeam/GEMS.git
cd GEMS
```

## Part 2 — Set up and run PyPSA-Eur

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

??? info "Example config file with oly FR node"

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

```bash
pixi run snakemake -c all all -j 4
```

To resume after an interrupted run:

```bash
pixi run snakemake -c all all -j 4 --rerun-incomplete
```

## Part 3 — Clone the PyPSA-to-GEMS Converter

These steps are run **on the remote server**.

We clone the converter which will transform the solved PyPSA-Eur network into a GEMS-compatible study through the Jupyter notebook. You can get more details on this conversion in this [tutorial](../../interoperability/pypsa-to-gems-converter/step-by-step-guide.md).

```bash
# Clone inside the Tutorial_2_PyPSA_eur/ directory so Docker can pick it up
cd doc/2_Getting_Started/Tutorial_2_PyPSA_eur
git clone https://github.com/AntaresSimulatorTeam/PyPSA-to-GEMS-Converter
```

## Part 4 — Build docker image and Open the Jupyter notebook via Remote SSH

We have all what is needed by the docker image :
- PyPSA Eur data
- GEMS repo with the jupyer notebook and docker configuration
- PyPSA to GEMS converter repo

We can create now the docker image inside the server :

1. In VS Code, open the **Command Palette** (`Ctrl+Shift+P`) and select **Remote-SSH: Connect to Host**.
2. Access to ```/home/ubuntu/GEMS/doc/2_Getting_Started/Tutorial_2_PyPSA_eur/``` 
3. Start the container by the command

    ```bash
    cd docker-pypsa-gemsv2
    docker compose up --build
    ```

    Docker Compose will build the image from `docker-pypsa-gemsv2/Dockerfile_PyPSA` using `Tutorial_2_PyPSA_eur/` as the build context and start the container. The Jupyter notebook will be exposed on port **8889**.

3. Open your browser at `http://localhost:8889`.
4. Open `2_Tutorial_PyPSA_eur.ipynb` and run the cells in order to:
