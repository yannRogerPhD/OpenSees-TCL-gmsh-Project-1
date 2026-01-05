//
SetFactory("OpenCASCADE");
//+
eps = DefineNumber[ 1e-06, Name "Global/Selection/eps" ];
// PREAMBLE (shared parameters / derived counts) 
//+
lTy_global = DefineNumber[ 10.0, Name "Global/Geometry/lTy" ];
//+
YMeshSize_global = DefineNumber[ 1.0, Name "Global/Mesh/YMeshSize" ];
//+
transY_global = Ceil(lTy_global/YMeshSize_global) + 1;
//+
lTz_transZ_L1 = DefineNumber[ 5.0, Name "Layer1/Geometry/thickness" ];
//+
ZMeshSize_transZ_L1 = DefineNumber[ 0.5, Name "Layer1/Mesh/ZMeshSize" ];
//+
transZ_L1 = Ceil(lTz_transZ_L1/ZMeshSize_transZ_L1) + 1;
//+
lTz_transZ_L2 = DefineNumber[ 7.0, Name "Layer2/Geometry/thickness" ];
//+
ZMeshSize_transZ_L2 = DefineNumber[ 1.0, Name "Layer2/Mesh/ZMeshSize" ];
//+
transZ_L2 = Ceil(lTz_transZ_L2/ZMeshSize_transZ_L2) + 1;
//+
XMeshSize_1 = DefineNumber[ 0.5, Name "Box 1/Mesh/XMeshSize" ];
//+
YMeshSize_1 = DefineNumber[ 1.0, Name "Box 1/Mesh/YMeshSize" ];
//+
ZMeshSize_1 = DefineNumber[ 0.5, Name "Box 1/Mesh/ZMeshSize" ];
//+
lTx_1 = DefineNumber[ 8.0, Name "Box 1/Geometry/lTx" ];
//+
lTy_1 = DefineNumber[ 10.0, Name "Box 1/Geometry/lTy" ];
//+
lTz_1 = DefineNumber[ 5.0, Name "Box 1/Geometry/lTz" ];
//+
x0_1 = DefineNumber[ -6.0, Name "Box 1/Geometry/x0" ];
//+
y0_1 = DefineNumber[ 0.0, Name "Box 1/Geometry/y0" ];
//+
z0_1 = DefineNumber[ 0.0, Name "Box 1/Geometry/z0" ];
//+
Box(1) = {x0_1 - lTx_1/2, y0_1 - lTy_1/2, z0_1 - lTz_1, lTx_1, lTy_1, lTz_1};
//+
XMeshSize_2 = DefineNumber[ 0.25, Name "Box 2/Mesh/XMeshSize" ];
//+
YMeshSize_2 = DefineNumber[ 1.0, Name "Box 2/Mesh/YMeshSize" ];
//+
ZMeshSize_2 = DefineNumber[ 0.5, Name "Box 2/Mesh/ZMeshSize" ];
//+
lTx_2 = DefineNumber[ 4.0, Name "Box 2/Geometry/lTx" ];
//+
lTy_2 = DefineNumber[ 10.0, Name "Box 2/Geometry/lTy" ];
//+
lTz_2 = DefineNumber[ 5.0, Name "Box 2/Geometry/lTz" ];
//+
x0_2 = DefineNumber[ 0.0, Name "Box 2/Geometry/x0" ];
//+
y0_2 = DefineNumber[ 0.0, Name "Box 2/Geometry/y0" ];
//+
z0_2 = DefineNumber[ 0.0, Name "Box 2/Geometry/z0" ];
//+
Box(2) = {x0_2 - lTx_2/2, y0_2 - lTy_2/2, z0_2 - lTz_2, lTx_2, lTy_2, lTz_2};
//+
XMeshSize_3 = DefineNumber[ 0.5, Name "Box 3/Mesh/XMeshSize" ];
//+
YMeshSize_3 = DefineNumber[ 1.0, Name "Box 3/Mesh/YMeshSize" ];
//+
ZMeshSize_3 = DefineNumber[ 0.5, Name "Box 3/Mesh/ZMeshSize" ];
//+
lTx_3 = DefineNumber[ 8.0, Name "Box 3/Geometry/lTx" ];
//+
lTy_3 = DefineNumber[ 10.0, Name "Box 3/Geometry/lTy" ];
//+
lTz_3 = DefineNumber[ 5.0, Name "Box 3/Geometry/lTz" ];
//+
x0_3 = DefineNumber[ 6.0, Name "Box 3/Geometry/x0" ];
//+
y0_3 = DefineNumber[ 0.0, Name "Box 3/Geometry/y0" ];
//+
z0_3 = DefineNumber[ 0.0, Name "Box 3/Geometry/z0" ];
//+
Box(3) = {x0_3 - lTx_3/2, y0_3 - lTy_3/2, z0_3 - lTz_3, lTx_3, lTy_3, lTz_3};
//+
XMeshSize_4 = DefineNumber[ 0.5, Name "Box 4/Mesh/XMeshSize" ];
//+
YMeshSize_4 = DefineNumber[ 1.0, Name "Box 4/Mesh/YMeshSize" ];
//+
ZMeshSize_4 = DefineNumber[ 1.0, Name "Box 4/Mesh/ZMeshSize" ];
//+
lTx_4 = DefineNumber[ 8.0, Name "Box 4/Geometry/lTx" ];
//+
lTy_4 = DefineNumber[ 10.0, Name "Box 4/Geometry/lTy" ];
//+
lTz_4 = DefineNumber[ 7.0, Name "Box 4/Geometry/lTz" ];
//+
x0_4 = DefineNumber[ -6.0, Name "Box 4/Geometry/x0" ];
//+
y0_4 = DefineNumber[ 0.0, Name "Box 4/Geometry/y0" ];
//+
z0_4 = DefineNumber[ -5.0, Name "Box 4/Geometry/z0" ];
//+
Box(4) = {x0_4 - lTx_4/2, y0_4 - lTy_4/2, z0_4 - lTz_4, lTx_4, lTy_4, lTz_4};
//+
XMeshSize_5 = DefineNumber[ 0.25, Name "Box 5/Mesh/XMeshSize" ];
//+
YMeshSize_5 = DefineNumber[ 1.0, Name "Box 5/Mesh/YMeshSize" ];
//+
ZMeshSize_5 = DefineNumber[ 1.0, Name "Box 5/Mesh/ZMeshSize" ];
//+
lTx_5 = DefineNumber[ 4.0, Name "Box 5/Geometry/lTx" ];
//+
lTy_5 = DefineNumber[ 10.0, Name "Box 5/Geometry/lTy" ];
//+
lTz_5 = DefineNumber[ 7.0, Name "Box 5/Geometry/lTz" ];
//+
x0_5 = DefineNumber[ 0.0, Name "Box 5/Geometry/x0" ];
//+
y0_5 = DefineNumber[ 0.0, Name "Box 5/Geometry/y0" ];
//+
z0_5 = DefineNumber[ -5.0, Name "Box 5/Geometry/z0" ];
//+
Box(5) = {x0_5 - lTx_5/2, y0_5 - lTy_5/2, z0_5 - lTz_5, lTx_5, lTy_5, lTz_5};
//+
XMeshSize_6 = DefineNumber[ 0.5, Name "Box 6/Mesh/XMeshSize" ];
//+
YMeshSize_6 = DefineNumber[ 1.0, Name "Box 6/Mesh/YMeshSize" ];
//+
ZMeshSize_6 = DefineNumber[ 1.0, Name "Box 6/Mesh/ZMeshSize" ];
//+
lTx_6 = DefineNumber[ 8.0, Name "Box 6/Geometry/lTx" ];
//+
lTy_6 = DefineNumber[ 10.0, Name "Box 6/Geometry/lTy" ];
//+
lTz_6 = DefineNumber[ 7.0, Name "Box 6/Geometry/lTz" ];
//+
x0_6 = DefineNumber[ 6.0, Name "Box 6/Geometry/x0" ];
//+
y0_6 = DefineNumber[ 0.0, Name "Box 6/Geometry/y0" ];
//+
z0_6 = DefineNumber[ -5.0, Name "Box 6/Geometry/z0" ];
//+
Box(6) = {x0_6 - lTx_6/2, y0_6 - lTy_6/2, z0_6 - lTz_6, lTx_6, lTy_6, lTz_6};
//+
Coherence;
//+
transX_1 = Ceil(lTx_1/XMeshSize_1) + 1;
//+
// --- Robust selection + transfinite for Volume 1 ---
xmin_1 = (x0_1 - lTx_1/2); xmax_1 = (x0_1 + lTx_1/2);
ymin_1 = (y0_1 - lTy_1/2); ymax_1 = (y0_1 + lTy_1/2);
zmin_1 = (z0_1 - lTz_1); zmax_1 = (z0_1);
cX_1[] = {}; cY_1[] = {}; cZ_1[] = {};
cX_1[] += Curve In BoundingBox { xmin_1-eps, ymin_1-eps, zmin_1-eps,  xmax_1+eps, ymin_1+eps, zmin_1+eps };
cX_1[] += Curve In BoundingBox { xmin_1-eps, ymin_1-eps, zmax_1-eps,  xmax_1+eps, ymin_1+eps, zmax_1+eps };
cX_1[] += Curve In BoundingBox { xmin_1-eps, ymax_1-eps, zmin_1-eps,  xmax_1+eps, ymax_1+eps, zmin_1+eps };
cX_1[] += Curve In BoundingBox { xmin_1-eps, ymax_1-eps, zmax_1-eps,  xmax_1+eps, ymax_1+eps, zmax_1+eps };
cY_1[] += Curve In BoundingBox { xmin_1-eps, ymin_1-eps, zmin_1-eps,  xmin_1+eps, ymax_1+eps, zmin_1+eps };
cY_1[] += Curve In BoundingBox { xmin_1-eps, ymin_1-eps, zmax_1-eps,  xmin_1+eps, ymax_1+eps, zmax_1+eps };
cY_1[] += Curve In BoundingBox { xmax_1-eps, ymin_1-eps, zmin_1-eps,  xmax_1+eps, ymax_1+eps, zmin_1+eps };
cY_1[] += Curve In BoundingBox { xmax_1-eps, ymin_1-eps, zmax_1-eps,  xmax_1+eps, ymax_1+eps, zmax_1+eps };
cZ_1[] += Curve In BoundingBox { xmin_1-eps, ymin_1-eps, zmin_1-eps,  xmin_1+eps, ymin_1+eps, zmax_1+eps };
cZ_1[] += Curve In BoundingBox { xmin_1-eps, ymax_1-eps, zmin_1-eps,  xmin_1+eps, ymax_1+eps, zmax_1+eps };
cZ_1[] += Curve In BoundingBox { xmax_1-eps, ymin_1-eps, zmin_1-eps,  xmax_1+eps, ymin_1+eps, zmax_1+eps };
cZ_1[] += Curve In BoundingBox { xmax_1-eps, ymax_1-eps, zmin_1-eps,  xmax_1+eps, ymax_1+eps, zmax_1+eps };
cX_1[] = Abs(cX_1[]); cX_1[] = Unique(cX_1[]);
cY_1[] = Abs(cY_1[]); cY_1[] = Unique(cY_1[]);
cZ_1[] = Abs(cZ_1[]); cZ_1[] = Unique(cZ_1[]);
Transfinite Curve {cX_1[]} = transX_1 Using Progression 1;
Transfinite Curve {cY_1[]} = transY_global Using Progression 1;
Transfinite Curve {cZ_1[]} = transZ_L1 Using Progression 1;
s_1[] = Abs(Boundary{ Volume{1}; });
s_1[] = Unique(s_1[]);
Transfinite Surface {s_1[]};
Recombine Surface {s_1[]};
Transfinite Volume {1};
//+
transX_2 = Ceil(lTx_2/XMeshSize_2) + 1;
//+
// --- Robust selection + transfinite for Volume 2 ---
xmin_2 = (x0_2 - lTx_2/2); xmax_2 = (x0_2 + lTx_2/2);
ymin_2 = (y0_2 - lTy_2/2); ymax_2 = (y0_2 + lTy_2/2);
zmin_2 = (z0_2 - lTz_2); zmax_2 = (z0_2);
cX_2[] = {}; cY_2[] = {}; cZ_2[] = {};
cX_2[] += Curve In BoundingBox { xmin_2-eps, ymin_2-eps, zmin_2-eps,  xmax_2+eps, ymin_2+eps, zmin_2+eps };
cX_2[] += Curve In BoundingBox { xmin_2-eps, ymin_2-eps, zmax_2-eps,  xmax_2+eps, ymin_2+eps, zmax_2+eps };
cX_2[] += Curve In BoundingBox { xmin_2-eps, ymax_2-eps, zmin_2-eps,  xmax_2+eps, ymax_2+eps, zmin_2+eps };
cX_2[] += Curve In BoundingBox { xmin_2-eps, ymax_2-eps, zmax_2-eps,  xmax_2+eps, ymax_2+eps, zmax_2+eps };
cY_2[] += Curve In BoundingBox { xmin_2-eps, ymin_2-eps, zmin_2-eps,  xmin_2+eps, ymax_2+eps, zmin_2+eps };
cY_2[] += Curve In BoundingBox { xmin_2-eps, ymin_2-eps, zmax_2-eps,  xmin_2+eps, ymax_2+eps, zmax_2+eps };
cY_2[] += Curve In BoundingBox { xmax_2-eps, ymin_2-eps, zmin_2-eps,  xmax_2+eps, ymax_2+eps, zmin_2+eps };
cY_2[] += Curve In BoundingBox { xmax_2-eps, ymin_2-eps, zmax_2-eps,  xmax_2+eps, ymax_2+eps, zmax_2+eps };
cZ_2[] += Curve In BoundingBox { xmin_2-eps, ymin_2-eps, zmin_2-eps,  xmin_2+eps, ymin_2+eps, zmax_2+eps };
cZ_2[] += Curve In BoundingBox { xmin_2-eps, ymax_2-eps, zmin_2-eps,  xmin_2+eps, ymax_2+eps, zmax_2+eps };
cZ_2[] += Curve In BoundingBox { xmax_2-eps, ymin_2-eps, zmin_2-eps,  xmax_2+eps, ymin_2+eps, zmax_2+eps };
cZ_2[] += Curve In BoundingBox { xmax_2-eps, ymax_2-eps, zmin_2-eps,  xmax_2+eps, ymax_2+eps, zmax_2+eps };
cX_2[] = Abs(cX_2[]); cX_2[] = Unique(cX_2[]);
cY_2[] = Abs(cY_2[]); cY_2[] = Unique(cY_2[]);
cZ_2[] = Abs(cZ_2[]); cZ_2[] = Unique(cZ_2[]);
Transfinite Curve {cX_2[]} = transX_2 Using Progression 1;
Transfinite Curve {cY_2[]} = transY_global Using Progression 1;
Transfinite Curve {cZ_2[]} = transZ_L1 Using Progression 1;
s_2[] = Abs(Boundary{ Volume{2}; });
s_2[] = Unique(s_2[]);
Transfinite Surface {s_2[]};
Recombine Surface {s_2[]};
Transfinite Volume {2};
//+
transX_3 = Ceil(lTx_3/XMeshSize_3) + 1;
//+
// --- Robust selection + transfinite for Volume 3 ---
xmin_3 = (x0_3 - lTx_3/2); xmax_3 = (x0_3 + lTx_3/2);
ymin_3 = (y0_3 - lTy_3/2); ymax_3 = (y0_3 + lTy_3/2);
zmin_3 = (z0_3 - lTz_3); zmax_3 = (z0_3);
cX_3[] = {}; cY_3[] = {}; cZ_3[] = {};
cX_3[] += Curve In BoundingBox { xmin_3-eps, ymin_3-eps, zmin_3-eps,  xmax_3+eps, ymin_3+eps, zmin_3+eps };
cX_3[] += Curve In BoundingBox { xmin_3-eps, ymin_3-eps, zmax_3-eps,  xmax_3+eps, ymin_3+eps, zmax_3+eps };
cX_3[] += Curve In BoundingBox { xmin_3-eps, ymax_3-eps, zmin_3-eps,  xmax_3+eps, ymax_3+eps, zmin_3+eps };
cX_3[] += Curve In BoundingBox { xmin_3-eps, ymax_3-eps, zmax_3-eps,  xmax_3+eps, ymax_3+eps, zmax_3+eps };
cY_3[] += Curve In BoundingBox { xmin_3-eps, ymin_3-eps, zmin_3-eps,  xmin_3+eps, ymax_3+eps, zmin_3+eps };
cY_3[] += Curve In BoundingBox { xmin_3-eps, ymin_3-eps, zmax_3-eps,  xmin_3+eps, ymax_3+eps, zmax_3+eps };
cY_3[] += Curve In BoundingBox { xmax_3-eps, ymin_3-eps, zmin_3-eps,  xmax_3+eps, ymax_3+eps, zmin_3+eps };
cY_3[] += Curve In BoundingBox { xmax_3-eps, ymin_3-eps, zmax_3-eps,  xmax_3+eps, ymax_3+eps, zmax_3+eps };
cZ_3[] += Curve In BoundingBox { xmin_3-eps, ymin_3-eps, zmin_3-eps,  xmin_3+eps, ymin_3+eps, zmax_3+eps };
cZ_3[] += Curve In BoundingBox { xmin_3-eps, ymax_3-eps, zmin_3-eps,  xmin_3+eps, ymax_3+eps, zmax_3+eps };
cZ_3[] += Curve In BoundingBox { xmax_3-eps, ymin_3-eps, zmin_3-eps,  xmax_3+eps, ymin_3+eps, zmax_3+eps };
cZ_3[] += Curve In BoundingBox { xmax_3-eps, ymax_3-eps, zmin_3-eps,  xmax_3+eps, ymax_3+eps, zmax_3+eps };
cX_3[] = Abs(cX_3[]); cX_3[] = Unique(cX_3[]);
cY_3[] = Abs(cY_3[]); cY_3[] = Unique(cY_3[]);
cZ_3[] = Abs(cZ_3[]); cZ_3[] = Unique(cZ_3[]);
Transfinite Curve {cX_3[]} = transX_3 Using Progression 1;
Transfinite Curve {cY_3[]} = transY_global Using Progression 1;
Transfinite Curve {cZ_3[]} = transZ_L1 Using Progression 1;
s_3[] = Abs(Boundary{ Volume{3}; });
s_3[] = Unique(s_3[]);
Transfinite Surface {s_3[]};
Recombine Surface {s_3[]};
Transfinite Volume {3};
//+
transX_4 = Ceil(lTx_4/XMeshSize_4) + 1;
//+
// --- Robust selection + transfinite for Volume 4 ---
xmin_4 = (x0_4 - lTx_4/2); xmax_4 = (x0_4 + lTx_4/2);
ymin_4 = (y0_4 - lTy_4/2); ymax_4 = (y0_4 + lTy_4/2);
zmin_4 = (z0_4 - lTz_4); zmax_4 = (z0_4);
cX_4[] = {}; cY_4[] = {}; cZ_4[] = {};
cX_4[] += Curve In BoundingBox { xmin_4-eps, ymin_4-eps, zmin_4-eps,  xmax_4+eps, ymin_4+eps, zmin_4+eps };
cX_4[] += Curve In BoundingBox { xmin_4-eps, ymin_4-eps, zmax_4-eps,  xmax_4+eps, ymin_4+eps, zmax_4+eps };
cX_4[] += Curve In BoundingBox { xmin_4-eps, ymax_4-eps, zmin_4-eps,  xmax_4+eps, ymax_4+eps, zmin_4+eps };
cX_4[] += Curve In BoundingBox { xmin_4-eps, ymax_4-eps, zmax_4-eps,  xmax_4+eps, ymax_4+eps, zmax_4+eps };
cY_4[] += Curve In BoundingBox { xmin_4-eps, ymin_4-eps, zmin_4-eps,  xmin_4+eps, ymax_4+eps, zmin_4+eps };
cY_4[] += Curve In BoundingBox { xmin_4-eps, ymin_4-eps, zmax_4-eps,  xmin_4+eps, ymax_4+eps, zmax_4+eps };
cY_4[] += Curve In BoundingBox { xmax_4-eps, ymin_4-eps, zmin_4-eps,  xmax_4+eps, ymax_4+eps, zmin_4+eps };
cY_4[] += Curve In BoundingBox { xmax_4-eps, ymin_4-eps, zmax_4-eps,  xmax_4+eps, ymax_4+eps, zmax_4+eps };
cZ_4[] += Curve In BoundingBox { xmin_4-eps, ymin_4-eps, zmin_4-eps,  xmin_4+eps, ymin_4+eps, zmax_4+eps };
cZ_4[] += Curve In BoundingBox { xmin_4-eps, ymax_4-eps, zmin_4-eps,  xmin_4+eps, ymax_4+eps, zmax_4+eps };
cZ_4[] += Curve In BoundingBox { xmax_4-eps, ymin_4-eps, zmin_4-eps,  xmax_4+eps, ymin_4+eps, zmax_4+eps };
cZ_4[] += Curve In BoundingBox { xmax_4-eps, ymax_4-eps, zmin_4-eps,  xmax_4+eps, ymax_4+eps, zmax_4+eps };
cX_4[] = Abs(cX_4[]); cX_4[] = Unique(cX_4[]);
cY_4[] = Abs(cY_4[]); cY_4[] = Unique(cY_4[]);
cZ_4[] = Abs(cZ_4[]); cZ_4[] = Unique(cZ_4[]);
Transfinite Curve {cX_4[]} = transX_4 Using Progression 1;
Transfinite Curve {cY_4[]} = transY_global Using Progression 1;
Transfinite Curve {cZ_4[]} = transZ_L2 Using Progression 1;
s_4[] = Abs(Boundary{ Volume{4}; });
s_4[] = Unique(s_4[]);
Transfinite Surface {s_4[]};
Recombine Surface {s_4[]};
Transfinite Volume {4};
//+
transX_5 = Ceil(lTx_5/XMeshSize_5) + 1;
//+
// --- Robust selection + transfinite for Volume 5 ---
xmin_5 = (x0_5 - lTx_5/2); xmax_5 = (x0_5 + lTx_5/2);
ymin_5 = (y0_5 - lTy_5/2); ymax_5 = (y0_5 + lTy_5/2);
zmin_5 = (z0_5 - lTz_5); zmax_5 = (z0_5);
cX_5[] = {}; cY_5[] = {}; cZ_5[] = {};
cX_5[] += Curve In BoundingBox { xmin_5-eps, ymin_5-eps, zmin_5-eps,  xmax_5+eps, ymin_5+eps, zmin_5+eps };
cX_5[] += Curve In BoundingBox { xmin_5-eps, ymin_5-eps, zmax_5-eps,  xmax_5+eps, ymin_5+eps, zmax_5+eps };
cX_5[] += Curve In BoundingBox { xmin_5-eps, ymax_5-eps, zmin_5-eps,  xmax_5+eps, ymax_5+eps, zmin_5+eps };
cX_5[] += Curve In BoundingBox { xmin_5-eps, ymax_5-eps, zmax_5-eps,  xmax_5+eps, ymax_5+eps, zmax_5+eps };
cY_5[] += Curve In BoundingBox { xmin_5-eps, ymin_5-eps, zmin_5-eps,  xmin_5+eps, ymax_5+eps, zmin_5+eps };
cY_5[] += Curve In BoundingBox { xmin_5-eps, ymin_5-eps, zmax_5-eps,  xmin_5+eps, ymax_5+eps, zmax_5+eps };
cY_5[] += Curve In BoundingBox { xmax_5-eps, ymin_5-eps, zmin_5-eps,  xmax_5+eps, ymax_5+eps, zmin_5+eps };
cY_5[] += Curve In BoundingBox { xmax_5-eps, ymin_5-eps, zmax_5-eps,  xmax_5+eps, ymax_5+eps, zmax_5+eps };
cZ_5[] += Curve In BoundingBox { xmin_5-eps, ymin_5-eps, zmin_5-eps,  xmin_5+eps, ymin_5+eps, zmax_5+eps };
cZ_5[] += Curve In BoundingBox { xmin_5-eps, ymax_5-eps, zmin_5-eps,  xmin_5+eps, ymax_5+eps, zmax_5+eps };
cZ_5[] += Curve In BoundingBox { xmax_5-eps, ymin_5-eps, zmin_5-eps,  xmax_5+eps, ymin_5+eps, zmax_5+eps };
cZ_5[] += Curve In BoundingBox { xmax_5-eps, ymax_5-eps, zmin_5-eps,  xmax_5+eps, ymax_5+eps, zmax_5+eps };
cX_5[] = Abs(cX_5[]); cX_5[] = Unique(cX_5[]);
cY_5[] = Abs(cY_5[]); cY_5[] = Unique(cY_5[]);
cZ_5[] = Abs(cZ_5[]); cZ_5[] = Unique(cZ_5[]);
Transfinite Curve {cX_5[]} = transX_5 Using Progression 1;
Transfinite Curve {cY_5[]} = transY_global Using Progression 1;
Transfinite Curve {cZ_5[]} = transZ_L2 Using Progression 1;
s_5[] = Abs(Boundary{ Volume{5}; });
s_5[] = Unique(s_5[]);
Transfinite Surface {s_5[]};
Recombine Surface {s_5[]};
Transfinite Volume {5};
//+
transX_6 = Ceil(lTx_6/XMeshSize_6) + 1;
//+
// --- Robust selection + transfinite for Volume 6 ---
xmin_6 = (x0_6 - lTx_6/2); xmax_6 = (x0_6 + lTx_6/2);
ymin_6 = (y0_6 - lTy_6/2); ymax_6 = (y0_6 + lTy_6/2);
zmin_6 = (z0_6 - lTz_6); zmax_6 = (z0_6);
cX_6[] = {}; cY_6[] = {}; cZ_6[] = {};
cX_6[] += Curve In BoundingBox { xmin_6-eps, ymin_6-eps, zmin_6-eps,  xmax_6+eps, ymin_6+eps, zmin_6+eps };
cX_6[] += Curve In BoundingBox { xmin_6-eps, ymin_6-eps, zmax_6-eps,  xmax_6+eps, ymin_6+eps, zmax_6+eps };
cX_6[] += Curve In BoundingBox { xmin_6-eps, ymax_6-eps, zmin_6-eps,  xmax_6+eps, ymax_6+eps, zmin_6+eps };
cX_6[] += Curve In BoundingBox { xmin_6-eps, ymax_6-eps, zmax_6-eps,  xmax_6+eps, ymax_6+eps, zmax_6+eps };
cY_6[] += Curve In BoundingBox { xmin_6-eps, ymin_6-eps, zmin_6-eps,  xmin_6+eps, ymax_6+eps, zmin_6+eps };
cY_6[] += Curve In BoundingBox { xmin_6-eps, ymin_6-eps, zmax_6-eps,  xmin_6+eps, ymax_6+eps, zmax_6+eps };
cY_6[] += Curve In BoundingBox { xmax_6-eps, ymin_6-eps, zmin_6-eps,  xmax_6+eps, ymax_6+eps, zmin_6+eps };
cY_6[] += Curve In BoundingBox { xmax_6-eps, ymin_6-eps, zmax_6-eps,  xmax_6+eps, ymax_6+eps, zmax_6+eps };
cZ_6[] += Curve In BoundingBox { xmin_6-eps, ymin_6-eps, zmin_6-eps,  xmin_6+eps, ymin_6+eps, zmax_6+eps };
cZ_6[] += Curve In BoundingBox { xmin_6-eps, ymax_6-eps, zmin_6-eps,  xmin_6+eps, ymax_6+eps, zmax_6+eps };
cZ_6[] += Curve In BoundingBox { xmax_6-eps, ymin_6-eps, zmin_6-eps,  xmax_6+eps, ymin_6+eps, zmax_6+eps };
cZ_6[] += Curve In BoundingBox { xmax_6-eps, ymax_6-eps, zmin_6-eps,  xmax_6+eps, ymax_6+eps, zmax_6+eps };
cX_6[] = Abs(cX_6[]); cX_6[] = Unique(cX_6[]);
cY_6[] = Abs(cY_6[]); cY_6[] = Unique(cY_6[]);
cZ_6[] = Abs(cZ_6[]); cZ_6[] = Unique(cZ_6[]);
Transfinite Curve {cX_6[]} = transX_6 Using Progression 1;
Transfinite Curve {cY_6[]} = transY_global Using Progression 1;
Transfinite Curve {cZ_6[]} = transZ_L2 Using Progression 1;
s_6[] = Abs(Boundary{ Volume{6}; });
s_6[] = Unique(s_6[]);
Transfinite Surface {s_6[]};
Recombine Surface {s_6[]};
Transfinite Volume {6};