wipe

set thickX 10
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

nDMaterial ElasticIsotropic $matTag $E $nu $rhoS
uniaxialMaterial Viscous $matZeroLengthTag $mC 1

source elements.tcl
element zeroLength $elementZeroLengthTag $dashTagL $dashTagR -mat $matZeroLengthTag -dir 1

constraints Transformation
numberer RCM
integrator LoadControl 0.1
algorithm Newton
system ProfileSPD
test NormDispIncr 1.0e-6 15 0
analysis Static

analyze 10

setTime 0.0
wipeAnalysis

set timeSeriesTag 1004
set dt 0.005
set seismicInput velHistory.out

timeSeries Path $timeSeriesTag -dt $dt -filePath $seismicInput -factor $mC

set plainPatterTag 1005
pattern Plain $plainPatterTag $timeSeriesTag {
    load 1 1.0 0.0
}

set topNode 3
set botNode 1

recorder Node -file velTopResults.out -time -node $topNode -dof 1 vel
recorder Node -file velBotResults.out -time -node $botNode -dof 1 vel

constraints Transformation
numberer RCM
algorithm Newton
system ProfileSPD
integrator Newmark 0.5 0.25
analysis Transient

analyze $motionSteps $dt
