# ============================================================================
# variable permeability data
# ============================================================================
# Based on Shahir & Pak (2009) / Rahmani & Pak (2012)
#
# Formula: k/k_init = 1 + (alpha - 1) * ru^beta
#   where ru = Δu / σ'v0 (excess pore pressure ratio)
#
# Soil parameters:
#   material 1: gamma_sat=19.87 kN/m³, gamma'=9.87 kN/m³
#   material 2: gamma_sat=20.41 kN/m³, gamma'=10.41 kN/m³
#   gamma_water = 10.0 kN/m³
#   surface elevation = 0.00 m
#   water table depth = 0.0 m
# ============================================================================

# parameters
set alpha  20.0     ;# maximum permeability ratio at full liquefaction
set beta1   1.0    ;# exponent during pore pressure buildup
set beta2   8.9    ;# exponent during consolidation

# SSPbrickUP element range
set firstSSPelem 9104
set lastSSPelem 10895
set numSSPelems 1792

# ============================================================================
# element data
# ============================================================================

# Element 9104: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9104) {2294 589 1 598 3234 2302 609 2318}
set elemKinit(9104) 6.169692025290639e-06
set sigmaV0(9104) 88.830000
set ruPrev(9104) 0.0

# Element 9105: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9105) {3234 2302 609 2318 3235 2306 610 2319}
set elemKinit(9105) 6.169692025290639e-06
set sigmaV0(9105) 88.830000
set ruPrev(9105) 0.0

# Element 9106: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9106) {3235 2306 610 2319 2298 599 5 608}
set elemKinit(9106) 6.169692025290639e-06
set sigmaV0(9106) 88.830000
set ruPrev(9106) 0.0

# Element 9107: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9107) {594 2294 598 4 2310 3234 2318 613}
set elemKinit(9107) 6.169692025290639e-06
set sigmaV0(9107) 88.830000
set ruPrev(9107) 0.0

# Element 9108: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9108) {2310 3234 2318 613 2314 3235 2319 614}
set elemKinit(9108) 6.169692025290639e-06
set sigmaV0(9108) 88.830000
set ruPrev(9108) 0.0

# Element 9109: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9109) {2314 3235 2319 614 604 2298 608 8}
set elemKinit(9109) 6.169692025290639e-06
set sigmaV0(9109) 88.830000
set ruPrev(9109) 0.0

# Element 9110: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9110) {2295 590 589 2294 3236 2303 2302 3234}
set elemKinit(9110) 6.169692025290639e-06
set sigmaV0(9110) 69.090000
set ruPrev(9110) 0.0

# Element 9111: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9111) {3236 2303 2302 3234 3237 2307 2306 3235}
set elemKinit(9111) 6.169692025290639e-06
set sigmaV0(9111) 69.090000
set ruPrev(9111) 0.0

# Element 9112: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9112) {3237 2307 2306 3235 2299 600 599 2298}
set elemKinit(9112) 6.169692025290639e-06
set sigmaV0(9112) 69.090000
set ruPrev(9112) 0.0

# Element 9113: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9113) {595 2295 2294 594 2311 3236 3234 2310}
set elemKinit(9113) 6.169692025290639e-06
set sigmaV0(9113) 69.090000
set ruPrev(9113) 0.0

# Element 9114: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9114) {2311 3236 3234 2310 2315 3237 3235 2314}
set elemKinit(9114) 6.169692025290639e-06
set sigmaV0(9114) 69.090000
set ruPrev(9114) 0.0

# Element 9115: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9115) {2315 3237 3235 2314 605 2299 2298 604}
set elemKinit(9115) 6.169692025290639e-06
set sigmaV0(9115) 69.090000
set ruPrev(9115) 0.0

# Element 9116: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9116) {2296 591 590 2295 3238 2304 2303 3236}
set elemKinit(9116) 6.169692025290639e-06
set sigmaV0(9116) 49.350000
set ruPrev(9116) 0.0

# Element 9117: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9117) {3238 2304 2303 3236 3239 2308 2307 3237}
set elemKinit(9117) 6.169692025290639e-06
set sigmaV0(9117) 49.350000
set ruPrev(9117) 0.0

# Element 9118: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9118) {3239 2308 2307 3237 2300 601 600 2299}
set elemKinit(9118) 6.169692025290639e-06
set sigmaV0(9118) 49.350000
set ruPrev(9118) 0.0

# Element 9119: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9119) {596 2296 2295 595 2312 3238 3236 2311}
set elemKinit(9119) 6.169692025290639e-06
set sigmaV0(9119) 49.350000
set ruPrev(9119) 0.0

# Element 9120: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9120) {2312 3238 3236 2311 2316 3239 3237 2315}
set elemKinit(9120) 6.169692025290639e-06
set sigmaV0(9120) 49.350000
set ruPrev(9120) 0.0

# Element 9121: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9121) {2316 3239 3237 2315 606 2300 2299 605}
set elemKinit(9121) 6.169692025290639e-06
set sigmaV0(9121) 49.350000
set ruPrev(9121) 0.0

# Element 9122: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9122) {2297 592 591 2296 3240 2305 2304 3238}
set elemKinit(9122) 6.169692025290639e-06
set sigmaV0(9122) 29.610000
set ruPrev(9122) 0.0

# Element 9123: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9123) {3240 2305 2304 3238 3241 2309 2308 3239}
set elemKinit(9123) 6.169692025290639e-06
set sigmaV0(9123) 29.610000
set ruPrev(9123) 0.0

# Element 9124: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9124) {3241 2309 2308 3239 2301 602 601 2300}
set elemKinit(9124) 6.169692025290639e-06
set sigmaV0(9124) 29.610000
set ruPrev(9124) 0.0

# Element 9125: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9125) {597 2297 2296 596 2313 3240 3238 2312}
set elemKinit(9125) 6.169692025290639e-06
set sigmaV0(9125) 29.610000
set ruPrev(9125) 0.0

# Element 9126: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9126) {2313 3240 3238 2312 2317 3241 3239 2316}
set elemKinit(9126) 6.169692025290639e-06
set sigmaV0(9126) 29.610000
set ruPrev(9126) 0.0

# Element 9127: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9127) {2317 3241 3239 2316 607 2301 2300 606}
set elemKinit(9127) 6.169692025290639e-06
set sigmaV0(9127) 29.610000
set ruPrev(9127) 0.0

# Element 9128: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9128) {593 2 592 2297 2320 611 2305 3240}
set elemKinit(9128) 6.169692025290639e-06
set sigmaV0(9128) 9.870000
set ruPrev(9128) 0.0

# Element 9129: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9129) {2320 611 2305 3240 2321 612 2309 3241}
set elemKinit(9129) 6.169692025290639e-06
set sigmaV0(9129) 9.870000
set ruPrev(9129) 0.0

# Element 9130: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9130) {2321 612 2309 3241 603 6 602 2301}
set elemKinit(9130) 6.169692025290639e-06
set sigmaV0(9130) 9.870000
set ruPrev(9130) 0.0

# Element 9131: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9131) {3 593 2297 597 615 2320 3240 2313}
set elemKinit(9131) 6.169692025290639e-06
set sigmaV0(9131) 9.870000
set ruPrev(9131) 0.0

# Element 9132: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9132) {615 2320 3240 2313 616 2321 3241 2317}
set elemKinit(9132) 6.169692025290639e-06
set sigmaV0(9132) 9.870000
set ruPrev(9132) 0.0

# Element 9133: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9133) {616 2321 3241 2317 7 603 2301 607}
set elemKinit(9133) 6.169692025290639e-06
set sigmaV0(9133) 9.870000
set ruPrev(9133) 0.0

# Element 9134: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9134) {2298 599 5 608 2322 617 9 626}
set elemKinit(9134) 6.169692025290639e-06
set sigmaV0(9134) 88.830000
set ruPrev(9134) 0.0

# Element 9135: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9135) {604 2298 608 8 622 2322 626 12}
set elemKinit(9135) 6.169692025290639e-06
set sigmaV0(9135) 88.830000
set ruPrev(9135) 0.0

# Element 9136: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9136) {2299 600 599 2298 2323 618 617 2322}
set elemKinit(9136) 6.169692025290639e-06
set sigmaV0(9136) 69.090000
set ruPrev(9136) 0.0

# Element 9137: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9137) {605 2299 2298 604 623 2323 2322 622}
set elemKinit(9137) 6.169692025290639e-06
set sigmaV0(9137) 69.090000
set ruPrev(9137) 0.0

# Element 9138: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9138) {2300 601 600 2299 2324 619 618 2323}
set elemKinit(9138) 6.169692025290639e-06
set sigmaV0(9138) 49.350000
set ruPrev(9138) 0.0

# Element 9139: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9139) {606 2300 2299 605 624 2324 2323 623}
set elemKinit(9139) 6.169692025290639e-06
set sigmaV0(9139) 49.350000
set ruPrev(9139) 0.0

# Element 9140: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9140) {2301 602 601 2300 2325 620 619 2324}
set elemKinit(9140) 6.169692025290639e-06
set sigmaV0(9140) 29.610000
set ruPrev(9140) 0.0

# Element 9141: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9141) {607 2301 2300 606 625 2325 2324 624}
set elemKinit(9141) 6.169692025290639e-06
set sigmaV0(9141) 29.610000
set ruPrev(9141) 0.0

# Element 9142: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9142) {603 6 602 2301 621 10 620 2325}
set elemKinit(9142) 6.169692025290639e-06
set sigmaV0(9142) 9.870000
set ruPrev(9142) 0.0

# Element 9143: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9143) {7 603 2301 607 11 621 2325 625}
set elemKinit(9143) 6.169692025290639e-06
set sigmaV0(9143) 9.870000
set ruPrev(9143) 0.0

# Element 9144: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9144) {2322 617 9 626 3242 2330 637 2338}
set elemKinit(9144) 6.169692025290639e-06
set sigmaV0(9144) 88.830000
set ruPrev(9144) 0.0

# Element 9145: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9145) {3242 2330 637 2338 2326 627 13 636}
set elemKinit(9145) 6.169692025290639e-06
set sigmaV0(9145) 88.830000
set ruPrev(9145) 0.0

# Element 9146: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9146) {622 2322 626 12 2334 3242 2338 639}
set elemKinit(9146) 6.169692025290639e-06
set sigmaV0(9146) 88.830000
set ruPrev(9146) 0.0

# Element 9147: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9147) {2334 3242 2338 639 632 2326 636 16}
set elemKinit(9147) 6.169692025290639e-06
set sigmaV0(9147) 88.830000
set ruPrev(9147) 0.0

# Element 9148: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9148) {2323 618 617 2322 3243 2331 2330 3242}
set elemKinit(9148) 6.169692025290639e-06
set sigmaV0(9148) 69.090000
set ruPrev(9148) 0.0

# Element 9149: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9149) {3243 2331 2330 3242 2327 628 627 2326}
set elemKinit(9149) 6.169692025290639e-06
set sigmaV0(9149) 69.090000
set ruPrev(9149) 0.0

# Element 9150: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9150) {623 2323 2322 622 2335 3243 3242 2334}
set elemKinit(9150) 6.169692025290639e-06
set sigmaV0(9150) 69.090000
set ruPrev(9150) 0.0

# Element 9151: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9151) {2335 3243 3242 2334 633 2327 2326 632}
set elemKinit(9151) 6.169692025290639e-06
set sigmaV0(9151) 69.090000
set ruPrev(9151) 0.0

# Element 9152: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9152) {2324 619 618 2323 3244 2332 2331 3243}
set elemKinit(9152) 6.169692025290639e-06
set sigmaV0(9152) 49.350000
set ruPrev(9152) 0.0

# Element 9153: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9153) {3244 2332 2331 3243 2328 629 628 2327}
set elemKinit(9153) 6.169692025290639e-06
set sigmaV0(9153) 49.350000
set ruPrev(9153) 0.0

# Element 9154: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9154) {624 2324 2323 623 2336 3244 3243 2335}
set elemKinit(9154) 6.169692025290639e-06
set sigmaV0(9154) 49.350000
set ruPrev(9154) 0.0

# Element 9155: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9155) {2336 3244 3243 2335 634 2328 2327 633}
set elemKinit(9155) 6.169692025290639e-06
set sigmaV0(9155) 49.350000
set ruPrev(9155) 0.0

# Element 9156: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9156) {2325 620 619 2324 3245 2333 2332 3244}
set elemKinit(9156) 6.169692025290639e-06
set sigmaV0(9156) 29.610000
set ruPrev(9156) 0.0

# Element 9157: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9157) {3245 2333 2332 3244 2329 630 629 2328}
set elemKinit(9157) 6.169692025290639e-06
set sigmaV0(9157) 29.610000
set ruPrev(9157) 0.0

# Element 9158: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9158) {625 2325 2324 624 2337 3245 3244 2336}
set elemKinit(9158) 6.169692025290639e-06
set sigmaV0(9158) 29.610000
set ruPrev(9158) 0.0

# Element 9159: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9159) {2337 3245 3244 2336 635 2329 2328 634}
set elemKinit(9159) 6.169692025290639e-06
set sigmaV0(9159) 29.610000
set ruPrev(9159) 0.0

# Element 9160: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9160) {621 10 620 2325 2339 638 2333 3245}
set elemKinit(9160) 6.169692025290639e-06
set sigmaV0(9160) 9.870000
set ruPrev(9160) 0.0

# Element 9161: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9161) {2339 638 2333 3245 631 14 630 2329}
set elemKinit(9161) 6.169692025290639e-06
set sigmaV0(9161) 9.870000
set ruPrev(9161) 0.0

# Element 9162: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9162) {11 621 2325 625 640 2339 3245 2337}
set elemKinit(9162) 6.169692025290639e-06
set sigmaV0(9162) 9.870000
set ruPrev(9162) 0.0

# Element 9163: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9163) {640 2339 3245 2337 15 631 2329 635}
set elemKinit(9163) 6.169692025290639e-06
set sigmaV0(9163) 9.870000
set ruPrev(9163) 0.0

# Element 9164: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9164) {2326 627 13 636 2340 641 17 650}
set elemKinit(9164) 6.169692025290639e-06
set sigmaV0(9164) 88.830000
set ruPrev(9164) 0.0

# Element 9165: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9165) {632 2326 636 16 646 2340 650 20}
set elemKinit(9165) 6.169692025290639e-06
set sigmaV0(9165) 88.830000
set ruPrev(9165) 0.0

# Element 9166: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9166) {2327 628 627 2326 2341 642 641 2340}
set elemKinit(9166) 6.169692025290639e-06
set sigmaV0(9166) 69.090000
set ruPrev(9166) 0.0

# Element 9167: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9167) {633 2327 2326 632 647 2341 2340 646}
set elemKinit(9167) 6.169692025290639e-06
set sigmaV0(9167) 69.090000
set ruPrev(9167) 0.0

# Element 9168: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9168) {2328 629 628 2327 2342 643 642 2341}
set elemKinit(9168) 6.169692025290639e-06
set sigmaV0(9168) 49.350000
set ruPrev(9168) 0.0

# Element 9169: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9169) {634 2328 2327 633 648 2342 2341 647}
set elemKinit(9169) 6.169692025290639e-06
set sigmaV0(9169) 49.350000
set ruPrev(9169) 0.0

# Element 9170: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9170) {2329 630 629 2328 2343 644 643 2342}
set elemKinit(9170) 6.169692025290639e-06
set sigmaV0(9170) 29.610000
set ruPrev(9170) 0.0

# Element 9171: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9171) {635 2329 2328 634 649 2343 2342 648}
set elemKinit(9171) 6.169692025290639e-06
set sigmaV0(9171) 29.610000
set ruPrev(9171) 0.0

# Element 9172: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9172) {631 14 630 2329 645 18 644 2343}
set elemKinit(9172) 6.169692025290639e-06
set sigmaV0(9172) 9.870000
set ruPrev(9172) 0.0

# Element 9173: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9173) {15 631 2329 635 19 645 2343 649}
set elemKinit(9173) 6.169692025290639e-06
set sigmaV0(9173) 9.870000
set ruPrev(9173) 0.0

# Element 9174: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9174) {2340 641 17 650 2344 651 21 660}
set elemKinit(9174) 6.169692025290639e-06
set sigmaV0(9174) 88.830000
set ruPrev(9174) 0.0

# Element 9175: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9175) {646 2340 650 20 656 2344 660 24}
set elemKinit(9175) 6.169692025290639e-06
set sigmaV0(9175) 88.830000
set ruPrev(9175) 0.0

# Element 9176: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9176) {2341 642 641 2340 2345 652 651 2344}
set elemKinit(9176) 6.169692025290639e-06
set sigmaV0(9176) 69.090000
set ruPrev(9176) 0.0

# Element 9177: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9177) {647 2341 2340 646 657 2345 2344 656}
set elemKinit(9177) 6.169692025290639e-06
set sigmaV0(9177) 69.090000
set ruPrev(9177) 0.0

# Element 9178: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9178) {2342 643 642 2341 2346 653 652 2345}
set elemKinit(9178) 6.169692025290639e-06
set sigmaV0(9178) 49.350000
set ruPrev(9178) 0.0

# Element 9179: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9179) {648 2342 2341 647 658 2346 2345 657}
set elemKinit(9179) 6.169692025290639e-06
set sigmaV0(9179) 49.350000
set ruPrev(9179) 0.0

# Element 9180: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9180) {2343 644 643 2342 2347 654 653 2346}
set elemKinit(9180) 6.169692025290639e-06
set sigmaV0(9180) 29.610000
set ruPrev(9180) 0.0

# Element 9181: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9181) {649 2343 2342 648 659 2347 2346 658}
set elemKinit(9181) 6.169692025290639e-06
set sigmaV0(9181) 29.610000
set ruPrev(9181) 0.0

# Element 9182: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9182) {645 18 644 2343 655 22 654 2347}
set elemKinit(9182) 6.169692025290639e-06
set sigmaV0(9182) 9.870000
set ruPrev(9182) 0.0

# Element 9183: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9183) {19 645 2343 649 23 655 2347 659}
set elemKinit(9183) 6.169692025290639e-06
set sigmaV0(9183) 9.870000
set ruPrev(9183) 0.0

# Element 9184: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9184) {2344 651 21 660 2348 661 25 670}
set elemKinit(9184) 6.169692025290639e-06
set sigmaV0(9184) 88.830000
set ruPrev(9184) 0.0

# Element 9185: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9185) {656 2344 660 24 666 2348 670 28}
set elemKinit(9185) 6.169692025290639e-06
set sigmaV0(9185) 88.830000
set ruPrev(9185) 0.0

# Element 9186: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9186) {2345 652 651 2344 2349 662 661 2348}
set elemKinit(9186) 6.169692025290639e-06
set sigmaV0(9186) 69.090000
set ruPrev(9186) 0.0

# Element 9187: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9187) {657 2345 2344 656 667 2349 2348 666}
set elemKinit(9187) 6.169692025290639e-06
set sigmaV0(9187) 69.090000
set ruPrev(9187) 0.0

# Element 9188: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9188) {2346 653 652 2345 2350 663 662 2349}
set elemKinit(9188) 6.169692025290639e-06
set sigmaV0(9188) 49.350000
set ruPrev(9188) 0.0

# Element 9189: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9189) {658 2346 2345 657 668 2350 2349 667}
set elemKinit(9189) 6.169692025290639e-06
set sigmaV0(9189) 49.350000
set ruPrev(9189) 0.0

# Element 9190: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9190) {2347 654 653 2346 2351 664 663 2350}
set elemKinit(9190) 6.169692025290639e-06
set sigmaV0(9190) 29.610000
set ruPrev(9190) 0.0

# Element 9191: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9191) {659 2347 2346 658 669 2351 2350 668}
set elemKinit(9191) 6.169692025290639e-06
set sigmaV0(9191) 29.610000
set ruPrev(9191) 0.0

# Element 9192: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9192) {655 22 654 2347 665 26 664 2351}
set elemKinit(9192) 6.169692025290639e-06
set sigmaV0(9192) 9.870000
set ruPrev(9192) 0.0

# Element 9193: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9193) {23 655 2347 659 27 665 2351 669}
set elemKinit(9193) 6.169692025290639e-06
set sigmaV0(9193) 9.870000
set ruPrev(9193) 0.0

# Element 9194: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9194) {2348 661 25 670 2352 671 29 680}
set elemKinit(9194) 6.169692025290639e-06
set sigmaV0(9194) 88.830000
set ruPrev(9194) 0.0

# Element 9195: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9195) {666 2348 670 28 676 2352 680 32}
set elemKinit(9195) 6.169692025290639e-06
set sigmaV0(9195) 88.830000
set ruPrev(9195) 0.0

# Element 9196: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9196) {2349 662 661 2348 2353 672 671 2352}
set elemKinit(9196) 6.169692025290639e-06
set sigmaV0(9196) 69.090000
set ruPrev(9196) 0.0

# Element 9197: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9197) {667 2349 2348 666 677 2353 2352 676}
set elemKinit(9197) 6.169692025290639e-06
set sigmaV0(9197) 69.090000
set ruPrev(9197) 0.0

# Element 9198: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9198) {2350 663 662 2349 2354 673 672 2353}
set elemKinit(9198) 6.169692025290639e-06
set sigmaV0(9198) 49.350000
set ruPrev(9198) 0.0

# Element 9199: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9199) {668 2350 2349 667 678 2354 2353 677}
set elemKinit(9199) 6.169692025290639e-06
set sigmaV0(9199) 49.350000
set ruPrev(9199) 0.0

# Element 9200: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9200) {2351 664 663 2350 2355 674 673 2354}
set elemKinit(9200) 6.169692025290639e-06
set sigmaV0(9200) 29.610000
set ruPrev(9200) 0.0

# Element 9201: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9201) {669 2351 2350 668 679 2355 2354 678}
set elemKinit(9201) 6.169692025290639e-06
set sigmaV0(9201) 29.610000
set ruPrev(9201) 0.0

# Element 9202: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9202) {665 26 664 2351 675 30 674 2355}
set elemKinit(9202) 6.169692025290639e-06
set sigmaV0(9202) 9.870000
set ruPrev(9202) 0.0

# Element 9203: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9203) {27 665 2351 669 31 675 2355 679}
set elemKinit(9203) 6.169692025290639e-06
set sigmaV0(9203) 9.870000
set ruPrev(9203) 0.0

# Element 9204: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9204) {2352 671 29 680 3246 2360 691 2368}
set elemKinit(9204) 6.169692025290639e-06
set sigmaV0(9204) 88.830000
set ruPrev(9204) 0.0

# Element 9205: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9205) {3246 2360 691 2368 2356 681 33 690}
set elemKinit(9205) 6.169692025290639e-06
set sigmaV0(9205) 88.830000
set ruPrev(9205) 0.0

# Element 9206: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9206) {676 2352 680 32 2364 3246 2368 693}
set elemKinit(9206) 6.169692025290639e-06
set sigmaV0(9206) 88.830000
set ruPrev(9206) 0.0

# Element 9207: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9207) {2364 3246 2368 693 686 2356 690 36}
set elemKinit(9207) 6.169692025290639e-06
set sigmaV0(9207) 88.830000
set ruPrev(9207) 0.0

# Element 9208: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9208) {2353 672 671 2352 3247 2361 2360 3246}
set elemKinit(9208) 6.169692025290639e-06
set sigmaV0(9208) 69.090000
set ruPrev(9208) 0.0

# Element 9209: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9209) {3247 2361 2360 3246 2357 682 681 2356}
set elemKinit(9209) 6.169692025290639e-06
set sigmaV0(9209) 69.090000
set ruPrev(9209) 0.0

# Element 9210: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9210) {677 2353 2352 676 2365 3247 3246 2364}
set elemKinit(9210) 6.169692025290639e-06
set sigmaV0(9210) 69.090000
set ruPrev(9210) 0.0

# Element 9211: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9211) {2365 3247 3246 2364 687 2357 2356 686}
set elemKinit(9211) 6.169692025290639e-06
set sigmaV0(9211) 69.090000
set ruPrev(9211) 0.0

# Element 9212: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9212) {2354 673 672 2353 3248 2362 2361 3247}
set elemKinit(9212) 6.169692025290639e-06
set sigmaV0(9212) 49.350000
set ruPrev(9212) 0.0

# Element 9213: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9213) {3248 2362 2361 3247 2358 683 682 2357}
set elemKinit(9213) 6.169692025290639e-06
set sigmaV0(9213) 49.350000
set ruPrev(9213) 0.0

# Element 9214: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9214) {678 2354 2353 677 2366 3248 3247 2365}
set elemKinit(9214) 6.169692025290639e-06
set sigmaV0(9214) 49.350000
set ruPrev(9214) 0.0

# Element 9215: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9215) {2366 3248 3247 2365 688 2358 2357 687}
set elemKinit(9215) 6.169692025290639e-06
set sigmaV0(9215) 49.350000
set ruPrev(9215) 0.0

# Element 9216: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9216) {2355 674 673 2354 3249 2363 2362 3248}
set elemKinit(9216) 6.169692025290639e-06
set sigmaV0(9216) 29.610000
set ruPrev(9216) 0.0

# Element 9217: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9217) {3249 2363 2362 3248 2359 684 683 2358}
set elemKinit(9217) 6.169692025290639e-06
set sigmaV0(9217) 29.610000
set ruPrev(9217) 0.0

# Element 9218: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9218) {679 2355 2354 678 2367 3249 3248 2366}
set elemKinit(9218) 6.169692025290639e-06
set sigmaV0(9218) 29.610000
set ruPrev(9218) 0.0

# Element 9219: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9219) {2367 3249 3248 2366 689 2359 2358 688}
set elemKinit(9219) 6.169692025290639e-06
set sigmaV0(9219) 29.610000
set ruPrev(9219) 0.0

# Element 9220: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9220) {675 30 674 2355 2369 692 2363 3249}
set elemKinit(9220) 6.169692025290639e-06
set sigmaV0(9220) 9.870000
set ruPrev(9220) 0.0

# Element 9221: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9221) {2369 692 2363 3249 685 34 684 2359}
set elemKinit(9221) 6.169692025290639e-06
set sigmaV0(9221) 9.870000
set ruPrev(9221) 0.0

# Element 9222: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9222) {31 675 2355 679 694 2369 3249 2367}
set elemKinit(9222) 6.169692025290639e-06
set sigmaV0(9222) 9.870000
set ruPrev(9222) 0.0

# Element 9223: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9223) {694 2369 3249 2367 35 685 2359 689}
set elemKinit(9223) 6.169692025290639e-06
set sigmaV0(9223) 9.870000
set ruPrev(9223) 0.0

# Element 9224: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9224) {2356 681 33 690 2370 695 37 704}
set elemKinit(9224) 6.169692025290639e-06
set sigmaV0(9224) 88.830000
set ruPrev(9224) 0.0

# Element 9225: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9225) {686 2356 690 36 700 2370 704 40}
set elemKinit(9225) 6.169692025290639e-06
set sigmaV0(9225) 88.830000
set ruPrev(9225) 0.0

# Element 9226: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9226) {2357 682 681 2356 2371 696 695 2370}
set elemKinit(9226) 6.169692025290639e-06
set sigmaV0(9226) 69.090000
set ruPrev(9226) 0.0

# Element 9227: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9227) {687 2357 2356 686 701 2371 2370 700}
set elemKinit(9227) 6.169692025290639e-06
set sigmaV0(9227) 69.090000
set ruPrev(9227) 0.0

# Element 9228: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9228) {2358 683 682 2357 2372 697 696 2371}
set elemKinit(9228) 6.169692025290639e-06
set sigmaV0(9228) 49.350000
set ruPrev(9228) 0.0

# Element 9229: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9229) {688 2358 2357 687 702 2372 2371 701}
set elemKinit(9229) 6.169692025290639e-06
set sigmaV0(9229) 49.350000
set ruPrev(9229) 0.0

# Element 9230: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9230) {2359 684 683 2358 2373 698 697 2372}
set elemKinit(9230) 6.169692025290639e-06
set sigmaV0(9230) 29.610000
set ruPrev(9230) 0.0

# Element 9231: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9231) {689 2359 2358 688 703 2373 2372 702}
set elemKinit(9231) 6.169692025290639e-06
set sigmaV0(9231) 29.610000
set ruPrev(9231) 0.0

# Element 9232: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9232) {685 34 684 2359 699 38 698 2373}
set elemKinit(9232) 6.169692025290639e-06
set sigmaV0(9232) 9.870000
set ruPrev(9232) 0.0

# Element 9233: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9233) {35 685 2359 689 39 699 2373 703}
set elemKinit(9233) 6.169692025290639e-06
set sigmaV0(9233) 9.870000
set ruPrev(9233) 0.0

# Element 9234: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9234) {2370 695 37 704 3250 2378 715 2394}
set elemKinit(9234) 6.169692025290639e-06
set sigmaV0(9234) 88.830000
set ruPrev(9234) 0.0

# Element 9235: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9235) {3250 2378 715 2394 3251 2382 716 2395}
set elemKinit(9235) 6.169692025290639e-06
set sigmaV0(9235) 88.830000
set ruPrev(9235) 0.0

# Element 9236: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9236) {3251 2382 716 2395 2374 705 41 714}
set elemKinit(9236) 6.169692025290639e-06
set sigmaV0(9236) 88.830000
set ruPrev(9236) 0.0

# Element 9237: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9237) {700 2370 704 40 2386 3250 2394 719}
set elemKinit(9237) 6.169692025290639e-06
set sigmaV0(9237) 88.830000
set ruPrev(9237) 0.0

# Element 9238: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9238) {2386 3250 2394 719 2390 3251 2395 720}
set elemKinit(9238) 6.169692025290639e-06
set sigmaV0(9238) 88.830000
set ruPrev(9238) 0.0

# Element 9239: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9239) {2390 3251 2395 720 710 2374 714 44}
set elemKinit(9239) 6.169692025290639e-06
set sigmaV0(9239) 88.830000
set ruPrev(9239) 0.0

# Element 9240: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9240) {2371 696 695 2370 3252 2379 2378 3250}
set elemKinit(9240) 6.169692025290639e-06
set sigmaV0(9240) 69.090000
set ruPrev(9240) 0.0

# Element 9241: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9241) {3252 2379 2378 3250 3253 2383 2382 3251}
set elemKinit(9241) 6.169692025290639e-06
set sigmaV0(9241) 69.090000
set ruPrev(9241) 0.0

# Element 9242: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9242) {3253 2383 2382 3251 2375 706 705 2374}
set elemKinit(9242) 6.169692025290639e-06
set sigmaV0(9242) 69.090000
set ruPrev(9242) 0.0

# Element 9243: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9243) {701 2371 2370 700 2387 3252 3250 2386}
set elemKinit(9243) 6.169692025290639e-06
set sigmaV0(9243) 69.090000
set ruPrev(9243) 0.0

# Element 9244: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9244) {2387 3252 3250 2386 2391 3253 3251 2390}
set elemKinit(9244) 6.169692025290639e-06
set sigmaV0(9244) 69.090000
set ruPrev(9244) 0.0

# Element 9245: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9245) {2391 3253 3251 2390 711 2375 2374 710}
set elemKinit(9245) 6.169692025290639e-06
set sigmaV0(9245) 69.090000
set ruPrev(9245) 0.0

# Element 9246: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9246) {2372 697 696 2371 3254 2380 2379 3252}
set elemKinit(9246) 6.169692025290639e-06
set sigmaV0(9246) 49.350000
set ruPrev(9246) 0.0

# Element 9247: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9247) {3254 2380 2379 3252 3255 2384 2383 3253}
set elemKinit(9247) 6.169692025290639e-06
set sigmaV0(9247) 49.350000
set ruPrev(9247) 0.0

# Element 9248: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9248) {3255 2384 2383 3253 2376 707 706 2375}
set elemKinit(9248) 6.169692025290639e-06
set sigmaV0(9248) 49.350000
set ruPrev(9248) 0.0

# Element 9249: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9249) {702 2372 2371 701 2388 3254 3252 2387}
set elemKinit(9249) 6.169692025290639e-06
set sigmaV0(9249) 49.350000
set ruPrev(9249) 0.0

# Element 9250: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9250) {2388 3254 3252 2387 2392 3255 3253 2391}
set elemKinit(9250) 6.169692025290639e-06
set sigmaV0(9250) 49.350000
set ruPrev(9250) 0.0

# Element 9251: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9251) {2392 3255 3253 2391 712 2376 2375 711}
set elemKinit(9251) 6.169692025290639e-06
set sigmaV0(9251) 49.350000
set ruPrev(9251) 0.0

# Element 9252: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9252) {2373 698 697 2372 3256 2381 2380 3254}
set elemKinit(9252) 6.169692025290639e-06
set sigmaV0(9252) 29.610000
set ruPrev(9252) 0.0

# Element 9253: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9253) {3256 2381 2380 3254 3257 2385 2384 3255}
set elemKinit(9253) 6.169692025290639e-06
set sigmaV0(9253) 29.610000
set ruPrev(9253) 0.0

# Element 9254: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9254) {3257 2385 2384 3255 2377 708 707 2376}
set elemKinit(9254) 6.169692025290639e-06
set sigmaV0(9254) 29.610000
set ruPrev(9254) 0.0

# Element 9255: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9255) {703 2373 2372 702 2389 3256 3254 2388}
set elemKinit(9255) 6.169692025290639e-06
set sigmaV0(9255) 29.610000
set ruPrev(9255) 0.0

# Element 9256: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9256) {2389 3256 3254 2388 2393 3257 3255 2392}
set elemKinit(9256) 6.169692025290639e-06
set sigmaV0(9256) 29.610000
set ruPrev(9256) 0.0

# Element 9257: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9257) {2393 3257 3255 2392 713 2377 2376 712}
set elemKinit(9257) 6.169692025290639e-06
set sigmaV0(9257) 29.610000
set ruPrev(9257) 0.0

# Element 9258: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9258) {699 38 698 2373 2396 717 2381 3256}
set elemKinit(9258) 6.169692025290639e-06
set sigmaV0(9258) 9.870000
set ruPrev(9258) 0.0

# Element 9259: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9259) {2396 717 2381 3256 2397 718 2385 3257}
set elemKinit(9259) 6.169692025290639e-06
set sigmaV0(9259) 9.870000
set ruPrev(9259) 0.0

# Element 9260: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9260) {2397 718 2385 3257 709 42 708 2377}
set elemKinit(9260) 6.169692025290639e-06
set sigmaV0(9260) 9.870000
set ruPrev(9260) 0.0

# Element 9261: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9261) {39 699 2373 703 721 2396 3256 2389}
set elemKinit(9261) 6.169692025290639e-06
set sigmaV0(9261) 9.870000
set ruPrev(9261) 0.0

# Element 9262: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9262) {721 2396 3256 2389 722 2397 3257 2393}
set elemKinit(9262) 6.169692025290639e-06
set sigmaV0(9262) 9.870000
set ruPrev(9262) 0.0

# Element 9263: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9263) {722 2397 3257 2393 43 709 2377 713}
set elemKinit(9263) 6.169692025290639e-06
set sigmaV0(9263) 9.870000
set ruPrev(9263) 0.0

# Element 9264: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9264) {723 594 4 46 2398 2310 613 731}
set elemKinit(9264) 6.169692025290639e-06
set sigmaV0(9264) 88.830000
set ruPrev(9264) 0.0

# Element 9265: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9265) {2398 2310 613 731 2402 2314 614 732}
set elemKinit(9265) 6.169692025290639e-06
set sigmaV0(9265) 88.830000
set ruPrev(9265) 0.0

# Element 9266: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9266) {2402 2314 614 732 727 604 8 48}
set elemKinit(9266) 6.169692025290639e-06
set sigmaV0(9266) 88.830000
set ruPrev(9266) 0.0

# Element 9267: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9267) {724 595 594 723 2399 2311 2310 2398}
set elemKinit(9267) 6.169692025290639e-06
set sigmaV0(9267) 69.090000
set ruPrev(9267) 0.0

# Element 9268: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9268) {2399 2311 2310 2398 2403 2315 2314 2402}
set elemKinit(9268) 6.169692025290639e-06
set sigmaV0(9268) 69.090000
set ruPrev(9268) 0.0

# Element 9269: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9269) {2403 2315 2314 2402 728 605 604 727}
set elemKinit(9269) 6.169692025290639e-06
set sigmaV0(9269) 69.090000
set ruPrev(9269) 0.0

# Element 9270: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9270) {725 596 595 724 2400 2312 2311 2399}
set elemKinit(9270) 6.169692025290639e-06
set sigmaV0(9270) 49.350000
set ruPrev(9270) 0.0

# Element 9271: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9271) {2400 2312 2311 2399 2404 2316 2315 2403}
set elemKinit(9271) 6.169692025290639e-06
set sigmaV0(9271) 49.350000
set ruPrev(9271) 0.0

# Element 9272: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9272) {2404 2316 2315 2403 729 606 605 728}
set elemKinit(9272) 6.169692025290639e-06
set sigmaV0(9272) 49.350000
set ruPrev(9272) 0.0

# Element 9273: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9273) {726 597 596 725 2401 2313 2312 2400}
set elemKinit(9273) 6.169692025290639e-06
set sigmaV0(9273) 29.610000
set ruPrev(9273) 0.0

# Element 9274: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9274) {2401 2313 2312 2400 2405 2317 2316 2404}
set elemKinit(9274) 6.169692025290639e-06
set sigmaV0(9274) 29.610000
set ruPrev(9274) 0.0

# Element 9275: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9275) {2405 2317 2316 2404 730 607 606 729}
set elemKinit(9275) 6.169692025290639e-06
set sigmaV0(9275) 29.610000
set ruPrev(9275) 0.0

# Element 9276: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9276) {45 3 597 726 733 615 2313 2401}
set elemKinit(9276) 6.169692025290639e-06
set sigmaV0(9276) 9.870000
set ruPrev(9276) 0.0

# Element 9277: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9277) {733 615 2313 2401 734 616 2317 2405}
set elemKinit(9277) 6.169692025290639e-06
set sigmaV0(9277) 9.870000
set ruPrev(9277) 0.0

# Element 9278: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9278) {734 616 2317 2405 47 7 607 730}
set elemKinit(9278) 6.169692025290639e-06
set sigmaV0(9278) 9.870000
set ruPrev(9278) 0.0

# Element 9279: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9279) {727 604 8 48 735 622 12 50}
set elemKinit(9279) 6.169692025290639e-06
set sigmaV0(9279) 88.830000
set ruPrev(9279) 0.0

# Element 9280: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9280) {728 605 604 727 736 623 622 735}
set elemKinit(9280) 6.169692025290639e-06
set sigmaV0(9280) 69.090000
set ruPrev(9280) 0.0

# Element 9281: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9281) {729 606 605 728 737 624 623 736}
set elemKinit(9281) 6.169692025290639e-06
set sigmaV0(9281) 49.350000
set ruPrev(9281) 0.0

# Element 9282: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9282) {730 607 606 729 738 625 624 737}
set elemKinit(9282) 6.169692025290639e-06
set sigmaV0(9282) 29.610000
set ruPrev(9282) 0.0

# Element 9283: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9283) {47 7 607 730 49 11 625 738}
set elemKinit(9283) 6.169692025290639e-06
set sigmaV0(9283) 9.870000
set ruPrev(9283) 0.0

# Element 9284: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9284) {735 622 12 50 2406 2334 639 743}
set elemKinit(9284) 6.169692025290639e-06
set sigmaV0(9284) 88.830000
set ruPrev(9284) 0.0

# Element 9285: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9285) {2406 2334 639 743 739 632 16 52}
set elemKinit(9285) 6.169692025290639e-06
set sigmaV0(9285) 88.830000
set ruPrev(9285) 0.0

# Element 9286: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9286) {736 623 622 735 2407 2335 2334 2406}
set elemKinit(9286) 6.169692025290639e-06
set sigmaV0(9286) 69.090000
set ruPrev(9286) 0.0

# Element 9287: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9287) {2407 2335 2334 2406 740 633 632 739}
set elemKinit(9287) 6.169692025290639e-06
set sigmaV0(9287) 69.090000
set ruPrev(9287) 0.0

# Element 9288: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9288) {737 624 623 736 2408 2336 2335 2407}
set elemKinit(9288) 6.169692025290639e-06
set sigmaV0(9288) 49.350000
set ruPrev(9288) 0.0

# Element 9289: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9289) {2408 2336 2335 2407 741 634 633 740}
set elemKinit(9289) 6.169692025290639e-06
set sigmaV0(9289) 49.350000
set ruPrev(9289) 0.0

# Element 9290: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9290) {738 625 624 737 2409 2337 2336 2408}
set elemKinit(9290) 6.169692025290639e-06
set sigmaV0(9290) 29.610000
set ruPrev(9290) 0.0

# Element 9291: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9291) {2409 2337 2336 2408 742 635 634 741}
set elemKinit(9291) 6.169692025290639e-06
set sigmaV0(9291) 29.610000
set ruPrev(9291) 0.0

# Element 9292: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9292) {49 11 625 738 744 640 2337 2409}
set elemKinit(9292) 6.169692025290639e-06
set sigmaV0(9292) 9.870000
set ruPrev(9292) 0.0

# Element 9293: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9293) {744 640 2337 2409 51 15 635 742}
set elemKinit(9293) 6.169692025290639e-06
set sigmaV0(9293) 9.870000
set ruPrev(9293) 0.0

# Element 9294: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9294) {739 632 16 52 745 646 20 54}
set elemKinit(9294) 6.169692025290639e-06
set sigmaV0(9294) 88.830000
set ruPrev(9294) 0.0

# Element 9295: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9295) {740 633 632 739 746 647 646 745}
set elemKinit(9295) 6.169692025290639e-06
set sigmaV0(9295) 69.090000
set ruPrev(9295) 0.0

# Element 9296: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9296) {741 634 633 740 747 648 647 746}
set elemKinit(9296) 6.169692025290639e-06
set sigmaV0(9296) 49.350000
set ruPrev(9296) 0.0

# Element 9297: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9297) {742 635 634 741 748 649 648 747}
set elemKinit(9297) 6.169692025290639e-06
set sigmaV0(9297) 29.610000
set ruPrev(9297) 0.0

# Element 9298: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9298) {51 15 635 742 53 19 649 748}
set elemKinit(9298) 6.169692025290639e-06
set sigmaV0(9298) 9.870000
set ruPrev(9298) 0.0

# Element 9299: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9299) {745 646 20 54 749 656 24 56}
set elemKinit(9299) 6.169692025290639e-06
set sigmaV0(9299) 88.830000
set ruPrev(9299) 0.0

# Element 9300: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9300) {746 647 646 745 750 657 656 749}
set elemKinit(9300) 6.169692025290639e-06
set sigmaV0(9300) 69.090000
set ruPrev(9300) 0.0

# Element 9301: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9301) {747 648 647 746 751 658 657 750}
set elemKinit(9301) 6.169692025290639e-06
set sigmaV0(9301) 49.350000
set ruPrev(9301) 0.0

# Element 9302: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9302) {748 649 648 747 752 659 658 751}
set elemKinit(9302) 6.169692025290639e-06
set sigmaV0(9302) 29.610000
set ruPrev(9302) 0.0

# Element 9303: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9303) {53 19 649 748 55 23 659 752}
set elemKinit(9303) 6.169692025290639e-06
set sigmaV0(9303) 9.870000
set ruPrev(9303) 0.0

# Element 9304: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9304) {749 656 24 56 753 666 28 58}
set elemKinit(9304) 6.169692025290639e-06
set sigmaV0(9304) 88.830000
set ruPrev(9304) 0.0

# Element 9305: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9305) {750 657 656 749 754 667 666 753}
set elemKinit(9305) 6.169692025290639e-06
set sigmaV0(9305) 69.090000
set ruPrev(9305) 0.0

# Element 9306: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9306) {751 658 657 750 755 668 667 754}
set elemKinit(9306) 6.169692025290639e-06
set sigmaV0(9306) 49.350000
set ruPrev(9306) 0.0

# Element 9307: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9307) {752 659 658 751 756 669 668 755}
set elemKinit(9307) 6.169692025290639e-06
set sigmaV0(9307) 29.610000
set ruPrev(9307) 0.0

# Element 9308: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9308) {55 23 659 752 57 27 669 756}
set elemKinit(9308) 6.169692025290639e-06
set sigmaV0(9308) 9.870000
set ruPrev(9308) 0.0

# Element 9309: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9309) {753 666 28 58 757 676 32 60}
set elemKinit(9309) 6.169692025290639e-06
set sigmaV0(9309) 88.830000
set ruPrev(9309) 0.0

# Element 9310: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9310) {754 667 666 753 758 677 676 757}
set elemKinit(9310) 6.169692025290639e-06
set sigmaV0(9310) 69.090000
set ruPrev(9310) 0.0

# Element 9311: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9311) {755 668 667 754 759 678 677 758}
set elemKinit(9311) 6.169692025290639e-06
set sigmaV0(9311) 49.350000
set ruPrev(9311) 0.0

# Element 9312: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9312) {756 669 668 755 760 679 678 759}
set elemKinit(9312) 6.169692025290639e-06
set sigmaV0(9312) 29.610000
set ruPrev(9312) 0.0

# Element 9313: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9313) {57 27 669 756 59 31 679 760}
set elemKinit(9313) 6.169692025290639e-06
set sigmaV0(9313) 9.870000
set ruPrev(9313) 0.0

# Element 9314: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9314) {757 676 32 60 2410 2364 693 765}
set elemKinit(9314) 6.169692025290639e-06
set sigmaV0(9314) 88.830000
set ruPrev(9314) 0.0

# Element 9315: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9315) {2410 2364 693 765 761 686 36 62}
set elemKinit(9315) 6.169692025290639e-06
set sigmaV0(9315) 88.830000
set ruPrev(9315) 0.0

# Element 9316: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9316) {758 677 676 757 2411 2365 2364 2410}
set elemKinit(9316) 6.169692025290639e-06
set sigmaV0(9316) 69.090000
set ruPrev(9316) 0.0

# Element 9317: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9317) {2411 2365 2364 2410 762 687 686 761}
set elemKinit(9317) 6.169692025290639e-06
set sigmaV0(9317) 69.090000
set ruPrev(9317) 0.0

# Element 9318: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9318) {759 678 677 758 2412 2366 2365 2411}
set elemKinit(9318) 6.169692025290639e-06
set sigmaV0(9318) 49.350000
set ruPrev(9318) 0.0

# Element 9319: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9319) {2412 2366 2365 2411 763 688 687 762}
set elemKinit(9319) 6.169692025290639e-06
set sigmaV0(9319) 49.350000
set ruPrev(9319) 0.0

# Element 9320: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9320) {760 679 678 759 2413 2367 2366 2412}
set elemKinit(9320) 6.169692025290639e-06
set sigmaV0(9320) 29.610000
set ruPrev(9320) 0.0

# Element 9321: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9321) {2413 2367 2366 2412 764 689 688 763}
set elemKinit(9321) 6.169692025290639e-06
set sigmaV0(9321) 29.610000
set ruPrev(9321) 0.0

# Element 9322: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9322) {59 31 679 760 766 694 2367 2413}
set elemKinit(9322) 6.169692025290639e-06
set sigmaV0(9322) 9.870000
set ruPrev(9322) 0.0

# Element 9323: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9323) {766 694 2367 2413 61 35 689 764}
set elemKinit(9323) 6.169692025290639e-06
set sigmaV0(9323) 9.870000
set ruPrev(9323) 0.0

# Element 9324: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9324) {761 686 36 62 767 700 40 64}
set elemKinit(9324) 6.169692025290639e-06
set sigmaV0(9324) 88.830000
set ruPrev(9324) 0.0

# Element 9325: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9325) {762 687 686 761 768 701 700 767}
set elemKinit(9325) 6.169692025290639e-06
set sigmaV0(9325) 69.090000
set ruPrev(9325) 0.0

# Element 9326: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9326) {763 688 687 762 769 702 701 768}
set elemKinit(9326) 6.169692025290639e-06
set sigmaV0(9326) 49.350000
set ruPrev(9326) 0.0

# Element 9327: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9327) {764 689 688 763 770 703 702 769}
set elemKinit(9327) 6.169692025290639e-06
set sigmaV0(9327) 29.610000
set ruPrev(9327) 0.0

# Element 9328: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9328) {61 35 689 764 63 39 703 770}
set elemKinit(9328) 6.169692025290639e-06
set sigmaV0(9328) 9.870000
set ruPrev(9328) 0.0

# Element 9329: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9329) {767 700 40 64 2414 2386 719 775}
set elemKinit(9329) 6.169692025290639e-06
set sigmaV0(9329) 88.830000
set ruPrev(9329) 0.0

# Element 9330: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9330) {2414 2386 719 775 2418 2390 720 776}
set elemKinit(9330) 6.169692025290639e-06
set sigmaV0(9330) 88.830000
set ruPrev(9330) 0.0

# Element 9331: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9331) {2418 2390 720 776 771 710 44 66}
set elemKinit(9331) 6.169692025290639e-06
set sigmaV0(9331) 88.830000
set ruPrev(9331) 0.0

# Element 9332: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9332) {768 701 700 767 2415 2387 2386 2414}
set elemKinit(9332) 6.169692025290639e-06
set sigmaV0(9332) 69.090000
set ruPrev(9332) 0.0

# Element 9333: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9333) {2415 2387 2386 2414 2419 2391 2390 2418}
set elemKinit(9333) 6.169692025290639e-06
set sigmaV0(9333) 69.090000
set ruPrev(9333) 0.0

# Element 9334: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9334) {2419 2391 2390 2418 772 711 710 771}
set elemKinit(9334) 6.169692025290639e-06
set sigmaV0(9334) 69.090000
set ruPrev(9334) 0.0

# Element 9335: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9335) {769 702 701 768 2416 2388 2387 2415}
set elemKinit(9335) 6.169692025290639e-06
set sigmaV0(9335) 49.350000
set ruPrev(9335) 0.0

# Element 9336: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9336) {2416 2388 2387 2415 2420 2392 2391 2419}
set elemKinit(9336) 6.169692025290639e-06
set sigmaV0(9336) 49.350000
set ruPrev(9336) 0.0

# Element 9337: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9337) {2420 2392 2391 2419 773 712 711 772}
set elemKinit(9337) 6.169692025290639e-06
set sigmaV0(9337) 49.350000
set ruPrev(9337) 0.0

# Element 9338: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9338) {770 703 702 769 2417 2389 2388 2416}
set elemKinit(9338) 6.169692025290639e-06
set sigmaV0(9338) 29.610000
set ruPrev(9338) 0.0

# Element 9339: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9339) {2417 2389 2388 2416 2421 2393 2392 2420}
set elemKinit(9339) 6.169692025290639e-06
set sigmaV0(9339) 29.610000
set ruPrev(9339) 0.0

# Element 9340: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9340) {2421 2393 2392 2420 774 713 712 773}
set elemKinit(9340) 6.169692025290639e-06
set sigmaV0(9340) 29.610000
set ruPrev(9340) 0.0

# Element 9341: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9341) {63 39 703 770 777 721 2389 2417}
set elemKinit(9341) 6.169692025290639e-06
set sigmaV0(9341) 9.870000
set ruPrev(9341) 0.0

# Element 9342: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9342) {777 721 2389 2417 778 722 2393 2421}
set elemKinit(9342) 6.169692025290639e-06
set sigmaV0(9342) 9.870000
set ruPrev(9342) 0.0

# Element 9343: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9343) {778 722 2393 2421 65 43 713 774}
set elemKinit(9343) 6.169692025290639e-06
set sigmaV0(9343) 9.870000
set ruPrev(9343) 0.0

# Element 9344: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9344) {779 723 46 68 2422 2398 731 787}
set elemKinit(9344) 6.169692025290639e-06
set sigmaV0(9344) 88.830000
set ruPrev(9344) 0.0

# Element 9345: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9345) {2422 2398 731 787 2426 2402 732 788}
set elemKinit(9345) 6.169692025290639e-06
set sigmaV0(9345) 88.830000
set ruPrev(9345) 0.0

# Element 9346: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9346) {2426 2402 732 788 783 727 48 70}
set elemKinit(9346) 6.169692025290639e-06
set sigmaV0(9346) 88.830000
set ruPrev(9346) 0.0

# Element 9347: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9347) {780 724 723 779 2423 2399 2398 2422}
set elemKinit(9347) 6.169692025290639e-06
set sigmaV0(9347) 69.090000
set ruPrev(9347) 0.0

# Element 9348: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9348) {2423 2399 2398 2422 2427 2403 2402 2426}
set elemKinit(9348) 6.169692025290639e-06
set sigmaV0(9348) 69.090000
set ruPrev(9348) 0.0

# Element 9349: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9349) {2427 2403 2402 2426 784 728 727 783}
set elemKinit(9349) 6.169692025290639e-06
set sigmaV0(9349) 69.090000
set ruPrev(9349) 0.0

# Element 9350: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9350) {781 725 724 780 2424 2400 2399 2423}
set elemKinit(9350) 6.169692025290639e-06
set sigmaV0(9350) 49.350000
set ruPrev(9350) 0.0

# Element 9351: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9351) {2424 2400 2399 2423 2428 2404 2403 2427}
set elemKinit(9351) 6.169692025290639e-06
set sigmaV0(9351) 49.350000
set ruPrev(9351) 0.0

# Element 9352: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9352) {2428 2404 2403 2427 785 729 728 784}
set elemKinit(9352) 6.169692025290639e-06
set sigmaV0(9352) 49.350000
set ruPrev(9352) 0.0

# Element 9353: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9353) {782 726 725 781 2425 2401 2400 2424}
set elemKinit(9353) 6.169692025290639e-06
set sigmaV0(9353) 29.610000
set ruPrev(9353) 0.0

# Element 9354: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9354) {2425 2401 2400 2424 2429 2405 2404 2428}
set elemKinit(9354) 6.169692025290639e-06
set sigmaV0(9354) 29.610000
set ruPrev(9354) 0.0

# Element 9355: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9355) {2429 2405 2404 2428 786 730 729 785}
set elemKinit(9355) 6.169692025290639e-06
set sigmaV0(9355) 29.610000
set ruPrev(9355) 0.0

# Element 9356: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9356) {67 45 726 782 789 733 2401 2425}
set elemKinit(9356) 6.169692025290639e-06
set sigmaV0(9356) 9.870000
set ruPrev(9356) 0.0

# Element 9357: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9357) {789 733 2401 2425 790 734 2405 2429}
set elemKinit(9357) 6.169692025290639e-06
set sigmaV0(9357) 9.870000
set ruPrev(9357) 0.0

# Element 9358: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9358) {790 734 2405 2429 69 47 730 786}
set elemKinit(9358) 6.169692025290639e-06
set sigmaV0(9358) 9.870000
set ruPrev(9358) 0.0

# Element 9359: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9359) {783 727 48 70 791 735 50 72}
set elemKinit(9359) 6.169692025290639e-06
set sigmaV0(9359) 88.830000
set ruPrev(9359) 0.0

# Element 9360: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9360) {784 728 727 783 792 736 735 791}
set elemKinit(9360) 6.169692025290639e-06
set sigmaV0(9360) 69.090000
set ruPrev(9360) 0.0

# Element 9361: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9361) {785 729 728 784 793 737 736 792}
set elemKinit(9361) 6.169692025290639e-06
set sigmaV0(9361) 49.350000
set ruPrev(9361) 0.0

# Element 9362: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9362) {786 730 729 785 794 738 737 793}
set elemKinit(9362) 6.169692025290639e-06
set sigmaV0(9362) 29.610000
set ruPrev(9362) 0.0

# Element 9363: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9363) {69 47 730 786 71 49 738 794}
set elemKinit(9363) 6.169692025290639e-06
set sigmaV0(9363) 9.870000
set ruPrev(9363) 0.0

# Element 9364: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9364) {791 735 50 72 2430 2406 743 799}
set elemKinit(9364) 6.169692025290639e-06
set sigmaV0(9364) 88.830000
set ruPrev(9364) 0.0

# Element 9365: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9365) {2430 2406 743 799 795 739 52 74}
set elemKinit(9365) 6.169692025290639e-06
set sigmaV0(9365) 88.830000
set ruPrev(9365) 0.0

# Element 9366: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9366) {792 736 735 791 2431 2407 2406 2430}
set elemKinit(9366) 6.169692025290639e-06
set sigmaV0(9366) 69.090000
set ruPrev(9366) 0.0

# Element 9367: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9367) {2431 2407 2406 2430 796 740 739 795}
set elemKinit(9367) 6.169692025290639e-06
set sigmaV0(9367) 69.090000
set ruPrev(9367) 0.0

# Element 9368: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9368) {793 737 736 792 2432 2408 2407 2431}
set elemKinit(9368) 6.169692025290639e-06
set sigmaV0(9368) 49.350000
set ruPrev(9368) 0.0

# Element 9369: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9369) {2432 2408 2407 2431 797 741 740 796}
set elemKinit(9369) 6.169692025290639e-06
set sigmaV0(9369) 49.350000
set ruPrev(9369) 0.0

# Element 9370: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9370) {794 738 737 793 2433 2409 2408 2432}
set elemKinit(9370) 6.169692025290639e-06
set sigmaV0(9370) 29.610000
set ruPrev(9370) 0.0

# Element 9371: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9371) {2433 2409 2408 2432 798 742 741 797}
set elemKinit(9371) 6.169692025290639e-06
set sigmaV0(9371) 29.610000
set ruPrev(9371) 0.0

# Element 9372: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9372) {71 49 738 794 800 744 2409 2433}
set elemKinit(9372) 6.169692025290639e-06
set sigmaV0(9372) 9.870000
set ruPrev(9372) 0.0

# Element 9373: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9373) {800 744 2409 2433 73 51 742 798}
set elemKinit(9373) 6.169692025290639e-06
set sigmaV0(9373) 9.870000
set ruPrev(9373) 0.0

# Element 9374: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9374) {795 739 52 74 801 745 54 76}
set elemKinit(9374) 6.169692025290639e-06
set sigmaV0(9374) 88.830000
set ruPrev(9374) 0.0

# Element 9375: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9375) {796 740 739 795 802 746 745 801}
set elemKinit(9375) 6.169692025290639e-06
set sigmaV0(9375) 69.090000
set ruPrev(9375) 0.0

# Element 9376: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9376) {797 741 740 796 803 747 746 802}
set elemKinit(9376) 6.169692025290639e-06
set sigmaV0(9376) 49.350000
set ruPrev(9376) 0.0

# Element 9377: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9377) {798 742 741 797 804 748 747 803}
set elemKinit(9377) 6.169692025290639e-06
set sigmaV0(9377) 29.610000
set ruPrev(9377) 0.0

# Element 9378: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9378) {73 51 742 798 75 53 748 804}
set elemKinit(9378) 6.169692025290639e-06
set sigmaV0(9378) 9.870000
set ruPrev(9378) 0.0

# Element 9379: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9379) {801 745 54 76 805 749 56 78}
set elemKinit(9379) 6.169692025290639e-06
set sigmaV0(9379) 88.830000
set ruPrev(9379) 0.0

# Element 9380: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9380) {802 746 745 801 806 750 749 805}
set elemKinit(9380) 6.169692025290639e-06
set sigmaV0(9380) 69.090000
set ruPrev(9380) 0.0

# Element 9381: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9381) {803 747 746 802 807 751 750 806}
set elemKinit(9381) 6.169692025290639e-06
set sigmaV0(9381) 49.350000
set ruPrev(9381) 0.0

# Element 9382: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9382) {804 748 747 803 808 752 751 807}
set elemKinit(9382) 6.169692025290639e-06
set sigmaV0(9382) 29.610000
set ruPrev(9382) 0.0

# Element 9383: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9383) {75 53 748 804 77 55 752 808}
set elemKinit(9383) 6.169692025290639e-06
set sigmaV0(9383) 9.870000
set ruPrev(9383) 0.0

# Element 9384: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9384) {805 749 56 78 809 753 58 80}
set elemKinit(9384) 6.169692025290639e-06
set sigmaV0(9384) 88.830000
set ruPrev(9384) 0.0

# Element 9385: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9385) {806 750 749 805 810 754 753 809}
set elemKinit(9385) 6.169692025290639e-06
set sigmaV0(9385) 69.090000
set ruPrev(9385) 0.0

# Element 9386: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9386) {807 751 750 806 811 755 754 810}
set elemKinit(9386) 6.169692025290639e-06
set sigmaV0(9386) 49.350000
set ruPrev(9386) 0.0

# Element 9387: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9387) {808 752 751 807 812 756 755 811}
set elemKinit(9387) 6.169692025290639e-06
set sigmaV0(9387) 29.610000
set ruPrev(9387) 0.0

# Element 9388: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9388) {77 55 752 808 79 57 756 812}
set elemKinit(9388) 6.169692025290639e-06
set sigmaV0(9388) 9.870000
set ruPrev(9388) 0.0

# Element 9389: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9389) {809 753 58 80 813 757 60 82}
set elemKinit(9389) 6.169692025290639e-06
set sigmaV0(9389) 88.830000
set ruPrev(9389) 0.0

# Element 9390: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9390) {810 754 753 809 814 758 757 813}
set elemKinit(9390) 6.169692025290639e-06
set sigmaV0(9390) 69.090000
set ruPrev(9390) 0.0

# Element 9391: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9391) {811 755 754 810 815 759 758 814}
set elemKinit(9391) 6.169692025290639e-06
set sigmaV0(9391) 49.350000
set ruPrev(9391) 0.0

# Element 9392: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9392) {812 756 755 811 816 760 759 815}
set elemKinit(9392) 6.169692025290639e-06
set sigmaV0(9392) 29.610000
set ruPrev(9392) 0.0

# Element 9393: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9393) {79 57 756 812 81 59 760 816}
set elemKinit(9393) 6.169692025290639e-06
set sigmaV0(9393) 9.870000
set ruPrev(9393) 0.0

# Element 9394: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9394) {813 757 60 82 2434 2410 765 821}
set elemKinit(9394) 6.169692025290639e-06
set sigmaV0(9394) 88.830000
set ruPrev(9394) 0.0

# Element 9395: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9395) {2434 2410 765 821 817 761 62 84}
set elemKinit(9395) 6.169692025290639e-06
set sigmaV0(9395) 88.830000
set ruPrev(9395) 0.0

# Element 9396: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9396) {814 758 757 813 2435 2411 2410 2434}
set elemKinit(9396) 6.169692025290639e-06
set sigmaV0(9396) 69.090000
set ruPrev(9396) 0.0

# Element 9397: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9397) {2435 2411 2410 2434 818 762 761 817}
set elemKinit(9397) 6.169692025290639e-06
set sigmaV0(9397) 69.090000
set ruPrev(9397) 0.0

# Element 9398: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9398) {815 759 758 814 2436 2412 2411 2435}
set elemKinit(9398) 6.169692025290639e-06
set sigmaV0(9398) 49.350000
set ruPrev(9398) 0.0

# Element 9399: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9399) {2436 2412 2411 2435 819 763 762 818}
set elemKinit(9399) 6.169692025290639e-06
set sigmaV0(9399) 49.350000
set ruPrev(9399) 0.0

# Element 9400: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9400) {816 760 759 815 2437 2413 2412 2436}
set elemKinit(9400) 6.169692025290639e-06
set sigmaV0(9400) 29.610000
set ruPrev(9400) 0.0

# Element 9401: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9401) {2437 2413 2412 2436 820 764 763 819}
set elemKinit(9401) 6.169692025290639e-06
set sigmaV0(9401) 29.610000
set ruPrev(9401) 0.0

# Element 9402: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9402) {81 59 760 816 822 766 2413 2437}
set elemKinit(9402) 6.169692025290639e-06
set sigmaV0(9402) 9.870000
set ruPrev(9402) 0.0

# Element 9403: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9403) {822 766 2413 2437 83 61 764 820}
set elemKinit(9403) 6.169692025290639e-06
set sigmaV0(9403) 9.870000
set ruPrev(9403) 0.0

# Element 9404: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9404) {817 761 62 84 823 767 64 86}
set elemKinit(9404) 6.169692025290639e-06
set sigmaV0(9404) 88.830000
set ruPrev(9404) 0.0

# Element 9405: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9405) {818 762 761 817 824 768 767 823}
set elemKinit(9405) 6.169692025290639e-06
set sigmaV0(9405) 69.090000
set ruPrev(9405) 0.0

# Element 9406: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9406) {819 763 762 818 825 769 768 824}
set elemKinit(9406) 6.169692025290639e-06
set sigmaV0(9406) 49.350000
set ruPrev(9406) 0.0

# Element 9407: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9407) {820 764 763 819 826 770 769 825}
set elemKinit(9407) 6.169692025290639e-06
set sigmaV0(9407) 29.610000
set ruPrev(9407) 0.0

# Element 9408: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9408) {83 61 764 820 85 63 770 826}
set elemKinit(9408) 6.169692025290639e-06
set sigmaV0(9408) 9.870000
set ruPrev(9408) 0.0

# Element 9409: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9409) {823 767 64 86 2438 2414 775 831}
set elemKinit(9409) 6.169692025290639e-06
set sigmaV0(9409) 88.830000
set ruPrev(9409) 0.0

# Element 9410: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9410) {2438 2414 775 831 2442 2418 776 832}
set elemKinit(9410) 6.169692025290639e-06
set sigmaV0(9410) 88.830000
set ruPrev(9410) 0.0

# Element 9411: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9411) {2442 2418 776 832 827 771 66 88}
set elemKinit(9411) 6.169692025290639e-06
set sigmaV0(9411) 88.830000
set ruPrev(9411) 0.0

# Element 9412: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9412) {824 768 767 823 2439 2415 2414 2438}
set elemKinit(9412) 6.169692025290639e-06
set sigmaV0(9412) 69.090000
set ruPrev(9412) 0.0

# Element 9413: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9413) {2439 2415 2414 2438 2443 2419 2418 2442}
set elemKinit(9413) 6.169692025290639e-06
set sigmaV0(9413) 69.090000
set ruPrev(9413) 0.0

# Element 9414: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9414) {2443 2419 2418 2442 828 772 771 827}
set elemKinit(9414) 6.169692025290639e-06
set sigmaV0(9414) 69.090000
set ruPrev(9414) 0.0

# Element 9415: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9415) {825 769 768 824 2440 2416 2415 2439}
set elemKinit(9415) 6.169692025290639e-06
set sigmaV0(9415) 49.350000
set ruPrev(9415) 0.0

# Element 9416: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9416) {2440 2416 2415 2439 2444 2420 2419 2443}
set elemKinit(9416) 6.169692025290639e-06
set sigmaV0(9416) 49.350000
set ruPrev(9416) 0.0

# Element 9417: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9417) {2444 2420 2419 2443 829 773 772 828}
set elemKinit(9417) 6.169692025290639e-06
set sigmaV0(9417) 49.350000
set ruPrev(9417) 0.0

# Element 9418: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9418) {826 770 769 825 2441 2417 2416 2440}
set elemKinit(9418) 6.169692025290639e-06
set sigmaV0(9418) 29.610000
set ruPrev(9418) 0.0

# Element 9419: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9419) {2441 2417 2416 2440 2445 2421 2420 2444}
set elemKinit(9419) 6.169692025290639e-06
set sigmaV0(9419) 29.610000
set ruPrev(9419) 0.0

# Element 9420: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9420) {2445 2421 2420 2444 830 774 773 829}
set elemKinit(9420) 6.169692025290639e-06
set sigmaV0(9420) 29.610000
set ruPrev(9420) 0.0

# Element 9421: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9421) {85 63 770 826 833 777 2417 2441}
set elemKinit(9421) 6.169692025290639e-06
set sigmaV0(9421) 9.870000
set ruPrev(9421) 0.0

# Element 9422: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9422) {833 777 2417 2441 834 778 2421 2445}
set elemKinit(9422) 6.169692025290639e-06
set sigmaV0(9422) 9.870000
set ruPrev(9422) 0.0

# Element 9423: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9423) {834 778 2421 2445 87 65 774 830}
set elemKinit(9423) 6.169692025290639e-06
set sigmaV0(9423) 9.870000
set ruPrev(9423) 0.0

# Element 9424: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9424) {835 779 68 90 2446 2422 787 843}
set elemKinit(9424) 6.169692025290639e-06
set sigmaV0(9424) 88.830000
set ruPrev(9424) 0.0

# Element 9425: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9425) {2446 2422 787 843 2450 2426 788 844}
set elemKinit(9425) 6.169692025290639e-06
set sigmaV0(9425) 88.830000
set ruPrev(9425) 0.0

# Element 9426: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9426) {2450 2426 788 844 839 783 70 92}
set elemKinit(9426) 6.169692025290639e-06
set sigmaV0(9426) 88.830000
set ruPrev(9426) 0.0

# Element 9427: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9427) {836 780 779 835 2447 2423 2422 2446}
set elemKinit(9427) 6.169692025290639e-06
set sigmaV0(9427) 69.090000
set ruPrev(9427) 0.0

# Element 9428: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9428) {2447 2423 2422 2446 2451 2427 2426 2450}
set elemKinit(9428) 6.169692025290639e-06
set sigmaV0(9428) 69.090000
set ruPrev(9428) 0.0

# Element 9429: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9429) {2451 2427 2426 2450 840 784 783 839}
set elemKinit(9429) 6.169692025290639e-06
set sigmaV0(9429) 69.090000
set ruPrev(9429) 0.0

# Element 9430: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9430) {837 781 780 836 2448 2424 2423 2447}
set elemKinit(9430) 6.169692025290639e-06
set sigmaV0(9430) 49.350000
set ruPrev(9430) 0.0

# Element 9431: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9431) {2448 2424 2423 2447 2452 2428 2427 2451}
set elemKinit(9431) 6.169692025290639e-06
set sigmaV0(9431) 49.350000
set ruPrev(9431) 0.0

# Element 9432: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9432) {2452 2428 2427 2451 841 785 784 840}
set elemKinit(9432) 6.169692025290639e-06
set sigmaV0(9432) 49.350000
set ruPrev(9432) 0.0

# Element 9433: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9433) {838 782 781 837 2449 2425 2424 2448}
set elemKinit(9433) 6.169692025290639e-06
set sigmaV0(9433) 29.610000
set ruPrev(9433) 0.0

# Element 9434: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9434) {2449 2425 2424 2448 2453 2429 2428 2452}
set elemKinit(9434) 6.169692025290639e-06
set sigmaV0(9434) 29.610000
set ruPrev(9434) 0.0

# Element 9435: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9435) {2453 2429 2428 2452 842 786 785 841}
set elemKinit(9435) 6.169692025290639e-06
set sigmaV0(9435) 29.610000
set ruPrev(9435) 0.0

# Element 9436: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9436) {89 67 782 838 845 789 2425 2449}
set elemKinit(9436) 6.169692025290639e-06
set sigmaV0(9436) 9.870000
set ruPrev(9436) 0.0

# Element 9437: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9437) {845 789 2425 2449 846 790 2429 2453}
set elemKinit(9437) 6.169692025290639e-06
set sigmaV0(9437) 9.870000
set ruPrev(9437) 0.0

# Element 9438: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9438) {846 790 2429 2453 91 69 786 842}
set elemKinit(9438) 6.169692025290639e-06
set sigmaV0(9438) 9.870000
set ruPrev(9438) 0.0

# Element 9439: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9439) {839 783 70 92 847 791 72 94}
set elemKinit(9439) 6.169692025290639e-06
set sigmaV0(9439) 88.830000
set ruPrev(9439) 0.0

# Element 9440: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9440) {840 784 783 839 848 792 791 847}
set elemKinit(9440) 6.169692025290639e-06
set sigmaV0(9440) 69.090000
set ruPrev(9440) 0.0

# Element 9441: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9441) {841 785 784 840 849 793 792 848}
set elemKinit(9441) 6.169692025290639e-06
set sigmaV0(9441) 49.350000
set ruPrev(9441) 0.0

# Element 9442: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9442) {842 786 785 841 850 794 793 849}
set elemKinit(9442) 6.169692025290639e-06
set sigmaV0(9442) 29.610000
set ruPrev(9442) 0.0

# Element 9443: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9443) {91 69 786 842 93 71 794 850}
set elemKinit(9443) 6.169692025290639e-06
set sigmaV0(9443) 9.870000
set ruPrev(9443) 0.0

# Element 9444: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9444) {847 791 72 94 2454 2430 799 855}
set elemKinit(9444) 6.169692025290639e-06
set sigmaV0(9444) 88.830000
set ruPrev(9444) 0.0

# Element 9445: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9445) {2454 2430 799 855 851 795 74 96}
set elemKinit(9445) 6.169692025290639e-06
set sigmaV0(9445) 88.830000
set ruPrev(9445) 0.0

# Element 9446: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9446) {848 792 791 847 2455 2431 2430 2454}
set elemKinit(9446) 6.169692025290639e-06
set sigmaV0(9446) 69.090000
set ruPrev(9446) 0.0

# Element 9447: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9447) {2455 2431 2430 2454 852 796 795 851}
set elemKinit(9447) 6.169692025290639e-06
set sigmaV0(9447) 69.090000
set ruPrev(9447) 0.0

# Element 9448: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9448) {849 793 792 848 2456 2432 2431 2455}
set elemKinit(9448) 6.169692025290639e-06
set sigmaV0(9448) 49.350000
set ruPrev(9448) 0.0

# Element 9449: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9449) {2456 2432 2431 2455 853 797 796 852}
set elemKinit(9449) 6.169692025290639e-06
set sigmaV0(9449) 49.350000
set ruPrev(9449) 0.0

# Element 9450: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9450) {850 794 793 849 2457 2433 2432 2456}
set elemKinit(9450) 6.169692025290639e-06
set sigmaV0(9450) 29.610000
set ruPrev(9450) 0.0

# Element 9451: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9451) {2457 2433 2432 2456 854 798 797 853}
set elemKinit(9451) 6.169692025290639e-06
set sigmaV0(9451) 29.610000
set ruPrev(9451) 0.0

# Element 9452: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9452) {93 71 794 850 856 800 2433 2457}
set elemKinit(9452) 6.169692025290639e-06
set sigmaV0(9452) 9.870000
set ruPrev(9452) 0.0

# Element 9453: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9453) {856 800 2433 2457 95 73 798 854}
set elemKinit(9453) 6.169692025290639e-06
set sigmaV0(9453) 9.870000
set ruPrev(9453) 0.0

# Element 9454: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9454) {851 795 74 96 857 801 76 98}
set elemKinit(9454) 6.169692025290639e-06
set sigmaV0(9454) 88.830000
set ruPrev(9454) 0.0

# Element 9455: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9455) {852 796 795 851 858 802 801 857}
set elemKinit(9455) 6.169692025290639e-06
set sigmaV0(9455) 69.090000
set ruPrev(9455) 0.0

# Element 9456: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9456) {853 797 796 852 859 803 802 858}
set elemKinit(9456) 6.169692025290639e-06
set sigmaV0(9456) 49.350000
set ruPrev(9456) 0.0

# Element 9457: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9457) {854 798 797 853 860 804 803 859}
set elemKinit(9457) 6.169692025290639e-06
set sigmaV0(9457) 29.610000
set ruPrev(9457) 0.0

# Element 9458: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9458) {95 73 798 854 97 75 804 860}
set elemKinit(9458) 6.169692025290639e-06
set sigmaV0(9458) 9.870000
set ruPrev(9458) 0.0

# Element 9459: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9459) {857 801 76 98 861 805 78 100}
set elemKinit(9459) 6.169692025290639e-06
set sigmaV0(9459) 88.830000
set ruPrev(9459) 0.0

# Element 9460: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9460) {858 802 801 857 862 806 805 861}
set elemKinit(9460) 6.169692025290639e-06
set sigmaV0(9460) 69.090000
set ruPrev(9460) 0.0

# Element 9461: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9461) {859 803 802 858 863 807 806 862}
set elemKinit(9461) 6.169692025290639e-06
set sigmaV0(9461) 49.350000
set ruPrev(9461) 0.0

# Element 9462: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9462) {860 804 803 859 864 808 807 863}
set elemKinit(9462) 6.169692025290639e-06
set sigmaV0(9462) 29.610000
set ruPrev(9462) 0.0

# Element 9463: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9463) {97 75 804 860 99 77 808 864}
set elemKinit(9463) 6.169692025290639e-06
set sigmaV0(9463) 9.870000
set ruPrev(9463) 0.0

# Element 9464: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9464) {861 805 78 100 865 809 80 102}
set elemKinit(9464) 6.169692025290639e-06
set sigmaV0(9464) 88.830000
set ruPrev(9464) 0.0

# Element 9465: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9465) {862 806 805 861 866 810 809 865}
set elemKinit(9465) 6.169692025290639e-06
set sigmaV0(9465) 69.090000
set ruPrev(9465) 0.0

# Element 9466: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9466) {863 807 806 862 867 811 810 866}
set elemKinit(9466) 6.169692025290639e-06
set sigmaV0(9466) 49.350000
set ruPrev(9466) 0.0

# Element 9467: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9467) {864 808 807 863 868 812 811 867}
set elemKinit(9467) 6.169692025290639e-06
set sigmaV0(9467) 29.610000
set ruPrev(9467) 0.0

# Element 9468: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9468) {99 77 808 864 101 79 812 868}
set elemKinit(9468) 6.169692025290639e-06
set sigmaV0(9468) 9.870000
set ruPrev(9468) 0.0

# Element 9469: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9469) {865 809 80 102 869 813 82 104}
set elemKinit(9469) 6.169692025290639e-06
set sigmaV0(9469) 88.830000
set ruPrev(9469) 0.0

# Element 9470: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9470) {866 810 809 865 870 814 813 869}
set elemKinit(9470) 6.169692025290639e-06
set sigmaV0(9470) 69.090000
set ruPrev(9470) 0.0

# Element 9471: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9471) {867 811 810 866 871 815 814 870}
set elemKinit(9471) 6.169692025290639e-06
set sigmaV0(9471) 49.350000
set ruPrev(9471) 0.0

# Element 9472: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9472) {868 812 811 867 872 816 815 871}
set elemKinit(9472) 6.169692025290639e-06
set sigmaV0(9472) 29.610000
set ruPrev(9472) 0.0

# Element 9473: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9473) {101 79 812 868 103 81 816 872}
set elemKinit(9473) 6.169692025290639e-06
set sigmaV0(9473) 9.870000
set ruPrev(9473) 0.0

# Element 9474: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9474) {869 813 82 104 2458 2434 821 877}
set elemKinit(9474) 6.169692025290639e-06
set sigmaV0(9474) 88.830000
set ruPrev(9474) 0.0

# Element 9475: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9475) {2458 2434 821 877 873 817 84 106}
set elemKinit(9475) 6.169692025290639e-06
set sigmaV0(9475) 88.830000
set ruPrev(9475) 0.0

# Element 9476: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9476) {870 814 813 869 2459 2435 2434 2458}
set elemKinit(9476) 6.169692025290639e-06
set sigmaV0(9476) 69.090000
set ruPrev(9476) 0.0

# Element 9477: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9477) {2459 2435 2434 2458 874 818 817 873}
set elemKinit(9477) 6.169692025290639e-06
set sigmaV0(9477) 69.090000
set ruPrev(9477) 0.0

# Element 9478: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9478) {871 815 814 870 2460 2436 2435 2459}
set elemKinit(9478) 6.169692025290639e-06
set sigmaV0(9478) 49.350000
set ruPrev(9478) 0.0

# Element 9479: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9479) {2460 2436 2435 2459 875 819 818 874}
set elemKinit(9479) 6.169692025290639e-06
set sigmaV0(9479) 49.350000
set ruPrev(9479) 0.0

# Element 9480: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9480) {872 816 815 871 2461 2437 2436 2460}
set elemKinit(9480) 6.169692025290639e-06
set sigmaV0(9480) 29.610000
set ruPrev(9480) 0.0

# Element 9481: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9481) {2461 2437 2436 2460 876 820 819 875}
set elemKinit(9481) 6.169692025290639e-06
set sigmaV0(9481) 29.610000
set ruPrev(9481) 0.0

# Element 9482: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9482) {103 81 816 872 878 822 2437 2461}
set elemKinit(9482) 6.169692025290639e-06
set sigmaV0(9482) 9.870000
set ruPrev(9482) 0.0

# Element 9483: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9483) {878 822 2437 2461 105 83 820 876}
set elemKinit(9483) 6.169692025290639e-06
set sigmaV0(9483) 9.870000
set ruPrev(9483) 0.0

# Element 9484: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9484) {873 817 84 106 879 823 86 108}
set elemKinit(9484) 6.169692025290639e-06
set sigmaV0(9484) 88.830000
set ruPrev(9484) 0.0

# Element 9485: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9485) {874 818 817 873 880 824 823 879}
set elemKinit(9485) 6.169692025290639e-06
set sigmaV0(9485) 69.090000
set ruPrev(9485) 0.0

# Element 9486: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9486) {875 819 818 874 881 825 824 880}
set elemKinit(9486) 6.169692025290639e-06
set sigmaV0(9486) 49.350000
set ruPrev(9486) 0.0

# Element 9487: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9487) {876 820 819 875 882 826 825 881}
set elemKinit(9487) 6.169692025290639e-06
set sigmaV0(9487) 29.610000
set ruPrev(9487) 0.0

# Element 9488: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9488) {105 83 820 876 107 85 826 882}
set elemKinit(9488) 6.169692025290639e-06
set sigmaV0(9488) 9.870000
set ruPrev(9488) 0.0

# Element 9489: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9489) {879 823 86 108 2462 2438 831 887}
set elemKinit(9489) 6.169692025290639e-06
set sigmaV0(9489) 88.830000
set ruPrev(9489) 0.0

# Element 9490: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9490) {2462 2438 831 887 2466 2442 832 888}
set elemKinit(9490) 6.169692025290639e-06
set sigmaV0(9490) 88.830000
set ruPrev(9490) 0.0

# Element 9491: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9491) {2466 2442 832 888 883 827 88 110}
set elemKinit(9491) 6.169692025290639e-06
set sigmaV0(9491) 88.830000
set ruPrev(9491) 0.0

# Element 9492: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9492) {880 824 823 879 2463 2439 2438 2462}
set elemKinit(9492) 6.169692025290639e-06
set sigmaV0(9492) 69.090000
set ruPrev(9492) 0.0

# Element 9493: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9493) {2463 2439 2438 2462 2467 2443 2442 2466}
set elemKinit(9493) 6.169692025290639e-06
set sigmaV0(9493) 69.090000
set ruPrev(9493) 0.0

# Element 9494: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9494) {2467 2443 2442 2466 884 828 827 883}
set elemKinit(9494) 6.169692025290639e-06
set sigmaV0(9494) 69.090000
set ruPrev(9494) 0.0

# Element 9495: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9495) {881 825 824 880 2464 2440 2439 2463}
set elemKinit(9495) 6.169692025290639e-06
set sigmaV0(9495) 49.350000
set ruPrev(9495) 0.0

# Element 9496: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9496) {2464 2440 2439 2463 2468 2444 2443 2467}
set elemKinit(9496) 6.169692025290639e-06
set sigmaV0(9496) 49.350000
set ruPrev(9496) 0.0

# Element 9497: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9497) {2468 2444 2443 2467 885 829 828 884}
set elemKinit(9497) 6.169692025290639e-06
set sigmaV0(9497) 49.350000
set ruPrev(9497) 0.0

# Element 9498: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9498) {882 826 825 881 2465 2441 2440 2464}
set elemKinit(9498) 6.169692025290639e-06
set sigmaV0(9498) 29.610000
set ruPrev(9498) 0.0

# Element 9499: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9499) {2465 2441 2440 2464 2469 2445 2444 2468}
set elemKinit(9499) 6.169692025290639e-06
set sigmaV0(9499) 29.610000
set ruPrev(9499) 0.0

# Element 9500: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9500) {2469 2445 2444 2468 886 830 829 885}
set elemKinit(9500) 6.169692025290639e-06
set sigmaV0(9500) 29.610000
set ruPrev(9500) 0.0

# Element 9501: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9501) {107 85 826 882 889 833 2441 2465}
set elemKinit(9501) 6.169692025290639e-06
set sigmaV0(9501) 9.870000
set ruPrev(9501) 0.0

# Element 9502: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9502) {889 833 2441 2465 890 834 2445 2469}
set elemKinit(9502) 6.169692025290639e-06
set sigmaV0(9502) 9.870000
set ruPrev(9502) 0.0

# Element 9503: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9503) {890 834 2445 2469 109 87 830 886}
set elemKinit(9503) 6.169692025290639e-06
set sigmaV0(9503) 9.870000
set ruPrev(9503) 0.0

# Element 9504: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9504) {891 835 90 112 2470 2446 843 899}
set elemKinit(9504) 6.169692025290639e-06
set sigmaV0(9504) 88.830000
set ruPrev(9504) 0.0

# Element 9505: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9505) {2470 2446 843 899 2474 2450 844 900}
set elemKinit(9505) 6.169692025290639e-06
set sigmaV0(9505) 88.830000
set ruPrev(9505) 0.0

# Element 9506: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9506) {2474 2450 844 900 895 839 92 114}
set elemKinit(9506) 6.169692025290639e-06
set sigmaV0(9506) 88.830000
set ruPrev(9506) 0.0

# Element 9507: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9507) {892 836 835 891 2471 2447 2446 2470}
set elemKinit(9507) 6.169692025290639e-06
set sigmaV0(9507) 69.090000
set ruPrev(9507) 0.0

# Element 9508: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9508) {2471 2447 2446 2470 2475 2451 2450 2474}
set elemKinit(9508) 6.169692025290639e-06
set sigmaV0(9508) 69.090000
set ruPrev(9508) 0.0

# Element 9509: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9509) {2475 2451 2450 2474 896 840 839 895}
set elemKinit(9509) 6.169692025290639e-06
set sigmaV0(9509) 69.090000
set ruPrev(9509) 0.0

# Element 9510: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9510) {893 837 836 892 2472 2448 2447 2471}
set elemKinit(9510) 6.169692025290639e-06
set sigmaV0(9510) 49.350000
set ruPrev(9510) 0.0

# Element 9511: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9511) {2472 2448 2447 2471 2476 2452 2451 2475}
set elemKinit(9511) 6.169692025290639e-06
set sigmaV0(9511) 49.350000
set ruPrev(9511) 0.0

# Element 9512: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9512) {2476 2452 2451 2475 897 841 840 896}
set elemKinit(9512) 6.169692025290639e-06
set sigmaV0(9512) 49.350000
set ruPrev(9512) 0.0

# Element 9513: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9513) {894 838 837 893 2473 2449 2448 2472}
set elemKinit(9513) 6.169692025290639e-06
set sigmaV0(9513) 29.610000
set ruPrev(9513) 0.0

# Element 9514: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9514) {2473 2449 2448 2472 2477 2453 2452 2476}
set elemKinit(9514) 6.169692025290639e-06
set sigmaV0(9514) 29.610000
set ruPrev(9514) 0.0

# Element 9515: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9515) {2477 2453 2452 2476 898 842 841 897}
set elemKinit(9515) 6.169692025290639e-06
set sigmaV0(9515) 29.610000
set ruPrev(9515) 0.0

# Element 9516: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9516) {111 89 838 894 901 845 2449 2473}
set elemKinit(9516) 6.169692025290639e-06
set sigmaV0(9516) 9.870000
set ruPrev(9516) 0.0

# Element 9517: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9517) {901 845 2449 2473 902 846 2453 2477}
set elemKinit(9517) 6.169692025290639e-06
set sigmaV0(9517) 9.870000
set ruPrev(9517) 0.0

# Element 9518: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9518) {902 846 2453 2477 113 91 842 898}
set elemKinit(9518) 6.169692025290639e-06
set sigmaV0(9518) 9.870000
set ruPrev(9518) 0.0

# Element 9519: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9519) {895 839 92 114 903 847 94 116}
set elemKinit(9519) 6.169692025290639e-06
set sigmaV0(9519) 88.830000
set ruPrev(9519) 0.0

# Element 9520: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9520) {896 840 839 895 904 848 847 903}
set elemKinit(9520) 6.169692025290639e-06
set sigmaV0(9520) 69.090000
set ruPrev(9520) 0.0

# Element 9521: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9521) {897 841 840 896 905 849 848 904}
set elemKinit(9521) 6.169692025290639e-06
set sigmaV0(9521) 49.350000
set ruPrev(9521) 0.0

# Element 9522: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9522) {898 842 841 897 906 850 849 905}
set elemKinit(9522) 6.169692025290639e-06
set sigmaV0(9522) 29.610000
set ruPrev(9522) 0.0

# Element 9523: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9523) {113 91 842 898 115 93 850 906}
set elemKinit(9523) 6.169692025290639e-06
set sigmaV0(9523) 9.870000
set ruPrev(9523) 0.0

# Element 9524: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9524) {903 847 94 116 2478 2454 855 911}
set elemKinit(9524) 6.169692025290639e-06
set sigmaV0(9524) 88.830000
set ruPrev(9524) 0.0

# Element 9525: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9525) {2478 2454 855 911 907 851 96 118}
set elemKinit(9525) 6.169692025290639e-06
set sigmaV0(9525) 88.830000
set ruPrev(9525) 0.0

# Element 9526: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9526) {904 848 847 903 2479 2455 2454 2478}
set elemKinit(9526) 6.169692025290639e-06
set sigmaV0(9526) 69.090000
set ruPrev(9526) 0.0

# Element 9527: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9527) {2479 2455 2454 2478 908 852 851 907}
set elemKinit(9527) 6.169692025290639e-06
set sigmaV0(9527) 69.090000
set ruPrev(9527) 0.0

# Element 9528: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9528) {905 849 848 904 2480 2456 2455 2479}
set elemKinit(9528) 6.169692025290639e-06
set sigmaV0(9528) 49.350000
set ruPrev(9528) 0.0

# Element 9529: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9529) {2480 2456 2455 2479 909 853 852 908}
set elemKinit(9529) 6.169692025290639e-06
set sigmaV0(9529) 49.350000
set ruPrev(9529) 0.0

# Element 9530: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9530) {906 850 849 905 2481 2457 2456 2480}
set elemKinit(9530) 6.169692025290639e-06
set sigmaV0(9530) 29.610000
set ruPrev(9530) 0.0

# Element 9531: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9531) {2481 2457 2456 2480 910 854 853 909}
set elemKinit(9531) 6.169692025290639e-06
set sigmaV0(9531) 29.610000
set ruPrev(9531) 0.0

# Element 9532: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9532) {115 93 850 906 912 856 2457 2481}
set elemKinit(9532) 6.169692025290639e-06
set sigmaV0(9532) 9.870000
set ruPrev(9532) 0.0

# Element 9533: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9533) {912 856 2457 2481 117 95 854 910}
set elemKinit(9533) 6.169692025290639e-06
set sigmaV0(9533) 9.870000
set ruPrev(9533) 0.0

# Element 9534: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9534) {907 851 96 118 913 857 98 120}
set elemKinit(9534) 6.169692025290639e-06
set sigmaV0(9534) 88.830000
set ruPrev(9534) 0.0

# Element 9535: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9535) {908 852 851 907 914 858 857 913}
set elemKinit(9535) 6.169692025290639e-06
set sigmaV0(9535) 69.090000
set ruPrev(9535) 0.0

# Element 9536: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9536) {909 853 852 908 915 859 858 914}
set elemKinit(9536) 6.169692025290639e-06
set sigmaV0(9536) 49.350000
set ruPrev(9536) 0.0

# Element 9537: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9537) {910 854 853 909 916 860 859 915}
set elemKinit(9537) 6.169692025290639e-06
set sigmaV0(9537) 29.610000
set ruPrev(9537) 0.0

# Element 9538: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9538) {117 95 854 910 119 97 860 916}
set elemKinit(9538) 6.169692025290639e-06
set sigmaV0(9538) 9.870000
set ruPrev(9538) 0.0

# Element 9539: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9539) {913 857 98 120 917 861 100 122}
set elemKinit(9539) 6.169692025290639e-06
set sigmaV0(9539) 88.830000
set ruPrev(9539) 0.0

# Element 9540: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9540) {914 858 857 913 918 862 861 917}
set elemKinit(9540) 6.169692025290639e-06
set sigmaV0(9540) 69.090000
set ruPrev(9540) 0.0

# Element 9541: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9541) {915 859 858 914 919 863 862 918}
set elemKinit(9541) 6.169692025290639e-06
set sigmaV0(9541) 49.350000
set ruPrev(9541) 0.0

# Element 9542: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9542) {916 860 859 915 920 864 863 919}
set elemKinit(9542) 6.169692025290639e-06
set sigmaV0(9542) 29.610000
set ruPrev(9542) 0.0

# Element 9543: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9543) {119 97 860 916 121 99 864 920}
set elemKinit(9543) 6.169692025290639e-06
set sigmaV0(9543) 9.870000
set ruPrev(9543) 0.0

# Element 9544: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9544) {917 861 100 122 921 865 102 124}
set elemKinit(9544) 6.169692025290639e-06
set sigmaV0(9544) 88.830000
set ruPrev(9544) 0.0

# Element 9545: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9545) {918 862 861 917 922 866 865 921}
set elemKinit(9545) 6.169692025290639e-06
set sigmaV0(9545) 69.090000
set ruPrev(9545) 0.0

# Element 9546: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9546) {919 863 862 918 923 867 866 922}
set elemKinit(9546) 6.169692025290639e-06
set sigmaV0(9546) 49.350000
set ruPrev(9546) 0.0

# Element 9547: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9547) {920 864 863 919 924 868 867 923}
set elemKinit(9547) 6.169692025290639e-06
set sigmaV0(9547) 29.610000
set ruPrev(9547) 0.0

# Element 9548: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9548) {121 99 864 920 123 101 868 924}
set elemKinit(9548) 6.169692025290639e-06
set sigmaV0(9548) 9.870000
set ruPrev(9548) 0.0

# Element 9549: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9549) {921 865 102 124 925 869 104 126}
set elemKinit(9549) 6.169692025290639e-06
set sigmaV0(9549) 88.830000
set ruPrev(9549) 0.0

# Element 9550: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9550) {922 866 865 921 926 870 869 925}
set elemKinit(9550) 6.169692025290639e-06
set sigmaV0(9550) 69.090000
set ruPrev(9550) 0.0

# Element 9551: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9551) {923 867 866 922 927 871 870 926}
set elemKinit(9551) 6.169692025290639e-06
set sigmaV0(9551) 49.350000
set ruPrev(9551) 0.0

# Element 9552: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9552) {924 868 867 923 928 872 871 927}
set elemKinit(9552) 6.169692025290639e-06
set sigmaV0(9552) 29.610000
set ruPrev(9552) 0.0

# Element 9553: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9553) {123 101 868 924 125 103 872 928}
set elemKinit(9553) 6.169692025290639e-06
set sigmaV0(9553) 9.870000
set ruPrev(9553) 0.0

# Element 9554: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9554) {925 869 104 126 2482 2458 877 933}
set elemKinit(9554) 6.169692025290639e-06
set sigmaV0(9554) 88.830000
set ruPrev(9554) 0.0

# Element 9555: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9555) {2482 2458 877 933 929 873 106 128}
set elemKinit(9555) 6.169692025290639e-06
set sigmaV0(9555) 88.830000
set ruPrev(9555) 0.0

# Element 9556: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9556) {926 870 869 925 2483 2459 2458 2482}
set elemKinit(9556) 6.169692025290639e-06
set sigmaV0(9556) 69.090000
set ruPrev(9556) 0.0

# Element 9557: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9557) {2483 2459 2458 2482 930 874 873 929}
set elemKinit(9557) 6.169692025290639e-06
set sigmaV0(9557) 69.090000
set ruPrev(9557) 0.0

# Element 9558: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9558) {927 871 870 926 2484 2460 2459 2483}
set elemKinit(9558) 6.169692025290639e-06
set sigmaV0(9558) 49.350000
set ruPrev(9558) 0.0

# Element 9559: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9559) {2484 2460 2459 2483 931 875 874 930}
set elemKinit(9559) 6.169692025290639e-06
set sigmaV0(9559) 49.350000
set ruPrev(9559) 0.0

# Element 9560: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9560) {928 872 871 927 2485 2461 2460 2484}
set elemKinit(9560) 6.169692025290639e-06
set sigmaV0(9560) 29.610000
set ruPrev(9560) 0.0

# Element 9561: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9561) {2485 2461 2460 2484 932 876 875 931}
set elemKinit(9561) 6.169692025290639e-06
set sigmaV0(9561) 29.610000
set ruPrev(9561) 0.0

# Element 9562: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9562) {125 103 872 928 934 878 2461 2485}
set elemKinit(9562) 6.169692025290639e-06
set sigmaV0(9562) 9.870000
set ruPrev(9562) 0.0

# Element 9563: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9563) {934 878 2461 2485 127 105 876 932}
set elemKinit(9563) 6.169692025290639e-06
set sigmaV0(9563) 9.870000
set ruPrev(9563) 0.0

# Element 9564: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9564) {929 873 106 128 935 879 108 130}
set elemKinit(9564) 6.169692025290639e-06
set sigmaV0(9564) 88.830000
set ruPrev(9564) 0.0

# Element 9565: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9565) {930 874 873 929 936 880 879 935}
set elemKinit(9565) 6.169692025290639e-06
set sigmaV0(9565) 69.090000
set ruPrev(9565) 0.0

# Element 9566: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9566) {931 875 874 930 937 881 880 936}
set elemKinit(9566) 6.169692025290639e-06
set sigmaV0(9566) 49.350000
set ruPrev(9566) 0.0

# Element 9567: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9567) {932 876 875 931 938 882 881 937}
set elemKinit(9567) 6.169692025290639e-06
set sigmaV0(9567) 29.610000
set ruPrev(9567) 0.0

# Element 9568: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9568) {127 105 876 932 129 107 882 938}
set elemKinit(9568) 6.169692025290639e-06
set sigmaV0(9568) 9.870000
set ruPrev(9568) 0.0

# Element 9569: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9569) {935 879 108 130 2486 2462 887 943}
set elemKinit(9569) 6.169692025290639e-06
set sigmaV0(9569) 88.830000
set ruPrev(9569) 0.0

# Element 9570: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9570) {2486 2462 887 943 2490 2466 888 944}
set elemKinit(9570) 6.169692025290639e-06
set sigmaV0(9570) 88.830000
set ruPrev(9570) 0.0

# Element 9571: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9571) {2490 2466 888 944 939 883 110 132}
set elemKinit(9571) 6.169692025290639e-06
set sigmaV0(9571) 88.830000
set ruPrev(9571) 0.0

# Element 9572: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9572) {936 880 879 935 2487 2463 2462 2486}
set elemKinit(9572) 6.169692025290639e-06
set sigmaV0(9572) 69.090000
set ruPrev(9572) 0.0

# Element 9573: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9573) {2487 2463 2462 2486 2491 2467 2466 2490}
set elemKinit(9573) 6.169692025290639e-06
set sigmaV0(9573) 69.090000
set ruPrev(9573) 0.0

# Element 9574: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9574) {2491 2467 2466 2490 940 884 883 939}
set elemKinit(9574) 6.169692025290639e-06
set sigmaV0(9574) 69.090000
set ruPrev(9574) 0.0

# Element 9575: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9575) {937 881 880 936 2488 2464 2463 2487}
set elemKinit(9575) 6.169692025290639e-06
set sigmaV0(9575) 49.350000
set ruPrev(9575) 0.0

# Element 9576: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9576) {2488 2464 2463 2487 2492 2468 2467 2491}
set elemKinit(9576) 6.169692025290639e-06
set sigmaV0(9576) 49.350000
set ruPrev(9576) 0.0

# Element 9577: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9577) {2492 2468 2467 2491 941 885 884 940}
set elemKinit(9577) 6.169692025290639e-06
set sigmaV0(9577) 49.350000
set ruPrev(9577) 0.0

# Element 9578: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9578) {938 882 881 937 2489 2465 2464 2488}
set elemKinit(9578) 6.169692025290639e-06
set sigmaV0(9578) 29.610000
set ruPrev(9578) 0.0

# Element 9579: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9579) {2489 2465 2464 2488 2493 2469 2468 2492}
set elemKinit(9579) 6.169692025290639e-06
set sigmaV0(9579) 29.610000
set ruPrev(9579) 0.0

# Element 9580: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9580) {2493 2469 2468 2492 942 886 885 941}
set elemKinit(9580) 6.169692025290639e-06
set sigmaV0(9580) 29.610000
set ruPrev(9580) 0.0

# Element 9581: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9581) {129 107 882 938 945 889 2465 2489}
set elemKinit(9581) 6.169692025290639e-06
set sigmaV0(9581) 9.870000
set ruPrev(9581) 0.0

# Element 9582: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9582) {945 889 2465 2489 946 890 2469 2493}
set elemKinit(9582) 6.169692025290639e-06
set sigmaV0(9582) 9.870000
set ruPrev(9582) 0.0

# Element 9583: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9583) {946 890 2469 2493 131 109 886 942}
set elemKinit(9583) 6.169692025290639e-06
set sigmaV0(9583) 9.870000
set ruPrev(9583) 0.0

# Element 9584: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9584) {2494 891 112 952 3258 2470 899 2510}
set elemKinit(9584) 6.169692025290639e-06
set sigmaV0(9584) 88.830000
set ruPrev(9584) 0.0

# Element 9585: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9585) {3258 2470 899 2510 3259 2474 900 2511}
set elemKinit(9585) 6.169692025290639e-06
set sigmaV0(9585) 88.830000
set ruPrev(9585) 0.0

# Element 9586: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9586) {3259 2474 900 2511 2498 895 114 958}
set elemKinit(9586) 6.169692025290639e-06
set sigmaV0(9586) 88.830000
set ruPrev(9586) 0.0

# Element 9587: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9587) {948 2494 952 134 2502 3258 2510 959}
set elemKinit(9587) 6.169692025290639e-06
set sigmaV0(9587) 88.830000
set ruPrev(9587) 0.0

# Element 9588: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9588) {2502 3258 2510 959 2506 3259 2511 960}
set elemKinit(9588) 6.169692025290639e-06
set sigmaV0(9588) 88.830000
set ruPrev(9588) 0.0

# Element 9589: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9589) {2506 3259 2511 960 954 2498 958 136}
set elemKinit(9589) 6.169692025290639e-06
set sigmaV0(9589) 88.830000
set ruPrev(9589) 0.0

# Element 9590: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9590) {2495 892 891 2494 3260 2471 2470 3258}
set elemKinit(9590) 6.169692025290639e-06
set sigmaV0(9590) 69.090000
set ruPrev(9590) 0.0

# Element 9591: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9591) {3260 2471 2470 3258 3261 2475 2474 3259}
set elemKinit(9591) 6.169692025290639e-06
set sigmaV0(9591) 69.090000
set ruPrev(9591) 0.0

# Element 9592: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9592) {3261 2475 2474 3259 2499 896 895 2498}
set elemKinit(9592) 6.169692025290639e-06
set sigmaV0(9592) 69.090000
set ruPrev(9592) 0.0

# Element 9593: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9593) {949 2495 2494 948 2503 3260 3258 2502}
set elemKinit(9593) 6.169692025290639e-06
set sigmaV0(9593) 69.090000
set ruPrev(9593) 0.0

# Element 9594: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9594) {2503 3260 3258 2502 2507 3261 3259 2506}
set elemKinit(9594) 6.169692025290639e-06
set sigmaV0(9594) 69.090000
set ruPrev(9594) 0.0

# Element 9595: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9595) {2507 3261 3259 2506 955 2499 2498 954}
set elemKinit(9595) 6.169692025290639e-06
set sigmaV0(9595) 69.090000
set ruPrev(9595) 0.0

# Element 9596: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9596) {2496 893 892 2495 3262 2472 2471 3260}
set elemKinit(9596) 6.169692025290639e-06
set sigmaV0(9596) 49.350000
set ruPrev(9596) 0.0

# Element 9597: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9597) {3262 2472 2471 3260 3263 2476 2475 3261}
set elemKinit(9597) 6.169692025290639e-06
set sigmaV0(9597) 49.350000
set ruPrev(9597) 0.0

# Element 9598: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9598) {3263 2476 2475 3261 2500 897 896 2499}
set elemKinit(9598) 6.169692025290639e-06
set sigmaV0(9598) 49.350000
set ruPrev(9598) 0.0

# Element 9599: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9599) {950 2496 2495 949 2504 3262 3260 2503}
set elemKinit(9599) 6.169692025290639e-06
set sigmaV0(9599) 49.350000
set ruPrev(9599) 0.0

# Element 9600: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9600) {2504 3262 3260 2503 2508 3263 3261 2507}
set elemKinit(9600) 6.169692025290639e-06
set sigmaV0(9600) 49.350000
set ruPrev(9600) 0.0

# Element 9601: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9601) {2508 3263 3261 2507 956 2500 2499 955}
set elemKinit(9601) 6.169692025290639e-06
set sigmaV0(9601) 49.350000
set ruPrev(9601) 0.0

# Element 9602: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9602) {2497 894 893 2496 3264 2473 2472 3262}
set elemKinit(9602) 6.169692025290639e-06
set sigmaV0(9602) 29.610000
set ruPrev(9602) 0.0

# Element 9603: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9603) {3264 2473 2472 3262 3265 2477 2476 3263}
set elemKinit(9603) 6.169692025290639e-06
set sigmaV0(9603) 29.610000
set ruPrev(9603) 0.0

# Element 9604: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9604) {3265 2477 2476 3263 2501 898 897 2500}
set elemKinit(9604) 6.169692025290639e-06
set sigmaV0(9604) 29.610000
set ruPrev(9604) 0.0

# Element 9605: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9605) {951 2497 2496 950 2505 3264 3262 2504}
set elemKinit(9605) 6.169692025290639e-06
set sigmaV0(9605) 29.610000
set ruPrev(9605) 0.0

# Element 9606: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9606) {2505 3264 3262 2504 2509 3265 3263 2508}
set elemKinit(9606) 6.169692025290639e-06
set sigmaV0(9606) 29.610000
set ruPrev(9606) 0.0

# Element 9607: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9607) {2509 3265 3263 2508 957 2501 2500 956}
set elemKinit(9607) 6.169692025290639e-06
set sigmaV0(9607) 29.610000
set ruPrev(9607) 0.0

# Element 9608: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9608) {947 111 894 2497 2512 901 2473 3264}
set elemKinit(9608) 6.169692025290639e-06
set sigmaV0(9608) 9.870000
set ruPrev(9608) 0.0

# Element 9609: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9609) {2512 901 2473 3264 2513 902 2477 3265}
set elemKinit(9609) 6.169692025290639e-06
set sigmaV0(9609) 9.870000
set ruPrev(9609) 0.0

# Element 9610: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9610) {2513 902 2477 3265 953 113 898 2501}
set elemKinit(9610) 6.169692025290639e-06
set sigmaV0(9610) 9.870000
set ruPrev(9610) 0.0

# Element 9611: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9611) {133 947 2497 951 961 2512 3264 2505}
set elemKinit(9611) 6.169692025290639e-06
set sigmaV0(9611) 9.870000
set ruPrev(9611) 0.0

# Element 9612: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9612) {961 2512 3264 2505 962 2513 3265 2509}
set elemKinit(9612) 6.169692025290639e-06
set sigmaV0(9612) 9.870000
set ruPrev(9612) 0.0

# Element 9613: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9613) {962 2513 3265 2509 135 953 2501 957}
set elemKinit(9613) 6.169692025290639e-06
set sigmaV0(9613) 9.870000
set ruPrev(9613) 0.0

# Element 9614: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9614) {2498 895 114 958 2514 903 116 968}
set elemKinit(9614) 6.169692025290639e-06
set sigmaV0(9614) 88.830000
set ruPrev(9614) 0.0

# Element 9615: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9615) {954 2498 958 136 964 2514 968 138}
set elemKinit(9615) 6.169692025290639e-06
set sigmaV0(9615) 88.830000
set ruPrev(9615) 0.0

# Element 9616: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9616) {2499 896 895 2498 2515 904 903 2514}
set elemKinit(9616) 6.169692025290639e-06
set sigmaV0(9616) 69.090000
set ruPrev(9616) 0.0

# Element 9617: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9617) {955 2499 2498 954 965 2515 2514 964}
set elemKinit(9617) 6.169692025290639e-06
set sigmaV0(9617) 69.090000
set ruPrev(9617) 0.0

# Element 9618: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9618) {2500 897 896 2499 2516 905 904 2515}
set elemKinit(9618) 6.169692025290639e-06
set sigmaV0(9618) 49.350000
set ruPrev(9618) 0.0

# Element 9619: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9619) {956 2500 2499 955 966 2516 2515 965}
set elemKinit(9619) 6.169692025290639e-06
set sigmaV0(9619) 49.350000
set ruPrev(9619) 0.0

# Element 9620: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9620) {2501 898 897 2500 2517 906 905 2516}
set elemKinit(9620) 6.169692025290639e-06
set sigmaV0(9620) 29.610000
set ruPrev(9620) 0.0

# Element 9621: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9621) {957 2501 2500 956 967 2517 2516 966}
set elemKinit(9621) 6.169692025290639e-06
set sigmaV0(9621) 29.610000
set ruPrev(9621) 0.0

# Element 9622: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9622) {953 113 898 2501 963 115 906 2517}
set elemKinit(9622) 6.169692025290639e-06
set sigmaV0(9622) 9.870000
set ruPrev(9622) 0.0

# Element 9623: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9623) {135 953 2501 957 137 963 2517 967}
set elemKinit(9623) 6.169692025290639e-06
set sigmaV0(9623) 9.870000
set ruPrev(9623) 0.0

# Element 9624: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9624) {2514 903 116 968 3266 2478 911 2526}
set elemKinit(9624) 6.169692025290639e-06
set sigmaV0(9624) 88.830000
set ruPrev(9624) 0.0

# Element 9625: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9625) {3266 2478 911 2526 2518 907 118 974}
set elemKinit(9625) 6.169692025290639e-06
set sigmaV0(9625) 88.830000
set ruPrev(9625) 0.0

# Element 9626: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9626) {964 2514 968 138 2522 3266 2526 975}
set elemKinit(9626) 6.169692025290639e-06
set sigmaV0(9626) 88.830000
set ruPrev(9626) 0.0

# Element 9627: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9627) {2522 3266 2526 975 970 2518 974 140}
set elemKinit(9627) 6.169692025290639e-06
set sigmaV0(9627) 88.830000
set ruPrev(9627) 0.0

# Element 9628: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9628) {2515 904 903 2514 3267 2479 2478 3266}
set elemKinit(9628) 6.169692025290639e-06
set sigmaV0(9628) 69.090000
set ruPrev(9628) 0.0

# Element 9629: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9629) {3267 2479 2478 3266 2519 908 907 2518}
set elemKinit(9629) 6.169692025290639e-06
set sigmaV0(9629) 69.090000
set ruPrev(9629) 0.0

# Element 9630: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9630) {965 2515 2514 964 2523 3267 3266 2522}
set elemKinit(9630) 6.169692025290639e-06
set sigmaV0(9630) 69.090000
set ruPrev(9630) 0.0

# Element 9631: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9631) {2523 3267 3266 2522 971 2519 2518 970}
set elemKinit(9631) 6.169692025290639e-06
set sigmaV0(9631) 69.090000
set ruPrev(9631) 0.0

# Element 9632: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9632) {2516 905 904 2515 3268 2480 2479 3267}
set elemKinit(9632) 6.169692025290639e-06
set sigmaV0(9632) 49.350000
set ruPrev(9632) 0.0

# Element 9633: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9633) {3268 2480 2479 3267 2520 909 908 2519}
set elemKinit(9633) 6.169692025290639e-06
set sigmaV0(9633) 49.350000
set ruPrev(9633) 0.0

# Element 9634: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9634) {966 2516 2515 965 2524 3268 3267 2523}
set elemKinit(9634) 6.169692025290639e-06
set sigmaV0(9634) 49.350000
set ruPrev(9634) 0.0

# Element 9635: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9635) {2524 3268 3267 2523 972 2520 2519 971}
set elemKinit(9635) 6.169692025290639e-06
set sigmaV0(9635) 49.350000
set ruPrev(9635) 0.0

# Element 9636: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9636) {2517 906 905 2516 3269 2481 2480 3268}
set elemKinit(9636) 6.169692025290639e-06
set sigmaV0(9636) 29.610000
set ruPrev(9636) 0.0

# Element 9637: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9637) {3269 2481 2480 3268 2521 910 909 2520}
set elemKinit(9637) 6.169692025290639e-06
set sigmaV0(9637) 29.610000
set ruPrev(9637) 0.0

# Element 9638: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9638) {967 2517 2516 966 2525 3269 3268 2524}
set elemKinit(9638) 6.169692025290639e-06
set sigmaV0(9638) 29.610000
set ruPrev(9638) 0.0

# Element 9639: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9639) {2525 3269 3268 2524 973 2521 2520 972}
set elemKinit(9639) 6.169692025290639e-06
set sigmaV0(9639) 29.610000
set ruPrev(9639) 0.0

# Element 9640: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9640) {963 115 906 2517 2527 912 2481 3269}
set elemKinit(9640) 6.169692025290639e-06
set sigmaV0(9640) 9.870000
set ruPrev(9640) 0.0

# Element 9641: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9641) {2527 912 2481 3269 969 117 910 2521}
set elemKinit(9641) 6.169692025290639e-06
set sigmaV0(9641) 9.870000
set ruPrev(9641) 0.0

# Element 9642: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9642) {137 963 2517 967 976 2527 3269 2525}
set elemKinit(9642) 6.169692025290639e-06
set sigmaV0(9642) 9.870000
set ruPrev(9642) 0.0

# Element 9643: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9643) {976 2527 3269 2525 139 969 2521 973}
set elemKinit(9643) 6.169692025290639e-06
set sigmaV0(9643) 9.870000
set ruPrev(9643) 0.0

# Element 9644: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9644) {2518 907 118 974 2528 913 120 982}
set elemKinit(9644) 6.169692025290639e-06
set sigmaV0(9644) 88.830000
set ruPrev(9644) 0.0

# Element 9645: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9645) {970 2518 974 140 978 2528 982 142}
set elemKinit(9645) 6.169692025290639e-06
set sigmaV0(9645) 88.830000
set ruPrev(9645) 0.0

# Element 9646: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9646) {2519 908 907 2518 2529 914 913 2528}
set elemKinit(9646) 6.169692025290639e-06
set sigmaV0(9646) 69.090000
set ruPrev(9646) 0.0

# Element 9647: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9647) {971 2519 2518 970 979 2529 2528 978}
set elemKinit(9647) 6.169692025290639e-06
set sigmaV0(9647) 69.090000
set ruPrev(9647) 0.0

# Element 9648: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9648) {2520 909 908 2519 2530 915 914 2529}
set elemKinit(9648) 6.169692025290639e-06
set sigmaV0(9648) 49.350000
set ruPrev(9648) 0.0

# Element 9649: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9649) {972 2520 2519 971 980 2530 2529 979}
set elemKinit(9649) 6.169692025290639e-06
set sigmaV0(9649) 49.350000
set ruPrev(9649) 0.0

# Element 9650: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9650) {2521 910 909 2520 2531 916 915 2530}
set elemKinit(9650) 6.169692025290639e-06
set sigmaV0(9650) 29.610000
set ruPrev(9650) 0.0

# Element 9651: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9651) {973 2521 2520 972 981 2531 2530 980}
set elemKinit(9651) 6.169692025290639e-06
set sigmaV0(9651) 29.610000
set ruPrev(9651) 0.0

# Element 9652: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9652) {969 117 910 2521 977 119 916 2531}
set elemKinit(9652) 6.169692025290639e-06
set sigmaV0(9652) 9.870000
set ruPrev(9652) 0.0

# Element 9653: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9653) {139 969 2521 973 141 977 2531 981}
set elemKinit(9653) 6.169692025290639e-06
set sigmaV0(9653) 9.870000
set ruPrev(9653) 0.0

# Element 9654: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9654) {2528 913 120 982 2532 917 122 988}
set elemKinit(9654) 6.169692025290639e-06
set sigmaV0(9654) 88.830000
set ruPrev(9654) 0.0

# Element 9655: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9655) {978 2528 982 142 984 2532 988 144}
set elemKinit(9655) 6.169692025290639e-06
set sigmaV0(9655) 88.830000
set ruPrev(9655) 0.0

# Element 9656: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9656) {2529 914 913 2528 2533 918 917 2532}
set elemKinit(9656) 6.169692025290639e-06
set sigmaV0(9656) 69.090000
set ruPrev(9656) 0.0

# Element 9657: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9657) {979 2529 2528 978 985 2533 2532 984}
set elemKinit(9657) 6.169692025290639e-06
set sigmaV0(9657) 69.090000
set ruPrev(9657) 0.0

# Element 9658: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9658) {2530 915 914 2529 2534 919 918 2533}
set elemKinit(9658) 6.169692025290639e-06
set sigmaV0(9658) 49.350000
set ruPrev(9658) 0.0

# Element 9659: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9659) {980 2530 2529 979 986 2534 2533 985}
set elemKinit(9659) 6.169692025290639e-06
set sigmaV0(9659) 49.350000
set ruPrev(9659) 0.0

# Element 9660: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9660) {2531 916 915 2530 2535 920 919 2534}
set elemKinit(9660) 6.169692025290639e-06
set sigmaV0(9660) 29.610000
set ruPrev(9660) 0.0

# Element 9661: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9661) {981 2531 2530 980 987 2535 2534 986}
set elemKinit(9661) 6.169692025290639e-06
set sigmaV0(9661) 29.610000
set ruPrev(9661) 0.0

# Element 9662: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9662) {977 119 916 2531 983 121 920 2535}
set elemKinit(9662) 6.169692025290639e-06
set sigmaV0(9662) 9.870000
set ruPrev(9662) 0.0

# Element 9663: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9663) {141 977 2531 981 143 983 2535 987}
set elemKinit(9663) 6.169692025290639e-06
set sigmaV0(9663) 9.870000
set ruPrev(9663) 0.0

# Element 9664: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9664) {2532 917 122 988 2536 921 124 994}
set elemKinit(9664) 6.169692025290639e-06
set sigmaV0(9664) 88.830000
set ruPrev(9664) 0.0

# Element 9665: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9665) {984 2532 988 144 990 2536 994 146}
set elemKinit(9665) 6.169692025290639e-06
set sigmaV0(9665) 88.830000
set ruPrev(9665) 0.0

# Element 9666: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9666) {2533 918 917 2532 2537 922 921 2536}
set elemKinit(9666) 6.169692025290639e-06
set sigmaV0(9666) 69.090000
set ruPrev(9666) 0.0

# Element 9667: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9667) {985 2533 2532 984 991 2537 2536 990}
set elemKinit(9667) 6.169692025290639e-06
set sigmaV0(9667) 69.090000
set ruPrev(9667) 0.0

# Element 9668: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9668) {2534 919 918 2533 2538 923 922 2537}
set elemKinit(9668) 6.169692025290639e-06
set sigmaV0(9668) 49.350000
set ruPrev(9668) 0.0

# Element 9669: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9669) {986 2534 2533 985 992 2538 2537 991}
set elemKinit(9669) 6.169692025290639e-06
set sigmaV0(9669) 49.350000
set ruPrev(9669) 0.0

# Element 9670: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9670) {2535 920 919 2534 2539 924 923 2538}
set elemKinit(9670) 6.169692025290639e-06
set sigmaV0(9670) 29.610000
set ruPrev(9670) 0.0

# Element 9671: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9671) {987 2535 2534 986 993 2539 2538 992}
set elemKinit(9671) 6.169692025290639e-06
set sigmaV0(9671) 29.610000
set ruPrev(9671) 0.0

# Element 9672: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9672) {983 121 920 2535 989 123 924 2539}
set elemKinit(9672) 6.169692025290639e-06
set sigmaV0(9672) 9.870000
set ruPrev(9672) 0.0

# Element 9673: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9673) {143 983 2535 987 145 989 2539 993}
set elemKinit(9673) 6.169692025290639e-06
set sigmaV0(9673) 9.870000
set ruPrev(9673) 0.0

# Element 9674: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9674) {2536 921 124 994 2540 925 126 1000}
set elemKinit(9674) 6.169692025290639e-06
set sigmaV0(9674) 88.830000
set ruPrev(9674) 0.0

# Element 9675: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9675) {990 2536 994 146 996 2540 1000 148}
set elemKinit(9675) 6.169692025290639e-06
set sigmaV0(9675) 88.830000
set ruPrev(9675) 0.0

# Element 9676: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9676) {2537 922 921 2536 2541 926 925 2540}
set elemKinit(9676) 6.169692025290639e-06
set sigmaV0(9676) 69.090000
set ruPrev(9676) 0.0

# Element 9677: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9677) {991 2537 2536 990 997 2541 2540 996}
set elemKinit(9677) 6.169692025290639e-06
set sigmaV0(9677) 69.090000
set ruPrev(9677) 0.0

# Element 9678: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9678) {2538 923 922 2537 2542 927 926 2541}
set elemKinit(9678) 6.169692025290639e-06
set sigmaV0(9678) 49.350000
set ruPrev(9678) 0.0

# Element 9679: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9679) {992 2538 2537 991 998 2542 2541 997}
set elemKinit(9679) 6.169692025290639e-06
set sigmaV0(9679) 49.350000
set ruPrev(9679) 0.0

# Element 9680: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9680) {2539 924 923 2538 2543 928 927 2542}
set elemKinit(9680) 6.169692025290639e-06
set sigmaV0(9680) 29.610000
set ruPrev(9680) 0.0

# Element 9681: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9681) {993 2539 2538 992 999 2543 2542 998}
set elemKinit(9681) 6.169692025290639e-06
set sigmaV0(9681) 29.610000
set ruPrev(9681) 0.0

# Element 9682: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9682) {989 123 924 2539 995 125 928 2543}
set elemKinit(9682) 6.169692025290639e-06
set sigmaV0(9682) 9.870000
set ruPrev(9682) 0.0

# Element 9683: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9683) {145 989 2539 993 147 995 2543 999}
set elemKinit(9683) 6.169692025290639e-06
set sigmaV0(9683) 9.870000
set ruPrev(9683) 0.0

# Element 9684: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9684) {2540 925 126 1000 3270 2482 933 2552}
set elemKinit(9684) 6.169692025290639e-06
set sigmaV0(9684) 88.830000
set ruPrev(9684) 0.0

# Element 9685: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9685) {3270 2482 933 2552 2544 929 128 1006}
set elemKinit(9685) 6.169692025290639e-06
set sigmaV0(9685) 88.830000
set ruPrev(9685) 0.0

# Element 9686: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9686) {996 2540 1000 148 2548 3270 2552 1007}
set elemKinit(9686) 6.169692025290639e-06
set sigmaV0(9686) 88.830000
set ruPrev(9686) 0.0

# Element 9687: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9687) {2548 3270 2552 1007 1002 2544 1006 150}
set elemKinit(9687) 6.169692025290639e-06
set sigmaV0(9687) 88.830000
set ruPrev(9687) 0.0

# Element 9688: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9688) {2541 926 925 2540 3271 2483 2482 3270}
set elemKinit(9688) 6.169692025290639e-06
set sigmaV0(9688) 69.090000
set ruPrev(9688) 0.0

# Element 9689: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9689) {3271 2483 2482 3270 2545 930 929 2544}
set elemKinit(9689) 6.169692025290639e-06
set sigmaV0(9689) 69.090000
set ruPrev(9689) 0.0

# Element 9690: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9690) {997 2541 2540 996 2549 3271 3270 2548}
set elemKinit(9690) 6.169692025290639e-06
set sigmaV0(9690) 69.090000
set ruPrev(9690) 0.0

# Element 9691: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9691) {2549 3271 3270 2548 1003 2545 2544 1002}
set elemKinit(9691) 6.169692025290639e-06
set sigmaV0(9691) 69.090000
set ruPrev(9691) 0.0

# Element 9692: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9692) {2542 927 926 2541 3272 2484 2483 3271}
set elemKinit(9692) 6.169692025290639e-06
set sigmaV0(9692) 49.350000
set ruPrev(9692) 0.0

# Element 9693: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9693) {3272 2484 2483 3271 2546 931 930 2545}
set elemKinit(9693) 6.169692025290639e-06
set sigmaV0(9693) 49.350000
set ruPrev(9693) 0.0

# Element 9694: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9694) {998 2542 2541 997 2550 3272 3271 2549}
set elemKinit(9694) 6.169692025290639e-06
set sigmaV0(9694) 49.350000
set ruPrev(9694) 0.0

# Element 9695: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9695) {2550 3272 3271 2549 1004 2546 2545 1003}
set elemKinit(9695) 6.169692025290639e-06
set sigmaV0(9695) 49.350000
set ruPrev(9695) 0.0

# Element 9696: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9696) {2543 928 927 2542 3273 2485 2484 3272}
set elemKinit(9696) 6.169692025290639e-06
set sigmaV0(9696) 29.610000
set ruPrev(9696) 0.0

# Element 9697: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9697) {3273 2485 2484 3272 2547 932 931 2546}
set elemKinit(9697) 6.169692025290639e-06
set sigmaV0(9697) 29.610000
set ruPrev(9697) 0.0

# Element 9698: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9698) {999 2543 2542 998 2551 3273 3272 2550}
set elemKinit(9698) 6.169692025290639e-06
set sigmaV0(9698) 29.610000
set ruPrev(9698) 0.0

# Element 9699: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9699) {2551 3273 3272 2550 1005 2547 2546 1004}
set elemKinit(9699) 6.169692025290639e-06
set sigmaV0(9699) 29.610000
set ruPrev(9699) 0.0

# Element 9700: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9700) {995 125 928 2543 2553 934 2485 3273}
set elemKinit(9700) 6.169692025290639e-06
set sigmaV0(9700) 9.870000
set ruPrev(9700) 0.0

# Element 9701: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9701) {2553 934 2485 3273 1001 127 932 2547}
set elemKinit(9701) 6.169692025290639e-06
set sigmaV0(9701) 9.870000
set ruPrev(9701) 0.0

# Element 9702: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9702) {147 995 2543 999 1008 2553 3273 2551}
set elemKinit(9702) 6.169692025290639e-06
set sigmaV0(9702) 9.870000
set ruPrev(9702) 0.0

# Element 9703: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9703) {1008 2553 3273 2551 149 1001 2547 1005}
set elemKinit(9703) 6.169692025290639e-06
set sigmaV0(9703) 9.870000
set ruPrev(9703) 0.0

# Element 9704: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9704) {2544 929 128 1006 2554 935 130 1014}
set elemKinit(9704) 6.169692025290639e-06
set sigmaV0(9704) 88.830000
set ruPrev(9704) 0.0

# Element 9705: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9705) {1002 2544 1006 150 1010 2554 1014 152}
set elemKinit(9705) 6.169692025290639e-06
set sigmaV0(9705) 88.830000
set ruPrev(9705) 0.0

# Element 9706: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9706) {2545 930 929 2544 2555 936 935 2554}
set elemKinit(9706) 6.169692025290639e-06
set sigmaV0(9706) 69.090000
set ruPrev(9706) 0.0

# Element 9707: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9707) {1003 2545 2544 1002 1011 2555 2554 1010}
set elemKinit(9707) 6.169692025290639e-06
set sigmaV0(9707) 69.090000
set ruPrev(9707) 0.0

# Element 9708: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9708) {2546 931 930 2545 2556 937 936 2555}
set elemKinit(9708) 6.169692025290639e-06
set sigmaV0(9708) 49.350000
set ruPrev(9708) 0.0

# Element 9709: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9709) {1004 2546 2545 1003 1012 2556 2555 1011}
set elemKinit(9709) 6.169692025290639e-06
set sigmaV0(9709) 49.350000
set ruPrev(9709) 0.0

# Element 9710: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9710) {2547 932 931 2546 2557 938 937 2556}
set elemKinit(9710) 6.169692025290639e-06
set sigmaV0(9710) 29.610000
set ruPrev(9710) 0.0

# Element 9711: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9711) {1005 2547 2546 1004 1013 2557 2556 1012}
set elemKinit(9711) 6.169692025290639e-06
set sigmaV0(9711) 29.610000
set ruPrev(9711) 0.0

# Element 9712: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9712) {1001 127 932 2547 1009 129 938 2557}
set elemKinit(9712) 6.169692025290639e-06
set sigmaV0(9712) 9.870000
set ruPrev(9712) 0.0

# Element 9713: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9713) {149 1001 2547 1005 151 1009 2557 1013}
set elemKinit(9713) 6.169692025290639e-06
set sigmaV0(9713) 9.870000
set ruPrev(9713) 0.0

# Element 9714: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9714) {2554 935 130 1014 3274 2486 943 2570}
set elemKinit(9714) 6.169692025290639e-06
set sigmaV0(9714) 88.830000
set ruPrev(9714) 0.0

# Element 9715: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9715) {3274 2486 943 2570 3275 2490 944 2571}
set elemKinit(9715) 6.169692025290639e-06
set sigmaV0(9715) 88.830000
set ruPrev(9715) 0.0

# Element 9716: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9716) {3275 2490 944 2571 2558 939 132 1020}
set elemKinit(9716) 6.169692025290639e-06
set sigmaV0(9716) 88.830000
set ruPrev(9716) 0.0

# Element 9717: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9717) {1010 2554 1014 152 2562 3274 2570 1021}
set elemKinit(9717) 6.169692025290639e-06
set sigmaV0(9717) 88.830000
set ruPrev(9717) 0.0

# Element 9718: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9718) {2562 3274 2570 1021 2566 3275 2571 1022}
set elemKinit(9718) 6.169692025290639e-06
set sigmaV0(9718) 88.830000
set ruPrev(9718) 0.0

# Element 9719: depth=9.00m, sigma_v0=88.83kPa, mat=1
set elemNodes(9719) {2566 3275 2571 1022 1016 2558 1020 154}
set elemKinit(9719) 6.169692025290639e-06
set sigmaV0(9719) 88.830000
set ruPrev(9719) 0.0

# Element 9720: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9720) {2555 936 935 2554 3276 2487 2486 3274}
set elemKinit(9720) 6.169692025290639e-06
set sigmaV0(9720) 69.090000
set ruPrev(9720) 0.0

# Element 9721: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9721) {3276 2487 2486 3274 3277 2491 2490 3275}
set elemKinit(9721) 6.169692025290639e-06
set sigmaV0(9721) 69.090000
set ruPrev(9721) 0.0

# Element 9722: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9722) {3277 2491 2490 3275 2559 940 939 2558}
set elemKinit(9722) 6.169692025290639e-06
set sigmaV0(9722) 69.090000
set ruPrev(9722) 0.0

# Element 9723: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9723) {1011 2555 2554 1010 2563 3276 3274 2562}
set elemKinit(9723) 6.169692025290639e-06
set sigmaV0(9723) 69.090000
set ruPrev(9723) 0.0

# Element 9724: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9724) {2563 3276 3274 2562 2567 3277 3275 2566}
set elemKinit(9724) 6.169692025290639e-06
set sigmaV0(9724) 69.090000
set ruPrev(9724) 0.0

# Element 9725: depth=7.00m, sigma_v0=69.09kPa, mat=1
set elemNodes(9725) {2567 3277 3275 2566 1017 2559 2558 1016}
set elemKinit(9725) 6.169692025290639e-06
set sigmaV0(9725) 69.090000
set ruPrev(9725) 0.0

# Element 9726: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9726) {2556 937 936 2555 3278 2488 2487 3276}
set elemKinit(9726) 6.169692025290639e-06
set sigmaV0(9726) 49.350000
set ruPrev(9726) 0.0

# Element 9727: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9727) {3278 2488 2487 3276 3279 2492 2491 3277}
set elemKinit(9727) 6.169692025290639e-06
set sigmaV0(9727) 49.350000
set ruPrev(9727) 0.0

# Element 9728: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9728) {3279 2492 2491 3277 2560 941 940 2559}
set elemKinit(9728) 6.169692025290639e-06
set sigmaV0(9728) 49.350000
set ruPrev(9728) 0.0

# Element 9729: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9729) {1012 2556 2555 1011 2564 3278 3276 2563}
set elemKinit(9729) 6.169692025290639e-06
set sigmaV0(9729) 49.350000
set ruPrev(9729) 0.0

# Element 9730: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9730) {2564 3278 3276 2563 2568 3279 3277 2567}
set elemKinit(9730) 6.169692025290639e-06
set sigmaV0(9730) 49.350000
set ruPrev(9730) 0.0

# Element 9731: depth=5.00m, sigma_v0=49.35kPa, mat=1
set elemNodes(9731) {2568 3279 3277 2567 1018 2560 2559 1017}
set elemKinit(9731) 6.169692025290639e-06
set sigmaV0(9731) 49.350000
set ruPrev(9731) 0.0

# Element 9732: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9732) {2557 938 937 2556 3280 2489 2488 3278}
set elemKinit(9732) 6.169692025290639e-06
set sigmaV0(9732) 29.610000
set ruPrev(9732) 0.0

# Element 9733: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9733) {3280 2489 2488 3278 3281 2493 2492 3279}
set elemKinit(9733) 6.169692025290639e-06
set sigmaV0(9733) 29.610000
set ruPrev(9733) 0.0

# Element 9734: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9734) {3281 2493 2492 3279 2561 942 941 2560}
set elemKinit(9734) 6.169692025290639e-06
set sigmaV0(9734) 29.610000
set ruPrev(9734) 0.0

# Element 9735: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9735) {1013 2557 2556 1012 2565 3280 3278 2564}
set elemKinit(9735) 6.169692025290639e-06
set sigmaV0(9735) 29.610000
set ruPrev(9735) 0.0

# Element 9736: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9736) {2565 3280 3278 2564 2569 3281 3279 2568}
set elemKinit(9736) 6.169692025290639e-06
set sigmaV0(9736) 29.610000
set ruPrev(9736) 0.0

# Element 9737: depth=3.00m, sigma_v0=29.61kPa, mat=1
set elemNodes(9737) {2569 3281 3279 2568 1019 2561 2560 1018}
set elemKinit(9737) 6.169692025290639e-06
set sigmaV0(9737) 29.610000
set ruPrev(9737) 0.0

# Element 9738: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9738) {1009 129 938 2557 2572 945 2489 3280}
set elemKinit(9738) 6.169692025290639e-06
set sigmaV0(9738) 9.870000
set ruPrev(9738) 0.0

# Element 9739: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9739) {2572 945 2489 3280 2573 946 2493 3281}
set elemKinit(9739) 6.169692025290639e-06
set sigmaV0(9739) 9.870000
set ruPrev(9739) 0.0

# Element 9740: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9740) {2573 946 2493 3281 1015 131 942 2561}
set elemKinit(9740) 6.169692025290639e-06
set sigmaV0(9740) 9.870000
set ruPrev(9740) 0.0

# Element 9741: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9741) {151 1009 2557 1013 1023 2572 3280 2565}
set elemKinit(9741) 6.169692025290639e-06
set sigmaV0(9741) 9.870000
set ruPrev(9741) 0.0

# Element 9742: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9742) {1023 2572 3280 2565 1024 2573 3281 2569}
set elemKinit(9742) 6.169692025290639e-06
set sigmaV0(9742) 9.870000
set ruPrev(9742) 0.0

# Element 9743: depth=1.00m, sigma_v0=9.87kPa, mat=1
set elemNodes(9743) {1024 2573 3281 2569 153 1015 2561 1019}
set elemKinit(9743) 6.169692025290639e-06
set sigmaV0(9743) 9.870000
set ruPrev(9743) 0.0

# Element 9744: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(9744) {2574 1025 155 1031 3282 2580 1039 2592}
set elemKinit(9744) 3.773200081582705e-06
set sigmaV0(9744) 158.752500
set ruPrev(9744) 0.0

# Element 9745: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(9745) {3282 2580 1039 2592 3283 2583 1040 2593}
set elemKinit(9745) 3.773200081582705e-06
set sigmaV0(9745) 158.752500
set ruPrev(9745) 0.0

# Element 9746: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(9746) {3283 2583 1040 2593 2577 1032 157 1038}
set elemKinit(9746) 3.773200081582705e-06
set sigmaV0(9746) 158.752500
set ruPrev(9746) 0.0

# Element 9747: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(9747) {1028 2574 1031 156 2586 3282 2592 1041}
set elemKinit(9747) 3.773200081582705e-06
set sigmaV0(9747) 158.752500
set ruPrev(9747) 0.0

# Element 9748: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(9748) {2586 3282 2592 1041 2589 3283 2593 1042}
set elemKinit(9748) 3.773200081582705e-06
set sigmaV0(9748) 158.752500
set ruPrev(9748) 0.0

# Element 9749: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(9749) {2589 3283 2593 1042 1035 2577 1038 158}
set elemKinit(9749) 3.773200081582705e-06
set sigmaV0(9749) 158.752500
set ruPrev(9749) 0.0

# Element 9750: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(9750) {2575 1026 1025 2574 3284 2581 2580 3282}
set elemKinit(9750) 3.773200081582705e-06
set sigmaV0(9750) 143.137500
set ruPrev(9750) 0.0

# Element 9751: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(9751) {3284 2581 2580 3282 3285 2584 2583 3283}
set elemKinit(9751) 3.773200081582705e-06
set sigmaV0(9751) 143.137500
set ruPrev(9751) 0.0

# Element 9752: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(9752) {3285 2584 2583 3283 2578 1033 1032 2577}
set elemKinit(9752) 3.773200081582705e-06
set sigmaV0(9752) 143.137500
set ruPrev(9752) 0.0

# Element 9753: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(9753) {1029 2575 2574 1028 2587 3284 3282 2586}
set elemKinit(9753) 3.773200081582705e-06
set sigmaV0(9753) 143.137500
set ruPrev(9753) 0.0

# Element 9754: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(9754) {2587 3284 3282 2586 2590 3285 3283 2589}
set elemKinit(9754) 3.773200081582705e-06
set sigmaV0(9754) 143.137500
set ruPrev(9754) 0.0

# Element 9755: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(9755) {2590 3285 3283 2589 1036 2578 2577 1035}
set elemKinit(9755) 3.773200081582705e-06
set sigmaV0(9755) 143.137500
set ruPrev(9755) 0.0

# Element 9756: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(9756) {2576 1027 1026 2575 3286 2582 2581 3284}
set elemKinit(9756) 3.773200081582705e-06
set sigmaV0(9756) 127.522500
set ruPrev(9756) 0.0

# Element 9757: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(9757) {3286 2582 2581 3284 3287 2585 2584 3285}
set elemKinit(9757) 3.773200081582705e-06
set sigmaV0(9757) 127.522500
set ruPrev(9757) 0.0

# Element 9758: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(9758) {3287 2585 2584 3285 2579 1034 1033 2578}
set elemKinit(9758) 3.773200081582705e-06
set sigmaV0(9758) 127.522500
set ruPrev(9758) 0.0

# Element 9759: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(9759) {1030 2576 2575 1029 2588 3286 3284 2587}
set elemKinit(9759) 3.773200081582705e-06
set sigmaV0(9759) 127.522500
set ruPrev(9759) 0.0

# Element 9760: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(9760) {2588 3286 3284 2587 2591 3287 3285 2590}
set elemKinit(9760) 3.773200081582705e-06
set sigmaV0(9760) 127.522500
set ruPrev(9760) 0.0

# Element 9761: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(9761) {2591 3287 3285 2590 1037 2579 2578 1036}
set elemKinit(9761) 3.773200081582705e-06
set sigmaV0(9761) 127.522500
set ruPrev(9761) 0.0

# Element 9762: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(9762) {598 1 1027 2576 2318 609 2582 3286}
set elemKinit(9762) 3.773200081582705e-06
set sigmaV0(9762) 111.907500
set ruPrev(9762) 0.0

# Element 9763: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(9763) {2318 609 2582 3286 2319 610 2585 3287}
set elemKinit(9763) 3.773200081582705e-06
set sigmaV0(9763) 111.907500
set ruPrev(9763) 0.0

# Element 9764: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(9764) {2319 610 2585 3287 608 5 1034 2579}
set elemKinit(9764) 3.773200081582705e-06
set sigmaV0(9764) 111.907500
set ruPrev(9764) 0.0

# Element 9765: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(9765) {4 598 2576 1030 613 2318 3286 2588}
set elemKinit(9765) 3.773200081582705e-06
set sigmaV0(9765) 111.907500
set ruPrev(9765) 0.0

# Element 9766: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(9766) {613 2318 3286 2588 614 2319 3287 2591}
set elemKinit(9766) 3.773200081582705e-06
set sigmaV0(9766) 111.907500
set ruPrev(9766) 0.0

# Element 9767: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(9767) {614 2319 3287 2591 8 608 2579 1037}
set elemKinit(9767) 3.773200081582705e-06
set sigmaV0(9767) 111.907500
set ruPrev(9767) 0.0

# Element 9768: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(9768) {2577 1032 157 1038 2594 1043 159 1049}
set elemKinit(9768) 3.773200081582705e-06
set sigmaV0(9768) 158.752500
set ruPrev(9768) 0.0

# Element 9769: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(9769) {1035 2577 1038 158 1046 2594 1049 160}
set elemKinit(9769) 3.773200081582705e-06
set sigmaV0(9769) 158.752500
set ruPrev(9769) 0.0

# Element 9770: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(9770) {2578 1033 1032 2577 2595 1044 1043 2594}
set elemKinit(9770) 3.773200081582705e-06
set sigmaV0(9770) 143.137500
set ruPrev(9770) 0.0

# Element 9771: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(9771) {1036 2578 2577 1035 1047 2595 2594 1046}
set elemKinit(9771) 3.773200081582705e-06
set sigmaV0(9771) 143.137500
set ruPrev(9771) 0.0

# Element 9772: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(9772) {2579 1034 1033 2578 2596 1045 1044 2595}
set elemKinit(9772) 3.773200081582705e-06
set sigmaV0(9772) 127.522500
set ruPrev(9772) 0.0

# Element 9773: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(9773) {1037 2579 2578 1036 1048 2596 2595 1047}
set elemKinit(9773) 3.773200081582705e-06
set sigmaV0(9773) 127.522500
set ruPrev(9773) 0.0

# Element 9774: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(9774) {608 5 1034 2579 626 9 1045 2596}
set elemKinit(9774) 3.773200081582705e-06
set sigmaV0(9774) 111.907500
set ruPrev(9774) 0.0

# Element 9775: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(9775) {8 608 2579 1037 12 626 2596 1048}
set elemKinit(9775) 3.773200081582705e-06
set sigmaV0(9775) 111.907500
set ruPrev(9775) 0.0

# Element 9776: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(9776) {2594 1043 159 1049 3288 2600 1057 2606}
set elemKinit(9776) 3.773200081582705e-06
set sigmaV0(9776) 158.752500
set ruPrev(9776) 0.0

# Element 9777: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(9777) {3288 2600 1057 2606 2597 1050 161 1056}
set elemKinit(9777) 3.773200081582705e-06
set sigmaV0(9777) 158.752500
set ruPrev(9777) 0.0

# Element 9778: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(9778) {1046 2594 1049 160 2603 3288 2606 1058}
set elemKinit(9778) 3.773200081582705e-06
set sigmaV0(9778) 158.752500
set ruPrev(9778) 0.0

# Element 9779: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(9779) {2603 3288 2606 1058 1053 2597 1056 162}
set elemKinit(9779) 3.773200081582705e-06
set sigmaV0(9779) 158.752500
set ruPrev(9779) 0.0

# Element 9780: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(9780) {2595 1044 1043 2594 3289 2601 2600 3288}
set elemKinit(9780) 3.773200081582705e-06
set sigmaV0(9780) 143.137500
set ruPrev(9780) 0.0

# Element 9781: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(9781) {3289 2601 2600 3288 2598 1051 1050 2597}
set elemKinit(9781) 3.773200081582705e-06
set sigmaV0(9781) 143.137500
set ruPrev(9781) 0.0

# Element 9782: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(9782) {1047 2595 2594 1046 2604 3289 3288 2603}
set elemKinit(9782) 3.773200081582705e-06
set sigmaV0(9782) 143.137500
set ruPrev(9782) 0.0

# Element 9783: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(9783) {2604 3289 3288 2603 1054 2598 2597 1053}
set elemKinit(9783) 3.773200081582705e-06
set sigmaV0(9783) 143.137500
set ruPrev(9783) 0.0

# Element 9784: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(9784) {2596 1045 1044 2595 3290 2602 2601 3289}
set elemKinit(9784) 3.773200081582705e-06
set sigmaV0(9784) 127.522500
set ruPrev(9784) 0.0

# Element 9785: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(9785) {3290 2602 2601 3289 2599 1052 1051 2598}
set elemKinit(9785) 3.773200081582705e-06
set sigmaV0(9785) 127.522500
set ruPrev(9785) 0.0

# Element 9786: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(9786) {1048 2596 2595 1047 2605 3290 3289 2604}
set elemKinit(9786) 3.773200081582705e-06
set sigmaV0(9786) 127.522500
set ruPrev(9786) 0.0

# Element 9787: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(9787) {2605 3290 3289 2604 1055 2599 2598 1054}
set elemKinit(9787) 3.773200081582705e-06
set sigmaV0(9787) 127.522500
set ruPrev(9787) 0.0

# Element 9788: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(9788) {626 9 1045 2596 2338 637 2602 3290}
set elemKinit(9788) 3.773200081582705e-06
set sigmaV0(9788) 111.907500
set ruPrev(9788) 0.0

# Element 9789: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(9789) {2338 637 2602 3290 636 13 1052 2599}
set elemKinit(9789) 3.773200081582705e-06
set sigmaV0(9789) 111.907500
set ruPrev(9789) 0.0

# Element 9790: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(9790) {12 626 2596 1048 639 2338 3290 2605}
set elemKinit(9790) 3.773200081582705e-06
set sigmaV0(9790) 111.907500
set ruPrev(9790) 0.0

# Element 9791: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(9791) {639 2338 3290 2605 16 636 2599 1055}
set elemKinit(9791) 3.773200081582705e-06
set sigmaV0(9791) 111.907500
set ruPrev(9791) 0.0

# Element 9792: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(9792) {2597 1050 161 1056 2607 1059 163 1065}
set elemKinit(9792) 3.773200081582705e-06
set sigmaV0(9792) 158.752500
set ruPrev(9792) 0.0

# Element 9793: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(9793) {1053 2597 1056 162 1062 2607 1065 164}
set elemKinit(9793) 3.773200081582705e-06
set sigmaV0(9793) 158.752500
set ruPrev(9793) 0.0

# Element 9794: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(9794) {2598 1051 1050 2597 2608 1060 1059 2607}
set elemKinit(9794) 3.773200081582705e-06
set sigmaV0(9794) 143.137500
set ruPrev(9794) 0.0

# Element 9795: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(9795) {1054 2598 2597 1053 1063 2608 2607 1062}
set elemKinit(9795) 3.773200081582705e-06
set sigmaV0(9795) 143.137500
set ruPrev(9795) 0.0

# Element 9796: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(9796) {2599 1052 1051 2598 2609 1061 1060 2608}
set elemKinit(9796) 3.773200081582705e-06
set sigmaV0(9796) 127.522500
set ruPrev(9796) 0.0

# Element 9797: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(9797) {1055 2599 2598 1054 1064 2609 2608 1063}
set elemKinit(9797) 3.773200081582705e-06
set sigmaV0(9797) 127.522500
set ruPrev(9797) 0.0

# Element 9798: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(9798) {636 13 1052 2599 650 17 1061 2609}
set elemKinit(9798) 3.773200081582705e-06
set sigmaV0(9798) 111.907500
set ruPrev(9798) 0.0

# Element 9799: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(9799) {16 636 2599 1055 20 650 2609 1064}
set elemKinit(9799) 3.773200081582705e-06
set sigmaV0(9799) 111.907500
set ruPrev(9799) 0.0

# Element 9800: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(9800) {2607 1059 163 1065 2610 1066 165 1072}
set elemKinit(9800) 3.773200081582705e-06
set sigmaV0(9800) 158.752500
set ruPrev(9800) 0.0

# Element 9801: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(9801) {1062 2607 1065 164 1069 2610 1072 166}
set elemKinit(9801) 3.773200081582705e-06
set sigmaV0(9801) 158.752500
set ruPrev(9801) 0.0

# Element 9802: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(9802) {2608 1060 1059 2607 2611 1067 1066 2610}
set elemKinit(9802) 3.773200081582705e-06
set sigmaV0(9802) 143.137500
set ruPrev(9802) 0.0

# Element 9803: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(9803) {1063 2608 2607 1062 1070 2611 2610 1069}
set elemKinit(9803) 3.773200081582705e-06
set sigmaV0(9803) 143.137500
set ruPrev(9803) 0.0

# Element 9804: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(9804) {2609 1061 1060 2608 2612 1068 1067 2611}
set elemKinit(9804) 3.773200081582705e-06
set sigmaV0(9804) 127.522500
set ruPrev(9804) 0.0

# Element 9805: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(9805) {1064 2609 2608 1063 1071 2612 2611 1070}
set elemKinit(9805) 3.773200081582705e-06
set sigmaV0(9805) 127.522500
set ruPrev(9805) 0.0

# Element 9806: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(9806) {650 17 1061 2609 660 21 1068 2612}
set elemKinit(9806) 3.773200081582705e-06
set sigmaV0(9806) 111.907500
set ruPrev(9806) 0.0

# Element 9807: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(9807) {20 650 2609 1064 24 660 2612 1071}
set elemKinit(9807) 3.773200081582705e-06
set sigmaV0(9807) 111.907500
set ruPrev(9807) 0.0

# Element 9808: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(9808) {2610 1066 165 1072 2613 1073 167 1079}
set elemKinit(9808) 3.773200081582705e-06
set sigmaV0(9808) 158.752500
set ruPrev(9808) 0.0

# Element 9809: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(9809) {1069 2610 1072 166 1076 2613 1079 168}
set elemKinit(9809) 3.773200081582705e-06
set sigmaV0(9809) 158.752500
set ruPrev(9809) 0.0

# Element 9810: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(9810) {2611 1067 1066 2610 2614 1074 1073 2613}
set elemKinit(9810) 3.773200081582705e-06
set sigmaV0(9810) 143.137500
set ruPrev(9810) 0.0

# Element 9811: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(9811) {1070 2611 2610 1069 1077 2614 2613 1076}
set elemKinit(9811) 3.773200081582705e-06
set sigmaV0(9811) 143.137500
set ruPrev(9811) 0.0

# Element 9812: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(9812) {2612 1068 1067 2611 2615 1075 1074 2614}
set elemKinit(9812) 3.773200081582705e-06
set sigmaV0(9812) 127.522500
set ruPrev(9812) 0.0

# Element 9813: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(9813) {1071 2612 2611 1070 1078 2615 2614 1077}
set elemKinit(9813) 3.773200081582705e-06
set sigmaV0(9813) 127.522500
set ruPrev(9813) 0.0

# Element 9814: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(9814) {660 21 1068 2612 670 25 1075 2615}
set elemKinit(9814) 3.773200081582705e-06
set sigmaV0(9814) 111.907500
set ruPrev(9814) 0.0

# Element 9815: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(9815) {24 660 2612 1071 28 670 2615 1078}
set elemKinit(9815) 3.773200081582705e-06
set sigmaV0(9815) 111.907500
set ruPrev(9815) 0.0

# Element 9816: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(9816) {2613 1073 167 1079 2616 1080 169 1086}
set elemKinit(9816) 3.773200081582705e-06
set sigmaV0(9816) 158.752500
set ruPrev(9816) 0.0

# Element 9817: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(9817) {1076 2613 1079 168 1083 2616 1086 170}
set elemKinit(9817) 3.773200081582705e-06
set sigmaV0(9817) 158.752500
set ruPrev(9817) 0.0

# Element 9818: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(9818) {2614 1074 1073 2613 2617 1081 1080 2616}
set elemKinit(9818) 3.773200081582705e-06
set sigmaV0(9818) 143.137500
set ruPrev(9818) 0.0

# Element 9819: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(9819) {1077 2614 2613 1076 1084 2617 2616 1083}
set elemKinit(9819) 3.773200081582705e-06
set sigmaV0(9819) 143.137500
set ruPrev(9819) 0.0

# Element 9820: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(9820) {2615 1075 1074 2614 2618 1082 1081 2617}
set elemKinit(9820) 3.773200081582705e-06
set sigmaV0(9820) 127.522500
set ruPrev(9820) 0.0

# Element 9821: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(9821) {1078 2615 2614 1077 1085 2618 2617 1084}
set elemKinit(9821) 3.773200081582705e-06
set sigmaV0(9821) 127.522500
set ruPrev(9821) 0.0

# Element 9822: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(9822) {670 25 1075 2615 680 29 1082 2618}
set elemKinit(9822) 3.773200081582705e-06
set sigmaV0(9822) 111.907500
set ruPrev(9822) 0.0

# Element 9823: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(9823) {28 670 2615 1078 32 680 2618 1085}
set elemKinit(9823) 3.773200081582705e-06
set sigmaV0(9823) 111.907500
set ruPrev(9823) 0.0

# Element 9824: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(9824) {2616 1080 169 1086 3291 2622 1094 2628}
set elemKinit(9824) 3.773200081582705e-06
set sigmaV0(9824) 158.752500
set ruPrev(9824) 0.0

# Element 9825: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(9825) {3291 2622 1094 2628 2619 1087 171 1093}
set elemKinit(9825) 3.773200081582705e-06
set sigmaV0(9825) 158.752500
set ruPrev(9825) 0.0

# Element 9826: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(9826) {1083 2616 1086 170 2625 3291 2628 1095}
set elemKinit(9826) 3.773200081582705e-06
set sigmaV0(9826) 158.752500
set ruPrev(9826) 0.0

# Element 9827: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(9827) {2625 3291 2628 1095 1090 2619 1093 172}
set elemKinit(9827) 3.773200081582705e-06
set sigmaV0(9827) 158.752500
set ruPrev(9827) 0.0

# Element 9828: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(9828) {2617 1081 1080 2616 3292 2623 2622 3291}
set elemKinit(9828) 3.773200081582705e-06
set sigmaV0(9828) 143.137500
set ruPrev(9828) 0.0

# Element 9829: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(9829) {3292 2623 2622 3291 2620 1088 1087 2619}
set elemKinit(9829) 3.773200081582705e-06
set sigmaV0(9829) 143.137500
set ruPrev(9829) 0.0

# Element 9830: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(9830) {1084 2617 2616 1083 2626 3292 3291 2625}
set elemKinit(9830) 3.773200081582705e-06
set sigmaV0(9830) 143.137500
set ruPrev(9830) 0.0

# Element 9831: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(9831) {2626 3292 3291 2625 1091 2620 2619 1090}
set elemKinit(9831) 3.773200081582705e-06
set sigmaV0(9831) 143.137500
set ruPrev(9831) 0.0

# Element 9832: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(9832) {2618 1082 1081 2617 3293 2624 2623 3292}
set elemKinit(9832) 3.773200081582705e-06
set sigmaV0(9832) 127.522500
set ruPrev(9832) 0.0

# Element 9833: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(9833) {3293 2624 2623 3292 2621 1089 1088 2620}
set elemKinit(9833) 3.773200081582705e-06
set sigmaV0(9833) 127.522500
set ruPrev(9833) 0.0

# Element 9834: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(9834) {1085 2618 2617 1084 2627 3293 3292 2626}
set elemKinit(9834) 3.773200081582705e-06
set sigmaV0(9834) 127.522500
set ruPrev(9834) 0.0

# Element 9835: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(9835) {2627 3293 3292 2626 1092 2621 2620 1091}
set elemKinit(9835) 3.773200081582705e-06
set sigmaV0(9835) 127.522500
set ruPrev(9835) 0.0

# Element 9836: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(9836) {680 29 1082 2618 2368 691 2624 3293}
set elemKinit(9836) 3.773200081582705e-06
set sigmaV0(9836) 111.907500
set ruPrev(9836) 0.0

# Element 9837: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(9837) {2368 691 2624 3293 690 33 1089 2621}
set elemKinit(9837) 3.773200081582705e-06
set sigmaV0(9837) 111.907500
set ruPrev(9837) 0.0

# Element 9838: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(9838) {32 680 2618 1085 693 2368 3293 2627}
set elemKinit(9838) 3.773200081582705e-06
set sigmaV0(9838) 111.907500
set ruPrev(9838) 0.0

# Element 9839: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(9839) {693 2368 3293 2627 36 690 2621 1092}
set elemKinit(9839) 3.773200081582705e-06
set sigmaV0(9839) 111.907500
set ruPrev(9839) 0.0

# Element 9840: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(9840) {2619 1087 171 1093 2629 1096 173 1102}
set elemKinit(9840) 3.773200081582705e-06
set sigmaV0(9840) 158.752500
set ruPrev(9840) 0.0

# Element 9841: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(9841) {1090 2619 1093 172 1099 2629 1102 174}
set elemKinit(9841) 3.773200081582705e-06
set sigmaV0(9841) 158.752500
set ruPrev(9841) 0.0

# Element 9842: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(9842) {2620 1088 1087 2619 2630 1097 1096 2629}
set elemKinit(9842) 3.773200081582705e-06
set sigmaV0(9842) 143.137500
set ruPrev(9842) 0.0

# Element 9843: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(9843) {1091 2620 2619 1090 1100 2630 2629 1099}
set elemKinit(9843) 3.773200081582705e-06
set sigmaV0(9843) 143.137500
set ruPrev(9843) 0.0

# Element 9844: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(9844) {2621 1089 1088 2620 2631 1098 1097 2630}
set elemKinit(9844) 3.773200081582705e-06
set sigmaV0(9844) 127.522500
set ruPrev(9844) 0.0

# Element 9845: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(9845) {1092 2621 2620 1091 1101 2631 2630 1100}
set elemKinit(9845) 3.773200081582705e-06
set sigmaV0(9845) 127.522500
set ruPrev(9845) 0.0

# Element 9846: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(9846) {690 33 1089 2621 704 37 1098 2631}
set elemKinit(9846) 3.773200081582705e-06
set sigmaV0(9846) 111.907500
set ruPrev(9846) 0.0

# Element 9847: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(9847) {36 690 2621 1092 40 704 2631 1101}
set elemKinit(9847) 3.773200081582705e-06
set sigmaV0(9847) 111.907500
set ruPrev(9847) 0.0

# Element 9848: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(9848) {2629 1096 173 1102 3294 2635 1110 2647}
set elemKinit(9848) 3.773200081582705e-06
set sigmaV0(9848) 158.752500
set ruPrev(9848) 0.0

# Element 9849: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(9849) {3294 2635 1110 2647 3295 2638 1111 2648}
set elemKinit(9849) 3.773200081582705e-06
set sigmaV0(9849) 158.752500
set ruPrev(9849) 0.0

# Element 9850: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(9850) {3295 2638 1111 2648 2632 1103 175 1109}
set elemKinit(9850) 3.773200081582705e-06
set sigmaV0(9850) 158.752500
set ruPrev(9850) 0.0

# Element 9851: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(9851) {1099 2629 1102 174 2641 3294 2647 1112}
set elemKinit(9851) 3.773200081582705e-06
set sigmaV0(9851) 158.752500
set ruPrev(9851) 0.0

# Element 9852: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(9852) {2641 3294 2647 1112 2644 3295 2648 1113}
set elemKinit(9852) 3.773200081582705e-06
set sigmaV0(9852) 158.752500
set ruPrev(9852) 0.0

# Element 9853: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(9853) {2644 3295 2648 1113 1106 2632 1109 176}
set elemKinit(9853) 3.773200081582705e-06
set sigmaV0(9853) 158.752500
set ruPrev(9853) 0.0

# Element 9854: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(9854) {2630 1097 1096 2629 3296 2636 2635 3294}
set elemKinit(9854) 3.773200081582705e-06
set sigmaV0(9854) 143.137500
set ruPrev(9854) 0.0

# Element 9855: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(9855) {3296 2636 2635 3294 3297 2639 2638 3295}
set elemKinit(9855) 3.773200081582705e-06
set sigmaV0(9855) 143.137500
set ruPrev(9855) 0.0

# Element 9856: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(9856) {3297 2639 2638 3295 2633 1104 1103 2632}
set elemKinit(9856) 3.773200081582705e-06
set sigmaV0(9856) 143.137500
set ruPrev(9856) 0.0

# Element 9857: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(9857) {1100 2630 2629 1099 2642 3296 3294 2641}
set elemKinit(9857) 3.773200081582705e-06
set sigmaV0(9857) 143.137500
set ruPrev(9857) 0.0

# Element 9858: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(9858) {2642 3296 3294 2641 2645 3297 3295 2644}
set elemKinit(9858) 3.773200081582705e-06
set sigmaV0(9858) 143.137500
set ruPrev(9858) 0.0

# Element 9859: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(9859) {2645 3297 3295 2644 1107 2633 2632 1106}
set elemKinit(9859) 3.773200081582705e-06
set sigmaV0(9859) 143.137500
set ruPrev(9859) 0.0

# Element 9860: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(9860) {2631 1098 1097 2630 3298 2637 2636 3296}
set elemKinit(9860) 3.773200081582705e-06
set sigmaV0(9860) 127.522500
set ruPrev(9860) 0.0

# Element 9861: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(9861) {3298 2637 2636 3296 3299 2640 2639 3297}
set elemKinit(9861) 3.773200081582705e-06
set sigmaV0(9861) 127.522500
set ruPrev(9861) 0.0

# Element 9862: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(9862) {3299 2640 2639 3297 2634 1105 1104 2633}
set elemKinit(9862) 3.773200081582705e-06
set sigmaV0(9862) 127.522500
set ruPrev(9862) 0.0

# Element 9863: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(9863) {1101 2631 2630 1100 2643 3298 3296 2642}
set elemKinit(9863) 3.773200081582705e-06
set sigmaV0(9863) 127.522500
set ruPrev(9863) 0.0

# Element 9864: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(9864) {2643 3298 3296 2642 2646 3299 3297 2645}
set elemKinit(9864) 3.773200081582705e-06
set sigmaV0(9864) 127.522500
set ruPrev(9864) 0.0

# Element 9865: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(9865) {2646 3299 3297 2645 1108 2634 2633 1107}
set elemKinit(9865) 3.773200081582705e-06
set sigmaV0(9865) 127.522500
set ruPrev(9865) 0.0

# Element 9866: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(9866) {704 37 1098 2631 2394 715 2637 3298}
set elemKinit(9866) 3.773200081582705e-06
set sigmaV0(9866) 111.907500
set ruPrev(9866) 0.0

# Element 9867: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(9867) {2394 715 2637 3298 2395 716 2640 3299}
set elemKinit(9867) 3.773200081582705e-06
set sigmaV0(9867) 111.907500
set ruPrev(9867) 0.0

# Element 9868: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(9868) {2395 716 2640 3299 714 41 1105 2634}
set elemKinit(9868) 3.773200081582705e-06
set sigmaV0(9868) 111.907500
set ruPrev(9868) 0.0

# Element 9869: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(9869) {40 704 2631 1101 719 2394 3298 2643}
set elemKinit(9869) 3.773200081582705e-06
set sigmaV0(9869) 111.907500
set ruPrev(9869) 0.0

# Element 9870: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(9870) {719 2394 3298 2643 720 2395 3299 2646}
set elemKinit(9870) 3.773200081582705e-06
set sigmaV0(9870) 111.907500
set ruPrev(9870) 0.0

# Element 9871: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(9871) {720 2395 3299 2646 44 714 2634 1108}
set elemKinit(9871) 3.773200081582705e-06
set sigmaV0(9871) 111.907500
set ruPrev(9871) 0.0

# Element 9872: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(9872) {1114 1028 156 177 2649 2586 1041 1120}
set elemKinit(9872) 3.773200081582705e-06
set sigmaV0(9872) 158.752500
set ruPrev(9872) 0.0

# Element 9873: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(9873) {2649 2586 1041 1120 2652 2589 1042 1121}
set elemKinit(9873) 3.773200081582705e-06
set sigmaV0(9873) 158.752500
set ruPrev(9873) 0.0

# Element 9874: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(9874) {2652 2589 1042 1121 1117 1035 158 178}
set elemKinit(9874) 3.773200081582705e-06
set sigmaV0(9874) 158.752500
set ruPrev(9874) 0.0

# Element 9875: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(9875) {1115 1029 1028 1114 2650 2587 2586 2649}
set elemKinit(9875) 3.773200081582705e-06
set sigmaV0(9875) 143.137500
set ruPrev(9875) 0.0

# Element 9876: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(9876) {2650 2587 2586 2649 2653 2590 2589 2652}
set elemKinit(9876) 3.773200081582705e-06
set sigmaV0(9876) 143.137500
set ruPrev(9876) 0.0

# Element 9877: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(9877) {2653 2590 2589 2652 1118 1036 1035 1117}
set elemKinit(9877) 3.773200081582705e-06
set sigmaV0(9877) 143.137500
set ruPrev(9877) 0.0

# Element 9878: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(9878) {1116 1030 1029 1115 2651 2588 2587 2650}
set elemKinit(9878) 3.773200081582705e-06
set sigmaV0(9878) 127.522500
set ruPrev(9878) 0.0

# Element 9879: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(9879) {2651 2588 2587 2650 2654 2591 2590 2653}
set elemKinit(9879) 3.773200081582705e-06
set sigmaV0(9879) 127.522500
set ruPrev(9879) 0.0

# Element 9880: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(9880) {2654 2591 2590 2653 1119 1037 1036 1118}
set elemKinit(9880) 3.773200081582705e-06
set sigmaV0(9880) 127.522500
set ruPrev(9880) 0.0

# Element 9881: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(9881) {46 4 1030 1116 731 613 2588 2651}
set elemKinit(9881) 3.773200081582705e-06
set sigmaV0(9881) 111.907500
set ruPrev(9881) 0.0

# Element 9882: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(9882) {731 613 2588 2651 732 614 2591 2654}
set elemKinit(9882) 3.773200081582705e-06
set sigmaV0(9882) 111.907500
set ruPrev(9882) 0.0

# Element 9883: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(9883) {732 614 2591 2654 48 8 1037 1119}
set elemKinit(9883) 3.773200081582705e-06
set sigmaV0(9883) 111.907500
set ruPrev(9883) 0.0

# Element 9884: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(9884) {1117 1035 158 178 1122 1046 160 179}
set elemKinit(9884) 3.773200081582705e-06
set sigmaV0(9884) 158.752500
set ruPrev(9884) 0.0

# Element 9885: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(9885) {1118 1036 1035 1117 1123 1047 1046 1122}
set elemKinit(9885) 3.773200081582705e-06
set sigmaV0(9885) 143.137500
set ruPrev(9885) 0.0

# Element 9886: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(9886) {1119 1037 1036 1118 1124 1048 1047 1123}
set elemKinit(9886) 3.773200081582705e-06
set sigmaV0(9886) 127.522500
set ruPrev(9886) 0.0

# Element 9887: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(9887) {48 8 1037 1119 50 12 1048 1124}
set elemKinit(9887) 3.773200081582705e-06
set sigmaV0(9887) 111.907500
set ruPrev(9887) 0.0

# Element 9888: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(9888) {1122 1046 160 179 2655 2603 1058 1128}
set elemKinit(9888) 3.773200081582705e-06
set sigmaV0(9888) 158.752500
set ruPrev(9888) 0.0

# Element 9889: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(9889) {2655 2603 1058 1128 1125 1053 162 180}
set elemKinit(9889) 3.773200081582705e-06
set sigmaV0(9889) 158.752500
set ruPrev(9889) 0.0

# Element 9890: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(9890) {1123 1047 1046 1122 2656 2604 2603 2655}
set elemKinit(9890) 3.773200081582705e-06
set sigmaV0(9890) 143.137500
set ruPrev(9890) 0.0

# Element 9891: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(9891) {2656 2604 2603 2655 1126 1054 1053 1125}
set elemKinit(9891) 3.773200081582705e-06
set sigmaV0(9891) 143.137500
set ruPrev(9891) 0.0

# Element 9892: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(9892) {1124 1048 1047 1123 2657 2605 2604 2656}
set elemKinit(9892) 3.773200081582705e-06
set sigmaV0(9892) 127.522500
set ruPrev(9892) 0.0

# Element 9893: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(9893) {2657 2605 2604 2656 1127 1055 1054 1126}
set elemKinit(9893) 3.773200081582705e-06
set sigmaV0(9893) 127.522500
set ruPrev(9893) 0.0

# Element 9894: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(9894) {50 12 1048 1124 743 639 2605 2657}
set elemKinit(9894) 3.773200081582705e-06
set sigmaV0(9894) 111.907500
set ruPrev(9894) 0.0

# Element 9895: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(9895) {743 639 2605 2657 52 16 1055 1127}
set elemKinit(9895) 3.773200081582705e-06
set sigmaV0(9895) 111.907500
set ruPrev(9895) 0.0

# Element 9896: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(9896) {1125 1053 162 180 1129 1062 164 181}
set elemKinit(9896) 3.773200081582705e-06
set sigmaV0(9896) 158.752500
set ruPrev(9896) 0.0

# Element 9897: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(9897) {1126 1054 1053 1125 1130 1063 1062 1129}
set elemKinit(9897) 3.773200081582705e-06
set sigmaV0(9897) 143.137500
set ruPrev(9897) 0.0

# Element 9898: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(9898) {1127 1055 1054 1126 1131 1064 1063 1130}
set elemKinit(9898) 3.773200081582705e-06
set sigmaV0(9898) 127.522500
set ruPrev(9898) 0.0

# Element 9899: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(9899) {52 16 1055 1127 54 20 1064 1131}
set elemKinit(9899) 3.773200081582705e-06
set sigmaV0(9899) 111.907500
set ruPrev(9899) 0.0

# Element 9900: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(9900) {1129 1062 164 181 1132 1069 166 182}
set elemKinit(9900) 3.773200081582705e-06
set sigmaV0(9900) 158.752500
set ruPrev(9900) 0.0

# Element 9901: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(9901) {1130 1063 1062 1129 1133 1070 1069 1132}
set elemKinit(9901) 3.773200081582705e-06
set sigmaV0(9901) 143.137500
set ruPrev(9901) 0.0

# Element 9902: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(9902) {1131 1064 1063 1130 1134 1071 1070 1133}
set elemKinit(9902) 3.773200081582705e-06
set sigmaV0(9902) 127.522500
set ruPrev(9902) 0.0

# Element 9903: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(9903) {54 20 1064 1131 56 24 1071 1134}
set elemKinit(9903) 3.773200081582705e-06
set sigmaV0(9903) 111.907500
set ruPrev(9903) 0.0

# Element 9904: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(9904) {1132 1069 166 182 1135 1076 168 183}
set elemKinit(9904) 3.773200081582705e-06
set sigmaV0(9904) 158.752500
set ruPrev(9904) 0.0

# Element 9905: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(9905) {1133 1070 1069 1132 1136 1077 1076 1135}
set elemKinit(9905) 3.773200081582705e-06
set sigmaV0(9905) 143.137500
set ruPrev(9905) 0.0

# Element 9906: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(9906) {1134 1071 1070 1133 1137 1078 1077 1136}
set elemKinit(9906) 3.773200081582705e-06
set sigmaV0(9906) 127.522500
set ruPrev(9906) 0.0

# Element 9907: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(9907) {56 24 1071 1134 58 28 1078 1137}
set elemKinit(9907) 3.773200081582705e-06
set sigmaV0(9907) 111.907500
set ruPrev(9907) 0.0

# Element 9908: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(9908) {1135 1076 168 183 1138 1083 170 184}
set elemKinit(9908) 3.773200081582705e-06
set sigmaV0(9908) 158.752500
set ruPrev(9908) 0.0

# Element 9909: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(9909) {1136 1077 1076 1135 1139 1084 1083 1138}
set elemKinit(9909) 3.773200081582705e-06
set sigmaV0(9909) 143.137500
set ruPrev(9909) 0.0

# Element 9910: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(9910) {1137 1078 1077 1136 1140 1085 1084 1139}
set elemKinit(9910) 3.773200081582705e-06
set sigmaV0(9910) 127.522500
set ruPrev(9910) 0.0

# Element 9911: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(9911) {58 28 1078 1137 60 32 1085 1140}
set elemKinit(9911) 3.773200081582705e-06
set sigmaV0(9911) 111.907500
set ruPrev(9911) 0.0

# Element 9912: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(9912) {1138 1083 170 184 2658 2625 1095 1144}
set elemKinit(9912) 3.773200081582705e-06
set sigmaV0(9912) 158.752500
set ruPrev(9912) 0.0

# Element 9913: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(9913) {2658 2625 1095 1144 1141 1090 172 185}
set elemKinit(9913) 3.773200081582705e-06
set sigmaV0(9913) 158.752500
set ruPrev(9913) 0.0

# Element 9914: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(9914) {1139 1084 1083 1138 2659 2626 2625 2658}
set elemKinit(9914) 3.773200081582705e-06
set sigmaV0(9914) 143.137500
set ruPrev(9914) 0.0

# Element 9915: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(9915) {2659 2626 2625 2658 1142 1091 1090 1141}
set elemKinit(9915) 3.773200081582705e-06
set sigmaV0(9915) 143.137500
set ruPrev(9915) 0.0

# Element 9916: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(9916) {1140 1085 1084 1139 2660 2627 2626 2659}
set elemKinit(9916) 3.773200081582705e-06
set sigmaV0(9916) 127.522500
set ruPrev(9916) 0.0

# Element 9917: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(9917) {2660 2627 2626 2659 1143 1092 1091 1142}
set elemKinit(9917) 3.773200081582705e-06
set sigmaV0(9917) 127.522500
set ruPrev(9917) 0.0

# Element 9918: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(9918) {60 32 1085 1140 765 693 2627 2660}
set elemKinit(9918) 3.773200081582705e-06
set sigmaV0(9918) 111.907500
set ruPrev(9918) 0.0

# Element 9919: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(9919) {765 693 2627 2660 62 36 1092 1143}
set elemKinit(9919) 3.773200081582705e-06
set sigmaV0(9919) 111.907500
set ruPrev(9919) 0.0

# Element 9920: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(9920) {1141 1090 172 185 1145 1099 174 186}
set elemKinit(9920) 3.773200081582705e-06
set sigmaV0(9920) 158.752500
set ruPrev(9920) 0.0

# Element 9921: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(9921) {1142 1091 1090 1141 1146 1100 1099 1145}
set elemKinit(9921) 3.773200081582705e-06
set sigmaV0(9921) 143.137500
set ruPrev(9921) 0.0

# Element 9922: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(9922) {1143 1092 1091 1142 1147 1101 1100 1146}
set elemKinit(9922) 3.773200081582705e-06
set sigmaV0(9922) 127.522500
set ruPrev(9922) 0.0

# Element 9923: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(9923) {62 36 1092 1143 64 40 1101 1147}
set elemKinit(9923) 3.773200081582705e-06
set sigmaV0(9923) 111.907500
set ruPrev(9923) 0.0

# Element 9924: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(9924) {1145 1099 174 186 2661 2641 1112 1151}
set elemKinit(9924) 3.773200081582705e-06
set sigmaV0(9924) 158.752500
set ruPrev(9924) 0.0

# Element 9925: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(9925) {2661 2641 1112 1151 2664 2644 1113 1152}
set elemKinit(9925) 3.773200081582705e-06
set sigmaV0(9925) 158.752500
set ruPrev(9925) 0.0

# Element 9926: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(9926) {2664 2644 1113 1152 1148 1106 176 187}
set elemKinit(9926) 3.773200081582705e-06
set sigmaV0(9926) 158.752500
set ruPrev(9926) 0.0

# Element 9927: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(9927) {1146 1100 1099 1145 2662 2642 2641 2661}
set elemKinit(9927) 3.773200081582705e-06
set sigmaV0(9927) 143.137500
set ruPrev(9927) 0.0

# Element 9928: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(9928) {2662 2642 2641 2661 2665 2645 2644 2664}
set elemKinit(9928) 3.773200081582705e-06
set sigmaV0(9928) 143.137500
set ruPrev(9928) 0.0

# Element 9929: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(9929) {2665 2645 2644 2664 1149 1107 1106 1148}
set elemKinit(9929) 3.773200081582705e-06
set sigmaV0(9929) 143.137500
set ruPrev(9929) 0.0

# Element 9930: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(9930) {1147 1101 1100 1146 2663 2643 2642 2662}
set elemKinit(9930) 3.773200081582705e-06
set sigmaV0(9930) 127.522500
set ruPrev(9930) 0.0

# Element 9931: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(9931) {2663 2643 2642 2662 2666 2646 2645 2665}
set elemKinit(9931) 3.773200081582705e-06
set sigmaV0(9931) 127.522500
set ruPrev(9931) 0.0

# Element 9932: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(9932) {2666 2646 2645 2665 1150 1108 1107 1149}
set elemKinit(9932) 3.773200081582705e-06
set sigmaV0(9932) 127.522500
set ruPrev(9932) 0.0

# Element 9933: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(9933) {64 40 1101 1147 775 719 2643 2663}
set elemKinit(9933) 3.773200081582705e-06
set sigmaV0(9933) 111.907500
set ruPrev(9933) 0.0

# Element 9934: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(9934) {775 719 2643 2663 776 720 2646 2666}
set elemKinit(9934) 3.773200081582705e-06
set sigmaV0(9934) 111.907500
set ruPrev(9934) 0.0

# Element 9935: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(9935) {776 720 2646 2666 66 44 1108 1150}
set elemKinit(9935) 3.773200081582705e-06
set sigmaV0(9935) 111.907500
set ruPrev(9935) 0.0

# Element 9936: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(9936) {1153 1114 177 188 2667 2649 1120 1159}
set elemKinit(9936) 3.773200081582705e-06
set sigmaV0(9936) 158.752500
set ruPrev(9936) 0.0

# Element 9937: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(9937) {2667 2649 1120 1159 2670 2652 1121 1160}
set elemKinit(9937) 3.773200081582705e-06
set sigmaV0(9937) 158.752500
set ruPrev(9937) 0.0

# Element 9938: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(9938) {2670 2652 1121 1160 1156 1117 178 189}
set elemKinit(9938) 3.773200081582705e-06
set sigmaV0(9938) 158.752500
set ruPrev(9938) 0.0

# Element 9939: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(9939) {1154 1115 1114 1153 2668 2650 2649 2667}
set elemKinit(9939) 3.773200081582705e-06
set sigmaV0(9939) 143.137500
set ruPrev(9939) 0.0

# Element 9940: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(9940) {2668 2650 2649 2667 2671 2653 2652 2670}
set elemKinit(9940) 3.773200081582705e-06
set sigmaV0(9940) 143.137500
set ruPrev(9940) 0.0

# Element 9941: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(9941) {2671 2653 2652 2670 1157 1118 1117 1156}
set elemKinit(9941) 3.773200081582705e-06
set sigmaV0(9941) 143.137500
set ruPrev(9941) 0.0

# Element 9942: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(9942) {1155 1116 1115 1154 2669 2651 2650 2668}
set elemKinit(9942) 3.773200081582705e-06
set sigmaV0(9942) 127.522500
set ruPrev(9942) 0.0

# Element 9943: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(9943) {2669 2651 2650 2668 2672 2654 2653 2671}
set elemKinit(9943) 3.773200081582705e-06
set sigmaV0(9943) 127.522500
set ruPrev(9943) 0.0

# Element 9944: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(9944) {2672 2654 2653 2671 1158 1119 1118 1157}
set elemKinit(9944) 3.773200081582705e-06
set sigmaV0(9944) 127.522500
set ruPrev(9944) 0.0

# Element 9945: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(9945) {68 46 1116 1155 787 731 2651 2669}
set elemKinit(9945) 3.773200081582705e-06
set sigmaV0(9945) 111.907500
set ruPrev(9945) 0.0

# Element 9946: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(9946) {787 731 2651 2669 788 732 2654 2672}
set elemKinit(9946) 3.773200081582705e-06
set sigmaV0(9946) 111.907500
set ruPrev(9946) 0.0

# Element 9947: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(9947) {788 732 2654 2672 70 48 1119 1158}
set elemKinit(9947) 3.773200081582705e-06
set sigmaV0(9947) 111.907500
set ruPrev(9947) 0.0

# Element 9948: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(9948) {1156 1117 178 189 1161 1122 179 190}
set elemKinit(9948) 3.773200081582705e-06
set sigmaV0(9948) 158.752500
set ruPrev(9948) 0.0

# Element 9949: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(9949) {1157 1118 1117 1156 1162 1123 1122 1161}
set elemKinit(9949) 3.773200081582705e-06
set sigmaV0(9949) 143.137500
set ruPrev(9949) 0.0

# Element 9950: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(9950) {1158 1119 1118 1157 1163 1124 1123 1162}
set elemKinit(9950) 3.773200081582705e-06
set sigmaV0(9950) 127.522500
set ruPrev(9950) 0.0

# Element 9951: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(9951) {70 48 1119 1158 72 50 1124 1163}
set elemKinit(9951) 3.773200081582705e-06
set sigmaV0(9951) 111.907500
set ruPrev(9951) 0.0

# Element 9952: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(9952) {1161 1122 179 190 2673 2655 1128 1167}
set elemKinit(9952) 3.773200081582705e-06
set sigmaV0(9952) 158.752500
set ruPrev(9952) 0.0

# Element 9953: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(9953) {2673 2655 1128 1167 1164 1125 180 191}
set elemKinit(9953) 3.773200081582705e-06
set sigmaV0(9953) 158.752500
set ruPrev(9953) 0.0

# Element 9954: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(9954) {1162 1123 1122 1161 2674 2656 2655 2673}
set elemKinit(9954) 3.773200081582705e-06
set sigmaV0(9954) 143.137500
set ruPrev(9954) 0.0

# Element 9955: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(9955) {2674 2656 2655 2673 1165 1126 1125 1164}
set elemKinit(9955) 3.773200081582705e-06
set sigmaV0(9955) 143.137500
set ruPrev(9955) 0.0

# Element 9956: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(9956) {1163 1124 1123 1162 2675 2657 2656 2674}
set elemKinit(9956) 3.773200081582705e-06
set sigmaV0(9956) 127.522500
set ruPrev(9956) 0.0

# Element 9957: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(9957) {2675 2657 2656 2674 1166 1127 1126 1165}
set elemKinit(9957) 3.773200081582705e-06
set sigmaV0(9957) 127.522500
set ruPrev(9957) 0.0

# Element 9958: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(9958) {72 50 1124 1163 799 743 2657 2675}
set elemKinit(9958) 3.773200081582705e-06
set sigmaV0(9958) 111.907500
set ruPrev(9958) 0.0

# Element 9959: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(9959) {799 743 2657 2675 74 52 1127 1166}
set elemKinit(9959) 3.773200081582705e-06
set sigmaV0(9959) 111.907500
set ruPrev(9959) 0.0

# Element 9960: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(9960) {1164 1125 180 191 1168 1129 181 192}
set elemKinit(9960) 3.773200081582705e-06
set sigmaV0(9960) 158.752500
set ruPrev(9960) 0.0

# Element 9961: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(9961) {1165 1126 1125 1164 1169 1130 1129 1168}
set elemKinit(9961) 3.773200081582705e-06
set sigmaV0(9961) 143.137500
set ruPrev(9961) 0.0

# Element 9962: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(9962) {1166 1127 1126 1165 1170 1131 1130 1169}
set elemKinit(9962) 3.773200081582705e-06
set sigmaV0(9962) 127.522500
set ruPrev(9962) 0.0

# Element 9963: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(9963) {74 52 1127 1166 76 54 1131 1170}
set elemKinit(9963) 3.773200081582705e-06
set sigmaV0(9963) 111.907500
set ruPrev(9963) 0.0

# Element 9964: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(9964) {1168 1129 181 192 1171 1132 182 193}
set elemKinit(9964) 3.773200081582705e-06
set sigmaV0(9964) 158.752500
set ruPrev(9964) 0.0

# Element 9965: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(9965) {1169 1130 1129 1168 1172 1133 1132 1171}
set elemKinit(9965) 3.773200081582705e-06
set sigmaV0(9965) 143.137500
set ruPrev(9965) 0.0

# Element 9966: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(9966) {1170 1131 1130 1169 1173 1134 1133 1172}
set elemKinit(9966) 3.773200081582705e-06
set sigmaV0(9966) 127.522500
set ruPrev(9966) 0.0

# Element 9967: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(9967) {76 54 1131 1170 78 56 1134 1173}
set elemKinit(9967) 3.773200081582705e-06
set sigmaV0(9967) 111.907500
set ruPrev(9967) 0.0

# Element 9968: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(9968) {1171 1132 182 193 1174 1135 183 194}
set elemKinit(9968) 3.773200081582705e-06
set sigmaV0(9968) 158.752500
set ruPrev(9968) 0.0

# Element 9969: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(9969) {1172 1133 1132 1171 1175 1136 1135 1174}
set elemKinit(9969) 3.773200081582705e-06
set sigmaV0(9969) 143.137500
set ruPrev(9969) 0.0

# Element 9970: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(9970) {1173 1134 1133 1172 1176 1137 1136 1175}
set elemKinit(9970) 3.773200081582705e-06
set sigmaV0(9970) 127.522500
set ruPrev(9970) 0.0

# Element 9971: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(9971) {78 56 1134 1173 80 58 1137 1176}
set elemKinit(9971) 3.773200081582705e-06
set sigmaV0(9971) 111.907500
set ruPrev(9971) 0.0

# Element 9972: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(9972) {1174 1135 183 194 1177 1138 184 195}
set elemKinit(9972) 3.773200081582705e-06
set sigmaV0(9972) 158.752500
set ruPrev(9972) 0.0

# Element 9973: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(9973) {1175 1136 1135 1174 1178 1139 1138 1177}
set elemKinit(9973) 3.773200081582705e-06
set sigmaV0(9973) 143.137500
set ruPrev(9973) 0.0

# Element 9974: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(9974) {1176 1137 1136 1175 1179 1140 1139 1178}
set elemKinit(9974) 3.773200081582705e-06
set sigmaV0(9974) 127.522500
set ruPrev(9974) 0.0

# Element 9975: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(9975) {80 58 1137 1176 82 60 1140 1179}
set elemKinit(9975) 3.773200081582705e-06
set sigmaV0(9975) 111.907500
set ruPrev(9975) 0.0

# Element 9976: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(9976) {1177 1138 184 195 2676 2658 1144 1183}
set elemKinit(9976) 3.773200081582705e-06
set sigmaV0(9976) 158.752500
set ruPrev(9976) 0.0

# Element 9977: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(9977) {2676 2658 1144 1183 1180 1141 185 196}
set elemKinit(9977) 3.773200081582705e-06
set sigmaV0(9977) 158.752500
set ruPrev(9977) 0.0

# Element 9978: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(9978) {1178 1139 1138 1177 2677 2659 2658 2676}
set elemKinit(9978) 3.773200081582705e-06
set sigmaV0(9978) 143.137500
set ruPrev(9978) 0.0

# Element 9979: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(9979) {2677 2659 2658 2676 1181 1142 1141 1180}
set elemKinit(9979) 3.773200081582705e-06
set sigmaV0(9979) 143.137500
set ruPrev(9979) 0.0

# Element 9980: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(9980) {1179 1140 1139 1178 2678 2660 2659 2677}
set elemKinit(9980) 3.773200081582705e-06
set sigmaV0(9980) 127.522500
set ruPrev(9980) 0.0

# Element 9981: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(9981) {2678 2660 2659 2677 1182 1143 1142 1181}
set elemKinit(9981) 3.773200081582705e-06
set sigmaV0(9981) 127.522500
set ruPrev(9981) 0.0

# Element 9982: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(9982) {82 60 1140 1179 821 765 2660 2678}
set elemKinit(9982) 3.773200081582705e-06
set sigmaV0(9982) 111.907500
set ruPrev(9982) 0.0

# Element 9983: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(9983) {821 765 2660 2678 84 62 1143 1182}
set elemKinit(9983) 3.773200081582705e-06
set sigmaV0(9983) 111.907500
set ruPrev(9983) 0.0

# Element 9984: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(9984) {1180 1141 185 196 1184 1145 186 197}
set elemKinit(9984) 3.773200081582705e-06
set sigmaV0(9984) 158.752500
set ruPrev(9984) 0.0

# Element 9985: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(9985) {1181 1142 1141 1180 1185 1146 1145 1184}
set elemKinit(9985) 3.773200081582705e-06
set sigmaV0(9985) 143.137500
set ruPrev(9985) 0.0

# Element 9986: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(9986) {1182 1143 1142 1181 1186 1147 1146 1185}
set elemKinit(9986) 3.773200081582705e-06
set sigmaV0(9986) 127.522500
set ruPrev(9986) 0.0

# Element 9987: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(9987) {84 62 1143 1182 86 64 1147 1186}
set elemKinit(9987) 3.773200081582705e-06
set sigmaV0(9987) 111.907500
set ruPrev(9987) 0.0

# Element 9988: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(9988) {1184 1145 186 197 2679 2661 1151 1190}
set elemKinit(9988) 3.773200081582705e-06
set sigmaV0(9988) 158.752500
set ruPrev(9988) 0.0

# Element 9989: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(9989) {2679 2661 1151 1190 2682 2664 1152 1191}
set elemKinit(9989) 3.773200081582705e-06
set sigmaV0(9989) 158.752500
set ruPrev(9989) 0.0

# Element 9990: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(9990) {2682 2664 1152 1191 1187 1148 187 198}
set elemKinit(9990) 3.773200081582705e-06
set sigmaV0(9990) 158.752500
set ruPrev(9990) 0.0

# Element 9991: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(9991) {1185 1146 1145 1184 2680 2662 2661 2679}
set elemKinit(9991) 3.773200081582705e-06
set sigmaV0(9991) 143.137500
set ruPrev(9991) 0.0

# Element 9992: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(9992) {2680 2662 2661 2679 2683 2665 2664 2682}
set elemKinit(9992) 3.773200081582705e-06
set sigmaV0(9992) 143.137500
set ruPrev(9992) 0.0

# Element 9993: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(9993) {2683 2665 2664 2682 1188 1149 1148 1187}
set elemKinit(9993) 3.773200081582705e-06
set sigmaV0(9993) 143.137500
set ruPrev(9993) 0.0

# Element 9994: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(9994) {1186 1147 1146 1185 2681 2663 2662 2680}
set elemKinit(9994) 3.773200081582705e-06
set sigmaV0(9994) 127.522500
set ruPrev(9994) 0.0

# Element 9995: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(9995) {2681 2663 2662 2680 2684 2666 2665 2683}
set elemKinit(9995) 3.773200081582705e-06
set sigmaV0(9995) 127.522500
set ruPrev(9995) 0.0

# Element 9996: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(9996) {2684 2666 2665 2683 1189 1150 1149 1188}
set elemKinit(9996) 3.773200081582705e-06
set sigmaV0(9996) 127.522500
set ruPrev(9996) 0.0

# Element 9997: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(9997) {86 64 1147 1186 831 775 2663 2681}
set elemKinit(9997) 3.773200081582705e-06
set sigmaV0(9997) 111.907500
set ruPrev(9997) 0.0

# Element 9998: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(9998) {831 775 2663 2681 832 776 2666 2684}
set elemKinit(9998) 3.773200081582705e-06
set sigmaV0(9998) 111.907500
set ruPrev(9998) 0.0

# Element 9999: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(9999) {832 776 2666 2684 88 66 1150 1189}
set elemKinit(9999) 3.773200081582705e-06
set sigmaV0(9999) 111.907500
set ruPrev(9999) 0.0

# Element 10000: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(10000) {1192 1153 188 199 2685 2667 1159 1198}
set elemKinit(10000) 3.773200081582705e-06
set sigmaV0(10000) 158.752500
set ruPrev(10000) 0.0

# Element 10001: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(10001) {2685 2667 1159 1198 2688 2670 1160 1199}
set elemKinit(10001) 3.773200081582705e-06
set sigmaV0(10001) 158.752500
set ruPrev(10001) 0.0

# Element 10002: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(10002) {2688 2670 1160 1199 1195 1156 189 200}
set elemKinit(10002) 3.773200081582705e-06
set sigmaV0(10002) 158.752500
set ruPrev(10002) 0.0

# Element 10003: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(10003) {1193 1154 1153 1192 2686 2668 2667 2685}
set elemKinit(10003) 3.773200081582705e-06
set sigmaV0(10003) 143.137500
set ruPrev(10003) 0.0

# Element 10004: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(10004) {2686 2668 2667 2685 2689 2671 2670 2688}
set elemKinit(10004) 3.773200081582705e-06
set sigmaV0(10004) 143.137500
set ruPrev(10004) 0.0

# Element 10005: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(10005) {2689 2671 2670 2688 1196 1157 1156 1195}
set elemKinit(10005) 3.773200081582705e-06
set sigmaV0(10005) 143.137500
set ruPrev(10005) 0.0

# Element 10006: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(10006) {1194 1155 1154 1193 2687 2669 2668 2686}
set elemKinit(10006) 3.773200081582705e-06
set sigmaV0(10006) 127.522500
set ruPrev(10006) 0.0

# Element 10007: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(10007) {2687 2669 2668 2686 2690 2672 2671 2689}
set elemKinit(10007) 3.773200081582705e-06
set sigmaV0(10007) 127.522500
set ruPrev(10007) 0.0

# Element 10008: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(10008) {2690 2672 2671 2689 1197 1158 1157 1196}
set elemKinit(10008) 3.773200081582705e-06
set sigmaV0(10008) 127.522500
set ruPrev(10008) 0.0

# Element 10009: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(10009) {90 68 1155 1194 843 787 2669 2687}
set elemKinit(10009) 3.773200081582705e-06
set sigmaV0(10009) 111.907500
set ruPrev(10009) 0.0

# Element 10010: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(10010) {843 787 2669 2687 844 788 2672 2690}
set elemKinit(10010) 3.773200081582705e-06
set sigmaV0(10010) 111.907500
set ruPrev(10010) 0.0

# Element 10011: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(10011) {844 788 2672 2690 92 70 1158 1197}
set elemKinit(10011) 3.773200081582705e-06
set sigmaV0(10011) 111.907500
set ruPrev(10011) 0.0

# Element 10012: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(10012) {1195 1156 189 200 1200 1161 190 201}
set elemKinit(10012) 3.773200081582705e-06
set sigmaV0(10012) 158.752500
set ruPrev(10012) 0.0

# Element 10013: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(10013) {1196 1157 1156 1195 1201 1162 1161 1200}
set elemKinit(10013) 3.773200081582705e-06
set sigmaV0(10013) 143.137500
set ruPrev(10013) 0.0

# Element 10014: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(10014) {1197 1158 1157 1196 1202 1163 1162 1201}
set elemKinit(10014) 3.773200081582705e-06
set sigmaV0(10014) 127.522500
set ruPrev(10014) 0.0

# Element 10015: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(10015) {92 70 1158 1197 94 72 1163 1202}
set elemKinit(10015) 3.773200081582705e-06
set sigmaV0(10015) 111.907500
set ruPrev(10015) 0.0

# Element 10016: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(10016) {1200 1161 190 201 2691 2673 1167 1206}
set elemKinit(10016) 3.773200081582705e-06
set sigmaV0(10016) 158.752500
set ruPrev(10016) 0.0

# Element 10017: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(10017) {2691 2673 1167 1206 1203 1164 191 202}
set elemKinit(10017) 3.773200081582705e-06
set sigmaV0(10017) 158.752500
set ruPrev(10017) 0.0

# Element 10018: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(10018) {1201 1162 1161 1200 2692 2674 2673 2691}
set elemKinit(10018) 3.773200081582705e-06
set sigmaV0(10018) 143.137500
set ruPrev(10018) 0.0

# Element 10019: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(10019) {2692 2674 2673 2691 1204 1165 1164 1203}
set elemKinit(10019) 3.773200081582705e-06
set sigmaV0(10019) 143.137500
set ruPrev(10019) 0.0

# Element 10020: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(10020) {1202 1163 1162 1201 2693 2675 2674 2692}
set elemKinit(10020) 3.773200081582705e-06
set sigmaV0(10020) 127.522500
set ruPrev(10020) 0.0

# Element 10021: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(10021) {2693 2675 2674 2692 1205 1166 1165 1204}
set elemKinit(10021) 3.773200081582705e-06
set sigmaV0(10021) 127.522500
set ruPrev(10021) 0.0

# Element 10022: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(10022) {94 72 1163 1202 855 799 2675 2693}
set elemKinit(10022) 3.773200081582705e-06
set sigmaV0(10022) 111.907500
set ruPrev(10022) 0.0

# Element 10023: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(10023) {855 799 2675 2693 96 74 1166 1205}
set elemKinit(10023) 3.773200081582705e-06
set sigmaV0(10023) 111.907500
set ruPrev(10023) 0.0

# Element 10024: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(10024) {1203 1164 191 202 1207 1168 192 203}
set elemKinit(10024) 3.773200081582705e-06
set sigmaV0(10024) 158.752500
set ruPrev(10024) 0.0

# Element 10025: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(10025) {1204 1165 1164 1203 1208 1169 1168 1207}
set elemKinit(10025) 3.773200081582705e-06
set sigmaV0(10025) 143.137500
set ruPrev(10025) 0.0

# Element 10026: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(10026) {1205 1166 1165 1204 1209 1170 1169 1208}
set elemKinit(10026) 3.773200081582705e-06
set sigmaV0(10026) 127.522500
set ruPrev(10026) 0.0

# Element 10027: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(10027) {96 74 1166 1205 98 76 1170 1209}
set elemKinit(10027) 3.773200081582705e-06
set sigmaV0(10027) 111.907500
set ruPrev(10027) 0.0

# Element 10028: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(10028) {1207 1168 192 203 1210 1171 193 204}
set elemKinit(10028) 3.773200081582705e-06
set sigmaV0(10028) 158.752500
set ruPrev(10028) 0.0

# Element 10029: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(10029) {1208 1169 1168 1207 1211 1172 1171 1210}
set elemKinit(10029) 3.773200081582705e-06
set sigmaV0(10029) 143.137500
set ruPrev(10029) 0.0

# Element 10030: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(10030) {1209 1170 1169 1208 1212 1173 1172 1211}
set elemKinit(10030) 3.773200081582705e-06
set sigmaV0(10030) 127.522500
set ruPrev(10030) 0.0

# Element 10031: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(10031) {98 76 1170 1209 100 78 1173 1212}
set elemKinit(10031) 3.773200081582705e-06
set sigmaV0(10031) 111.907500
set ruPrev(10031) 0.0

# Element 10032: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(10032) {1210 1171 193 204 1213 1174 194 205}
set elemKinit(10032) 3.773200081582705e-06
set sigmaV0(10032) 158.752500
set ruPrev(10032) 0.0

# Element 10033: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(10033) {1211 1172 1171 1210 1214 1175 1174 1213}
set elemKinit(10033) 3.773200081582705e-06
set sigmaV0(10033) 143.137500
set ruPrev(10033) 0.0

# Element 10034: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(10034) {1212 1173 1172 1211 1215 1176 1175 1214}
set elemKinit(10034) 3.773200081582705e-06
set sigmaV0(10034) 127.522500
set ruPrev(10034) 0.0

# Element 10035: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(10035) {100 78 1173 1212 102 80 1176 1215}
set elemKinit(10035) 3.773200081582705e-06
set sigmaV0(10035) 111.907500
set ruPrev(10035) 0.0

# Element 10036: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(10036) {1213 1174 194 205 1216 1177 195 206}
set elemKinit(10036) 3.773200081582705e-06
set sigmaV0(10036) 158.752500
set ruPrev(10036) 0.0

# Element 10037: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(10037) {1214 1175 1174 1213 1217 1178 1177 1216}
set elemKinit(10037) 3.773200081582705e-06
set sigmaV0(10037) 143.137500
set ruPrev(10037) 0.0

# Element 10038: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(10038) {1215 1176 1175 1214 1218 1179 1178 1217}
set elemKinit(10038) 3.773200081582705e-06
set sigmaV0(10038) 127.522500
set ruPrev(10038) 0.0

# Element 10039: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(10039) {102 80 1176 1215 104 82 1179 1218}
set elemKinit(10039) 3.773200081582705e-06
set sigmaV0(10039) 111.907500
set ruPrev(10039) 0.0

# Element 10040: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(10040) {1216 1177 195 206 2694 2676 1183 1222}
set elemKinit(10040) 3.773200081582705e-06
set sigmaV0(10040) 158.752500
set ruPrev(10040) 0.0

# Element 10041: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(10041) {2694 2676 1183 1222 1219 1180 196 207}
set elemKinit(10041) 3.773200081582705e-06
set sigmaV0(10041) 158.752500
set ruPrev(10041) 0.0

# Element 10042: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(10042) {1217 1178 1177 1216 2695 2677 2676 2694}
set elemKinit(10042) 3.773200081582705e-06
set sigmaV0(10042) 143.137500
set ruPrev(10042) 0.0

# Element 10043: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(10043) {2695 2677 2676 2694 1220 1181 1180 1219}
set elemKinit(10043) 3.773200081582705e-06
set sigmaV0(10043) 143.137500
set ruPrev(10043) 0.0

# Element 10044: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(10044) {1218 1179 1178 1217 2696 2678 2677 2695}
set elemKinit(10044) 3.773200081582705e-06
set sigmaV0(10044) 127.522500
set ruPrev(10044) 0.0

# Element 10045: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(10045) {2696 2678 2677 2695 1221 1182 1181 1220}
set elemKinit(10045) 3.773200081582705e-06
set sigmaV0(10045) 127.522500
set ruPrev(10045) 0.0

# Element 10046: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(10046) {104 82 1179 1218 877 821 2678 2696}
set elemKinit(10046) 3.773200081582705e-06
set sigmaV0(10046) 111.907500
set ruPrev(10046) 0.0

# Element 10047: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(10047) {877 821 2678 2696 106 84 1182 1221}
set elemKinit(10047) 3.773200081582705e-06
set sigmaV0(10047) 111.907500
set ruPrev(10047) 0.0

# Element 10048: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(10048) {1219 1180 196 207 1223 1184 197 208}
set elemKinit(10048) 3.773200081582705e-06
set sigmaV0(10048) 158.752500
set ruPrev(10048) 0.0

# Element 10049: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(10049) {1220 1181 1180 1219 1224 1185 1184 1223}
set elemKinit(10049) 3.773200081582705e-06
set sigmaV0(10049) 143.137500
set ruPrev(10049) 0.0

# Element 10050: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(10050) {1221 1182 1181 1220 1225 1186 1185 1224}
set elemKinit(10050) 3.773200081582705e-06
set sigmaV0(10050) 127.522500
set ruPrev(10050) 0.0

# Element 10051: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(10051) {106 84 1182 1221 108 86 1186 1225}
set elemKinit(10051) 3.773200081582705e-06
set sigmaV0(10051) 111.907500
set ruPrev(10051) 0.0

# Element 10052: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(10052) {1223 1184 197 208 2697 2679 1190 1229}
set elemKinit(10052) 3.773200081582705e-06
set sigmaV0(10052) 158.752500
set ruPrev(10052) 0.0

# Element 10053: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(10053) {2697 2679 1190 1229 2700 2682 1191 1230}
set elemKinit(10053) 3.773200081582705e-06
set sigmaV0(10053) 158.752500
set ruPrev(10053) 0.0

# Element 10054: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(10054) {2700 2682 1191 1230 1226 1187 198 209}
set elemKinit(10054) 3.773200081582705e-06
set sigmaV0(10054) 158.752500
set ruPrev(10054) 0.0

# Element 10055: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(10055) {1224 1185 1184 1223 2698 2680 2679 2697}
set elemKinit(10055) 3.773200081582705e-06
set sigmaV0(10055) 143.137500
set ruPrev(10055) 0.0

# Element 10056: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(10056) {2698 2680 2679 2697 2701 2683 2682 2700}
set elemKinit(10056) 3.773200081582705e-06
set sigmaV0(10056) 143.137500
set ruPrev(10056) 0.0

# Element 10057: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(10057) {2701 2683 2682 2700 1227 1188 1187 1226}
set elemKinit(10057) 3.773200081582705e-06
set sigmaV0(10057) 143.137500
set ruPrev(10057) 0.0

# Element 10058: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(10058) {1225 1186 1185 1224 2699 2681 2680 2698}
set elemKinit(10058) 3.773200081582705e-06
set sigmaV0(10058) 127.522500
set ruPrev(10058) 0.0

# Element 10059: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(10059) {2699 2681 2680 2698 2702 2684 2683 2701}
set elemKinit(10059) 3.773200081582705e-06
set sigmaV0(10059) 127.522500
set ruPrev(10059) 0.0

# Element 10060: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(10060) {2702 2684 2683 2701 1228 1189 1188 1227}
set elemKinit(10060) 3.773200081582705e-06
set sigmaV0(10060) 127.522500
set ruPrev(10060) 0.0

# Element 10061: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(10061) {108 86 1186 1225 887 831 2681 2699}
set elemKinit(10061) 3.773200081582705e-06
set sigmaV0(10061) 111.907500
set ruPrev(10061) 0.0

# Element 10062: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(10062) {887 831 2681 2699 888 832 2684 2702}
set elemKinit(10062) 3.773200081582705e-06
set sigmaV0(10062) 111.907500
set ruPrev(10062) 0.0

# Element 10063: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(10063) {888 832 2684 2702 110 88 1189 1228}
set elemKinit(10063) 3.773200081582705e-06
set sigmaV0(10063) 111.907500
set ruPrev(10063) 0.0

# Element 10064: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(10064) {1231 1192 199 210 2703 2685 1198 1237}
set elemKinit(10064) 3.773200081582705e-06
set sigmaV0(10064) 158.752500
set ruPrev(10064) 0.0

# Element 10065: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(10065) {2703 2685 1198 1237 2706 2688 1199 1238}
set elemKinit(10065) 3.773200081582705e-06
set sigmaV0(10065) 158.752500
set ruPrev(10065) 0.0

# Element 10066: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(10066) {2706 2688 1199 1238 1234 1195 200 211}
set elemKinit(10066) 3.773200081582705e-06
set sigmaV0(10066) 158.752500
set ruPrev(10066) 0.0

# Element 10067: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(10067) {1232 1193 1192 1231 2704 2686 2685 2703}
set elemKinit(10067) 3.773200081582705e-06
set sigmaV0(10067) 143.137500
set ruPrev(10067) 0.0

# Element 10068: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(10068) {2704 2686 2685 2703 2707 2689 2688 2706}
set elemKinit(10068) 3.773200081582705e-06
set sigmaV0(10068) 143.137500
set ruPrev(10068) 0.0

# Element 10069: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(10069) {2707 2689 2688 2706 1235 1196 1195 1234}
set elemKinit(10069) 3.773200081582705e-06
set sigmaV0(10069) 143.137500
set ruPrev(10069) 0.0

# Element 10070: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(10070) {1233 1194 1193 1232 2705 2687 2686 2704}
set elemKinit(10070) 3.773200081582705e-06
set sigmaV0(10070) 127.522500
set ruPrev(10070) 0.0

# Element 10071: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(10071) {2705 2687 2686 2704 2708 2690 2689 2707}
set elemKinit(10071) 3.773200081582705e-06
set sigmaV0(10071) 127.522500
set ruPrev(10071) 0.0

# Element 10072: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(10072) {2708 2690 2689 2707 1236 1197 1196 1235}
set elemKinit(10072) 3.773200081582705e-06
set sigmaV0(10072) 127.522500
set ruPrev(10072) 0.0

# Element 10073: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(10073) {112 90 1194 1233 899 843 2687 2705}
set elemKinit(10073) 3.773200081582705e-06
set sigmaV0(10073) 111.907500
set ruPrev(10073) 0.0

# Element 10074: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(10074) {899 843 2687 2705 900 844 2690 2708}
set elemKinit(10074) 3.773200081582705e-06
set sigmaV0(10074) 111.907500
set ruPrev(10074) 0.0

# Element 10075: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(10075) {900 844 2690 2708 114 92 1197 1236}
set elemKinit(10075) 3.773200081582705e-06
set sigmaV0(10075) 111.907500
set ruPrev(10075) 0.0

# Element 10076: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(10076) {1234 1195 200 211 1239 1200 201 212}
set elemKinit(10076) 3.773200081582705e-06
set sigmaV0(10076) 158.752500
set ruPrev(10076) 0.0

# Element 10077: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(10077) {1235 1196 1195 1234 1240 1201 1200 1239}
set elemKinit(10077) 3.773200081582705e-06
set sigmaV0(10077) 143.137500
set ruPrev(10077) 0.0

# Element 10078: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(10078) {1236 1197 1196 1235 1241 1202 1201 1240}
set elemKinit(10078) 3.773200081582705e-06
set sigmaV0(10078) 127.522500
set ruPrev(10078) 0.0

# Element 10079: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(10079) {114 92 1197 1236 116 94 1202 1241}
set elemKinit(10079) 3.773200081582705e-06
set sigmaV0(10079) 111.907500
set ruPrev(10079) 0.0

# Element 10080: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(10080) {1239 1200 201 212 2709 2691 1206 1245}
set elemKinit(10080) 3.773200081582705e-06
set sigmaV0(10080) 158.752500
set ruPrev(10080) 0.0

# Element 10081: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(10081) {2709 2691 1206 1245 1242 1203 202 213}
set elemKinit(10081) 3.773200081582705e-06
set sigmaV0(10081) 158.752500
set ruPrev(10081) 0.0

# Element 10082: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(10082) {1240 1201 1200 1239 2710 2692 2691 2709}
set elemKinit(10082) 3.773200081582705e-06
set sigmaV0(10082) 143.137500
set ruPrev(10082) 0.0

# Element 10083: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(10083) {2710 2692 2691 2709 1243 1204 1203 1242}
set elemKinit(10083) 3.773200081582705e-06
set sigmaV0(10083) 143.137500
set ruPrev(10083) 0.0

# Element 10084: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(10084) {1241 1202 1201 1240 2711 2693 2692 2710}
set elemKinit(10084) 3.773200081582705e-06
set sigmaV0(10084) 127.522500
set ruPrev(10084) 0.0

# Element 10085: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(10085) {2711 2693 2692 2710 1244 1205 1204 1243}
set elemKinit(10085) 3.773200081582705e-06
set sigmaV0(10085) 127.522500
set ruPrev(10085) 0.0

# Element 10086: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(10086) {116 94 1202 1241 911 855 2693 2711}
set elemKinit(10086) 3.773200081582705e-06
set sigmaV0(10086) 111.907500
set ruPrev(10086) 0.0

# Element 10087: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(10087) {911 855 2693 2711 118 96 1205 1244}
set elemKinit(10087) 3.773200081582705e-06
set sigmaV0(10087) 111.907500
set ruPrev(10087) 0.0

# Element 10088: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(10088) {1242 1203 202 213 1246 1207 203 214}
set elemKinit(10088) 3.773200081582705e-06
set sigmaV0(10088) 158.752500
set ruPrev(10088) 0.0

# Element 10089: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(10089) {1243 1204 1203 1242 1247 1208 1207 1246}
set elemKinit(10089) 3.773200081582705e-06
set sigmaV0(10089) 143.137500
set ruPrev(10089) 0.0

# Element 10090: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(10090) {1244 1205 1204 1243 1248 1209 1208 1247}
set elemKinit(10090) 3.773200081582705e-06
set sigmaV0(10090) 127.522500
set ruPrev(10090) 0.0

# Element 10091: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(10091) {118 96 1205 1244 120 98 1209 1248}
set elemKinit(10091) 3.773200081582705e-06
set sigmaV0(10091) 111.907500
set ruPrev(10091) 0.0

# Element 10092: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(10092) {1246 1207 203 214 1249 1210 204 215}
set elemKinit(10092) 3.773200081582705e-06
set sigmaV0(10092) 158.752500
set ruPrev(10092) 0.0

# Element 10093: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(10093) {1247 1208 1207 1246 1250 1211 1210 1249}
set elemKinit(10093) 3.773200081582705e-06
set sigmaV0(10093) 143.137500
set ruPrev(10093) 0.0

# Element 10094: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(10094) {1248 1209 1208 1247 1251 1212 1211 1250}
set elemKinit(10094) 3.773200081582705e-06
set sigmaV0(10094) 127.522500
set ruPrev(10094) 0.0

# Element 10095: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(10095) {120 98 1209 1248 122 100 1212 1251}
set elemKinit(10095) 3.773200081582705e-06
set sigmaV0(10095) 111.907500
set ruPrev(10095) 0.0

# Element 10096: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(10096) {1249 1210 204 215 1252 1213 205 216}
set elemKinit(10096) 3.773200081582705e-06
set sigmaV0(10096) 158.752500
set ruPrev(10096) 0.0

# Element 10097: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(10097) {1250 1211 1210 1249 1253 1214 1213 1252}
set elemKinit(10097) 3.773200081582705e-06
set sigmaV0(10097) 143.137500
set ruPrev(10097) 0.0

# Element 10098: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(10098) {1251 1212 1211 1250 1254 1215 1214 1253}
set elemKinit(10098) 3.773200081582705e-06
set sigmaV0(10098) 127.522500
set ruPrev(10098) 0.0

# Element 10099: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(10099) {122 100 1212 1251 124 102 1215 1254}
set elemKinit(10099) 3.773200081582705e-06
set sigmaV0(10099) 111.907500
set ruPrev(10099) 0.0

# Element 10100: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(10100) {1252 1213 205 216 1255 1216 206 217}
set elemKinit(10100) 3.773200081582705e-06
set sigmaV0(10100) 158.752500
set ruPrev(10100) 0.0

# Element 10101: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(10101) {1253 1214 1213 1252 1256 1217 1216 1255}
set elemKinit(10101) 3.773200081582705e-06
set sigmaV0(10101) 143.137500
set ruPrev(10101) 0.0

# Element 10102: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(10102) {1254 1215 1214 1253 1257 1218 1217 1256}
set elemKinit(10102) 3.773200081582705e-06
set sigmaV0(10102) 127.522500
set ruPrev(10102) 0.0

# Element 10103: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(10103) {124 102 1215 1254 126 104 1218 1257}
set elemKinit(10103) 3.773200081582705e-06
set sigmaV0(10103) 111.907500
set ruPrev(10103) 0.0

# Element 10104: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(10104) {1255 1216 206 217 2712 2694 1222 1261}
set elemKinit(10104) 3.773200081582705e-06
set sigmaV0(10104) 158.752500
set ruPrev(10104) 0.0

# Element 10105: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(10105) {2712 2694 1222 1261 1258 1219 207 218}
set elemKinit(10105) 3.773200081582705e-06
set sigmaV0(10105) 158.752500
set ruPrev(10105) 0.0

# Element 10106: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(10106) {1256 1217 1216 1255 2713 2695 2694 2712}
set elemKinit(10106) 3.773200081582705e-06
set sigmaV0(10106) 143.137500
set ruPrev(10106) 0.0

# Element 10107: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(10107) {2713 2695 2694 2712 1259 1220 1219 1258}
set elemKinit(10107) 3.773200081582705e-06
set sigmaV0(10107) 143.137500
set ruPrev(10107) 0.0

# Element 10108: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(10108) {1257 1218 1217 1256 2714 2696 2695 2713}
set elemKinit(10108) 3.773200081582705e-06
set sigmaV0(10108) 127.522500
set ruPrev(10108) 0.0

# Element 10109: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(10109) {2714 2696 2695 2713 1260 1221 1220 1259}
set elemKinit(10109) 3.773200081582705e-06
set sigmaV0(10109) 127.522500
set ruPrev(10109) 0.0

# Element 10110: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(10110) {126 104 1218 1257 933 877 2696 2714}
set elemKinit(10110) 3.773200081582705e-06
set sigmaV0(10110) 111.907500
set ruPrev(10110) 0.0

# Element 10111: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(10111) {933 877 2696 2714 128 106 1221 1260}
set elemKinit(10111) 3.773200081582705e-06
set sigmaV0(10111) 111.907500
set ruPrev(10111) 0.0

# Element 10112: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(10112) {1258 1219 207 218 1262 1223 208 219}
set elemKinit(10112) 3.773200081582705e-06
set sigmaV0(10112) 158.752500
set ruPrev(10112) 0.0

# Element 10113: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(10113) {1259 1220 1219 1258 1263 1224 1223 1262}
set elemKinit(10113) 3.773200081582705e-06
set sigmaV0(10113) 143.137500
set ruPrev(10113) 0.0

# Element 10114: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(10114) {1260 1221 1220 1259 1264 1225 1224 1263}
set elemKinit(10114) 3.773200081582705e-06
set sigmaV0(10114) 127.522500
set ruPrev(10114) 0.0

# Element 10115: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(10115) {128 106 1221 1260 130 108 1225 1264}
set elemKinit(10115) 3.773200081582705e-06
set sigmaV0(10115) 111.907500
set ruPrev(10115) 0.0

# Element 10116: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(10116) {1262 1223 208 219 2715 2697 1229 1268}
set elemKinit(10116) 3.773200081582705e-06
set sigmaV0(10116) 158.752500
set ruPrev(10116) 0.0

# Element 10117: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(10117) {2715 2697 1229 1268 2718 2700 1230 1269}
set elemKinit(10117) 3.773200081582705e-06
set sigmaV0(10117) 158.752500
set ruPrev(10117) 0.0

# Element 10118: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(10118) {2718 2700 1230 1269 1265 1226 209 220}
set elemKinit(10118) 3.773200081582705e-06
set sigmaV0(10118) 158.752500
set ruPrev(10118) 0.0

# Element 10119: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(10119) {1263 1224 1223 1262 2716 2698 2697 2715}
set elemKinit(10119) 3.773200081582705e-06
set sigmaV0(10119) 143.137500
set ruPrev(10119) 0.0

# Element 10120: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(10120) {2716 2698 2697 2715 2719 2701 2700 2718}
set elemKinit(10120) 3.773200081582705e-06
set sigmaV0(10120) 143.137500
set ruPrev(10120) 0.0

# Element 10121: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(10121) {2719 2701 2700 2718 1266 1227 1226 1265}
set elemKinit(10121) 3.773200081582705e-06
set sigmaV0(10121) 143.137500
set ruPrev(10121) 0.0

# Element 10122: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(10122) {1264 1225 1224 1263 2717 2699 2698 2716}
set elemKinit(10122) 3.773200081582705e-06
set sigmaV0(10122) 127.522500
set ruPrev(10122) 0.0

# Element 10123: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(10123) {2717 2699 2698 2716 2720 2702 2701 2719}
set elemKinit(10123) 3.773200081582705e-06
set sigmaV0(10123) 127.522500
set ruPrev(10123) 0.0

# Element 10124: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(10124) {2720 2702 2701 2719 1267 1228 1227 1266}
set elemKinit(10124) 3.773200081582705e-06
set sigmaV0(10124) 127.522500
set ruPrev(10124) 0.0

# Element 10125: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(10125) {130 108 1225 1264 943 887 2699 2717}
set elemKinit(10125) 3.773200081582705e-06
set sigmaV0(10125) 111.907500
set ruPrev(10125) 0.0

# Element 10126: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(10126) {943 887 2699 2717 944 888 2702 2720}
set elemKinit(10126) 3.773200081582705e-06
set sigmaV0(10126) 111.907500
set ruPrev(10126) 0.0

# Element 10127: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(10127) {944 888 2702 2720 132 110 1228 1267}
set elemKinit(10127) 3.773200081582705e-06
set sigmaV0(10127) 111.907500
set ruPrev(10127) 0.0

# Element 10128: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(10128) {2721 1231 210 1273 3300 2703 1237 2733}
set elemKinit(10128) 3.773200081582705e-06
set sigmaV0(10128) 158.752500
set ruPrev(10128) 0.0

# Element 10129: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(10129) {3300 2703 1237 2733 3301 2706 1238 2734}
set elemKinit(10129) 3.773200081582705e-06
set sigmaV0(10129) 158.752500
set ruPrev(10129) 0.0

# Element 10130: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(10130) {3301 2706 1238 2734 2724 1234 211 1277}
set elemKinit(10130) 3.773200081582705e-06
set sigmaV0(10130) 158.752500
set ruPrev(10130) 0.0

# Element 10131: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(10131) {1270 2721 1273 221 2727 3300 2733 1278}
set elemKinit(10131) 3.773200081582705e-06
set sigmaV0(10131) 158.752500
set ruPrev(10131) 0.0

# Element 10132: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(10132) {2727 3300 2733 1278 2730 3301 2734 1279}
set elemKinit(10132) 3.773200081582705e-06
set sigmaV0(10132) 158.752500
set ruPrev(10132) 0.0

# Element 10133: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(10133) {2730 3301 2734 1279 1274 2724 1277 222}
set elemKinit(10133) 3.773200081582705e-06
set sigmaV0(10133) 158.752500
set ruPrev(10133) 0.0

# Element 10134: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(10134) {2722 1232 1231 2721 3302 2704 2703 3300}
set elemKinit(10134) 3.773200081582705e-06
set sigmaV0(10134) 143.137500
set ruPrev(10134) 0.0

# Element 10135: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(10135) {3302 2704 2703 3300 3303 2707 2706 3301}
set elemKinit(10135) 3.773200081582705e-06
set sigmaV0(10135) 143.137500
set ruPrev(10135) 0.0

# Element 10136: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(10136) {3303 2707 2706 3301 2725 1235 1234 2724}
set elemKinit(10136) 3.773200081582705e-06
set sigmaV0(10136) 143.137500
set ruPrev(10136) 0.0

# Element 10137: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(10137) {1271 2722 2721 1270 2728 3302 3300 2727}
set elemKinit(10137) 3.773200081582705e-06
set sigmaV0(10137) 143.137500
set ruPrev(10137) 0.0

# Element 10138: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(10138) {2728 3302 3300 2727 2731 3303 3301 2730}
set elemKinit(10138) 3.773200081582705e-06
set sigmaV0(10138) 143.137500
set ruPrev(10138) 0.0

# Element 10139: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(10139) {2731 3303 3301 2730 1275 2725 2724 1274}
set elemKinit(10139) 3.773200081582705e-06
set sigmaV0(10139) 143.137500
set ruPrev(10139) 0.0

# Element 10140: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(10140) {2723 1233 1232 2722 3304 2705 2704 3302}
set elemKinit(10140) 3.773200081582705e-06
set sigmaV0(10140) 127.522500
set ruPrev(10140) 0.0

# Element 10141: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(10141) {3304 2705 2704 3302 3305 2708 2707 3303}
set elemKinit(10141) 3.773200081582705e-06
set sigmaV0(10141) 127.522500
set ruPrev(10141) 0.0

# Element 10142: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(10142) {3305 2708 2707 3303 2726 1236 1235 2725}
set elemKinit(10142) 3.773200081582705e-06
set sigmaV0(10142) 127.522500
set ruPrev(10142) 0.0

# Element 10143: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(10143) {1272 2723 2722 1271 2729 3304 3302 2728}
set elemKinit(10143) 3.773200081582705e-06
set sigmaV0(10143) 127.522500
set ruPrev(10143) 0.0

# Element 10144: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(10144) {2729 3304 3302 2728 2732 3305 3303 2731}
set elemKinit(10144) 3.773200081582705e-06
set sigmaV0(10144) 127.522500
set ruPrev(10144) 0.0

# Element 10145: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(10145) {2732 3305 3303 2731 1276 2726 2725 1275}
set elemKinit(10145) 3.773200081582705e-06
set sigmaV0(10145) 127.522500
set ruPrev(10145) 0.0

# Element 10146: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(10146) {952 112 1233 2723 2510 899 2705 3304}
set elemKinit(10146) 3.773200081582705e-06
set sigmaV0(10146) 111.907500
set ruPrev(10146) 0.0

# Element 10147: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(10147) {2510 899 2705 3304 2511 900 2708 3305}
set elemKinit(10147) 3.773200081582705e-06
set sigmaV0(10147) 111.907500
set ruPrev(10147) 0.0

# Element 10148: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(10148) {2511 900 2708 3305 958 114 1236 2726}
set elemKinit(10148) 3.773200081582705e-06
set sigmaV0(10148) 111.907500
set ruPrev(10148) 0.0

# Element 10149: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(10149) {134 952 2723 1272 959 2510 3304 2729}
set elemKinit(10149) 3.773200081582705e-06
set sigmaV0(10149) 111.907500
set ruPrev(10149) 0.0

# Element 10150: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(10150) {959 2510 3304 2729 960 2511 3305 2732}
set elemKinit(10150) 3.773200081582705e-06
set sigmaV0(10150) 111.907500
set ruPrev(10150) 0.0

# Element 10151: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(10151) {960 2511 3305 2732 136 958 2726 1276}
set elemKinit(10151) 3.773200081582705e-06
set sigmaV0(10151) 111.907500
set ruPrev(10151) 0.0

# Element 10152: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(10152) {2724 1234 211 1277 2735 1239 212 1283}
set elemKinit(10152) 3.773200081582705e-06
set sigmaV0(10152) 158.752500
set ruPrev(10152) 0.0

# Element 10153: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(10153) {1274 2724 1277 222 1280 2735 1283 223}
set elemKinit(10153) 3.773200081582705e-06
set sigmaV0(10153) 158.752500
set ruPrev(10153) 0.0

# Element 10154: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(10154) {2725 1235 1234 2724 2736 1240 1239 2735}
set elemKinit(10154) 3.773200081582705e-06
set sigmaV0(10154) 143.137500
set ruPrev(10154) 0.0

# Element 10155: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(10155) {1275 2725 2724 1274 1281 2736 2735 1280}
set elemKinit(10155) 3.773200081582705e-06
set sigmaV0(10155) 143.137500
set ruPrev(10155) 0.0

# Element 10156: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(10156) {2726 1236 1235 2725 2737 1241 1240 2736}
set elemKinit(10156) 3.773200081582705e-06
set sigmaV0(10156) 127.522500
set ruPrev(10156) 0.0

# Element 10157: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(10157) {1276 2726 2725 1275 1282 2737 2736 1281}
set elemKinit(10157) 3.773200081582705e-06
set sigmaV0(10157) 127.522500
set ruPrev(10157) 0.0

# Element 10158: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(10158) {958 114 1236 2726 968 116 1241 2737}
set elemKinit(10158) 3.773200081582705e-06
set sigmaV0(10158) 111.907500
set ruPrev(10158) 0.0

# Element 10159: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(10159) {136 958 2726 1276 138 968 2737 1282}
set elemKinit(10159) 3.773200081582705e-06
set sigmaV0(10159) 111.907500
set ruPrev(10159) 0.0

# Element 10160: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(10160) {2735 1239 212 1283 3306 2709 1245 2744}
set elemKinit(10160) 3.773200081582705e-06
set sigmaV0(10160) 158.752500
set ruPrev(10160) 0.0

# Element 10161: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(10161) {3306 2709 1245 2744 2738 1242 213 1287}
set elemKinit(10161) 3.773200081582705e-06
set sigmaV0(10161) 158.752500
set ruPrev(10161) 0.0

# Element 10162: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(10162) {1280 2735 1283 223 2741 3306 2744 1288}
set elemKinit(10162) 3.773200081582705e-06
set sigmaV0(10162) 158.752500
set ruPrev(10162) 0.0

# Element 10163: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(10163) {2741 3306 2744 1288 1284 2738 1287 224}
set elemKinit(10163) 3.773200081582705e-06
set sigmaV0(10163) 158.752500
set ruPrev(10163) 0.0

# Element 10164: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(10164) {2736 1240 1239 2735 3307 2710 2709 3306}
set elemKinit(10164) 3.773200081582705e-06
set sigmaV0(10164) 143.137500
set ruPrev(10164) 0.0

# Element 10165: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(10165) {3307 2710 2709 3306 2739 1243 1242 2738}
set elemKinit(10165) 3.773200081582705e-06
set sigmaV0(10165) 143.137500
set ruPrev(10165) 0.0

# Element 10166: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(10166) {1281 2736 2735 1280 2742 3307 3306 2741}
set elemKinit(10166) 3.773200081582705e-06
set sigmaV0(10166) 143.137500
set ruPrev(10166) 0.0

# Element 10167: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(10167) {2742 3307 3306 2741 1285 2739 2738 1284}
set elemKinit(10167) 3.773200081582705e-06
set sigmaV0(10167) 143.137500
set ruPrev(10167) 0.0

# Element 10168: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(10168) {2737 1241 1240 2736 3308 2711 2710 3307}
set elemKinit(10168) 3.773200081582705e-06
set sigmaV0(10168) 127.522500
set ruPrev(10168) 0.0

# Element 10169: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(10169) {3308 2711 2710 3307 2740 1244 1243 2739}
set elemKinit(10169) 3.773200081582705e-06
set sigmaV0(10169) 127.522500
set ruPrev(10169) 0.0

# Element 10170: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(10170) {1282 2737 2736 1281 2743 3308 3307 2742}
set elemKinit(10170) 3.773200081582705e-06
set sigmaV0(10170) 127.522500
set ruPrev(10170) 0.0

# Element 10171: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(10171) {2743 3308 3307 2742 1286 2740 2739 1285}
set elemKinit(10171) 3.773200081582705e-06
set sigmaV0(10171) 127.522500
set ruPrev(10171) 0.0

# Element 10172: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(10172) {968 116 1241 2737 2526 911 2711 3308}
set elemKinit(10172) 3.773200081582705e-06
set sigmaV0(10172) 111.907500
set ruPrev(10172) 0.0

# Element 10173: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(10173) {2526 911 2711 3308 974 118 1244 2740}
set elemKinit(10173) 3.773200081582705e-06
set sigmaV0(10173) 111.907500
set ruPrev(10173) 0.0

# Element 10174: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(10174) {138 968 2737 1282 975 2526 3308 2743}
set elemKinit(10174) 3.773200081582705e-06
set sigmaV0(10174) 111.907500
set ruPrev(10174) 0.0

# Element 10175: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(10175) {975 2526 3308 2743 140 974 2740 1286}
set elemKinit(10175) 3.773200081582705e-06
set sigmaV0(10175) 111.907500
set ruPrev(10175) 0.0

# Element 10176: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(10176) {2738 1242 213 1287 2745 1246 214 1292}
set elemKinit(10176) 3.773200081582705e-06
set sigmaV0(10176) 158.752500
set ruPrev(10176) 0.0

# Element 10177: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(10177) {1284 2738 1287 224 1289 2745 1292 225}
set elemKinit(10177) 3.773200081582705e-06
set sigmaV0(10177) 158.752500
set ruPrev(10177) 0.0

# Element 10178: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(10178) {2739 1243 1242 2738 2746 1247 1246 2745}
set elemKinit(10178) 3.773200081582705e-06
set sigmaV0(10178) 143.137500
set ruPrev(10178) 0.0

# Element 10179: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(10179) {1285 2739 2738 1284 1290 2746 2745 1289}
set elemKinit(10179) 3.773200081582705e-06
set sigmaV0(10179) 143.137500
set ruPrev(10179) 0.0

# Element 10180: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(10180) {2740 1244 1243 2739 2747 1248 1247 2746}
set elemKinit(10180) 3.773200081582705e-06
set sigmaV0(10180) 127.522500
set ruPrev(10180) 0.0

# Element 10181: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(10181) {1286 2740 2739 1285 1291 2747 2746 1290}
set elemKinit(10181) 3.773200081582705e-06
set sigmaV0(10181) 127.522500
set ruPrev(10181) 0.0

# Element 10182: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(10182) {974 118 1244 2740 982 120 1248 2747}
set elemKinit(10182) 3.773200081582705e-06
set sigmaV0(10182) 111.907500
set ruPrev(10182) 0.0

# Element 10183: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(10183) {140 974 2740 1286 142 982 2747 1291}
set elemKinit(10183) 3.773200081582705e-06
set sigmaV0(10183) 111.907500
set ruPrev(10183) 0.0

# Element 10184: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(10184) {2745 1246 214 1292 2748 1249 215 1296}
set elemKinit(10184) 3.773200081582705e-06
set sigmaV0(10184) 158.752500
set ruPrev(10184) 0.0

# Element 10185: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(10185) {1289 2745 1292 225 1293 2748 1296 226}
set elemKinit(10185) 3.773200081582705e-06
set sigmaV0(10185) 158.752500
set ruPrev(10185) 0.0

# Element 10186: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(10186) {2746 1247 1246 2745 2749 1250 1249 2748}
set elemKinit(10186) 3.773200081582705e-06
set sigmaV0(10186) 143.137500
set ruPrev(10186) 0.0

# Element 10187: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(10187) {1290 2746 2745 1289 1294 2749 2748 1293}
set elemKinit(10187) 3.773200081582705e-06
set sigmaV0(10187) 143.137500
set ruPrev(10187) 0.0

# Element 10188: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(10188) {2747 1248 1247 2746 2750 1251 1250 2749}
set elemKinit(10188) 3.773200081582705e-06
set sigmaV0(10188) 127.522500
set ruPrev(10188) 0.0

# Element 10189: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(10189) {1291 2747 2746 1290 1295 2750 2749 1294}
set elemKinit(10189) 3.773200081582705e-06
set sigmaV0(10189) 127.522500
set ruPrev(10189) 0.0

# Element 10190: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(10190) {982 120 1248 2747 988 122 1251 2750}
set elemKinit(10190) 3.773200081582705e-06
set sigmaV0(10190) 111.907500
set ruPrev(10190) 0.0

# Element 10191: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(10191) {142 982 2747 1291 144 988 2750 1295}
set elemKinit(10191) 3.773200081582705e-06
set sigmaV0(10191) 111.907500
set ruPrev(10191) 0.0

# Element 10192: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(10192) {2748 1249 215 1296 2751 1252 216 1300}
set elemKinit(10192) 3.773200081582705e-06
set sigmaV0(10192) 158.752500
set ruPrev(10192) 0.0

# Element 10193: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(10193) {1293 2748 1296 226 1297 2751 1300 227}
set elemKinit(10193) 3.773200081582705e-06
set sigmaV0(10193) 158.752500
set ruPrev(10193) 0.0

# Element 10194: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(10194) {2749 1250 1249 2748 2752 1253 1252 2751}
set elemKinit(10194) 3.773200081582705e-06
set sigmaV0(10194) 143.137500
set ruPrev(10194) 0.0

# Element 10195: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(10195) {1294 2749 2748 1293 1298 2752 2751 1297}
set elemKinit(10195) 3.773200081582705e-06
set sigmaV0(10195) 143.137500
set ruPrev(10195) 0.0

# Element 10196: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(10196) {2750 1251 1250 2749 2753 1254 1253 2752}
set elemKinit(10196) 3.773200081582705e-06
set sigmaV0(10196) 127.522500
set ruPrev(10196) 0.0

# Element 10197: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(10197) {1295 2750 2749 1294 1299 2753 2752 1298}
set elemKinit(10197) 3.773200081582705e-06
set sigmaV0(10197) 127.522500
set ruPrev(10197) 0.0

# Element 10198: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(10198) {988 122 1251 2750 994 124 1254 2753}
set elemKinit(10198) 3.773200081582705e-06
set sigmaV0(10198) 111.907500
set ruPrev(10198) 0.0

# Element 10199: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(10199) {144 988 2750 1295 146 994 2753 1299}
set elemKinit(10199) 3.773200081582705e-06
set sigmaV0(10199) 111.907500
set ruPrev(10199) 0.0

# Element 10200: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(10200) {2751 1252 216 1300 2754 1255 217 1304}
set elemKinit(10200) 3.773200081582705e-06
set sigmaV0(10200) 158.752500
set ruPrev(10200) 0.0

# Element 10201: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(10201) {1297 2751 1300 227 1301 2754 1304 228}
set elemKinit(10201) 3.773200081582705e-06
set sigmaV0(10201) 158.752500
set ruPrev(10201) 0.0

# Element 10202: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(10202) {2752 1253 1252 2751 2755 1256 1255 2754}
set elemKinit(10202) 3.773200081582705e-06
set sigmaV0(10202) 143.137500
set ruPrev(10202) 0.0

# Element 10203: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(10203) {1298 2752 2751 1297 1302 2755 2754 1301}
set elemKinit(10203) 3.773200081582705e-06
set sigmaV0(10203) 143.137500
set ruPrev(10203) 0.0

# Element 10204: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(10204) {2753 1254 1253 2752 2756 1257 1256 2755}
set elemKinit(10204) 3.773200081582705e-06
set sigmaV0(10204) 127.522500
set ruPrev(10204) 0.0

# Element 10205: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(10205) {1299 2753 2752 1298 1303 2756 2755 1302}
set elemKinit(10205) 3.773200081582705e-06
set sigmaV0(10205) 127.522500
set ruPrev(10205) 0.0

# Element 10206: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(10206) {994 124 1254 2753 1000 126 1257 2756}
set elemKinit(10206) 3.773200081582705e-06
set sigmaV0(10206) 111.907500
set ruPrev(10206) 0.0

# Element 10207: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(10207) {146 994 2753 1299 148 1000 2756 1303}
set elemKinit(10207) 3.773200081582705e-06
set sigmaV0(10207) 111.907500
set ruPrev(10207) 0.0

# Element 10208: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(10208) {2754 1255 217 1304 3309 2712 1261 2763}
set elemKinit(10208) 3.773200081582705e-06
set sigmaV0(10208) 158.752500
set ruPrev(10208) 0.0

# Element 10209: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(10209) {3309 2712 1261 2763 2757 1258 218 1308}
set elemKinit(10209) 3.773200081582705e-06
set sigmaV0(10209) 158.752500
set ruPrev(10209) 0.0

# Element 10210: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(10210) {1301 2754 1304 228 2760 3309 2763 1309}
set elemKinit(10210) 3.773200081582705e-06
set sigmaV0(10210) 158.752500
set ruPrev(10210) 0.0

# Element 10211: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(10211) {2760 3309 2763 1309 1305 2757 1308 229}
set elemKinit(10211) 3.773200081582705e-06
set sigmaV0(10211) 158.752500
set ruPrev(10211) 0.0

# Element 10212: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(10212) {2755 1256 1255 2754 3310 2713 2712 3309}
set elemKinit(10212) 3.773200081582705e-06
set sigmaV0(10212) 143.137500
set ruPrev(10212) 0.0

# Element 10213: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(10213) {3310 2713 2712 3309 2758 1259 1258 2757}
set elemKinit(10213) 3.773200081582705e-06
set sigmaV0(10213) 143.137500
set ruPrev(10213) 0.0

# Element 10214: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(10214) {1302 2755 2754 1301 2761 3310 3309 2760}
set elemKinit(10214) 3.773200081582705e-06
set sigmaV0(10214) 143.137500
set ruPrev(10214) 0.0

# Element 10215: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(10215) {2761 3310 3309 2760 1306 2758 2757 1305}
set elemKinit(10215) 3.773200081582705e-06
set sigmaV0(10215) 143.137500
set ruPrev(10215) 0.0

# Element 10216: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(10216) {2756 1257 1256 2755 3311 2714 2713 3310}
set elemKinit(10216) 3.773200081582705e-06
set sigmaV0(10216) 127.522500
set ruPrev(10216) 0.0

# Element 10217: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(10217) {3311 2714 2713 3310 2759 1260 1259 2758}
set elemKinit(10217) 3.773200081582705e-06
set sigmaV0(10217) 127.522500
set ruPrev(10217) 0.0

# Element 10218: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(10218) {1303 2756 2755 1302 2762 3311 3310 2761}
set elemKinit(10218) 3.773200081582705e-06
set sigmaV0(10218) 127.522500
set ruPrev(10218) 0.0

# Element 10219: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(10219) {2762 3311 3310 2761 1307 2759 2758 1306}
set elemKinit(10219) 3.773200081582705e-06
set sigmaV0(10219) 127.522500
set ruPrev(10219) 0.0

# Element 10220: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(10220) {1000 126 1257 2756 2552 933 2714 3311}
set elemKinit(10220) 3.773200081582705e-06
set sigmaV0(10220) 111.907500
set ruPrev(10220) 0.0

# Element 10221: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(10221) {2552 933 2714 3311 1006 128 1260 2759}
set elemKinit(10221) 3.773200081582705e-06
set sigmaV0(10221) 111.907500
set ruPrev(10221) 0.0

# Element 10222: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(10222) {148 1000 2756 1303 1007 2552 3311 2762}
set elemKinit(10222) 3.773200081582705e-06
set sigmaV0(10222) 111.907500
set ruPrev(10222) 0.0

# Element 10223: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(10223) {1007 2552 3311 2762 150 1006 2759 1307}
set elemKinit(10223) 3.773200081582705e-06
set sigmaV0(10223) 111.907500
set ruPrev(10223) 0.0

# Element 10224: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(10224) {2757 1258 218 1308 2764 1262 219 1313}
set elemKinit(10224) 3.773200081582705e-06
set sigmaV0(10224) 158.752500
set ruPrev(10224) 0.0

# Element 10225: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(10225) {1305 2757 1308 229 1310 2764 1313 230}
set elemKinit(10225) 3.773200081582705e-06
set sigmaV0(10225) 158.752500
set ruPrev(10225) 0.0

# Element 10226: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(10226) {2758 1259 1258 2757 2765 1263 1262 2764}
set elemKinit(10226) 3.773200081582705e-06
set sigmaV0(10226) 143.137500
set ruPrev(10226) 0.0

# Element 10227: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(10227) {1306 2758 2757 1305 1311 2765 2764 1310}
set elemKinit(10227) 3.773200081582705e-06
set sigmaV0(10227) 143.137500
set ruPrev(10227) 0.0

# Element 10228: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(10228) {2759 1260 1259 2758 2766 1264 1263 2765}
set elemKinit(10228) 3.773200081582705e-06
set sigmaV0(10228) 127.522500
set ruPrev(10228) 0.0

# Element 10229: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(10229) {1307 2759 2758 1306 1312 2766 2765 1311}
set elemKinit(10229) 3.773200081582705e-06
set sigmaV0(10229) 127.522500
set ruPrev(10229) 0.0

# Element 10230: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(10230) {1006 128 1260 2759 1014 130 1264 2766}
set elemKinit(10230) 3.773200081582705e-06
set sigmaV0(10230) 111.907500
set ruPrev(10230) 0.0

# Element 10231: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(10231) {150 1006 2759 1307 152 1014 2766 1312}
set elemKinit(10231) 3.773200081582705e-06
set sigmaV0(10231) 111.907500
set ruPrev(10231) 0.0

# Element 10232: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(10232) {2764 1262 219 1313 3312 2715 1268 2776}
set elemKinit(10232) 3.773200081582705e-06
set sigmaV0(10232) 158.752500
set ruPrev(10232) 0.0

# Element 10233: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(10233) {3312 2715 1268 2776 3313 2718 1269 2777}
set elemKinit(10233) 3.773200081582705e-06
set sigmaV0(10233) 158.752500
set ruPrev(10233) 0.0

# Element 10234: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(10234) {3313 2718 1269 2777 2767 1265 220 1317}
set elemKinit(10234) 3.773200081582705e-06
set sigmaV0(10234) 158.752500
set ruPrev(10234) 0.0

# Element 10235: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(10235) {1310 2764 1313 230 2770 3312 2776 1318}
set elemKinit(10235) 3.773200081582705e-06
set sigmaV0(10235) 158.752500
set ruPrev(10235) 0.0

# Element 10236: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(10236) {2770 3312 2776 1318 2773 3313 2777 1319}
set elemKinit(10236) 3.773200081582705e-06
set sigmaV0(10236) 158.752500
set ruPrev(10236) 0.0

# Element 10237: depth=15.25m, sigma_v0=158.75kPa, mat=2
set elemNodes(10237) {2773 3313 2777 1319 1314 2767 1317 231}
set elemKinit(10237) 3.773200081582705e-06
set sigmaV0(10237) 158.752500
set ruPrev(10237) 0.0

# Element 10238: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(10238) {2765 1263 1262 2764 3314 2716 2715 3312}
set elemKinit(10238) 3.773200081582705e-06
set sigmaV0(10238) 143.137500
set ruPrev(10238) 0.0

# Element 10239: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(10239) {3314 2716 2715 3312 3315 2719 2718 3313}
set elemKinit(10239) 3.773200081582705e-06
set sigmaV0(10239) 143.137500
set ruPrev(10239) 0.0

# Element 10240: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(10240) {3315 2719 2718 3313 2768 1266 1265 2767}
set elemKinit(10240) 3.773200081582705e-06
set sigmaV0(10240) 143.137500
set ruPrev(10240) 0.0

# Element 10241: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(10241) {1311 2765 2764 1310 2771 3314 3312 2770}
set elemKinit(10241) 3.773200081582705e-06
set sigmaV0(10241) 143.137500
set ruPrev(10241) 0.0

# Element 10242: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(10242) {2771 3314 3312 2770 2774 3315 3313 2773}
set elemKinit(10242) 3.773200081582705e-06
set sigmaV0(10242) 143.137500
set ruPrev(10242) 0.0

# Element 10243: depth=13.75m, sigma_v0=143.14kPa, mat=2
set elemNodes(10243) {2774 3315 3313 2773 1315 2768 2767 1314}
set elemKinit(10243) 3.773200081582705e-06
set sigmaV0(10243) 143.137500
set ruPrev(10243) 0.0

# Element 10244: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(10244) {2766 1264 1263 2765 3316 2717 2716 3314}
set elemKinit(10244) 3.773200081582705e-06
set sigmaV0(10244) 127.522500
set ruPrev(10244) 0.0

# Element 10245: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(10245) {3316 2717 2716 3314 3317 2720 2719 3315}
set elemKinit(10245) 3.773200081582705e-06
set sigmaV0(10245) 127.522500
set ruPrev(10245) 0.0

# Element 10246: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(10246) {3317 2720 2719 3315 2769 1267 1266 2768}
set elemKinit(10246) 3.773200081582705e-06
set sigmaV0(10246) 127.522500
set ruPrev(10246) 0.0

# Element 10247: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(10247) {1312 2766 2765 1311 2772 3316 3314 2771}
set elemKinit(10247) 3.773200081582705e-06
set sigmaV0(10247) 127.522500
set ruPrev(10247) 0.0

# Element 10248: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(10248) {2772 3316 3314 2771 2775 3317 3315 2774}
set elemKinit(10248) 3.773200081582705e-06
set sigmaV0(10248) 127.522500
set ruPrev(10248) 0.0

# Element 10249: depth=12.25m, sigma_v0=127.52kPa, mat=2
set elemNodes(10249) {2775 3317 3315 2774 1316 2769 2768 1315}
set elemKinit(10249) 3.773200081582705e-06
set sigmaV0(10249) 127.522500
set ruPrev(10249) 0.0

# Element 10250: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(10250) {1014 130 1264 2766 2570 943 2717 3316}
set elemKinit(10250) 3.773200081582705e-06
set sigmaV0(10250) 111.907500
set ruPrev(10250) 0.0

# Element 10251: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(10251) {2570 943 2717 3316 2571 944 2720 3317}
set elemKinit(10251) 3.773200081582705e-06
set sigmaV0(10251) 111.907500
set ruPrev(10251) 0.0

# Element 10252: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(10252) {2571 944 2720 3317 1020 132 1267 2769}
set elemKinit(10252) 3.773200081582705e-06
set sigmaV0(10252) 111.907500
set ruPrev(10252) 0.0

# Element 10253: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(10253) {152 1014 2766 1312 1021 2570 3316 2772}
set elemKinit(10253) 3.773200081582705e-06
set sigmaV0(10253) 111.907500
set ruPrev(10253) 0.0

# Element 10254: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(10254) {1021 2570 3316 2772 1022 2571 3317 2775}
set elemKinit(10254) 3.773200081582705e-06
set sigmaV0(10254) 111.907500
set ruPrev(10254) 0.0

# Element 10255: depth=10.75m, sigma_v0=111.91kPa, mat=2
set elemNodes(10255) {1022 2571 3317 2775 154 1020 2769 1316}
set elemKinit(10255) 3.773200081582705e-06
set sigmaV0(10255) 111.907500
set ruPrev(10255) 0.0

# Element 10256: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10256) {2778 1320 232 1328 3318 2786 1338 2802}
set elemKinit(10256) 3.773200081582705e-06
set sigmaV0(10256) 213.405000
set ruPrev(10256) 0.0

# Element 10257: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10257) {3318 2786 1338 2802 3319 2790 1339 2803}
set elemKinit(10257) 3.773200081582705e-06
set sigmaV0(10257) 213.405000
set ruPrev(10257) 0.0

# Element 10258: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10258) {3319 2790 1339 2803 2782 1329 234 1337}
set elemKinit(10258) 3.773200081582705e-06
set sigmaV0(10258) 213.405000
set ruPrev(10258) 0.0

# Element 10259: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10259) {1324 2778 1328 233 2794 3318 2802 1340}
set elemKinit(10259) 3.773200081582705e-06
set sigmaV0(10259) 213.405000
set ruPrev(10259) 0.0

# Element 10260: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10260) {2794 3318 2802 1340 2798 3319 2803 1341}
set elemKinit(10260) 3.773200081582705e-06
set sigmaV0(10260) 213.405000
set ruPrev(10260) 0.0

# Element 10261: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10261) {2798 3319 2803 1341 1333 2782 1337 235}
set elemKinit(10261) 3.773200081582705e-06
set sigmaV0(10261) 213.405000
set ruPrev(10261) 0.0

# Element 10262: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10262) {2779 1321 1320 2778 3320 2787 2786 3318}
set elemKinit(10262) 3.773200081582705e-06
set sigmaV0(10262) 202.995000
set ruPrev(10262) 0.0

# Element 10263: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10263) {3320 2787 2786 3318 3321 2791 2790 3319}
set elemKinit(10263) 3.773200081582705e-06
set sigmaV0(10263) 202.995000
set ruPrev(10263) 0.0

# Element 10264: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10264) {3321 2791 2790 3319 2783 1330 1329 2782}
set elemKinit(10264) 3.773200081582705e-06
set sigmaV0(10264) 202.995000
set ruPrev(10264) 0.0

# Element 10265: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10265) {1325 2779 2778 1324 2795 3320 3318 2794}
set elemKinit(10265) 3.773200081582705e-06
set sigmaV0(10265) 202.995000
set ruPrev(10265) 0.0

# Element 10266: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10266) {2795 3320 3318 2794 2799 3321 3319 2798}
set elemKinit(10266) 3.773200081582705e-06
set sigmaV0(10266) 202.995000
set ruPrev(10266) 0.0

# Element 10267: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10267) {2799 3321 3319 2798 1334 2783 2782 1333}
set elemKinit(10267) 3.773200081582705e-06
set sigmaV0(10267) 202.995000
set ruPrev(10267) 0.0

# Element 10268: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10268) {2780 1322 1321 2779 3322 2788 2787 3320}
set elemKinit(10268) 3.773200081582705e-06
set sigmaV0(10268) 192.585000
set ruPrev(10268) 0.0

# Element 10269: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10269) {3322 2788 2787 3320 3323 2792 2791 3321}
set elemKinit(10269) 3.773200081582705e-06
set sigmaV0(10269) 192.585000
set ruPrev(10269) 0.0

# Element 10270: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10270) {3323 2792 2791 3321 2784 1331 1330 2783}
set elemKinit(10270) 3.773200081582705e-06
set sigmaV0(10270) 192.585000
set ruPrev(10270) 0.0

# Element 10271: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10271) {1326 2780 2779 1325 2796 3322 3320 2795}
set elemKinit(10271) 3.773200081582705e-06
set sigmaV0(10271) 192.585000
set ruPrev(10271) 0.0

# Element 10272: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10272) {2796 3322 3320 2795 2800 3323 3321 2799}
set elemKinit(10272) 3.773200081582705e-06
set sigmaV0(10272) 192.585000
set ruPrev(10272) 0.0

# Element 10273: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10273) {2800 3323 3321 2799 1335 2784 2783 1334}
set elemKinit(10273) 3.773200081582705e-06
set sigmaV0(10273) 192.585000
set ruPrev(10273) 0.0

# Element 10274: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10274) {2781 1323 1322 2780 3324 2789 2788 3322}
set elemKinit(10274) 3.773200081582705e-06
set sigmaV0(10274) 182.175000
set ruPrev(10274) 0.0

# Element 10275: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10275) {3324 2789 2788 3322 3325 2793 2792 3323}
set elemKinit(10275) 3.773200081582705e-06
set sigmaV0(10275) 182.175000
set ruPrev(10275) 0.0

# Element 10276: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10276) {3325 2793 2792 3323 2785 1332 1331 2784}
set elemKinit(10276) 3.773200081582705e-06
set sigmaV0(10276) 182.175000
set ruPrev(10276) 0.0

# Element 10277: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10277) {1327 2781 2780 1326 2797 3324 3322 2796}
set elemKinit(10277) 3.773200081582705e-06
set sigmaV0(10277) 182.175000
set ruPrev(10277) 0.0

# Element 10278: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10278) {2797 3324 3322 2796 2801 3325 3323 2800}
set elemKinit(10278) 3.773200081582705e-06
set sigmaV0(10278) 182.175000
set ruPrev(10278) 0.0

# Element 10279: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10279) {2801 3325 3323 2800 1336 2785 2784 1335}
set elemKinit(10279) 3.773200081582705e-06
set sigmaV0(10279) 182.175000
set ruPrev(10279) 0.0

# Element 10280: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10280) {1031 155 1323 2781 2592 1039 2789 3324}
set elemKinit(10280) 3.773200081582705e-06
set sigmaV0(10280) 171.765000
set ruPrev(10280) 0.0

# Element 10281: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10281) {2592 1039 2789 3324 2593 1040 2793 3325}
set elemKinit(10281) 3.773200081582705e-06
set sigmaV0(10281) 171.765000
set ruPrev(10281) 0.0

# Element 10282: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10282) {2593 1040 2793 3325 1038 157 1332 2785}
set elemKinit(10282) 3.773200081582705e-06
set sigmaV0(10282) 171.765000
set ruPrev(10282) 0.0

# Element 10283: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10283) {156 1031 2781 1327 1041 2592 3324 2797}
set elemKinit(10283) 3.773200081582705e-06
set sigmaV0(10283) 171.765000
set ruPrev(10283) 0.0

# Element 10284: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10284) {1041 2592 3324 2797 1042 2593 3325 2801}
set elemKinit(10284) 3.773200081582705e-06
set sigmaV0(10284) 171.765000
set ruPrev(10284) 0.0

# Element 10285: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10285) {1042 2593 3325 2801 158 1038 2785 1336}
set elemKinit(10285) 3.773200081582705e-06
set sigmaV0(10285) 171.765000
set ruPrev(10285) 0.0

# Element 10286: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10286) {2782 1329 234 1337 2804 1342 236 1350}
set elemKinit(10286) 3.773200081582705e-06
set sigmaV0(10286) 213.405000
set ruPrev(10286) 0.0

# Element 10287: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10287) {1333 2782 1337 235 1346 2804 1350 237}
set elemKinit(10287) 3.773200081582705e-06
set sigmaV0(10287) 213.405000
set ruPrev(10287) 0.0

# Element 10288: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10288) {2783 1330 1329 2782 2805 1343 1342 2804}
set elemKinit(10288) 3.773200081582705e-06
set sigmaV0(10288) 202.995000
set ruPrev(10288) 0.0

# Element 10289: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10289) {1334 2783 2782 1333 1347 2805 2804 1346}
set elemKinit(10289) 3.773200081582705e-06
set sigmaV0(10289) 202.995000
set ruPrev(10289) 0.0

# Element 10290: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10290) {2784 1331 1330 2783 2806 1344 1343 2805}
set elemKinit(10290) 3.773200081582705e-06
set sigmaV0(10290) 192.585000
set ruPrev(10290) 0.0

# Element 10291: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10291) {1335 2784 2783 1334 1348 2806 2805 1347}
set elemKinit(10291) 3.773200081582705e-06
set sigmaV0(10291) 192.585000
set ruPrev(10291) 0.0

# Element 10292: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10292) {2785 1332 1331 2784 2807 1345 1344 2806}
set elemKinit(10292) 3.773200081582705e-06
set sigmaV0(10292) 182.175000
set ruPrev(10292) 0.0

# Element 10293: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10293) {1336 2785 2784 1335 1349 2807 2806 1348}
set elemKinit(10293) 3.773200081582705e-06
set sigmaV0(10293) 182.175000
set ruPrev(10293) 0.0

# Element 10294: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10294) {1038 157 1332 2785 1049 159 1345 2807}
set elemKinit(10294) 3.773200081582705e-06
set sigmaV0(10294) 171.765000
set ruPrev(10294) 0.0

# Element 10295: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10295) {158 1038 2785 1336 160 1049 2807 1349}
set elemKinit(10295) 3.773200081582705e-06
set sigmaV0(10295) 171.765000
set ruPrev(10295) 0.0

# Element 10296: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10296) {2804 1342 236 1350 3326 2812 1360 2820}
set elemKinit(10296) 3.773200081582705e-06
set sigmaV0(10296) 213.405000
set ruPrev(10296) 0.0

# Element 10297: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10297) {3326 2812 1360 2820 2808 1351 238 1359}
set elemKinit(10297) 3.773200081582705e-06
set sigmaV0(10297) 213.405000
set ruPrev(10297) 0.0

# Element 10298: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10298) {1346 2804 1350 237 2816 3326 2820 1361}
set elemKinit(10298) 3.773200081582705e-06
set sigmaV0(10298) 213.405000
set ruPrev(10298) 0.0

# Element 10299: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10299) {2816 3326 2820 1361 1355 2808 1359 239}
set elemKinit(10299) 3.773200081582705e-06
set sigmaV0(10299) 213.405000
set ruPrev(10299) 0.0

# Element 10300: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10300) {2805 1343 1342 2804 3327 2813 2812 3326}
set elemKinit(10300) 3.773200081582705e-06
set sigmaV0(10300) 202.995000
set ruPrev(10300) 0.0

# Element 10301: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10301) {3327 2813 2812 3326 2809 1352 1351 2808}
set elemKinit(10301) 3.773200081582705e-06
set sigmaV0(10301) 202.995000
set ruPrev(10301) 0.0

# Element 10302: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10302) {1347 2805 2804 1346 2817 3327 3326 2816}
set elemKinit(10302) 3.773200081582705e-06
set sigmaV0(10302) 202.995000
set ruPrev(10302) 0.0

# Element 10303: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10303) {2817 3327 3326 2816 1356 2809 2808 1355}
set elemKinit(10303) 3.773200081582705e-06
set sigmaV0(10303) 202.995000
set ruPrev(10303) 0.0

# Element 10304: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10304) {2806 1344 1343 2805 3328 2814 2813 3327}
set elemKinit(10304) 3.773200081582705e-06
set sigmaV0(10304) 192.585000
set ruPrev(10304) 0.0

# Element 10305: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10305) {3328 2814 2813 3327 2810 1353 1352 2809}
set elemKinit(10305) 3.773200081582705e-06
set sigmaV0(10305) 192.585000
set ruPrev(10305) 0.0

# Element 10306: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10306) {1348 2806 2805 1347 2818 3328 3327 2817}
set elemKinit(10306) 3.773200081582705e-06
set sigmaV0(10306) 192.585000
set ruPrev(10306) 0.0

# Element 10307: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10307) {2818 3328 3327 2817 1357 2810 2809 1356}
set elemKinit(10307) 3.773200081582705e-06
set sigmaV0(10307) 192.585000
set ruPrev(10307) 0.0

# Element 10308: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10308) {2807 1345 1344 2806 3329 2815 2814 3328}
set elemKinit(10308) 3.773200081582705e-06
set sigmaV0(10308) 182.175000
set ruPrev(10308) 0.0

# Element 10309: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10309) {3329 2815 2814 3328 2811 1354 1353 2810}
set elemKinit(10309) 3.773200081582705e-06
set sigmaV0(10309) 182.175000
set ruPrev(10309) 0.0

# Element 10310: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10310) {1349 2807 2806 1348 2819 3329 3328 2818}
set elemKinit(10310) 3.773200081582705e-06
set sigmaV0(10310) 182.175000
set ruPrev(10310) 0.0

# Element 10311: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10311) {2819 3329 3328 2818 1358 2811 2810 1357}
set elemKinit(10311) 3.773200081582705e-06
set sigmaV0(10311) 182.175000
set ruPrev(10311) 0.0

# Element 10312: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10312) {1049 159 1345 2807 2606 1057 2815 3329}
set elemKinit(10312) 3.773200081582705e-06
set sigmaV0(10312) 171.765000
set ruPrev(10312) 0.0

# Element 10313: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10313) {2606 1057 2815 3329 1056 161 1354 2811}
set elemKinit(10313) 3.773200081582705e-06
set sigmaV0(10313) 171.765000
set ruPrev(10313) 0.0

# Element 10314: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10314) {160 1049 2807 1349 1058 2606 3329 2819}
set elemKinit(10314) 3.773200081582705e-06
set sigmaV0(10314) 171.765000
set ruPrev(10314) 0.0

# Element 10315: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10315) {1058 2606 3329 2819 162 1056 2811 1358}
set elemKinit(10315) 3.773200081582705e-06
set sigmaV0(10315) 171.765000
set ruPrev(10315) 0.0

# Element 10316: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10316) {2808 1351 238 1359 2821 1362 240 1370}
set elemKinit(10316) 3.773200081582705e-06
set sigmaV0(10316) 213.405000
set ruPrev(10316) 0.0

# Element 10317: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10317) {1355 2808 1359 239 1366 2821 1370 241}
set elemKinit(10317) 3.773200081582705e-06
set sigmaV0(10317) 213.405000
set ruPrev(10317) 0.0

# Element 10318: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10318) {2809 1352 1351 2808 2822 1363 1362 2821}
set elemKinit(10318) 3.773200081582705e-06
set sigmaV0(10318) 202.995000
set ruPrev(10318) 0.0

# Element 10319: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10319) {1356 2809 2808 1355 1367 2822 2821 1366}
set elemKinit(10319) 3.773200081582705e-06
set sigmaV0(10319) 202.995000
set ruPrev(10319) 0.0

# Element 10320: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10320) {2810 1353 1352 2809 2823 1364 1363 2822}
set elemKinit(10320) 3.773200081582705e-06
set sigmaV0(10320) 192.585000
set ruPrev(10320) 0.0

# Element 10321: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10321) {1357 2810 2809 1356 1368 2823 2822 1367}
set elemKinit(10321) 3.773200081582705e-06
set sigmaV0(10321) 192.585000
set ruPrev(10321) 0.0

# Element 10322: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10322) {2811 1354 1353 2810 2824 1365 1364 2823}
set elemKinit(10322) 3.773200081582705e-06
set sigmaV0(10322) 182.175000
set ruPrev(10322) 0.0

# Element 10323: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10323) {1358 2811 2810 1357 1369 2824 2823 1368}
set elemKinit(10323) 3.773200081582705e-06
set sigmaV0(10323) 182.175000
set ruPrev(10323) 0.0

# Element 10324: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10324) {1056 161 1354 2811 1065 163 1365 2824}
set elemKinit(10324) 3.773200081582705e-06
set sigmaV0(10324) 171.765000
set ruPrev(10324) 0.0

# Element 10325: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10325) {162 1056 2811 1358 164 1065 2824 1369}
set elemKinit(10325) 3.773200081582705e-06
set sigmaV0(10325) 171.765000
set ruPrev(10325) 0.0

# Element 10326: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10326) {2821 1362 240 1370 2825 1371 242 1379}
set elemKinit(10326) 3.773200081582705e-06
set sigmaV0(10326) 213.405000
set ruPrev(10326) 0.0

# Element 10327: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10327) {1366 2821 1370 241 1375 2825 1379 243}
set elemKinit(10327) 3.773200081582705e-06
set sigmaV0(10327) 213.405000
set ruPrev(10327) 0.0

# Element 10328: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10328) {2822 1363 1362 2821 2826 1372 1371 2825}
set elemKinit(10328) 3.773200081582705e-06
set sigmaV0(10328) 202.995000
set ruPrev(10328) 0.0

# Element 10329: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10329) {1367 2822 2821 1366 1376 2826 2825 1375}
set elemKinit(10329) 3.773200081582705e-06
set sigmaV0(10329) 202.995000
set ruPrev(10329) 0.0

# Element 10330: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10330) {2823 1364 1363 2822 2827 1373 1372 2826}
set elemKinit(10330) 3.773200081582705e-06
set sigmaV0(10330) 192.585000
set ruPrev(10330) 0.0

# Element 10331: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10331) {1368 2823 2822 1367 1377 2827 2826 1376}
set elemKinit(10331) 3.773200081582705e-06
set sigmaV0(10331) 192.585000
set ruPrev(10331) 0.0

# Element 10332: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10332) {2824 1365 1364 2823 2828 1374 1373 2827}
set elemKinit(10332) 3.773200081582705e-06
set sigmaV0(10332) 182.175000
set ruPrev(10332) 0.0

# Element 10333: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10333) {1369 2824 2823 1368 1378 2828 2827 1377}
set elemKinit(10333) 3.773200081582705e-06
set sigmaV0(10333) 182.175000
set ruPrev(10333) 0.0

# Element 10334: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10334) {1065 163 1365 2824 1072 165 1374 2828}
set elemKinit(10334) 3.773200081582705e-06
set sigmaV0(10334) 171.765000
set ruPrev(10334) 0.0

# Element 10335: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10335) {164 1065 2824 1369 166 1072 2828 1378}
set elemKinit(10335) 3.773200081582705e-06
set sigmaV0(10335) 171.765000
set ruPrev(10335) 0.0

# Element 10336: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10336) {2825 1371 242 1379 2829 1380 244 1388}
set elemKinit(10336) 3.773200081582705e-06
set sigmaV0(10336) 213.405000
set ruPrev(10336) 0.0

# Element 10337: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10337) {1375 2825 1379 243 1384 2829 1388 245}
set elemKinit(10337) 3.773200081582705e-06
set sigmaV0(10337) 213.405000
set ruPrev(10337) 0.0

# Element 10338: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10338) {2826 1372 1371 2825 2830 1381 1380 2829}
set elemKinit(10338) 3.773200081582705e-06
set sigmaV0(10338) 202.995000
set ruPrev(10338) 0.0

# Element 10339: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10339) {1376 2826 2825 1375 1385 2830 2829 1384}
set elemKinit(10339) 3.773200081582705e-06
set sigmaV0(10339) 202.995000
set ruPrev(10339) 0.0

# Element 10340: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10340) {2827 1373 1372 2826 2831 1382 1381 2830}
set elemKinit(10340) 3.773200081582705e-06
set sigmaV0(10340) 192.585000
set ruPrev(10340) 0.0

# Element 10341: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10341) {1377 2827 2826 1376 1386 2831 2830 1385}
set elemKinit(10341) 3.773200081582705e-06
set sigmaV0(10341) 192.585000
set ruPrev(10341) 0.0

# Element 10342: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10342) {2828 1374 1373 2827 2832 1383 1382 2831}
set elemKinit(10342) 3.773200081582705e-06
set sigmaV0(10342) 182.175000
set ruPrev(10342) 0.0

# Element 10343: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10343) {1378 2828 2827 1377 1387 2832 2831 1386}
set elemKinit(10343) 3.773200081582705e-06
set sigmaV0(10343) 182.175000
set ruPrev(10343) 0.0

# Element 10344: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10344) {1072 165 1374 2828 1079 167 1383 2832}
set elemKinit(10344) 3.773200081582705e-06
set sigmaV0(10344) 171.765000
set ruPrev(10344) 0.0

# Element 10345: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10345) {166 1072 2828 1378 168 1079 2832 1387}
set elemKinit(10345) 3.773200081582705e-06
set sigmaV0(10345) 171.765000
set ruPrev(10345) 0.0

# Element 10346: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10346) {2829 1380 244 1388 2833 1389 246 1397}
set elemKinit(10346) 3.773200081582705e-06
set sigmaV0(10346) 213.405000
set ruPrev(10346) 0.0

# Element 10347: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10347) {1384 2829 1388 245 1393 2833 1397 247}
set elemKinit(10347) 3.773200081582705e-06
set sigmaV0(10347) 213.405000
set ruPrev(10347) 0.0

# Element 10348: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10348) {2830 1381 1380 2829 2834 1390 1389 2833}
set elemKinit(10348) 3.773200081582705e-06
set sigmaV0(10348) 202.995000
set ruPrev(10348) 0.0

# Element 10349: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10349) {1385 2830 2829 1384 1394 2834 2833 1393}
set elemKinit(10349) 3.773200081582705e-06
set sigmaV0(10349) 202.995000
set ruPrev(10349) 0.0

# Element 10350: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10350) {2831 1382 1381 2830 2835 1391 1390 2834}
set elemKinit(10350) 3.773200081582705e-06
set sigmaV0(10350) 192.585000
set ruPrev(10350) 0.0

# Element 10351: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10351) {1386 2831 2830 1385 1395 2835 2834 1394}
set elemKinit(10351) 3.773200081582705e-06
set sigmaV0(10351) 192.585000
set ruPrev(10351) 0.0

# Element 10352: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10352) {2832 1383 1382 2831 2836 1392 1391 2835}
set elemKinit(10352) 3.773200081582705e-06
set sigmaV0(10352) 182.175000
set ruPrev(10352) 0.0

# Element 10353: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10353) {1387 2832 2831 1386 1396 2836 2835 1395}
set elemKinit(10353) 3.773200081582705e-06
set sigmaV0(10353) 182.175000
set ruPrev(10353) 0.0

# Element 10354: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10354) {1079 167 1383 2832 1086 169 1392 2836}
set elemKinit(10354) 3.773200081582705e-06
set sigmaV0(10354) 171.765000
set ruPrev(10354) 0.0

# Element 10355: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10355) {168 1079 2832 1387 170 1086 2836 1396}
set elemKinit(10355) 3.773200081582705e-06
set sigmaV0(10355) 171.765000
set ruPrev(10355) 0.0

# Element 10356: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10356) {2833 1389 246 1397 3330 2841 1407 2849}
set elemKinit(10356) 3.773200081582705e-06
set sigmaV0(10356) 213.405000
set ruPrev(10356) 0.0

# Element 10357: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10357) {3330 2841 1407 2849 2837 1398 248 1406}
set elemKinit(10357) 3.773200081582705e-06
set sigmaV0(10357) 213.405000
set ruPrev(10357) 0.0

# Element 10358: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10358) {1393 2833 1397 247 2845 3330 2849 1408}
set elemKinit(10358) 3.773200081582705e-06
set sigmaV0(10358) 213.405000
set ruPrev(10358) 0.0

# Element 10359: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10359) {2845 3330 2849 1408 1402 2837 1406 249}
set elemKinit(10359) 3.773200081582705e-06
set sigmaV0(10359) 213.405000
set ruPrev(10359) 0.0

# Element 10360: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10360) {2834 1390 1389 2833 3331 2842 2841 3330}
set elemKinit(10360) 3.773200081582705e-06
set sigmaV0(10360) 202.995000
set ruPrev(10360) 0.0

# Element 10361: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10361) {3331 2842 2841 3330 2838 1399 1398 2837}
set elemKinit(10361) 3.773200081582705e-06
set sigmaV0(10361) 202.995000
set ruPrev(10361) 0.0

# Element 10362: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10362) {1394 2834 2833 1393 2846 3331 3330 2845}
set elemKinit(10362) 3.773200081582705e-06
set sigmaV0(10362) 202.995000
set ruPrev(10362) 0.0

# Element 10363: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10363) {2846 3331 3330 2845 1403 2838 2837 1402}
set elemKinit(10363) 3.773200081582705e-06
set sigmaV0(10363) 202.995000
set ruPrev(10363) 0.0

# Element 10364: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10364) {2835 1391 1390 2834 3332 2843 2842 3331}
set elemKinit(10364) 3.773200081582705e-06
set sigmaV0(10364) 192.585000
set ruPrev(10364) 0.0

# Element 10365: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10365) {3332 2843 2842 3331 2839 1400 1399 2838}
set elemKinit(10365) 3.773200081582705e-06
set sigmaV0(10365) 192.585000
set ruPrev(10365) 0.0

# Element 10366: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10366) {1395 2835 2834 1394 2847 3332 3331 2846}
set elemKinit(10366) 3.773200081582705e-06
set sigmaV0(10366) 192.585000
set ruPrev(10366) 0.0

# Element 10367: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10367) {2847 3332 3331 2846 1404 2839 2838 1403}
set elemKinit(10367) 3.773200081582705e-06
set sigmaV0(10367) 192.585000
set ruPrev(10367) 0.0

# Element 10368: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10368) {2836 1392 1391 2835 3333 2844 2843 3332}
set elemKinit(10368) 3.773200081582705e-06
set sigmaV0(10368) 182.175000
set ruPrev(10368) 0.0

# Element 10369: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10369) {3333 2844 2843 3332 2840 1401 1400 2839}
set elemKinit(10369) 3.773200081582705e-06
set sigmaV0(10369) 182.175000
set ruPrev(10369) 0.0

# Element 10370: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10370) {1396 2836 2835 1395 2848 3333 3332 2847}
set elemKinit(10370) 3.773200081582705e-06
set sigmaV0(10370) 182.175000
set ruPrev(10370) 0.0

# Element 10371: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10371) {2848 3333 3332 2847 1405 2840 2839 1404}
set elemKinit(10371) 3.773200081582705e-06
set sigmaV0(10371) 182.175000
set ruPrev(10371) 0.0

# Element 10372: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10372) {1086 169 1392 2836 2628 1094 2844 3333}
set elemKinit(10372) 3.773200081582705e-06
set sigmaV0(10372) 171.765000
set ruPrev(10372) 0.0

# Element 10373: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10373) {2628 1094 2844 3333 1093 171 1401 2840}
set elemKinit(10373) 3.773200081582705e-06
set sigmaV0(10373) 171.765000
set ruPrev(10373) 0.0

# Element 10374: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10374) {170 1086 2836 1396 1095 2628 3333 2848}
set elemKinit(10374) 3.773200081582705e-06
set sigmaV0(10374) 171.765000
set ruPrev(10374) 0.0

# Element 10375: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10375) {1095 2628 3333 2848 172 1093 2840 1405}
set elemKinit(10375) 3.773200081582705e-06
set sigmaV0(10375) 171.765000
set ruPrev(10375) 0.0

# Element 10376: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10376) {2837 1398 248 1406 2850 1409 250 1417}
set elemKinit(10376) 3.773200081582705e-06
set sigmaV0(10376) 213.405000
set ruPrev(10376) 0.0

# Element 10377: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10377) {1402 2837 1406 249 1413 2850 1417 251}
set elemKinit(10377) 3.773200081582705e-06
set sigmaV0(10377) 213.405000
set ruPrev(10377) 0.0

# Element 10378: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10378) {2838 1399 1398 2837 2851 1410 1409 2850}
set elemKinit(10378) 3.773200081582705e-06
set sigmaV0(10378) 202.995000
set ruPrev(10378) 0.0

# Element 10379: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10379) {1403 2838 2837 1402 1414 2851 2850 1413}
set elemKinit(10379) 3.773200081582705e-06
set sigmaV0(10379) 202.995000
set ruPrev(10379) 0.0

# Element 10380: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10380) {2839 1400 1399 2838 2852 1411 1410 2851}
set elemKinit(10380) 3.773200081582705e-06
set sigmaV0(10380) 192.585000
set ruPrev(10380) 0.0

# Element 10381: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10381) {1404 2839 2838 1403 1415 2852 2851 1414}
set elemKinit(10381) 3.773200081582705e-06
set sigmaV0(10381) 192.585000
set ruPrev(10381) 0.0

# Element 10382: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10382) {2840 1401 1400 2839 2853 1412 1411 2852}
set elemKinit(10382) 3.773200081582705e-06
set sigmaV0(10382) 182.175000
set ruPrev(10382) 0.0

# Element 10383: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10383) {1405 2840 2839 1404 1416 2853 2852 1415}
set elemKinit(10383) 3.773200081582705e-06
set sigmaV0(10383) 182.175000
set ruPrev(10383) 0.0

# Element 10384: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10384) {1093 171 1401 2840 1102 173 1412 2853}
set elemKinit(10384) 3.773200081582705e-06
set sigmaV0(10384) 171.765000
set ruPrev(10384) 0.0

# Element 10385: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10385) {172 1093 2840 1405 174 1102 2853 1416}
set elemKinit(10385) 3.773200081582705e-06
set sigmaV0(10385) 171.765000
set ruPrev(10385) 0.0

# Element 10386: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10386) {2850 1409 250 1417 3334 2858 1427 2874}
set elemKinit(10386) 3.773200081582705e-06
set sigmaV0(10386) 213.405000
set ruPrev(10386) 0.0

# Element 10387: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10387) {3334 2858 1427 2874 3335 2862 1428 2875}
set elemKinit(10387) 3.773200081582705e-06
set sigmaV0(10387) 213.405000
set ruPrev(10387) 0.0

# Element 10388: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10388) {3335 2862 1428 2875 2854 1418 252 1426}
set elemKinit(10388) 3.773200081582705e-06
set sigmaV0(10388) 213.405000
set ruPrev(10388) 0.0

# Element 10389: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10389) {1413 2850 1417 251 2866 3334 2874 1429}
set elemKinit(10389) 3.773200081582705e-06
set sigmaV0(10389) 213.405000
set ruPrev(10389) 0.0

# Element 10390: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10390) {2866 3334 2874 1429 2870 3335 2875 1430}
set elemKinit(10390) 3.773200081582705e-06
set sigmaV0(10390) 213.405000
set ruPrev(10390) 0.0

# Element 10391: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10391) {2870 3335 2875 1430 1422 2854 1426 253}
set elemKinit(10391) 3.773200081582705e-06
set sigmaV0(10391) 213.405000
set ruPrev(10391) 0.0

# Element 10392: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10392) {2851 1410 1409 2850 3336 2859 2858 3334}
set elemKinit(10392) 3.773200081582705e-06
set sigmaV0(10392) 202.995000
set ruPrev(10392) 0.0

# Element 10393: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10393) {3336 2859 2858 3334 3337 2863 2862 3335}
set elemKinit(10393) 3.773200081582705e-06
set sigmaV0(10393) 202.995000
set ruPrev(10393) 0.0

# Element 10394: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10394) {3337 2863 2862 3335 2855 1419 1418 2854}
set elemKinit(10394) 3.773200081582705e-06
set sigmaV0(10394) 202.995000
set ruPrev(10394) 0.0

# Element 10395: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10395) {1414 2851 2850 1413 2867 3336 3334 2866}
set elemKinit(10395) 3.773200081582705e-06
set sigmaV0(10395) 202.995000
set ruPrev(10395) 0.0

# Element 10396: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10396) {2867 3336 3334 2866 2871 3337 3335 2870}
set elemKinit(10396) 3.773200081582705e-06
set sigmaV0(10396) 202.995000
set ruPrev(10396) 0.0

# Element 10397: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10397) {2871 3337 3335 2870 1423 2855 2854 1422}
set elemKinit(10397) 3.773200081582705e-06
set sigmaV0(10397) 202.995000
set ruPrev(10397) 0.0

# Element 10398: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10398) {2852 1411 1410 2851 3338 2860 2859 3336}
set elemKinit(10398) 3.773200081582705e-06
set sigmaV0(10398) 192.585000
set ruPrev(10398) 0.0

# Element 10399: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10399) {3338 2860 2859 3336 3339 2864 2863 3337}
set elemKinit(10399) 3.773200081582705e-06
set sigmaV0(10399) 192.585000
set ruPrev(10399) 0.0

# Element 10400: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10400) {3339 2864 2863 3337 2856 1420 1419 2855}
set elemKinit(10400) 3.773200081582705e-06
set sigmaV0(10400) 192.585000
set ruPrev(10400) 0.0

# Element 10401: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10401) {1415 2852 2851 1414 2868 3338 3336 2867}
set elemKinit(10401) 3.773200081582705e-06
set sigmaV0(10401) 192.585000
set ruPrev(10401) 0.0

# Element 10402: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10402) {2868 3338 3336 2867 2872 3339 3337 2871}
set elemKinit(10402) 3.773200081582705e-06
set sigmaV0(10402) 192.585000
set ruPrev(10402) 0.0

# Element 10403: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10403) {2872 3339 3337 2871 1424 2856 2855 1423}
set elemKinit(10403) 3.773200081582705e-06
set sigmaV0(10403) 192.585000
set ruPrev(10403) 0.0

# Element 10404: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10404) {2853 1412 1411 2852 3340 2861 2860 3338}
set elemKinit(10404) 3.773200081582705e-06
set sigmaV0(10404) 182.175000
set ruPrev(10404) 0.0

# Element 10405: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10405) {3340 2861 2860 3338 3341 2865 2864 3339}
set elemKinit(10405) 3.773200081582705e-06
set sigmaV0(10405) 182.175000
set ruPrev(10405) 0.0

# Element 10406: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10406) {3341 2865 2864 3339 2857 1421 1420 2856}
set elemKinit(10406) 3.773200081582705e-06
set sigmaV0(10406) 182.175000
set ruPrev(10406) 0.0

# Element 10407: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10407) {1416 2853 2852 1415 2869 3340 3338 2868}
set elemKinit(10407) 3.773200081582705e-06
set sigmaV0(10407) 182.175000
set ruPrev(10407) 0.0

# Element 10408: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10408) {2869 3340 3338 2868 2873 3341 3339 2872}
set elemKinit(10408) 3.773200081582705e-06
set sigmaV0(10408) 182.175000
set ruPrev(10408) 0.0

# Element 10409: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10409) {2873 3341 3339 2872 1425 2857 2856 1424}
set elemKinit(10409) 3.773200081582705e-06
set sigmaV0(10409) 182.175000
set ruPrev(10409) 0.0

# Element 10410: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10410) {1102 173 1412 2853 2647 1110 2861 3340}
set elemKinit(10410) 3.773200081582705e-06
set sigmaV0(10410) 171.765000
set ruPrev(10410) 0.0

# Element 10411: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10411) {2647 1110 2861 3340 2648 1111 2865 3341}
set elemKinit(10411) 3.773200081582705e-06
set sigmaV0(10411) 171.765000
set ruPrev(10411) 0.0

# Element 10412: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10412) {2648 1111 2865 3341 1109 175 1421 2857}
set elemKinit(10412) 3.773200081582705e-06
set sigmaV0(10412) 171.765000
set ruPrev(10412) 0.0

# Element 10413: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10413) {174 1102 2853 1416 1112 2647 3340 2869}
set elemKinit(10413) 3.773200081582705e-06
set sigmaV0(10413) 171.765000
set ruPrev(10413) 0.0

# Element 10414: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10414) {1112 2647 3340 2869 1113 2648 3341 2873}
set elemKinit(10414) 3.773200081582705e-06
set sigmaV0(10414) 171.765000
set ruPrev(10414) 0.0

# Element 10415: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10415) {1113 2648 3341 2873 176 1109 2857 1425}
set elemKinit(10415) 3.773200081582705e-06
set sigmaV0(10415) 171.765000
set ruPrev(10415) 0.0

# Element 10416: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10416) {1431 1324 233 254 2876 2794 1340 1439}
set elemKinit(10416) 3.773200081582705e-06
set sigmaV0(10416) 213.405000
set ruPrev(10416) 0.0

# Element 10417: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10417) {2876 2794 1340 1439 2880 2798 1341 1440}
set elemKinit(10417) 3.773200081582705e-06
set sigmaV0(10417) 213.405000
set ruPrev(10417) 0.0

# Element 10418: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10418) {2880 2798 1341 1440 1435 1333 235 255}
set elemKinit(10418) 3.773200081582705e-06
set sigmaV0(10418) 213.405000
set ruPrev(10418) 0.0

# Element 10419: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10419) {1432 1325 1324 1431 2877 2795 2794 2876}
set elemKinit(10419) 3.773200081582705e-06
set sigmaV0(10419) 202.995000
set ruPrev(10419) 0.0

# Element 10420: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10420) {2877 2795 2794 2876 2881 2799 2798 2880}
set elemKinit(10420) 3.773200081582705e-06
set sigmaV0(10420) 202.995000
set ruPrev(10420) 0.0

# Element 10421: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10421) {2881 2799 2798 2880 1436 1334 1333 1435}
set elemKinit(10421) 3.773200081582705e-06
set sigmaV0(10421) 202.995000
set ruPrev(10421) 0.0

# Element 10422: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10422) {1433 1326 1325 1432 2878 2796 2795 2877}
set elemKinit(10422) 3.773200081582705e-06
set sigmaV0(10422) 192.585000
set ruPrev(10422) 0.0

# Element 10423: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10423) {2878 2796 2795 2877 2882 2800 2799 2881}
set elemKinit(10423) 3.773200081582705e-06
set sigmaV0(10423) 192.585000
set ruPrev(10423) 0.0

# Element 10424: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10424) {2882 2800 2799 2881 1437 1335 1334 1436}
set elemKinit(10424) 3.773200081582705e-06
set sigmaV0(10424) 192.585000
set ruPrev(10424) 0.0

# Element 10425: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10425) {1434 1327 1326 1433 2879 2797 2796 2878}
set elemKinit(10425) 3.773200081582705e-06
set sigmaV0(10425) 182.175000
set ruPrev(10425) 0.0

# Element 10426: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10426) {2879 2797 2796 2878 2883 2801 2800 2882}
set elemKinit(10426) 3.773200081582705e-06
set sigmaV0(10426) 182.175000
set ruPrev(10426) 0.0

# Element 10427: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10427) {2883 2801 2800 2882 1438 1336 1335 1437}
set elemKinit(10427) 3.773200081582705e-06
set sigmaV0(10427) 182.175000
set ruPrev(10427) 0.0

# Element 10428: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10428) {177 156 1327 1434 1120 1041 2797 2879}
set elemKinit(10428) 3.773200081582705e-06
set sigmaV0(10428) 171.765000
set ruPrev(10428) 0.0

# Element 10429: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10429) {1120 1041 2797 2879 1121 1042 2801 2883}
set elemKinit(10429) 3.773200081582705e-06
set sigmaV0(10429) 171.765000
set ruPrev(10429) 0.0

# Element 10430: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10430) {1121 1042 2801 2883 178 158 1336 1438}
set elemKinit(10430) 3.773200081582705e-06
set sigmaV0(10430) 171.765000
set ruPrev(10430) 0.0

# Element 10431: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10431) {1435 1333 235 255 1441 1346 237 256}
set elemKinit(10431) 3.773200081582705e-06
set sigmaV0(10431) 213.405000
set ruPrev(10431) 0.0

# Element 10432: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10432) {1436 1334 1333 1435 1442 1347 1346 1441}
set elemKinit(10432) 3.773200081582705e-06
set sigmaV0(10432) 202.995000
set ruPrev(10432) 0.0

# Element 10433: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10433) {1437 1335 1334 1436 1443 1348 1347 1442}
set elemKinit(10433) 3.773200081582705e-06
set sigmaV0(10433) 192.585000
set ruPrev(10433) 0.0

# Element 10434: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10434) {1438 1336 1335 1437 1444 1349 1348 1443}
set elemKinit(10434) 3.773200081582705e-06
set sigmaV0(10434) 182.175000
set ruPrev(10434) 0.0

# Element 10435: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10435) {178 158 1336 1438 179 160 1349 1444}
set elemKinit(10435) 3.773200081582705e-06
set sigmaV0(10435) 171.765000
set ruPrev(10435) 0.0

# Element 10436: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10436) {1441 1346 237 256 2884 2816 1361 1449}
set elemKinit(10436) 3.773200081582705e-06
set sigmaV0(10436) 213.405000
set ruPrev(10436) 0.0

# Element 10437: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10437) {2884 2816 1361 1449 1445 1355 239 257}
set elemKinit(10437) 3.773200081582705e-06
set sigmaV0(10437) 213.405000
set ruPrev(10437) 0.0

# Element 10438: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10438) {1442 1347 1346 1441 2885 2817 2816 2884}
set elemKinit(10438) 3.773200081582705e-06
set sigmaV0(10438) 202.995000
set ruPrev(10438) 0.0

# Element 10439: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10439) {2885 2817 2816 2884 1446 1356 1355 1445}
set elemKinit(10439) 3.773200081582705e-06
set sigmaV0(10439) 202.995000
set ruPrev(10439) 0.0

# Element 10440: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10440) {1443 1348 1347 1442 2886 2818 2817 2885}
set elemKinit(10440) 3.773200081582705e-06
set sigmaV0(10440) 192.585000
set ruPrev(10440) 0.0

# Element 10441: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10441) {2886 2818 2817 2885 1447 1357 1356 1446}
set elemKinit(10441) 3.773200081582705e-06
set sigmaV0(10441) 192.585000
set ruPrev(10441) 0.0

# Element 10442: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10442) {1444 1349 1348 1443 2887 2819 2818 2886}
set elemKinit(10442) 3.773200081582705e-06
set sigmaV0(10442) 182.175000
set ruPrev(10442) 0.0

# Element 10443: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10443) {2887 2819 2818 2886 1448 1358 1357 1447}
set elemKinit(10443) 3.773200081582705e-06
set sigmaV0(10443) 182.175000
set ruPrev(10443) 0.0

# Element 10444: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10444) {179 160 1349 1444 1128 1058 2819 2887}
set elemKinit(10444) 3.773200081582705e-06
set sigmaV0(10444) 171.765000
set ruPrev(10444) 0.0

# Element 10445: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10445) {1128 1058 2819 2887 180 162 1358 1448}
set elemKinit(10445) 3.773200081582705e-06
set sigmaV0(10445) 171.765000
set ruPrev(10445) 0.0

# Element 10446: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10446) {1445 1355 239 257 1450 1366 241 258}
set elemKinit(10446) 3.773200081582705e-06
set sigmaV0(10446) 213.405000
set ruPrev(10446) 0.0

# Element 10447: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10447) {1446 1356 1355 1445 1451 1367 1366 1450}
set elemKinit(10447) 3.773200081582705e-06
set sigmaV0(10447) 202.995000
set ruPrev(10447) 0.0

# Element 10448: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10448) {1447 1357 1356 1446 1452 1368 1367 1451}
set elemKinit(10448) 3.773200081582705e-06
set sigmaV0(10448) 192.585000
set ruPrev(10448) 0.0

# Element 10449: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10449) {1448 1358 1357 1447 1453 1369 1368 1452}
set elemKinit(10449) 3.773200081582705e-06
set sigmaV0(10449) 182.175000
set ruPrev(10449) 0.0

# Element 10450: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10450) {180 162 1358 1448 181 164 1369 1453}
set elemKinit(10450) 3.773200081582705e-06
set sigmaV0(10450) 171.765000
set ruPrev(10450) 0.0

# Element 10451: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10451) {1450 1366 241 258 1454 1375 243 259}
set elemKinit(10451) 3.773200081582705e-06
set sigmaV0(10451) 213.405000
set ruPrev(10451) 0.0

# Element 10452: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10452) {1451 1367 1366 1450 1455 1376 1375 1454}
set elemKinit(10452) 3.773200081582705e-06
set sigmaV0(10452) 202.995000
set ruPrev(10452) 0.0

# Element 10453: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10453) {1452 1368 1367 1451 1456 1377 1376 1455}
set elemKinit(10453) 3.773200081582705e-06
set sigmaV0(10453) 192.585000
set ruPrev(10453) 0.0

# Element 10454: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10454) {1453 1369 1368 1452 1457 1378 1377 1456}
set elemKinit(10454) 3.773200081582705e-06
set sigmaV0(10454) 182.175000
set ruPrev(10454) 0.0

# Element 10455: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10455) {181 164 1369 1453 182 166 1378 1457}
set elemKinit(10455) 3.773200081582705e-06
set sigmaV0(10455) 171.765000
set ruPrev(10455) 0.0

# Element 10456: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10456) {1454 1375 243 259 1458 1384 245 260}
set elemKinit(10456) 3.773200081582705e-06
set sigmaV0(10456) 213.405000
set ruPrev(10456) 0.0

# Element 10457: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10457) {1455 1376 1375 1454 1459 1385 1384 1458}
set elemKinit(10457) 3.773200081582705e-06
set sigmaV0(10457) 202.995000
set ruPrev(10457) 0.0

# Element 10458: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10458) {1456 1377 1376 1455 1460 1386 1385 1459}
set elemKinit(10458) 3.773200081582705e-06
set sigmaV0(10458) 192.585000
set ruPrev(10458) 0.0

# Element 10459: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10459) {1457 1378 1377 1456 1461 1387 1386 1460}
set elemKinit(10459) 3.773200081582705e-06
set sigmaV0(10459) 182.175000
set ruPrev(10459) 0.0

# Element 10460: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10460) {182 166 1378 1457 183 168 1387 1461}
set elemKinit(10460) 3.773200081582705e-06
set sigmaV0(10460) 171.765000
set ruPrev(10460) 0.0

# Element 10461: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10461) {1458 1384 245 260 1462 1393 247 261}
set elemKinit(10461) 3.773200081582705e-06
set sigmaV0(10461) 213.405000
set ruPrev(10461) 0.0

# Element 10462: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10462) {1459 1385 1384 1458 1463 1394 1393 1462}
set elemKinit(10462) 3.773200081582705e-06
set sigmaV0(10462) 202.995000
set ruPrev(10462) 0.0

# Element 10463: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10463) {1460 1386 1385 1459 1464 1395 1394 1463}
set elemKinit(10463) 3.773200081582705e-06
set sigmaV0(10463) 192.585000
set ruPrev(10463) 0.0

# Element 10464: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10464) {1461 1387 1386 1460 1465 1396 1395 1464}
set elemKinit(10464) 3.773200081582705e-06
set sigmaV0(10464) 182.175000
set ruPrev(10464) 0.0

# Element 10465: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10465) {183 168 1387 1461 184 170 1396 1465}
set elemKinit(10465) 3.773200081582705e-06
set sigmaV0(10465) 171.765000
set ruPrev(10465) 0.0

# Element 10466: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10466) {1462 1393 247 261 2888 2845 1408 1470}
set elemKinit(10466) 3.773200081582705e-06
set sigmaV0(10466) 213.405000
set ruPrev(10466) 0.0

# Element 10467: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10467) {2888 2845 1408 1470 1466 1402 249 262}
set elemKinit(10467) 3.773200081582705e-06
set sigmaV0(10467) 213.405000
set ruPrev(10467) 0.0

# Element 10468: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10468) {1463 1394 1393 1462 2889 2846 2845 2888}
set elemKinit(10468) 3.773200081582705e-06
set sigmaV0(10468) 202.995000
set ruPrev(10468) 0.0

# Element 10469: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10469) {2889 2846 2845 2888 1467 1403 1402 1466}
set elemKinit(10469) 3.773200081582705e-06
set sigmaV0(10469) 202.995000
set ruPrev(10469) 0.0

# Element 10470: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10470) {1464 1395 1394 1463 2890 2847 2846 2889}
set elemKinit(10470) 3.773200081582705e-06
set sigmaV0(10470) 192.585000
set ruPrev(10470) 0.0

# Element 10471: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10471) {2890 2847 2846 2889 1468 1404 1403 1467}
set elemKinit(10471) 3.773200081582705e-06
set sigmaV0(10471) 192.585000
set ruPrev(10471) 0.0

# Element 10472: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10472) {1465 1396 1395 1464 2891 2848 2847 2890}
set elemKinit(10472) 3.773200081582705e-06
set sigmaV0(10472) 182.175000
set ruPrev(10472) 0.0

# Element 10473: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10473) {2891 2848 2847 2890 1469 1405 1404 1468}
set elemKinit(10473) 3.773200081582705e-06
set sigmaV0(10473) 182.175000
set ruPrev(10473) 0.0

# Element 10474: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10474) {184 170 1396 1465 1144 1095 2848 2891}
set elemKinit(10474) 3.773200081582705e-06
set sigmaV0(10474) 171.765000
set ruPrev(10474) 0.0

# Element 10475: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10475) {1144 1095 2848 2891 185 172 1405 1469}
set elemKinit(10475) 3.773200081582705e-06
set sigmaV0(10475) 171.765000
set ruPrev(10475) 0.0

# Element 10476: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10476) {1466 1402 249 262 1471 1413 251 263}
set elemKinit(10476) 3.773200081582705e-06
set sigmaV0(10476) 213.405000
set ruPrev(10476) 0.0

# Element 10477: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10477) {1467 1403 1402 1466 1472 1414 1413 1471}
set elemKinit(10477) 3.773200081582705e-06
set sigmaV0(10477) 202.995000
set ruPrev(10477) 0.0

# Element 10478: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10478) {1468 1404 1403 1467 1473 1415 1414 1472}
set elemKinit(10478) 3.773200081582705e-06
set sigmaV0(10478) 192.585000
set ruPrev(10478) 0.0

# Element 10479: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10479) {1469 1405 1404 1468 1474 1416 1415 1473}
set elemKinit(10479) 3.773200081582705e-06
set sigmaV0(10479) 182.175000
set ruPrev(10479) 0.0

# Element 10480: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10480) {185 172 1405 1469 186 174 1416 1474}
set elemKinit(10480) 3.773200081582705e-06
set sigmaV0(10480) 171.765000
set ruPrev(10480) 0.0

# Element 10481: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10481) {1471 1413 251 263 2892 2866 1429 1479}
set elemKinit(10481) 3.773200081582705e-06
set sigmaV0(10481) 213.405000
set ruPrev(10481) 0.0

# Element 10482: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10482) {2892 2866 1429 1479 2896 2870 1430 1480}
set elemKinit(10482) 3.773200081582705e-06
set sigmaV0(10482) 213.405000
set ruPrev(10482) 0.0

# Element 10483: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10483) {2896 2870 1430 1480 1475 1422 253 264}
set elemKinit(10483) 3.773200081582705e-06
set sigmaV0(10483) 213.405000
set ruPrev(10483) 0.0

# Element 10484: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10484) {1472 1414 1413 1471 2893 2867 2866 2892}
set elemKinit(10484) 3.773200081582705e-06
set sigmaV0(10484) 202.995000
set ruPrev(10484) 0.0

# Element 10485: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10485) {2893 2867 2866 2892 2897 2871 2870 2896}
set elemKinit(10485) 3.773200081582705e-06
set sigmaV0(10485) 202.995000
set ruPrev(10485) 0.0

# Element 10486: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10486) {2897 2871 2870 2896 1476 1423 1422 1475}
set elemKinit(10486) 3.773200081582705e-06
set sigmaV0(10486) 202.995000
set ruPrev(10486) 0.0

# Element 10487: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10487) {1473 1415 1414 1472 2894 2868 2867 2893}
set elemKinit(10487) 3.773200081582705e-06
set sigmaV0(10487) 192.585000
set ruPrev(10487) 0.0

# Element 10488: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10488) {2894 2868 2867 2893 2898 2872 2871 2897}
set elemKinit(10488) 3.773200081582705e-06
set sigmaV0(10488) 192.585000
set ruPrev(10488) 0.0

# Element 10489: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10489) {2898 2872 2871 2897 1477 1424 1423 1476}
set elemKinit(10489) 3.773200081582705e-06
set sigmaV0(10489) 192.585000
set ruPrev(10489) 0.0

# Element 10490: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10490) {1474 1416 1415 1473 2895 2869 2868 2894}
set elemKinit(10490) 3.773200081582705e-06
set sigmaV0(10490) 182.175000
set ruPrev(10490) 0.0

# Element 10491: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10491) {2895 2869 2868 2894 2899 2873 2872 2898}
set elemKinit(10491) 3.773200081582705e-06
set sigmaV0(10491) 182.175000
set ruPrev(10491) 0.0

# Element 10492: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10492) {2899 2873 2872 2898 1478 1425 1424 1477}
set elemKinit(10492) 3.773200081582705e-06
set sigmaV0(10492) 182.175000
set ruPrev(10492) 0.0

# Element 10493: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10493) {186 174 1416 1474 1151 1112 2869 2895}
set elemKinit(10493) 3.773200081582705e-06
set sigmaV0(10493) 171.765000
set ruPrev(10493) 0.0

# Element 10494: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10494) {1151 1112 2869 2895 1152 1113 2873 2899}
set elemKinit(10494) 3.773200081582705e-06
set sigmaV0(10494) 171.765000
set ruPrev(10494) 0.0

# Element 10495: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10495) {1152 1113 2873 2899 187 176 1425 1478}
set elemKinit(10495) 3.773200081582705e-06
set sigmaV0(10495) 171.765000
set ruPrev(10495) 0.0

# Element 10496: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10496) {1481 1431 254 265 2900 2876 1439 1489}
set elemKinit(10496) 3.773200081582705e-06
set sigmaV0(10496) 213.405000
set ruPrev(10496) 0.0

# Element 10497: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10497) {2900 2876 1439 1489 2904 2880 1440 1490}
set elemKinit(10497) 3.773200081582705e-06
set sigmaV0(10497) 213.405000
set ruPrev(10497) 0.0

# Element 10498: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10498) {2904 2880 1440 1490 1485 1435 255 266}
set elemKinit(10498) 3.773200081582705e-06
set sigmaV0(10498) 213.405000
set ruPrev(10498) 0.0

# Element 10499: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10499) {1482 1432 1431 1481 2901 2877 2876 2900}
set elemKinit(10499) 3.773200081582705e-06
set sigmaV0(10499) 202.995000
set ruPrev(10499) 0.0

# Element 10500: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10500) {2901 2877 2876 2900 2905 2881 2880 2904}
set elemKinit(10500) 3.773200081582705e-06
set sigmaV0(10500) 202.995000
set ruPrev(10500) 0.0

# Element 10501: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10501) {2905 2881 2880 2904 1486 1436 1435 1485}
set elemKinit(10501) 3.773200081582705e-06
set sigmaV0(10501) 202.995000
set ruPrev(10501) 0.0

# Element 10502: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10502) {1483 1433 1432 1482 2902 2878 2877 2901}
set elemKinit(10502) 3.773200081582705e-06
set sigmaV0(10502) 192.585000
set ruPrev(10502) 0.0

# Element 10503: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10503) {2902 2878 2877 2901 2906 2882 2881 2905}
set elemKinit(10503) 3.773200081582705e-06
set sigmaV0(10503) 192.585000
set ruPrev(10503) 0.0

# Element 10504: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10504) {2906 2882 2881 2905 1487 1437 1436 1486}
set elemKinit(10504) 3.773200081582705e-06
set sigmaV0(10504) 192.585000
set ruPrev(10504) 0.0

# Element 10505: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10505) {1484 1434 1433 1483 2903 2879 2878 2902}
set elemKinit(10505) 3.773200081582705e-06
set sigmaV0(10505) 182.175000
set ruPrev(10505) 0.0

# Element 10506: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10506) {2903 2879 2878 2902 2907 2883 2882 2906}
set elemKinit(10506) 3.773200081582705e-06
set sigmaV0(10506) 182.175000
set ruPrev(10506) 0.0

# Element 10507: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10507) {2907 2883 2882 2906 1488 1438 1437 1487}
set elemKinit(10507) 3.773200081582705e-06
set sigmaV0(10507) 182.175000
set ruPrev(10507) 0.0

# Element 10508: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10508) {188 177 1434 1484 1159 1120 2879 2903}
set elemKinit(10508) 3.773200081582705e-06
set sigmaV0(10508) 171.765000
set ruPrev(10508) 0.0

# Element 10509: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10509) {1159 1120 2879 2903 1160 1121 2883 2907}
set elemKinit(10509) 3.773200081582705e-06
set sigmaV0(10509) 171.765000
set ruPrev(10509) 0.0

# Element 10510: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10510) {1160 1121 2883 2907 189 178 1438 1488}
set elemKinit(10510) 3.773200081582705e-06
set sigmaV0(10510) 171.765000
set ruPrev(10510) 0.0

# Element 10511: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10511) {1485 1435 255 266 1491 1441 256 267}
set elemKinit(10511) 3.773200081582705e-06
set sigmaV0(10511) 213.405000
set ruPrev(10511) 0.0

# Element 10512: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10512) {1486 1436 1435 1485 1492 1442 1441 1491}
set elemKinit(10512) 3.773200081582705e-06
set sigmaV0(10512) 202.995000
set ruPrev(10512) 0.0

# Element 10513: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10513) {1487 1437 1436 1486 1493 1443 1442 1492}
set elemKinit(10513) 3.773200081582705e-06
set sigmaV0(10513) 192.585000
set ruPrev(10513) 0.0

# Element 10514: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10514) {1488 1438 1437 1487 1494 1444 1443 1493}
set elemKinit(10514) 3.773200081582705e-06
set sigmaV0(10514) 182.175000
set ruPrev(10514) 0.0

# Element 10515: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10515) {189 178 1438 1488 190 179 1444 1494}
set elemKinit(10515) 3.773200081582705e-06
set sigmaV0(10515) 171.765000
set ruPrev(10515) 0.0

# Element 10516: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10516) {1491 1441 256 267 2908 2884 1449 1499}
set elemKinit(10516) 3.773200081582705e-06
set sigmaV0(10516) 213.405000
set ruPrev(10516) 0.0

# Element 10517: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10517) {2908 2884 1449 1499 1495 1445 257 268}
set elemKinit(10517) 3.773200081582705e-06
set sigmaV0(10517) 213.405000
set ruPrev(10517) 0.0

# Element 10518: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10518) {1492 1442 1441 1491 2909 2885 2884 2908}
set elemKinit(10518) 3.773200081582705e-06
set sigmaV0(10518) 202.995000
set ruPrev(10518) 0.0

# Element 10519: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10519) {2909 2885 2884 2908 1496 1446 1445 1495}
set elemKinit(10519) 3.773200081582705e-06
set sigmaV0(10519) 202.995000
set ruPrev(10519) 0.0

# Element 10520: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10520) {1493 1443 1442 1492 2910 2886 2885 2909}
set elemKinit(10520) 3.773200081582705e-06
set sigmaV0(10520) 192.585000
set ruPrev(10520) 0.0

# Element 10521: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10521) {2910 2886 2885 2909 1497 1447 1446 1496}
set elemKinit(10521) 3.773200081582705e-06
set sigmaV0(10521) 192.585000
set ruPrev(10521) 0.0

# Element 10522: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10522) {1494 1444 1443 1493 2911 2887 2886 2910}
set elemKinit(10522) 3.773200081582705e-06
set sigmaV0(10522) 182.175000
set ruPrev(10522) 0.0

# Element 10523: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10523) {2911 2887 2886 2910 1498 1448 1447 1497}
set elemKinit(10523) 3.773200081582705e-06
set sigmaV0(10523) 182.175000
set ruPrev(10523) 0.0

# Element 10524: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10524) {190 179 1444 1494 1167 1128 2887 2911}
set elemKinit(10524) 3.773200081582705e-06
set sigmaV0(10524) 171.765000
set ruPrev(10524) 0.0

# Element 10525: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10525) {1167 1128 2887 2911 191 180 1448 1498}
set elemKinit(10525) 3.773200081582705e-06
set sigmaV0(10525) 171.765000
set ruPrev(10525) 0.0

# Element 10526: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10526) {1495 1445 257 268 1500 1450 258 269}
set elemKinit(10526) 3.773200081582705e-06
set sigmaV0(10526) 213.405000
set ruPrev(10526) 0.0

# Element 10527: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10527) {1496 1446 1445 1495 1501 1451 1450 1500}
set elemKinit(10527) 3.773200081582705e-06
set sigmaV0(10527) 202.995000
set ruPrev(10527) 0.0

# Element 10528: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10528) {1497 1447 1446 1496 1502 1452 1451 1501}
set elemKinit(10528) 3.773200081582705e-06
set sigmaV0(10528) 192.585000
set ruPrev(10528) 0.0

# Element 10529: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10529) {1498 1448 1447 1497 1503 1453 1452 1502}
set elemKinit(10529) 3.773200081582705e-06
set sigmaV0(10529) 182.175000
set ruPrev(10529) 0.0

# Element 10530: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10530) {191 180 1448 1498 192 181 1453 1503}
set elemKinit(10530) 3.773200081582705e-06
set sigmaV0(10530) 171.765000
set ruPrev(10530) 0.0

# Element 10531: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10531) {1500 1450 258 269 1504 1454 259 270}
set elemKinit(10531) 3.773200081582705e-06
set sigmaV0(10531) 213.405000
set ruPrev(10531) 0.0

# Element 10532: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10532) {1501 1451 1450 1500 1505 1455 1454 1504}
set elemKinit(10532) 3.773200081582705e-06
set sigmaV0(10532) 202.995000
set ruPrev(10532) 0.0

# Element 10533: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10533) {1502 1452 1451 1501 1506 1456 1455 1505}
set elemKinit(10533) 3.773200081582705e-06
set sigmaV0(10533) 192.585000
set ruPrev(10533) 0.0

# Element 10534: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10534) {1503 1453 1452 1502 1507 1457 1456 1506}
set elemKinit(10534) 3.773200081582705e-06
set sigmaV0(10534) 182.175000
set ruPrev(10534) 0.0

# Element 10535: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10535) {192 181 1453 1503 193 182 1457 1507}
set elemKinit(10535) 3.773200081582705e-06
set sigmaV0(10535) 171.765000
set ruPrev(10535) 0.0

# Element 10536: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10536) {1504 1454 259 270 1508 1458 260 271}
set elemKinit(10536) 3.773200081582705e-06
set sigmaV0(10536) 213.405000
set ruPrev(10536) 0.0

# Element 10537: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10537) {1505 1455 1454 1504 1509 1459 1458 1508}
set elemKinit(10537) 3.773200081582705e-06
set sigmaV0(10537) 202.995000
set ruPrev(10537) 0.0

# Element 10538: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10538) {1506 1456 1455 1505 1510 1460 1459 1509}
set elemKinit(10538) 3.773200081582705e-06
set sigmaV0(10538) 192.585000
set ruPrev(10538) 0.0

# Element 10539: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10539) {1507 1457 1456 1506 1511 1461 1460 1510}
set elemKinit(10539) 3.773200081582705e-06
set sigmaV0(10539) 182.175000
set ruPrev(10539) 0.0

# Element 10540: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10540) {193 182 1457 1507 194 183 1461 1511}
set elemKinit(10540) 3.773200081582705e-06
set sigmaV0(10540) 171.765000
set ruPrev(10540) 0.0

# Element 10541: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10541) {1508 1458 260 271 1512 1462 261 272}
set elemKinit(10541) 3.773200081582705e-06
set sigmaV0(10541) 213.405000
set ruPrev(10541) 0.0

# Element 10542: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10542) {1509 1459 1458 1508 1513 1463 1462 1512}
set elemKinit(10542) 3.773200081582705e-06
set sigmaV0(10542) 202.995000
set ruPrev(10542) 0.0

# Element 10543: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10543) {1510 1460 1459 1509 1514 1464 1463 1513}
set elemKinit(10543) 3.773200081582705e-06
set sigmaV0(10543) 192.585000
set ruPrev(10543) 0.0

# Element 10544: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10544) {1511 1461 1460 1510 1515 1465 1464 1514}
set elemKinit(10544) 3.773200081582705e-06
set sigmaV0(10544) 182.175000
set ruPrev(10544) 0.0

# Element 10545: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10545) {194 183 1461 1511 195 184 1465 1515}
set elemKinit(10545) 3.773200081582705e-06
set sigmaV0(10545) 171.765000
set ruPrev(10545) 0.0

# Element 10546: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10546) {1512 1462 261 272 2912 2888 1470 1520}
set elemKinit(10546) 3.773200081582705e-06
set sigmaV0(10546) 213.405000
set ruPrev(10546) 0.0

# Element 10547: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10547) {2912 2888 1470 1520 1516 1466 262 273}
set elemKinit(10547) 3.773200081582705e-06
set sigmaV0(10547) 213.405000
set ruPrev(10547) 0.0

# Element 10548: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10548) {1513 1463 1462 1512 2913 2889 2888 2912}
set elemKinit(10548) 3.773200081582705e-06
set sigmaV0(10548) 202.995000
set ruPrev(10548) 0.0

# Element 10549: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10549) {2913 2889 2888 2912 1517 1467 1466 1516}
set elemKinit(10549) 3.773200081582705e-06
set sigmaV0(10549) 202.995000
set ruPrev(10549) 0.0

# Element 10550: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10550) {1514 1464 1463 1513 2914 2890 2889 2913}
set elemKinit(10550) 3.773200081582705e-06
set sigmaV0(10550) 192.585000
set ruPrev(10550) 0.0

# Element 10551: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10551) {2914 2890 2889 2913 1518 1468 1467 1517}
set elemKinit(10551) 3.773200081582705e-06
set sigmaV0(10551) 192.585000
set ruPrev(10551) 0.0

# Element 10552: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10552) {1515 1465 1464 1514 2915 2891 2890 2914}
set elemKinit(10552) 3.773200081582705e-06
set sigmaV0(10552) 182.175000
set ruPrev(10552) 0.0

# Element 10553: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10553) {2915 2891 2890 2914 1519 1469 1468 1518}
set elemKinit(10553) 3.773200081582705e-06
set sigmaV0(10553) 182.175000
set ruPrev(10553) 0.0

# Element 10554: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10554) {195 184 1465 1515 1183 1144 2891 2915}
set elemKinit(10554) 3.773200081582705e-06
set sigmaV0(10554) 171.765000
set ruPrev(10554) 0.0

# Element 10555: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10555) {1183 1144 2891 2915 196 185 1469 1519}
set elemKinit(10555) 3.773200081582705e-06
set sigmaV0(10555) 171.765000
set ruPrev(10555) 0.0

# Element 10556: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10556) {1516 1466 262 273 1521 1471 263 274}
set elemKinit(10556) 3.773200081582705e-06
set sigmaV0(10556) 213.405000
set ruPrev(10556) 0.0

# Element 10557: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10557) {1517 1467 1466 1516 1522 1472 1471 1521}
set elemKinit(10557) 3.773200081582705e-06
set sigmaV0(10557) 202.995000
set ruPrev(10557) 0.0

# Element 10558: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10558) {1518 1468 1467 1517 1523 1473 1472 1522}
set elemKinit(10558) 3.773200081582705e-06
set sigmaV0(10558) 192.585000
set ruPrev(10558) 0.0

# Element 10559: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10559) {1519 1469 1468 1518 1524 1474 1473 1523}
set elemKinit(10559) 3.773200081582705e-06
set sigmaV0(10559) 182.175000
set ruPrev(10559) 0.0

# Element 10560: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10560) {196 185 1469 1519 197 186 1474 1524}
set elemKinit(10560) 3.773200081582705e-06
set sigmaV0(10560) 171.765000
set ruPrev(10560) 0.0

# Element 10561: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10561) {1521 1471 263 274 2916 2892 1479 1529}
set elemKinit(10561) 3.773200081582705e-06
set sigmaV0(10561) 213.405000
set ruPrev(10561) 0.0

# Element 10562: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10562) {2916 2892 1479 1529 2920 2896 1480 1530}
set elemKinit(10562) 3.773200081582705e-06
set sigmaV0(10562) 213.405000
set ruPrev(10562) 0.0

# Element 10563: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10563) {2920 2896 1480 1530 1525 1475 264 275}
set elemKinit(10563) 3.773200081582705e-06
set sigmaV0(10563) 213.405000
set ruPrev(10563) 0.0

# Element 10564: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10564) {1522 1472 1471 1521 2917 2893 2892 2916}
set elemKinit(10564) 3.773200081582705e-06
set sigmaV0(10564) 202.995000
set ruPrev(10564) 0.0

# Element 10565: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10565) {2917 2893 2892 2916 2921 2897 2896 2920}
set elemKinit(10565) 3.773200081582705e-06
set sigmaV0(10565) 202.995000
set ruPrev(10565) 0.0

# Element 10566: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10566) {2921 2897 2896 2920 1526 1476 1475 1525}
set elemKinit(10566) 3.773200081582705e-06
set sigmaV0(10566) 202.995000
set ruPrev(10566) 0.0

# Element 10567: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10567) {1523 1473 1472 1522 2918 2894 2893 2917}
set elemKinit(10567) 3.773200081582705e-06
set sigmaV0(10567) 192.585000
set ruPrev(10567) 0.0

# Element 10568: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10568) {2918 2894 2893 2917 2922 2898 2897 2921}
set elemKinit(10568) 3.773200081582705e-06
set sigmaV0(10568) 192.585000
set ruPrev(10568) 0.0

# Element 10569: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10569) {2922 2898 2897 2921 1527 1477 1476 1526}
set elemKinit(10569) 3.773200081582705e-06
set sigmaV0(10569) 192.585000
set ruPrev(10569) 0.0

# Element 10570: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10570) {1524 1474 1473 1523 2919 2895 2894 2918}
set elemKinit(10570) 3.773200081582705e-06
set sigmaV0(10570) 182.175000
set ruPrev(10570) 0.0

# Element 10571: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10571) {2919 2895 2894 2918 2923 2899 2898 2922}
set elemKinit(10571) 3.773200081582705e-06
set sigmaV0(10571) 182.175000
set ruPrev(10571) 0.0

# Element 10572: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10572) {2923 2899 2898 2922 1528 1478 1477 1527}
set elemKinit(10572) 3.773200081582705e-06
set sigmaV0(10572) 182.175000
set ruPrev(10572) 0.0

# Element 10573: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10573) {197 186 1474 1524 1190 1151 2895 2919}
set elemKinit(10573) 3.773200081582705e-06
set sigmaV0(10573) 171.765000
set ruPrev(10573) 0.0

# Element 10574: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10574) {1190 1151 2895 2919 1191 1152 2899 2923}
set elemKinit(10574) 3.773200081582705e-06
set sigmaV0(10574) 171.765000
set ruPrev(10574) 0.0

# Element 10575: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10575) {1191 1152 2899 2923 198 187 1478 1528}
set elemKinit(10575) 3.773200081582705e-06
set sigmaV0(10575) 171.765000
set ruPrev(10575) 0.0

# Element 10576: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10576) {1531 1481 265 276 2924 2900 1489 1539}
set elemKinit(10576) 3.773200081582705e-06
set sigmaV0(10576) 213.405000
set ruPrev(10576) 0.0

# Element 10577: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10577) {2924 2900 1489 1539 2928 2904 1490 1540}
set elemKinit(10577) 3.773200081582705e-06
set sigmaV0(10577) 213.405000
set ruPrev(10577) 0.0

# Element 10578: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10578) {2928 2904 1490 1540 1535 1485 266 277}
set elemKinit(10578) 3.773200081582705e-06
set sigmaV0(10578) 213.405000
set ruPrev(10578) 0.0

# Element 10579: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10579) {1532 1482 1481 1531 2925 2901 2900 2924}
set elemKinit(10579) 3.773200081582705e-06
set sigmaV0(10579) 202.995000
set ruPrev(10579) 0.0

# Element 10580: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10580) {2925 2901 2900 2924 2929 2905 2904 2928}
set elemKinit(10580) 3.773200081582705e-06
set sigmaV0(10580) 202.995000
set ruPrev(10580) 0.0

# Element 10581: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10581) {2929 2905 2904 2928 1536 1486 1485 1535}
set elemKinit(10581) 3.773200081582705e-06
set sigmaV0(10581) 202.995000
set ruPrev(10581) 0.0

# Element 10582: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10582) {1533 1483 1482 1532 2926 2902 2901 2925}
set elemKinit(10582) 3.773200081582705e-06
set sigmaV0(10582) 192.585000
set ruPrev(10582) 0.0

# Element 10583: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10583) {2926 2902 2901 2925 2930 2906 2905 2929}
set elemKinit(10583) 3.773200081582705e-06
set sigmaV0(10583) 192.585000
set ruPrev(10583) 0.0

# Element 10584: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10584) {2930 2906 2905 2929 1537 1487 1486 1536}
set elemKinit(10584) 3.773200081582705e-06
set sigmaV0(10584) 192.585000
set ruPrev(10584) 0.0

# Element 10585: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10585) {1534 1484 1483 1533 2927 2903 2902 2926}
set elemKinit(10585) 3.773200081582705e-06
set sigmaV0(10585) 182.175000
set ruPrev(10585) 0.0

# Element 10586: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10586) {2927 2903 2902 2926 2931 2907 2906 2930}
set elemKinit(10586) 3.773200081582705e-06
set sigmaV0(10586) 182.175000
set ruPrev(10586) 0.0

# Element 10587: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10587) {2931 2907 2906 2930 1538 1488 1487 1537}
set elemKinit(10587) 3.773200081582705e-06
set sigmaV0(10587) 182.175000
set ruPrev(10587) 0.0

# Element 10588: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10588) {199 188 1484 1534 1198 1159 2903 2927}
set elemKinit(10588) 3.773200081582705e-06
set sigmaV0(10588) 171.765000
set ruPrev(10588) 0.0

# Element 10589: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10589) {1198 1159 2903 2927 1199 1160 2907 2931}
set elemKinit(10589) 3.773200081582705e-06
set sigmaV0(10589) 171.765000
set ruPrev(10589) 0.0

# Element 10590: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10590) {1199 1160 2907 2931 200 189 1488 1538}
set elemKinit(10590) 3.773200081582705e-06
set sigmaV0(10590) 171.765000
set ruPrev(10590) 0.0

# Element 10591: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10591) {1535 1485 266 277 1541 1491 267 278}
set elemKinit(10591) 3.773200081582705e-06
set sigmaV0(10591) 213.405000
set ruPrev(10591) 0.0

# Element 10592: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10592) {1536 1486 1485 1535 1542 1492 1491 1541}
set elemKinit(10592) 3.773200081582705e-06
set sigmaV0(10592) 202.995000
set ruPrev(10592) 0.0

# Element 10593: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10593) {1537 1487 1486 1536 1543 1493 1492 1542}
set elemKinit(10593) 3.773200081582705e-06
set sigmaV0(10593) 192.585000
set ruPrev(10593) 0.0

# Element 10594: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10594) {1538 1488 1487 1537 1544 1494 1493 1543}
set elemKinit(10594) 3.773200081582705e-06
set sigmaV0(10594) 182.175000
set ruPrev(10594) 0.0

# Element 10595: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10595) {200 189 1488 1538 201 190 1494 1544}
set elemKinit(10595) 3.773200081582705e-06
set sigmaV0(10595) 171.765000
set ruPrev(10595) 0.0

# Element 10596: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10596) {1541 1491 267 278 2932 2908 1499 1549}
set elemKinit(10596) 3.773200081582705e-06
set sigmaV0(10596) 213.405000
set ruPrev(10596) 0.0

# Element 10597: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10597) {2932 2908 1499 1549 1545 1495 268 279}
set elemKinit(10597) 3.773200081582705e-06
set sigmaV0(10597) 213.405000
set ruPrev(10597) 0.0

# Element 10598: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10598) {1542 1492 1491 1541 2933 2909 2908 2932}
set elemKinit(10598) 3.773200081582705e-06
set sigmaV0(10598) 202.995000
set ruPrev(10598) 0.0

# Element 10599: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10599) {2933 2909 2908 2932 1546 1496 1495 1545}
set elemKinit(10599) 3.773200081582705e-06
set sigmaV0(10599) 202.995000
set ruPrev(10599) 0.0

# Element 10600: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10600) {1543 1493 1492 1542 2934 2910 2909 2933}
set elemKinit(10600) 3.773200081582705e-06
set sigmaV0(10600) 192.585000
set ruPrev(10600) 0.0

# Element 10601: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10601) {2934 2910 2909 2933 1547 1497 1496 1546}
set elemKinit(10601) 3.773200081582705e-06
set sigmaV0(10601) 192.585000
set ruPrev(10601) 0.0

# Element 10602: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10602) {1544 1494 1493 1543 2935 2911 2910 2934}
set elemKinit(10602) 3.773200081582705e-06
set sigmaV0(10602) 182.175000
set ruPrev(10602) 0.0

# Element 10603: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10603) {2935 2911 2910 2934 1548 1498 1497 1547}
set elemKinit(10603) 3.773200081582705e-06
set sigmaV0(10603) 182.175000
set ruPrev(10603) 0.0

# Element 10604: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10604) {201 190 1494 1544 1206 1167 2911 2935}
set elemKinit(10604) 3.773200081582705e-06
set sigmaV0(10604) 171.765000
set ruPrev(10604) 0.0

# Element 10605: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10605) {1206 1167 2911 2935 202 191 1498 1548}
set elemKinit(10605) 3.773200081582705e-06
set sigmaV0(10605) 171.765000
set ruPrev(10605) 0.0

# Element 10606: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10606) {1545 1495 268 279 1550 1500 269 280}
set elemKinit(10606) 3.773200081582705e-06
set sigmaV0(10606) 213.405000
set ruPrev(10606) 0.0

# Element 10607: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10607) {1546 1496 1495 1545 1551 1501 1500 1550}
set elemKinit(10607) 3.773200081582705e-06
set sigmaV0(10607) 202.995000
set ruPrev(10607) 0.0

# Element 10608: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10608) {1547 1497 1496 1546 1552 1502 1501 1551}
set elemKinit(10608) 3.773200081582705e-06
set sigmaV0(10608) 192.585000
set ruPrev(10608) 0.0

# Element 10609: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10609) {1548 1498 1497 1547 1553 1503 1502 1552}
set elemKinit(10609) 3.773200081582705e-06
set sigmaV0(10609) 182.175000
set ruPrev(10609) 0.0

# Element 10610: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10610) {202 191 1498 1548 203 192 1503 1553}
set elemKinit(10610) 3.773200081582705e-06
set sigmaV0(10610) 171.765000
set ruPrev(10610) 0.0

# Element 10611: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10611) {1550 1500 269 280 1554 1504 270 281}
set elemKinit(10611) 3.773200081582705e-06
set sigmaV0(10611) 213.405000
set ruPrev(10611) 0.0

# Element 10612: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10612) {1551 1501 1500 1550 1555 1505 1504 1554}
set elemKinit(10612) 3.773200081582705e-06
set sigmaV0(10612) 202.995000
set ruPrev(10612) 0.0

# Element 10613: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10613) {1552 1502 1501 1551 1556 1506 1505 1555}
set elemKinit(10613) 3.773200081582705e-06
set sigmaV0(10613) 192.585000
set ruPrev(10613) 0.0

# Element 10614: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10614) {1553 1503 1502 1552 1557 1507 1506 1556}
set elemKinit(10614) 3.773200081582705e-06
set sigmaV0(10614) 182.175000
set ruPrev(10614) 0.0

# Element 10615: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10615) {203 192 1503 1553 204 193 1507 1557}
set elemKinit(10615) 3.773200081582705e-06
set sigmaV0(10615) 171.765000
set ruPrev(10615) 0.0

# Element 10616: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10616) {1554 1504 270 281 1558 1508 271 282}
set elemKinit(10616) 3.773200081582705e-06
set sigmaV0(10616) 213.405000
set ruPrev(10616) 0.0

# Element 10617: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10617) {1555 1505 1504 1554 1559 1509 1508 1558}
set elemKinit(10617) 3.773200081582705e-06
set sigmaV0(10617) 202.995000
set ruPrev(10617) 0.0

# Element 10618: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10618) {1556 1506 1505 1555 1560 1510 1509 1559}
set elemKinit(10618) 3.773200081582705e-06
set sigmaV0(10618) 192.585000
set ruPrev(10618) 0.0

# Element 10619: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10619) {1557 1507 1506 1556 1561 1511 1510 1560}
set elemKinit(10619) 3.773200081582705e-06
set sigmaV0(10619) 182.175000
set ruPrev(10619) 0.0

# Element 10620: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10620) {204 193 1507 1557 205 194 1511 1561}
set elemKinit(10620) 3.773200081582705e-06
set sigmaV0(10620) 171.765000
set ruPrev(10620) 0.0

# Element 10621: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10621) {1558 1508 271 282 1562 1512 272 283}
set elemKinit(10621) 3.773200081582705e-06
set sigmaV0(10621) 213.405000
set ruPrev(10621) 0.0

# Element 10622: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10622) {1559 1509 1508 1558 1563 1513 1512 1562}
set elemKinit(10622) 3.773200081582705e-06
set sigmaV0(10622) 202.995000
set ruPrev(10622) 0.0

# Element 10623: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10623) {1560 1510 1509 1559 1564 1514 1513 1563}
set elemKinit(10623) 3.773200081582705e-06
set sigmaV0(10623) 192.585000
set ruPrev(10623) 0.0

# Element 10624: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10624) {1561 1511 1510 1560 1565 1515 1514 1564}
set elemKinit(10624) 3.773200081582705e-06
set sigmaV0(10624) 182.175000
set ruPrev(10624) 0.0

# Element 10625: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10625) {205 194 1511 1561 206 195 1515 1565}
set elemKinit(10625) 3.773200081582705e-06
set sigmaV0(10625) 171.765000
set ruPrev(10625) 0.0

# Element 10626: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10626) {1562 1512 272 283 2936 2912 1520 1570}
set elemKinit(10626) 3.773200081582705e-06
set sigmaV0(10626) 213.405000
set ruPrev(10626) 0.0

# Element 10627: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10627) {2936 2912 1520 1570 1566 1516 273 284}
set elemKinit(10627) 3.773200081582705e-06
set sigmaV0(10627) 213.405000
set ruPrev(10627) 0.0

# Element 10628: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10628) {1563 1513 1512 1562 2937 2913 2912 2936}
set elemKinit(10628) 3.773200081582705e-06
set sigmaV0(10628) 202.995000
set ruPrev(10628) 0.0

# Element 10629: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10629) {2937 2913 2912 2936 1567 1517 1516 1566}
set elemKinit(10629) 3.773200081582705e-06
set sigmaV0(10629) 202.995000
set ruPrev(10629) 0.0

# Element 10630: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10630) {1564 1514 1513 1563 2938 2914 2913 2937}
set elemKinit(10630) 3.773200081582705e-06
set sigmaV0(10630) 192.585000
set ruPrev(10630) 0.0

# Element 10631: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10631) {2938 2914 2913 2937 1568 1518 1517 1567}
set elemKinit(10631) 3.773200081582705e-06
set sigmaV0(10631) 192.585000
set ruPrev(10631) 0.0

# Element 10632: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10632) {1565 1515 1514 1564 2939 2915 2914 2938}
set elemKinit(10632) 3.773200081582705e-06
set sigmaV0(10632) 182.175000
set ruPrev(10632) 0.0

# Element 10633: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10633) {2939 2915 2914 2938 1569 1519 1518 1568}
set elemKinit(10633) 3.773200081582705e-06
set sigmaV0(10633) 182.175000
set ruPrev(10633) 0.0

# Element 10634: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10634) {206 195 1515 1565 1222 1183 2915 2939}
set elemKinit(10634) 3.773200081582705e-06
set sigmaV0(10634) 171.765000
set ruPrev(10634) 0.0

# Element 10635: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10635) {1222 1183 2915 2939 207 196 1519 1569}
set elemKinit(10635) 3.773200081582705e-06
set sigmaV0(10635) 171.765000
set ruPrev(10635) 0.0

# Element 10636: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10636) {1566 1516 273 284 1571 1521 274 285}
set elemKinit(10636) 3.773200081582705e-06
set sigmaV0(10636) 213.405000
set ruPrev(10636) 0.0

# Element 10637: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10637) {1567 1517 1516 1566 1572 1522 1521 1571}
set elemKinit(10637) 3.773200081582705e-06
set sigmaV0(10637) 202.995000
set ruPrev(10637) 0.0

# Element 10638: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10638) {1568 1518 1517 1567 1573 1523 1522 1572}
set elemKinit(10638) 3.773200081582705e-06
set sigmaV0(10638) 192.585000
set ruPrev(10638) 0.0

# Element 10639: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10639) {1569 1519 1518 1568 1574 1524 1523 1573}
set elemKinit(10639) 3.773200081582705e-06
set sigmaV0(10639) 182.175000
set ruPrev(10639) 0.0

# Element 10640: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10640) {207 196 1519 1569 208 197 1524 1574}
set elemKinit(10640) 3.773200081582705e-06
set sigmaV0(10640) 171.765000
set ruPrev(10640) 0.0

# Element 10641: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10641) {1571 1521 274 285 2940 2916 1529 1579}
set elemKinit(10641) 3.773200081582705e-06
set sigmaV0(10641) 213.405000
set ruPrev(10641) 0.0

# Element 10642: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10642) {2940 2916 1529 1579 2944 2920 1530 1580}
set elemKinit(10642) 3.773200081582705e-06
set sigmaV0(10642) 213.405000
set ruPrev(10642) 0.0

# Element 10643: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10643) {2944 2920 1530 1580 1575 1525 275 286}
set elemKinit(10643) 3.773200081582705e-06
set sigmaV0(10643) 213.405000
set ruPrev(10643) 0.0

# Element 10644: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10644) {1572 1522 1521 1571 2941 2917 2916 2940}
set elemKinit(10644) 3.773200081582705e-06
set sigmaV0(10644) 202.995000
set ruPrev(10644) 0.0

# Element 10645: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10645) {2941 2917 2916 2940 2945 2921 2920 2944}
set elemKinit(10645) 3.773200081582705e-06
set sigmaV0(10645) 202.995000
set ruPrev(10645) 0.0

# Element 10646: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10646) {2945 2921 2920 2944 1576 1526 1525 1575}
set elemKinit(10646) 3.773200081582705e-06
set sigmaV0(10646) 202.995000
set ruPrev(10646) 0.0

# Element 10647: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10647) {1573 1523 1522 1572 2942 2918 2917 2941}
set elemKinit(10647) 3.773200081582705e-06
set sigmaV0(10647) 192.585000
set ruPrev(10647) 0.0

# Element 10648: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10648) {2942 2918 2917 2941 2946 2922 2921 2945}
set elemKinit(10648) 3.773200081582705e-06
set sigmaV0(10648) 192.585000
set ruPrev(10648) 0.0

# Element 10649: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10649) {2946 2922 2921 2945 1577 1527 1526 1576}
set elemKinit(10649) 3.773200081582705e-06
set sigmaV0(10649) 192.585000
set ruPrev(10649) 0.0

# Element 10650: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10650) {1574 1524 1523 1573 2943 2919 2918 2942}
set elemKinit(10650) 3.773200081582705e-06
set sigmaV0(10650) 182.175000
set ruPrev(10650) 0.0

# Element 10651: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10651) {2943 2919 2918 2942 2947 2923 2922 2946}
set elemKinit(10651) 3.773200081582705e-06
set sigmaV0(10651) 182.175000
set ruPrev(10651) 0.0

# Element 10652: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10652) {2947 2923 2922 2946 1578 1528 1527 1577}
set elemKinit(10652) 3.773200081582705e-06
set sigmaV0(10652) 182.175000
set ruPrev(10652) 0.0

# Element 10653: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10653) {208 197 1524 1574 1229 1190 2919 2943}
set elemKinit(10653) 3.773200081582705e-06
set sigmaV0(10653) 171.765000
set ruPrev(10653) 0.0

# Element 10654: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10654) {1229 1190 2919 2943 1230 1191 2923 2947}
set elemKinit(10654) 3.773200081582705e-06
set sigmaV0(10654) 171.765000
set ruPrev(10654) 0.0

# Element 10655: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10655) {1230 1191 2923 2947 209 198 1528 1578}
set elemKinit(10655) 3.773200081582705e-06
set sigmaV0(10655) 171.765000
set ruPrev(10655) 0.0

# Element 10656: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10656) {1581 1531 276 287 2948 2924 1539 1589}
set elemKinit(10656) 3.773200081582705e-06
set sigmaV0(10656) 213.405000
set ruPrev(10656) 0.0

# Element 10657: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10657) {2948 2924 1539 1589 2952 2928 1540 1590}
set elemKinit(10657) 3.773200081582705e-06
set sigmaV0(10657) 213.405000
set ruPrev(10657) 0.0

# Element 10658: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10658) {2952 2928 1540 1590 1585 1535 277 288}
set elemKinit(10658) 3.773200081582705e-06
set sigmaV0(10658) 213.405000
set ruPrev(10658) 0.0

# Element 10659: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10659) {1582 1532 1531 1581 2949 2925 2924 2948}
set elemKinit(10659) 3.773200081582705e-06
set sigmaV0(10659) 202.995000
set ruPrev(10659) 0.0

# Element 10660: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10660) {2949 2925 2924 2948 2953 2929 2928 2952}
set elemKinit(10660) 3.773200081582705e-06
set sigmaV0(10660) 202.995000
set ruPrev(10660) 0.0

# Element 10661: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10661) {2953 2929 2928 2952 1586 1536 1535 1585}
set elemKinit(10661) 3.773200081582705e-06
set sigmaV0(10661) 202.995000
set ruPrev(10661) 0.0

# Element 10662: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10662) {1583 1533 1532 1582 2950 2926 2925 2949}
set elemKinit(10662) 3.773200081582705e-06
set sigmaV0(10662) 192.585000
set ruPrev(10662) 0.0

# Element 10663: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10663) {2950 2926 2925 2949 2954 2930 2929 2953}
set elemKinit(10663) 3.773200081582705e-06
set sigmaV0(10663) 192.585000
set ruPrev(10663) 0.0

# Element 10664: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10664) {2954 2930 2929 2953 1587 1537 1536 1586}
set elemKinit(10664) 3.773200081582705e-06
set sigmaV0(10664) 192.585000
set ruPrev(10664) 0.0

# Element 10665: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10665) {1584 1534 1533 1583 2951 2927 2926 2950}
set elemKinit(10665) 3.773200081582705e-06
set sigmaV0(10665) 182.175000
set ruPrev(10665) 0.0

# Element 10666: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10666) {2951 2927 2926 2950 2955 2931 2930 2954}
set elemKinit(10666) 3.773200081582705e-06
set sigmaV0(10666) 182.175000
set ruPrev(10666) 0.0

# Element 10667: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10667) {2955 2931 2930 2954 1588 1538 1537 1587}
set elemKinit(10667) 3.773200081582705e-06
set sigmaV0(10667) 182.175000
set ruPrev(10667) 0.0

# Element 10668: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10668) {210 199 1534 1584 1237 1198 2927 2951}
set elemKinit(10668) 3.773200081582705e-06
set sigmaV0(10668) 171.765000
set ruPrev(10668) 0.0

# Element 10669: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10669) {1237 1198 2927 2951 1238 1199 2931 2955}
set elemKinit(10669) 3.773200081582705e-06
set sigmaV0(10669) 171.765000
set ruPrev(10669) 0.0

# Element 10670: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10670) {1238 1199 2931 2955 211 200 1538 1588}
set elemKinit(10670) 3.773200081582705e-06
set sigmaV0(10670) 171.765000
set ruPrev(10670) 0.0

# Element 10671: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10671) {1585 1535 277 288 1591 1541 278 289}
set elemKinit(10671) 3.773200081582705e-06
set sigmaV0(10671) 213.405000
set ruPrev(10671) 0.0

# Element 10672: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10672) {1586 1536 1535 1585 1592 1542 1541 1591}
set elemKinit(10672) 3.773200081582705e-06
set sigmaV0(10672) 202.995000
set ruPrev(10672) 0.0

# Element 10673: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10673) {1587 1537 1536 1586 1593 1543 1542 1592}
set elemKinit(10673) 3.773200081582705e-06
set sigmaV0(10673) 192.585000
set ruPrev(10673) 0.0

# Element 10674: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10674) {1588 1538 1537 1587 1594 1544 1543 1593}
set elemKinit(10674) 3.773200081582705e-06
set sigmaV0(10674) 182.175000
set ruPrev(10674) 0.0

# Element 10675: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10675) {211 200 1538 1588 212 201 1544 1594}
set elemKinit(10675) 3.773200081582705e-06
set sigmaV0(10675) 171.765000
set ruPrev(10675) 0.0

# Element 10676: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10676) {1591 1541 278 289 2956 2932 1549 1599}
set elemKinit(10676) 3.773200081582705e-06
set sigmaV0(10676) 213.405000
set ruPrev(10676) 0.0

# Element 10677: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10677) {2956 2932 1549 1599 1595 1545 279 290}
set elemKinit(10677) 3.773200081582705e-06
set sigmaV0(10677) 213.405000
set ruPrev(10677) 0.0

# Element 10678: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10678) {1592 1542 1541 1591 2957 2933 2932 2956}
set elemKinit(10678) 3.773200081582705e-06
set sigmaV0(10678) 202.995000
set ruPrev(10678) 0.0

# Element 10679: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10679) {2957 2933 2932 2956 1596 1546 1545 1595}
set elemKinit(10679) 3.773200081582705e-06
set sigmaV0(10679) 202.995000
set ruPrev(10679) 0.0

# Element 10680: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10680) {1593 1543 1542 1592 2958 2934 2933 2957}
set elemKinit(10680) 3.773200081582705e-06
set sigmaV0(10680) 192.585000
set ruPrev(10680) 0.0

# Element 10681: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10681) {2958 2934 2933 2957 1597 1547 1546 1596}
set elemKinit(10681) 3.773200081582705e-06
set sigmaV0(10681) 192.585000
set ruPrev(10681) 0.0

# Element 10682: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10682) {1594 1544 1543 1593 2959 2935 2934 2958}
set elemKinit(10682) 3.773200081582705e-06
set sigmaV0(10682) 182.175000
set ruPrev(10682) 0.0

# Element 10683: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10683) {2959 2935 2934 2958 1598 1548 1547 1597}
set elemKinit(10683) 3.773200081582705e-06
set sigmaV0(10683) 182.175000
set ruPrev(10683) 0.0

# Element 10684: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10684) {212 201 1544 1594 1245 1206 2935 2959}
set elemKinit(10684) 3.773200081582705e-06
set sigmaV0(10684) 171.765000
set ruPrev(10684) 0.0

# Element 10685: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10685) {1245 1206 2935 2959 213 202 1548 1598}
set elemKinit(10685) 3.773200081582705e-06
set sigmaV0(10685) 171.765000
set ruPrev(10685) 0.0

# Element 10686: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10686) {1595 1545 279 290 1600 1550 280 291}
set elemKinit(10686) 3.773200081582705e-06
set sigmaV0(10686) 213.405000
set ruPrev(10686) 0.0

# Element 10687: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10687) {1596 1546 1545 1595 1601 1551 1550 1600}
set elemKinit(10687) 3.773200081582705e-06
set sigmaV0(10687) 202.995000
set ruPrev(10687) 0.0

# Element 10688: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10688) {1597 1547 1546 1596 1602 1552 1551 1601}
set elemKinit(10688) 3.773200081582705e-06
set sigmaV0(10688) 192.585000
set ruPrev(10688) 0.0

# Element 10689: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10689) {1598 1548 1547 1597 1603 1553 1552 1602}
set elemKinit(10689) 3.773200081582705e-06
set sigmaV0(10689) 182.175000
set ruPrev(10689) 0.0

# Element 10690: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10690) {213 202 1548 1598 214 203 1553 1603}
set elemKinit(10690) 3.773200081582705e-06
set sigmaV0(10690) 171.765000
set ruPrev(10690) 0.0

# Element 10691: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10691) {1600 1550 280 291 1604 1554 281 292}
set elemKinit(10691) 3.773200081582705e-06
set sigmaV0(10691) 213.405000
set ruPrev(10691) 0.0

# Element 10692: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10692) {1601 1551 1550 1600 1605 1555 1554 1604}
set elemKinit(10692) 3.773200081582705e-06
set sigmaV0(10692) 202.995000
set ruPrev(10692) 0.0

# Element 10693: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10693) {1602 1552 1551 1601 1606 1556 1555 1605}
set elemKinit(10693) 3.773200081582705e-06
set sigmaV0(10693) 192.585000
set ruPrev(10693) 0.0

# Element 10694: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10694) {1603 1553 1552 1602 1607 1557 1556 1606}
set elemKinit(10694) 3.773200081582705e-06
set sigmaV0(10694) 182.175000
set ruPrev(10694) 0.0

# Element 10695: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10695) {214 203 1553 1603 215 204 1557 1607}
set elemKinit(10695) 3.773200081582705e-06
set sigmaV0(10695) 171.765000
set ruPrev(10695) 0.0

# Element 10696: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10696) {1604 1554 281 292 1608 1558 282 293}
set elemKinit(10696) 3.773200081582705e-06
set sigmaV0(10696) 213.405000
set ruPrev(10696) 0.0

# Element 10697: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10697) {1605 1555 1554 1604 1609 1559 1558 1608}
set elemKinit(10697) 3.773200081582705e-06
set sigmaV0(10697) 202.995000
set ruPrev(10697) 0.0

# Element 10698: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10698) {1606 1556 1555 1605 1610 1560 1559 1609}
set elemKinit(10698) 3.773200081582705e-06
set sigmaV0(10698) 192.585000
set ruPrev(10698) 0.0

# Element 10699: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10699) {1607 1557 1556 1606 1611 1561 1560 1610}
set elemKinit(10699) 3.773200081582705e-06
set sigmaV0(10699) 182.175000
set ruPrev(10699) 0.0

# Element 10700: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10700) {215 204 1557 1607 216 205 1561 1611}
set elemKinit(10700) 3.773200081582705e-06
set sigmaV0(10700) 171.765000
set ruPrev(10700) 0.0

# Element 10701: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10701) {1608 1558 282 293 1612 1562 283 294}
set elemKinit(10701) 3.773200081582705e-06
set sigmaV0(10701) 213.405000
set ruPrev(10701) 0.0

# Element 10702: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10702) {1609 1559 1558 1608 1613 1563 1562 1612}
set elemKinit(10702) 3.773200081582705e-06
set sigmaV0(10702) 202.995000
set ruPrev(10702) 0.0

# Element 10703: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10703) {1610 1560 1559 1609 1614 1564 1563 1613}
set elemKinit(10703) 3.773200081582705e-06
set sigmaV0(10703) 192.585000
set ruPrev(10703) 0.0

# Element 10704: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10704) {1611 1561 1560 1610 1615 1565 1564 1614}
set elemKinit(10704) 3.773200081582705e-06
set sigmaV0(10704) 182.175000
set ruPrev(10704) 0.0

# Element 10705: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10705) {216 205 1561 1611 217 206 1565 1615}
set elemKinit(10705) 3.773200081582705e-06
set sigmaV0(10705) 171.765000
set ruPrev(10705) 0.0

# Element 10706: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10706) {1612 1562 283 294 2960 2936 1570 1620}
set elemKinit(10706) 3.773200081582705e-06
set sigmaV0(10706) 213.405000
set ruPrev(10706) 0.0

# Element 10707: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10707) {2960 2936 1570 1620 1616 1566 284 295}
set elemKinit(10707) 3.773200081582705e-06
set sigmaV0(10707) 213.405000
set ruPrev(10707) 0.0

# Element 10708: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10708) {1613 1563 1562 1612 2961 2937 2936 2960}
set elemKinit(10708) 3.773200081582705e-06
set sigmaV0(10708) 202.995000
set ruPrev(10708) 0.0

# Element 10709: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10709) {2961 2937 2936 2960 1617 1567 1566 1616}
set elemKinit(10709) 3.773200081582705e-06
set sigmaV0(10709) 202.995000
set ruPrev(10709) 0.0

# Element 10710: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10710) {1614 1564 1563 1613 2962 2938 2937 2961}
set elemKinit(10710) 3.773200081582705e-06
set sigmaV0(10710) 192.585000
set ruPrev(10710) 0.0

# Element 10711: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10711) {2962 2938 2937 2961 1618 1568 1567 1617}
set elemKinit(10711) 3.773200081582705e-06
set sigmaV0(10711) 192.585000
set ruPrev(10711) 0.0

# Element 10712: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10712) {1615 1565 1564 1614 2963 2939 2938 2962}
set elemKinit(10712) 3.773200081582705e-06
set sigmaV0(10712) 182.175000
set ruPrev(10712) 0.0

# Element 10713: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10713) {2963 2939 2938 2962 1619 1569 1568 1618}
set elemKinit(10713) 3.773200081582705e-06
set sigmaV0(10713) 182.175000
set ruPrev(10713) 0.0

# Element 10714: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10714) {217 206 1565 1615 1261 1222 2939 2963}
set elemKinit(10714) 3.773200081582705e-06
set sigmaV0(10714) 171.765000
set ruPrev(10714) 0.0

# Element 10715: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10715) {1261 1222 2939 2963 218 207 1569 1619}
set elemKinit(10715) 3.773200081582705e-06
set sigmaV0(10715) 171.765000
set ruPrev(10715) 0.0

# Element 10716: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10716) {1616 1566 284 295 1621 1571 285 296}
set elemKinit(10716) 3.773200081582705e-06
set sigmaV0(10716) 213.405000
set ruPrev(10716) 0.0

# Element 10717: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10717) {1617 1567 1566 1616 1622 1572 1571 1621}
set elemKinit(10717) 3.773200081582705e-06
set sigmaV0(10717) 202.995000
set ruPrev(10717) 0.0

# Element 10718: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10718) {1618 1568 1567 1617 1623 1573 1572 1622}
set elemKinit(10718) 3.773200081582705e-06
set sigmaV0(10718) 192.585000
set ruPrev(10718) 0.0

# Element 10719: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10719) {1619 1569 1568 1618 1624 1574 1573 1623}
set elemKinit(10719) 3.773200081582705e-06
set sigmaV0(10719) 182.175000
set ruPrev(10719) 0.0

# Element 10720: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10720) {218 207 1569 1619 219 208 1574 1624}
set elemKinit(10720) 3.773200081582705e-06
set sigmaV0(10720) 171.765000
set ruPrev(10720) 0.0

# Element 10721: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10721) {1621 1571 285 296 2964 2940 1579 1629}
set elemKinit(10721) 3.773200081582705e-06
set sigmaV0(10721) 213.405000
set ruPrev(10721) 0.0

# Element 10722: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10722) {2964 2940 1579 1629 2968 2944 1580 1630}
set elemKinit(10722) 3.773200081582705e-06
set sigmaV0(10722) 213.405000
set ruPrev(10722) 0.0

# Element 10723: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10723) {2968 2944 1580 1630 1625 1575 286 297}
set elemKinit(10723) 3.773200081582705e-06
set sigmaV0(10723) 213.405000
set ruPrev(10723) 0.0

# Element 10724: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10724) {1622 1572 1571 1621 2965 2941 2940 2964}
set elemKinit(10724) 3.773200081582705e-06
set sigmaV0(10724) 202.995000
set ruPrev(10724) 0.0

# Element 10725: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10725) {2965 2941 2940 2964 2969 2945 2944 2968}
set elemKinit(10725) 3.773200081582705e-06
set sigmaV0(10725) 202.995000
set ruPrev(10725) 0.0

# Element 10726: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10726) {2969 2945 2944 2968 1626 1576 1575 1625}
set elemKinit(10726) 3.773200081582705e-06
set sigmaV0(10726) 202.995000
set ruPrev(10726) 0.0

# Element 10727: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10727) {1623 1573 1572 1622 2966 2942 2941 2965}
set elemKinit(10727) 3.773200081582705e-06
set sigmaV0(10727) 192.585000
set ruPrev(10727) 0.0

# Element 10728: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10728) {2966 2942 2941 2965 2970 2946 2945 2969}
set elemKinit(10728) 3.773200081582705e-06
set sigmaV0(10728) 192.585000
set ruPrev(10728) 0.0

# Element 10729: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10729) {2970 2946 2945 2969 1627 1577 1576 1626}
set elemKinit(10729) 3.773200081582705e-06
set sigmaV0(10729) 192.585000
set ruPrev(10729) 0.0

# Element 10730: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10730) {1624 1574 1573 1623 2967 2943 2942 2966}
set elemKinit(10730) 3.773200081582705e-06
set sigmaV0(10730) 182.175000
set ruPrev(10730) 0.0

# Element 10731: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10731) {2967 2943 2942 2966 2971 2947 2946 2970}
set elemKinit(10731) 3.773200081582705e-06
set sigmaV0(10731) 182.175000
set ruPrev(10731) 0.0

# Element 10732: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10732) {2971 2947 2946 2970 1628 1578 1577 1627}
set elemKinit(10732) 3.773200081582705e-06
set sigmaV0(10732) 182.175000
set ruPrev(10732) 0.0

# Element 10733: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10733) {219 208 1574 1624 1268 1229 2943 2967}
set elemKinit(10733) 3.773200081582705e-06
set sigmaV0(10733) 171.765000
set ruPrev(10733) 0.0

# Element 10734: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10734) {1268 1229 2943 2967 1269 1230 2947 2971}
set elemKinit(10734) 3.773200081582705e-06
set sigmaV0(10734) 171.765000
set ruPrev(10734) 0.0

# Element 10735: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10735) {1269 1230 2947 2971 220 209 1578 1628}
set elemKinit(10735) 3.773200081582705e-06
set sigmaV0(10735) 171.765000
set ruPrev(10735) 0.0

# Element 10736: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10736) {2972 1581 287 1635 3342 2948 1589 2988}
set elemKinit(10736) 3.773200081582705e-06
set sigmaV0(10736) 213.405000
set ruPrev(10736) 0.0

# Element 10737: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10737) {3342 2948 1589 2988 3343 2952 1590 2989}
set elemKinit(10737) 3.773200081582705e-06
set sigmaV0(10737) 213.405000
set ruPrev(10737) 0.0

# Element 10738: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10738) {3343 2952 1590 2989 2976 1585 288 1640}
set elemKinit(10738) 3.773200081582705e-06
set sigmaV0(10738) 213.405000
set ruPrev(10738) 0.0

# Element 10739: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10739) {1631 2972 1635 298 2980 3342 2988 1641}
set elemKinit(10739) 3.773200081582705e-06
set sigmaV0(10739) 213.405000
set ruPrev(10739) 0.0

# Element 10740: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10740) {2980 3342 2988 1641 2984 3343 2989 1642}
set elemKinit(10740) 3.773200081582705e-06
set sigmaV0(10740) 213.405000
set ruPrev(10740) 0.0

# Element 10741: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10741) {2984 3343 2989 1642 1636 2976 1640 299}
set elemKinit(10741) 3.773200081582705e-06
set sigmaV0(10741) 213.405000
set ruPrev(10741) 0.0

# Element 10742: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10742) {2973 1582 1581 2972 3344 2949 2948 3342}
set elemKinit(10742) 3.773200081582705e-06
set sigmaV0(10742) 202.995000
set ruPrev(10742) 0.0

# Element 10743: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10743) {3344 2949 2948 3342 3345 2953 2952 3343}
set elemKinit(10743) 3.773200081582705e-06
set sigmaV0(10743) 202.995000
set ruPrev(10743) 0.0

# Element 10744: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10744) {3345 2953 2952 3343 2977 1586 1585 2976}
set elemKinit(10744) 3.773200081582705e-06
set sigmaV0(10744) 202.995000
set ruPrev(10744) 0.0

# Element 10745: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10745) {1632 2973 2972 1631 2981 3344 3342 2980}
set elemKinit(10745) 3.773200081582705e-06
set sigmaV0(10745) 202.995000
set ruPrev(10745) 0.0

# Element 10746: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10746) {2981 3344 3342 2980 2985 3345 3343 2984}
set elemKinit(10746) 3.773200081582705e-06
set sigmaV0(10746) 202.995000
set ruPrev(10746) 0.0

# Element 10747: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10747) {2985 3345 3343 2984 1637 2977 2976 1636}
set elemKinit(10747) 3.773200081582705e-06
set sigmaV0(10747) 202.995000
set ruPrev(10747) 0.0

# Element 10748: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10748) {2974 1583 1582 2973 3346 2950 2949 3344}
set elemKinit(10748) 3.773200081582705e-06
set sigmaV0(10748) 192.585000
set ruPrev(10748) 0.0

# Element 10749: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10749) {3346 2950 2949 3344 3347 2954 2953 3345}
set elemKinit(10749) 3.773200081582705e-06
set sigmaV0(10749) 192.585000
set ruPrev(10749) 0.0

# Element 10750: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10750) {3347 2954 2953 3345 2978 1587 1586 2977}
set elemKinit(10750) 3.773200081582705e-06
set sigmaV0(10750) 192.585000
set ruPrev(10750) 0.0

# Element 10751: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10751) {1633 2974 2973 1632 2982 3346 3344 2981}
set elemKinit(10751) 3.773200081582705e-06
set sigmaV0(10751) 192.585000
set ruPrev(10751) 0.0

# Element 10752: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10752) {2982 3346 3344 2981 2986 3347 3345 2985}
set elemKinit(10752) 3.773200081582705e-06
set sigmaV0(10752) 192.585000
set ruPrev(10752) 0.0

# Element 10753: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10753) {2986 3347 3345 2985 1638 2978 2977 1637}
set elemKinit(10753) 3.773200081582705e-06
set sigmaV0(10753) 192.585000
set ruPrev(10753) 0.0

# Element 10754: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10754) {2975 1584 1583 2974 3348 2951 2950 3346}
set elemKinit(10754) 3.773200081582705e-06
set sigmaV0(10754) 182.175000
set ruPrev(10754) 0.0

# Element 10755: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10755) {3348 2951 2950 3346 3349 2955 2954 3347}
set elemKinit(10755) 3.773200081582705e-06
set sigmaV0(10755) 182.175000
set ruPrev(10755) 0.0

# Element 10756: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10756) {3349 2955 2954 3347 2979 1588 1587 2978}
set elemKinit(10756) 3.773200081582705e-06
set sigmaV0(10756) 182.175000
set ruPrev(10756) 0.0

# Element 10757: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10757) {1634 2975 2974 1633 2983 3348 3346 2982}
set elemKinit(10757) 3.773200081582705e-06
set sigmaV0(10757) 182.175000
set ruPrev(10757) 0.0

# Element 10758: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10758) {2983 3348 3346 2982 2987 3349 3347 2986}
set elemKinit(10758) 3.773200081582705e-06
set sigmaV0(10758) 182.175000
set ruPrev(10758) 0.0

# Element 10759: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10759) {2987 3349 3347 2986 1639 2979 2978 1638}
set elemKinit(10759) 3.773200081582705e-06
set sigmaV0(10759) 182.175000
set ruPrev(10759) 0.0

# Element 10760: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10760) {1273 210 1584 2975 2733 1237 2951 3348}
set elemKinit(10760) 3.773200081582705e-06
set sigmaV0(10760) 171.765000
set ruPrev(10760) 0.0

# Element 10761: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10761) {2733 1237 2951 3348 2734 1238 2955 3349}
set elemKinit(10761) 3.773200081582705e-06
set sigmaV0(10761) 171.765000
set ruPrev(10761) 0.0

# Element 10762: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10762) {2734 1238 2955 3349 1277 211 1588 2979}
set elemKinit(10762) 3.773200081582705e-06
set sigmaV0(10762) 171.765000
set ruPrev(10762) 0.0

# Element 10763: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10763) {221 1273 2975 1634 1278 2733 3348 2983}
set elemKinit(10763) 3.773200081582705e-06
set sigmaV0(10763) 171.765000
set ruPrev(10763) 0.0

# Element 10764: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10764) {1278 2733 3348 2983 1279 2734 3349 2987}
set elemKinit(10764) 3.773200081582705e-06
set sigmaV0(10764) 171.765000
set ruPrev(10764) 0.0

# Element 10765: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10765) {1279 2734 3349 2987 222 1277 2979 1639}
set elemKinit(10765) 3.773200081582705e-06
set sigmaV0(10765) 171.765000
set ruPrev(10765) 0.0

# Element 10766: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10766) {2976 1585 288 1640 2990 1591 289 1647}
set elemKinit(10766) 3.773200081582705e-06
set sigmaV0(10766) 213.405000
set ruPrev(10766) 0.0

# Element 10767: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10767) {1636 2976 1640 299 1643 2990 1647 300}
set elemKinit(10767) 3.773200081582705e-06
set sigmaV0(10767) 213.405000
set ruPrev(10767) 0.0

# Element 10768: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10768) {2977 1586 1585 2976 2991 1592 1591 2990}
set elemKinit(10768) 3.773200081582705e-06
set sigmaV0(10768) 202.995000
set ruPrev(10768) 0.0

# Element 10769: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10769) {1637 2977 2976 1636 1644 2991 2990 1643}
set elemKinit(10769) 3.773200081582705e-06
set sigmaV0(10769) 202.995000
set ruPrev(10769) 0.0

# Element 10770: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10770) {2978 1587 1586 2977 2992 1593 1592 2991}
set elemKinit(10770) 3.773200081582705e-06
set sigmaV0(10770) 192.585000
set ruPrev(10770) 0.0

# Element 10771: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10771) {1638 2978 2977 1637 1645 2992 2991 1644}
set elemKinit(10771) 3.773200081582705e-06
set sigmaV0(10771) 192.585000
set ruPrev(10771) 0.0

# Element 10772: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10772) {2979 1588 1587 2978 2993 1594 1593 2992}
set elemKinit(10772) 3.773200081582705e-06
set sigmaV0(10772) 182.175000
set ruPrev(10772) 0.0

# Element 10773: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10773) {1639 2979 2978 1638 1646 2993 2992 1645}
set elemKinit(10773) 3.773200081582705e-06
set sigmaV0(10773) 182.175000
set ruPrev(10773) 0.0

# Element 10774: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10774) {1277 211 1588 2979 1283 212 1594 2993}
set elemKinit(10774) 3.773200081582705e-06
set sigmaV0(10774) 171.765000
set ruPrev(10774) 0.0

# Element 10775: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10775) {222 1277 2979 1639 223 1283 2993 1646}
set elemKinit(10775) 3.773200081582705e-06
set sigmaV0(10775) 171.765000
set ruPrev(10775) 0.0

# Element 10776: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10776) {2990 1591 289 1647 3350 2956 1599 3002}
set elemKinit(10776) 3.773200081582705e-06
set sigmaV0(10776) 213.405000
set ruPrev(10776) 0.0

# Element 10777: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10777) {3350 2956 1599 3002 2994 1595 290 1652}
set elemKinit(10777) 3.773200081582705e-06
set sigmaV0(10777) 213.405000
set ruPrev(10777) 0.0

# Element 10778: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10778) {1643 2990 1647 300 2998 3350 3002 1653}
set elemKinit(10778) 3.773200081582705e-06
set sigmaV0(10778) 213.405000
set ruPrev(10778) 0.0

# Element 10779: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10779) {2998 3350 3002 1653 1648 2994 1652 301}
set elemKinit(10779) 3.773200081582705e-06
set sigmaV0(10779) 213.405000
set ruPrev(10779) 0.0

# Element 10780: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10780) {2991 1592 1591 2990 3351 2957 2956 3350}
set elemKinit(10780) 3.773200081582705e-06
set sigmaV0(10780) 202.995000
set ruPrev(10780) 0.0

# Element 10781: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10781) {3351 2957 2956 3350 2995 1596 1595 2994}
set elemKinit(10781) 3.773200081582705e-06
set sigmaV0(10781) 202.995000
set ruPrev(10781) 0.0

# Element 10782: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10782) {1644 2991 2990 1643 2999 3351 3350 2998}
set elemKinit(10782) 3.773200081582705e-06
set sigmaV0(10782) 202.995000
set ruPrev(10782) 0.0

# Element 10783: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10783) {2999 3351 3350 2998 1649 2995 2994 1648}
set elemKinit(10783) 3.773200081582705e-06
set sigmaV0(10783) 202.995000
set ruPrev(10783) 0.0

# Element 10784: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10784) {2992 1593 1592 2991 3352 2958 2957 3351}
set elemKinit(10784) 3.773200081582705e-06
set sigmaV0(10784) 192.585000
set ruPrev(10784) 0.0

# Element 10785: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10785) {3352 2958 2957 3351 2996 1597 1596 2995}
set elemKinit(10785) 3.773200081582705e-06
set sigmaV0(10785) 192.585000
set ruPrev(10785) 0.0

# Element 10786: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10786) {1645 2992 2991 1644 3000 3352 3351 2999}
set elemKinit(10786) 3.773200081582705e-06
set sigmaV0(10786) 192.585000
set ruPrev(10786) 0.0

# Element 10787: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10787) {3000 3352 3351 2999 1650 2996 2995 1649}
set elemKinit(10787) 3.773200081582705e-06
set sigmaV0(10787) 192.585000
set ruPrev(10787) 0.0

# Element 10788: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10788) {2993 1594 1593 2992 3353 2959 2958 3352}
set elemKinit(10788) 3.773200081582705e-06
set sigmaV0(10788) 182.175000
set ruPrev(10788) 0.0

# Element 10789: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10789) {3353 2959 2958 3352 2997 1598 1597 2996}
set elemKinit(10789) 3.773200081582705e-06
set sigmaV0(10789) 182.175000
set ruPrev(10789) 0.0

# Element 10790: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10790) {1646 2993 2992 1645 3001 3353 3352 3000}
set elemKinit(10790) 3.773200081582705e-06
set sigmaV0(10790) 182.175000
set ruPrev(10790) 0.0

# Element 10791: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10791) {3001 3353 3352 3000 1651 2997 2996 1650}
set elemKinit(10791) 3.773200081582705e-06
set sigmaV0(10791) 182.175000
set ruPrev(10791) 0.0

# Element 10792: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10792) {1283 212 1594 2993 2744 1245 2959 3353}
set elemKinit(10792) 3.773200081582705e-06
set sigmaV0(10792) 171.765000
set ruPrev(10792) 0.0

# Element 10793: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10793) {2744 1245 2959 3353 1287 213 1598 2997}
set elemKinit(10793) 3.773200081582705e-06
set sigmaV0(10793) 171.765000
set ruPrev(10793) 0.0

# Element 10794: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10794) {223 1283 2993 1646 1288 2744 3353 3001}
set elemKinit(10794) 3.773200081582705e-06
set sigmaV0(10794) 171.765000
set ruPrev(10794) 0.0

# Element 10795: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10795) {1288 2744 3353 3001 224 1287 2997 1651}
set elemKinit(10795) 3.773200081582705e-06
set sigmaV0(10795) 171.765000
set ruPrev(10795) 0.0

# Element 10796: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10796) {2994 1595 290 1652 3003 1600 291 1658}
set elemKinit(10796) 3.773200081582705e-06
set sigmaV0(10796) 213.405000
set ruPrev(10796) 0.0

# Element 10797: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10797) {1648 2994 1652 301 1654 3003 1658 302}
set elemKinit(10797) 3.773200081582705e-06
set sigmaV0(10797) 213.405000
set ruPrev(10797) 0.0

# Element 10798: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10798) {2995 1596 1595 2994 3004 1601 1600 3003}
set elemKinit(10798) 3.773200081582705e-06
set sigmaV0(10798) 202.995000
set ruPrev(10798) 0.0

# Element 10799: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10799) {1649 2995 2994 1648 1655 3004 3003 1654}
set elemKinit(10799) 3.773200081582705e-06
set sigmaV0(10799) 202.995000
set ruPrev(10799) 0.0

# Element 10800: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10800) {2996 1597 1596 2995 3005 1602 1601 3004}
set elemKinit(10800) 3.773200081582705e-06
set sigmaV0(10800) 192.585000
set ruPrev(10800) 0.0

# Element 10801: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10801) {1650 2996 2995 1649 1656 3005 3004 1655}
set elemKinit(10801) 3.773200081582705e-06
set sigmaV0(10801) 192.585000
set ruPrev(10801) 0.0

# Element 10802: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10802) {2997 1598 1597 2996 3006 1603 1602 3005}
set elemKinit(10802) 3.773200081582705e-06
set sigmaV0(10802) 182.175000
set ruPrev(10802) 0.0

# Element 10803: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10803) {1651 2997 2996 1650 1657 3006 3005 1656}
set elemKinit(10803) 3.773200081582705e-06
set sigmaV0(10803) 182.175000
set ruPrev(10803) 0.0

# Element 10804: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10804) {1287 213 1598 2997 1292 214 1603 3006}
set elemKinit(10804) 3.773200081582705e-06
set sigmaV0(10804) 171.765000
set ruPrev(10804) 0.0

# Element 10805: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10805) {224 1287 2997 1651 225 1292 3006 1657}
set elemKinit(10805) 3.773200081582705e-06
set sigmaV0(10805) 171.765000
set ruPrev(10805) 0.0

# Element 10806: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10806) {3003 1600 291 1658 3007 1604 292 1663}
set elemKinit(10806) 3.773200081582705e-06
set sigmaV0(10806) 213.405000
set ruPrev(10806) 0.0

# Element 10807: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10807) {1654 3003 1658 302 1659 3007 1663 303}
set elemKinit(10807) 3.773200081582705e-06
set sigmaV0(10807) 213.405000
set ruPrev(10807) 0.0

# Element 10808: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10808) {3004 1601 1600 3003 3008 1605 1604 3007}
set elemKinit(10808) 3.773200081582705e-06
set sigmaV0(10808) 202.995000
set ruPrev(10808) 0.0

# Element 10809: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10809) {1655 3004 3003 1654 1660 3008 3007 1659}
set elemKinit(10809) 3.773200081582705e-06
set sigmaV0(10809) 202.995000
set ruPrev(10809) 0.0

# Element 10810: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10810) {3005 1602 1601 3004 3009 1606 1605 3008}
set elemKinit(10810) 3.773200081582705e-06
set sigmaV0(10810) 192.585000
set ruPrev(10810) 0.0

# Element 10811: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10811) {1656 3005 3004 1655 1661 3009 3008 1660}
set elemKinit(10811) 3.773200081582705e-06
set sigmaV0(10811) 192.585000
set ruPrev(10811) 0.0

# Element 10812: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10812) {3006 1603 1602 3005 3010 1607 1606 3009}
set elemKinit(10812) 3.773200081582705e-06
set sigmaV0(10812) 182.175000
set ruPrev(10812) 0.0

# Element 10813: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10813) {1657 3006 3005 1656 1662 3010 3009 1661}
set elemKinit(10813) 3.773200081582705e-06
set sigmaV0(10813) 182.175000
set ruPrev(10813) 0.0

# Element 10814: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10814) {1292 214 1603 3006 1296 215 1607 3010}
set elemKinit(10814) 3.773200081582705e-06
set sigmaV0(10814) 171.765000
set ruPrev(10814) 0.0

# Element 10815: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10815) {225 1292 3006 1657 226 1296 3010 1662}
set elemKinit(10815) 3.773200081582705e-06
set sigmaV0(10815) 171.765000
set ruPrev(10815) 0.0

# Element 10816: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10816) {3007 1604 292 1663 3011 1608 293 1668}
set elemKinit(10816) 3.773200081582705e-06
set sigmaV0(10816) 213.405000
set ruPrev(10816) 0.0

# Element 10817: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10817) {1659 3007 1663 303 1664 3011 1668 304}
set elemKinit(10817) 3.773200081582705e-06
set sigmaV0(10817) 213.405000
set ruPrev(10817) 0.0

# Element 10818: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10818) {3008 1605 1604 3007 3012 1609 1608 3011}
set elemKinit(10818) 3.773200081582705e-06
set sigmaV0(10818) 202.995000
set ruPrev(10818) 0.0

# Element 10819: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10819) {1660 3008 3007 1659 1665 3012 3011 1664}
set elemKinit(10819) 3.773200081582705e-06
set sigmaV0(10819) 202.995000
set ruPrev(10819) 0.0

# Element 10820: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10820) {3009 1606 1605 3008 3013 1610 1609 3012}
set elemKinit(10820) 3.773200081582705e-06
set sigmaV0(10820) 192.585000
set ruPrev(10820) 0.0

# Element 10821: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10821) {1661 3009 3008 1660 1666 3013 3012 1665}
set elemKinit(10821) 3.773200081582705e-06
set sigmaV0(10821) 192.585000
set ruPrev(10821) 0.0

# Element 10822: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10822) {3010 1607 1606 3009 3014 1611 1610 3013}
set elemKinit(10822) 3.773200081582705e-06
set sigmaV0(10822) 182.175000
set ruPrev(10822) 0.0

# Element 10823: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10823) {1662 3010 3009 1661 1667 3014 3013 1666}
set elemKinit(10823) 3.773200081582705e-06
set sigmaV0(10823) 182.175000
set ruPrev(10823) 0.0

# Element 10824: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10824) {1296 215 1607 3010 1300 216 1611 3014}
set elemKinit(10824) 3.773200081582705e-06
set sigmaV0(10824) 171.765000
set ruPrev(10824) 0.0

# Element 10825: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10825) {226 1296 3010 1662 227 1300 3014 1667}
set elemKinit(10825) 3.773200081582705e-06
set sigmaV0(10825) 171.765000
set ruPrev(10825) 0.0

# Element 10826: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10826) {3011 1608 293 1668 3015 1612 294 1673}
set elemKinit(10826) 3.773200081582705e-06
set sigmaV0(10826) 213.405000
set ruPrev(10826) 0.0

# Element 10827: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10827) {1664 3011 1668 304 1669 3015 1673 305}
set elemKinit(10827) 3.773200081582705e-06
set sigmaV0(10827) 213.405000
set ruPrev(10827) 0.0

# Element 10828: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10828) {3012 1609 1608 3011 3016 1613 1612 3015}
set elemKinit(10828) 3.773200081582705e-06
set sigmaV0(10828) 202.995000
set ruPrev(10828) 0.0

# Element 10829: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10829) {1665 3012 3011 1664 1670 3016 3015 1669}
set elemKinit(10829) 3.773200081582705e-06
set sigmaV0(10829) 202.995000
set ruPrev(10829) 0.0

# Element 10830: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10830) {3013 1610 1609 3012 3017 1614 1613 3016}
set elemKinit(10830) 3.773200081582705e-06
set sigmaV0(10830) 192.585000
set ruPrev(10830) 0.0

# Element 10831: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10831) {1666 3013 3012 1665 1671 3017 3016 1670}
set elemKinit(10831) 3.773200081582705e-06
set sigmaV0(10831) 192.585000
set ruPrev(10831) 0.0

# Element 10832: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10832) {3014 1611 1610 3013 3018 1615 1614 3017}
set elemKinit(10832) 3.773200081582705e-06
set sigmaV0(10832) 182.175000
set ruPrev(10832) 0.0

# Element 10833: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10833) {1667 3014 3013 1666 1672 3018 3017 1671}
set elemKinit(10833) 3.773200081582705e-06
set sigmaV0(10833) 182.175000
set ruPrev(10833) 0.0

# Element 10834: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10834) {1300 216 1611 3014 1304 217 1615 3018}
set elemKinit(10834) 3.773200081582705e-06
set sigmaV0(10834) 171.765000
set ruPrev(10834) 0.0

# Element 10835: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10835) {227 1300 3014 1667 228 1304 3018 1672}
set elemKinit(10835) 3.773200081582705e-06
set sigmaV0(10835) 171.765000
set ruPrev(10835) 0.0

# Element 10836: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10836) {3015 1612 294 1673 3354 2960 1620 3027}
set elemKinit(10836) 3.773200081582705e-06
set sigmaV0(10836) 213.405000
set ruPrev(10836) 0.0

# Element 10837: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10837) {3354 2960 1620 3027 3019 1616 295 1678}
set elemKinit(10837) 3.773200081582705e-06
set sigmaV0(10837) 213.405000
set ruPrev(10837) 0.0

# Element 10838: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10838) {1669 3015 1673 305 3023 3354 3027 1679}
set elemKinit(10838) 3.773200081582705e-06
set sigmaV0(10838) 213.405000
set ruPrev(10838) 0.0

# Element 10839: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10839) {3023 3354 3027 1679 1674 3019 1678 306}
set elemKinit(10839) 3.773200081582705e-06
set sigmaV0(10839) 213.405000
set ruPrev(10839) 0.0

# Element 10840: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10840) {3016 1613 1612 3015 3355 2961 2960 3354}
set elemKinit(10840) 3.773200081582705e-06
set sigmaV0(10840) 202.995000
set ruPrev(10840) 0.0

# Element 10841: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10841) {3355 2961 2960 3354 3020 1617 1616 3019}
set elemKinit(10841) 3.773200081582705e-06
set sigmaV0(10841) 202.995000
set ruPrev(10841) 0.0

# Element 10842: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10842) {1670 3016 3015 1669 3024 3355 3354 3023}
set elemKinit(10842) 3.773200081582705e-06
set sigmaV0(10842) 202.995000
set ruPrev(10842) 0.0

# Element 10843: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10843) {3024 3355 3354 3023 1675 3020 3019 1674}
set elemKinit(10843) 3.773200081582705e-06
set sigmaV0(10843) 202.995000
set ruPrev(10843) 0.0

# Element 10844: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10844) {3017 1614 1613 3016 3356 2962 2961 3355}
set elemKinit(10844) 3.773200081582705e-06
set sigmaV0(10844) 192.585000
set ruPrev(10844) 0.0

# Element 10845: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10845) {3356 2962 2961 3355 3021 1618 1617 3020}
set elemKinit(10845) 3.773200081582705e-06
set sigmaV0(10845) 192.585000
set ruPrev(10845) 0.0

# Element 10846: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10846) {1671 3017 3016 1670 3025 3356 3355 3024}
set elemKinit(10846) 3.773200081582705e-06
set sigmaV0(10846) 192.585000
set ruPrev(10846) 0.0

# Element 10847: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10847) {3025 3356 3355 3024 1676 3021 3020 1675}
set elemKinit(10847) 3.773200081582705e-06
set sigmaV0(10847) 192.585000
set ruPrev(10847) 0.0

# Element 10848: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10848) {3018 1615 1614 3017 3357 2963 2962 3356}
set elemKinit(10848) 3.773200081582705e-06
set sigmaV0(10848) 182.175000
set ruPrev(10848) 0.0

# Element 10849: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10849) {3357 2963 2962 3356 3022 1619 1618 3021}
set elemKinit(10849) 3.773200081582705e-06
set sigmaV0(10849) 182.175000
set ruPrev(10849) 0.0

# Element 10850: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10850) {1672 3018 3017 1671 3026 3357 3356 3025}
set elemKinit(10850) 3.773200081582705e-06
set sigmaV0(10850) 182.175000
set ruPrev(10850) 0.0

# Element 10851: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10851) {3026 3357 3356 3025 1677 3022 3021 1676}
set elemKinit(10851) 3.773200081582705e-06
set sigmaV0(10851) 182.175000
set ruPrev(10851) 0.0

# Element 10852: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10852) {1304 217 1615 3018 2763 1261 2963 3357}
set elemKinit(10852) 3.773200081582705e-06
set sigmaV0(10852) 171.765000
set ruPrev(10852) 0.0

# Element 10853: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10853) {2763 1261 2963 3357 1308 218 1619 3022}
set elemKinit(10853) 3.773200081582705e-06
set sigmaV0(10853) 171.765000
set ruPrev(10853) 0.0

# Element 10854: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10854) {228 1304 3018 1672 1309 2763 3357 3026}
set elemKinit(10854) 3.773200081582705e-06
set sigmaV0(10854) 171.765000
set ruPrev(10854) 0.0

# Element 10855: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10855) {1309 2763 3357 3026 229 1308 3022 1677}
set elemKinit(10855) 3.773200081582705e-06
set sigmaV0(10855) 171.765000
set ruPrev(10855) 0.0

# Element 10856: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10856) {3019 1616 295 1678 3028 1621 296 1684}
set elemKinit(10856) 3.773200081582705e-06
set sigmaV0(10856) 213.405000
set ruPrev(10856) 0.0

# Element 10857: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10857) {1674 3019 1678 306 1680 3028 1684 307}
set elemKinit(10857) 3.773200081582705e-06
set sigmaV0(10857) 213.405000
set ruPrev(10857) 0.0

# Element 10858: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10858) {3020 1617 1616 3019 3029 1622 1621 3028}
set elemKinit(10858) 3.773200081582705e-06
set sigmaV0(10858) 202.995000
set ruPrev(10858) 0.0

# Element 10859: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10859) {1675 3020 3019 1674 1681 3029 3028 1680}
set elemKinit(10859) 3.773200081582705e-06
set sigmaV0(10859) 202.995000
set ruPrev(10859) 0.0

# Element 10860: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10860) {3021 1618 1617 3020 3030 1623 1622 3029}
set elemKinit(10860) 3.773200081582705e-06
set sigmaV0(10860) 192.585000
set ruPrev(10860) 0.0

# Element 10861: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10861) {1676 3021 3020 1675 1682 3030 3029 1681}
set elemKinit(10861) 3.773200081582705e-06
set sigmaV0(10861) 192.585000
set ruPrev(10861) 0.0

# Element 10862: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10862) {3022 1619 1618 3021 3031 1624 1623 3030}
set elemKinit(10862) 3.773200081582705e-06
set sigmaV0(10862) 182.175000
set ruPrev(10862) 0.0

# Element 10863: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10863) {1677 3022 3021 1676 1683 3031 3030 1682}
set elemKinit(10863) 3.773200081582705e-06
set sigmaV0(10863) 182.175000
set ruPrev(10863) 0.0

# Element 10864: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10864) {1308 218 1619 3022 1313 219 1624 3031}
set elemKinit(10864) 3.773200081582705e-06
set sigmaV0(10864) 171.765000
set ruPrev(10864) 0.0

# Element 10865: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10865) {229 1308 3022 1677 230 1313 3031 1683}
set elemKinit(10865) 3.773200081582705e-06
set sigmaV0(10865) 171.765000
set ruPrev(10865) 0.0

# Element 10866: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10866) {3028 1621 296 1684 3358 2964 1629 3044}
set elemKinit(10866) 3.773200081582705e-06
set sigmaV0(10866) 213.405000
set ruPrev(10866) 0.0

# Element 10867: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10867) {3358 2964 1629 3044 3359 2968 1630 3045}
set elemKinit(10867) 3.773200081582705e-06
set sigmaV0(10867) 213.405000
set ruPrev(10867) 0.0

# Element 10868: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10868) {3359 2968 1630 3045 3032 1625 297 1689}
set elemKinit(10868) 3.773200081582705e-06
set sigmaV0(10868) 213.405000
set ruPrev(10868) 0.0

# Element 10869: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10869) {1680 3028 1684 307 3036 3358 3044 1690}
set elemKinit(10869) 3.773200081582705e-06
set sigmaV0(10869) 213.405000
set ruPrev(10869) 0.0

# Element 10870: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10870) {3036 3358 3044 1690 3040 3359 3045 1691}
set elemKinit(10870) 3.773200081582705e-06
set sigmaV0(10870) 213.405000
set ruPrev(10870) 0.0

# Element 10871: depth=20.50m, sigma_v0=213.41kPa, mat=2
set elemNodes(10871) {3040 3359 3045 1691 1685 3032 1689 308}
set elemKinit(10871) 3.773200081582705e-06
set sigmaV0(10871) 213.405000
set ruPrev(10871) 0.0

# Element 10872: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10872) {3029 1622 1621 3028 3360 2965 2964 3358}
set elemKinit(10872) 3.773200081582705e-06
set sigmaV0(10872) 202.995000
set ruPrev(10872) 0.0

# Element 10873: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10873) {3360 2965 2964 3358 3361 2969 2968 3359}
set elemKinit(10873) 3.773200081582705e-06
set sigmaV0(10873) 202.995000
set ruPrev(10873) 0.0

# Element 10874: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10874) {3361 2969 2968 3359 3033 1626 1625 3032}
set elemKinit(10874) 3.773200081582705e-06
set sigmaV0(10874) 202.995000
set ruPrev(10874) 0.0

# Element 10875: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10875) {1681 3029 3028 1680 3037 3360 3358 3036}
set elemKinit(10875) 3.773200081582705e-06
set sigmaV0(10875) 202.995000
set ruPrev(10875) 0.0

# Element 10876: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10876) {3037 3360 3358 3036 3041 3361 3359 3040}
set elemKinit(10876) 3.773200081582705e-06
set sigmaV0(10876) 202.995000
set ruPrev(10876) 0.0

# Element 10877: depth=19.50m, sigma_v0=203.00kPa, mat=2
set elemNodes(10877) {3041 3361 3359 3040 1686 3033 3032 1685}
set elemKinit(10877) 3.773200081582705e-06
set sigmaV0(10877) 202.995000
set ruPrev(10877) 0.0

# Element 10878: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10878) {3030 1623 1622 3029 3362 2966 2965 3360}
set elemKinit(10878) 3.773200081582705e-06
set sigmaV0(10878) 192.585000
set ruPrev(10878) 0.0

# Element 10879: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10879) {3362 2966 2965 3360 3363 2970 2969 3361}
set elemKinit(10879) 3.773200081582705e-06
set sigmaV0(10879) 192.585000
set ruPrev(10879) 0.0

# Element 10880: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10880) {3363 2970 2969 3361 3034 1627 1626 3033}
set elemKinit(10880) 3.773200081582705e-06
set sigmaV0(10880) 192.585000
set ruPrev(10880) 0.0

# Element 10881: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10881) {1682 3030 3029 1681 3038 3362 3360 3037}
set elemKinit(10881) 3.773200081582705e-06
set sigmaV0(10881) 192.585000
set ruPrev(10881) 0.0

# Element 10882: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10882) {3038 3362 3360 3037 3042 3363 3361 3041}
set elemKinit(10882) 3.773200081582705e-06
set sigmaV0(10882) 192.585000
set ruPrev(10882) 0.0

# Element 10883: depth=18.50m, sigma_v0=192.59kPa, mat=2
set elemNodes(10883) {3042 3363 3361 3041 1687 3034 3033 1686}
set elemKinit(10883) 3.773200081582705e-06
set sigmaV0(10883) 192.585000
set ruPrev(10883) 0.0

# Element 10884: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10884) {3031 1624 1623 3030 3364 2967 2966 3362}
set elemKinit(10884) 3.773200081582705e-06
set sigmaV0(10884) 182.175000
set ruPrev(10884) 0.0

# Element 10885: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10885) {3364 2967 2966 3362 3365 2971 2970 3363}
set elemKinit(10885) 3.773200081582705e-06
set sigmaV0(10885) 182.175000
set ruPrev(10885) 0.0

# Element 10886: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10886) {3365 2971 2970 3363 3035 1628 1627 3034}
set elemKinit(10886) 3.773200081582705e-06
set sigmaV0(10886) 182.175000
set ruPrev(10886) 0.0

# Element 10887: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10887) {1683 3031 3030 1682 3039 3364 3362 3038}
set elemKinit(10887) 3.773200081582705e-06
set sigmaV0(10887) 182.175000
set ruPrev(10887) 0.0

# Element 10888: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10888) {3039 3364 3362 3038 3043 3365 3363 3042}
set elemKinit(10888) 3.773200081582705e-06
set sigmaV0(10888) 182.175000
set ruPrev(10888) 0.0

# Element 10889: depth=17.50m, sigma_v0=182.18kPa, mat=2
set elemNodes(10889) {3043 3365 3363 3042 1688 3035 3034 1687}
set elemKinit(10889) 3.773200081582705e-06
set sigmaV0(10889) 182.175000
set ruPrev(10889) 0.0

# Element 10890: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10890) {1313 219 1624 3031 2776 1268 2967 3364}
set elemKinit(10890) 3.773200081582705e-06
set sigmaV0(10890) 171.765000
set ruPrev(10890) 0.0

# Element 10891: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10891) {2776 1268 2967 3364 2777 1269 2971 3365}
set elemKinit(10891) 3.773200081582705e-06
set sigmaV0(10891) 171.765000
set ruPrev(10891) 0.0

# Element 10892: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10892) {2777 1269 2971 3365 1317 220 1628 3035}
set elemKinit(10892) 3.773200081582705e-06
set sigmaV0(10892) 171.765000
set ruPrev(10892) 0.0

# Element 10893: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10893) {230 1313 3031 1683 1318 2776 3364 3039}
set elemKinit(10893) 3.773200081582705e-06
set sigmaV0(10893) 171.765000
set ruPrev(10893) 0.0

# Element 10894: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10894) {1318 2776 3364 3039 1319 2777 3365 3043}
set elemKinit(10894) 3.773200081582705e-06
set sigmaV0(10894) 171.765000
set ruPrev(10894) 0.0

# Element 10895: depth=16.50m, sigma_v0=171.77kPa, mat=2
set elemNodes(10895) {1319 2777 3365 3043 231 1317 3035 1688}
set elemKinit(10895) 3.773200081582705e-06
set sigmaV0(10895) 171.765000
set ruPrev(10895) 0.0

# ============================================================================
# PROCEDURES
# ============================================================================

proc getElementPWP {elemTag} {
    global elemNodes
    if {![info exists elemNodes($elemTag)]} { return 0.0 }
    set nodeList $elemNodes($elemTag)
    set sumPWP 0.0
    set count 0
    foreach nd $nodeList {
        if {[catch {set pwp [nodeVel $nd 4]} err]} { continue }
        set sumPWP [expr $sumPWP + $pwp]
        incr count
    }
    if {$count > 0} { return [expr $sumPWP / $count] }
    return 0.0
}

proc updateElementPermeability {elemTag} {
    global alpha beta1 beta2 sigmaV0 ruPrev elemKinit
    if {![info exists sigmaV0($elemTag)]} { return [list 0.0 1.0 0.0] }

    # STEP 1: Get pore pressure
    set pwp [getElementPWP $elemTag]

    # STEP 2: Calculate ru
    if {$sigmaV0($elemTag) > 0.0} {
        set ru [expr abs($pwp) / $sigmaV0($elemTag)]
    } else {
        set ru 0.0
    }
    if {$ru < 0.0} {set ru 0.0}
    if {$ru > 1.0} {set ru 1.0}

    # STEP 3: Calculate new permeability
    if {$ru >= $ruPrev($elemTag)} {
        set beta $beta1
    } else {
        set beta $beta2
    }
    if {$ru < 0.001} {
        set kRatio 1.0
    } else {
        set kRatio [expr 1.0 + ($alpha - 1.0) * pow($ru, $beta)]
    }
    set kNew [expr $elemKinit($elemTag) * $kRatio]

    # STEP 4: Update element
    setParameter -value $kNew -ele $elemTag xPerm
    setParameter -value $kNew -ele $elemTag yPerm
    setParameter -value $kNew -ele $elemTag zPerm
    set ruPrev($elemTag) $ru

    return [list $ru $kRatio $kNew]
}

proc updateAllPermeabilities {} {
    global firstSSPelem lastSSPelem
    for {set e $firstSSPelem} {$e <= $lastSSPelem} {incr e} {
        updateElementPermeability $e
    }
}

puts "\[INFO\] Variable permeability data loaded: $numSSPelems SSPbrickUP elements"
puts "\[INFO\] Parameters: alpha=$alpha, beta1=$beta1, beta2=$beta2"
