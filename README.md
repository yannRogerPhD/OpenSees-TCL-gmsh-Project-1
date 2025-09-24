# OpenSees + Gmsh Example Models

This gitHub page aims to illustrate the practical use of **OpenSees TCL** in combination with **Gmsh** to perform:

- General geotechnical and structural simulations using **OpenSees Tcl**
- Soil-structure interaction (SSI) modeling  
- Site response analyses  

The examples and methodology are based on resources from:  
[http://soilquake.net/opensees/version2.1/index.htm](http://soilquake.net/opensees/version2.1/index.htm)

---

## ✅ Workflow

### 1. Geometry Creation
Create the model geometry using **Gmsh**.

### 2. Element Type Decision
Determine whether the model uses `quad4` or `quad9` elements (for the moment only these two are available; extension is envisionned).

#### (2a). If using `quad4` elements:
Ensure the following parameters are set correctly for *each layer*:
- `thickness`
- `pressure`
- `rhoVal`
- `massDen`
- `fluidDen`

#### (2b). If using `quad9` elements:

Add layer-specific **tags** if necessary.

---

## ⚠️ Version Control Tip

If you encounter conflicts when trying to pull changes (especially related to IDE configuration files), enforce cleanup by running:

```bash
rm -rf .idea/
git pull origin master
