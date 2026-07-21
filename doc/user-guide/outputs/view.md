# Views

## What are Views?

**Views** are result tables produced from simulation outputs; users configure with metrics aggregated over locations and time. They are produced from the simulation outputs.

???+ tip "Free customisable `Views`"
    These `Views` are fully designed by users through the configuration files ([Taxonomy file](../input-files/taxonomy.md), [Catalog file](../input-files/catalog.md), [View Configuration file](../input-files/-config.md)).

???+ info "Links with Catalog and View Configuration files"
    `metrics` are defined in the [Catalog file](../input-files/catalog.md).

    The configuration of which metrics to compute and at what temporal resolution is inside the [View Configuration file](../input-files/-config.md).

## Structure of Views

Views are written as Parquet files at `results/<timestamp>.parquet`.

| Views Column | Description |
|--------|-------------|
| `metric_id` | Identifier of the metric, as defined in the [Catalog file](../input-files/catalog.md).|
| `metric_location` | Location name based on the [`taxonomy-category`](../input-files/taxonomy.md) used as location in the [View Configuration file](../input-files/view-config.md).|
| `view_date` | Date truncated to the requested time aggregation level.|
| `scenario_id` | Monte-Carlo Scenario Index.|
| `value` | Aggregated metric value.|

