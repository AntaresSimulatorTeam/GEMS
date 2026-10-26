# Outputs

The study will generate two types of output files:

- [**Files similar to Legacy studies**](https://antares-simulator.readthedocs.io/en/latest/reference/solver/outputs/): outputs corresponding to the optimization results coming from the components created by the Legacy study.
- [**Simulation tables**](../../user-guide/outputs/simulation-table.md): specific to modeler's components optimization, in the same output folder as the Legacy outputs. They are only written when the study is run with the `--output all` (or `--output simulation-tables`) option of Antares Solver. One simulation table is generated for each Monte-Carlo year and each resolution stage that runs, called `simulation-table-<year>-<stage>.csv` (e.g. `simulation-table-0-optim-nb-1.csv`): `optim-nb-1` and `optim-nb-2` for the first and second optimizations (there is no second optimization when `unit-commitment-mode` is `milp`), `peak-shaving` and `adq-patch` for the post-processes.
