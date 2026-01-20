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

A connection must be established between the GEMS component and the Legacy area on which the component refers to.

The following steps describe how to connect the modeler-study (GEMS framework) with the solver-study (Legacy framework):

### Define the connections (in the system.yml file)

The connection between GEMS component `generator1` and Legacy area `area1` needs to be defined through the **system.yml** file in the `area-connections` section :

```yaml
area-connections:
 - component: generator1  # the ID of the component to connect to the area, as defined in the components section
  port: injection        # the ID of the component's port to connect to the area. This port must be of a type that defines an area-connection injection field.
  area: area1            # the ID of the area to connect the component to, as defined in the antares-solver input files
 - component: generator2
   port: injection
   area: area1
```
### Define the are-connection fieds (in the library.yml file)

As it mentions above, the port field needs to be defined in order to specify what data will be exchange between the component and the area.

This area-connection field is defined inside the port type definition inside the library file:

```yaml 
port-type:
  id: ac_link
  fields:
    - id: flow
    - id: angle
  # area-connection is the name of the optional section to use.
  # It is mandatory if you want to use such a port type to connect modeler components to solver areas.
  area-connection:
    # injection-field: the field to use when adding the contribution of this port bearer to a connected area
    - injection-field: flow
```


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