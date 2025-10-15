wipe

set thickX 0.2
set nu 0.0
set matTag 1
set rhoS 1.7
set VsS 250
set rhoB 2.4
set VsB 760
set G [expr {$rhoS * pow($VsS, 2)}]
set E [expr {2 * $G * (1 + $nu)}]
set K [expr {$E / (3 * (1 - 2 * $nu))}]

set mC [expr {$thickX * $VsB * $rhoB}]
set mC2 [expr {$mC}]

set motionSteps 7990

set dashTagL 2000
set dashTagR 2001
set matZeroLengthTag 3000
set elementZeroLengthTag 4000

source nodes2D.tcl
node $dashTagL 0.0 0.0
node $dashTagR 0.0 0.0

source fixity2D.tcl
fix $dashTagL 1 1
fix $dashTagR 0 1

source equalDOFs2D.tcl
source equalDOFs2DBottom.tcl
equalDOF 1 $dashTagR 1

# nDMaterial ElasticIsotropic $matTag $E $nu $rhoS
source matModelParams.tcl
nDMaterial PressureIndependMultiYield $matTag $nd $rho $refShearModul $refBulkModul $cohesion $peakShearStra \
                                      $frictionAng $refPress $pressDependCoe $noYieldSurf
uniaxialMaterial Viscous $matZeroLengthTag $mC2 1

source elements.tcl
element zeroLength $elementZeroLengthTag $dashTagL $dashTagR -mat $matZeroLengthTag -dir 1

constraints Transformation
numberer RCM
integrator LoadControl 0.1
algorithm Newton
system ProfileSPD
test NormDispIncr 1.0e-5 30 1
# analysis Static
analysis Transient

analyze 10 5.0e2

updateMaterialStage -material 1 -stage 1

analyze 40 5.0e2

setTime 0.0
wipeAnalysis

set timeSeriesTag 1004
set dt 0.005
set seismicInput velHistory.out
# set seismicInput rickerVelocity.txt

timeSeries Path $timeSeriesTag -dt $dt -filePath $seismicInput -factor $mC2

set plainPatterTag 1005
pattern Plain $plainPatterTag $timeSeriesTag {
    load 1 1.0 0.0
}

set topNode 3
set botNode 1

recorder Node -file velTopResults.out -time -node $topNode -dof 1 vel
recorder Node -file velBotResults.out -time -node $botNode -dof 1 vel

recorder Node -file accelTopResults.out -time -node $topNode -dof 1 2 accel

set damp 0.02
set pi 3.141592654
set fLower 0.2
set fHigher 20.0

set omega1 [expr {2 * $pi * $fLower}]
set omega2 [expr {2 * $pi * $fHigher}]

set a0 [expr {2 * $damp * $omega1 * $omega2 / ($omega1 + $omega2)}]
set a1 [expr {2 * $damp / ($omega1 + $omega2)}]

constraints Transformation
numberer RCM
algorithm Newton
system ProfileSPD
integrator Newmark 0.5 0.25
analysis Transient
rayleigh $a0 $a1 0.0 0.0
test NormDispIncr 1.0e-3 15 1

analyze $motionSteps $dt
