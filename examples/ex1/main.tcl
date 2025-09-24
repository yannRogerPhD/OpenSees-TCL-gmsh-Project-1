wipe

source nodes2D.tcl
source fixity2D.tcl
source materials.tcl
source elements.tcl
source updateMat.tcl
source equalDOFs2D.tcl

source updateMat.tcl

system      ProfileSPD
constraints Transformation
integrator  LoadControl 0.1
algorithm   Newton
numberer    RCM
test        NormDispIncr 1.0e-8 20 0

analysis    Static

set ok 0
set nSSteps 10

for {set i 1} {$i <= $nSSteps} {incr i} {
    set ok [analyze 1]
    if {$ok != 0} {
        puts "gravity step $i failed"
        break
    }
}

if {$ok == 0} {
    puts "gravity analysis went on successfully"
}

reactions

set reactionN1 [nodeReaction 1 2]

set nodes [getNodeTags]

set sumReactions 0
foreach n $nodes {
    set r [nodeReaction $n 2]
    set sumReactions [expr $sumReactions + $r]
    }

puts "$sumReactions"

setTime 0.0
wipeAnalysis

# we proceed to perform dynamic analysis
set timeSeriesTag 200
set period 1
set cFactor 9.806
timeSeries Sine $timeSeriesTag 0 10 $period -factor $cFactor

set accelTag 1000
pattern UniformExcitation $accelTag 1 -accel $timeSeriesTag


# pattern UniformExcitation applies to all nodes that are
# kinematically restrained (fixed) in the excitation direction.

constraints Penalty 1.0e18 1.0e18
test NormDispIncr 1.e-12 25 0
algorithm Newton
numberer RCM
system ProfileSPD
rayleigh $massProportionalDamping 0.0 $stiffnessProportionalDamping 0.
integrator Newmark $gamma  [expr pow($gamma+0.5, 2)/4]
analysis VariableTransient

#create the recorder
recorder Node -file disp.out   -time  -node 1 2 3 4 -dof 1 2 -dT  0.01 disp
recorder Node -file accel.out  -time  -node 1 2 3 4 -dof 1 2 -dT 0.01 accel
recorder Element -ele 1 -time -file stress1.out -dT 0.01 material 1 stress
recorder Element -ele 1 -time -file strain1.out -dT 0.01 material 1 strain
recorder Element -ele 1 -time -file stress3.out -dT 0.01 material 3 stress
recorder Element -ele 1 -time -file strain3.out -dT 0.01 material 3 strain

#analyze
set startT [clock seconds]
analyze $numSteps $deltaT [expr $deltaT/100] $deltaT 10
set endT [clock seconds]
puts "Execution time: [expr $endT-$startT] seconds."

wipe  #flush output stream