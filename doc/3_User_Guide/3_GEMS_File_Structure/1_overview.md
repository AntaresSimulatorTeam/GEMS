<div style="display: flex; justify-content: space-between; align-items: center;">
  <div style="text-align: left;">
    <a href="../../../..">Main Section</a>
  </div>
  <div style="text-align: right;">
    <img src="../../../assets/gemsV2.png" alt="GEMS Logo" width="150"/>
  </div>
</div>

# File Structure

This section provides a high-level overview of the specific files used by [**GEMS framework**](../../index.md) and how they collectively describe a complete GEMS study.

These files describe the models logic, input data, scenarios, solver settings, and output representations. A summary of the expected files and their roles is provided in the [GEMS Architecture](../../1_Overview/1_Architecture.md).

Understanding how these files fit together is essential for building, modifying, maintaining and analyzing GEMS studies.

The diagram below illustrates the typical organisation of a GEMS study:

```mermaid
flowchart LR
    Study["📁 GEMS_Study/"]
    Input["📁 input/"]
    ModelLib["📁 model-libraries/"]
    DataSeries["📁 data-series/"]
    
    System["📄 system.yml"]
    Params["📄 parameters.yml"]
    Lib1["📄 library_1.yml"]
    Lib2["📄 library_2.yml"]
    Data1["📊 data-series_1.csv"]
    Data2["📊 data-series_2.csv"]
    Scenario["📄 modeler-scenariobuilder.dat"]
    
    Study --> Input
    Study --> Params
    Input --> ModelLib
    Input --> System
    Input --> DataSeries
    ModelLib --> Lib1
    ModelLib --> Lib2
    DataSeries --> Data1
    DataSeries --> Data2
    DataSeries --> Scenario
    
    style Study fill:#fff3cd,stroke:#ffc107,stroke-width:3px
    style Input fill:#d1ecf1,stroke:#0dcaf0,stroke-width:2px
    style ModelLib fill:#d1ecf1,stroke:#0dcaf0,stroke-width:2px
    style DataSeries fill:#d1ecf1,stroke:#0dcaf0,stroke-width:2px
    style System fill:#d4edda,stroke:#28a745,stroke-width:3px
    style Params fill:#d4edda,stroke:#28a745,stroke-width:3px
    style Lib1 fill:#d4edda,stroke:#28a745,stroke-width:3px
    style Lib2 fill:#e1f5ff,stroke:#0288d1,stroke-width:2px
    style Data1 fill:#e1f5ff,stroke:#0288d1,stroke-width:2px
    style Data2 fill:#e1f5ff,stroke:#0288d1,stroke-width:2px
    style Scenario fill:#e1f5ff,stroke:#0288d1,stroke-width:2px

    
    click ModelLib "../2_library/"
    click System "../3_system/"
    click DataSeries "../4_data_series/"
    click Scenario "../5_scenario_builder/"
    click Params "../6_solver_optimization/"
```

The following pages of this section describe each file and folder in detail. Each page focuses on the role of a specific file, its expected structure, and how it interacts with the rest of the file to form a consistent and executable GEMS study.