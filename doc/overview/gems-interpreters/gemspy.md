# GemsPy Presentation

[GemsPy](https://gemspy.readthedocs.io/en/latest/) is a stand-alone Python package to interpret the language GEMS. GemsPy is under active development.

## GemsPy API Overview

GemsPy's API allows users to create studies programmatically.

For detailed API usage and examples, see:

- [Installation Guide](../../getting-started/installation/gemspy-installation.md)
- In the [Examples section](../../examples/overview-examples.md), it is explained how simulations can be run with GemsPy.
- [Building with GemsPy API](https://gemspy.readthedocs.io/en/latest/user-guide/building/)

## Package Structure

Since v0.1.3, GemsPy is divided into two sub-packages :

| Sub-package | Role |
|---|---|
| `gems_craft` | Create and read studies |
| `gems_runner` | Run studies |

!!! warning
    The legacy `gems.*` import path (e.g. `from gems.study.parsing import ...`) is no longer valid as of GemsPy v0.1.3.
    Always use `gems_craft.*` or `gems_runner.*` depending on the operation.

    === "<v0.1.3"
        ```python
        # Invalid with v0.1.3+
        from gems.study.parsing import ComponentSchema
        from gems.model.parsing import parse_yaml_library
        from gems.model.resolve_library import resolve_library

        from gems.session.session import SimulationSession
        ```
    === "v0.1.3+"
        ```python
        # Adapted to v0.1.3+
        from gems_craft.study.parsing import ComponentSchema
        from gems_craft.model.parsing import parse_yaml_library
        from gems_craft.model.resolve_library import resolve_library

        from gems_runner.session.session import SimulationSession
        ```
