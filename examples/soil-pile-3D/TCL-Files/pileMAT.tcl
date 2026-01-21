# creating pile elements
set numIntgrPts   5
set secTag        1
set transfTag     1
set diameter      1.5 ; # pile diameter (m)
set radius        [expr $diameter/2.]
set pi            3.141593
set Epile         1e10
set nu            0.3
set Gpile         [expr $Epile/(2*(1+$nu))]
set Area          [expr ($diameter**2)*$pi/2.]
set Iy            [expr ($diameter**4)*$pi/64.]
set Iz            [expr ($diameter**4)*$pi/64.]
set J             [expr ($diameter**4)*$pi/32.]

# geomTransf PDelta $transfTag $vecxzX $vecxzY $vecxzZ
geomTransf   PDelta $transfTag  -1.0   0.0     0.0

# section Elastic $secTag $E $A $Iz $Iy $G $J
section Elastic $secTag $Epile $Area $Iz $Iy $Gpile $J
