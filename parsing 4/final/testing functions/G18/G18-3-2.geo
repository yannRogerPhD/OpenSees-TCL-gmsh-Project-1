//
//+
Point(1) = {0, 0, 0, 1.0};
//+
Point(2) = {0, 1, 0, 1.0};
//+
//+
Point(3) = {1, 0, 0, 1.0};
//+
Point(4) = {1, 1, 0, 1.0};
//+
Line(1) = {1, 3};
//+
Line(2) = {3, 4};
//+
Line(3) = {2, 4};
//+
Line(4) = {1, 2};
//+
Transfinite Curve {4, 2} = 9 Using Progression 1;
//+
Transfinite Curve {3, 1} = 7 Using Progression 1;
//+
Curve Loop(1) = {1, 2, -3, -4};
//+
Plane Surface(1) = {1};
//+
Transfinite Surface {1};
//+
Recombine Surface {1};
//+
Point(5) = {0.35, 0.5, 0, 1.0};
//+
Point(6) = {0.35, 1.25, 0, 1.0};
//+
Point(7) = {0.65, 1.25, 0, 1.0};
//+
Point(8) = {0.65, 0.5, 0, 1.0};
//+
Line(5) = {5, 6};
//+
Line(6) = {6, 7};
//+
Line(7) = {8, 7};
//+
Transfinite Curve {5, 7} = 7 Using Progression 1;
//+
Transfinite Curve {6} = 5 Using Progression 1;
