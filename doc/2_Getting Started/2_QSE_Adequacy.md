![Template Banner](../assets/template_banner.svg)
<div style="display: flex; justify-content: space-between; align-items: center;">
  <div style="text-align: left;">
    <a href="folder1/home1.md">Main Section</a>
  </div>
  <div style="text-align: right;">
    <img src="assets/gemsV2.png" alt="GEMS Logo" width="150"/>
  </div>
</div>


# QSE 1 : Three-Bus Adequacy System

## Overview
This tutorial demonstrates adequacy modeling in a meshed three-bus network. Unlike the previous two-bus example, a three-bus system allows us to illustrate **Kirchhoff's Second Law** (loop flows) and network effects that cannot be shown with only two nodes.

## Problem Description

### Network
**Components:**
- **3 Buses** (Regions 1, 2, 3 forming a triangle)
- **3 Links** (connecting each pair of regions)
- **3 Generators** (different capacities and costs)
- **3 Loads** (varying demands)

**Time Horizon:** 1 hour is used for this example

## Files Structure
```
tutorial_QSE_adequacy/
├── input/
│   ├── library.yml
│   ├── system.yml
│   └── data-series/
│       └──  ...
└── parameters.yml
```

## Step 1: Library File

Use `basic-model-library.yml` from [libraries folder](../../libraries/basic_models_library.yml)

## Step 2: System File

Creation of `system.yml` [file](../2_Getting%20Started/QSE_Study/input/system.yml)

## Step 3: Kirchhoff's Law (Balance of Flows)

### Definition

**Kirchhoff's Second Law** states that the sum of voltages (or flow costs) around any closed loop must equal zero.

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