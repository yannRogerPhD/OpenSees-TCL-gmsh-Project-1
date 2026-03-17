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

# Static analysis (or quasi-static)
# absorbing boundaries now are in STAGE 0 --> they act as constraints
constraints Transformation
numberer RCM
system UmfPack
test NormUnbalance 0.001 10 1
algorithm Newton
integrator LoadControl 1.0
analysis Static

set tGravityStart [clock seconds]

set ok [analyze 5]
if {$ok != 0} {
    error "Gravity analysis failed"
}

set tGravityEnd [clock seconds]
set grativyTime [expr $tGravityEnd - $tGravityStart]

puts "completed the elastic gravity analysis"

loadConst -time 0.0
wipeAnalysis

source updateASD.tcl

set soilBase 147
set soilTopZ 282
set soilTopY 176

recorder Node -file "soilBase.txt" -time -node $soilBase -dof 1 2 3 accel
recorder Node -file "soilTopY.txt" -time -node $soilTopY -dof 1 2 3 accel
recorder Node -file "soilTopZ.txt" -time -node $soilTopZ -dof 1 2 3 accel

constraints Transformation
numberer RCM
system UmfPack
test NormUnbalance 0.0001 10 1
algorithm Newton
integrator TRBDF2
analysis Transient
set nSteps [expr int($duration/$dt)]
set dt [expr $duration/$nSteps.0]

set tDynamicStart [clock seconds]

set ok [analyze $nSteps $dt]
if {$ok != 0} {
    error "Dynamic analysis failed"
}

set tDynamicEnd [clock seconds]
set dynamicTime [expr $tDynamicEnd - $tDynamicStart]

puts "Dynamic analysis runtime = $dynamicTime seconds"

wipe
