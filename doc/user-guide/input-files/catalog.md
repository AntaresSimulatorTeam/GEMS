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

This is a partial excerpt from the [test_3 catalog](https://github.com/AntaresSimulatorTeam/GEMS-ViewsBuilder/blob/main/resources/test_inputs/test_3/catalogs/catalog.yml) in the GEMS-ViewsBuilder repository.

```yaml
catalog:
  id: test_example_pypsa
  taxonomy: my_taxonomy

  location:
    taxonomy-category: balance

  metrics-definition:

    - id: PROD
      terms:
        - taxonomy-category: production
          output-id: p
          location-ports: p_balance_port
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
