# ============================================================
# mainInit.tcl for model4
# ============================================================

set tsX 1
set tsY 2 2
set thickX 0.083333
set thickY 0.125
set thickZ -0.0

# timeSeries Path $tsX - filePath 'vx_record.txt' - factor 1.0
# timeSeries Path $tsY - filePath 'vy_record.txt' - factor 1.0

# writing main code HERE
wipe
model BasicBuilder -ndm 2 -ndf 3

constraints Transformation
numberer RCM
system ProfileSPD
test NormUnbalance 1e-05 25 1
algorithm Newton
integrator LoadControl 1.0
analysis Static


