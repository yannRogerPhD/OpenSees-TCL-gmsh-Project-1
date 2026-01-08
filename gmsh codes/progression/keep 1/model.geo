//
SetFactory("OpenCASCADE");
//+
lTx_stack = DefineNumber[ 20.0, Name "Stack/Geometry/lTx" ];
//+
lTy_stack = DefineNumber[ 10.0, Name "Stack/Geometry/lTy" ];
//+
XMeshSize_stack = DefineNumber[ 1.0, Name "Stack/Mesh/XMeshSize" ];
//+
YMeshSize_stack = DefineNumber[ 1.0, Name "Stack/Mesh/YMeshSize" ];
//+
transX_stack = Ceil(lTx_stack/XMeshSize_stack) + 1;
//+
transY_stack = Ceil(lTy_stack/YMeshSize_stack) + 1;
//+
ZMeshSize_1 = DefineNumber[ 0.5, Name "Box 1/Mesh/ZMeshSize" ];
//+
lTz_1 = DefineNumber[ 2.0, Name "Box 1/Geometry/lTz" ];
//+
x0_1 = DefineNumber[ 0.0, Name "Box 1/Geometry/x0" ];
//+
y0_1 = DefineNumber[ 0.0, Name "Box 1/Geometry/y0" ];
//+
z0_1 = DefineNumber[ 0.0, Name "Box 1/Geometry/z0" ];
//+
Box(1) = {x0_1 - lTx_stack/2, y0_1 - lTy_stack/2, z0_1 - lTz_1, lTx_stack, lTy_stack, lTz_1};
//+
transZ_1 = Ceil(lTz_1/ZMeshSize_1) + 1;
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
ZMeshSize_2 = DefineNumber[ 1.0, Name "Box 2/Mesh/ZMeshSize" ];
//+
lTz_2 = DefineNumber[ 5.0, Name "Box 2/Geometry/lTz" ];
//+
x0_2 = DefineNumber[ 0.0, Name "Box 2/Geometry/x0" ];
//+
y0_2 = DefineNumber[ 0.0, Name "Box 2/Geometry/y0" ];
//+
z0_2 = DefineNumber[ -2.0, Name "Box 2/Geometry/z0" ];
//+
Box(2) = {x0_2 - lTx_stack/2, y0_2 - lTy_stack/2, z0_2 - lTz_2, lTx_stack, lTy_stack, lTz_2};
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
ZMeshSize_3 = DefineNumber[ 0.5, Name "Box 3/Mesh/ZMeshSize" ];
//+
lTz_3 = DefineNumber[ 3.0, Name "Box 3/Geometry/lTz" ];
//+
x0_3 = DefineNumber[ 0.0, Name "Box 3/Geometry/x0" ];
//+
y0_3 = DefineNumber[ 0.0, Name "Box 3/Geometry/y0" ];
//+
z0_3 = DefineNumber[ -7.0, Name "Box 3/Geometry/z0" ];
//+
Box(3) = {x0_3 - lTx_stack/2, y0_3 - lTy_stack/2, z0_3 - lTz_3, lTx_stack, lTy_stack, lTz_3};
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
