# !!!!!!!!!!!!!=======================================================================!!!!!!!!!!!!!
#                    DYNAMIC ANALYSIS WITH ADAPTIVE TIME STEPPING
# !!!!!!!!!!!!!=======================================================================!!!!!!!!!!!!!
#
# Features:
#   - Automatic time step reduction on convergence failure
#   - Time step recovery after consecutive successes
#   - Progress reporting
#   - Variable permeability updates (Shahir & Pak model)
#
# ============================================================================


# ============================================================================
# ADAPTIVE TIME STEPPING PROCEDURE
# ============================================================================
# Features:
#   - Reduces dT on convergence failure (halves each time)
#   - Increases dT after N consecutive successes (doubles, up to dT_max)
#   - Stops if dT falls below dT_min
#   - Reports progress every 100 steps
#
# Usage:
#   set ok [adaptiveAnalyze $totalTime $dT_initial $dT_min $dT_max $N_success]
#   - totalTime:    total duration to analyze (s)
#   - dT_initial:   starting time step (s)
#   - dT_min:       minimum allowed time step (default: dT_initial/64)
#   - dT_max:       maximum allowed time step (default: dT_initial)
#   - N_success:    consecutive successes before increasing dT (default: 10)
# ============================================================================

proc adaptiveAnalyze {totalTime dT_initial {dT_min ""} {dT_max ""} {N_success 10}} {

    # set defaults if not provided
    if {$dT_min eq ""} {set dT_min [expr $dT_initial / 64.0]}
    if {$dT_max eq ""} {set dT_max $dT_initial}

    set dT $dT_initial
    set currentTime [getTime]
    set startTime $currentTime
    set targetTime [expr $currentTime + $totalTime]
    set successCount 0
    set totalSteps 0
    set reductions 0
    set increases 0

    puts ""
    puts "=============================================="
    puts "ADAPTIVE TIME STEPPING"
    puts "=============================================="
    puts "Start time:     [format %.4f $currentTime] s"
    puts "Target time:    [format %.4f $targetTime] s"
    puts "Duration:       $totalTime s"
    puts "Initial dT:     [format %.2e $dT_initial] s"
    puts "Min dT:         [format %.2e $dT_min] s"
    puts "Max dT:         [format %.2e $dT_max] s"
    puts "Success threshold: $N_success steps"
    puts "=============================================="
    puts ""

    set analysisStartT [clock seconds]

    while {$currentTime < [expr $targetTime - 1.0e-12]} {

        # don't overshoot the target time
        if {[expr $currentTime + $dT] > $targetTime} {
            set dT [expr $targetTime - $currentTime]
        }

        # try one step
        set ok [analyze 1 $dT]

        if {$ok == 0} {
            # SUCCESS
            set currentTime [getTime]
            incr successCount
            incr totalSteps

            # try to increase dT after N consecutive successes
            if {$successCount >= $N_success && $dT < [expr $dT_max - 1.0e-12]} {
                set dT_new [expr $dT * 2.0]
                if {$dT_new > $dT_max} {set dT_new $dT_max}
                if {$dT_new > [expr $dT + 1.0e-12]} {
                    set dT $dT_new
                    incr increases
                    puts "  t=[format %.4f $currentTime]s: increasing dT to [format %.2e $dT]"
                }
                set successCount 0
            }

            # progress report every 100 steps
            if {[expr $totalSteps % 100] == 0} {
                set elapsed [expr [clock seconds] - $analysisStartT]
                set pct [expr int(100.0 * ($currentTime - $startTime) / $totalTime)]
                puts "  Progress: $pct% | t=[format %.4f $currentTime]s | dT=[format %.2e $dT] | steps=$totalSteps | ${elapsed}s"
            }

        } else {
            # FAILURE - reduce time step
            set successCount 0
            set dT [expr $dT / 2.0]
            incr reductions

            puts "  t=[format %.4f $currentTime]s: no convergence, reducing dT to [format %.2e $dT]"

            # check if dT is too small
            if {$dT < $dT_min} {
                puts ""
                puts "ERROR: dT below minimum ([format %.2e $dT_min]). Analysis aborted."
                puts "  Total steps completed: $totalSteps"
                puts "  Time reached: [format %.4f $currentTime] s"
                puts ""
                return -1
            }
        }
    }

    set analysisEndT [clock seconds]
    set wallTime [expr $analysisEndT - $analysisStartT]

    # final report
    puts ""
    puts "=============================================="
    puts "ADAPTIVE ANALYSIS COMPLETE"
    puts "=============================================="
    puts "Final time:     [format %.4f $currentTime] s"
    puts "Total steps:    $totalSteps"
    puts "dT reductions:  $reductions"
    puts "dT increases:   $increases"
    puts "Final dT:       [format %.2e $dT] s"
    puts "Wall time:      $wallTime seconds"
    puts "=============================================="
    puts ""

    return 0
}

# ============================================================================
# ANALYSIS PARAMETERS
# ============================================================================

set totalTime    15.0       ;# total analysis duration (s)
set dT_initial   0.0025   ;# initial time step (s)
set dT_min       7.81e-05   ;# minimum time step (s)
set dT_max       5.00e-03   ;# maximum time step (s)
set N_success    100          ;# successes before increasing dT

# ============================================================================
# ANALYSIS SETUP
# ============================================================================

constraints Transformation
test NormDispIncr 0.005 10 1
algorithm KrylovNewton
numberer RCM
system UmfPack
integrator Newmark 0.5 0.25
rayleigh $a0 0.0 $a1 0.0
analysis Transient

# ============================================================================
# ADAPTIVE ANALYSIS WITH VARIABLE PERMEABILITY
# ============================================================================

set permUpdateInterval 60

# wrapper procedure that combines adaptive stepping with permeability updates
proc adaptiveAnalyzeWithPerm {totalTime dT_initial dT_min dT_max N_success permInterval} {
    global firstSSPelem lastSSPelem

    set dT $dT_initial
    set currentTime [getTime]
    set startTime $currentTime
    set targetTime [expr $currentTime + $totalTime]
    set successCount 0
    set totalSteps 0
    set reductions 0
    set increases 0
    set permUpdates 0
    set stepsSincePermUpdate 0

    puts ""
    puts "=============================================="
    puts "ADAPTIVE ANALYSIS + VARIABLE PERMEABILITY"
    puts "=============================================="
    puts "Start time:         [format %.4f $currentTime] s"
    puts "Target time:        [format %.4f $targetTime] s"
    puts "Initial dT:         [format %.2e $dT_initial] s"
    puts "Perm update every:  $permInterval steps"
    puts "=============================================="
    puts ""

    set analysisStartT [clock seconds]

    # output file for permeability evolution
    file mkdir results
    set permLog [open "results/permeability_evolution.csv" w]
    puts $permLog "Time,Steps,dT,Reductions,SampleRu"
    set sampleElem [expr ($firstSSPelem + $lastSSPelem) / 2]

    while {$currentTime < [expr $targetTime - 1.0e-12]} {

        # don't overshoot
        if {[expr $currentTime + $dT] > $targetTime} {
            set dT [expr $targetTime - $currentTime]
        }

        # try one step
        set ok [analyze 1 $dT]

        if {$ok == 0} {
            # SUCCESS
            set currentTime [getTime]
            incr successCount
            incr totalSteps
            incr stepsSincePermUpdate

            # update permeabilities periodically
            if {$stepsSincePermUpdate >= $permInterval} {
                updateAllPermeabilities
                incr permUpdates
                set stepsSincePermUpdate 0
            }

            # try to increase dT
            if {$successCount >= $N_success && $dT < [expr $dT_max - 1.0e-12]} {
                set dT_new [expr $dT * 2.0]
                if {$dT_new > $dT_max} {set dT_new $dT_max}
                if {$dT_new > [expr $dT + 1.0e-12]} {
                    set dT $dT_new
                    incr increases
                    puts "  t=[format %.4f $currentTime]s: increasing dT to [format %.2e $dT]"
                }
                set successCount 0
            }

            # progress report
            if {[expr $totalSteps % 100] == 0} {
                set elapsed [expr [clock seconds] - $analysisStartT]
                set pct [expr int(100.0 * ($currentTime - $startTime) / $totalTime)]

                # get sample ru value
                global ruPrev
                if {[info exists ruPrev($sampleElem)]} {
                    set sampleRu $ruPrev($sampleElem)
                    puts "  Progress: $pct% | t=[format %.4f $currentTime]s | dT=[format %.2e $dT] | ru=[format %.3f $sampleRu] | ${elapsed}s"
                    puts $permLog "[format %.4f $currentTime],$totalSteps,[format %.2e $dT],$reductions,[format %.4f $sampleRu]"
                } else {
                    puts "  Progress: $pct% | t=[format %.4f $currentTime]s | dT=[format %.2e $dT] | ${elapsed}s"
                    puts $permLog "[format %.4f $currentTime],$totalSteps,[format %.2e $dT],$reductions,0.0"
                }
                flush $permLog
            }

        } else {
            # FAILURE
            set successCount 0
            set dT [expr $dT / 2.0]
            incr reductions

            puts "  t=[format %.4f $currentTime]s: no convergence, reducing dT to [format %.2e $dT]"

            if {$dT < $dT_min} {
                puts ""
                puts "ERROR: dT below minimum. Analysis aborted."
                close $permLog
                return -1
            }
        }
    }

    close $permLog
    set wallTime [expr [clock seconds] - $analysisStartT]

    puts ""
    puts "=============================================="
    puts "ANALYSIS COMPLETE"
    puts "=============================================="
    puts "Final time:         [format %.4f $currentTime] s"
    puts "Total steps:        $totalSteps"
    puts "dT reductions:      $reductions"
    puts "dT increases:       $increases"
    puts "Perm updates:       $permUpdates"
    puts "Wall time:          $wallTime seconds"
    puts "=============================================="
    puts ""

    return 0
}

# run the analysis
puts "Starting adaptive analysis with variable permeability..."
set ok [adaptiveAnalyzeWithPerm $totalTime $dT_initial $dT_min $dT_max $N_success $permUpdateInterval]

if {$ok != 0} {
    puts "Analysis failed to complete!"
} else {
    puts "Analysis completed successfully."
}
