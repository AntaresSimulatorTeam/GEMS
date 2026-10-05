# Views

## What are Views?

**Views** are result tables produced from [simulation outputs](simulation-table.md); users configure them with metrics aggregated over locations, time and scenarios.

???+ tip "Free customisable `Views`"
    These `Views` are fully designed by users through the configuration files ([Taxonomy file](../input-files/taxonomy.md), [Catalog file](../input-files/catalog.md), [View Configuration file](../input-files/view-config.md)).

???+ info "Links with Catalog and View Configuration files"
    `metrics` are defined in the [Catalog files](../input-files/catalog.md).

    The configuration of which metrics to compute, at which locations, and at what temporal and scenario resolution is inside the [View Configuration file](../input-files/view-config.md).

## View output files

One View Configuration file produces one output file per `time-granularity` used in its [aggregation patterns](../input-files/view-config.md#aggregation-patterns). The files are written in the output directory and named `view_<time-granularity>_<timestamp>.parquet` (e.g. `view_hour_20261005T133900.parquet`), where `<timestamp>` is the UTC time of the run, written `YYYYMMDDTHHMMSS`. Views can also be written as CSV files, with the `.csv` extension.

Patterns sharing the same `time-granularity` are written in the same file: the `scenario_aggregation` column tells them apart.

???+ warning "Read columns by name"
    The order of the columns and of the rows is not guaranteed: it can differ from one file to another. Columns should be read by their name.

## Structure of Views

| Views Column | Type | Description |
|--------|------|-------------|
| `metric_id` | String | Identifier of the metric, as defined in the [Catalog file](../input-files/catalog.md#2-metrics-definition). Only the metric `id` is written, without the catalog `id`.|
| `metric_location` | String | Location of the value: the `id` of a component of the location [`taxonomy-category`](../input-files/taxonomy.md) set in the [View Configuration file](../input-files/view-config.md#scope), or the name of an [extra-location](../input-files/view-config.md#scope).|
| `breakdown_properties` | String | Values of the [`breakdown`](../input-files/catalog.md#2-metrics-definition) properties of the contributing components, as `(key,value)` pairs (e.g. `{(technology,nuclear),(company,A)}`). A component that does not have the property gets the value `None`. `{}` for a metric without `breakdown`.|
| `view_date` | Datetime | Start of the period, i.e. the date truncated to the `time-granularity` of the pattern (e.g. `2025-01-01 00:00:00` for the year 2025). Weeks start on Monday. Empty for outputs that are not time-dependent.|
| `scenario_id` | Integer | Monte-Carlo scenario index. Empty when `scenario_aggregation` is `true`, and for outputs that are not scenario-dependent.|
| `metric_value` | Float | Aggregated metric value. When `scenario_aggregation` is `true`, value of the statistic named in `scenario_stat`.|
| `scenario_aggregation` | Boolean | `false` for the rows of a pattern with `scenario: false` (one value per scenario), `true` for the rows of a pattern with `scenario: true` (statistics across scenarios).|
| `scenario_stat` | String | Statistic across scenarios when `scenario_aggregation` is `true`: `exp` (expectation), `std` (population standard deviation), `min` or `max`. Empty when `scenario_aggregation` is `false`.|

## Example

These rows are extracts of the Views produced by the [View Configuration file example](../input-files/view-config.md#example), with the [taxonomy](../input-files/taxonomy.md#example) and [catalog](../input-files/catalog.md#example) examples, for a system with a single area `area_fr` having the property `country: France`.

Extract of `view_hour_<timestamp>.parquet` (pattern `hourly`, one value per scenario):

| metric_id | metric_location | breakdown_properties | view_date | scenario_id | metric_value | scenario_aggregation | scenario_stat |
|---|---|---|---|---|---|---|---|
| PRODUCTION | area_fr | {} | 2025-01-01 04:00:00 | 0 | 437.15 | false | |
| PRODUCTION | France | {} | 2025-01-01 04:00:00 | 0 | 437.15 | false | |
| PRODUCTION_BY_TECH_AND_COMPANY | area_fr | {(technology,gas),(company,rhonepower)} | 2025-01-01 04:00:00 | 0 | 0.0 | false | |
| PRODUCTION_BY_TECH_AND_COMPANY | area_fr | {(technology,nuclear),(company,britishnuke)} | 2025-01-01 04:00:00 | 0 | 187.15 | false | |
| PRODUCTION_BY_TECH_AND_COMPANY | area_fr | {(technology,nuclear),(company,rhonepower)} | 2025-01-01 04:00:00 | 0 | 250.0 | false | |

Extract of `view_year_<timestamp>.parquet` (pattern `yearly_stats`, statistics across scenarios):

| metric_id | metric_location | breakdown_properties | view_date | scenario_id | metric_value | scenario_aggregation | scenario_stat |
|---|---|---|---|---|---|---|---|
| PRODUCTION | area_fr | {} | 2025-01-01 00:00:00 | | 14557.952 | true | exp |
| PRODUCTION | area_fr | {} | 2025-01-01 00:00:00 | | 1249.679 | true | std |
| PRODUCTION | area_fr | {} | 2025-01-01 00:00:00 | | 12194.6 | true | min |
| PRODUCTION | area_fr | {} | 2025-01-01 00:00:00 | | 17297.17 | true | max |
