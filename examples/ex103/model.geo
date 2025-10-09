//
hSoil = DefineNumber[ 40.0, Name "Parameters/hSoil" ];
//+
thickX = DefineNumber[ 0.2, Name "Parameters/thickX" ];
//+
transX = DefineNumber[ 2, Name "Parameters/transX" ];
//+
transY = DefineNumber[ 161, Name "Parameters/transY" ];
//+
Point(1) = {0.0, 0.0, 0.0, 1.0};
//+
Point(2) = {thickX, 0.0, 0.0, 1.0};
//+
Point(3) = {thickX, hSoil, 0.0, 1.0};
//+
Point(4) = {0.0, hSoil, 0.0, 1.0};

//+
Line(1) = {1, 2};
//+
Line(2) = {2, 3};
//+
Line(3) = {4, 3};
//+
Line(4) = {1, 4};
//+
Curve Loop(1) = {1, 2, -3, -4};
//+
Plane Surface(1) = {1};
//+
Transfinite Curve {4, 2} = transY Using Progression 1;
//+
Transfinite Curve {1, 3} = transX Using Progression 1;
//+
Transfinite Surface {1};
//+
Recombine Surface {1};
