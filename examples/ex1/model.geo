//
//+
Point(1) = {0.0, 0.0, 0.0, 1.0};
//+
Point(2) = {1.0, 0.0, 0.0, 1.0};
//+
Point(3) = {1.0, 1.0, 0.0, 1.0};
//+
Point(4) = {0.0, 1.0, 0.0, 1.0};
//+
Line(1) = {1, 2};
//+
Line(2) = {4, 3};
//+
Line(3) = {2, 3};
//+
Line(4) = {1, 4};
//+
Curve Loop(1) = {1, 3, -2, -4};
//+
Plane Surface(1) = {1};
//+
Transfinite Curve {4, 3, 2, 1} = 2 Using Progression 1;
//+
Transfinite Surface {1};
//+
Recombine Surface {1};
