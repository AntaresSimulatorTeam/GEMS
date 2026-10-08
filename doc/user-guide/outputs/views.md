# Views

## What are Views?

**Views** are result tables computed from the [simulation outputs](simulation-table.md). Each row holds a metric aggregated over a location, a time period and either one scenario or all scenarios (in case of statistics over several scenarios).

???+ tip "Freely customisable `Views`"
    These `Views` are fully designed by users through the configuration files ([Taxonomy file](../input-files/taxonomy.md), [Catalog file](../input-files/catalog.md), [View Configuration file](../input-files/view-config.md)).

???+ info "Links with Catalog and View Configuration files"
    `metrics` are defined in the [Catalog files](../input-files/catalog.md).

    The configuration of which metrics to compute, at which locations, and at what temporal and scenario resolution is inside the [View Configuration file](../input-files/view-config.md).

## View output files

One [View Configuration file](../input-files/view-config.md) produces one timestamped file per `time-granularity` used in its [aggregation patterns](../input-files/view-config.md#aggregation-patterns). Views are written as Parquet or CSV files.

Patterns sharing the same `time-granularity` (at most two: one with `scenario: false`, one with `scenario: true`) are written in the same file: the `scenario_aggregation` column tells them apart. With a [`spatial-filter`](../input-files/view-config.md#aggregation-patterns), these two patterns can cover different locations.

???+ info "CSV files"
    CSV files use a comma separator and a header row. An empty field is a missing value (e.g. the `scenario_id` of the statistics rows). Booleans are written `true`/`false` and dates in ISO 8601 format (e.g. `2025-01-01T04:00:00.000000`, followed by `+0000` when the calendar dates have a UTC offset). Values containing a comma, such as most `breakdown_properties`, are double-quoted.

## Columns of Views

???+ warning "Read columns by name"
    The order of the columns and of the rows is not guaranteed: it can differ from one file to another. Columns should be read by their name.

| Views Column | Type | Description |
|--------|------|-------------|
| `metric_id` | String | Identifier of the metric, as defined in the [Catalog file](../input-files/catalog.md#2-metrics-definition). Only the metric `id` is written, without the catalog `id`.|
| `metric_location` | String | Location of the value: the `id` of a location component, i.e. a component of the location [`taxonomy-category`](../input-files/taxonomy.md) set in the [View Configuration file](../input-files/view-config.md#scope), or the value of an [extra-location](../input-files/view-config.md#scope) property of that component (e.g. `France` for `country: France`).|
| `breakdown_properties` | String | Values of the [`breakdown`](../input-files/catalog.md#2-metrics-definition) properties of the contributing components, as `(key,value)` pairs (e.g. `{(technology,nuclear),(company,A)}`). A component that does not have the property gets the value `None`. `{}` for a metric without `breakdown`.|
| `view_date` | Datetime | Start of the period, i.e. the date truncated to the `time-granularity` of the pattern (e.g. `2025-01-01 00:00:00` for the year 2025). Weeks start on Monday. When the calendar dates have a UTC offset, dates are in UTC. Empty for outputs that are not time-dependent.|
| `scenario_id` | Integer | Monte-Carlo scenario index, as in the `scenario_index` column of the [simulation table](simulation-table.md). Empty when `scenario_aggregation` is `true`, and for outputs that are not scenario-dependent.|
| `metric_value` | Float | Aggregated metric value. When `scenario_aggregation` is `true`, value of the statistic named in `scenario_stat`.|
| `scenario_aggregation` | Boolean | `false` for the rows of a pattern with `scenario: false` (one value per scenario), `true` for the rows of a pattern with `scenario: true` (statistics across scenarios).|
| `scenario_stat` | String | Statistic across scenarios when `scenario_aggregation` is `true`: `exp` (mean over the scenarios, all having the same weight), `std` (population standard deviation), `min` or `max`. Empty when `scenario_aggregation` is `false`.|

## Rows of a View

With a pattern having `scenario: false`, a View has one row per metric, location, breakdown value, period and scenario. With a pattern having `scenario: true`, it has four rows, one per statistic, per metric, location, breakdown value and period. A location with no contributing component has no row (and not a `0` value).

Values only cover the time steps listed in the calendar. A period only partly covered by the calendar (e.g. a year, for a one-week simulation) is aggregated over its covered time steps only, and is still dated by the start of the period: a simulation starting on Wednesday `2025-01-01` gives a first week dated Monday `2024-12-30`.

Statistics across scenarios are computed on the time-aggregated values: for a yearly pattern, `max` is the largest yearly value among the scenarios, not an hourly peak.

## Example

These rows are extracts of the Views produced by the [View Configuration file example](../input-files/view-config.md#example), with the [taxonomy](../input-files/taxonomy.md#example) and [catalog](../input-files/catalog.md#example) examples. The system has a single area `area_fr` with the property `country: France`, two nuclear and two gas generators and a load. It is simulated over 30 hourly time steps from `2025-01-01 00:00:00`, with 10 scenarios: the yearly values therefore cover these 30 hours only. Values are rounded, and columns are shown in a fixed order for readability.

Extract of the hourly file (pattern `hourly`, one value per scenario):

| metric_id | metric_location | breakdown_properties | view_date | scenario_id | metric_value | scenario_aggregation | scenario_stat |
|---|---|---|---|---|---|---|---|
| PRODUCTION | area_fr | {} | 2025-01-01 04:00:00 | 0 | 437.15 | false | |
| PRODUCTION | France | {} | 2025-01-01 04:00:00 | 0 | 437.15 | false | |
| PRODUCTION_BY_TECH_AND_COMPANY | area_fr | {(technology,gas),(company,rhonepower)} | 2025-01-01 04:00:00 | 0 | 0.0 | false | |
| PRODUCTION_BY_TECH_AND_COMPANY | area_fr | {(technology,nuclear),(company,britishnuke)} | 2025-01-01 04:00:00 | 0 | 187.15 | false | |
| PRODUCTION_BY_TECH_AND_COMPANY | area_fr | {(technology,nuclear),(company,rhonepower)} | 2025-01-01 04:00:00 | 0 | 250.0 | false | |

Extract of the yearly file (pattern `yearly_stats`, statistics across scenarios):

| metric_id | metric_location | breakdown_properties | view_date | scenario_id | metric_value | scenario_aggregation | scenario_stat |
|---|---|---|---|---|---|---|---|
| PRODUCTION | area_fr | {} | 2025-01-01 00:00:00 | | 14557.952 | true | exp |
| PRODUCTION | area_fr | {} | 2025-01-01 00:00:00 | | 1249.679 | true | std |
| PRODUCTION | area_fr | {} | 2025-01-01 00:00:00 | | 12194.6 | true | min |
| PRODUCTION | area_fr | {} | 2025-01-01 00:00:00 | | 17297.17 | true | max |
