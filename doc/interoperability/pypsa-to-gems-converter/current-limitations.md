# Current Limitations of the Converter

We explicit here the **current** limitation of the PyPSA-to-GEMS converter, that are related to the current state of development of the converter. We foresee no limitations in terms of the expressiveness of the GEMS modelling language.

## Unsupported PyPSA Components

- Transformers (not implemented)

## Component Restrictions

### Generators

- **`active = 1`** - All generators are included in the optimization.
- **`marginal_cost_quadratic = 0`** - Only linear generation costs are supported.
- **`committable = False`** - Unit commitment (on/off decisions) is not supported.

### Loads

- **`active = 1`** - All loads are fixed and always active.

### Links

- **`active = 1`** - All links are always active.

### Storage Units

- **`active = 1`** - All storage units are included in the optimization.
- **`sign = 1`** - Storage operates with positive dispatch direction.
- **`cyclic_state_of_charge = 1`** - End state of charge must equal the initial state.
- **`marginal_cost_quadratic = 0`** - Only linear storage costs are supported.

### Stores

- **`active = 1`** - All stores are included in the optimization.
- **`sign = 1`** - Store energy flows are positive.
- **`e_cyclic = 1`** - End energy level must equal the initial level.
- **`marginal_cost_quadratic = 0`** - Only linear storage costs are supported.

### Global Constraints

- **`type = primary_energy`** - Only primary energy constraints are supported.
- **`carrier.co2_emissions`** - CO₂ accounting must be defined at the carrier level.
- **Supported senses:** `<=`, `==`
