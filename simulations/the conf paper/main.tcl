wipe 
model BasicBuilder -ndm 3 -ndf 4

source TCL-Files/model/soil_nodesByDOF_4DOF.tcl
source TCL-Files/model/fixBaseNodes.tcl
source TCL-Files/model/equalDOFs.tcl
# source TCL-Files/model/fixDryNodes.tcl
source TCL-Files/model/symmetryPlaneBCs.tcl

source materials.tcl
source TCL-Files/model/elements_SSPbrickUP.tcl
source TCL-Files/model/analysisParams.tcl

# # gravity analysis
# model BasicBuilder -ndm 3 -ndf 4

updateMaterialStage -material 1 -stage 0
updateMaterialStage -material 2 -stage 0
updateMaterialStage -material 3 -stage 0
updateMaterialStage -material 4 -stage 0
updateMaterialStage -material 5 -stage 0
updateMaterialStage -material 6 -stage 0
updateMaterialStage -material 7 -stage 0

constraints Penalty 1.e10 1.e10
test        NormDispIncr 1e-4 50 1
algorithm   Newton
numberer    RCM
# system      SparseGeneral
system      Mumps
integrator  Newmark $gamma $beta
analysis    Transient
#
set startT  [clock seconds]
# analyze     20 5.0e2
# analyze     200 50
analyze     20 5.0

puts "Finished with elastic gravity analysis..."

updateMaterialStage -material 1 -stage 1
updateMaterialStage -material 2 -stage 1
updateMaterialStage -material 3 -stage 1
updateMaterialStage -material 4 -stage 1
updateMaterialStage -material 5 -stage 1
updateMaterialStage -material 6 -stage 1
updateMaterialStage -material 7 -stage 1

# # plastic gravity loading
# # analyze     40 5.0e-2
# # analyze     100 5.0e-2
analyze 10 1.0e-4

puts "Finished with plastic gravity analysis..."
puts " "

#
# # update permeabilities for post-gravity analyses
set xPerm1 1.0e-8; set yPerm1 1.0e-8; set zPerm1 1.0e-8
set xPerm2 1.0e-9; set yPerm2 1.0e-9; set zPerm2 1.0e-9
set xPerm3 1.0e-8; set yPerm3 1.0e-8; set zPerm3 1.0e-8
set xPerm4 1.0e-8; set yPerm4 1.0e-8; set zPerm4 1.0e-8
set xPerm5 6.6e-5; set yPerm5 6.6e-5; set zPerm5 6.6e-5
set xPerm6 6.6e-5; set yPerm6 6.6e-5; set zPerm6 6.6e-5
set xPerm7 6.6e-5; set yPerm7 6.6e-5; set zPerm7 6.6e-5

puts "Finished updating permeabilities for dynamic analysis..."
puts " "

# source TCL-Files/model/updatePerm.tcl

# # post-gravity recorders
setTime 0.0
wipeAnalysis

remove recorders
# # set recorder time step
set recDT [expr 10*$motionDT]

set node1 197; set node2 174; set node3 151; set node4 105; set node5 81; set node6 57; set node7 18; set node8 15


# # create recorders
recorder Node -file results/accelRigidBaseSPConf.out -time -dT $recDT  -node $node1 $node2 $node3 $node4 $node5 $node6 $node7 $node8 -dof 1 2 3 accel
# recorder Node -file results/accelRigidBaseSPConf.out -time -dT $recDT  -node $node2 -dof 1 2 3 accel

recorder Node -file results/porePressureRBSPConf.out -time -dT $recDT  -node 105 -dof 4 vel
#
# # define acceleration time history file
set accelFile accelerationHistory.out

# timeseries object for acceleration input
timeSeries Path 1 -dt $motionDT -filePath $accelFile -factor 0.49

# uniform excitation in X direction (DOF 1)
pattern UniformExcitation 10 1 -accel 1

puts "Dynamic loading created..."; puts "Dynamic loading created..."; puts "Dynamic loading created..."; puts " "


constraints Penalty 1.e10 1.e10
test        NormDispIncr 1.0e-3 55 1
algorithm   KrylovNewton
numberer    RCM
# numberer AMD; approximate minimum degree
# system      SparseGeneral
system Mumps
integrator  Newmark $gamma $beta
rayleigh    $a0 $a1 0.0 0.0
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
