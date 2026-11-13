# PyPSA -> GEMS -> GemsPy (no Antares)
# Run with the .venv Python: ..\.venv\Scripts\python.exe new_tuto_gemspypsa.py

# %% 0. Build the PyPSA-Eur network (France, 1 node, 48 h) with Pixi + Snakemake
# See https://gems-energy.readthedocs.io/en/latest/getting-started/quick-start/pypsa-eur/
# Skipped if the network already exists. First run: installation + ~10 min of downloads.
import os
import shutil
import subprocess
from pathlib import Path
import platform

if "__file__" in globals():  # paths relative to the script folder, wherever it is launched from
    os.chdir(Path(__file__).resolve().parent)

# PyPSA-Eur in a SHORT path: Windows limits paths to 260 characters and Snakemake
# creates files with very long names in .snakemake/ -> failure in a deeply nested folder.
pypsa_eur_dir = Path.home() / "pypsa-eur"  # C:\Users\<user>\pypsa-eur
pypsa_eur_file = pypsa_eur_dir / "resources/networks/base_s_1_elec.nc"
# Pre-generated copy shipped with the tutorial, in case the workflow below fails
backup_file = Path("pypsa-eur/resources/networks/base_s_1_elec.nc").resolve()

PYPSA_EUR_CONFIG = """\
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
"""

if not pypsa_eur_file.is_file():
    try:
        # 0.1 Install Pixi (PyPSA-Eur package manager)
        pixi = shutil.which("pixi") or str(Path.home() / ".pixi/bin/pixi.exe")
        if not Path(pixi).is_file():
            if platform.system() == "Windows":
                subprocess.run(["powershell", "-ExecutionPolicy", "ByPass", "-c",
                            "irm -useb https://pixi.sh/install.ps1 | iex"], check=True)
            elif platform.system() == "Linux":
                subprocess.run(["bash", "-c",
                            "curl -sSL https://pixi.sh/install.sh | bash"], check=True)
            else:
                raise OSError(f"Pixi installation not implemented for {platform.system()}")
        print(f"Pixi installed: {pixi}")

        # 0.2 Clone PyPSA-Eur v2026.08.0: last release that still produces base_s_{clusters}_elec.nc
        #     (from v2026.09.0 on, networks are named networks/clustered.nc / composed_{horizon}.nc)
        if not pypsa_eur_dir.is_dir():
            subprocess.run(["git", "clone", "--branch", "v2026.08.0", "--depth", "1",
                            "https://github.com/PyPSA/pypsa-eur.git", str(pypsa_eur_dir)], check=True)
        print(f"PyPSA-Eur cloned: {pypsa_eur_dir}")

        # 0.3 Install the environment (reads pixi.toml -> .pixi/envs/default/)
        subprocess.run([pixi, "install"], cwd=pypsa_eur_dir, check=True)
        print(f"Environment installed: {pypsa_eur_dir}")

        # 0.4 Configure the study (FR, 1 cluster, 48 h); automatically merged with config.default.yaml
        (pypsa_eur_dir / "config/config.yaml").write_text(PYPSA_EUR_CONFIG, encoding="utf-8")
        print(f"PyPSA-Eur configured: {pypsa_eur_dir / 'config/config.yaml'}")

        # 0.5 Run the workflow only up to base_s_1_elec.nc
        #     (no sector coupling, no solving; --rerun-incomplete resumes after an interruption)
        subprocess.run([pixi, "run", "snakemake", "-c", "all", "-j", "4", "--rerun-incomplete",
                        pypsa_eur_file.relative_to(pypsa_eur_dir).as_posix()],
                       cwd=pypsa_eur_dir, check=True)
        print(f"PyPSA-Eur generated: {pypsa_eur_file}")
        
    except (subprocess.CalledProcessError, OSError) as err:
        print(f"PyPSA-Eur generation failed: {err}")

# %% 1. Load the PyPSA network
import sys
import types
import warnings
import pandas as pd
import matplotlib.pyplot as plt
import pypsa

warnings.filterwarnings("ignore")

if not pypsa_eur_file.is_file():
    raise FileNotFoundError(
        f"\n\nThe PyPSA-Eur network was not generated:\n  {pypsa_eur_file}\n\n"
        f"A pre-generated copy is provided with this tutorial:\n  {backup_file}\n\n"
        f"Copy it to the location above, then re-run this cell."
    )
network = pypsa.Network(str(pypsa_eur_file))
print(f"PyPSA-Eur network loaded: {pypsa_eur_file}")

# %% 2. Conversion to a GEMS study
# The converter imports antares.craft but does not need it for GEMS: dummy module + hybrid study disabled.
sys.modules.setdefault("antares", types.ModuleType("antares"))
sys.modules.setdefault("antares.craft", types.ModuleType("antares.craft"))
from src.pypsa_converter import PyPSAStudyConverter  # pypsa-to-gems-converter package (module name "src")

PyPSAStudyConverter._write_antares_hybrid_study = lambda self: None

study_dir = Path("tmp/my_study").resolve()
shutil.rmtree(study_dir, ignore_errors=True)
PyPSAStudyConverter(network, study_dir, series_file_format=".tsv", solver_name="coin").to_gems_study()

# %% 3. Solve with GemsPy
from gems_craft.study.folder import load_study
from gems_craft.optim_config.parsing import OptimConfig, TimeScopeConfig, ScenarioScopeConfig
from gems_runner.session.session import SimulationSession

optim_config = OptimConfig(
    time_scope=TimeScopeConfig(first_time_step=0, last_time_step=len(network.snapshots) - 1),
    scenario_scope=ScenarioScopeConfig(include=[0]),
)
result = SimulationSession(study=load_study(study_dir / "systems"), optim_config=optim_config).run()
df = result.data


# %% 4. Comparison with PyPSA
obj = float(df.loc[df["output"] == "objective-value", "value"].iloc[0])
print(f"GEMS total cost  : {obj:,.0f} €")

network.optimize(solver_name="highs")
# PyPSA keeps the fixed cost of existing non-extendable capacity apart (objective_constant); GEMS includes it.
pypsa_obj = network.objective + network.objective_constant
print(f"PyPSA total cost : {pypsa_obj:,.0f} €")
print(f"Relative gap     : {abs(obj - pypsa_obj) / pypsa_obj:.1e}")

# %% 5. Results plots
gen = df[df["component"].str.startswith("generator_", na=False)].copy()
gen["technology"] = gen["component"].str.split("_").str[-1]

obj = float(df.loc[df["output"] == "objective-value", "value"].iloc[0])
print(f"GEMS total cost  : {obj:,.0f} €")

capacity = gen[gen["output"] == "p_nom"].groupby("technology")["value"].sum()
dispatch = (gen[(gen["output"] == "p") & gen["absolute_time_index"].notna()]
            .assign(t=lambda d: pd.to_numeric(d["absolute_time_index"]))
            .pivot_table(index="t", columns="technology", values="value", aggfunc="sum")
            .clip(lower=0))

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
(capacity[capacity > 0] / 1e3).plot.barh(ax=axes[0], title="Installed capacity (GW)")
(dispatch / 1e3).plot.area(ax=axes[1], linewidth=0, title="Dispatch (GW)")
plt.tight_layout()
plt.show()
