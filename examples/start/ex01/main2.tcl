wipe

set matSoilTag 1
set matZeroElmTag 2
set zeroElmTag 1000

set poisson 0.0
set VsSoil 230.9
set rhoSoil 1755
set GSoil [expr {$rhoSoil * pow($VsSoil, 2)}]
set ESoil [expr {2 * $GSoil * (1 + $poisson)}]

set VsRock 1010
set rhoRock 2000
set thickX 10.0
set mC [expr {$thickX * $VsRock * $rhoRock}]

set dashpotL 2000
set dashpotR 2001

source nodes2D.tcl
node $dashpotL 0.0 0.0
node $dashpotR 0.0 0.0

source fixity2D.tcl
fix $dashpotL 1 1
fix $dashpotR 0 1

nDMaterial ElasticIsotropic $matSoilTag $ESoil $poisson $rhoSoil
uniaxialMaterial Viscous $matZeroElmTag $mC 1

source elements.tcl
element zeroLength $zeroElmTag $dashpotL $dashpotR -mat $matZeroElmTag -dir 1

source equalDOFs2D.tcl
source equalDOFs2DBottom.tcl
equalDOF 1 $dashpotR 1

constraints Transformation
numberer RCM
algorithm Newton
integrator LoadControl 0.1
system ProfileSPD
analysis Static
test NormDispIncr 1.0e-6 20 0

analyze 10

setTime 0.0
wipeAnalysis

set tsX 11
set dt 0.001
set mCc [expr {2 * $mC}]
timeSeries Path $tsX -dt $dt -filePath "rickerInputVelocity.txt" -factor $mC
# timeSeries Path $tsX -dt $dt -filePath "rickerInputVelocity.txt" -factor 2

set patternTag 20
pattern Plain $patternTag $tsX {
    load 1 1.0 0.0
    # load 2 1.0 0.0
    # load 5 1.0 0.0
}

set topNode 3
set botNode 1

recorder Node -file velTop.out -time -node $topNode -dof 1 vel
recorder Node -file velBot.out -time -node $botNode -dof 1 vel

recorder Node -file accelTop.out -time -node $topNode -dof 1 accel

constraints Transformation
numberer RCM
system BandGeneral
test NormDispIncr 1.0e-6 20 1
algorithm Newton
integrator Newmark 0.5 0.25
rayleigh 0.0 0.0 0.000 0.
analysis Transient

analyze 10000 $dt
