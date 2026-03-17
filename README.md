# OpenSees-Geotechnical

A practical toolkit for **geotechnical and soil-structure interaction (SSI) finite element simulations** using [OpenSees TCL](https://opensees.berkeley.edu/) with [Gmsh](https://gmsh.info/) as a pre-processor. Includes a Python-based parsing pipeline that converts Gmsh meshes into ready-to-run OpenSees TCL model files.

---

## Contents

- [Overview](#overview)
- [Workflow](#workflow)
- [Repository Structure](#repository-structure)
- [Examples](#examples)
- [Parsing Pipeline](#parsing-pipeline)
- [Dependencies](#dependencies)
- [Resources](#resources)

---

## Overview

This project covers:

- General **geotechnical and structural simulations** in OpenSees TCL
- **Soil-Structure Interaction (SSI)** modeling, including:
  - Soil-structure interface contact elements
  - Absorbing boundary conditions (ASDs) for soil-domain truncation
- **1D/3D Soil Response Analyses (SRAs)**
- **Solid-fluid coupling** (PIMY, PDMY materials, u-p formulation)

---

## Workflow

```
1. Build geometry       →  Gmsh (.geo file)
2. Generate mesh        →  Gmsh mesh file (.msh)
3. Parse mesh           →  Python parsing pipeline
4. Output TCL files     →  OpenSees model files (.tcl)
5. Run simulation       →  OpenSees TCL
```

The Python scripts in `parsing 4/final/` represent the most up-to-date version of the parsing pipeline.

---

## Examples

| Example | Description | Dimension |
|---|---|---|
| `1DfreeField` | Free-field 1D SRA with PIMY/elastic material | 1D |
| `ASD2D` | SSI with 2D absorbing boundaries | 2D |
| `ASD3D` | SSI with 3D absorbing boundaries | 3D |
| `ASD3D-1` | 3D SSI — alternate configuration | 3D |
| `ASD3D half` | 3D SSI on half-domain (symmetry) | 3D |
| `ASD3D-SP` | 3D SSI with soil-pile system | 3D |
| `soil-pile-3D` | 3D soil-pile lateral interaction | 3D |
| `SSI test` | Benchmark SSI test case | 3D |

Each example folder contains:
- `model.geo` — Gmsh geometry
- `model.msh` — Gmsh mesh
- `meshHelpF.py` / `parsingF.py` — parsing scripts
- `main.tcl` — OpenSees simulation script
- `updateASD.tcl` / `ASD_elements.tcl` — absorbing boundary setup

---

## Parsing Pipeline

The pipeline converts a Gmsh `.msh` file into OpenSees TCL model files (nodes, elements, boundary conditions, DOF assignments).

**Main scripts (`parsing 4/final/`):**

| Script | Role |
|---|---|
| `meshHelper.py` | Reads `.msh`, extracts nodes and elements by physical group |
| `elWriters.py` | Writes TCL files for each element type (brickUP, ASD3D, etc.) |
| `geoXYZF5.py` | Coordinate sorting and geometry utilities |
| `parsingF.py` | Entry point — orchestrates the full parsing workflow |
| `testFXNs.py` | Unit tests for parsing functions |

**Supported element types:**
- `brickUP` — 8-node brick, u-p formulation (solid-fluid coupling)
- `ASD3D` — 3D Absorbing-Scaling Dashpot boundary elements (multiple configurations: B, BF, BK, BL, BLF, BLK, BR, BRF, BRK, F, K, L, LF, LK, R, RF, RK)

---

## Dependencies

- [OpenSees](https://opensees.berkeley.edu/) (TCL interpreter)
- [Gmsh](https://gmsh.info/) (mesh generation)
- Python 3.x with:
  - `gmsh` Python API
  - `numpy`

Install Python dependencies:
```bash
pip install gmsh numpy
```

---

## Resources

- [OpenSees Wiki — Main Examples](https://opensees.berkeley.edu/wiki/index.php?title=Examples)
- [OpenSees Wiki — Basic Examples](https://opensees.berkeley.edu/wiki/index.php?title=Basic_Examples_Manual)
- [OpenSees Wiki — Advanced Structural Examples](https://opensees.berkeley.edu/wiki/index.php?title=Examples_Manual)
- [OpenSees Wiki — Sensitivity Analysis](https://opensees.berkeley.edu/wiki/index.php?title=Sensitivity_Analysis)
- [soilQuake — PIMY, PDMY, solid-fluid coupling examples](http://soilquake.net/opensees/version2.1/index.htm)
- [Gmsh Documentation](https://gmsh.info/doc/texinfo/gmsh.html)

---

## Notes

**Gmsh conformal meshing across shared surfaces:**
```
SetFactory("OpenCASCADE");
// After building volumes with coincident faces:
Coherence;  // merges duplicate points/curves/surfaces
// Or use Boolean Fragments:
BooleanFragments{ Volume{1:N}; Delete; }{}
```

**Git conflict resolution tip:**
```bash
rm -rf .idea/
git pull origin master
```
