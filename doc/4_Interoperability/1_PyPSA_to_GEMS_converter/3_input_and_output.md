<div style="display: flex; justify-content: space-between; align-items: center;">
  <div style="text-align: left;">
    <a href="../..">Main Section</a>
  </div>
  <div style="text-align: right;">
    <img src="../../../assets/gemsV2.png" alt="GEMS Logo" width="150"/>
  </div>
</div>
<div>
<h2>Input and Output of the Converter</h2>

<h3>Input</h3>
<p>The converter requires the following inputs:</p>
<ul>
  <li><strong>PyPSA network object</strong><br/>
  The fully defined PyPSA network that will be converted into a GEMS-compatible study.</li>
  <li><strong>Logger</strong><br/>
  Used for debugging and tracing the conversion process. Logs can help identify configuration issues or data inconsistencies during conversion.</li>
  <li><strong>Output path</strong><br/>
  The directory where the generated GEMS study will be created.</li>
  <li><strong>Time series file format</strong><br/>
  Format used for exported time-dependent data (e.g. csv, tsv).</li>
</ul>

<h3>Output</h3>
<p>The converter generates a <strong>structured GEMS study directory</strong> at the provided output path.</p>
<p>The directory layout follows the conventions expected by the GEMS modeler:</p>
<pre><code>study_directory/
└── systems/
    └── system_name/
        └── input/
            ├── optim-config.yml   --------&gt; Benders decomposition parameters, used by the modeler to generate MPS files
            ├── system.yml         -------------&gt; Main system description
            ├── parameters.yml     -----------&gt; Solver and simulation parameters
            ├── model-libraries/
            │   └── pypsa_models.yml ---&gt; Model library definitions
            └── data-series/       -----------&gt; Time and/or scenarion dependent parameters
                └── ...
</code></pre>
</div>

---
**Navigation**
<div style="display: flex; justify-content: space-between;">
  <div style="text-align: left;">
  <button type="button" style="background-color:#CCCCCC; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
    <a href="../2_how_the_converter_works/" style="text-decoration:none; color: #000000">⬅️ Previous page</a>
  </button>
  </div>
  <button type="button" style="background-color:#AAAAFF; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
    <a href="Home/Main_Home/1_context_GEMS.md" style="text-decoration:none; color: #FFFFFF">Home</a>
  </button>
  <div style="text-align: right;">
  <button type="button" style="background-color:#CCCCCC; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
    <a href="../4_current_limitations/" style="text-decoration:none; color: #000000">Next page ➡️</a>
  </button>
  </div>
</div>

---
