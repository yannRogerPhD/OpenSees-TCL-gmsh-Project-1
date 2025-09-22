# Properties for the 9_4_QuadUP element.
# The keys are the physical tags from Gmsh.

# From the OpenSees Wiki for 9_4_QuadUP element:
# element 9_4_QuadUP $eleTag $node1..$node9 $thick $matTag $bulk $fmass $hPerm $vPerm
#
# $thick: Element thickness
# $matTag: Tag of an NDMaterial object
# $bulk: Combined undrained bulk modulus Bc (Bc ≈ Bf/n, where Bf is bulk modulus of fluid, n is porosity)
# $fmass: Fluid mass density
# $hPerm: Horizontal permeability
# $vPerm: Vertical permeability

quadUP_materials = {
    0: {  # Default material for elements with physical tag 0
        "thick": 1.0,
        "matTag": 1,      # This should correspond to an nDMaterial tag defined elsewhere (e.g., in materials.tcl)
        "bulk": 2.2e6,    # Example: Bulk modulus of water
        "fmass": 1000.0,  # Example: Density of water
        "hPerm": 1.0e-5,
        "vPerm": 1.0e-5
    },
    1: {  # Material for physical group 1
        "thick": 1.0,
        "matTag": 1,
        "bulk": 2.2e6,
        "fmass": 1000.0,
        "hPerm": 1.0e-5,
        "vPerm": 1.0e-5
    },
    2: {  # Material for physical group 2
        "thick": 1.0,
        "matTag": 2,
        "bulk": 2.5e6,
        "fmass": 1100.0,
        "hPerm": 5.0e-6,
        "vPerm": 5.0e-6
    }
    # Add more materials as needed
}
