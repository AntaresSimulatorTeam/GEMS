<div style="display: flex; justify-content: space-between; align-items: center;">
  <div style="text-align: left;">
    <a href="../../index.md">Main Section</a>
  </div>
  <div style="text-align: right;">
    <img src="../../../assets/gemsV2.png" alt="GEMS Logo" width="150"/>
  </div>
</div>


# Classification of Models (Taxonomy)

GEMS provides the functionality to use a classification of models defined via the configuration file, `taxonomy.yml`. 
The `taxonomy.yml` file defines categories of models and serves multiple utilities:

- The taxonomy defines **mandatory requirements** for models belonging to a specific category, such as **parameters, variables, ports, and extra-outputs**.

- This method avoids duplication and uniformization of similar models.

- In this scheme, there are two categories defined inside the taxonomy file, and one model was configured. In this model, 2 parameters and 1 variable are in fact directly configured by the taxonomy file.


![Taxonomy scheme](../../assets/6_taxonomy.png)


# Configuration of Output Files

With these configurations files, users can define specified results from raw optimization problem outputs:

- **`business_metrics.yml`**: Configures the metrics displayed in business views.
- **`business_view.yml`**: Allows users to select the export format of these chosen outputs.

---
**Navigation**
<div style="display: flex; justify-content: space-between;">
  <div style="text-align: left;">
  <button type="button" style="background-color:#CCCCCC; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
    <a href="../GEMS Interpreters/2_antares_simulator_modeler.md" style="text-decoration:none; color: #000000">⬅️ Previous page</a>
  </button>
  </div>
  <button type="button" style="background-color:#AAAAFF; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
    <a href="../../index.md" style="text-decoration:none; color: #FFFFFF">Index</a>
  </button>
  <div style="text-align: right;">
  <button type="button" style="background-color:#CCCCCC; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
    <a href="2_Libraries.md" style="text-decoration:none; color: #000000">Next page ➡️</a>
  </button>
  </div>
</div>

---

© GEMS (LICENSE)