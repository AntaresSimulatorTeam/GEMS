# Catalog Files

GEMS lets the users the possibility to configure its own outputs. The outputs are defined by **Metrics** specified inside the **Catalog** file. Each metric aggregates [simulation outputs](../outputs/simulation-table.md) from components selected by their [`taxonomy-category`](taxonomy.md).

> Users can use **several catalog files** based on their needs.

???+ info "Links with `taxonomy.yml` and `view-config.yml`"
    Catalogs use the taxonomy categories defined in [a taxonomy file](taxonomy.md).

    [`view-config.yml`](view-config.md) uses the metrics from catalogs to then produce [Views](../outputs/business-view.md).

## Structure of `catalog` files

### 1. `catalog` header

*This first part configures the `catalog` file.*

| Element | Type | Description |
|------|------|--------------------------|
| `catalog.id` | String | A unique identifier for the catalog.|
| `catalog.taxonomy` | String | The `id` of the [taxonomy](taxonomy.md) this catalog uses.|
| `catalog.location.taxonomy-category` | String | The [taxonomy category](taxonomy.md) whose components serve as location objects for the View (e.g. buses/areas, links, generators...).|

### 2. Metrics definition

*This second part defines the metrics.*

| Element | Type | Description |
|------|------|--------------------------|
| `metrics-definition.id` | String | A unique identifier for the metric.|
| `metrics-definition.terms` | List | List of [terms](#3-terms) contributing to the metric.|
| `metrics-definition.terms-operator` | String | How to combine values across components: `sum` or `avg`.|
| `metrics-definition.time-operator` | String | How to aggregate values over time: `sum` or `avg`.|

#### 3. Terms

*This third section focuses on the terms definition*

Each term in `metrics-definition.terms` selects a group of components defined by the `taxonomy` file and a simulation output to aggregate into the metric.

| Element | Type | Description |
|------|------|--------------------------|
| `taxonomy-category` | String | The [`taxonomy-category`](taxonomy.md) identifying the group of components to aggregate.|
| `output-id` | String | The identifier of the [model output](library.md#extra-output) to read from those components.|
| `location-port` | String | The [`location-port`](taxonomy.md#key-elements-in-taxonomy-file) through which the selected components connect to the metric location.|

## Example

This example uses the [Antares Legacy Models library](https://github.com/AntaresSimulatorTeam/GEMS/blob/main/libraries/antares_legacy_models.yml) and its taxonomy `antares_legacy_taxonomy.yml`.

```yaml
catalog:
  id: antares_legacy_catalog
  taxonomy: antares_legacy_taxonomy

  location:
    taxonomy-category: balance

  metrics-definition:

    - id: PROD
      terms:
        - taxonomy-category: generation
          output-id: generation_power
          location-ports: balance_port
      terms-operator: sum
      time-operator: sum

    - id: PRICE
      terms:
        - taxonomy-category: balance
          output-id: price
          location-ports: balance_port
      terms-operator: avg
      time-operator: avg
```
