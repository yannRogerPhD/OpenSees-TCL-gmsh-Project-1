//
//+
Point(1) = {0, 0, 0, 1.0};
//+
Point(2) = {1, 0, 0, 1.0};
//+
Point(3) = {1, 1, 0, 1.0};
//+
Point(4) = {0, 1, 0, 1.0};
//+
Point(5) = {0, 2, 0, 1.0};
//+
Point(6) = {1, 2, 0, 1.0};
//+
Line(1) = {1, 2};
//+
Line(2) = {4, 3};
//+
Line(3) = {5, 6};
//+
Line(4) = {2, 3};
//+
Line(5) = {3, 6};
//+
Line(6) = {1, 4};
//+
Line(7) = {4, 5};

//+
Curve Loop(1) = {1, 4, -2, -6};
//+
Plane Surface(1) = {1};
//+
Curve Loop(2) = {2, 5, -3, -7};
//+
Plane Surface(2) = {2};
//+
Transfinite Curve {6, 4} = 8 Using Progression 1;
//+
Transfinite Curve {7, 5} = 6 Using Progression 1;
//+
Transfinite Curve {1, 2, 3} = 4 Using Progression 1;
//+
Transfinite Surface {1};
//+
Transfinite Surface {2};
//+
Recombine Surface {1, 2};
