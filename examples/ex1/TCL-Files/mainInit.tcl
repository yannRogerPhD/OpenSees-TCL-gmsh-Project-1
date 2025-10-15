# ============================================================
# main.tcl for ex1
# loaded automatically from/by Python
# ============================================================

puts "==== Running main.tcl for ex1 ===="

set thickX 1.0
set thickY 1.0
set thickZ -0.0

# writing main code HERE
wipe
model BasicBuilder -ndm 2 -ndf 3

source modelHeader_2DOF.tcl
constraints Transformation
numberer RCM
system ProfileSPD
test NormUnbalance 1e-05 25 1
algorithm Newton
integrator LoadControl
analysis Static

puts "==== ex1 TCL model loaded successfully ===="
