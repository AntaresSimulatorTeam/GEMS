<div style="display: flex; justify-content: space-between; align-items: center;">
  <div style="text-align: left;">
    <a href="../..">Main Section</a>
  </div>
  <div style="text-align: right;">
    <img src="../../../assets/gemsV2.png" alt="GEMS Logo" width="150"/>
  </div>
</div>
<div>
<h1>Input and Output of the Converter</h1>

<h2>Input</h2>
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

<h2>Output</h2>
<p>The converter generates a <strong>structured GEMS study directory</strong> at the provided output path.</p>
<p>The directory layout follows the conventions expected by the GEMS modeler:</p>
```text
study_directory/
└── systems/
    └── system_name/
        └── input/
            ├── optim-config.yml   -------> Benders decomposition parameters, used by the modeler to generate MPS files
            ├── system.yml         -------> Main system description
            ├── parameters.yml     -------> Solver and simulation parameters
            ├── model-libraries/
            │   └── pypsa_models.yml -----> Model library definitions
            └── data-series/       -------> Time and/or scenarion dependent parameters
                └── ...
```
</div>

