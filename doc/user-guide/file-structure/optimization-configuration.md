# Optimization Configuration File

The `optim-config.yml` file defines the resolution strategy and execution scope of a GEMS study. It is placed at `input/optim-config.yml` inside the study directory.

This file is **optional**. If users don't mention it, default values apply and the study runs in frontal (single LP) mode over scenario `0`.

It controls:

- the **time scope** and **scenario scope** of the simulation
- the **solver** used to solve the optimisation problem
- the **resolution strategy**: how the optimisation horizon is decomposed (frontal, sequential blocks, parallel blocks, or Benders decomposition for investment studies)
- **per-model settings**: out-of-bounds time handling and decomposition assignment

The file is read by both the [Antares Modeler](../../overview/gems-interpreters/antares-simulator.md) and [GemsPy](../../overview/gems-interpreters/gemspy.md) interpreters.


## Example

Minimal configuration for a frontal simulation run:

```yaml
# Time range matching a typical weekly optimisation (168 h, 0-based)
first-time-step: 0
last-time-step: 167

# Run over 3 Monte Carlo scenarios
scenario-scope:
  include:
    - "0-2"

solver:
  name: highs
  logs: false

resolution-mode: frontal

# short_term_storage.level_equation references level[t-1].
# At t=0 that is out of bounds; cyclic wraps it to level[167],
# which is pinned by the library's initial_level_constraint.
models:
  - id: antares_legacy_models.short_term_storage
    out-of-bounds-processing:
      constraints:
        - id: level_equation
          mode: cyclic 
```
