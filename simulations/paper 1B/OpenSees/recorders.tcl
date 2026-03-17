# ============================================================
# recorders_all.tcl
# ============================================================

file mkdir Results
file mkdir Results/Pile
file mkdir Results/Soil
file mkdir Results/Superstructure
file mkdir Results/Settlement

# ----------------------------
# Pile nodes (all depths provided)
# ----------------------------
set pileNodes {586 2276 2277 2278 2279 2280 2281 2282 2283 2284 2285 2286 2287 2288 2289 2290 587 2291 2292 2293 588}

# --------------------------------------------------------------
# Pile elements (dispBeamColumn3D)
# --------------------------------------------------------------
set pileEles {3804 3805 3806 3807 3808 3809 3810 3811 3812 3813 3814 3815 3816 3817 3818 3819 3820 3821 3822 3823}

# ============================================================
# A) PILE: LATERAL DISPLACEMENT vs depth (time histories)
# ============================================================
# UX, UY for each pile node. Post-process to get max with depth.
recorder Node -file Results/Pile/pileDisp_UxUy.out -time -node {*}$pileNodes -dof 1 2 disp

# ============================================================
# B) PILE: BENDING MOMENT (via local end forces)
# ============================================================
# localForce contains end forces/moments in local system (includes My, Mz).
# Post-process to get max bending moment vs depth.
recorder Element -file Results/Pile/pileEle_localForce.out -time -ele {*}$pileEles localForce

# ============================================================
# C) SUPERSTRUCTURE: TOP NODE (588) ACCELERATION TIME HISTORY
# ============================================================
# Relative acceleration in global X/Y/Z
recorder Node -file Results/Superstructure/topNode588_accel_XYZ.out -time -node 588 -dof 1 2 3 accel

# ============================================================
# D) SOIL: PWP TIME HISTORIES
# ============================================================
# Provided PWP nodes: 2m->703, 4m->707, 6m->711, 21m->1341
# PWP DOF confirmed as 4
set pwpNodes {703 707 711 1341}
set pwpDOF 4
recorder Node -file Results/Soil/PWP_nodes_703_707_711_1341.out -time -node {*}$pwpNodes -dof $pwpDOF disp

# ============================================================
# E) SOIL: SETTLEMENT TIME HISTORY at node 3132
# ============================================================
# Vertical axis is Z => vertical displacement is DOF 3
set settlementNode 3132
set settlementVertDOF 3
recorder Node -file Results/Settlement/settlement_node3132_Uz.out -time -node $settlementNode -dof $settlementVertDOF disp

# ============================================================
# F) SUPERSTRUCTURE: BENDING MOMENT TIME HISTORY
# ============================================================
# Using the same dispBeamColumn elements you listed.
# localForce contains end moments; post-process to extract bending moment history.
set superEles $pileEles
recorder Element -file Results/Superstructure/superEle_localForce.out -time -ele $superEles localForce
