<div style="display: flex; justify-content: space-between; align-items: center;">
  <div style="text-align: left;">
    <a href="../../index.md">Main Section</a>
  </div>
  <div style="text-align: right;">
    <img src="../assets/gemsV2.png" alt="GEMS Logo" width="150"/>
  </div>
</div>

# Installation
This section provides installation instructions for the different GEMS interpreters and tools available to work with GEMS studies.

## Available Interpreters
As mentioned in the Overview section, GEMS studies can be executed using different interpreters:
- **[GEMSPy](../1_Overview/GEMS%20Interpreters/1_gemspy.md)**
- **[Antares Modeler](../1_Overview/GEMS%20Interpreters/2_antares_simulator_modeler.md)**

The following documentation will explain how to install and use these interpreters for the first time.

---

# GEMSPy
GEMSPy is a Python interpreter for GEMS that allows you to create, manipulate, and simulate energy system models.

## Requirements
This package requires:
- **Python 3.11** (recommended for optimal compatibility and performance) or Python 3.8+
- Git (for cloning the GEMSPy repository)
- pip package manager (for installing required Python libraries)

## Installation from Source
Currently, GEMSPy must be installed by cloning the repository manually.

```bash
# Clone the repository
git clone https://github.com/AntaresSimulatorTeam/GemsPy.git
cd GemsPy
```

## Virtual Environment Setup
It is usually recommended to create a **virtual environment** before installing GEMSPy. A virtual environment provides a dedicated space with its own libraries, avoiding dependency conflicts and maintaining a clean global Python environment. All required dependencies will be installed automatically within your virtual environment when you run the installation command.

### Create and Set Up the Virtual Environment

| Step                        | Windows Command                              | macOS/Linux Command                        |
|-----------------------------|----------------------------------------------|--------------------------------------------|
| Create virtual environment  | `python -m venv gemspy-env`                  | `python3 -m venv gemspy-env`               |
| Activate environment        | `gemspy-env\Scripts\activate`               | `source gemspy-env/bin/activate`           |
| Clone GEMSPy repository     | `git clone https://github.com/AntaresSimulatorTeam/GemsPy.git` | `git clone https://github.com/AntaresSimulatorTeam/GemsPy.git` |
| Enter GEMSPy directory      | `cd GemsPy`                                  | `cd GemsPy`                                |
| Install GEMSPy requirements | `pip install -r requirements.txt`            | `pip install -r requirements.txt`          |

**Main dependencies installed via `requirements.txt`:**
- numpy
- pandas
- scipy

---

### Work with Virtual Environments

1. **Activate the Virtual Environment**
   While working with GEMSPy, activate the virtual environment:

   **Windows:**
   ```bash
   gemspy-env\Scripts\activate
   ```

   **macOS/Linux:**
   ```bash
   source gemspy-env/bin/activate
   ```

   When activated, the environment name will be visible in the terminal prompt:
   ```bash
   (gemspy-env) user@machine:~\$
   ```

   The virtual environment is now ready to be used.

2. **Deactivating Your Environment**
   Before working on another project, deactivate the environment:
   ```bash
   deactivate
   ```

3. **Deleting a Virtual Environment**
   If you need to completely remove a virtual environment:
   - Make sure it is deactivated first.
   - Delete the `gemspy-env` folder directly.

   **Note:** Ensure you have saved any important work before deleting the environment.

## Troubleshooting
If you encounter issues during installation:
- Ensure Python 3.11 or 3.8+ is installed 
- If `pip install -r requirements.txt` fails, try installing dependencies manually


## Additional Resources

| Resource                | Link                                                                 |
|-------------------------|----------------------------------------------------------------------|
| GitHub Repository       | [GemsPy on GitHub](https://github.com/AntaresSimulatorTeam/GemsPy)   |
| Online Documentation    | [gemspy.readthedocs.io](https://gemspy.readthedocs.io)               |
| Examples                | See the repository's `examples/` directory                           |
| FAQ                     | [FAQ](../../6_Support%20&%20Contributing/1_faq.md)                   |
| GitHub Issues           | [GemsPy Issues](https://github.com/AntaresSimulatorTeam/GemsPy/issues)|
| Contact Support         | [Contact support](../../6_Support%20&%20Contributing/2_contact.md)   |

---

**Navigation**
<div style="display: flex; justify-content: space-between;">
  <div style="text-align: left;">
    <a href="../1_Overview/References/4_Users.md">Previous Section</a>
  </div>
  <div style="text-align: center;">
    <a href="../../index.md">Back to Home</a>
  </div>
  <div style="text-align: right;">
    <a href="2_quick start examples.md">Next Section</a>
  </div>
</div>

---

© GEMS (LICENSE)
