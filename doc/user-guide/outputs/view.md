<div style="display: flex; justify-content: flex-end;">
    <a href="../../../..">
        <img src="../../../assets/gemsV2.png" alt="GEMS Logo" width="150"/>
    </a>
</div>

# View

## What are Views?

**Views** are result tables designed to meet users' expectations. Each View exposes a set of **Metrics**, which define the columns of the resulting tables. They are produced by [GEMS-ViewsBuilder](https://github.com/AntaresSimulatorTeam/GEMS-ViewsBuilder) from GEMS simulation outputs.

???+ note "Links with `catalog.yml` and `view-config.yml`"
    Metrics are defined in [`catalog.yml`](../input-files/catalog.md).

    Which metrics to compute and at what temporal resolution is configured in [`view-config.yml`](../input-files/view-config.md).

## Output format

Views are written as Parquet files at `results/view<timestamp>.parquet` inside the GEMS-ViewsBuilder input directory.

| Column | Description |
|--------|-------------|
| `metric_id` | Identifier of the metric, as defined in [`catalog.yml`](../input-files/catalog.md).|
| `metric_location` | Location name (e.g. bus or area), drawn from the [`taxonomy-category`](../input-files/taxonomy.md) used as location in [`view-config.yml`](../input-files/view-config.md).|
| `granular_date` | Date truncated to the requested time aggregation level (e.g. hourly, daily).|
| `scenario_index` | Scenario index from the [simulation table](simulation-table.md). `null` for deterministic outputs.|
| `value` | Aggregated metric value.|

## Views & advanced (graphical) representation

Output representation describes how simulation results are exposed and formatted for end users. It operates downstream of **Views** and does not affect simulation or metric calculations. This layer is responsible only for structuring and presenting already computed outputs.

**The output representation layer and its supported formats are still under active development.**
