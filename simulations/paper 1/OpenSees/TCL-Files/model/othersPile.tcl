# --------------------------------------------------------
# Steel pipe pile (prototype) per Rahmani & Pak (2012)
# D = 0.67 m, t = 19 mm
# Ep = 3.0e7 kPa, nu = 0.2
# Units consistent with kN-m-s (so kPa = kN/m^2)
# --------------------------------------------------------

set numIntgrPts   5
set secTag        1
set transfTag     1

set pi        3.141593
set D         0.67          ;# outer diameter (m)
set tWall     0.019         ;# wall thickness (m)
set Di        [expr $D - 2.0*$tWall]

# material
set Epile     3.0e10        ;# kPa
set nuP       0.2
set Gpile     [expr $Epile/(2.0*(1.0+$nuP))]

# hollow circular section
set Area      [expr $pi/4.0  * (pow($D,2) - pow($Di,2))]
set Iy        [expr $pi/64.0 * (pow($D,4) - pow($Di,4))]
set Iz        $Iy
set J         [expr $pi/32.0 * (pow($D,4) - pow($Di,4))]

# geometric transformation (choose vecxz not parallel to pile axis)
# typical for a vertical pile along global Z:
geomTransf PDelta $transfTag  1.0 0.0 0.0

# elastic section
section Elastic $secTag $Epile $Area $Iz $Iy $Gpile $J
