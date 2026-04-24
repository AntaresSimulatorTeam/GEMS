---
description: Current limitations of the PyPSA-to-GEMS Converter — known restrictions in component support and conversion scope for the current release.
tags:
  - Interoperability
  - PyPSA
---

<div style="display: flex; justify-content: flex-end;">
  <a href="../..">
    <img src="../../../assets/gemsV2.png" alt="GEMS Logo" width="150"/>
  </a>
</div>
<div>
<h1>Current Limitations of the Converter</h1>
<p>We explicit here the <strong>current</strong> limitation of the PyPSA-to-GEMS converter, that are related to the current state of development of the converter. We foresee no limitations in terms of the expressiveness of the GEMS modelling language.</p>

<h2>Unsupported PyPSA Components</h2>
<ul>
  <li>Lines (not implemented)</li>
  <li>Transformers (not implemented)</li>
</ul>

<h2>Component Restrictions</h2>

<h3>Generators</h3>
<ul>
  <li><strong><code>active = 1</code></strong> — All generators are included in the optimization.</li>
  <li><strong><code>marginal_cost_quadratic = 0</code></strong> — Only linear generation costs are supported.</li>
  <li><strong><code>committable = False</code></strong> — Unit commitment (on/off decisions) is not supported.</li>
</ul>

<h3>Loads</h3>
<ul>
  <li><strong><code>active = 1</code></strong> — All loads are fixed and always active.</li>
</ul>

<h3>Links</h3>
<ul>
  <li><strong><code>active = 1</code></strong> — All links are always active.</li>
</ul>

<h3>Storage Units</h3>
<ul>
  <li><strong><code>active = 1</code></strong> — All storage units are included in the optimization.</li>
  <li><strong><code>sign = 1</code></strong> — Storage operates with positive dispatch direction.</li>
  <li><strong><code>cyclic_state_of_charge = 1</code></strong> — End state of charge must equal the initial state.</li>
  <li><strong><code>marginal_cost_quadratic = 0</code></strong> — Only linear storage costs are supported.</li>
</ul>

<h3>Stores</h3>
<ul>
  <li><strong><code>active = 1</code></strong> — All stores are included in the optimization.</li>
  <li><strong><code>sign = 1</code></strong> — Store energy flows are positive.</li>
  <li><strong><code>e_cyclic = 1</code></strong> — End energy level must equal the initial level.</li>
  <li><strong><code>marginal_cost_quadratic = 0</code></strong> — Only linear storage costs are supported.</li>
</ul>

<h3>Global Constraints</h3>
<ul>
  <li><strong><code>type = primary_energy</code></strong> — Only primary energy constraints are supported.</li>
  <li><strong><code>carrier.co2_emissions</code></strong> — CO₂ accounting must be defined at the carrier level.</li>
  <li><strong>Supported senses:</strong> <code>&lt;=</code>, <code>==</code></li>
</ul>
</div>