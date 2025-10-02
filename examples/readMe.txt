These examples are taken from:
http://soilquake.net/opensees/version2.1/index.htm

Steps:
(1) geometry from gmsh
(2) it should be known wether quad4 or quad9
    (a) if quad 4:
        - check thickness, pressure, rhoVal, massDen and fluidDen for all layers
        - add tags if necessary
    (b) if quad9:
        - check node ordering from ".msh" file
        - see more instructions in the "getInfoG.py" file

WHEN EVER CONFLICTS HAPPEN WHEN TRYING TO PULL, ENFORCE
rm -rf .idea/
