<div style="display: flex; justify-content: flex-end;">
  <a href="../..">
    <img src="../../../assets/gemsV2.png" alt="GEMS Logo" width="150"/>
  </a>
</div>

# Hybrid connections: coupling GEMS Components with Legacy Areas

In a **hybrid study**, a `area-connection` between a GEMS component and a Legacy Area means that the component contributes to the energy balance at the given node, through a given port (field).

In practical terms, connecting a GEMS **Generator** component to an Antares Legacy Area injects the generator's power output into that area's balance equation (the supply-demand constraint). *Without this connection, the GEMS component would remain isolated*.

The following steps describe how to **link the GEMS part of the study to the Legacy part**:

## Abstract definition of the area-connection field type (in the [library](../../3_User_Guide/3_GEMS_File_Structure/2_library.md) file)

In order to successfully inject a GEMS component's port into an Antares Legacy Area, the port's type must declare which field will contribute to the optimization problem. This is configured in the [library](../../3_User_Guide/3_GEMS_File_Structure/2_library.md) of the component's model (e.g. a file `model-libraries/library.yml`). 

The `area-connection` section is optional in general, but becomes mandatory when the port type is intended to be used in a **hybrid study**. It can accept 3 types of fields `injection-to-balance`, `spillage-bound` and `unsupplied-energy-bound` :

```yaml
port-types:
   - id: port-to-area
     fields:
        - id: field_to_balance
        - id: to-area-bound
        - id: from-area-bound
     area-connection:
        injection-to-balance: field_to_balance
        spillage-bound: to-area-bound
        unsupplied-energy-bound: from-area-bound
```

The nature of the contribution depends on the fields:

- `injection-to-balance`: the linear expression is injected in the balance constraint of the Legacy Area.
- `spillage-bound`: the linear expression is added to the sum of all variables or linear expressions already used to bound the spillage in the constraint called "fictitious load" in the Legacy Area.
- `unsupplied-energy-bound`: the linear expression is added to any linear expression already used to bound the unsupplied energy in the Legacy Area.

These fields are independent: you don't have to define all 3 at the same time, you can define only one. However, all three keys must be present in the `area-connection` section even if some values are left empty.

## Conventions on the sign of expressions

When connecting a component to an area, you must respect conventions on the sign of the linear expression contributed by the port field.


| Area Connecton Field | Sign Convention: Positive for... |
|---|---|
| injection-to-balance | Production |
| spillage-bound | Production |
| unsupplied-energy-bound | Load |


<details>
<summary>Sign conventions for the <code>injection-to-balance</code></summary>

<ul>
  <li>If you need to involve a <strong>production</strong>, make the expression <strong>positive</strong> (no <code>-</code> prefix):
<pre><code class="language-yaml">port-field-definitions:
  - port: balance_port
    field: flow_field
    definition: flat_production   # positive production
</code></pre>
  </li>
  <li>If you need to involve a <strong>load</strong>, make the expression <strong>negative</strong> (prefix with <code>-</code>):
<pre><code class="language-yaml">port-field-definitions:
  - port: balance_port
    field: flow_field
    definition: -flat_load   # negative load
</code></pre>
  </li>
</ul>

</details>

<details>
<summary>Sign conventions for the <code>spillage-bound</code></summary>

<p>This connection is intended to limit the spillage optimization variable. The convention is the same as for the balance constraint: make the <strong>production positive</strong>, with no <code>-</code> prefix:</p>

<pre><code class="language-yaml">port-field-definitions:
  - port: spillage_port
    field: to-area-bound
    definition: flat_production   # positive production
</code></pre>

</details>

<details>
<summary>Sign conventions for the <code>unsupplied-energy-bound</code></summary>

<p>This connection is intended to limit the unsupplied energy optimization variable. Here, make the <strong>load positive</strong>, with no <code>-</code> prefix:</p>

<pre><code class="language-yaml">port-field-definitions:
  - port: unsup_energy_port
    field: from-area-bound
    definition: flat_load   # positive load
</code></pre>

</details>

## Definition of the area-connections (in the [system](../../3_User_Guide/3_GEMS_File_Structure/3_system.md) file)

The `area-connections` section of the system file is used to declare each connection between a GEMS component and an Antares Legacy Area.

For every component that should supply or interact with an Antares Area, an entry is added specifying the component, the port through which it connects, and the target area name. The port must belong to a port type that defines an `area-connection` section in the model library. For example, to connect a component `wind_farm` to a legacy area `area1` through `wind_farm`'s port named `balance_port`, the following configuration is used:

```yaml
area-connections:
  - component: wind_farm
    port: balance_port
    area: area1
```

Explanation of fields:

- **component:** Refers to the `id` of the GEMS component to be connected. This `id` must match the one declared in the components section of the `system.yml` file. In this example, it refers to a component named `wind_farm`
- **port:** Specifies which port on the component is used to establish the connection to the Antares Simulator area. The corresponding **port type** must include an `area-connection` section in the model library definition, and must specify at least one of `injection-to-balance`, `spillage-bound` or `unsupplied-energy-bound`
- **area:** Indicates the target Antares Simulator area. The component's output, through the defined port, will contribute to this Antares Simulator area's balance constraint during simulation
