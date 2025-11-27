---
title: "File title"
author: "Author name"
date: "29/01/2025" 
logo: "assets/gemsV2.png"
---

<div style="display: flex; justify-content: space-between; align-items: center;">
  <div style="text-align: left;">
    <a href="folder1/home1.md">Main Section</a>
  </div>
  <div style="text-align: right;">
    <img src="assets/gemsV2.png" alt="GEMS Logo" width="150"/>
  </div>
</div>

![Template Banner](/doc/assets/template_banner.svg)

# Title 1

<div style="display: flex; flex-direction: column; align-items: center; gap: 10px;">
  <div style="display: flex; justify-content: center; align-items: flex-end; gap: 40px;">
    <div style="display: flex; flex-direction: column; align-items: center;">
      <img src="assets/4_RTE_logo.svg.png" alt="RTE Logo" style="height: 80"/>
      <div style="font-size: 0.9em; color: #555; margin-top: 8px;"><em>RTE - French Transmission System Operator</em></div>
    </div>
    <div style="display: flex; flex-direction: column; align-items: center;">
      <img src="assets/5_antares_sim_logo.webp" alt="Antares Simulator Logo" style="height: 80"/>
      <div style="font-size: 0.9em; color: #555; margin-top: 8px;"><em>Antares Simulator Team</em></div>
    </div>
  </div>
</div>

## Sub-Title 2
Content or text here.

**Code block example (YAML):**
```yaml
connections:
  - component1: generator1
    port1: injection_port
    component2: node1
    port2: injection_port
  - component1: generator2
    port1: injection_port
    component2: node1
    port2: injection_port
  - component1: demand
    port1: injection_port
    component2: node1
    port2: injection_port
```

**Code block example (Python):**
```python
print("Hello World")
```
**Note Example:**

<div style="border:1px solid #ccc; padding:10px; background:#f9f9f9;">
<strong>🖊️ Note :</strong> This is an important note
</div>


**Simple Equation example:**

 $3 * parameter_1 * variable_a + variable_b + 56.4 <= variable_4 * 439$ 

**LATEC equation example:**
$$
3 \cdot \text{parameter\_1} \cdot \text{variable\_a} + \text{variable\_b} + 56.4 \leq \text{variable\_4} \cdot 439
$$

---
**Navigation**
<div style="display: flex; justify-content: space-between;">
  <div style="text-align: left;">
    <a href="previous.md">Previous Section</a>
  </div>
    <div style="text-align: center;">
    <a href="../../index.md">Back to Home</a>
  </div>
  <div style="text-align: right;">
    <a href="next.md">Next Section</a>
  </div>
</div>

---

© GEMS (LICENSE)