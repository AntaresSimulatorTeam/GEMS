<div style="display: flex; justify-content: space-between; align-items: center;">
  <div style="text-align: left;">
    <a href="../../../..">Main Section</a>
  </div>
  <div style="text-align: right;">
    <img src="../../../assets/gemsV2.png" alt="GEMS Logo" width="150"/>
  </div>
</div>

# File Structure

This section provides a high-level overview of the specific files used by [**GEMS framework**](../../../..) and how they collectively describe a complete GEMS study.

These files describe the models logic, input data, scenarios, solver settings, and output representations. A summary of the expected files and their roles is provided in the [GEMS Architecture](../../../1_Overview/Concepts/2_architecture).

Understanding how these files fit together is essential for building, modifying, maintaining and analyzing GEMS studies.

The diagram below illustrates the typical organisation of a GEMS study:

<div style="background: #f5f5f5; padding: 20px; border-radius: 8px; font-family: 'Courier New', monospace; margin: 20px 0;">

📁 **QSE_1_adequacy/**  
├── 📁 **input/**  
│   ├── 📁 **model-libraries/**  
│   │   ├── 📄 library_1.yml <small>→ [<i>example: basic_models_library</i>](https://github.com/AntaresSimulatorTeam/GEMS/blob/main/libraries/basic_models_library.yml)</small>  
│   │   ├── 📄 library_2.yml  
│   │   └── ...  
│   ├── 📄 **system.yml** <small>→ [<i>example from QSE 1</i>](https://github.com/AntaresSimulatorTeam/GEMS/blob/documentation/get_started_quick_examples/resources/Documentation_Examples/QSE/QSE_1_Adequacy/input/system.yml)</small>  
│   └── 📁 **data-series/**  
│       ├── 📊 data-series_1.csv  
│       ├── 📊 data-series_2.csv  
│       └── ...  
└── 📄 **parameters.yml** <small>→ [<i>example</i>](https://github.com/AntaresSimulatorTeam/GEMS/blob/documentation/get_started_quick_examples/resources/Documentation_Examples/QSE/QSE_1_Adequacy/parameters.yml)</small>

</div>

The following pages of this section describe each file and folder in detail. Each page focuses on the role of a specific file, its expected structure, and how it interacts with the rest of the file to form a consistent and executable GEMS study.

**Navigation**

<div style="display: flex; justify-content: space-between;">
  <div style="text-align: left;">
  <button type="button" style="background-color:#CCCCCC; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
    <a href="../../1_Overview/References/4_Users" style="text-decoration:none; color: #000000">⬅️ Previous page</a>
  </button>
  </div>
  <button type="button" style="background-color:#AAAAFF; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
    <a href="../../../.." style="text-decoration:none; color: #FFFFFF">Index</a>
  </button>
  <div style="text-align: right;">
  <button type="button" style="background-color:#CCCCCC; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
    <a href="../1B_gemspy_installation" style="text-decoration:none; color: #000000">Next page ➡️</a>
  </button>
  </div>
</div>

---


© GEMS (LICENSE)