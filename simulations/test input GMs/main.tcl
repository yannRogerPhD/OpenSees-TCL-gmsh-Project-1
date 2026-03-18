wipe 
model BasicBuilder -ndm 3 -ndf 4

# souce nodes
source TCL-Files/model/soil_nodesByDOF_4DOF.tcl

# define BCs at the base of the soil model (fix and equalDOF)
source TCL-Files/model/fixBaseNodes.tcl
source TCL-Files/model/baseEqualDOFs.tcl

# define period BCs
source TCL-Files/model/equalDOFs.tcl

# define dry nodes
source TCL-Files/model/fixDryNodes.tcl

# define materials
source materials.tcl

# define elements
source TCL-Files/model/elements_SSPbrickUP.tcl

# create base dashpots (LK)
# source TCL-Files/model/baseDashpot.tcl

# rigid base: fix DOF 1 (X) at all base nodes
fix 1 1 1 1 0
fix 5 1 1 1 0
fix 8 1 1 1 0
fix 4 1 1 1 0

# analysis parameters
source TCL-Files/model/analysisParams.tcl


# gravity analysis
model BasicBuilder -ndm 3 -ndf 4

updateMaterialStage -material 1 -stage 0
updateMaterialStage -material 2 -stage 0
updateMaterialStage -material 3 -stage 0

constraints Penalty 1.e14 1.e14
test        NormDispIncr 1e-5 30 1
algorithm   Newton
numberer    RCM
system      SparseGeneral
integrator  Newmark $gamma $beta 
analysis    Transient

set startT  [clock seconds]
analyze     20 5.0e2

puts "Finished with elastic gravity analysis..."

updateMaterialStage -material 1 -stage 1
updateMaterialStage -material 2 -stage 1
updateMaterialStage -material 3 -stage 1

# plastic gravity loading
analyze     40 5.0e-2


# update permeabilities for post-gravity analyses
set xPerm3 1.0e-2
set yPerm3 1.0e-2
set zPerm3 1.0e-2

set xPerm2 1.0e-5
set yPerm2 1.0e-5
set zPerm2 1.0e-5

set xPerm1 1.0e-2 
set yPerm1 1.0e-2
set zPerm1 1.0e-2

source TCL-Files/model/updatePerm.tcl

# post-gravity recorders
setTime 0.0
wipeAnalysis

remove recorders

# set recorder time step
set recDT [expr 10*$motionDT]

# create recorders
recorder Node -file results/accelRigidBase.out -time -dT $recDT  -node 15 -dof 1 2 3 accel
recorder Node -file results/porePressureRB.out -time -dT $recDT  -node 212 -dof 4 vel

# define acceleration time history file
set accelFile accelerationHistory.out

# timeseries object for acceleration input
set aSeries "Path -dt $motionDT -filePath $accelFile -factor 0.49"

# uniform excitation in X direction (DOF 1)
pattern UniformExcitation 10 1 -accel $aSeries
puts "Dynamic loading created..."
 
constraints Penalty 1.e14 1.e14
test        NormDispIncr 1.0e-3 55 1
algorithm   KrylovNewton
numberer    RCM
# numberer AMD; approximate minimum degree
system      SparseGeneral
integrator  Newmark $gamma $beta
#rayleigh    $a0 $a1 0.0 0.0
analysis    Transient

# perform analysis with timestep reduction loop
set ok [analyze $nSteps  $dT]
 
# if analysis fails, reduce timestep and continue with analysis
if {$ok != 0} {
    puts "did not converge, reducing time step"
    set curTime  [getTime]
    set mTime $curTime
    puts "curTime: $curTime"
    set curStep  [expr $curTime/$dT]
    puts "curStep: $curStep"
    set rStep  [expr ($nSteps-$curStep)*2.0]
    set remStep  [expr int(($nSteps-$curStep)*2.0)]
    puts "remStep: $remStep"
    set dT       [expr $dT/2.0]
    puts "dT: $dT"
 
    set ok [analyze  $remStep  $dT]
 
    # if analysis fails again, reduce timestep and continue with analysis
    if {$ok != 0} {
        puts "did not converge, reducing time step"
        set curTime  [getTime]
        puts "curTime: $curTime"
        set curStep  [expr ($curTime-$mTime)/$dT]
        puts "curStep: $curStep"
        set remStep  [expr int(($rStep-$curStep)*2.0)]
        puts "remStep: $remStep"
        set dT       [expr $dT/2.0]
        puts "dT: $dT"
 
        analyze  $remStep  $dT
    }
}
set endT    [clock seconds]
puts "Finished with dynamic analysis..."
puts "Analysis execution time: [expr $endT-$startT] seconds"

wipe
