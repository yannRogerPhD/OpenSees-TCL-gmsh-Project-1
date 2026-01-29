# ================================================================================================
# ZeroLengthContactASDimplex for Pile Interface
# Adds friction, gap opening, slip behavior
# ===============================================================================================

set Kn 1.000000e+04  ;# Normal stiffness
set Kt 5.000000e+02  ;# Tangential stiffness
set mu 0.466805      ;# Friction coefficient

element zeroLengthContactASDimplex 8000000 586 1507 $Kn $Kt $mu -orient 1.000000 0.000000 0.000000

element zeroLengthContactASDimplex 8000001 587 77 $Kn $Kt $mu -orient 1.000000 0.000000 0.000000

element zeroLengthContactASDimplex 8000002 2276 193 $Kn $Kt $mu -orient 1.000000 0.000000 0.000000

element zeroLengthContactASDimplex 8000003 2277 1171 $Kn $Kt $mu -orient 1.000000 0.000000 0.000000

element zeroLengthContactASDimplex 8000004 2278 1171 $Kn $Kt $mu -orient 1.000000 0.000000 0.000000

element zeroLengthContactASDimplex 8000005 2279 1172 $Kn $Kt $mu -orient 1.000000 0.000000 0.000000

element zeroLengthContactASDimplex 8000006 2280 1173 $Kn $Kt $mu -orient 1.000000 0.000000 0.000000

element zeroLengthContactASDimplex 8000007 2281 78 $Kn $Kt $mu -orient 1.000000 0.000000 0.000000

element zeroLengthContactASDimplex 8000008 2282 78 $Kn $Kt $mu -orient 1.000000 0.000000 0.000000

element zeroLengthContactASDimplex 8000009 2283 805 $Kn $Kt $mu -orient 1.000000 0.000000 0.000000

element zeroLengthContactASDimplex 8000010 2284 805 $Kn $Kt $mu -orient 1.000000 0.000000 0.000000

element zeroLengthContactASDimplex 8000011 2285 806 $Kn $Kt $mu -orient 1.000000 0.000000 0.000000

element zeroLengthContactASDimplex 8000012 2286 806 $Kn $Kt $mu -orient 1.000000 0.000000 0.000000

element zeroLengthContactASDimplex 8000013 2287 807 $Kn $Kt $mu -orient 1.000000 0.000000 0.000000

element zeroLengthContactASDimplex 8000014 2288 807 $Kn $Kt $mu -orient 1.000000 0.000000 0.000000

element zeroLengthContactASDimplex 8000015 2289 808 $Kn $Kt $mu -orient 1.000000 0.000000 0.000000

element zeroLengthContactASDimplex 8000016 2290 808 $Kn $Kt $mu -orient 1.000000 0.000000 0.000000

