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

This example uses the [Antares Legacy model library](https://github.com/AntaresSimulatorTeam/GEMS/blob/main/libraries/antares_legacy_models.yml). Each category matches the `taxonomy-category` declared on the corresponding model in the library.

```yaml
taxonomy:
  id: antares_legacy_taxonomy
  description: Taxonomy for the Antares Legacy model library

  categories:
    - id: balance
      ports:
        - id: balance_port

    - id: fatal_consumption
      ports:
        - id: balance_port

    - id: dispatchable_generation
      ports:
        - id: balance_port

    - id: renewable_fatal_generation
      ports:
        - id: balance_port

    - id: miscellaneous_fatal_generation
      ports:
        - id: balance_port

    - id: short_term_storage
      ports:
        - id: balance_port

    - id: long_term_storage
      ports:
        - id: balance_port

    - id: link
      ports:
        - id: out_port
        - id: in_port
```

## Key elements in taxonomy file

| Element | Type | Description |
|------|------|--------------------------|
| `taxonomy.id` | String | A unique identifier for the taxonomy.|
| `taxonomy.description` | String | *(Optional)* A human-readable description of the taxonomy.|
| `categories.id` | String | A unique identifier for the category.|
| `categories.ports` | List | The [ports](library.md#ports) on which metrics can be computed for this category. It has to be the same port names as declared in the [library](library.md) [models](library.md#models).|