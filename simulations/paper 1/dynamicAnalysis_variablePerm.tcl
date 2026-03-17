# ============================================================================
# DYNAMIC ANALYSIS WITH VARIABLE PERMEABILITY
# ============================================================================
# Generated automatically by parsingF.py
# Source this file AFTER updateASD.tcl in your main.tcl
# ============================================================================

puts ""
puts "=============================================="
puts "DYNAMIC ANALYSIS WITH VARIABLE PERMEABILITY"
puts "=============================================="

# Analysis parameters
set dtAnalysis 0.005
set totalTime 17.00
set updateInterval 5
set totalSteps [expr int($totalTime / $dtAnalysis)]
set useVariablePerm 1

puts "Time step: $dtAnalysis s"
puts "Total time: $totalTime s"
puts "Total steps: $totalSteps"
puts "Update interval: every $updateInterval steps"
puts "Variable permeability: [expr {$useVariablePerm ? "ENABLED" : "DISABLED"}]"
puts ""

# setup analysis
# constraints Transformation
# test NormDispIncr 1.0e-3 30 1
# algorithm KrylovNewton
# numberer RCM
# system UmfPack
# integrator Newmark 0.5 0.25
# rayleigh $a0 0.0 $a1 0.0
# analysis Transient

constraints Penalty 1.e14 1.e14
test        EnergyIncr 0.001 60 1
algorithm   KrylovNewton
numberer    RCM
system      UmfPack
integrator  Newmark 0.5 0.25
rayleigh    $a0 $a1 0.0 0.0
analysis    Transient

# output
file mkdir results
set permLog [open "results/permeability_evolution.csv" w]
puts $permLog "Time, Element, ru, kRatio, kNew"
set sampleElem [expr ($firstSSPelem + $lastSSPelem) / 2]

# main loop
puts "Starting analysis..."
set startT [clock seconds]
set currentStep 0
set currentTime 0.0

while {$currentStep < $totalSteps} {

    if {$useVariablePerm} {
        set stepsToRun $updateInterval
    } else {
        set stepsToRun [expr min(500, $totalSteps - $currentStep)]
    }

    if {[expr $currentStep + $stepsToRun] > $totalSteps} {
        set stepsToRun [expr $totalSteps - $currentStep]
    }

    set ok [analyze $stepsToRun $dtAnalysis]

    if {$ok != 0} {
        puts "WARNING: Convergence issue at t=[format %.3f $currentTime]s"
        set ok [analyze 1 [expr $dtAnalysis/2.0]]
        if {$ok != 0} {
            set ok [analyze 1 [expr $dtAnalysis/4.0]]
            if {$ok != 0} {
                puts "ERROR: Not converging. Stopping."
                break
            }
        }
    }

    set currentStep [expr $currentStep + $stepsToRun]
    set currentTime [getTime]

    if {$useVariablePerm} {
        updateAllPermeabilities
        if {[expr $currentStep % 200] == 0} {
            set result [updateElementPermeability $sampleElem]
            puts $permLog "[format %.4f $currentTime],$sampleElem,[lindex $result 0],[lindex $result 1],[lindex $result 2]"
            flush $permLog
        }
    }

    if {[expr $currentStep % 400] == 0} {
        set pct [expr int(100.0 * $currentTime / $totalTime)]
        set elapsed [expr [clock seconds] - $startT]
        if {$useVariablePerm && [info exists ruPrev($sampleElem)]} {
            puts "Progress: $pct% | t=[format %.2f $currentTime]s | ru=[format %.3f $ruPrev($sampleElem)] | ${elapsed}s"
        } else {
            puts "Progress: $pct% | t=[format %.2f $currentTime]s | ${elapsed}s"
        }
    }
}

close $permLog
set endT [clock seconds]

puts ""
puts "=============================================="
puts "ANALYSIS COMPLETE"
puts "=============================================="
puts "Time: [format %.2f $currentTime] s"
puts "Steps: $currentStep"
puts "Duration: [expr $endT - $startT] seconds"
puts "=============================================="
