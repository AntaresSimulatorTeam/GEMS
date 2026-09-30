# Taxonomy

The **Taxonomy** defines a shared classification of GEMS models. It is used to organize models by users' needs. If a [model](library.md#models) in a [library](library.md) declares a `taxonomy-category` (for example `production` or `balance`), it should then comply with the expected parameters, variables, constraints, properties, ports and extra-outputs of its category. On the contrary, additional features in the model (not declared in the taxonomy-category) are allowed.

This classification is "transparent" and doesn't impact the optimization solution: it is only used for the building of Views and to standardize graphical interfaces.

???+ info "Link to `catalog.yml` and `view-config.yml`"
    The taxonomy is notably used by `catalog.yml` to define **Metrics** ; taxonomy categories serve as interface with [Models](library.md#models), to specify the variables, extra-outputs or ports that are expected by the Catalog for the computation of each Metric. See [Views](../outputs/views.md) for more details.

    Both the [Catalog files](catalog.md) and the [View Configuration file](view-config.md) reference the taxonomy by its `id`: it must match the `id` of the taxonomy file.

???+ warning "Every model used in the system needs a `taxonomy-category`"
    To build Views, each component of the [system](system.md) is attached to the `taxonomy-category` of its model. Models without a `taxonomy-category` cannot be used to build Views.

    The building of Views does not check that models comply with their category: only the [Catalog](catalog.md) terms are checked against the taxonomy. A model's `taxonomy-category` should therefore be a category of the taxonomy file.

## Key elements in taxonomy file

The taxonomy file has a single root key `taxonomy`. Unknown keys under `taxonomy` are rejected.

| Element | Type | Description |
|------|------|--------------------------|
| `taxonomy.id` | String | A unique identifier for the taxonomy.|
| `taxonomy.description` | String | *(Optional)* A human-readable description of the taxonomy.|
| `taxonomy.categories` | List | *(Optional)* The list of [categories](#categories) of the taxonomy.|

### Categories

Each category lists the elements expected from the models declaring it. Each element of these lists is given by its `id` (`- id: <element_id>`).

| Element | Type | Description |
|------|------|--------------------------|
| `id` | String | A unique identifier for the category.|
| `parent-category` | String | *(Optional)* The `id` of a parent category. It is currently informative only: a category does **not** inherit the elements of its parent, so all the elements needed by the catalog must be declared on the category itself.|
| `variables` | List | *(Optional)* The [variables](library.md#variables) that models in this category must declare.|
| `parameters` | List | *(Optional)* The [parameters](library.md#parameters) that models in this category must declare.|
| `ports` | List | *(Optional)* The [ports](library.md#ports) on which metrics can be located for this category. It has to be the same port names as declared in the [library](library.md) [models](library.md#models).|
| `constraints` | List | *(Optional)* The [constraints](library.md#constraints) that models in this category must declare.|
| `extra-outputs` | List | *(Optional)* The [extra-outputs](library.md#extra-output) that models in this category must declare.|
| `properties` | List | *(Optional)* The [properties](library.md#properties) that models in this category must declare. They can be used by catalogs to [filter or break down](catalog.md#2-metrics-definition) metrics.|

???+ info "What the Catalog can use"
    In a [Catalog](catalog.md) term using a given category:

    - `output-id` must be one of the category's `variables` or `extra-outputs` ;
    - `location-port` must be one of the category's `ports`.

## Example

Each category matches the `taxonomy-category` declared on the corresponding model in the library.

```yaml
taxonomy:
  id: my_taxonomy
  description: Example taxonomy

  categories:

    - id: balance
      variables:
        - id: unsupplied_energy
        - id: spillage
      ports:
        - id: balance_port
      constraints:
        - id: balance
      parameters:
        - id: unsupplied_energy_cost
        - id: spillage_cost

    - id: production
      parameters:
        - id: p_max
        - id: cost
      variables:
        - id: generation
      ports:
        - id: balance_port
      properties:
        - id: company
        - id: technology

    - id: consumption
      parameters:
        - id: load
      ports:
        - id: balance_port
      extra-outputs:
        - id: effective_load
```
