wipe

source nodes2D.tcl

set matTag 1
set E 3000000000.0
set poisson 0.3
set rho 2100.0

nDMaterial ElasticIsotropic $matTag $E $poisson $rho


set dt 0.001
# predominant frequency of the Ricker Wavelet
set freq 10.0
# total duration of the dynamic analysis
set duration 1.0
set pi [expr acos(-1.0)]
set wl [expr sqrt(3.0/2.0)/$pi/$freq*10.0]
set ndiv [expr int($wl/$dt)]
set dt [expr $wl/$ndiv.0]
set ts_vals {}
for {set i 0} {$i < $ndiv} {incr i} {
    set ix [expr $i.0*$dt-$wl/2.0]
    set iy [expr $ix*exp(-$pi*$pi*$freq*$freq*$ix*$ix)]
    lappend ts_vals $iy
}
set tsX 1
timeSeries Path $tsX -dt $dt -values $ts_vals  -factor 9.806

source elements.tcl

constraints Transformation
numberer RCM
system UmfPack
test NormUnbalance 0.0001 10 1
algorithm Newton
integrator LoadControl 1.0
analysis Static
set ok [analyze 1]
if {$ok != 0} {
    error "Gravity analysis failed"
}
loadConst -time 0.0
wipeAnalysis

source updateASD.tcl

# recorders
set soil_base 20
set soil_top 180
recorder Node -file "soil_base.txt" -time -node $soil_base -dof 1 accel
recorder Node -file "soil_top.txt" -time -node $soil_top -dof 1 accel

# Dynamic analysis
# The absorbing boundaries now are in STAGE 0, so they act as constraints
constraints Transformation
numberer RCM
system UmfPack
test NormUnbalance 0.0001 10 1
algorithm Newton
integrator TRBDF2
analysis Transient
set nsteps [expr int($duration/$dt)]
set dt [expr $duration/$nsteps.0]
set ok [analyze $nsteps $dt]
if {$ok != 0} {
    error "Dynamic analysis failed"
}
