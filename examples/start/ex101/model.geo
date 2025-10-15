//
//+
thickX = DefineNumber[ 2.0, Name "Parameters/thickX" ];
//+
Point(1) = {0, 0, 0, 1.0};
//+
Point(2) = {thickX, 0, 0, 1.0};
//+
Point(3) = {thickX, 20, 0, 1.0};
//+
Point(4) = {0, 20, 0, 1.0};
//+
Point(5) = {0, 28, 0, 1.0};
//+
Point(6) = {thickX, 28, 0, 1.0};
//+
Point(7) = {thickX, 30, 0, 1.0};
//+
Point(8) = {0, 30, 0, 1.0};
//+
//+
Line(1) = {1, 2};
//+
Line(2) = {4, 3};
//+
Line(3) = {5, 6};
//+
Line(4) = {8, 7};
//+
Line(5) = {2, 3};
//+
Line(6) = {3, 6};
//+
Line(7) = {6, 7};
//+
Line(8) = {1, 4};
//+
Line(9) = {4, 5};
//+
Line(10) = {5, 8};
//+
Curve Loop(1) = {1, 5, -2, -8};
//+
Plane Surface(1) = {1};
//+
Curve Loop(2) = {2, 6, -3, -9};
//+
Plane Surface(2) = {2};
//+
Curve Loop(3) = {3, 7, -4, -10};
//+
Plane Surface(3) = {3};
//+
Transfinite Curve {8, 5} = 41 Using Progression 1;
//+
Transfinite Curve {9, 6} = 17 Using Progression 1;
//+
Transfinite Curve {10, 7} = 5 Using Progression 1;
//+
Transfinite Curve {1, 2, 3, 4} = 2 Using Progression 1;
//+
Transfinite Surface {1};
//+
Transfinite Surface {2};
//+
Transfinite Surface {3};
//+
Recombine Surface {1, 2, 3};
