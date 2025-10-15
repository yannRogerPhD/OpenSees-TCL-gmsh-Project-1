set thickX 1.0
set thickY 1.0
set thickZ -0.0

# writing main code HERE

wipe
source ex1/modelHeader_2DOF.tcl


constraints Transformation
numberer RCM
system ProfileSPD
test NormUnbalance 1e-05 25 1
algorithm Newton
integrator LoadControl 1.0
analysis Static

