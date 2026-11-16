# How to run a PyPSA-Eur study with GEMS

This tutorial runs a [PyPSA-Eur](https://github.com/PyPSA/pypsa-eur) study with GEMS. [PyPSA-Eur](https://github.com/PyPSA/pypsa-eur) is an open-source energy system model of the European power grid. It is written in PyPSA format, which Antares Modeler cannot read directly. The [PyPSA-to-GEMS-Converter](https://github.com/AntaresSimulatorTeam/PyPSA-to-GEMS-Converter) package converts PyPSA studies into GEMS studies.

## Locally

The conversion workflow can be run locally :

[Download the jupyter notebook](https://github.com/AntaresSimulatorTeam/GEMS/blob/docs/refactor-pypsa-eur-notebook/doc/examples/notebooks/tutorial-two-pypsa-eur/tutorial_pypsa_eur_local.ipynb)

The notebook covers these steps:

1. **Get a PyPSA-Eur network** (France only, 3 days). By default it downloads a pre-generated copy. It can also rebuild the network with Pixi and Snakemake.
2. **Convert it to GEMS format** with [PyPSA-to-GEMS-Converter](https://github.com/AntaresSimulatorTeam/PyPSA-to-GEMS-Converter).
3. **Run the simulation** with [GemsPy](../installation/gemspy-installation.md).
4. **Analyse the results** and check them against the original PyPSA solution.

## On Google Colab

The whole workflow is also uploaded on Google Colab, so you can use it without installing anything:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1u1ZczyVc0d6D3DWWbFHfxqqgc9QJAIF0#scrollTo=colab-title)