set G0 150
set nu 0.05
set e_init1 0.69204737732657
set e_init2 0.60513643659711
set Mc 1.14
set c 0.78
set lambda_c 0.027
set e0 0.83
set ksi 0.45
set P_atm 101.3
set m 0.02
set h0 9.7
set ch 1.02
set nb 2.56
set A0 0.81
set nd 1.05
set z_max 5.0
set cz 800.0
set Den1 2.0255
set Den2 2.0805

set matTagLoose 1
set matTagDense 2
nDMaterial ManzariDafalias $matTagLoose $G0 $nu $e_init1 $Mc $c $lambda_c $e0 $ksi $P_atm $m $h0 $ch $nb $A0 $nd $z_max $cz $Den1
nDMaterial ManzariDafalias $matTagDense $G0 $nu $e_init2 $Mc $c $lambda_c $e0 $ksi $P_atm $m $h0 $ch $nb $A0 $nd $z_max $cz $Den2