//
SetFactory("OpenCASCADE");

// Parameters, selection tolerance, and mesh sizes
x0 = 0; y0 = 0; z0 = 0;
Lx = 20; Ly = 10; Lz = 10;
eps = 1e-6;
XMeshSize = 1; YMeshSize = 1; ZMeshSize = 1;

// Geometry 
Box(1) = {x0 - Lx/2, y0 - Ly/2, z0 - Lz, Lx, Ly, Lz};

xmin = x0 - Lx/2; xmax = x0 + Lx/2;
ymin = y0 - Ly/2; ymax = y0 + Ly/2;
zmin = z0 - Lz; zmax = z0;

// Robust edge selection 
cX[] = {}; cY[] = {}; cZ[] = {};

// X edges (y fixed, z fixed, x varies)
cX[] += Curve In BoundingBox { xmin-eps, ymin-eps, zmin-eps,  xmax+eps, ymin+eps, zmin+eps };
cX[] += Curve In BoundingBox { xmin-eps, ymin-eps, zmax-eps,  xmax+eps, ymin+eps, zmax+eps };
cX[] += Curve In BoundingBox { xmin-eps, ymax-eps, zmin-eps,  xmax+eps, ymax+eps, zmin+eps };
cX[] += Curve In BoundingBox { xmin-eps, ymax-eps, zmax-eps,  xmax+eps, ymax+eps, zmax+eps };

// Y edges (x fixed, z fixed, y varies)
cY[] += Curve In BoundingBox { xmin-eps, ymin-eps, zmin-eps,  xmin+eps, ymax+eps, zmin+eps };
cY[] += Curve In BoundingBox { xmin-eps, ymin-eps, zmax-eps,  xmin+eps, ymax+eps, zmax+eps };
cY[] += Curve In BoundingBox { xmax-eps, ymin-eps, zmin-eps,  xmax+eps, ymax+eps, zmin+eps };
cY[] += Curve In BoundingBox { xmax-eps, ymin-eps, zmax-eps,  xmax+eps, ymax+eps, zmax+eps };

// Z edges (x fixed, y fixed, z varies)
cZ[] += Curve In BoundingBox { xmin-eps, ymin-eps, zmin-eps,  xmin+eps, ymin+eps, zmax+eps };
cZ[] += Curve In BoundingBox { xmin-eps, ymax-eps, zmin-eps,  xmin+eps, ymax+eps, zmax+eps };
cZ[] += Curve In BoundingBox { xmax-eps, ymin-eps, zmin-eps,  xmax+eps, ymin+eps, zmax+eps };
cZ[] += Curve In BoundingBox { xmax-eps, ymax-eps, zmin-eps,  xmax+eps, ymax+eps, zmax+eps };

// Debug 1: raw selections 
Printf("RAW counts: #cX=%g #cY=%g #cZ=%g", #cX[], #cY[], #cZ[]);

Printf("RAW cX:");
For k In {0:#cX[]-1}
  Printf("  cX[%g]=%g", k, cX[k]);
EndFor
Printf("RAW cY:");
For k In {0:#cY[]-1}
  Printf("  cY[%g]=%g", k, cY[k]);
EndFor
Printf("RAW cZ:");
For k In {0:#cZ[]-1}
  Printf("  cZ[%g]=%g", k, cZ[k]);
EndFor

// Sort copies (useful to spot duplicates visually)
cXsorted[] = cX[];
cYsorted[] = cY[];
cZsorted[] = cZ[];

Printf("SORTED cX:");
For k In {0:#cXsorted[]-1}
  Printf("  cXsorted[%g]=%g", k, cXsorted[k]);
EndFor
Printf("SORTED cY:");
For k In {0:#cYsorted[]-1}
  Printf("  cYsorted[%g]=%g", k, cYsorted[k]);
EndFor
Printf("SORTED cZ:");
For k In {0:#cZsorted[]-1}
  Printf("  cZsorted[%g]=%g", k, cZsorted[k]);
EndFor

// Remove duplicates

// Step 1A: global edge sanity
allC[] = {};
allC[] += cX[];
allC[] += cY[];
allC[] += cZ[];
Printf("TOTAL unique curves in cX+cY+cZ: %g (should be 12)", #allC[]);

// Step 1B: check endpoints of each curve 
// For a clean box, every edge curve should have exactly 2 boundary points
For k In {0:#allC[]-1}
  cc = allC[k];
  bp[] = Boundary{ Curve{cc}; };
  Printf("Curve %g has %g boundary points", cc, #bp[]);
  For j In {0:#bp[]-1}
    Printf("  endpoint[%g] = %g", j, bp[j]);
  EndFor
EndFor


Printf("AFTER Unique counts: #cX=%g #cY=%g #cZ=%g", #cX[], #cY[], #cZ[]);

Printf("AFTER Unique cX:");
For k In {0:#cX[]-1}
  Printf("  cX[%g]=%g", k, cX[k]);
EndFor
Printf("AFTER Unique cY:");
For k In {0:#cY[]-1}
  Printf("  cY[%g]=%g", k, cY[k]);
EndFor
Printf("AFTER Unique cZ:");
For k In {0:#cZ[]-1}
  Printf("  cZ[%g]=%g", k, cZ[k]);
EndFor

// Transfinite counts 
nx = Ceil(Lx/XMeshSize) + 1;
ny = Ceil(Ly/YMeshSize) + 1;
nz = Ceil(Lz/ZMeshSize) + 1;
Printf("Transfinite points: nx=%g ny=%g nz=%g", nx, ny, nz);

// Apply curve constraints
Transfinite Curve {cX[]} = nx Using Progression 1;
Transfinite Curve {cY[]} = ny Using Progression 1;
Transfinite Curve {cZ[]} = nz Using Progression 1;

// Debug 2: surface boundaries 
s[] = Boundary{ Volume{1}; };
Printf("Boundary surfaces raw count #s=%g", #s[]);

// Print each surface and its boundary curves
For j In {0:#s[]-1}
  ss = s[j];
  bcur[] = Boundary{ Surface{ss}; };
  Printf("Surface %g has #boundaryCurves=%g", ss, #bcur[]);
  For k In {0:#bcur[]-1}
    Printf("  bcur[%g]=%g", k, bcur[k]);
  EndFor
EndFor

// Try transfinite surfaces/volume
// (Keep Left; it sometimes helps with orientation)
Transfinite Surface {1:6};
Recombine Surface {1:6};
Transfinite Volume {1};

