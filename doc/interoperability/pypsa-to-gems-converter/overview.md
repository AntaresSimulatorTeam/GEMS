---
description: Overview of the PyPSA-to-GEMS Converter — an open-source Python package that exports PyPSA networks as GEMS study folders, supporting linear OPF and stochastic optimisation.
---

<div style="display: flex; justify-content: flex-end;">
  <a href="../..">
    <img src="../../../assets/gemsV2.png" alt="GEMS Logo" width="150"/>
  </a>
</div>
<div>
<h1>About</h1>
<p>The <a href="https://pypsa.org/">PyPSA</a>-to-<a href="https://gems-energy.readthedocs.io/en/latest/">GEMS</a> Converter is an open-source &amp; standalone python package that enables the conversion of studies conducted in PyPSA into the GEMS format: it exports a <a href="https://docs.pypsa.org/latest/api/networks/network/">PyPSA Network</a> as a <a href="https://gems-energy.readthedocs.io/en/latest/user-guide/file-structure/overview/">GEMS</a> folder.</p>
<p>This converter is based on the representation of the PyPSA models of components as a GEMS library of models: <a href="https://github.com/AntaresSimulatorTeam/GEMS/blob/main/libraries/pypsa_models.yml">pypsa_models.yml</a>.</p>

<h3>Key Features</h3>
<ul>
  <li><strong>Conversion of linear optimal power flow &amp; economical dispatch studies</strong></li>
  <li><strong>Conversion of two-stage stochastic optimization studies</strong></li>
</ul>
</div>

<h2>Table of Contents</h2>
<ul>
  <li><a href="../how-the-converter-works/">How the Converter Works</a></li>
  <li><a href="../input-and-output/">Input and Output of the Converter</a></li>
  <li><a href="../current-limitations/">Current Limitations of the Converter</a></li>
  <li><a href="../step-by-step-guide/">Step-by-Step Guide: Manually Executing a Simulation in GEMS Modeler</a></li>
  <li><a href="../comparing-results/">Comparing Results Between GEMS Modeler and PyPSA</a></li>
</ul>