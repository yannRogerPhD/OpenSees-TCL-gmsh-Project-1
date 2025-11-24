# OpenSees TCL + Gmsh (Pre-Processor) Application Models

This GitHub page aims to primarily illustrate the practical use of **OpenSees TCL** in combination with **Gmsh** to perform:

- General geotechnical and structural simulations using **OpenSees TCL**
- Soil-structure interaction (SSI) modeling, with particular attention paid to:  
  - the modeling of soil-structure interface contact, and
  - precisely accounting for absorbing boundary conditions due to soil-domain truncation
- Soil Response Analyses (SRAs)

Most of the examples as well as the methodology are based on resources from:  
- OpenSees wiki: 
  - [main geotechnical and structural examples](https://opensees.berkeley.edu/wiki/index.php?title=Examples)
  - [basic examples](https://opensees.berkeley.edu/wiki/index.php?title=Basic_Examples_Manual)
  - [advanced (structural) examples](https://opensees.berkeley.edu/wiki/index.php?title=Examples_Manual)
  - [sensitivity analysis](https://opensees.berkeley.edu/wiki/index.php?title=Sensitivity_Analysis)
- soilQuake (mainly for material applications):
  - 25 different examples in various configurations
  - [PIMY, PDMY, and solid-fluid coupling problems](http://soilquake.net/opensees/version2.1/index.htm)

## Notes about gmsh

In case we want two volumes to share a single, continuous interface so the mesh is conformal across that face.


```bash
SetFactory("OpenCASCADE");

// ... build your two volumes; they currently have coincident faces
// e.g., Volume{v1}; Volume{v2}; and the interface appears as Surface{10} in one
// and Surface{11} in the other

Coherence; // merges duplicate points/curves/surfaces so both volumes share one face
// Or use Boolean Fragments
BooleanFragments{{ Volume{{1:{end}}}; Delete; }}{{}
```

## Version Control Tip

If you encounter conflicts when trying to pull changes (especially related to IDE configuration files), enforce cleanup by running:

```bash
rm -rf .idea/
git pull origin master
```
