proc updateAllPermeabilities {} {
    global firstSSPelem lastSSPelem
    global alpha beta1 beta2 sigmaV0 ruPrev elemKinit

    set ruThreshold 0.02   ;# Only update if ru changed by more than 2%
    set minRu 0.005        ;# Skip elements with ru below this

    for {set e $firstSSPelem} {$e <= $lastSSPelem} {incr e} {

        # Get pore pressure
        set pwp [getElementPWP $e]

        # Calculate ru
        if {$sigmaV0($e) > 0.0} {
            set ru [expr {abs($pwp) / $sigmaV0($e)}]
        } else {
            continue
        }
        if {$ru > 1.0} {set ru 1.0}

        # SKIP if ru is negligible
        if {$ru < $minRu && $ruPrev($e) < $minRu} {
            continue
        }

        # SKIP if ru hasn't changed much
        set ruChange [expr {abs($ru - $ruPrev($e))}]
        if {$ruChange < $ruThreshold} {
            continue
        }

        # Calculate new permeability
        if {$ru >= $ruPrev($e)} {
            set kRatio [expr {1.0 + ($alpha - 1.0) * pow($ru, $beta1)}]
        } else {
            set kRatio [expr {1.0 + ($alpha - 1.0) * pow($ru, $beta2)}]
        }
        set kNew [expr {$elemKinit($e) * $kRatio}]

        # Update element (all 3 directions)
        setParameter -value $kNew -ele $e xPerm
        setParameter -value $kNew -ele $e yPerm
        setParameter -value $kNew -ele $e zPerm

        set ruPrev($e) $ru
    }
}
