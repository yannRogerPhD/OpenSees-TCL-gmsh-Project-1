//
thickX = DefineNumber[ 10, Name "Parameters/thickX" ];
thickY = DefineNumber[ 30, Name "Parameters/thickY" ];
//+
Point(1) = {0, 0, 0, 1.0};
//+
Point(2) = {thickX, 0, 0, 1.0};
//+
Point(3) = {thickX, thickY, 0, 1.0};
//+
Point(4) = {0.0, thickY, 0, 1.0};
//+

//+
Line(1) = {1, 2};
//+
Line(2) = {2, 3};
//+
Line(3) = {3, 4};
//+
Line(4) = {4, 1};
//+
Curve Loop(1) = {1, 2, 3, 4};
//+
Plane Surface(1) = {1};
//+
Transfinite Curve {4, 2} = 23 Using Progression 1;
//+
Transfinite Curve {3, 1} = 11 Using Progression 1;
//+
Transfinite Surface {1};
//+
Recombine Surface {1};
