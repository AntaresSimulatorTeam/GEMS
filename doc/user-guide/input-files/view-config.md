# Views Configuration Files

The **Views configuration file** defines which [Views](../outputs/views.md) to produce and how. It selects the metrics to compute, the locations to aggregate over and the temporal and scenario resolutions of the outputs fit for users ; the **views**.

> One Views Configuration file define a **[View](../outputs/views.md)**. One output file is produced per `time-granularity` used in the [aggregation patterns](#aggregation-patterns).

???+ info "Links with Catalog, Taxonomy and Calendar files"
    The views configuration uses `metrics` defined in the [Catalog files](catalog.md).

    Locations are selected thanks to [`taxonomy-category`](taxonomy.md) from the [Taxonomy file](taxonomy.md).

    The Calendar file maps simulation time indices to real dates. Only the time steps listed in the calendar (with the same `block` as in the simulation table) are used to build the View. It is a CSV file with exactly the following columns:

    | Column in the Calendar file | Description |
    |--------|-------------|
    | `absolute_time_index` | Integer time index from the [simulation table](../outputs/simulation-table.md). Values must be contiguous and start at `0` (`0, 1, ..., N-1`).|
    | `block` | Scenario block index. |
    | `granular_date` | Real datetime (like `2025-01-01 00:00:00`). The time step between two consecutive rows must be constant. |

## Example

This example uses the `my_taxonomy` taxonomy and the `catalog` catalog defined in the [taxonomy](taxonomy.md#example) and [catalog](catalog.md#example) pages.

```yaml
view:
  id: view_area

  taxonomy: my_taxonomy

  scope:
    location:
      taxonomy-category: balance
    calendar: calendar_file
    extra-locations:
      - id: country

  aggregations-patterns:
    - id: hourly
      time-granularity: hour
      scenario: false
    - id: yearly_stats
      time-granularity: year
      scenario: true
      spatial-filter:
        - area_fr
        - France

  catalogs:
    - id: catalog

  metrics:
    - id: catalog.PRODUCTION
    - id: catalog.LOAD
    - id: catalog.PRODUCTION_BY_TECH_AND_COMPANY
    - id: catalog.NUCLEAR_PRODUCTION
```

## Structure of the Views Configuration files

The view configuration file has a single root key `view`. Unknown keys are rejected.

### Scope

*This first part defines what is evaluated.*

| Element | Type | Description |
|------|------|--------------------------|
| `id` | String | A unique identifier for the view.|
| `taxonomy` | String | The `id` of the [taxonomy](taxonomy.md) used by the view. It must match the taxonomy file and the `taxonomy` of every [catalog](catalog.md) used.|
| `scope.location.taxonomy-category` | String | The [`taxonomy-category`](taxonomy.md) whose components serve as location objects (e.g. buses or areas). It must be defined in the taxonomy and match the `location.taxonomy-category` of every [catalog](catalog.md) used.|
| `scope.calendar` | String | Name of the calendar file (without the `.csv` extension) used to map time indices to real dates. It is informative: the calendar actually used is the file given to ViewsBuilder.|
| `scope.extra-locations` | List | *(Optional)* List of [property](library.md#properties) keys, each given by its `id` (`- id: country`). For each location component having one of these properties, the metric is also computed at the location named by the property value (e.g. all areas with `country: France` also contribute to the location `France`). Location components without the property only contribute to their own location.|

### Aggregation patterns

*This second part defines at what resolution the metrics are evaluated. `aggregations-patterns` is a list of at least one pattern.*

| Element | Type | Description |
|------|------|--------------------------|
| `id` | String | A unique identifier for the pattern.|
| `time-granularity` | String | Temporal resolution for the output: `hour`, `day`, `week`, `month`, or `year`. Values are aggregated over time with the metric's [`time-operator`](catalog.md#2-metrics-definition). Dates are truncated to the start of the period (weeks start on Monday).|
| `scenario` | Boolean | If `false`, one value is written per Monte-Carlo scenario. If `true`, the time-aggregated values are aggregated across scenarios and the expectation (`exp`), standard deviation (`std`, population standard deviation), minimum (`min`) and maximum (`max`) are written instead.|
| `spatial-filter` | List | *(Optional)* List of location names (`metric_location` values, including [extra-locations](#scope)) to keep in the output. If omitted, all locations are kept.|

???+ warning "Rules on aggregation patterns"
    Each combination of (`time-granularity`, `scenario`) can only be defined once, which gives at most 10 patterns per view.

    Patterns sharing the same `time-granularity` are written in the same output file; the `scenario_aggregation` column of the [Views](../outputs/views.md) tells them apart. The pattern `id` is not written in the output.

### Catalogs and metrics

*This third part selects which Metrics from which Catalogs to include in the View.*

| Element | Type | Description |
|------|------|--------------------------|
| `catalogs` | List | List of at least one [catalog](catalog.md), each given by its `id` (`- id: catalog`). The catalog is read from the file `<id>.yml` of the catalogs directory; other catalog files of the directory are ignored.|
| `metrics` | List | List of at least one metric, each given by its `id` referenced as `<catalog_id>.<metric_id>`. The catalog must be listed in `catalogs` and the metric must be defined in that [catalog](catalog.md). As `.` is the separator, catalog and metric ids must not contain a `.`.|
