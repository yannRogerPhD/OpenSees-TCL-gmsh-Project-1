# !!!!!!!!!=========!!!!!!!!!=========!!!!!!!!!=========!!!!!!!!!=========!!!!!!!!!=======!!!!!!!!!
# ZeroLengthContactASDimplex for Structure-Soil Interface (2D)
# !!!!!!!!!=========!!!!!!!!!=========!!!!!!!!!=========!!!!!!!!!=========!!!!!!!!!=======!!!!!!!

set Kn 1.000000e+04  ;# Normal stiffness
set Kt 5.000000e+02  ;# Tangential stiffness
set mu 0.466805      ;# Friction coefficient

element zeroLengthContactASDimplex 8000000 5 78 $Kn $Kt $mu -orient -1.000000 0.000000 0.000000

element zeroLengthContactASDimplex 8000001 6 102 $Kn $Kt $mu -orient 1.000000 0.000000 0.000000

element zeroLengthContactASDimplex 8000002 41 79 $Kn $Kt $mu -orient -1.000000 0.000000 0.000000

element zeroLengthContactASDimplex 8000003 42 80 $Kn $Kt $mu -orient -1.000000 0.000000 0.000000

element zeroLengthContactASDimplex 8000004 43 81 $Kn $Kt $mu -orient -1.000000 0.000000 0.000000

element zeroLengthContactASDimplex 8000005 44 82 $Kn $Kt $mu -orient -1.000000 0.000000 0.000000

element zeroLengthContactASDimplex 8000006 45 27 $Kn $Kt $mu -orient -1.000000 0.000000 0.000000

element zeroLengthContactASDimplex 8000007 49 103 $Kn $Kt $mu -orient 1.000000 0.000000 0.000000

element zeroLengthContactASDimplex 8000008 50 104 $Kn $Kt $mu -orient 1.000000 0.000000 0.000000

element zeroLengthContactASDimplex 8000009 51 105 $Kn $Kt $mu -orient 1.000000 0.000000 0.000000

element zeroLengthContactASDimplex 8000010 52 106 $Kn $Kt $mu -orient 1.000000 0.000000 0.000000

element zeroLengthContactASDimplex 8000011 53 30 $Kn $Kt $mu -orient 1.000000 0.000000 0.000000

