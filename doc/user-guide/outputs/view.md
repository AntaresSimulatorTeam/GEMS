# Views

## What are Views?

**Views** are result tables designed by trimming and aggregation set by users called the metrics. They are produced from the simulation outputs.

???+ tip "Free customisable `Views`"
    These `Views` are fully designed by users through the configuration files ([`taxonomy.yml`](../input-files/taxonomy.md), [`catalog.yml`](../input-files/catalog.md), [`-config.yml`](../input-files/-config.md)).

???+ info "Links with `catalog.yml` and `-config.yml`"
    `metrics` are defined in [`catalog.yml`](../input-files/catalog.md).

    The configuration of which metrics to compute and at what temporal resolution is inside the file [`-config.yml`](../input-files/-config.md).

## Output format

Views are written as Parquet files at `results/<timestamp>.parquet`.

| Column | Description |
|--------|-------------|
| `metric_id` | Identifier of the metric, as defined in [`catalog.yml`](../input-files/catalog.md).|
| `metric_location` | Location name based on the [`taxonomy-category`](../input-files/taxonomy.md) used as location in [`-config.yml`](../input-files/-config.md).|
| `granular_date` | Date truncated to the requested time aggregation level.|
| `scenario_index` | Scenario Index of the simulation.|
| `value` | Aggregated metric value.|

