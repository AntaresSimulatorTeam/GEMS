# Taxonomy

The **Taxonomy** defines a shared classification of GEMS models. It is used to organize models by users' needs. If a [model](library.md#models) in a [library](library.md) declares a `taxonomy-category` (for example `production` or `balance`), it should then comply with the expected parameters, variables, properties, ports and extra-outputs of its category. On the contrary, additional features in the model (not declared in the taxonomy-category) are allowed. 

This classification is "transparent" and doesn't impact the optimization solution: it is only used for the building of Views and to standardize graphical interfaces.

???+ info "Link to `catalog.yml`"
    The taxonomy is notably used by `catalog.yml` to define **Metrics** ; taxonomy categories serve as interface with [Models](library.md#models), to specify the variables, properties, extra-outputs or ports that are expected by the Catalog for the computation of each Metric. See [Views](../outputs/views.md) for more details.

## Key elements in taxonomy file

| Element | Type | Description |
|------|------|--------------------------|
| `taxonomy.id` | String | A unique identifier for the taxonomy.|
| `taxonomy.description` | String | *(Optional)* A human-readable description of the taxonomy.|
| `categories.id` | String | A unique identifier for the category.|
| `categories.variables` | List | *(Optional)* The [variables](library.md#variables) that models in this category must declare.|
| `categories.parameters` | List | *(Optional)* The [parameters](library.md#parameters) that models in this category must declare.|
| `categories.ports` | List | *(Optional)* The [ports](library.md#ports) on which metrics can be computed for this category. It has to be the same port names as declared in the [library](library.md) [models](library.md#models).|
| `categories.extra-outputs` | List | *(Optional)* The [extra-outputs](library.md#extra-outputs) that models in this category must declare.|
| `categories.properties` | List | *(Optional)* The [properties](library.md#properties) that models in this category must declare.|

## Example

This example uses the [Antares Legacy model library](https://github.com/AntaresSimulatorTeam/GEMS/blob/main/libraries/antares_legacy_models.yml). Each category matches the `taxonomy-category` declared on the corresponding model in the library.

```yaml
taxonomy:
  id: antares_legacy_taxonomy
  description: GEMS taxonomy configuration for Antares Legacy Models.
  categories:

    - id: balance
      variables:
        - id: unsupplied_energy
        - id: spilled_energy
      ports:
        - id: balance_port
      binding-constraints:
        - id: balance
      extra-outputs:
        - id: price
        - id: imbalance_cost
        - id: is_loss_of_load
        - id: is_significant_loss_of_load
        - id: is_near_loss_of_load

    - id: generation
      ports:
        - id: balance_port
```