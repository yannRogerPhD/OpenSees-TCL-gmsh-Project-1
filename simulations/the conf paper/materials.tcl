set nd 3
# FROZEN sublayers (pore fluid = ice, rho_ice = 917 kg/m3)
set void1  0.77  ;# sublayers 1-4, frozen, e=(2.7*0.917-1.8)/(1.8-0.917)
set void2  0.77
set void3  0.77
set void4  0.77

# UNFROZEN active layer (pore fluid = water, rho_w = 1000 kg/m3)
set void10 1.1   ;# e=(2.7-1.8)/(1.8-1.0)


# =============================================================================
# FROZEN ACTIVE LAYER — PressureIndependMultiYield (PIMY)
# Used in the FROZEN CASE to represent winter conditions.
# Active layer total thickness: 4.0 m, divided into 4 sublayers of 1.0 m each.
# Temperature increases linearly from -12°C at surface to 0°C at base.
# One average temperature is assigned per sublayer.
# =============================================================================

# !!!!!!!!!!!!!! material sublayer 1 (0.0 - 1.0 m; T_avg = -10.5°C) !!!!!!!!!!!!!!
# VolumeID Tags in GMSH: (102 - 115) + (200 - 211) --> total 26 volumes --> OK
set matTag1         1
set rho1            1.8  ;# mass density (kg/m3)
set refShearModul1  2.5e6  ;# reference shear modulus (kPa)
set refBulkModul1   5.4e6  ;# reference bulk modulus (kPa)
set cohesi1         2.6e3  ;# apparent cohesion at zero confinement (kPa)
set peakShearStra1  0.01   ;# octahedral shear strain at peak strength
set frictionAng1    25     ;# friction angle (degrees)
set refPress1       100    ;# reference pressure (kPa) — PIMY default
set pressDependCoe1 0      ;# pressure-independent (frozen soil)
set noYieldSurf1    20     ;# number of yield surfaces — default

nDMaterial PressureIndependMultiYield $matTag1 $nd \
    $rho1 $refShearModul1 $refBulkModul1 \
    $cohesi1 $peakShearStra1 \
    $frictionAng1 $refPress1 $pressDependCoe1 $noYieldSurf1


set xPerm1 1.0e-8
set yPerm1 1.0e-8
set zPerm1 1.0e-8



# !!!!!!!!!!!!!! material sublayer 2 (1.0 - 2.0 m; T_avg = -7.5°C) !!!!!!!!!!!!!!
# VolumeID Tags in GMSH: (88 - 101) + (188 - 199) --> total 26 volumes --> OK
set matTag2         2
set rho2            1.8
set refShearModul2  2.1e6
set refBulkModul2   4.6e6
set cohesi2         2.2e3
set peakShearStra2  0.01
set frictionAng2    25
set refPress2       100
set pressDependCoe2 0
set noYieldSurf2    20

nDMaterial PressureIndependMultiYield $matTag2 $nd \
    $rho2 $refShearModul2 $refBulkModul2 \
    $cohesi2 $peakShearStra2 \
    $frictionAng2 $refPress2 $pressDependCoe2 $noYieldSurf2

set xPerm2  1.0e-9  ;# NOTE: lower permeability for this sublayer
set yPerm2  1.0e-9
set zPerm2  1.0e-9





# !!!!!!!!!!!!!! material sublayer 3 (2.0 - 3.0 m; T_avg = -4.5°C) !!!!!!!!!!!!!!
# VolumeID Tags in GMSH: (74 - 87) + (176 - 187) --> total 26 volumes --> OK
set matTag3         3
set rho3            1.8
set refShearModul3  1.7e6
set refBulkModul3   3.8e6
set cohesi3         1.7e3
set peakShearStra3  0.01
set frictionAng3    25
set refPress3       100
set pressDependCoe3 0
set noYieldSurf3    20

nDMaterial PressureIndependMultiYield $matTag3 $nd \
    $rho3 $refShearModul3 $refBulkModul3 \
    $cohesi3 $peakShearStra3 \
    $frictionAng3 $refPress3 $pressDependCoe3 $noYieldSurf3

set xPerm3  1.0e-8
set yPerm3  1.0e-8
set zPerm3  1.0e-8


# !!!!!!!!!!!!!! material sublayer 4 (3.0 - 4.0 m; T_avg = -1.5°C) !!!!!!!!!!!!!!
# VolumeID Tags in GMSH: (60 - 73) + (164 - 175) --> total 26 volumes --> OK
set matTag4         4
set rho4            1.8
set refShearModul4  1.3e6
set refBulkModul4   2.9e6
set cohesi4         1.2e3
set peakShearStra4  0.01
set frictionAng4    25
set refPress4       100
set pressDependCoe4 0
set noYieldSurf4    20

nDMaterial PressureIndependMultiYield $matTag4 $nd \
    $rho4 $refShearModul4 $refBulkModul4 \
    $cohesi4 $peakShearStra4 \
    $frictionAng4 $refPress4 $pressDependCoe4 $noYieldSurf4

set xPerm4  1.0e-8
set yPerm4  1.0e-8
set zPerm4  1.0e-8




# =============================================================================
# UNFROZEN ACTIVE LAYER — PressureIndependMultiYield (PIMY), tag 10
# Used in the UNFROZEN CASE (summer conditions) to replace tags 1–4.
# All 4 sublayers (0.0–4.0 m) share identical unfrozen parameters.
# Switch tags 1–4 --> tag 10 in element definitions for the unfrozen case.
# =============================================================================

## for the ABOVE 04 SUBLAYERS, the unfrozen active layer (all 04 sublayers share
# identical unfrozen parameters): let's call it tag 10
set matTag10          10
set rho10            1.8    ;# mass density (kg/m3)
set refShearModul10  7.5e4  ;# reference shear modulus (kPa)
set refBulkModul10   2.0e5  ;# reference bulk modulus (kPa)
set cohesi10         50     ;# cohesion (kPa)
set peakShearStra10  0.1    ;# peak shear strain
set frictionAng10    30     ;# friction angle (degrees)
set refPress10       100    ;# reference pressure (kPa)
set pressDependCoe10 0      ;# pressure-independent
set noYieldSurf10    20

nDMaterial PressureIndependMultiYield $matTag10 $nd \
    $rho10 $refShearModul10 $refBulkModul10 \
    $cohesi10 $peakShearStra10 \
    $frictionAng10 $refPress10 $pressDependCoe10 $noYieldSurf10

set xPerm10  1.0e-7  ;# unfrozen permeability (m/s) — same for all 4 unfrozen sublayers
set yPerm10  1.0e-7
set zPerm10  1.0e-7




# =============================================================================
# SANDY LAYERS — PressureDependMultiYield (PDMY)
# Based on Parra (1996), Yang & Elgamal (2002), Elgamal et al. (2003).
# Directly from report:   rho, refShearModul, refBulkModul, frictionAng,
#                         peakShearStra
# Inferred from PDMY suggested parameter table (matched by Dr):
#                         refPress, pressDependCoe, PTAng, contrac,
#                         dilat1, dilat2, liquefac1-3, e                [PDMY]
# =============================================================================

# !!!!!!!!!!!!!!!!!!!!!!!!!!!! material sublayer 5 !!!!!!!!!!!!!!!!!!!!!!!!!!!!

# material layer 5 (Dr = 40%)
# VolumeID Tags in GMSH: (46 - 59) + (152 - 163) --> total 26 volumes --> OK
# VolumeID Tags in GMSH: (31 - 45) + (140 - 151) --> total 27 volumes --> OK
set matTag5         5
set rho5            1.9     ;# mass density (kg/m3)
set refShearModul5  5.5e4   ;# reference shear modulus (kPa)
set refBulkModul5   1.5e5   ;# reference bulk modulus (kPa)
set frictionAng5    30      ;# friction angle (degrees)
set peakShearStra5  0.1     ;# peak shear strain
set refPress5       80      ;# reference pressure (kPa)          [PDMY]
set pressDependCoe5 0.5     ;# pressure dependence coefficient   [PDMY]
set PTAng5          26      ;# phase transformation angle (deg)  [PDMY, Dr=40%]
set contrac5        0.067   ;# contraction rate parameter        [PDMY, Dr=40%]
set dilat15         0.06    ;# dilation parameter 1              [PDMY, Dr=40%]
set dilat25         2       ;# dilation parameter 2              [PDMY, Dr=40%]
set liquefac15      10      ;# liquefaction parameter 1 (kPa)    [PDMY, Dr=40%]
set liquefac25      0.01    ;# liquefaction parameter 2          [PDMY, Dr=40%]
set liquefac35      1       ;# liquefaction parameter 3          [PDMY, Dr=40%]
set e5              0.77    ;# initial void ratio                [PDMY, Dr=40%]


nDMaterial PressureDependMultiYield $matTag5 $nd \
    $rho5 $refShearModul5 $refBulkModul5 \
    $frictionAng5 $peakShearStra5 $refPress5 $pressDependCoe5 \
    $PTAng5 $contrac5 $dilat15 $dilat25 \
    $liquefac15 $liquefac25 $liquefac35 \
    20 $e5

set xPerm5  6.6e-5  ;# permeability (m/s)
set yPerm5  6.6e-5
set zPerm5  6.6e-5



# !!!!!!!!!!!!!!!!!!!!!!!!!!!! material sublayer 6 !!!!!!!!!!!!!!!!!!!!!!!!!!!!
# VolumeID Tags in GMSH: (16 - 30) + (128 - 139) --> total 27 volumes --> OK
set matTag6         6
set rho6            1.9     ;#
set refShearModul6  7.5e4   ;#
set refBulkModul6   2.0e5   ;#
set frictionAng6    33      ;#
set peakShearStra6  0.1     ;#
set refPress6       80      ;# [PDMY]
set pressDependCoe6 0.5     ;# [PDMY]
set PTAng6          26      ;# [PDMY, Dr=60%]
set contrac6        0.028   ;# [PDMY, Dr=60%]
set dilat16         0.1     ;# [PDMY, Dr=60%]
set dilat26         3       ;# [PDMY, Dr=60%]
set liquefac16      10      ;# [PDMY, Dr=60%]
set liquefac26      0.003   ;# [PDMY, Dr=60%]
set liquefac36      1       ;# [PDMY, Dr=60%]
set e6              0.65    ;# [PDMY, Dr=60%]


nDMaterial PressureDependMultiYield $matTag6 $nd \
    $rho6 $refShearModul6 $refBulkModul6 \
    $frictionAng6 $peakShearStra6 $refPress6 $pressDependCoe6 \
    $PTAng6 $contrac6 $dilat16 $dilat26 \
    $liquefac16 $liquefac26 $liquefac36 \
    20 $e6

set xPerm6  6.6e-5  ;#
set yPerm6  6.6e-5
set zPerm6  6.6e-5





# !!!!!!!!!!!!!!!!!!!!!!!!!!!! material sublayer 7 !!!!!!!!!!!!!!!!!!!!!!!!!!!!
# VolumeID Tags in GMSH: (1 - 15) + (116 - 127) --> total 27 volumes --> OK
set matTag7         7
set rho7            2.1     ;#
set refShearModul7  1.3e5   ;#
set refBulkModul7   3.9e5   ;#
set frictionAng7    40      ;#
set peakShearStra7  0.1     ;#
set refPress7       80      ;# [PDMY]
set pressDependCoe7 0.5     ;# [PDMY]
set PTAng7          27      ;# [PDMY, Dr~85%]
set contrac7        0.03    ;# [PDMY, Dr~85%]
set dilat17         0.8     ;# [PDMY, Dr~85%]
set dilat27         5       ;# [PDMY, Dr~85%]
set liquefac17      0       ;# dense sand — liquefaction mechanism deactivated [PDMY]
set liquefac27      0       ;# [PDMY]
set liquefac37      0       ;# [PDMY]
set e7              0.45    ;# [PDMY, Dr~85%]

nDMaterial PressureDependMultiYield $matTag7 $nd \
    $rho7 $refShearModul7 $refBulkModul7 \
    $frictionAng7 $peakShearStra7 $refPress7 $pressDependCoe7 \
    $PTAng7 $contrac7 $dilat17 $dilat27 \
    $liquefac17 $liquefac27 $liquefac37 \
    20 $e7

set xPerm7  6.6e-5
set yPerm7  6.6e-5
set zPerm7  6.6e-5
