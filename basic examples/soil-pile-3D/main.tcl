wipe

source parameters/params.tcl

model BasicBuilder -ndm 3 -ndf 3

source parameters/ricker.tcl
set tsX 1
set tsY 2
set tsZ 3
timeSeries Path $tsX -dt $dt -values $ts_vals  -factor 9.806
timeSeries Path $tsY -dt $dt -values $ts_vals  -factor 0.0
timeSeries Path $tsZ -dt $dt -values $ts_vals  -factor 0.0

set matTag 1
nDMaterial ElasticIsotropic $matTag $E $poiss $rho

source TCL-Files/model/soil_nodesByDOF_3DOF.tcl

source TCL-Files/model/elements_SSPbrick.tcl
# source ASD_elements.tcl
source TCL-Files/model/elements_ASD3DB.tcl
source TCL-Files/model/elements_ASD3DBF.tcl
source TCL-Files/model/elements_ASD3DBK.tcl
source TCL-Files/model/elements_ASD3DBL.tcl
source TCL-Files/model/elements_ASD3DBLF.tcl
source TCL-Files/model/elements_ASD3DBLK.tcl
source TCL-Files/model/elements_ASD3DBR.tcl
source TCL-Files/model/elements_ASD3DBRF.tcl
source TCL-Files/model/elements_ASD3DBRK.tcl
source TCL-Files/model/elements_ASD3DF.tcl
source TCL-Files/model/elements_ASD3DK.tcl
source TCL-Files/model/elements_ASD3DL.tcl
source TCL-Files/model/elements_ASD3DLF.tcl
source TCL-Files/model/elements_ASD3DLK.tcl
source TCL-Files/model/elements_ASD3DR.tcl
source TCL-Files/model/elements_ASD3DRF.tcl
source TCL-Files/model/elements_ASD3DRK.tcl

model BasicBuilder -ndm 3 -ndf 6
source TCL-Files/model/structure_nodesByDOF_6DOF.tcl
source TCL-Files/pileMAT.tcl
source TCL-Files/model/elements_dispBeamColumn3D.tcl

# create a lumped mass at the top of the pile
set lumpedMass 25000.0; # lumped mass at the top of the pile kg
set nodeLumped 389
mass $nodeLumped $lumpedMass 0.0 0.0 0.0 0.0 0.0

source TCL-Files/model/equalDOF_SSI_interface.tcl

# Static analysis (or quasi-static)
# absorbing boundaries now are in STAGE 0 --> they act as constraints
constraints Transformation
numberer RCM
system UmfPack
test NormUnbalance 0.001 10 1
algorithm Newton
integrator LoadControl 1.0
analysis Static
set ok [analyze 5]
if {$ok != 0} {
    error "Gravity analysis failed"
}
puts "completed the elastic gravity analysis"

loadConst -time 0.0
wipeAnalysis

source updateASD.tcl



set soilBase 147
set soilTopZ 282
set soilTopY 176
set pileTopISSZ 388
set pileBotISSZ 385
set pileTopZ 389

recorder Node -file "soilBaseISS.txt" -time -node $soilBase -dof 1 2 3 accel
recorder Node -file "soilTopYISS.txt" -time -node $soilTopY -dof 1 2 3 accel
recorder Node -file "soilTopZISS.txt" -time -node $soilTopZ -dof 1 2 3 accel

constraints Transformation
numberer RCM
system UmfPack
test NormUnbalance 0.0001 10 1
algorithm Newton
integrator TRBDF2
analysis Transient
set nSteps [expr int($duration/$dt)]
set dt [expr $duration/$nSteps.0]
set ok [analyze $nSteps $dt]
if {$ok != 0} {
    error "Dynamic analysis failed"
}

wipe
# analysis started at 09:00
# temporary stop at 14:50, iteration 5.24467e-08
# 15:15 - 14:55 at iteration 2.41984e-08
# 16:30 - 19:30

# after refinements
# (1) analysis start - 08:05 - 09:20
# (2) analysis start - 06:05 - 07:25
