//
//+
lxTot = DefineNumber[ 30, Name "Parameters/lxTot" ];
//+
lyTot = DefineNumber[ 30, Name "Parameters/lyTot" ];
//+
lzTot = DefineNumber[ 30, Name "Parameters/lzTot" ];
//+
hLayer1 = 20; hLayer2 = 8; hLayer3 = 2;
//+
SetFactory("OpenCASCADE");
Box(1) = {-lxTot/2, -lyTot/2, -lzTot, lxTot, lyTot, hLayer1};
//+
Box(2) = {-lxTot/2, -lyTot/2, -(lzTot - hLayer1), lxTot, lyTot, hLayer2};
//+
Box(3) = {-lxTot/2, -lyTot/2, -(lzTot - hLayer1 - hLayer2), lxTot, lyTot, hLayer3};
//+
Coherence;
//+
// sElemZ = 0.5; sElemY = 10; sElemX = 10;
sElemZ = 0.5; sElemY = 5; sElemX = 5;
transZ1 = hLayer1 / sElemZ;
transZ2 = hLayer2 / sElemZ;
transZ3 = hLayer3 / sElemZ;
transX = lxTot / sElemX;
transY = lyTot / sElemY;
//+
Transfinite Curve {5, 7, 1, 3} = Ceil(transZ1) + 1 Using Progression 1;
//+
Transfinite Curve {16, 18, 13, 15} = Ceil(transZ2) + 1 Using Progression 1;
//+
Transfinite Curve {24, 26, 21, 23} = Ceil(transZ3) + 1 Using Progression 1;
//+
Transfinite Curve {25, 17, 6, 8, 22, 14, 2, 4} = Ceil(transY) + 1 Using Progression 1;
//+
Transfinite Curve {27, 19, 10, 9, 28, 20, 12, 11} = Ceil(transX) + 1 Using Progression 1;
//+
Transfinite Surface {:};
//+
Recombine Surface {:};
//+
Transfinite Volume {:};
