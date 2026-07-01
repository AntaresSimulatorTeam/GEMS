<div style="display: flex; justify-content: flex-end;">
    <a href="../../../..">
        <img src="../../../assets/gemsV2.png" alt="GEMS Logo" width="150"/>
    </a>
</div>

# Catalog File

The **Catalog** file defines **Metrics**. Each metric aggregates simulation outputs from components selected by their [`taxonomy-category`](taxonomy.md). 

> Users can use **several catalog files** based on its needs

???+ idea "Links with `taxonomy.yml` and `views-config.yml`"
    Catalogs uses the taxonomy-ctagories defind inside [`taxonomy.yml`](taxonomy.md)

    [`views-config.yml`](view-config.md) uses the metrics from catlogs to then produce [Views](../outputs/business-view.md).

## Example

This is a partial excerpt from the [test_3 catalog](https://github.com/AntaresSimulatorTeam/GEMS-ViewsBuilder/blob/main/resources/test_inputs/test_3/catalogs/yml) in the GEMS-ViewsBuilder repo.

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

Generalities :

*This first part configures the `catalog` file*

| Element | Type | Description |
|------|------|--------------------------|
| `id` | String | A unique identifier for the |
| `taxonomy` | String | The `id` of the [taxonomy](taxonomy.md) this catalog used.|
| `location.taxonomy-category` | String | The [taxonomy category](taxonomy.md) whose components serve as location objects.|

Metrics definition :

*This second part defines the metrics*

| Element | Type | Description |
|------|------|--------------------------|
| `id` | String | A unique identifier for the metric.|
| `terms` | List | List of terms contributing to the metric. Each term selects a component group by `taxonomy-category`, an `output-id` and the `location-ports`.|
| `terms-operator` | String | How to combine values across components: `sum` or `avg`.|
| `time-operator` | String | How to aggregate values over time: `sum` or `avg`.|
