<div style="display: flex; justify-content: space-between; align-items: center;">
  <div style="text-align: left;">
    <a href="../../../..">Main Section</a>
  </div>
  <div style="text-align: right;">
    <img src="../../../assets/gemsV2.png" alt="GEMS Logo" width="150"/>
  </div>
</div>

# GEMS Architecture Breakthrough


GEMS represents a fundamental change from classical **OOME architectures (Object-Oriented Modelling Environment)**, where mathematical models are typically **hard-coded** in the software itself.

<div style="text-align: center;">
  <img src="../../../assets/Architecture_OOME.png" alt="Architecture Breakthrough of GEMS comparing to Classical OOME" />
</div>


This architecture of GEMS aims to export the definition of component models and system configuration from the core software, by relying on **external YAML files**, which enables:

- **Flexible modelling:** Models and system configurations can be defined, extended, or modified directly in configuration files—no changes to the core code are required.
- **Interoperability:** The GEMS file format supports seamless integration with external tools and workflows, such as converting and simulating PyPSA studies using GemsPy.


<div style="text-align: center; width:1000px;">
  <img src="../../../assets/Architecture_GEMS.png" alt="Architecture Breakthrough of GEMS comparing to Classical OOME" />
</div>


<div style="border: 2px solid #2196F3; padding: 15px; border-radius: 8px; background-color: #e8f4ff; max-width: 400px; position: relative;">
  <strong>ℹ️ For more information:</strong>
    <br>
    <a href="../2_File_structure" target="_blank" title="YAML File Structure">
      YAML File Structure
    </a>
    <br>
    <a href="../4_GEMS Interpreters/1_gemspy" target="_blank" title="GemsPy Interpreter">
      GemsPy Interpreter
    </a>
</div>

**Navigation**

<div style="display: flex; justify-content: space-between;">
  <div style="text-align: left;">
  <button type="button" style="background-color:#CCCCCC; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
    <a href="../../0_Home/4_release_notes" style="text-decoration:none; color: #000000">⬅️ Previous page</a>
  </button>
  </div>
  <button type="button" style="background-color:#AAAAFF; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
    <a href="../../../.." style="text-decoration:none; color: #FFFFFF">Home</a>
  </button>
  <div style="text-align: right;">
  <button type="button" style="background-color:#CCCCCC; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
    <a href="../2_File_structure" style="text-decoration:none; color: #000000">Next page ➡️</a>
  </button>
  </div>
</div>