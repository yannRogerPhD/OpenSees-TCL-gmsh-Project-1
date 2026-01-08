wipe

source TCL-Files/paramsNInput/params.tcl

model BasicBuilder -ndm 2 -ndf 2

source TCL-Files/paramsNInput/ricker.tcl

# material
set matTag 1
nDMaterial ElasticIsotropic $matTag $E $poiss $rho

source TCL-Files/model/soil_nodesByDOF_2DOF.tcl

source TCL-Files/model/elements_quad4.tcl

source TCL-Files/model/elements_ASDBottom.tcl
source TCL-Files/model/elements_ASDBottomL.tcl
source TCL-Files/model/elements_ASDBottomR.tcl
source TCL-Files/model/elements_ASDLeft.tcl
source TCL-Files/model/elements_ASDRight.tcl

# Static analysis (or quasi-static)
# The absorbing boundaries now are in STAGE 0, so they act as constraints
constraints Transformation
numberer RCM
system UmfPack
test NormUnbalance 0.0001 10 1
algorithm Newton
integrator LoadControl 1.0
analysis Static
set ok [analyze 1]
if {$ok != 0} {
    error "Gravity analysis failed"
}
loadConst -time 0.0
wipeAnalysis

source updateASD.tcl

set soilBase 1
set soilTopP 9
recorder Node -file "soilBase.txt" -time -node $soilBase -dof 1 accel
recorder Node -file "soilTopP.txt" -time -node $soilTopP -dof 1 accel

# Dynamic analysis
# The absorbing boundaries now are in STAGE 0, so they act as constraints
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