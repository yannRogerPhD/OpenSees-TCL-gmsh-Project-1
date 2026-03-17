//
SetFactory("OpenCASCADE");
eps = 1e-06;

Box(1) = {-0.5, -0.5, -0.5, 1, 1, 0.5};
Coherence;

XMIN_SOIL = -0.5; XMAX_SOIL = 0.5;
YMIN_SOIL = -0.5; YMAX_SOIL = 0.5;
ZMIN_SOIL = -0.5; ZMAX_SOIL = 0;

tAbsB = 20; nAbsB = 1;
tAbsL = 20; nAbsL = 1;
tAbsR = 20; nAbsR = 1;
tAbsF = 20; nAbsF = 1;
tAbsK = 20; nAbsK = 1;


// Coherence after absorbing layers
Coherence;

// Reusable curve-constraint macro (keeps .geo small)
Macro ApplyBBoxCurveConstraints
  xMin = (X0 - Lx/2); xMax = (X0 + Lx/2);
  yMin = (Y0 - Ly/2); yMax = (Y0 + Ly/2);
  zMin = (Z0 - Lz  ); zMax = (Z0      );
  cX[] = {}; cY[] = {}; cZ[] = {};
  // X edges
  cX[] += Curve In BoundingBox { xMin-eps, yMin-eps, zMin-eps, xMax+eps, yMin+eps, zMin+eps };
  cX[] += Curve In BoundingBox { xMin-eps, yMin-eps, zMax-eps, xMax+eps, yMin+eps, zMax+eps };
  cX[] += Curve In BoundingBox { xMin-eps, yMax-eps, zMin-eps, xMax+eps, yMax+eps, zMin+eps };
  cX[] += Curve In BoundingBox { xMin-eps, yMax-eps, zMax-eps, xMax+eps, yMax+eps, zMax+eps };
  // Y edges
  cY[] += Curve In BoundingBox { xMin-eps, yMin-eps, zMin-eps, xMin+eps, yMax+eps, zMin+eps };
  cY[] += Curve In BoundingBox { xMin-eps, yMin-eps, zMax-eps, xMin+eps, yMax+eps, zMax+eps };
  cY[] += Curve In BoundingBox { xMax-eps, yMin-eps, zMin-eps, xMax+eps, yMax+eps, zMin+eps };
  cY[] += Curve In BoundingBox { xMax-eps, yMin-eps, zMax-eps, xMax+eps, yMax+eps, zMax+eps };
  // Z edges
  cZ[] += Curve In BoundingBox { xMin-eps, yMin-eps, zMin-eps, xMin+eps, yMin+eps, zMax+eps };
  cZ[] += Curve In BoundingBox { xMin-eps, yMax-eps, zMin-eps, xMin+eps, yMax+eps, zMax+eps };
  cZ[] += Curve In BoundingBox { xMax-eps, yMin-eps, zMin-eps, xMax+eps, yMin+eps, zMax+eps };
  cZ[] += Curve In BoundingBox { xMax-eps, yMax-eps, zMin-eps, xMax+eps, yMax+eps, zMax+eps };
  cX[] = Unique(Abs(cX[])); cY[] = Unique(Abs(cY[])); cZ[] = Unique(Abs(cZ[]));
  Transfinite Curve {cX[]} = TX Using Progression 1;
  Transfinite Curve {cY[]} = TY Using Progression 1;
  Transfinite Curve {cZ[]} = TZ Using Progression 1;
Return

transX_col1 = Ceil(1/0.3333333333333333) + 1;
transY_row1 = Ceil(1/0.3333333333333333) + 1;
transZ_L1 = Ceil(0.5/0.125) + 1;

Lx_1 = 1; Ly_1 = 1; Lz_1 = 0.5;
X0 = 0; Y0 = 0; Z0 = 0;
Lx = Lx_1; Ly = Ly_1; Lz = Lz_1;
TX = transX_col1; TY = transY_row1; TZ = transZ_L1;
Call ApplyBBoxCurveConstraints;

// Apply surface/volume transfinite + recombine to all volumes
allVols[] = Volume{:};
allVols[] = Unique(Abs(allVols[]));
For vi In {0:#allVols[]-1}
  vtag = allVols[vi];
  ss[] = Unique(Abs(Boundary{ Volume{vtag}; }));
  Transfinite Surface {ss[]};
  Recombine Surface {ss[]};
  Transfinite Volume {vtag};
EndFor//+
Point(9) = {0, 0, -0.25, 1.0};
//+
Point(10) = {0, 0, 0, 1.0};
//+
Point(11) = {0, 0, 0.15, 1.0};
//+
Line(13) = {9, 10};
//+
Line(14) = {10, 11};
//+
Transfinite Curve {13} = 3 Using Progression 1;
//+
Transfinite Curve {14} = 3 Using Progression 1;
