<div style="display: flex; justify-content: space-between; align-items: center;">
  <div style="text-align: left;">
    <a href="../../../..">Main Section</a>
  </div>
  <div style="text-align: right;">
    <img src="../../../assets/gemsV2.png" alt="GEMS Logo" width="150"/>
  </div>
</div>

# GemsPy

[GemsPy](https://gemspy.readthedocs.io/en/latest/) is a Python interpreter for GEMS that allows you to create, manipulate, and simulate energy system models.

## Requirements

This package requires:

- **Python 3.11** (recommended for optimal compatibility and performance) or Python 3.8+
- Git (for cloning the [GemsPy repository](https://github.com/AntaresSimulatorTeam/GemsPy))
- pip package manager (for installing required Python libraries)

## GemsPy installation

Currently, [GemsPy](https://github.com/AntaresSimulatorTeam/GemsPy) must be installed by cloning the repository manually:

```bash
# Clone the repository
git clone https://github.com/AntaresSimulatorTeam/GemsPy.git
cd GemsPy
```

## Virtual Environment Setup

It is recommended to create a **virtual environment** before installing [GemsPy](https://github.com/AntaresSimulatorTeam/GemsPy). This provides a dedicated space with its own libraries, avoiding dependency conflicts and maintaining a clean global Python environment. All required dependencies will be installed automatically within your virtual environment when you run the installation command.

### Create and Set Up the Virtual Environment

| Step                        | Windows Command                              | macOS/Linux Command                        |
|-----------------------------|----------------------------------------------|--------------------------------------------|
| Create virtual environment  | `python -m venv gemspy-env`                  | `python3 -m venv gemspy-env`               |
| Activate environment        | `gemspy-env\Scripts\activate`               | `source gemspy-env/bin/activate`           |
| Clone GemsPy repository     | `git clone https://github.com/AntaresSimulatorTeam/GemsPy.git` | `git clone https://github.com/AntaresSimulatorTeam/GemsPy.git` |
| Enter GemsPy directory      | `cd GemsPy`                                  | `cd GemsPy`                                |
| Install requirements        | `pip install -r requirements.txt`            | `pip install -r requirements.txt`          |

List of **main dependencies** installed via **`requirements.txt`**:

- numpy
- pandas
- scipy

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
| GitHub Repository     | [GemsPy on GitHub](https://github.com/AntaresSimulatorTeam/GemsPy)   |
| Online Documentation  | [gemspy.readthedocs.io](https://gemspy.readthedocs.io)               |
| Examples              | See the repository's `examples/` directory                           |
| FAQ                   | [FAQ](../6_Support_Contributing/1_faq.md)                      |
| GitHub Issues         | [GemsPy Issues](https://github.com/AntaresSimulatorTeam/GemsPy/issues)|
| Contact Support       | [Contact support](../6_Support_Contributing/2_contact.md)      |

---

**Navigation**

<div style="display: flex; justify-content: space-between;">
  <div style="text-align: left;">
  <button type="button" style="background-color:#CCCCCC; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
    <a href="../1A_modeler_installation" style="text-decoration:none; color: #000000">⬅️ Previous page</a>
  </button>
  </div>
  <button type="button" style="background-color:#AAAAFF; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
    <a href="../../../.." style="text-decoration:none; color: #FFFFFF">Home</a>
  </button>
  <div style="text-align: right;">
  <button type="button" style="background-color:#CCCCCC; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
    <a href="../2A_QSE_adequacy" style="text-decoration:none; color: #000000">Next page ➡️</a>
  </button>
  </div>
</div>

---


© GEMS (LICENSE)
