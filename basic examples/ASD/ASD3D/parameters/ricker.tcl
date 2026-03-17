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
