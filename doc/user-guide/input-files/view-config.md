# Views Configuration Files

The **View Configuration file** defines which [Views](../outputs/views.md) to produce and how. It selects the metrics to compute, the locations to aggregate over and the temporal and scenario resolutions of the outputs fit for users ; the **views**.

> One View Configuration file defines a **[View](../outputs/views.md)**. One output file is produced per `time-granularity` used in the [aggregation patterns](#aggregation-patterns).

???+ info "Links with Catalog, Taxonomy and Calendar files"
    The View Configuration file uses `metrics` defined in the [Catalog files](catalog.md).

    Locations are selected thanks to [`taxonomy-category`](taxonomy.md) from the [Taxonomy file](taxonomy.md).

    The Calendar file maps simulation time indices to real dates. Only the time steps listed in the calendar (with the same `block` as in the simulation table) are used to build the View. It is a comma-separated CSV file with a header row and exactly the following columns:

    | Column in the Calendar file | Description |
    |--------|-------------|
    | `absolute_time_index` | Integer time index from the [simulation table](../outputs/simulation-table.md). Values must be contiguous and start at `0` (`0, 1, ..., N-1`). Each calendar row gives the date of the simulation table rows having the same `absolute_time_index`: the calendar must therefore follow the time indexing of the simulation table, and simulation time steps beyond the last calendar row are not used.|
    | `block` | Time block index. It must match the `block` column of the simulation table. |
    | `granular_date` | Real datetime, written `YYYY-MM-DD HH:MM:SS` (like `2025-01-01 00:00:00`). The time step between two consecutive rows must be constant. Dates in another format may not be recognized and make the building of Views fail with an error that does not mention the calendar. Dates with a UTC offset (like `2025-01-01 00:00:00+01:00`) are converted to UTC, and periods (days, months, years) are then cut in UTC. |

    ???+ warning "Calendar and simulation table must match"
        If no time step of the calendar matches the simulation table (for example because of different `block` values), the View is still produced without error, but each metric on time-dependent outputs only has a single row with an empty `view_date` and `scenario_id` and a `0` value (an empty value with `avg`). Metrics on outputs that are not time-dependent keep their values, so the View can look partly correct.

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

## Structure of the View Configuration file

The View Configuration file has a single root key `view`. Unknown keys under `view` are rejected.

### Scope

*This first part defines what is evaluated.*

| Element | Type | Description |
|------|------|--------------------------|
| `id` | String | A unique identifier for the view.|
| `taxonomy` | String | The `id` of the [taxonomy](taxonomy.md) used by the view. It must match the taxonomy file and the `taxonomy` of every [catalog](catalog.md) listed in `catalogs`.|
| `scope.location.taxonomy-category` | String | The [`taxonomy-category`](taxonomy.md) whose components serve as location objects (e.g. buses or areas). It must be defined in the taxonomy and match the `location.taxonomy-category` of every [catalog](catalog.md) listed in `catalogs`.|
| `scope.calendar` | String | Name of the calendar file (without the `.csv` extension) used to map time indices to real dates. It is informative: the calendar actually used is the calendar file provided as input.|
| `scope.extra-locations` | List | *(Optional)* List of [property](library.md#properties) keys, each given by its `id` (`- id: country`). For each location component having one of these properties, the metric is also computed at the location named by the property value (e.g. all areas with `country: France` also contribute to the location `France`). Location components without the property only contribute to their own location. Location ids and extra-location names share the same names: contributions to the same name are added together, so an extra-location value should not be equal to a location component id, and one location component should not get the same name from two extra-location keys.|

### Aggregation patterns

*This second part defines at what resolution the metrics are evaluated. `aggregations-patterns` is a list of at least one pattern.*

| Element | Type | Description |
|------|------|--------------------------|
| `id` | String | A unique identifier for the pattern.|
| `time-granularity` | String | Temporal resolution for the output: `hour`, `day`, `week`, `month`, or `year`. Values are aggregated over time with the metric's [`time-operator`](catalog.md#2-metrics-definition). Dates are truncated to the start of the period (weeks start on Monday).|
| `scenario` | Boolean | If `false`, one value is written per Monte-Carlo scenario. If `true`, the time-aggregated values are aggregated across scenarios and the expectation (`exp`), standard deviation (`std`, population standard deviation), minimum (`min`) and maximum (`max`) are written instead, one row per statistic: the statistic is named in the `scenario_stat` column, `scenario_id` is empty and `scenario_aggregation` is `true`. With `false`, `scenario_stat` is empty and `scenario_aggregation` is `false`.|
| `spatial-filter` | List | *(Optional)* List of location names (`metric_location` values, including [extra-locations](#scope)) to keep in the output. If omitted or empty, all locations are kept. Names matching no location are ignored: if none of the listed names match, the pattern gives no rows.|

???+ warning "Rules on aggregation patterns"
    Each combination of (`time-granularity`, `scenario`) can only be defined once, which gives at most 10 patterns per view.

    Patterns sharing the same `time-granularity` are written in the same output file; the `scenario_aggregation` column of the [Views](../outputs/views.md) tells them apart. The pattern `id` is not written in the output.

### Catalogs and metrics

*This third part selects which Metrics from which Catalogs to include in the View.*

| Element | Type | Description |
|------|------|--------------------------|
| `catalogs` | List | List of at least one [catalog](catalog.md), each given by its `id` (`- id: catalog`). The catalog is read from the file `<id>.yml` of the catalogs directory; other catalog files of the directory are ignored. Every listed catalog is fully checked, including the metrics that are not selected in `metrics`.|
| `metrics` | List | List of at least one metric, each given by its `id` referenced as `<catalog_id>.<metric_id>`. The catalog must be listed in `catalogs` and the metric must be defined in that [catalog](catalog.md). As `.` is the separator, catalog and metric ids must not contain a `.`. Only the metric id is written in the Views: selected metrics should have different ids, and a metric should be listed only once (otherwise its rows are written twice).|
