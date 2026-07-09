# Business Views

## What are Business Views?

**Views** are result tables designed to meet business-user expectations. Each View exposes a set of Variables, which define the columns of the resulting tables. Their computation is configured through [View Configuration Files](../file-structure/business-view-configuration.md), which operate on data from the [Simulation Table](simulation-table.md).

**The generation of Business View is still under active development in GEMS interpreters.**
## Views & advanced (graphical) representation

Output representation describes how simulation results are exposed and formatted for end users. It operates downstream of **Views** and does not affect simulation or metric calculations. This layer is responsible only for structuring and presenting already computed Metrics.

**The output representation layer and its supported formats are still under active development.**