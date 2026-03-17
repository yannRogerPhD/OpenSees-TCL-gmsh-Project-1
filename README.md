# OpenSees-Geotechnical

A practical toolkit for **geotechnical and soil-structure interaction (SSI) finite element simulations** using [OpenSees TCL](https://opensees.berkeley.edu/) with [Gmsh](https://gmsh.info/) as a pre-processor. Includes a Python-based parsing pipeline that converts Gmsh meshes into ready-to-run OpenSees TCL model files.

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
