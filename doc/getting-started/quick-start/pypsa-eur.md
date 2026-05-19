<div style="display: flex; justify-content: flex-end;">
  <a href="../../../..">
    <img src="../../../assets/gemsV2.png" alt="GEMS Logo" width="150"/>
  </a>
</div>

# How to run a PyPSA-Eur study on a server with GEMS

This tutorial walks through the full workflow for running a PyPSA-Eur sector-coupled network study and converting its outputs into a GEMS study that can be solved with Antares Modeler — all inside a Docker container accessible via a remote Jupyter notebook.

## Prerequisites

- A remote Linux server with Docker and Docker Compose installed
- [VS Code](https://code.visualstudio.com/) with the [Remote - SSH](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-ssh) extension installed locally

For a full guide on configuring VS Code Remote SSH with Jupyter, see the [VS Code Remote SSH + Jupyter tutorial](https://www.w3tutorials.net/blog/vscode-how-to-run-a-jupyter-notebook-in-a-docker-container-over-a-remote-server/).

---

## Part 1 — Set up and run PyPSA-Eur

These steps are run **on the remote server** (connect via SSH first).

### 1.1 Install Pixi

[Pixi](https://pixi.sh) is the package manager used by PyPSA-Eur.

```bash
curl -fsSL https://pixi.sh/install.sh | bash
source ~/.bashrc  # or restart the terminal
```

### 1.2 Clone PyPSA-Eur

```bash
git clone https://github.com/PyPSA/pypsa-eur.git
cd pypsa-eur
```

### 1.3 Install the environment

```bash
pixi install
```

This reads `pixi.toml` and installs all dependencies into `.pixi/envs/default/`. The first run takes a few minutes.

### 1.4 Configure the study

```bash
cp config/config.default.yaml config/config.yaml
```

Edit `config/config.yaml` to set the target countries, number of clusters, planning horizon, and other study parameters.

### 1.5 Run the workflow

```bash
pixi run snakemake -c all all -j 4
```

To resume after an interrupted run:

```bash
pixi run snakemake -c all all -j 4 --rerun-incomplete
```

---

## Part 2 — Clone the GEMS repository

The GEMS repository contains the Docker configuration and the pre-built Jupyter notebook needed for the conversion step.

```bash
git clone https://github.com/AntaresSimulatorTeam/GEMS.git
cd GEMS
```

---

## Part 3 — Clone the PyPSA-to-GEMS Converter

The converter transforms the solved PyPSA-Eur network into a GEMS-compatible study.

```bash
# Clone inside the Tutorial_2_PyPSA_eur/ directory so Docker can pick it up
cd doc/2_Getting_Started/Tutorial_2_PyPSA_eur
git clone https://github.com/AntaresSimulatorTeam/PyPSA-to-GEMS-Converter
```

---

## Part 4 — Build and run the Docker image

The Docker image bundles the converter, Antares Modeler, and Jupyter in a single container.

### 4.1 Place the PyPSA-Eur output resources

The container expects the PyPSA-Eur `resources/` directory to be available at:

```text
doc/2_Getting_Started/Tutorial_2_PyPSA_eur/pypsa-eur/resources/
```

Copy or symlink your PyPSA-Eur run directory there:

```bash
# From GEMS/doc/2_Getting_Started/Tutorial_2_PyPSA_eur/
ln -s /path/to/your/pypsa-eur pypsa-eur
```

### 4.2 Start the container

```bash
cd docker-pypsa-gemsv2
docker compose up --build
```

Docker Compose will:

1. Build the image from `docker-pypsa-gemsv2/Dockerfile_PyPSA` using `Tutorial_2_PyPSA_eur/` as the build context.
2. Start the container, exposing Jupyter on port **8889**.
3. Mount `pypsa-eur/resources/` as read-only inside the container so the notebook can read your results.

The relevant `docker-compose.yml` (`doc/2_Getting_Started/Tutorial_2_PyPSA_eur/docker-pypsa-gemsv2/docker-compose.yml`):

```yaml
services:
  pypsa:
    build:
      context: ..
      dockerfile: docker-pypsa-gemsv2/Dockerfile_PyPSA
      network: host
    image: my-pypsa
    container_name: my-pypsa
    ports:
      - "8889:8889"
    volumes:
      - ../pypsa-eur/resources:/workspace/pypsa-eur/resources:ro
```

---

## Part 5 — Open the Jupyter notebook via Remote SSH

1. In VS Code, open the **Command Palette** (`Ctrl+Shift+P`) and select **Remote-SSH: Connect to Host**.
2. Forward port **8889** from the remote server to your local machine (VS Code does this automatically when connected).
3. Open your browser at `http://localhost:8889`.
4. Open `2_Tutorial_PyPSA_eur.ipynb` and run the cells in order to:
   - Load the solved PyPSA-Eur network.
   - Convert it to a GEMS study.
   - Run Antares Modeler.
   - Analyse the results.

<div style="background-color:#fff3cd;border-left:5px solid #ffc107;padding:12px 16px;border-radius:4px;margin:16px 0;">
  <strong>⚠️ Note</strong><br>
  The notebook connects to Antares Modeler via the <code>antares-modeler</code> binary that is pre-installed inside the container (Antares Simulator v10.1.0). No local installation is required.
</div>

---

## Converter and interoperability reference

For a detailed explanation of how the PyPSA-to-GEMS Converter works, its inputs, outputs, and current limitations, see the [PyPSA to GEMS Converter](../../interoperability/pypsa-to-gems-converter/overview.md) section.
