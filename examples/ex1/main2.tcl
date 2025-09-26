wipe

set zeroLengthElementTag 3000
set zeroLengthMaterialTag 2
set dashpotL 2000
set dashpotR 2001
set rhoB 2000
set VsB 1010
set mC [expr 0.5*$rhoB*$VsB]


# Soil material
set matSoil 1
set rhoS 1755
set VsS 230.9
set nu 0.0
set E_S [expr 2.0 * $rhoS * pow($VsS, 2)]

source nodes2D.tcl
node $dashpotL 0.000 0.000
node $dashpotR 0.000 0.000

source fixity2D.tcl
fix $dashpotL 1 1
fix $dashpotR 0 1

source equalDOFs2D.tcl
equalDOF 1 $dashpotR 1
equalDOF 1 2 1

# source materials.tcl
nDMaterial ElasticIsotropic $matSoil $E_S $nu $rhoS

# Bedrock material
uniaxialMaterial Viscous $zeroLengthMaterialTag $mC 1

source elements.tcl
element zeroLength $zeroLengthElementTag $dashpotL $dashpotR -mat $zeroLengthMaterialTag -dir 1


# Define analysis parameters
constraints Transformation
numberer RCM
system BandGeneral
test NormDispIncr 1.0e-6 20
algorithm Newton
integrator LoadControl 1 1 1 1
analysis Static

# Run until load = 1.0
analyze 2


reactions

setTime 0.0
wipeAnalysis

set r1 [nodeReaction 1 2]
set r2 [nodeReaction 2 2]
set r3 [nodeReaction $dashpotR 2]

# puts "$r1"
# puts "$r2"
# puts "$r3"

set dt 0.001
timeSeries Path 2 -dt $dt -filePath "rickerInputVelocity.txt" -factor $mC

pattern Plain 2 2 {
    load 1 1.0 0.0
    load 2 1.0 0.0
}

set topNode 3
set baseNode 1

recorder Node -file surfAcc.out -time -node $topNode -dof 1 accel
recorder Node -file baseAcc.out -time -node $baseNode -dof 1 accel

constraints Transformation
numberer RCM
system BandGeneral
test NormDispIncr 1.0e-6 20 1
algorithm Newton
integrator Newmark 0.625 0.375
analysis Transient

analyze 10000 $dt
