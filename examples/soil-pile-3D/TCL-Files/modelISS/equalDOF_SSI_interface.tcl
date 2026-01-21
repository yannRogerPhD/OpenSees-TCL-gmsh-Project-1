# =================================================================================================
# SSI pile-soil interface constraints/elements
# =================================================================================================

# Interface material (ElasticPP)
uniaxialMaterial ElasticPP 990001 2000.0 0.04

node 86 0.000000 0.000000 -0.125000
node 87 0.000000 0.000000 -0.125000
element dispBeamColumn 158 40 86 5 1 1
equalDOF 87 82 1 2 3
equalDOF 87 83 1 2 3
equalDOF 87 84 1 2 3
equalDOF 87 85 1 2 3
element zeroLength 159 86 87 -mat 990001 990001 990001 -dir 1 2 3

node 88 0.000000 0.000000 -0.250000
node 89 0.000000 0.000000 -0.250000
element dispBeamColumn 160 9 88 5 1 1
equalDOF 89 78 1 2 3
equalDOF 89 79 1 2 3
equalDOF 89 80 1 2 3
equalDOF 89 81 1 2 3
element zeroLength 161 88 89 -mat 990001 990001 990001 -dir 1 2 3

node 90 0.000000 0.000000 0.000000
node 91 0.000000 0.000000 0.000000
element dispBeamColumn 162 10 90 5 1 1
equalDOF 91 70 1 2 3
equalDOF 91 71 1 2 3
equalDOF 91 72 1 2 3
equalDOF 91 73 1 2 3
element zeroLength 163 90 91 -mat 990001 990001 990001 -dir 1 2 3

