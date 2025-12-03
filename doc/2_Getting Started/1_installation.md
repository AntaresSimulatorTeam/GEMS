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

As it's mentionned in Overview section, GEMS studies can be executed using different interpreters:

- **[GEMSPy](../1_Overview/GEMS%20Interpreters/1_gemspy.md)**
- **[Antares Modeler](../1_Overview/GEMS%20Interpreters/2_antares_simulator_modeler.md)**

The following documentaiton will explain how to install and use for the first time these interpreters

# GEMSPy

GEMSPy is a Python interpreter for GEMS that allows you to create, manipulate, and simulate energy system models.

## Requirements

This package requires :

- **Python 3.11** (recommended) or Python 3.8+
- Git (for cloning the GEMSPY repository)
- pip package manager (for installing required Python libraries)

## Installation from Source

Currently, GEMSPy must be installed by cloning the repository manually. 

```bash
# Clone the repository
git clone https://github.com/AntaresSimulatorTeam/GemsPy.git
cd GemsPy
```

## Virtual Environment Setup

It *usually recommend* to create a **virtual environment** before installing GEMSPy. It will be a dedicated environment with its own libraries installed which avoids dependency conflicts and maintains a clean global Python environment,
Indeed, all required dependencies will be installed automatically within your virtual environment when you run the installation command.

### Create and Set Up the Virtual Environment

| Step                        | Windows Command                              | macOS/Linux Command                        |
|-----------------------------|----------------------------------------------|--------------------------------------------|
| Create virtual environment  | `python -m venv gemspy-env`                  | `python3 -m venv gemspy-env`               |
| Activate environment        | `gemspy-env\Scripts\activate`               | `source gemspy-env/bin/activate`           |
| Clone GEMSPy repository     | `git clone https://github.com/AntaresSimulatorTeam/GemsPy.git` | `git clone https://github.com/AntaresSimulatorTeam/GemsPy.git` |
| Enter GEMSPy directory      | `cd GemsPy`                                  | `cd GemsPy`                                |
|Install GEMSPY requirements|pip install -r requirements.txt|pip install -r requirements.txt|

### Work with Virtual Environments

1. Activate the Virtual Environment

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
(gemspy-env) user@machine:~$
```

***The virtual environment is now ready to be used.***

2. Deactivating Your Environment

Before working to another project
```bash
deactivate
```

3. Deleting a Virtual Environment

Rarely, it's needed to completely remove a virtual environment:

- Make sure it's deactivated first 
- Delete directly the gemspy-environment folder

## Verification of the Installation

To verify that GEMSPy is correctly installed:

```python
# Activate your virtual environment first, then start Python
python

# In the Python interpreter:
import gemspy
print(gemspy.__version__)
```

If this runs without errors and displays a version number, your installation is successful.

### Quick Test

You can also run a quick test to ensure the core functionality works:

```python
import gemspy

# This should run without errors
print("GEMSPy is installed correctly!")
```

## Additional Resources

| Resource                | Link                                                                 |
|-------------------------|----------------------------------------------------------------------|
| GitHub Repository       | [GemsPy on GitHub](https://github.com/AntaresSimulatorTeam/GemsPy)   |
| Online Documentation    | [gemspy.readthedocs.io](https://gemspy.readthedocs.io)               |
| Examples                | See the repository's `examples/` directory                           |
| FAQ                     | [FAQ](../../6_Support & Contributing/1_faq.md)                       |
| GitHub Issues           | [GemsPy Issues](https://github.com/AntaresSimulatorTeam/GemsPy/issues)|
| Contact Support         | [Contact support](../../6_Support & Contributing/2_contact.md)       |
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