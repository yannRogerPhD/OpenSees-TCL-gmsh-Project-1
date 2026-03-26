//
x0 = 0; y0 = 0;
//+
zMeshDense = 2; zMeshMedDense = 2; zMeshLoose = 2;
//+
lx1 = DefineNumber[ 2, Name "Parameters/initDims/lx1" ];
//+
ly1 = DefineNumber[ 2, Name "Parameters/initDims/ly1" ];
//+
transX1 = DefineNumber[ 2, Name "Parameters/initDims/transX1" ];
//+
transY1 = DefineNumber[ 2, Name "Parameters/initDims/transY1" ];
//+
zLoose = DefineNumber[ 30, Name "Parameters/zLoose" ];
zTransLoose = Ceil(zLoose/zMeshLoose) + 1;
//+
zMedDense = DefineNumber[ 30, Name "Parameters//zMedDense" ];
zTransMedDense = Ceil(zMedDense/zMeshMedDense) + 1;
//+ 
zDense = DefineNumber[ 36, Name "Parameters//zDense" ];
zTransDense = Ceil(zDense/zMeshDense) + 1;
//+
zLayer1 = 1; zLayer2 = zLayer1; zLayer3 = zLayer1; zLayer4 = zLayer1;
//+
SetFactory("OpenCASCADE");
//+
Box(1) = {x0, y0, -zLayer1, lx1, ly1, zLayer1};
//+
Box(2) = {x0, y0, -(zLayer1 + zLayer2), lx1, ly1, zLayer2};
//+
Box(3) = {x0, y0, -(zLayer1 + zLayer2 + zLayer3), lx1, ly1, zLayer3};
//+
Box(4) = {x0, y0, -(zLayer1 + zLayer2 + zLayer3 + zLayer4), lx1, ly1, zLayer4};
//+
Box(5) = {x0, y0, -(zLayer1 + zLayer2 + zLayer3 + zLayer4 + zLoose), lx1, ly1, zLoose};
//+
Box(6) = {x0, y0, -(zLayer1 + zLayer2 + zLayer3 + zLayer4 + zLoose + zMedDense), lx1, ly1, zMedDense};
//+
Box(7) = {x0, y0, -(zLayer1 + zLayer2 + zLayer3 + zLayer4 + zLoose + zMedDense + zDense), lx1, ly1, zDense};
//
Coherence;
//+
Transfinite Curve {10, 9, 19, 27, 35, 43, 51, 59, 12, 11, 20, 28, 36, 44, 52, 60} = transX1 Using Progression 1;
//+
Transfinite Curve {2, 4, 15, 23, 31, 39, 47, 55, 6, 8, 18, 26, 34, 42, 50, 58} = transY1 Using Progression 1;
//+
Transfinite Curve {29, 32, 30, 33, 21, 24, 22, 25, 13, 16, 14, 17, 1, 5, 3, 7} = 2 Using Progression 1;
//+
Transfinite Curve {53, 56, 54, 57} = zTransDense Using Progression 1;
//+
Transfinite Curve {45, 48, 46, 49} = zTransMedDense Using Progression 1;
//+
Transfinite Curve {37, 40, 38, 41} = zTransLoose Using Progression 1;
//+
// Transfinite Curve {41, 37, 43, 39, 29, 25, 31, 27, 17, 13, 19, 15, 5, 1, 7, 3} = 2 Using Progression 1;
//+
Transfinite Surface {:};
//+
Recombine Surface {:};
//+
Transfinite Volume {:};
