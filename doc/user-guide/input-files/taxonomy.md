<div style="display: flex; justify-content: flex-end;">
    <a href="../../../..">
        <img src="../../../assets/gemsV2.png" alt="GEMS Logo" width="150"/>
    </a>
</div>

# Taxonomy

The **Taxonomy** defines a shared classification of GEMS models. It is used to organize models and components by users' needs. Each [model](library.md#models) in a [library](library.md) declares a `taxonomy-category` (for example `production` or `balance`) that maps it to one of the categories defined here. This classification is "transparent" and doesn't impact the optimization solution

???+ info "Link to `catalog.yml`"
    The taxonomy is used by `catalog.yml` in [GEMS-ViewsBuilder](https://github.com/AntaresSimulatorTeam/GEMS-ViewsBuilder) to define **metrics** for each `taxonomy-category`. See [Business Views](../outputs/business-view.md) for more details.

## Example

This is a partial excerpt from the [test_3 taxonomy](https://github.com/AntaresSimulatorTeam/GEMS-ViewsBuilder/blob/main/resources/test_inputs/test_3/taxonomy.yml) in the GEMS-ViewsBuilder repository.

```yaml
taxonomy:
  id: my_taxonomy
  description: Minimal taxonomy

  categories:
    - id: balance
      ports:
        - id: p_balance_port
        - id: q_balance_port
```

## Key elements in taxonomy file

| Element | Type | Description |
|------|------|--------------------------|
| `taxonomy.id` | String | A unique identifier for the taxonomy.|
| `taxonomy.description` | String | *(Optional)* A human-readable description of the taxonomy.|
| `categories.id` | String | A unique identifier for the category.|
| `categories.ports` | List | The [ports](library.md#ports) on which metrics can be computed for this category. It has to be the same port names as declared in the [library](library.md) [models](library.md#models).|