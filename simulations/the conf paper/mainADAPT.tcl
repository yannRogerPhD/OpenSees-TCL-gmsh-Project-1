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

# ──────────────────────────────────────────────
# ELASTIC GRAVITY ANALYSIS
# ──────────────────────────────────────────────
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
system      Mumps
integrator  Newmark $gamma $beta
analysis    Transient

set startT [clock seconds]
analyze 20 5.0

puts "Finished with elastic gravity analysis..."


# ──────────────────────────────────────────────
# PLASTIC GRAVITY ANALYSIS
# ──────────────────────────────────────────────
updateMaterialStage -material 1 -stage 1
updateMaterialStage -material 2 -stage 1
updateMaterialStage -material 3 -stage 1
updateMaterialStage -material 4 -stage 1
updateMaterialStage -material 5 -stage 1
updateMaterialStage -material 6 -stage 1
updateMaterialStage -material 7 -stage 1

analyze 100 1.0e-4

puts "Finished with plastic gravity analysis..."
puts " "

# ──────────────────────────────────────────────
# UPDATE PERMEABILITIES FOR DYNAMIC ANALYSIS
# ──────────────────────────────────────────────
set xPerm1 1.0e-8; set yPerm1 1.0e-8; set zPerm1 1.0e-8
set xPerm2 1.0e-9; set yPerm2 1.0e-9; set zPerm2 1.0e-9
set xPerm3 1.0e-8; set yPerm3 1.0e-8; set zPerm3 1.0e-8
set xPerm4 1.0e-8; set yPerm4 1.0e-8; set zPerm4 1.0e-8
set xPerm5 6.6e-5; set yPerm5 6.6e-5; set zPerm5 6.6e-5
set xPerm6 6.6e-5; set yPerm6 6.6e-5; set zPerm6 6.6e-5
set xPerm7 6.6e-5; set yPerm7 6.6e-5; set zPerm7 6.6e-5

puts "Finished updating permeabilities for dynamic analysis..."
puts " "

source TCL-Files/model/updatePerm.tcl

# ──────────────────────────────────────────────
# POST-GRAVITY SETUP
# ──────────────────────────────────────────────
setTime 0.0
wipeAnalysis
remove recorders

set recDT [expr 10*$motionDT]

set node1 197; set node2 174; set node3 151; set node4 105
set node5  81; set node6  57; set node7  18; set node8  15

recorder Node -file results/accelRigidBaseSPConf.out  -time -dT $recDT \
    -node $node1 $node2 $node3 $node4 $node5 $node6 $node7 $node8 \
    -dof 1 2 3 accel

recorder Node -file results/porePressureRBSPConf.out  -time -dT $recDT \
    -node 105 -dof 4 vel

# ──────────────────────────────────────────────
# DYNAMIC LOADING
# ──────────────────────────────────────────────
set accelFile accelerationHistory.out
timeSeries Path 1 -dt $motionDT -filePath $accelFile -factor 0.49
pattern UniformExcitation 10 1 -accel 1

puts "Dynamic loading created..."
puts " "

# ──────────────────────────────────────────────
# ADAPTIVE TIMESTEP LOOP
#
# History-aware controller:
#   - tightens tolerance after 10 consecutive successes (floor: tolFloor)
#   - grows timestep after 20 consecutive successes (cap: original dT)
#   - on failure: halves dt, loosens tol ONLY if already stuck (iSuc==0
#     checked BEFORE reset), then resets iSuc
#   - raises iterMax to 200 when dt becomes very small (last resort)
#   - aborts cleanly if dt collapses below 1e-6 s
# ──────────────────────────────────────────────

set endTime     [expr $nSteps * $dT]  ;# total duration to analyse
set dt          $dT                   ;# current timestep (will adapt)
set tol         1.0e-3               ;# current convergence tolerance
set tolFloor    5.0e-4                ;# tightest tolerance allowed
set iterMax     50                    ;# current max iterations
set iterMax2    70
set iSuc        0                     ;# consecutive success counter
set iSucMax1    10
set iSucMax2    20
set iExtrNL     0                     ;# diagnostic: steps needing loose tol
set currentTime 0.0

set test "RelativeTotalNormDispIncr"
# set test "NormUnbalance"  
# set test "RelativeEnergyIncr"
# set test "NormDispIncr"
# set test "EnergyIncr"

# ──────────────────────────────────────────────
# DYNAMIC ANALYSIS OBJECTS
# ──────────────────────────────────────────────
constraints Penalty  1.e10 1.e10
# test        NormDispIncr 1.0e-3 55 1
# test        EnergyIncr 1.0e-3 15 1
test          $test $tol $iterMax 1
algorithm   KrylovNewton
numberer    RCM
system      Mumps
integrator  Newmark $gamma $beta
rayleigh    $a0 $a1 0.0 0.0
analysis    Transient


puts "Starting adaptive dynamic analysis..."
puts "Target end time: $endTime s,  initial dt: $dt s"
puts " "

while {$currentTime < $endTime} {

    # ── attempt one step with current settings ──
    # test NormDispIncr $tol $iterMax 1
    test $test $tol $iterMax 1
    set ok [analyze 1 $dt]
    set currentTime [getTime]

    # ════════════════ SUCCESS ════════════════
    if {$ok == 0} {

        set iSuc [expr $iSuc + 1]

        # diagnostic: count steps that required a loosened tolerance
        if {$tol > 1.0e-3} {
            set iExtrNL [expr $iExtrNL + 1]
        }

        # Gate 1 — tighten tolerance after 10 consecutive wins
        if {$iSuc > $iSucMax1} {
            set tol [expr $tol / 2.0]
            if {$tol < $tolFloor} { set tol $tolFloor }
            if {$dt < 0.0005}     { set iterMax $iterMax2    }
        }

        # Gate 2 — grow timestep after 20 consecutive wins
        if {$iSuc > $iSucMax2} {
            set dt [expr $dt * 2.0]
            if {$dt > $dT}  { set dt $dT  }  ;# never exceed original dt
            if {$dt > 0.05} { set dt 0.05 }  ;# absolute cap
        }

        puts "ok  | t=[format %.4f $currentTime]s  dt=$dt  tol=$tol  iSuc=$iSuc"

    # ════════════════ FAILURE ════════════════
    } else {

        set dt [expr $dt / 2.0]

        # loosen tolerance only if already stuck — checked BEFORE resetting iSuc
        # (if iSuc > 0, a smaller dt alone should recover; don't loosen yet)
        if {$iSuc == 0} {
            set tol [expr $tol * 2.0]
            if {$tol > 0.005} { set tol 0.005 }
        }

        # now reset the success counter
        set iSuc 0

        # last resort: tiny dt → allow many more Newton iterations
        if {$dt < 0.0005} {
            set iterMax $iterMax2
        }

        puts "FAIL| t=[format %.4f $currentTime]s  dt=$dt  tol=$tol  iSuc=$iSuc"

        # safety exit: dt has collapsed — abort rather than hang
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
