![Template Banner](../assets/template_banner.svg)
<div style="display: flex; justify-content: space-between; align-items: center;">
  <div style="text-align: left;">
    <a href="../../../..">Main Section</a>
  </div>
  <div style="text-align: right;">
    <img src="../../../assets/gemsV2.png" alt="GEMS Logo" width="150"/>
  </div>
</div>


# Hybrid studies

This page aims to explain how to run a study made with Modeler part and Legacy part with Antares Simulator.

# Definition

To define a hybrid study, it's a solver study, with modeler files and directories in the input directory.    
The parameter.yml file from modeler studies is not needed (if it exists, it will be ignored). The solver parameters are used, since hybrid studies are conducted using antares-solver

```
solver-study/
├── input/
│   ├── areas/
│   ├── bindingconstraints/
│   ├── ...
│   └── modeler-study/    <-- Modeler files go here
├── layers/
├── logs/
├── output/
├── settings/
├── user/
├── Desktop.ini
├── Logs.log
└── study.antares
```

# Running an hybrid study

## How to connect the modeler part and the solver part



---
**Navigation**
<div style="display: flex; justify-content: space-between;">
  <div style="text-align: left;">
  <button type="button" style="background-color:#CCCCCC; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
    <a href="../2_antares_legacy" style="text-decoration:none; color: #000000">⬅️ Previous page</a>
  </button>
  </div>
  <button type="button" style="background-color:#AAAAFF; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
    <a href="../../../.." style="text-decoration:none; color: #FFFFFF">Home</a>
  </button>
  <div style="text-align: right;">
  <button type="button" style="background-color:#CCCCCC; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
    <a href="../../5_Examples/1_optimization_problem" style="text-decoration:none; color: #000000">Next page ➡️</a>
  </button>
  </div>
</div>

---

© GEMS (LICENSE)