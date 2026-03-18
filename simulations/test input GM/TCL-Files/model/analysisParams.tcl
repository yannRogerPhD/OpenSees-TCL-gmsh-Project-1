# analysis parameters

set motionDT 0.005
set motionSteps 7990

set pi 3.141592653589793
set damp 0.02
set fLower 0.2
set fHigher 20.0
set omega1 [expr 2.0*$pi*$fLower]
set omega2 [expr 2.0*$pi*$fHigher]
set a0 [expr 2*$damp*$omega1*$omega2/($omega1 + $omega2)]
set a1 [expr 2*$damp/($omega1 + $omega2)]

set vsMax 250.0
set duration [expr $motionSteps*$motionDT]

set minSize 0.5

set kTrial      [expr $minSize/(pow($vsMax,0.5))]
if { $motionDT <= $kTrial } {
    set nSteps  $motionSteps
    set dT      $motionDT
} else {
    set nSteps  [expr int(floor($duration/$kTrial)+1)]
    set dT      [expr $duration/$nSteps]
}

# Newmark parameters
set gamma  0.5
set beta   0.25