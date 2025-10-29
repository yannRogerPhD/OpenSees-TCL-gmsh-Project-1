# OpenSees + Gmsh Example Models

This gitHub page aims to illustrate the practical use of **OpenSees TCL** in combination with **Gmsh** to perform:

- General geotechnical and structural simulations using **OpenSees Tcl**
- Soil-structure interaction (SSI) modeling  
- Site response analyses  

The examples and methodology are based on resources from:  
[http://soilquake.net/opensees/version2.1/index.htm](http://soilquake.net/opensees/version2.1/index.htm)

## Note about gmsh

In case we want two volumes to share a single, continuous interface so the mesh is conformal across that face.

```bash
SetFactory("OpenCASCADE");

// ... build your two volumes; they currently have coincident faces
// e.g., Volume{v1}; Volume{v2}; and the interface appears as Surface{10} in one
// and Surface{11} in the other

Coherence; // merges duplicate points/curves/surfaces so both volumes share one face
```

## Version Control Tip

If you encounter conflicts when trying to pull changes (especially related to IDE configuration files), enforce cleanup by running:

```bash
rm -rf .idea/
git pull origin master
```
