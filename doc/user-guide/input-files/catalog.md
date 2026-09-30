# Catalog Files

GEMS lets users configure their own outputs. The outputs are defined by **Metrics** specified inside the **Catalog** file. Each metric aggregates [simulation outputs](../outputs/simulation-table.md) from components selected by their [`taxonomy-category`](taxonomy.md).

> Users can use **several catalog files** based on their needs. All catalog files are placed in a single catalogs directory, which must only contain `.yml` files, and each file must be named after its `id` (`<catalog_id>.yml`).

???+ info "Links with `taxonomy.yml` and `view-config.yml`"
    Catalogs use the taxonomy categories defined in [a taxonomy file](taxonomy.md).

    [`view-config.yml`](view-config.md) uses the metrics from catalogs to then produce [Views](../outputs/views.md). The `taxonomy` and `location.taxonomy-category` of each catalog used by a View must match the ones of the [View Configuration file](view-config.md).

## Structure of `catalog` files

The catalog file has a single root key `catalog`. Unknown keys are rejected.

### 1. `catalog` header

*This first part configures the `catalog` file.*

| Element | Type | Description |
|------|------|--------------------------|
| `catalog.id` | String | A unique identifier for the catalog. It must match the file name (`<id>.yml`) and must not contain a `.`.|
| `catalog.taxonomy` | String | The `id` of the [taxonomy](taxonomy.md) this catalog uses.|
| `catalog.location.taxonomy-category` | String | The [taxonomy category](taxonomy.md) whose components serve as location objects for the metrics (e.g. buses/areas, links, generators...).|

### 2. Metrics definition

*This second part defines the metrics, listed under `catalog.metrics-definition`.*

| Element | Type | Description |
|------|------|--------------------------|
| `id` | String | A unique identifier for the metric within the catalog. It must not contain a `.`.|
| `terms` | List | List of [terms](#3-terms) contributing to the metric.|
| `terms-operator` | String | How to combine values across contributing components of all terms (for a given location, time step and scenario): `sum` or `avg`.|
| `time-operator` | String | How to aggregate values over time, up to the time granularity requested in the [View Configuration file](view-config.md#aggregation-patterns): `sum` or `avg`.|
| `breakdown` | List | *(Optional)* List of component [properties](library.md#properties) (as set in the [system](system.md)) used to split the metric, each given by its `key` (`- key: technology`). The values of these properties on the contributing components are written in the `breakdown_properties` column of the [Views](../outputs/views.md) (e.g. `{(technology,nuclear),(company,A)}`). A component that does not have the property gets the value `None`.|
| `filter` | Object | *(Optional)* A single component [property](library.md#properties) condition, given by a `key` and a `value`. Only the contributing components whose property `key` is equal to `value` are kept for the metric. `value` is mandatory and is a string: quote numbers or booleans (e.g. `value: "1"`).|

#### 3. Terms

*This third section focuses on the terms definition.*

Each term in `terms` selects a group of components defined by the `taxonomy` file and a simulation output to aggregate into the metric.

| Element | Type | Description |
|------|------|--------------------------|
| `taxonomy-category` | String | The [`taxonomy-category`](taxonomy.md) identifying the group of components to aggregate. It must be defined in the taxonomy.|
| `output-id` | String | The identifier of the output to read from those components. It must be declared as a `variable` or an `extra-output` of the [taxonomy category](taxonomy.md#categories).|
| `location-port` | String/null | The [port](taxonomy.md#categories) that connects each contributing component to its location, i.e. a component of the `catalog.location.taxonomy-category`. It must be declared as a `port` of the taxonomy category, and each contributing component must be connected through this port to exactly one location component, otherwise the View building fails. If `null`, each contributing component is its own location (self-reference): the term `taxonomy-category` must then be the location taxonomy category.|
| `weight-output-id` | String | *(Optional)* Reserved for weighted aggregation. It is accepted but not used yet: all terms currently have a weight of 1.|

???+ warning "`location-port` is required"
    `location-port` must always be written in each term, even for a self-referencing term (`location-port: null`). An empty string is not allowed.

## Example

This example uses the taxonomy `my_taxonomy` defined in the [taxonomy page](taxonomy.md#example). The catalog file is named `catalog.yml`.

```yaml
catalog:
  id: catalog
  taxonomy: my_taxonomy

  location:
    taxonomy-category: balance

  metrics-definition:

    - id: LOAD
      terms:
        - taxonomy-category: consumption
          output-id: effective_load
          location-port: balance_port
      terms-operator: sum
      time-operator: sum

    - id: PRODUCTION
      terms:
        - taxonomy-category: production
          output-id: generation
          location-port: balance_port
      terms-operator: sum
      time-operator: sum

    - id: PRODUCTION_BY_TECH_AND_COMPANY
      terms:
        - taxonomy-category: production
          output-id: generation
          location-port: balance_port
      terms-operator: sum
      time-operator: sum
      breakdown:
        - key: technology
        - key: company

    - id: NUCLEAR_PRODUCTION
      terms:
        - taxonomy-category: production
          output-id: generation
          location-port: balance_port
      terms-operator: sum
      time-operator: sum
      filter:
        key: technology
        value: nuclear

    - id: UNSUPPLIED_ENERGY
      terms:
        - taxonomy-category: balance
          output-id: unsupplied_energy
          location-port: null
      terms-operator: sum
      time-operator: sum
```
