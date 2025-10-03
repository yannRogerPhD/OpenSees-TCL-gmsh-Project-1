//
//+
thickX = DefineNumber[ 2.0, Name "Parameters/thickX" ];
thickY1 = DefineNumber[ 20.0, Name "Parameters/thickY1" ];
thickY2 = DefineNumber[ 8.0, Name "Parameters/thickY2" ];
thickY3 = DefineNumber[ 2.0, Name "Parameters/thickY3" ];
//+
Point(1) = {0, 0, 0, 1.0};
//+
Point(2) = {thickX, 0, 0, 1.0};
//+
Point(3) = {thickX, thickY1, 0, 1.0};
//+
Point(4) = {0.0, thickY1, 0, 1.0};
//+
Point(5) = {0.0, thickY1 + thickY2, 0, 1.0};
//+
Point(6) = {thickX, thickY1 + thickY2, 0, 1.0};
//+
Point(7) = {thickX, thickY1 + thickY2 + thickY3, 0, 1.0};
//+
Point(8) = {0.0, thickY1 + thickY2 + thickY3, 0, 1.0};

//+
Line(1) = {1, 2};
//+
Line(2) = {4, 3};
//+
Line(3) = {5, 6};
//+
Line(4) = {8, 7};
//+
Line(5) = {1, 4};
//+
Line(6) = {4, 5};
//+
Line(7) = {5, 8};
//+
Line(8) = {2, 3};
//+
Line(9) = {3, 6};
//+
Line(10) = {6, 7};
//+
Curve Loop(1) = {1, 8, -2, -5};
//+
Plane Surface(1) = {1};
//+
Curve Loop(2) = {2, 9, -3, -6};
//+
Plane Surface(2) = {2};
//+
Curve Loop(3) = {3, 10, -4, -7};
//+
Plane Surface(3) = {3};
//+
Transfinite Curve {5, 8} = 51 Using Progression 1;
//+
Transfinite Curve {6, 9} = 17 Using Progression 1;
//+
Transfinite Curve {7, 10} = 5 Using Progression 1;
//+
Transfinite Curve {4, 3, 2, 1} = 2 Using Progression 1;
//+
Transfinite Surface {1};
//+
Transfinite Surface {2};
//+
Transfinite Surface {3};
//+
Recombine Surface {1, 2, 3};
