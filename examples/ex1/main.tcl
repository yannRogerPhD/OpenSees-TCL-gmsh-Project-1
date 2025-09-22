wipe

source nodes2D.tcl
source fixity2D.tcl
source materials.tcl
source elements.tcl
source updateMat.tcl
source equalDOFs2D.tcl

system ProfileSPD
test NormDispIncr 1.e-12 25 1
constraints Transformation
integrator LoadControl 1 1 1 1
algorithm Newton
numberer RCM

# create the Analysis
analysis Static

#analyze
analyze 2