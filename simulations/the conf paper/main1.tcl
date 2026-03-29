wipe
model BasicBuilder -ndm 3 -ndf 4

source TCL-Files/model10/soil_nodesByDOF_4DOF.tcl
source TCL-Files/model10/fixBaseNodes.tcl
source TCL-Files/model10/equalDOFs1D.tcl

fix 2  0 0 0 1    ;# surface nodes: PP = 0 (free drainage)
fix 3  0 0 0 1
fix 6  0 0 0 1
fix 7  0 0 0 1

source materials.tcl

source TCL-Files/model10/elements_SSPbrickUP.tcl 
source TCL-Files/model/analysisParams.tcl

numberer    RCM
system      SparseGeneral
test		RelativeEnergyIncr 1e-3 50 1
algorithm	KrylovNewton
constraints	Penalty 1.0e14 1.0e14
integrator 	Newmark 0.6 0.3025
analysis	Transient

recorder Node -file results/results10/gravE_disp.out    -time -nodeRange 1 32  -dof 1 2 3 disp
recorder Node -file results/results10/gravE_pp.out      -time -nodeRange 1 32  -dof 4 vel
recorder Element -file results/results10/gravE_stress.out -time -eleRange 489 540 stress
recorder Element -file results/results10/gravE_strain.out -time -eleRange 489 540 strain

updateMaterialStage -material 1 -stage 0
updateMaterialStage -material 2 -stage 0
updateMaterialStage -material 3 -stage 0
updateMaterialStage -material 4 -stage 0
updateMaterialStage -material 5 -stage 0
updateMaterialStage -material 6 -stage 0
updateMaterialStage -material 7 -stage 0

recorder Node -file results/results10/gravP_disp.out    -time -nodeRange 1 32  -dof 1 2 3 disp
recorder Node -file results/results10/gravP_pp.out      -time -nodeRange 1 32  -dof 4 vel
recorder Element -file results/results10/gravP_stress.out -time -eleRange 489 540 stress
recorder Element -file results/results10/gravP_strain.out -time -eleRange 489 540 strain

set startT  [clock seconds]

set NumIncr0 5
for {set numincr 1} {$numincr <= $NumIncr0} {incr numincr 1} {
	puts "**Elastic Geostatic Analysis step : $numincr **"
	analyze 20  5.0e2
}

puts " Elastic Geostatic Analysis step success ";


# switch material stage from elastic (gravity) to plastic -------> 2nd run

updateMaterialStage -material 1 -stage 1
updateMaterialStage -material 2 -stage 1
updateMaterialStage -material 3 -stage 1
updateMaterialStage -material 4 -stage 1
updateMaterialStage -material 5 -stage 1
updateMaterialStage -material 6 -stage 1
updateMaterialStage -material 7 -stage 1

set NumIncr1 5
for {set numincr 1} {$numincr <= $NumIncr1} {incr numincr 1} {
	puts "**Plastic Geostatic Analysis step : $numincr **"
	analyze 40  5e2
}

puts " Plastic Geostatic Analysis step success ";
puts "First run done. Gravity Applied"


# After plastic geostatic
set node_top    6
set node_bottom 31

set disp_top    [nodeDisp $node_top    3]
set disp_bot    [nodeDisp $node_bottom 3]
set pp_top      [nodeDisp $node_top    4]
set pp_bot      [nodeDisp $node_bottom 4]

puts "Geostatic Check"
puts "Vertical disp top node:    $disp_top  (should be approx 0)"
puts "Vertical disp bottom node: $disp_bot  (should be 0, fixed)"
puts "Pore pressure top:         $pp_top    (should be approx 0 if drained top)"
puts "Pore pressure bottom:      $pp_bot    (should be gamma_w * H)"


# update permeability for dynamic analysis
set xPerm1 1.0e-8; set yPerm1 1.0e-8; set zPerm1 1.0e-8
set xPerm2 1.0e-9; set yPerm2 1.0e-9; set zPerm2 1.0e-9
set xPerm3 1.0e-8; set yPerm3 1.0e-8; set zPerm3 1.0e-8
set xPerm4 1.0e-8; set yPerm4 1.0e-8; set zPerm4 1.0e-8
set xPerm5 6.6e-5; set yPerm5 6.6e-5; set zPerm5 6.6e-5
set xPerm6 6.6e-5; set yPerm6 6.6e-5; set zPerm6 6.6e-5
set xPerm7 6.6e-5; set yPerm7 6.6e-5; set zPerm7 6.6e-5

source TCL-Files/model10/updatePerm.tcl
puts "Finished updating permeabilities for dynamic analysis..."
puts " "


setTime 0.0
wipeAnalysis
remove recorders

set recDT [expr 10*$motionDT]

set node1 6; set node2 19; set node3 23; set node4 27

recorder Node -file results/results10/accelRigidBaseSPConf.out -time -dT $recDT \
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