# ============================================================
# main.tcl for model4
# loaded automatically from/by Python
# ============================================================

puts "==== Running main.tcl for model4 ===="

set thickX 0.083333
set thickY 0.125
set thickZ -0.0

# writing main code HERE
wipe
model BasicBuilder -ndm 2 -ndf 3

constraints Transformation
numberer RCM
system ProfileSPD
test NormUnbalance 1e-05 25 1
algorithm Newton
integrator LoadControl
analysis Static

puts "==== model4 TCL model loaded successfully ===="
