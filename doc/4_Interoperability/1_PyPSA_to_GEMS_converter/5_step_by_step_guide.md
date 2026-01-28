<div style="display: flex; justify-content: space-between; align-items: center;">
  <div style="text-align: left;">
    <a href="../..">Main Section</a>
  </div>
  <div style="text-align: right;">
    <img src="../../../assets/gemsV2.png" alt="GEMS Logo" width="150"/>
  </div>
</div>
<div>
<h2>Step-by-Step Guide: Manually Executing a Simulation in GEMS Modeler</h2>

<ol>
<li><strong>Build or load a PyPSA network</strong>
```python
# Setup
logger = logging.getLogger(__name__)
study_dir = Path("tmp/my_study")  # Absolute path to the GEMS study directory

# Option A: build the network in code
network = Network()
network.add("Bus", "bus1", v_nom=1)
network.add("Load", "load1", bus="bus1", p_set=[10, 20, 30])
network.add("Generator", "gen1", bus="bus1", p_nom=100, marginal_cost=50)

# Option B: load the network from a file
network = Network("simple_network.nc")  # Absolute path to the PyPSA file
```
</li>

<li><strong>Convert the PyPSA network to a GEMS study</strong>
```python
# Convert PyPSA network to GEMS
converter = PyPSAStudyConverter(
    pypsa_network=network,
    logger=logger,
    study_dir=study_dir,
    series_file_format=".tsv",  # Supported formats: .tsv, .csv, tsv, csv
).to_gems_study()
```
</li>

<li><strong>Run the GEMS(Antares) optimization</strong>
```python
# Path to the Antares modeler binary
modeler_bin = Path("antares-9.3.5-Ubuntu-22.04/bin/antares-modeler")

# Run the optimization
subprocess.run([
    str(modeler_bin),
    str(study_dir / "systems")
])
```
</li>
</ol>
</div>

---
**Navigation**
<div style="display: flex; justify-content: space-between;">
  <div style="text-align: left;">
  <button type="button" style="background-color:#CCCCCC; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
    <a href="../4_current_limitations/" style="text-decoration:none; color: #000000">⬅️ Previous page</a>
  </button>
  </div>
  <button type="button" style="background-color:#AAAAFF; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
    <a href="Home/Main_Home/1_context_GEMS.md" style="text-decoration:none; color: #FFFFFF">Home</a>
  </button>
  <div style="text-align: right;">
  <button type="button" style="background-color:#CCCCCC; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
    <a href="../6_comparing_results/" style="text-decoration:none; color: #000000">Next page ➡️</a>
  </button>
  </div>
</div>

---
