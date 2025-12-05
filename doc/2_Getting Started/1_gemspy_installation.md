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

- [**GEMSPy**](../1_Overview/GEMS%20Interpreters/1_gemspy.md)
- [**Antares Modeler**](../1_Overview/GEMS%20Interpreters/2_antares_simulator_modeler.md)

The following documentation explains how to install and use these interpreters for the first time.

# GEMSPy

GEMSPy is a Python interpreter for GEMS that allows you to create, manipulate, and simulate energy system models.


## Requirements

This package requires:

- **Python 3.11** (recommended for optimal compatibility and performance) or Python 3.8+
- Git (for cloning the GEMSPy repository)
- pip package manager (for installing required Python libraries)


## GEMSPy installation

Currently, GEMSPy must be installed by cloning the repository manually:

```bash
# Clone the repository
git clone https://github.com/AntaresSimulatorTeam/GemsPy.git
cd GemsPy
```


## Virtual Environment Setup

It is recommended to create a **virtual environment** before installing GEMSPy. This provides a dedicated space with its own libraries, avoiding dependency conflicts and maintaining a clean global Python environment. All required dependencies will be installed automatically within your virtual environment when you run the installation command.

### Create and Set Up the Virtual Environment

| Step                        | Windows Command                              | macOS/Linux Command                        |
|-----------------------------|----------------------------------------------|--------------------------------------------|
| Create virtual environment  | `python -m venv gemspy-env`                  | `python3 -m venv gemspy-env`               |
| Activate environment        | `gemspy-env\Scripts\activate`               | `source gemspy-env/bin/activate`           |
| Clone GEMSPy repository     | `git clone https://github.com/AntaresSimulatorTeam/GemsPy.git` | `git clone https://github.com/AntaresSimulatorTeam/GemsPy.git` |
| Enter GEMSPy directory      | `cd GemsPy`                                  | `cd GemsPy`                                |
| Install requirements        | `pip install -r requirements.txt`            | `pip install -r requirements.txt`          |

List of **main dependencies** installed via **`requirements.txt`**:

- numpy
- pandas
- scipy


### Working with Virtual Environments

1. **Activate the Virtual Environment**

  While working with GEMSPy, activate the virtual environment:

  - **Windows:**
    ```bash
    gemspy-env\Scripts\activate
    ```
  - **macOS/Linux:**
    ```bash
    source gemspy-env/bin/activate
    ```

  When activated, the environment name will be visible in the terminal prompt:
  ```bash
  (gemspy-env) user@machine:~$
  ```

2. **Deactivate the Environment**

  Before working on another project, deactivate the environment:
  ```bash
  deactivate
  ```

3. **Delete the Virtual Environment**

  If you need to completely remove a virtual environment:
  - Make sure it is deactivated first.
  - Delete the `gemspy-env` folder directly.

  **Note:** Ensure you have saved any important work before deleting the environment.


## Troubleshooting

If you encounter issues during installation:

- Ensure Python 3.11 or 3.8+ is installed.
- If `pip install -r requirements.txt` fails, try installing dependencies manually.

### Python 3.11 Installation (Linux/Ubuntu)

If you need to install Python 3.11 and set up the environment:

```bash
# 1. Install Python 3.11
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.11 python3.11-venv

# 2. Remove old virtual environment (if any)
rm -rf gemspy-env

# 3. Create a new virtual environment with Python 3.11
python3.11 -m venv gemspy-env

# 4. Activate the virtual environment
source gemspy-env/bin/activate
# Verify the Python version
python --version  # Should display "Python 3.11.x"

# 5. Upgrade pip
pip install --upgrade pip

# 6. Install dependencies
pip install -r requirements.txt

# 7. Verify installation
python -c "import scipy; print(scipy.__version__)"
```


## Additional Resources

| Resource              | Link                                                                 |
|-----------------------|----------------------------------------------------------------------|
| GitHub Repository     | [GEMSPy on GitHub](https://github.com/AntaresSimulatorTeam/GemsPy)   |
| Online Documentation  | [gemspy.readthedocs.io](https://gemspy.readthedocs.io)               |
| Examples              | See the repository's `examples/` directory                           |
| FAQ                   | [FAQ](../6_Support%20&%20Contributing/1_faq.md)                      |
| GitHub Issues         | [GEMSPy Issues](https://github.com/AntaresSimulatorTeam/GemsPy/issues)|
| Contact Support       | [Contact support](../6_Support%20&%20Contributing/2_contact.md)      |


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
