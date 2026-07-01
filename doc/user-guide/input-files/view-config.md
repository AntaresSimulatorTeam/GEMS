<div style="display: flex; justify-content: flex-end;">
    <a href="../../../..">
        <img src="../../../assets/gemsV2.png" alt="GEMS Logo" width="150"/>
    </a>
</div>

# Views Configuration File

The **Views configuration file** defines which [Views](../outputs/business-view.md) to produce and how. It selects the metrics to compute, the locations to aggregate over and the temporal resolution of the outputs fit for users ; the **views**.

> One `view_config.yml` file can define **views**.

???+ note "Links with `catalog.yml`, `taxonomy.yml` and `calendar_file.csv`"
    The views configuration uses `metrics` defined in [`catalog.yml`](catalog.md).

    Locations are selected thanks to [`taxonomy-category`](taxonomy.md) from [`taxonomy.yml`](taxonomy.md).

    The `calendar_file.csv` maps simulation time indices to real dates. It is a CSV file with the following columns:

    | Column in `calendar_file` | Description |
    |--------|-------------|
    | `absolute_time_index` | Integer time index from the [simulation table](../outputs/simulation-table.md). |
    | `block` | Scenario block index. |
    | `granular_date` | Real datetime (like `2025-01-01 00:00:00`). |

## Example

This is a partial excerpt from the [test_3 view_config](https://github.com/AntaresSimulatorTeam/GEMS-ViewsBuilder/blob/main/resources/test_inputs/test_3/view_config.yml) in the GEMS-ViewsBuilder repo.

```yaml
view:
  id: view_area
  scope:
    - location:
        taxonomy-category: balance
    - calendar: calendar_file
  aggregation:
    - time: hour
  catalog:
    - id: catalog
  metrics:
    - id: catalog.PROD
    - id: catalog.LOAD
    - id: catalog.BALANCE
```

## Key elements in views configuration file

Scope and Aggregation:

*This first part defines what is evaluated and at what resolution.*

| Element | Type | Description |
|------|------|--------------------------|
| `id` | String | A unique identifier for the view.|
| `scope.location` | String | The [`taxonomy-category`](taxonomy.md) whose components serve as location objects (e.g. buses or areas).|
| `scope.calendar` | String | Reference to the calendar file used to map time indices to real dates.|
| `aggregation.time` | String | Temporal resolution for the output: `hour`, `day`, `week`, `month`, or `year`.|

Catalog and metrics:

*This second part selects which metrics to include in the views.*

| Element | Type | Description |
|------|------|--------------------------|
| `catalog.id` | String | The `id` of a [catalog](catalog.md) to use.|
| `metrics.id` | String | A metric to include, referenced as `<catalog_id>.<metric_id>` from [`catalog.yml`](catalog.md).|
