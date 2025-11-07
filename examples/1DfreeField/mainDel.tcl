set tsX 1
set dt 0.001

wipe
model BasicBuilder -ndm 2 -ndf 2

timeSeries Path $tsX -dt $dt -filePath velInput.out -factor 0.50

source matELAS.tcl

source TCL-Files/model/nodesByDOF_2DOF.tcl
source TCL-Files/model/equalDOFsLR.tcl
# equalDOF 1 2 1 2

source TCL-Files/model/elements_quad4.tcl
source TCL-Files/model/elements_ASDBottom.tcl

constraints Transformation
numberer RCM
integrator LoadControl 0.1
algorithm Newton
system BandGeneral
test NormDispIncr 0.0001 35 1
analysis Static

analyze 10

setTime 0.0
wipeAnalysis

wipeAnalysis

# --- Compute Rayleigh damping (5%) ---
set dampRatio 0.05
set lambda [eigen 2]
set lambda [eigen 2]
puts "Eigenvalues: $lambda"


# set omega1 [expr sqrt([lindex $lambda 0])]
# set omega2 [expr sqrt([lindex $lambda 1])]
# set a0 [expr 2.0*$dampRatio*$omega1*$omega2/($omega1+$omega2)]
# set a1 [expr 2.0*$dampRatio/($omega1+$omega2)]
# rayleigh $a0 0.0 0.0 $a1
# -------------------------------------