# ============================================================
# mainInit.tcl for model
# ============================================================

set tsX 1
set tsY 2 2
set thickX 1.0
set thickY 1.0
set thickZ 1.0

# timeSeries Path $tsX - filePath 'vx_record.txt' - factor 1.0
# timeSeries Path $tsY - filePath 'vy_record.txt' - factor 1.0

# writing main code HERE
wipe
model BasicBuilder -ndm 2 -ndf 3

constraints Transformation
# Plain
# Penalty 1.e18 1.e18
# Lagrange
# Transformation
numberer RCM
system ProfileSPD
test NormUnbalance 1e-05 25 1
algorithm Newton
integrator LoadControl 1.0
analysis Static


