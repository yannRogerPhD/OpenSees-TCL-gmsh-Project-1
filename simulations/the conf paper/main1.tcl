wipe
model BasicBuilder -ndm 3 -ndf 4

source TCL-Files/model1/soil_nodesByDOF_4DOF.tcl
source TCL-Files/model1/fixBaseNodes.tcl
source TCL-Files/model1/equalDOFs1D.tcl

source materials.tcl

source TCL-Files/model1/elements_SSPbrickUP.tcl 
source TCL-Files/model1/analysisParams.tcl

updateMaterialStage -material 1 -stage 0
updateMaterialStage -material 2 -stage 0
updateMaterialStage -material 3 -stage 0
updateMaterialStage -material 4 -stage 0
updateMaterialStage -material 5 -stage 0
updateMaterialStage -material 6 -stage 0
updateMaterialStage -material 7 -stage 0

# constraints Penalty 1.e10 1.e10
constraints Transformation
test        RelativeNormDispIncr 1e-5 50 1
algorithm   Newton
numberer    RCM
system      SparseGeneral
integrator  Newmark $gamma $beta
analysis    Transient

# InitialStateAnalysis on

set startT [clock seconds]
set ok [analyze 2 5.0e-2]
if {$ok != 0} {
    puts "WARNING: elastic gravity did not converge — retrying with relaxed tolerance"
    test NormDispIncr 1e-3 100 1
    analyze 2 5.0e-2
}

puts "Finished with elastic gravity analysis..."

# InitialStateAnalysis off
# puts "InitialStateAnalysis is OFF — starting plastic gravity..."

updateMaterialStage -material 5 -stage 1
updateMaterialStage -material 6 -stage 1
updateMaterialStage -material 7 -stage 1

# DIAGNOSTIC RECORDERS for gravity phase
recorder Node -file results1/grav_disp.out    -time -nodeRange 1 32  -dof 1 2 3 disp
recorder Node -file results1/grav_pp.out      -time -nodeRange 1 32  -dof 4 vel
recorder Element -file results1/grav_stress.out -time -eleRange 489 540 stress
recorder Element -file results1/grav_strain.out -time -eleRange 489 540 strain

test NormDispIncr 1e-3 50 1
system BandGeneral
analyze 40 5.0e-4


# update permeability for dynamic analysis
set xPerm1 1.0e-8; set yPerm1 1.0e-8; set zPerm1 1.0e-8
set xPerm2 1.0e-9; set yPerm2 1.0e-9; set zPerm2 1.0e-9
set xPerm3 1.0e-8; set yPerm3 1.0e-8; set zPerm3 1.0e-8
set xPerm4 1.0e-8; set yPerm4 1.0e-8; set zPerm4 1.0e-8
set xPerm5 6.6e-5; set yPerm5 6.6e-5; set zPerm5 6.6e-5
set xPerm6 6.6e-5; set yPerm6 6.6e-5; set zPerm6 6.6e-5
set xPerm7 6.6e-5; set yPerm7 6.6e-5; set zPerm7 6.6e-5

source TCL-Files/model1/updatePerm.tcl
puts "Finished updating permeabilities for dynamic analysis..."
puts " "
flush stdout

setTime 0.0
wipeAnalysis
remove recorders

set recDT [expr 10*$motionDT]

set node1 6; set node2 19; set node3 23; set node4 27

recorder Node -file results1/accelRigidBaseSPConf.out -time -dT $recDT \
    -node $node1 $node2 $node3 $node4 \
    -dof 1 2 3 accel

set accelFile accelerationHistory.out
timeSeries Path 1 -dt $motionDT -filePath $accelFile -factor 0.49
pattern UniformExcitation 10 1 -accel 1

puts "Dynamic loading created..."
puts " "

set endTime     [expr $nSteps * $dT]
set dt          $dT
set tol         1.0e-3
set tolFloor    5.0e-4
set iterMax     50
set iterMax2    70
set iSuc        0
set iSucMax1    10
set iSucMax2    20
set iExtrNL     0
set currentTime 0.0

set testType "RelativeTotalNormDispIncr"

constraints Penalty 1.e10 1.e10
test        $testType $tol $iterMax 1
algorithm   KrylovNewton
numberer    RCM
system      SparseGeneral
integrator  Newmark $gamma $beta
rayleigh    $a0 $a1 0.0 0.0
analysis    Transient

puts "Starting adaptive dynamic analysis..."
puts "Target end time: $endTime s,  initial dt: $dt s"
puts " "

while {$currentTime < $endTime} {

    test $testType $tol $iterMax 1
    set ok [analyze 1 $dt]
    set currentTime [getTime]

    if {$ok == 0} {

        set iSuc [expr $iSuc + 1]

        if {$tol > 1.0e-3} {
            set iExtrNL [expr $iExtrNL + 1]
        }

        # Gate 1 — tighten tolerance after 10 consecutive successes
        if {$iSuc > $iSucMax1} {
            set tol [expr $tol / 2.0]
            if {$tol < $tolFloor} { set tol $tolFloor }
            if {$dt < 0.0005}     { set iterMax $iterMax2 }
        }

        # Gate 2 — grow timestep after 20 consecutive successes
        if {$iSuc > $iSucMax2} {
            set dt [expr $dt * 2.0]
            if {$dt > $dT}  { set dt $dT  }
            if {$dt > 0.05} { set dt 0.05 }
        }

        puts "ok  | t=[format %.4f $currentTime]s  dt=$dt  tol=$tol  iSuc=$iSuc"

    } else {

        set dt [expr $dt / 2.0]

        if {$iSuc == 0} {
            set tol [expr $tol * 2.0]
            if {$tol > 0.005} { set tol 0.005 }
        }

        set iSuc 0

        if {$dt < 0.0005} {
            set iterMax $iterMax2
        }

        puts "FAIL| t=[format %.4f $currentTime]s  dt=$dt  tol=$tol  iSuc=$iSuc"

        if {$dt < 1.0e-6} {
            puts "ERROR: dt collapsed below 1e-6 s — analysis aborted at t=$currentTime s"
            break
        }

    }
}

set endT [clock seconds]
puts " "
puts "Finished with dynamic analysis."
puts "Extremely nonlinear steps (loose tol needed): $iExtrNL"
puts "Analysis execution time: [expr $endT-$startT] seconds"

wipe