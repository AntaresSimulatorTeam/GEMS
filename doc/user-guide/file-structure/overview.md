# File Structure

This section provides a high-level overview of the specific files used by [**GEMS framework**](../../index.md) and how they collectively describe a complete GEMS study.

These files describe the models logic, input data, scenarios, solver settings, and output representations. A summary of the expected files and their roles is provided in the [GEMS Architecture](../../overview/architecture.md).

Understanding how these files fit together is essential for building, modifying, maintaining and analyzing GEMS studies.

The diagram below illustrates the typical organisation of a GEMS study:

*Click on the elements with the 🔗 emoji in order to be redirected to their dedicated documentation*

```mermaid
flowchart LR
    Study["📁 GEMS_Study/"]
    Input["📁 input/"]
    ModelLib["📁 model-libraries/ 🔗"]
    DataSeries["📁 data-series/ 🔗"]
    
    System["📄 system.yml 🔗"]
    Params["📄 parameters.yml 🔗"]
    Lib1["📄 library_1.yml"]
    Lib2["📄 library_2.yml"]
    Data1["📊 data-series_1.csv"]
    Data2["📊 data-series_2.csv"]
    Scenario["📄 modeler-scenariobuilder.dat 🔗"]
    
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
    
    style Study fill:#c97d00,stroke:#ffc107,stroke-width:3px,color:#ffffff
    style Input fill:#0a7fa8,stroke:#0dcaf0,stroke-width:2px,color:#ffffff
    style ModelLib fill:#0a7fa8,stroke:#0dcaf0,stroke-width:2px,color:#ffffff
    style DataSeries fill:#0a7fa8,stroke:#0dcaf0,stroke-width:2px,color:#ffffff
    style System fill:#1e8a3f,stroke:#28a745,stroke-width:3px,color:#ffffff
    style Params fill:#1e8a3f,stroke:#28a745,stroke-width:3px,color:#ffffff
    style Lib1 fill:#1e8a3f,stroke:#28a745,stroke-width:3px,color:#ffffff
    style Lib2 fill:#0270a0,stroke:#0288d1,stroke-width:2px,color:#ffffff
    style Data1 fill:#0270a0,stroke:#0288d1,stroke-width:2px,color:#ffffff
    style Data2 fill:#0270a0,stroke:#0288d1,stroke-width:2px,color:#ffffff
    style Scenario fill:#0270a0,stroke:#0288d1,stroke-width:2px,color:#ffffff

    
    click ModelLib "../library/"
    click System "../system/"
    click DataSeries "../data-series/"
    click Scenario "../scenario-builder/"
    click Params "../solver-optimization/"
```

The following pages of this section describe each file and folder in detail. Each page focuses on the role of a specific file, its expected structure, and how it interacts with the rest of the file to form a consistent and executable GEMS study.