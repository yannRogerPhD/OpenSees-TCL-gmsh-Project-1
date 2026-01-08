//
SetFactory("OpenCASCADE");
//+
XMeshSize_1 = DefineNumber[ 1.0, Name "Box 1/Mesh/XMeshSize" ];
//+
YMeshSize_1 = DefineNumber[ 1.0, Name "Box 1/Mesh/YMeshSize" ];
//+
ZMeshSize_1 = DefineNumber[ 0.5, Name "Box 1/Mesh/ZMeshSize" ];
//+
lTx_1 = DefineNumber[ 20.0, Name "Box 1/Geometry/lTx" ];
//+
lTy_1 = DefineNumber[ 10.0, Name "Box 1/Geometry/lTy" ];
//+
lTz_1 = DefineNumber[ 2.0, Name "Box 1/Geometry/lTz" ];
//+
x0_1 = DefineNumber[ 0.0, Name "Box 1/Geometry/x0" ];
//+
y0_1 = DefineNumber[ 0.0, Name "Box 1/Geometry/y0" ];
//+
z0_1 = DefineNumber[ 0.0, Name "Box 1/Geometry/z0" ];
//+
Box(1) = {x0_1 - lTx_1/2, y0_1 - lTy_1/2, z0_1 - lTz_1, lTx_1, lTy_1, lTz_1};
//+
transZ_1 = Ceil(lTz_1/ZMeshSize_1) + 1;
//+
transX_stack = Ceil(lTx_1/XMeshSize_1) + 1;
//+
transY_stack = Ceil(lTy_1/YMeshSize_1) + 1;
//+
Transfinite Curve {1, 3, 5, 7} = transZ_1 Using Progression 1;
Transfinite Curve {9, 10, 11, 12} = transX_stack Using Progression 1;
Transfinite Curve {2, 4, 6, 8} = transY_stack Using Progression 1;
//+
Transfinite Surface {1:6};
//+
Recombine Surface {1:6};
//+
Transfinite Volume {1};
//+
XMeshSize_2 = DefineNumber[ 1.0, Name "Box 2/Mesh/XMeshSize" ];
//+
YMeshSize_2 = DefineNumber[ 1.0, Name "Box 2/Mesh/YMeshSize" ];
//+
ZMeshSize_2 = DefineNumber[ 1.0, Name "Box 2/Mesh/ZMeshSize" ];
//+
lTx_2 = DefineNumber[ 20.0, Name "Box 2/Geometry/lTx" ];
//+
lTy_2 = DefineNumber[ 10.0, Name "Box 2/Geometry/lTy" ];
//+
lTz_2 = DefineNumber[ 5.0, Name "Box 2/Geometry/lTz" ];
//+
x0_2 = DefineNumber[ 0.0, Name "Box 2/Geometry/x0" ];
//+
y0_2 = DefineNumber[ 0.0, Name "Box 2/Geometry/y0" ];
//+
z0_2 = DefineNumber[ -2.0, Name "Box 2/Geometry/z0" ];
//+
Box(2) = {x0_2 - lTx_2/2, y0_2 - lTy_2/2, z0_2 - lTz_2, lTx_2, lTy_2, lTz_2};
//+
transZ_2 = Ceil(lTz_2/ZMeshSize_2) + 1;
//+
Transfinite Curve {13, 15, 17, 19} = transZ_2 Using Progression 1;
Transfinite Curve {21, 22, 23, 24} = transX_stack Using Progression 1;
Transfinite Curve {14, 16, 18, 20} = transY_stack Using Progression 1;
//+
Transfinite Surface {7:12};
//+
Recombine Surface {7:12};
//+
Transfinite Volume {2};
//+
XMeshSize_3 = DefineNumber[ 1.0, Name "Box 3/Mesh/XMeshSize" ];
//+
YMeshSize_3 = DefineNumber[ 1.0, Name "Box 3/Mesh/YMeshSize" ];
//+
ZMeshSize_3 = DefineNumber[ 0.5, Name "Box 3/Mesh/ZMeshSize" ];
//+
lTx_3 = DefineNumber[ 20.0, Name "Box 3/Geometry/lTx" ];
//+
lTy_3 = DefineNumber[ 10.0, Name "Box 3/Geometry/lTy" ];
//+
lTz_3 = DefineNumber[ 3.0, Name "Box 3/Geometry/lTz" ];
//+
x0_3 = DefineNumber[ 0.0, Name "Box 3/Geometry/x0" ];
//+
y0_3 = DefineNumber[ 0.0, Name "Box 3/Geometry/y0" ];
//+
z0_3 = DefineNumber[ -7.0, Name "Box 3/Geometry/z0" ];
//+
Box(3) = {x0_3 - lTx_3/2, y0_3 - lTy_3/2, z0_3 - lTz_3, lTx_3, lTy_3, lTz_3};
//+
transZ_3 = Ceil(lTz_3/ZMeshSize_3) + 1;
//+
Transfinite Curve {25, 27, 29, 31} = transZ_3 Using Progression 1;
Transfinite Curve {33, 34, 35, 36} = transX_stack Using Progression 1;
Transfinite Curve {26, 28, 30, 32} = transY_stack Using Progression 1;
//+
Transfinite Surface {13:18};
//+
Recombine Surface {13:18};
//+
Transfinite Volume {3};