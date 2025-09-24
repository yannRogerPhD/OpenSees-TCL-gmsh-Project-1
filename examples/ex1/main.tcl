wipe

source nodes2D.tcl
source fixity2D.tcl
source materials.tcl
source elements.tcl
source updateMat.tcl
source equalDOFs2D.tcl

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
