set E 3000000000.0
set poiss 0.3
set rho 2100.0
set thickness 1.0
set G [expr $E/(2.0*(1.0+$poiss))]
# time increment
set dt 0.001
# predominant frequency of the Ricker Wavelet
set freq 10.0
# total duration of the dynamic analysis
set duration 1.0
