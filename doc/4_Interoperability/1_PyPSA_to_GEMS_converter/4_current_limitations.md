<div style="display: flex; justify-content: space-between; align-items: center;">
  <div style="text-align: left;">
    <a href="../..">Main Section</a>
  </div>
  <div style="text-align: right;">
    <img src="../../../assets/gemsV2.png" alt="GEMS Logo" width="150"/>
  </div>
</div>
<div>
<h2>Current Limitations of the Converter</h2>
<p>We explicit here the <strong>current</strong> limitation of the PyPSA-to-GEMS converter, that are related to the current state of development of the converter. We foresee no limitations in terms of the expressiveness of the GEMS modelling language.</p>

<h3>Unsupported PyPSA Components</h3>
<ul>
  <li>Lines (not implemented)</li>
  <li>Transformers (not implemented)</li>
</ul>

<h3>Component Restrictions</h3>

<h4>Generators</h4>
<ul>
  <li><strong><code>active = 1</code></strong> — All generators are included in the optimization.</li>
  <li><strong><code>marginal_cost_quadratic = 0</code></strong> — Only linear generation costs are supported.</li>
  <li><strong><code>committable = False</code></strong> — Unit commitment (on/off decisions) is not supported.</li>
</ul>

<h4>Loads</h4>
<ul>
  <li><strong><code>active = 1</code></strong> — All loads are fixed and always active.</li>
</ul>

<h4>Links</h4>
<ul>
  <li><strong><code>active = 1</code></strong> — All links are always active.</li>
</ul>

<h4>Storage Units</h4>
<ul>
  <li><strong><code>active = 1</code></strong> — All storage units are included in the optimization.</li>
  <li><strong><code>sign = 1</code></strong> — Storage operates with positive dispatch direction.</li>
  <li><strong><code>cyclic_state_of_charge = 1</code></strong> — End state of charge must equal the initial state.</li>
  <li><strong><code>marginal_cost_quadratic = 0</code></strong> — Only linear storage costs are supported.</li>
</ul>

<h4>Stores</h4>
<ul>
  <li><strong><code>active = 1</code></strong> — All stores are included in the optimization.</li>
  <li><strong><code>sign = 1</code></strong> — Store energy flows are positive.</li>
  <li><strong><code>e_cyclic = 1</code></strong> — End energy level must equal the initial level.</li>
  <li><strong><code>marginal_cost_quadratic = 0</code></strong> — Only linear storage costs are supported.</li>
</ul>

<h4>Global Constraints</h4>
<ul>
  <li><strong><code>type = primary_energy</code></strong> — Only primary energy constraints are supported.</li>
  <li><strong><code>carrier.co2_emissions</code></strong> — CO₂ accounting must be defined at the carrier level.</li>
  <li><strong>Supported senses:</strong> <code>&lt;=</code>, <code>==</code></li>
</ul>
</div>

---
**Navigation**
<div style="display: flex; justify-content: space-between;">
  <div style="text-align: left;">
  <button type="button" style="background-color:#CCCCCC; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
    <a href="../3_input_and_output/" style="text-decoration:none; color: #000000">⬅️ Previous page</a>
  </button>
  </div>
  <button type="button" style="background-color:#AAAAFF; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
    <a href="Home/Main_Home/1_context_GEMS.md" style="text-decoration:none; color: #FFFFFF">Home</a>
  </button>
  <div style="text-align: right;">
  <button type="button" style="background-color:#CCCCCC; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
    <a href="../5_step_by_step_guide/" style="text-decoration:none; color: #000000">Next page ➡️</a>
  </button>
  </div>
</div>

---
