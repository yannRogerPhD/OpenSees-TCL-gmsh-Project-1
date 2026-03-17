wipe

model BasicBuilder -ndm 3 -ndf 4

# !!!!!!!!!!!! definition of soil material properties !!!!!!!!!!!!
source parametersMD/manzariD.tcl

# !!!!!!!!!!!!! importing/sourcing nodes and elements !!!!!!!!!!!!
source TCL-Files/model/soil_nodesByDOF_4DOF.tcl
source TCL-Files/model/elements_SSPbrickUP.tcl

model BasicBuilder -ndm 3 -ndf 3
# !!!!!!!!!!!! definition of the input seismic motion !!!!!!!!!!!!
set tsX 1
set tsY 2
set tsZ 3
set dt 0.005
set seismicInput "elcentro.txt"
timeSeries Path $tsX -dt $dt -filePath $seismicInput -factor 9.81
timeSeries Path $tsY -dt $dt -filePath $seismicInput -factor 0.0
timeSeries Path $tsZ -dt $dt -filePath $seismicInput -factor 0.0

source TCL-Files/model/soil_nodesByDOF_3DOF.tcl
source TCL-Files/model/elements_ASD3DB.tcl
source TCL-Files/model/elements_ASD3DBF.tcl
source TCL-Files/model/elements_ASD3DBK.tcl
source TCL-Files/model/elements_ASD3DBL.tcl
source TCL-Files/model/elements_ASD3DBLF.tcl
source TCL-Files/model/elements_ASD3DBLK.tcl
source TCL-Files/model/elements_ASD3DBR.tcl
source TCL-Files/model/elements_ASD3DBRF.tcl
source TCL-Files/model/elements_ASD3DBRK.tcl
source TCL-Files/model/elements_ASD3DF.tcl
source TCL-Files/model/elements_ASD3DK.tcl
source TCL-Files/model/elements_ASD3DL.tcl
source TCL-Files/model/elements_ASD3DLF.tcl
source TCL-Files/model/elements_ASD3DLK.tcl
source TCL-Files/model/elements_ASD3DR.tcl
source TCL-Files/model/elements_ASD3DRF.tcl
source TCL-Files/model/elements_ASD3DRK.tcl
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# !!!!!!!!!!!! definition of structure/pile model !!!!!!!!!!!!
model BasicBuilder -ndm 3 -ndf 6
source TCL-Files/model/structure_nodesByDOF_6DOF.tcl
source TCL-Files/model/othersPile.tcl

set lumpNode 588
set lumpedMass 48.93
mass $lumpNode $lumpedMass 0.0 0.0 0.0 0.0 0.0

source TCL-Files/model/elements_dispBeamColumn3D.tcl
source TCL-Files/model/embeddedPileElements.tcl
source TCL-Files/model/contactPileElements.tcl
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


model BasicBuilder -ndm 3 -ndf 4
updateMaterialStage -material 1 -stage 0
updateMaterialStage -material 2 -stage 0

# constraints Penalty 1.0e18 1.0e18
# constraints Penalty 1.0e14 1.0e14
# test        NormDispIncr 0.001 20 1

constraints Transformation
# constraints Penalty 1.0e10 1.0e10
test        NormUnbalance 0.001 20 1
algorithm   Newton
numberer    RCM
system      UmfPack
integrator  Newmark 0.5 0.25
# rayleigh    $a0 0. $a1 0.0
analysis    Transient

set startT  [clock seconds]
analyze 1 5.0e3

updateMaterialStage -material 1 -stage 1
updateMaterialStage -material 2 -stage 1

# plastic gravity loading
analyze 1 5.0e-5

set endT    [clock seconds]
puts "Finished with gravity analysis..."
set timeSecs [expr {$endT-$startT}]
set timeMins [expr {double($timeSecs) / 60}]
puts "Analysis execution time: $timeSecs seconds and $timeMins minutes"


loadConst -time 0.0
wipeAnalysis

# ADD RAYLEIGH DAMPING
set omega1 [expr 2.0 * 3.14159 * 0.5]
set omega2 [expr 2.0 * 3.14159 * 10.0]
set dampRatio 0.05
set a0 [expr 2.0 * $dampRatio * $omega1 * $omega2 / ($omega1 + $omega2)]
set a1 [expr 2.0 * $dampRatio / ($omega1 + $omega2)]


source updateASD.tcl
source recorders.tcl

source TCL-Files/model/variablePermeabilityData.tcl
source TCL-Files/model/dynamicAnalysis_adaptive.tcl

wipe
