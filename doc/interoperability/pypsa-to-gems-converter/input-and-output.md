# Input and Output of the Converter

## Input

The converter requires the following inputs:

- **PyPSA network object**  
  The fully defined PyPSA network that will be converted into a GEMS-compatible study.
- **Logger**  
  Used for debugging and tracing the conversion process. Logs can help identify configuration issues or data inconsistencies during conversion.
- **Output path**  
  The directory where the generated GEMS study will be created.
- **Time series file format**  
  Format used for exported time-dependent data (e.g. csv, tsv).

## Output

The converter generates a **structured GEMS study directory** at the provided output path.

The directory layout follows the conventions expected by the GEMS modeler:

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
            └── data-series/       -------> Time and/or scenario dependent parameters
                └── ...
```

Each generated file follows the GEMS file structure conventions: see the [system file](../../user-guide/file-structure/system.md), [library file](../../user-guide/file-structure/library.md), [data series](../../user-guide/file-structure/data-series.md), and [solver parameters](../../user-guide/file-structure/solver-optimization.md) documentation for details on their format and content.