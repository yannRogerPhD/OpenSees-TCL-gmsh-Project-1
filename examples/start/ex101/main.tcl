wipe

set thickX 2.0
set dashL 2000
set dashR 2001
set matViscous 3000
set eltViscous 3001
set rhoB 2.5
set VsB 700.0
set mC [expr {$thickX * $rhoB * $VsB}]

source nodes3D.tcl
source fixity3DWT.tcl
source fixity3D.tcl
source equalDOFs3D.tcl

source nodes2D.tcl
node $dashL 0.0 0.0
node $dashR 0.0 0.0

source fixity2D.tcl
fix $dashL 1 1
fix $dashR 0 1

source equalDOFs2D.tcl
source equalDOFs2DBottom.tcl
source equalDOFs2DMiddle.tcl
equalDOF 1 $dashR 1
equalDOF 1 9 1 2

source materials.tcl
uniaxialMaterial Viscous $matViscous $mC 1

source elements.tcl
element zeroLength $eltViscous $dashL $dashR -mat $matViscous -dir 1

updateMaterialStage -material 1 -stage 0
updateMaterialStage -material 2 -stage 0
updateMaterialStage -material 3 -stage 0

# constraints Transformation
constraints Penalty 1.e14 1.e14
test NormDispIncr 1.0e-4 35 1
numberer RCM
integrator Newmark 0.5 0.25
algorithm KrylovNewton
system ProfileSPD
analysis Transient

analyze 10 5.0e2

updateMaterialStage -material 1 -stage 1
updateMaterialStage -material 2 -stage 1
updateMaterialStage -material 3 -stage 1

analyze 40 5.0e-2

setTime 0.0
wipeAnalysis

set dt     0.005
set nSteps  7990
set pi      3.141592654
set damp    0.02
set omega1  [expr 2*$pi*0.2]
set omega2  [expr 2*$pi*20]
set a0      [expr 2*$damp*$omega1*$omega2/($omega1 + $omega2)]
set a1      [expr 2*$damp/($omega1 + $omega2)]
set gamma  0.5
set beta   0.25