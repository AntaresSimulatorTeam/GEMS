<div style="display: flex; justify-content: flex-end;">
  <a href="../../../..">
    <img src="../../../assets/gemsV2.png" alt="GEMS Logo" width="150"/>
  </a>
</div>

# GemsPy

[GemsPy](https://gemspy.readthedocs.io/en/latest/) is a Python interpreter for GEMS that allows you to create, manipulate, and simulate energy system models.

## Requirements

This package requires:

- **Python 3.10+**

## GemsPy installation

You can [GemsPy](https://github.com/AntaresSimulatorTeam/GemsPy) by using `pip` installation :

```bash
# Install GemsPy package
pip install gemspy
```

## Virtual Environment Setup

It is recommended to create a **virtual environment** before installing [GemsPy](https://github.com/AntaresSimulatorTeam/GemsPy). This provides a dedicated space with its own libraries, avoiding dependency conflicts and maintaining a clean global Python environment. All required dependencies will be installed automatically within your virtual environment when you run the installation command.

### Create and Set Up the Virtual Environment

| Step                        | Windows Command                              | macOS/Linux Command                        |
|-----------------------------|----------------------------------------------|--------------------------------------------|
| Create virtual environment  | `python -m venv gemspy-env`                  | `python3 -m venv gemspy-env`               |
| Activate environment        | `gemspy-env\Scripts\activate`               | `source gemspy-env/bin/activate`           |
| Clone GemsPy repository     | `pip install gemspy`          | `pip install gemspy`          |

### Working with Virtual Environments

1. **Activate the Virtual Environment**

    While working with GemsPy, activate the virtual environment:

    - **Windows:**
      ```
      gemspy-env\Scripts\activate
      ```
    - **macOS/Linux:**
      ```
      source gemspy-env/bin/activate
      ```

    When activated, the environment name will be visible in the terminal prompt:

    ```
    (gemspy-env) user@machine:~$
    ```

2. **Deactivate the Environment**

    Before working on another project, deactivate the environment:
    ```
    deactivate
    ```

3. **Delete the Virtual Environment**

    If you need to completely remove a virtual environment:
    - Make sure it is deactivated first.
    - Delete the `gemspy-env` folder directly.

    **Note:** Ensure you have saved any important work before deleting the environment.

## Additional Resources

| Resource              | Link                                                                 |
|-----------------------|----------------------------------------------------------------------|
| GitHub Repository     | [GemsPy on GitHub](https://github.com/AntaresSimulatorTeam/GemsPy)   |
| Online Documentation  | [gemspy.readthedocs.io](https://gemspy.readthedocs.io)               |
| Examples              | See the repository's `examples/` directory                           |
| FAQ                   | [FAQ](../../support/faq.md)                      |
| GitHub Issues         | [GemsPy Issues](https://github.com/AntaresSimulatorTeam/GemsPy/issues)|
| Contact Support       | [Contact support](../../support/contact.md)      |