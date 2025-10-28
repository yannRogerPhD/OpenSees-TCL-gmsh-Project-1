set tsX 1
set dt 0.001

wipe
model BasicBuilder -ndm 2 -ndf 2

timeSeries Path $tsX -dt $dt -filePath velInput.out -factor 0.50

source matELAS.tcl

source TCL-Files/model/nodesByDOF_2DOF.tcl
source TCL-Files/model/equalDOFsLR.tcl
equalDOF 1 2 1 2

source TCL-Files/model/elements_quad4.tcl
source TCL-Files/model/elements_ASDBottom.tcl

constraints Transformation
numberer RCM
integrator LoadControl 0.1
algorithm Newton
system ProfileSPD
test NormDispIncr 0.0001 35 1
analysis Static

analyze 10

setTime 0.0
wipeAnalysis

source TCL-Files/model/updateASDElements.tcl

set topNode 3
set botNode 1
recorder Node -file accelTop.out -time -dT $dt -node $topNode -dof 1 2 accel
recorder Node -file accelBot.out -time -dT $dt -node $botNode -dof 1 2 accel

recorder Node -file velTop.out -time -dT $dt -node $topNode -dof 1 2 vel
recorder Node -file velBot.out -time -dT $dt -node $botNode -dof 1 2 vel

constraints Transformation
numberer RCM
algorithm Newton
integrator Newmark 0.5 0.25
system BandGeneral
test NormDispIncr 0.001 35 1
analysis Transient

analyze 10000 $dt

wipe