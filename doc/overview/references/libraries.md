<div style="display: flex; justify-content: flex-end;">
  <a href="../../..">
    <img src="../../../assets/gemsV2.png" alt="GEMS Logo" width="150"/>
  </a>
</div>

# Reference libraries of models

The following table lists reference model libraries developed within projects that make use of the GEMS modelling framework.

| Library Name         | Description                  | Link                                                      |
|----------------------|------------------------------|-----------------------------------------------------------|
| Basic Models Library  | Basic library for newcomers  | [basic-models-library.yml](https://github.com/AntaresSimulatorTeam/GEMS/blob/main/libraries/basic_models_library.yml) |
| Andromede Models | Library of models from RTE's Andromede project         | [andromede_models.yml](https://github.com/AntaresSimulatorTeam/GEMS/blob/main/libraries/andromede_models.yml)  |
|Antares Legacy Models|Library of models of the legacy [Antares Simulator](https://antares-simulator.readthedocs.io/en/latest/user-guide/03-getting_started/)|[antares_legacy_models.yml](https://github.com/AntaresSimulatorTeam/GEMS/blob/main/libraries/antares_legacy_models.yml)|
|PyPSA Models|Library of models available on [PyPSA](https://docs.pypsa.org/latest/home/installation/)|[pypsa_models.yml](https://github.com/AntaresSimulatorTeam/GEMS/blob/main/libraries/pypsa_models.yml)|


To verify that a downloaded library file matches the official release, see
[Verifying GEMS Libraries](verifying-libraries.md).

## Library Viewer

Explore how each library is written by navigating in the next interactive window. Click on its different elements for getting a good overview of its structure.

*As the visualization is automatically updated with the newest libraries' version, the loading can last a few seconds*

<!--
  The JSON files are generated before each build by doc/hooks/yaml_to_json.py. 
  They are not commited on the repo through gitignore.
-->
<div class="yaml-loader-container" id="yaml-loader-main" data-yaml-url="../../../assets/data/basic_models_library.json" data-library-name="Basic Models Library">
  <div class="yaml-library-selector">
    <button class="yaml-library-nav-btn" data-url="../../../assets/data/basic_models_library.json" data-name="Basic Models Library">Basic Models Library</button>
    <button class="yaml-library-nav-btn" data-url="../../../assets/data/andromede_models.json" data-name="Andromede Models">Andromede Models</button>
    <button class="yaml-library-nav-btn" data-url="../../../assets/data/antares_legacy_models.json" data-name="Antares Legacy Models">Antares Legacy Models</button>
    <button class="yaml-library-nav-btn" data-url="../../../assets/data/pypsa_models.json" data-name="PyPSA Models">PyPSA Models</button>
  </div>
</div>