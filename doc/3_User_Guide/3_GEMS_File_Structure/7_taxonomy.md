![Template Banner](../../assets/template_banner.svg)
<div style="display: flex; justify-content: space-between; align-items: center;">
  <div style="text-align: left;">
    <a href="../../../../..">Main Section</a>
  </div>
  <div style="text-align: right;">
    <img src="../../../assets/gemsV2.png" alt="GEMS Logo" width="150"/>
  </div>
</div>

# Taxonomy

The **taxonomy** defines a shared classification system used to organize models and components according to their functional role within the system. Each model declares a `taxonomy-group` (for example `production`, `consumption`, `storage`, or `balance`) that describes how its components participate in the overall system architecture. This classification is structural and descriptive, and does not define any calculations, constraints, or result aggregation by itself.  

**Intermediary Outputs** represent the detailed technical results produced directly by the simulation and optimization process. These outputs include decision variable values, evaluated port fields, extra outputs defined in models, and solver-related information such as objective values or dual variables. Intermediary Outputs should be stored in the `simulation_table`, which serves as the simulator’s internal memory across time blocks and scenarios.

## Example: Taxonomy Usage in a Model Definition

A simplified example of taxonomy usage in a model definition is shown below:

```yaml
models:
  - id: generator
    taxonomy-group: production
```

Example of catalog file:

```yaml
catalog:
  
  id: antares_area_output

  taxonomy: my_taxonomy

  location:
    taxonomy-group: balance

  metrics-definition: 

  - id: OV.COST
    terms:
      - taxonomy-group: balance
        output-id: imbalance_cost
        location-ports: null 
      - taxonomy-group: dispatchable_production
        output-id: proportional_cost
        location-ports: balance_port
      - taxonomy-group: dispatchable_production
        output-id: non_proportional_cost
        location-ports: balance_port
    terms-operator: sum
    time-operator: sum
```

**The taxonomy structure and the definition of Intermediary Outputs are still under active development.**

**Navigation**

<div style="display: flex; justify-content: space-between;">
  <div style="text-align: left;">
  <button type="button" style="background-color:#CCCCCC; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
    <a href="../../1_Overview/References/4_Users" style="text-decoration:none; color: #000000">⬅️ Previous page</a>
  </button>
  </div>
  <button type="button" style="background-color:#AAAAFF; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
    <a href="../../../.." style="text-decoration:none; color: #FFFFFF">Index</a>
  </button>
  <div style="text-align: right;">
  <button type="button" style="background-color:#CCCCCC; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
    <a href="../1B_gemspy_installation" style="text-decoration:none; color: #000000">Next page ➡️</a>
  </button>
  </div>
</div>

---


© GEMS (LICENSE)