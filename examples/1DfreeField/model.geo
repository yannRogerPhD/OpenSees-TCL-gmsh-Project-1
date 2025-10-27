//
//+
hSoil = DefineNumber[ 30.0, Name "Parameters/hSoil" ];
//+
thickX = DefineNumber[ 0.25, Name "Parameters/thickX" ];
//+
thickASD = DefineNumber[ 5, Name "Parameters/thickX" ];
//+
transX = DefineNumber[ 30, Name "Parameters/transX" ];
//+
Point(1) = {0, 0, 0, 1.0};
//+
Point(2) = {thickX, 0, 0, 1.0};
//+
Point(3) = {thickX, hSoil, 0, 1.0};
//+
Point(4) = {0, hSoil, 0, 1.0};
//+
Point(5) = {0, - thickASD, 0, 1.0};
//+
Point(6) = {thickX, - thickASD, 0, 1.0};
//+
Line(1) = {1, 2};
//+
Line(2) = {4, 3};
//+
Line(3) = {5, 6};
//+
Line(4) = {6, 2};
//+
Line(5) = {2, 3};
//+
Line(6) = {5, 1};
//+
Line(7) = {1, 4};
//+
Curve Loop(1) = {1, 5, -2, -7};
//+
Plane Surface(1) = {1};
//+
Curve Loop(2) = {3, 4, -1, -6};
//+
Plane Surface(2) = {2};
//+
Transfinite Curve {7, 5} = 30 Using Progression 1;
//+
Transfinite Curve {2, 1, 3} = 2 Using Progression 1;
//+
Transfinite Curve {6, 4} = 2 Using Progression 1;
//+
Transfinite Surface {2};
//+
Transfinite Surface {1};
//+
Recombine Surface {2, 1};
