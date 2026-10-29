# Views Configuration Files

The **View Configuration file** defines which [Views](../outputs/views.md) to produce and how. It selects the metrics to compute, the locations to aggregate over and the temporal and scenario resolutions of the outputs fit for users ; the **views**.

> One View Configuration file defines a **[View](../outputs/views.md)**. One output file is produced per [aggregation pattern](#aggregation-patterns).
>
> Several View Configuration files can be processed in the same run: each one produces its own output files, and their `id` must all be different.

???+ info "Links with Catalog, Taxonomy and Calendar files"
    The View Configuration file uses `metrics` defined in the [Catalog files](catalog.md).

    Locations are selected thanks to [`taxonomy-category`](taxonomy.md) from the [Taxonomy file](taxonomy.md).

    The [Calendar file](calendar.md), named by `scope.calendar`, maps the time indices of the simulation to real dates. Only the time steps listed in the calendar are used to build the View.

## Structure of the View Configuration file

The View Configuration file has a single root key `view`. Unknown keys under `view` are rejected.

### Scope

*This first part defines what is evaluated.*

| Element | Type | Description |
|------|------|--------------------------|
| `id` | String | A unique identifier for the view. It is used in the name of the [output files](../outputs/views.md#view-output-files).|
| `scope.location.taxonomy-category` | String | The [`taxonomy-category`](taxonomy.md) whose components serve as location objects (e.g. buses or areas). It must be defined in the taxonomy and match the `location.taxonomy-category` of every [catalog](catalog.md) used in `metrics`.|
| `taxonomy` | String | The `id` of the [taxonomy](taxonomy.md) used by the view. It must match the taxonomy file and the `taxonomy` of every [catalog](catalog.md) used in `metrics`.|
| `scope.extra-locations` | List | *(Optional)* List of [property](library.md#properties) keys, each given by its `id` (`- id: country`). For each location component having one of these properties, the metric is also computed at the location named by the property value (e.g. all areas with `country: France` also contribute to the location `France`). Location components without the property only contribute to their own location. Location ids and extra-location names share the same names: contributions to the same name are added together, so an extra-location value should not be equal to a location component id, and one location component should not get the same name from two extra-location keys.|

### Aggregation patterns

*This second part defines at what resolution the metrics are evaluated. `aggregations-patterns` is a list of at least one pattern.*

| Element | Type | Description |
|------|------|--------------------------|
| `id` | String | A unique identifier for the pattern within the view. It is used in the name of the [output file](../outputs/views.md#view-output-files) of the pattern.|
| `time-granularity` | String | Temporal resolution for the output: `hour`, `day`, `week`, `month`, or `year`. Values are aggregated over time with the metric's [`time-operator`](catalog.md#2-metrics-definition). Dates are truncated to the start of the period (weeks start on Monday).|
| `scenario` | Boolean | If `false`, one value is written per Monte-Carlo scenario. If `true`, the time-aggregated values are aggregated across scenarios and the expectation (`exp`), standard deviation (`std`, population standard deviation), minimum (`min`) and maximum (`max`) are written instead, one row per statistic: the statistic is named in the `scenario_stat` column, `scenario_id` is empty and `scenario_aggregation` is `true`. With `false`, `scenario_stat` is empty and `scenario_aggregation` is `false`.|
| `location-filter` | List | *(Optional)* List of location names (`metric_location` values, including [extra-locations](#scope)) to keep in the output. If omitted or empty, all locations are kept. Names matching no location are ignored: if none of the listed names match, the pattern gives no rows.|

???+ warning "Rules on aggregation patterns"
    Each combination of (`time-granularity`, `scenario`) can only be defined once, which gives at most 10 patterns per view.

    Each pattern is written in its own [output file](../outputs/views.md#view-output-files), whose name contains the pattern `id`. The pattern `id` is not written in the rows of the file.

### Metrics

*This third part selects which Metrics from which Catalogs to include in the View.*

| Element | Type | Description |
|------|------|--------------------------|
| `metrics` | List | List of at least one metric, each given by its `id` referenced as `<catalog_id>.<metric_id>`. The catalog is found by its `id` among the catalogs of the catalogs directory, and the metric must be defined in that [catalog](catalog.md).|

## Example

This example uses the `my_taxonomy` taxonomy and the `catalog` catalog defined in the [taxonomy](taxonomy.md#example) and [catalog](catalog.md#example) pages.

```yaml
view:
  id: view_area

  taxonomy: my_taxonomy

  scope:
    location:
      taxonomy-category: balance
    extra-locations:
      - id: country

  aggregations-patterns:
    - id: hourly
      time-granularity: hour
      scenario: false
    - id: yearly_stats
      time-granularity: year
      scenario: true
      location-filter:
        - area_fr
        - France

  metrics:
    - id: catalog.PRODUCTION
    - id: catalog.LOAD
    - id: catalog.PRODUCTION_BY_TECH_AND_COMPANY
    - id: catalog.NUCLEAR_PRODUCTION
```
