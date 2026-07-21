# Views Configuration Files

The **Views configuration file** defines which [Views](../outputs/business-view.md) to produce and how. It selects the metrics to compute, the locations to aggregate over and the temporal resolution of the outputs fit for users ; the **views**.

> One `view_config.yml` file define a **Views**.

???+ info "Links with Catalog, Taxonomy and Calendar files"
    The views configuration uses `metrics` defined in the [Catalog file](catalog.md).

    Locations are selected thanks to [`taxonomy-category`](taxonomy.md) from the [Taxonomy file](taxonomy.md).

    The Calendar file maps simulation time indices to real dates. It is a CSV file with the following columns:

    | Column in the Calendar file | Description |
    |--------|-------------|
    | `absolute_time_index` | Integer time index from the [simulation table](../outputs/simulation-table.md). |
    | `block` | Scenario block index. |
    | `granular_date` | Real datetime (like `2025-01-01 00:00:00`). |

## Example

This example uses the `antares_legacy_taxonomy` and `antares_legacy_catalog` defined in the [taxonomy](taxonomy.md) and [catalog](catalog.md) pages.

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
    - id: antares_legacy_catalog
  metrics:
    - id: antares_legacy_catalog.PROD
    - id: antares_legacy_catalog.LOAD
    - id: antares_legacy_catalog.INSTALLED_PROD_CAPACITY
    - id: antares_legacy_catalog.BALANCE
```

## Structure of the View Configuration files

### Scope and Aggregation

*This first part defines what is evaluated and at what resolution.*

| Element | Type | Description |
|------|------|--------------------------|
| `id` | String | A unique identifier for the view.|
| `scope.location` | String | The [`taxonomy-category`](taxonomy.md) whose components serve as location objects (e.g. buses or areas).|
| `scope.calendar` | String | Reference to the calendar file used to map time indices to real dates.|
| `aggregation.time` | String | Temporal resolution for the output: `hour`, `day`, `week`, `month`, or `year`.|

### Catalog and metrics

*This second part selects which Metrics from which Catalogs to include in the View.

| Element | Type | Description |
|------|------|--------------------------|
| `catalog.id` | String | The `id` of a [catalog](catalog.md) to use.|
| `metrics.id` | String | A metric to include, referenced as `<catalog_id>.<metric_id>` from the [Catalog file](catalog.md).|
