<div style="display: flex; justify-content: space-between; align-items: center;">
  <div style="text-align: left;">
    <a href="../../../..">Main Section</a>
  </div>
  <div style="text-align: right;">
    <img src="../../../assets/gemsV2.png" alt="GEMS Logo" width="150"/>
  </div>
</div>

# Hypergraph Structure

GEMS organizes energy system models into components, ports, and connections. Each component represents a physical unit (e.g. generator, load, storage, bus) with internal parameters, variables, and equations. Ports are named interaction points on components through which quantities (like power flow) are exchanged. A port has a specified port type defining what fields it carries (e.g. a dc_port has a single flow field for power). Connections link one component’s port to another’s, allowing the flow value to pass between them. In each connection, one component acts as the emitter (it defines the port’s flow value via its internal variable or equation) and the other acts as the receiver (it uses that incoming value in its own equations). When defining a connection in YAML, you list the two component IDs and their port names, and exactly one of those components must define the port’s flow field in its model definition. This framework ensures a clear structure where components communicate through ports and all interactions are explicitly modeled.


**Navigation**

<div style="display: flex; justify-content: space-between;">
  <div style="text-align: left;">
  <button type="button" style="background-color:#CCCCCC; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
    <a href="../../1_Overview/References/4_Users" style="text-decoration:none; color: #000000">⬅️ Previous page</a>
  </button>
  </div>
  <button type="button" style="background-color:#AAAAFF; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
    <a href="../../../.." style="text-decoration:none; color: #FFFFFF">Index</a>
  </button>
  <div style="text-align: right;">
  <button type="button" style="background-color:#CCCCCC; border:none; padding:8px 16px; border-radius:4px; cursor:pointer">
    <a href="../1B_gemspy_installation" style="text-decoration:none; color: #000000">Next page ➡️</a>
  </button>
  </div>
</div>

---


© GEMS (LICENSE)