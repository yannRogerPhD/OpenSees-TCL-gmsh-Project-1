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
test        NormDispIncr 1.0e-8 20

analysis    Static

set ok 0
set nStaticSteps 10

for {set i 1} {$i <= $nStaticSteps} {incr i} {
    set ok [analyze 1]
    if {$ok != 0} {
        puts "Gravity analysis step $i failed"
        break
    }
}

if {$ok == 0} {
    puts "Gravity analysis has been successful"
}

# make sure reactions are assembled
reactions

# get list of nodes
set nodes [getNodeTags]

# sum vertical reactions and applied vertical nodal loads
set sumReact 0.0
set sumApplied 0.0
foreach n $nodes {
    # DOF numbering: in 2D frames typical order is 1=UX, 2=UY, 3=RZ
    set r [nodeReaction $n 2]        ;# reaction at DOF 2 (vertical)
    set u [nodeUnbalance $n 2]      ;# unbalanced force (applied) at DOF 2
    set sumReact [expr {$sumReact + $r}]
    set sumApplied [expr {$sumApplied + $u}]
}
puts "Total vertical reaction = $sumReact"
puts "Total vertical applied (unbalance) = $sumApplied"
puts "Difference (React - Applied) = [expr {$sumReact - $sumApplied}]"
