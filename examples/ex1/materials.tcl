# Generated nDMaterial definitions for the soil profile

# Material for Layer 1
# nDMaterial PressureIndependMultiYield 1 2 2.0 32142.8571 150000.0000 30 0.1 0.0 100.0 0.0 20

# Soil material
set matSoil 1
set rhoS 1755
set VsS 230.9
set nu 0.0
set E_S [expr 2.0 * $rhoS * pow($VsS, 2)]
nDMaterial ElasticIsotropic $matSoil $E_S $nu $rhoS

# Bedrock material
uniaxialMaterial Viscous $zeroLengthMaterialTag $mC 1
