# Properties for the 4-node quad element.
# The keys are the physical tags from Gmsh.

# From the OpenSees Wiki for quad element:
# element quad $eleTag $iNode $jNode $kNode $lNode $thick $type $matTag <$pressure $rho $b1 $b2>
#
# $thick: Element thickness
# $type: "PlaneStrain" or "PlaneStress"
# $matTag: Tag of an NDMaterial object
# $pressure: surface pressure (optional, default = 0.0)
# $rho: element mass density (optional, default = 0.0)
# $b1, $b2: constant body forces (optional, default = 0.0)

quadMaterials = {
    0: {  # Default material for elements with physical tag 0
        "thick": 1.0,
        "type": "PlaneStrain",
        "matTag": 1,  # This should correspond to an nDMaterial tag
        "pressure": 0.0,
        "rho": 0.0,
        "b1": 0.0,
        "b2": 0.0
    },
    1: {  # Material for physical group 1
        "thick": 1.0,
        "type": "PlaneStrain",
        "matTag": 1,  # This should correspond to an nDMaterial tag
        "pressure": 0.0,
        "rho": 0.0,
        "b1": 0.0,
        "b2": 0.0
    },
    2: {  # Material for physical group 2
        "thick": 1.0,
        "type": "PlaneStrain",
        "matTag": 2,
        "pressure": 0.0,
        "rho": 0.0,
        "b1": 0.0,
        "b2": 0.0
    }
    # Add more materials as needed
}

print("Use more general formula for weightX and weightY\nSee formula\n")

""" 
unitWeightX = (massDen - fluidDen) * gVal * sin((alpha/180) * pi)
unitWeightY = - (massDen - fluidDen) * gVal * cos((alpha/180) * pi)
"""
