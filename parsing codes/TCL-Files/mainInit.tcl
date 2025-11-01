# ============================================================
# mainInit.tcl for modelBeam
# ============================================================

set a0 0.049768
set a1 0.000315
set gamma 0.5
set beta 0.25
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
# Plain
system ProfileSPD
# BandGeneral
# BandSPD
# ProfileSPD
# SparseGeneral
# UmfPack
# SparseSPD
test NormDispIncr 1e-05 25 1
algorithm Newton
# Linear
# Newton
# NewtonLineSearch $ratio
# ModifiedNewton
# KrylovNewton
# BFGS $count
# Broyden $count
integrator LoadControl 1.0
analysis Static





constraints Transformation
# Plain
# Penalty 1.e18 1.e18
# Lagrange
# Transformation
numberer RCM
# Plain
system ProfileSPD
# BandGeneral
# BandSPD
# ProfileSPD
# SparseGeneral
# UmfPack
# SparseSPD
test NormDispIncr 1e-05 25 1
algorithm Newton
# Linear
# Newton
# NewtonLineSearch $ratio
# ModifiedNewton
# KrylovNewton
# BFGS $count
# Broyden $count
integrator LoadControl 1.0
analysis Static


