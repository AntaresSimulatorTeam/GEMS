# How the Converter Works

The PyPSA to GEMS Converter transforms [PyPSA Network](https://docs.pypsa.org/latest/api/networks/network/) into a [GEMS study folder](../../user-guide/file-structure/overview.md), through the following steps.

## 1. Input Validation and Preprocessing

The converter first validates that the PyPSA network meets the requirements for conversion.
It performs necessary preprocessing steps such as normalizing component names, handling missing attributes, and ensuring data consistency.
This stage ensures the input PyPSA model is **compatible** with the conversion process.

## 2. Component Registration and Data Extraction

The converter identifies and extracts all relevant components from the PyPSA network, including both **static (constant)** and **dynamic (time-dependent)** parameters.
It maps PyPSA-specific parameter names to their GEMS equivalents and organizes the data for conversion.

## 3. Time Series Processing

For parameters that vary over time, the converter extracts time series data and writes them to separate data files (**CSV** or **TSV** format).
The converter handles both deterministic studies (single time series) and stochastic studies (multiple scenarios), maintaining the temporal structure of the original PyPSA model.

## 4. GEMS Component Generation

Each PyPSA component is transformed into its corresponding GEMS representation.
The converter creates GEMS components with appropriate parameters, distinguishing between constant values and time-dependent references.
Connections between components (such as generators and loads connected to buses) are established through GEMS port connections.

## 5. Global Constraints Handling

If the PyPSA model includes global constraints (such as CO₂ emission limits), the converter identifies these and creates corresponding GEMS constraint components, linking them to the relevant system components.

## 6. Study Structure Generation

Finally, the converter generates the complete GEMS study structure.

