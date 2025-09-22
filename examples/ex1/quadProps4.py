# Properties for the 4-node quad element.
# The keys are the physical tags from Gmsh.
import numpy as np

# From the OpenSees Wiki for quad element:
# element quad $eleTag $iNode $jNode $kNode $lNode $thick $type $matTag <$pressure $rho $b1 $b2>
#
# $thick: Element thickness
# $type: "PlaneStrain" or "PlaneStress"
# $matTag: Tag of an NDMaterial object
# $pressure: surface pressure (optional, default = 0.0)
# $rho: element mass density (optional, default = 0.0)
# $b1, $b2: constant body forces (optional, default = 0.0)

thickness = 1.0
pressure = 0.0
rhoVal = 0.0
gVal = 9.806
massDen, fluidDen = 2.0, 1.0
alpha = 0

alphaRads = np.deg2rad(alpha)
b1 = (massDen - fluidDen) * gVal * np.sin(alphaRads)
b2 = - (massDen - fluidDen) * gVal * np.cos(alphaRads)

quad4Materials = {
    0: {  # Default material for elements with physical tag 0
        "thick": thickness,
        "type": "PlaneStrain",
        "matTag": 1,  # This should correspond to an nDMaterial tag
        "pressure": pressure,
        "rho": rhoVal,
        "b1": b1,
        "b2": b2
    },
    1: {  # Material for physical group 1
        "thick": thickness,
        "type": "PlaneStrain",
        "matTag": 1,  # This should correspond to an nDMaterial tag
        "pressure": pressure,
        "rho": rhoVal,
        "b1": b1,
        "b2": b2
    },
    2: {  # Material for physical group 2
        "thick": thickness,
        "type": "PlaneStrain",
        "matTag": 2,
        "pressure": pressure,
        "rho": rhoVal,
        "b1": b1,
        "b2": b2
    }
    # Add more materials as needed
}

