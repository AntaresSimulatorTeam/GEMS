<div style="display: flex; justify-content: flex-end;">
    <a href="../../../..">
        <img src="../../../assets/gemsV2.png" alt="GEMS Logo" width="150"/>
    </a>
</div>

# Catalog File

The **Catalog** file defines **Metrics**. Each metric aggregates [simulation outputs](../outputs/simulation-table.md) from components selected by their [`taxonomy-category`](taxonomy.md).

> Users can use **several catalog files** based on their needs.

???+ info "Links with `taxonomy.yml` and `view-config.yml`"
    Catalogs use the taxonomy categories defined in [`taxonomy.yml`](taxonomy.md).

    [`view-config.yml`](view-config.md) uses the metrics from catalogs to then produce [Business Views](../outputs/business-view.md).

## Example

This example uses the [Antares Legacy model library](https://github.com/AntaresSimulatorTeam/GEMS/blob/main/libraries/antares_legacy_models.yml) and its `antares_legacy_taxonomy`.

```yaml
catalog:
  id: antares_legacy_catalog
  taxonomy: antares_legacy_taxonomy

  location:
    taxonomy-category: balance

  metrics-definition:

    - id: PROD
      terms:
        - taxonomy-category: dispatchable_generation
          output-id: generation_power
          location-ports: balance_port
      terms-operator: sum
      time-operator: sum

    - id: LOAD
      terms:
        - taxonomy-category: fatal_consumption
          output-id: actual_load
          location-ports: balance_port
      terms-operator: sum
      time-operator: sum

    - id: INSTALLED_PROD_CAPACITY
      terms:
        - taxonomy-category: dispatchable_generation
          output-id: cluster_availability
          location-ports: balance_port
      terms-operator: sum
      time-operator: sum

    - id: BALANCE
      terms:
        - taxonomy-category: link
          output-id: flow
          location-ports: in_port
        - taxonomy-category: link
          output-id: minus_flow
          location-ports: out_port
      terms-operator: sum
      time-operator: sum
```

## Key elements in catalog file

Generalities:

*This first part configures the `catalog` file.*

| Element | Type | Description |
|------|------|--------------------------|
| `id` | String | A unique identifier for the catalog.|
| `taxonomy` | String | The `id` of the [taxonomy](taxonomy.md) this catalog uses.|
| `location.taxonomy-category` | String | The [taxonomy category](taxonomy.md) whose components serve as location objects (e.g. buses or areas).|

Metrics definition:

*This second part defines the metrics.*

| Element | Type | Description |
|------|------|--------------------------|
| `id` | String | A unique identifier for the metric.|
| `terms` | List | List of terms contributing to the metric. Each term selects a component group by [`taxonomy-category`](taxonomy.md), an `output-id` (referencing a [model output](library.md#extra-output)) and the [`location-ports`](taxonomy.md#key-elements-in-taxonomy-file) through which it connects to the location.|
| `terms-operator` | String | How to combine values across components: `sum` or `avg`.|
| `time-operator` | String | How to aggregate values over time: `sum` or `avg`.|
