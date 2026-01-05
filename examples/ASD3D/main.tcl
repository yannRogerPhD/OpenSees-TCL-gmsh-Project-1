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
source ASD_elements.tcl

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

set soilBase 22
set soilBott 24

recorder Node -file "soilBase.txt" -time -node $soilBase -dof 1 accel
recorder Node -file "soilBott.txt" -time -node $soilBott -dof 1 accel

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

# analysis started at 09:00
# temporary stop at 14:50, iteration 5.24467e-08
# 15:15 - 14:55 at iteration 2.41984e-08
# 16:30 - 19:30

# Started- 03h20