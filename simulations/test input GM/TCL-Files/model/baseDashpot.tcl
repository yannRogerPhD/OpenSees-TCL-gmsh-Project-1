# dashpot definition

model BasicBuilder -ndm 3 -ndf 3
set dashF 3000
set dashX 3001
set dashY 3002
set matTagViscous 40000

node $dashF -1.0 -1.0 -30.0
node $dashX -1.0 -1.0 -30.0
node $dashY -1.0 -1.0 -30.0

fix $dashF 1 1 1
fix $dashX 0 1 1
fix $dashY 1 0 1

equalDOF 1 $dashX 1
equalDOF 1 $dashY 2

set sizeElX 2.0
set sizeElY 2.0

set colA [expr $sizeElX*$sizeElY]
set rockVS 700.0
set rockDen 2.5
set dashpotCoeff [expr $rockDen*$rockVS*$colA]

uniaxialMaterial Viscous $matTagViscous $dashpotCoeff 1

element zeroLength 3003 $dashF $dashX -mat $matTagViscous -dir 1
element zeroLength 3004 $dashF $dashY -mat $matTagViscous -dir 2