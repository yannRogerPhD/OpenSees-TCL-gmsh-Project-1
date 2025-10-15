# ============================================================
# main.tcl for ex1
# ============================================================

set thickX 1.0
set thickY 1.0
set thickZ -0.0

wipe
model BasicBuilder -ndm 2 -ndf 2

source ex1/nodesByDOF_2DOF.tcl
source ex1/fixityBottom.tcl
source material_pressureindependmultiyield_test.tcl
source ex1/elements_quad4.tcl
updateMaterialStage -material 1 -stage 0


constraints Transformation
numberer RCM
system ProfileSPD
test NormUnbalance 1e-05 25 1
algorithm Newton
integrator LoadControl 1 1 1 1
analysis Static

analyze 2
