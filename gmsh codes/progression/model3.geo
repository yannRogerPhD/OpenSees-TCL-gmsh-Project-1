//
SetFactory("OpenCASCADE");
// ---- PREAMBLE (shared parameters / derived counts) ----
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
transX_1 = Ceil(lTx_1/XMeshSize_1) + 1;
//+
Transfinite Curve {1, 3, 5, 7} = transZ_L1 Using Progression 1;
Transfinite Curve {9, 10, 11, 12} = transX_1 Using Progression 1;
Transfinite Curve {2, 4, 6, 8} = transY_global Using Progression 1;
//+
Transfinite Surface {1:6};
//+
Recombine Surface {1:6};
//+
Transfinite Volume {1};
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
transX_2 = Ceil(lTx_2/XMeshSize_2) + 1;
//+
Transfinite Curve {13, 15, 17, 19} = transZ_L1 Using Progression 1;
Transfinite Curve {21, 22, 23, 24} = transX_2 Using Progression 1;
Transfinite Curve {14, 16, 18, 20} = transY_global Using Progression 1;
//+
Transfinite Surface {7:12};
//+
Recombine Surface {7:12};
//+
Transfinite Volume {2};
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
transX_3 = Ceil(lTx_3/XMeshSize_3) + 1;
//+
Transfinite Curve {25, 27, 29, 31} = transZ_L1 Using Progression 1;
Transfinite Curve {33, 34, 35, 36} = transX_3 Using Progression 1;
Transfinite Curve {26, 28, 30, 32} = transY_global Using Progression 1;
//+
Transfinite Surface {13:18};
//+
Recombine Surface {13:18};
//+
Transfinite Volume {3};
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
transX_4 = Ceil(lTx_4/XMeshSize_4) + 1;
//+
Transfinite Curve {37, 39, 41, 43} = transZ_L2 Using Progression 1;
Transfinite Curve {45, 46, 47, 48} = transX_4 Using Progression 1;
Transfinite Curve {38, 40, 42, 44} = transY_global Using Progression 1;
//+
Transfinite Surface {19:24};
//+
Recombine Surface {19:24};
//+
Transfinite Volume {4};
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
transX_5 = Ceil(lTx_5/XMeshSize_5) + 1;
//+
Transfinite Curve {49, 51, 53, 55} = transZ_L2 Using Progression 1;
Transfinite Curve {57, 58, 59, 60} = transX_5 Using Progression 1;
Transfinite Curve {50, 52, 54, 56} = transY_global Using Progression 1;
//+
Transfinite Surface {25:30};
//+
Recombine Surface {25:30};
//+
Transfinite Volume {5};
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
transX_6 = Ceil(lTx_6/XMeshSize_6) + 1;
//+
Transfinite Curve {61, 63, 65, 67} = transZ_L2 Using Progression 1;
Transfinite Curve {69, 70, 71, 72} = transX_6 Using Progression 1;
Transfinite Curve {62, 64, 66, 68} = transY_global Using Progression 1;
//+
Transfinite Surface {31:36};
//+
Recombine Surface {31:36};
//+
Transfinite Volume {6};
//+
Transfinite Surface {1:36};
//+
Recombine Surface {1:36};
//+
Transfinite Volume {1:6};
