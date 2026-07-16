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
    Catalogs["📁 catalogs/ 🔗"]
    ModelLib["📁 model-libraries/ 🔗"]
    DataSeries["📁 data-series/ 🔗"]
    
    System["📄 system.yml 🔗"]
    Params["📄 parameters.yml 🔗"]
    Lib1["📄 library_1.yml"]
    Lib2["📄 library_2.yml"]
    Data1["📊 data-series_1.csv"]
    Data2["📊 data-series_2.csv"]
    Scenario["📄 modeler-scenariobuilder.dat 🔗"]
    Calendar["📊 calendar_file.csv"]
    Taxonomy["📊 taxonomy.yml 🔗"]
    View_Configuration["📊 view_config.yml 🔗"]
    
    Study --> Input
    Study --> Params
    Input --> ModelLib
    Input --> System
    Input --> DataSeries
    Input --> Catalogs
    Input --> Taxonomy
    Input --> Calendar
    Input --> View_Configuration
    ModelLib --> Lib1
    ModelLib --> Lib2
    DataSeries --> Data1
    DataSeries --> Data2
    DataSeries --> Scenario
    
    style Study stroke:#d97706,stroke-width:3px,color:#ffffff
    style Input stroke:#0891b2,stroke-width:3px,color:#ffffff
    style ModelLib stroke:#0891b2,stroke-width:3px,color:#ffffff
    style DataSeries stroke:#0891b2,stroke-width:3px,color:#ffffff
    style Catalogs fill:#d1ecf1,stroke:#0dcaf0,stroke-width:3px,color:#ffffff
    style System stroke:#16a34a,stroke-width:3px,color:#ffffff
    style Taxonomy fill:#d4edda,stroke:#28a745,stroke-width:3px,color:#ffffff
    style View_Configuration fill:#d4edda,stroke:#28a745,stroke-width:3px,color:#ffffff
    style Calendar fill:#d4edda,stroke:#28a745,stroke-width:1px,color:#ffffff
    style Params stroke:#16a34a,stroke-width:3px,color:#ffffff
    style Lib1 stroke:#16a34a,stroke-width:3px,color:#ffffff
    style Lib2 stroke:#3b82f6,stroke-width:3px,color:#ffffff
    style Data1 stroke:#3b82f6,stroke-width:3px,color:#ffffff
    style Data2 stroke:#3b82f6,stroke-width:3px,color:#ffffff
    style Scenario stroke:#3b82f6,stroke-width:3px,color:#ffffff

    
    click ModelLib "../library/"
    click System "../system/"
    click DataSeries "../data-series/"
    click Scenario "../scenario-builder/"
    click Params "../solver-optimization/"
    click Catalogs "../catalog/"
    click Taxonomy "../taxonomy/"
    click View_Configuration "../view-config/"
```

The following pages of this section describe each file and folder in detail. Each page focuses on the role of a specific file, its expected structure, and how it interacts with the rest of the file to form a consistent and executable GEMS study.