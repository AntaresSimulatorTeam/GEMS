<div style="display: flex; justify-content: space-between; align-items: center;">
  <div style="text-align: left;">
    <a href="../..">Main Section</a>
  </div>
  <div style="text-align: right;">
    <img src="../../../assets/gemsV2.png" alt="GEMS Logo" width="150"/>
  </div>
</div>
<div>
<h1>How the Converter Works</h1>
<p>The PyPSA to GEMS Converter transforms <a href="https://docs.pypsa.org/latest/api/networks/network/">PyPSA Network</a> into a <a href="https://gems-energy.readthedocs.io/en/latest/3_User_Guide/3_GEMS_File_Structure/1_overview/">GEMS study folder</a>, through the following steps.</p>

<h2 id="1-input-validation-and-preprocessing">1. <strong>Input Validation and Preprocessing</strong></h2>
<p>The converter first validates that the PyPSA network meets the requirements for conversion.<br/>
It performs necessary preprocessing steps such as normalizing component names, handling missing attributes, and ensuring data consistency.<br/>
This stage ensures the input PyPSA model is <strong>compatible</strong> with the conversion process.</p>

<h2 id="2-component-registration-and-data-extraction">2. <strong>Component Registration and Data Extraction</strong></h2>
<p>The converter identifies and extracts all relevant components from the PyPSA network, including both <strong>static (constant)</strong> and <strong>dynamic (time-dependent)</strong> parameters.<br/>
It maps PyPSA-specific parameter names to their GEMS equivalents and organizes the data for conversion.</p>

<h2 id="3-time-series-processing">3. <strong>Time Series Processing</strong></h2>
<p>For parameters that vary over time, the converter extracts time series data and writes them to separate data files (<strong>CSV</strong> or <strong>TSV</strong> format).<br/>
The converter handles both deterministic studies (single time series) and stochastic studies (multiple scenarios), maintaining the temporal structure of the original PyPSA model.</p>

<h2 id="4-gems-component-generation">4. <strong>GEMS Component Generation</strong></h2>
<p>Each PyPSA component is transformed into its corresponding GEMS representation.<br/>
The converter creates GEMS components with appropriate parameters, distinguishing between constant values and time-dependent references.<br/>
Connections between components (such as generators and loads connected to buses) are established through GEMS port connections.</p>

<h2 id="5-global-constraints-handling">5. <strong>Global Constraints Handling</strong></h2>
<p>If the PyPSA model includes global constraints (such as CO₂ emission limits), the converter identifies these and creates corresponding GEMS constraint components, linking them to the relevant system components.</p>

<h2 id="6-study-structure-generation">6. <strong>Study Structure Generation</strong></h2>
<p>Finally, the converter generates the complete GEMS study structure.</p>
</div>

---
**Navigation**
<div style="display: flex; justify-content: space-between;">
  <div style="text-align: left;">
  <button type="button" style="background-color:#CCCCCC; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
    <a href="../1_overview/" style="text-decoration:none; color: #000000">⬅️ Previous page</a>
  </button>
  </div>
  <button type="button" style="background-color:#AAAAFF; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
    <a href="Home/Main_Home/1_context_GEMS.md" style="text-decoration:none; color: #FFFFFF">Home</a>
  </button>
  <div style="text-align: right;">
  <button type="button" style="background-color:#CCCCCC; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
    <a href="../3_input_and_output/" style="text-decoration:none; color: #000000">Next page ➡️</a>
  </button>
  </div>
</div>

---
