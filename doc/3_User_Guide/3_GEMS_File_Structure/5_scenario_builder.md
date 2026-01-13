<div style="display: flex; justify-content: space-between; align-items: center;">
  <div style="text-align: left;">
    <a href="../../../..">Main Section</a>
  </div>
  <div style="text-align: right;">
    <img src="../../../assets/gemsV2.png" alt="GEMS Logo" width="150"/>
  </div>
</div>

# Scenario Builder

The `modeler-scenariobuilder.dat` file, located in the `data-series` directory, is used to map simulation scenarios to data series. Each line defines an association between a **group name** and a **Monte Carlo year** (referred to as *year*) with a **data series identifier** (referred to as *time series number*).

## Purpose

The scenario builder associates:

- **scenario group ID**
- **Monte Carlo year** (referred to as *year*)
- **time series index**

allowing the model to select which data series column is used for a given scenario group and simulation scenario.

## File Format

Each line in the `modeler-scenariobuilder.dat` file defines a single mapping using the following format:

```text
scenario_group_id, scenario = time_series_index
```


## Example

```text
thermal_group, 0 = 1
thermal_group, 1 = 5
hydro_group, 2 = 7
```



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