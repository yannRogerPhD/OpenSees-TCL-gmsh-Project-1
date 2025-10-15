wipe

#-----------------------------------------------------------------------------------------
#  1. DEFINE SOIL AND MESH GEOMETRY
#-----------------------------------------------------------------------------------------

#---SOIL GEOMETRY
# thicknesses of soil profile (m)
set soilThick      30.0
# number of soil layers
set numLayers      3
# layer thicknesses
set layerThick(3)  2.0
set layerThick(2)  8.0
set layerThick(1)  20.0
# depth of water table
set waterTable     2.0

# define layer boundaries
set layerBound(1) $layerThick(1)
for {set i 2} {$i <= $numLayers} {incr i 1} {
    set layerBound($i) [expr $layerBound([expr $i-1])+$layerThick($i)]
}

#---MESH GEOMETRY
# number of elements in horizontal direction
set nElemX  1
# number of nodes in horizontal direction
set nNodeX  [expr 2*$nElemX+1]
# horizontal element size (m)
set sElemX  2.0

# number of elements in vertical direction for each layer
set nElemY(3)  4
set nElemY(2)  16
set nElemY(1)  40
# total number of elements in vertical direction
set nElemT     60
# vertical element size in each layer
for {set i 1} {$i <=$numLayers} {incr i 1} {
    set sElemY($i) [expr $layerThick($i)/$nElemY($i)]
    # puts "size:  $sElemY($i)"
}

# number of nodes in vertical direction
set nNodeY  [expr 2*$nElemT+1]
# total number of nodes
set nNodeT  [expr $nNodeX*$nNodeY]

#-----------------------------------------------------------------------------------------
#  2. CREATE PORE PRESSURE NODES AND FIXITIES
#-----------------------------------------------------------------------------------------
model BasicBuilder -ndm 2 -ndf 3

set ppNodesInfo [open ppNodesInfo.dat w]
set count 1
set layerNodeCount 0
# loop over soil layers
for {set k 1} {$k <= $numLayers} {incr k 1} {
  # loop in horizontal direction
    for {set i 1} {$i <= $nNodeX} {incr i 2} {
      # loop in vertical direction
        if {$k == 1} {
            set bump 1
        } else {
            set bump 0
        }
        for {set j 1} {$j <= [expr 2*$nElemY($k)+$bump]} {incr j 2} {

            set xCoord  [expr ($i-1)*$sElemX/2]
            set yctr    [expr $j + $layerNodeCount]
            set yCoord  [expr ($yctr-1)*$sElemY($k)/2]
            set nodeNum [expr $i + ($yctr-1)*$nNodeX]

            node $nodeNum  $xCoord  $yCoord
            puts "node $nodeNum  $xCoord  $yCoord"

          # output nodal information to data file
            puts $ppNodesInfo "$nodeNum  $xCoord  $yCoord"
            # puts "$ppNodesInfo '$nodeNum  $xCoord  $yCoord'"

          # designate nodes above water table
            set waterHeight [expr $soilThick-$waterTable]
            if {$yCoord>=$waterHeight} {
                set dryNode($count) $nodeNum
                set count [expr $count+1]
            }
        }
    }
    set layerNodeCount [expr $yctr + 1]
}
close $ppNodesInfo
# puts "Finished creating all -ndf 3 nodes..."

# define fixities for pore pressure nodes above water table
for {set i 1} {$i < $count} {incr i 1} {
    fix $dryNode($i)  0 0 1
    # puts "fix $dryNode($i)  0 0 1"
}

# define fixities for pore pressure nodes at base of soil column
fix 1  0 1 0
fix 3  0 1 0
# puts "Finished creating all -ndf 3 boundary conditions..."


# define equal degrees of freedom for pore pressure nodes
for {set i 1} {$i <= [expr 3*$nNodeY-2]} {incr i 6} {
    equalDOF $i [expr $i+2]  1 2
    # puts "equalDOF $i [expr $i+2]  1 2"
}
# puts "Finished creating equalDOF for pore pressure nodes..."

#-----------------------------------------------------------------------------------------
#  3. CREATE INTERIOR NODES AND FIXITIES
#-----------------------------------------------------------------------------------------
model BasicBuilder -ndm 2 -ndf 2

# central column of nodes
set xCoord  [expr $sElemX/2]
# loop over soil layers
set layerNodeCount 0
for {set k 1} {$k <= $numLayers} {incr k 1} {
  # loop in vertical direction
    if {$k == 1} {
        set bump 1
    } else {
        set bump 0
    }
    for {set j 1} {$j <= [expr 2*$nElemY($k)+$bump]} {incr j 1} {

        set yctr    [expr $j + $layerNodeCount]
        set yCoord  [expr ($yctr-1)*$sElemY($k)/2]
        set nodeNum [expr 3*$yctr - 1]

        node  $nodeNum  $xCoord  $yCoord
    }
    set layerNodeCount $yctr
}

# interior nodes on the element edges
# loop over layers
set layerNodeCount 0
for {set k 1} {$k <= $numLayers} {incr k 1} {
  # loop in vertical direction
    for {set j 1} {$j <= $nElemY($k)} {incr j 1} {

        set yctr [expr $j + $layerNodeCount]
        set yCoord   [expr $sElemY($k)*($yctr-0.5)]
        set nodeNumL [expr 6*$yctr - 2]
        set nodeNumR [expr $nodeNumL + 2]

        node  $nodeNumL  0.0  $yCoord
        node  $nodeNumR  $sElemX  $yCoord
    }
    set layerNodeCount $yctr
}
# puts "Finished creating all -ndf 2 nodes..."

# define fixities for interior nodes at base of soil column
fix 2  0 1
# puts "Finished creating all -ndf 2 boundary conditions..."

# define equal degrees of freedom which have not yet been defined
for {set i 1} {$i <= [expr 3*$nNodeY-6]} {incr i 6} {
    equalDOF $i          [expr $i+1]  1 2
    equalDOF [expr $i+3] [expr $i+4]  1 2
    equalDOF [expr $i+3] [expr $i+5]  1 2
}
equalDOF [expr $nNodeT-2] [expr $nNodeT-1]  1 2
# puts "Finished creating equalDOF constraints..."

#-----------------------------------------------------------------------------------------
#  4. CREATE SOIL MATERIALS
#-----------------------------------------------------------------------------------------

# define grade of slope (%)
set grade 2.0
set slope [expr atan($grade/100.0)]
set g -9.81

nDMaterial PressureDependMultiYield02 3 2 1.8 9.0e4 2.2e5 32 0.1 \
                                      101.0 0.5 26 0.067 0.23 0.06 \
                                      0.27 20 5.0 3.0 1.0 \
                                      0.0 0.77 0.9 0.02 0.7 101.0
set thick(3) 1.0
set xWgt(3)  [expr $g*sin($slope)]
set yWgt(3)  [expr $g*cos($slope)]
set uBulk(3) 5e-6
set hPerm(3) 1.0e-4
set vPerm(3) 1.0e-4

nDMaterial PressureDependMultiYield02 2 2 2.24 9.0e4 2.2e5 32 0.1 \
                                      101.0 0.5 26 0.067 0.23 0.06 \
                                      0.27 20 5.0 3.0 1.0 \
                                      0.0 0.77 0.9 0.02 0.7 101.0
set thick(2) 1.0
set xWgt(2)  [expr $g*sin($slope)]
set yWgt(2)  [expr $g*cos($slope)]
set uBulk(2) 5.06e6
set hPerm(2) 1.0e-4
set vPerm(2) 1.0e-4
nDMaterial PressureDependMultiYield02 1 2 2.45 1.3e5 2.6e5 39 0.1 \
                                      101.0 0.5 26 0.010 0.0 0.35 \
                                      0.0 20 5.0 3.0 1.0 \
                                      0.0 0.47 0.9 0.02 0.7 101.0
set thick(1) 1.0
set xWgt(1)  [expr $g*sin($slope)]
set yWgt(1)  [expr $g*cos($slope)]
set uBulk(1) 6.88e6
set hPerm(1) 1.0e-4
set vPerm(1) 1.0e-4
puts "Finished creating all soil materials..."

#-----------------------------------------------------------------------------------------
#  5. CREATE SOIL ELEMENTS
#-----------------------------------------------------------------------------------------

for {set j 1} {$j <= $nElemT} {incr j 1} {

    set nI  [expr 6*$j - 5]
    set nJ  [expr $nI + 2]
    set nK  [expr $nI + 8]
    set nL  [expr $nI + 6]
    set nM  [expr $nI + 1]
    set nN  [expr $nI + 5]
    set nP  [expr $nI + 7]
    set nQ  [expr $nI + 3]
    set nR  [expr $nI + 4]

    set lowerBound 0.0
    for {set i 1} {$i <= $numLayers} {incr i 1} {

        if {[expr $j*$sElemY($i)] <= $layerBound($i) && [expr $j*$sElemY($i)] > $lowerBound} {

          # permeabilities are initially set at 1.0 m/s for gravity analysis, values are updated post-gravity
            element 9_4_QuadUP $j $nI $nJ $nK $nL $nM $nN $nP $nQ $nR \
                           $thick($i) $i $uBulk($i) 1.0 1.0 1.0 $xWgt($i) $yWgt($i)
        }
        set lowerBound $layerBound($i)
    }
}
# puts "Finished creating all soil elements..."

#-----------------------------------------------------------------------------------------
#  6. LYSMER DASHPOT
#-----------------------------------------------------------------------------------------

# define dashpot nodes
set dashF [expr $nNodeT+1]
set dashS [expr $nNodeT+2]

node $dashF  0.0 0.0
node $dashS  0.0 0.0

# define fixities for dashpot nodes
fix $dashF  1 1
fix $dashS  0 1

# define equal DOF for dashpot and base soil node
equalDOF 1 $dashS  1
# puts "Finished creating dashpot nodes and boundary conditions..."

# define dashpot material
set colArea       [expr $sElemX*$thick(1)]
set rockVS        700.0
set rockDen       2.5
set dashpotCoeff  [expr $rockVS*$rockDen]
uniaxialMaterial Viscous [expr $numLayers+1] [expr $dashpotCoeff*$colArea] 1

# define dashpot element
element zeroLength [expr $nElemT+1]  $dashF $dashS -mat [expr $numLayers+1]  -dir 1
# puts "Finished creating dashpot material and element..."

#-----------------------------------------------------------------------------------------
#  7. CREATE GRAVITY RECORDERS
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
#  9. DEFINE ANALYSIS PARAMETERS
#-----------------------------------------------------------------------------------------

#---GROUND MOTION PARAMETERS
# time step in ground motion record
set motionDT     0.005
# number of steps in ground motion record
set motionSteps  7990

#---RAYLEIGH DAMPING PARAMETERS
set pi      3.141592654
# damping ratio
set damp    0.02
# lower frequency
set omega1  [expr 2*$pi*0.2]
# upper frequency
set omega2  [expr 2*$pi*20]
# damping coefficients
set a0      [expr 2*$damp*$omega1*$omega2/($omega1 + $omega2)]
set a1      [expr 2*$damp/($omega1 + $omega2)]
# puts "damping coefficients: a_0 = $a0;  a_1 = $a1"

#---DETERMINE STABLE ANALYSIS TIME STEP USING CFL CONDITION
# maximum shear wave velocity (m/s)
set vsMax       250.0
# duration of ground motion (s)
set duration    [expr $motionDT*$motionSteps]
# minimum element size
set minSize $sElemY(1)
for {set i 2} {$i <= $numLayers} {incr i 1} {
    if {$sElemY($i) < $minSize} {
        set minSize $sElemY($i)
    }
}
# trial analysis time step
set kTrial      [expr $minSize/(pow($vsMax,0.5))]
# define time step and number of steps for analysis
if { $motionDT <= $kTrial } {
    set nSteps  $motionSteps
    set dT      $motionDT
} else {
    set nSteps  [expr int(floor($duration/$kTrial)+1)]
    set dT      [expr $duration/$nSteps]
}
# puts "number of steps in analysis: $nSteps"
# puts "analysis time step: $dT"

#---ANALYSIS PARAMETERS
# Newmark parameters
set gamma  0.5
set beta   0.25

#-----------------------------------------------------------------------------------------
#  10. GRAVITY ANALYSIS
#-----------------------------------------------------------------------------------------

# update materials to ensure elastic behavior
updateMaterialStage -material 1 -stage 0
updateMaterialStage -material 2 -stage 0
updateMaterialStage -material 3 -stage 0

constraints Penalty 1.e14 1.e14
test        NormDispIncr 1e-4 35 1
algorithm   KrylovNewton
numberer    RCM
system      ProfileSPD
integrator  Newmark $gamma $beta
analysis    Transient

set startT  [clock seconds]
analyze     10 5.0e2
# puts "Finished with elastic gravity analysis..."

# update materials to consider plastic behavior
updateMaterialStage -material 1 -stage 1
updateMaterialStage -material 2 -stage 1
updateMaterialStage -material 3 -stage 1

# plastic gravity loading
analyze     40 5.0e-2
# puts "Finished with plastic gravity analysis..."
