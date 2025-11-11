//
//+
//+
Point(1) = {0, 0, 0, 1.0};
//+
Point(2) = {1, 0, 0, 1.0};
//+
Point(3) = {1, 1, 0, 1.0};
//+
Point(4) = {0, 1, 0, 1.0};
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
Transfinite Curve {4, 2} = 5 Using Progression 1;
//+
Transfinite Curve {3, 1} = 2 Using Progression 1;
//+
Transfinite Surface {1};
//+
Recombine Surface {1};
//+
Point(5) = {0, 2, 0, 1.0};
//+
Point(6) = {1, 2, 0, 1.0};
//+
Line(5) = {3, 6};
//+
Line(6) = {6, 5};
//+
Line(7) = {5, 4};
//+
Curve Loop(2) = {3, -7, -6, -5};
//+
Plane Surface(2) = {2};
//+
Transfinite Curve {7, 5} = 6 Using Progression 1;
//+
Transfinite Curve {3, 6} = 2 Using Progression 1;
//+
Transfinite Surface {2};
//+
Recombine Surface {2};

//+
Physical Surface("quad4", 8) = {1};
//+
Physical Surface("quadUP", 9) = {2};
//+
Point(7) = {1, 1, 0, 1.0};
//+
Point(8) = {1, 2, 0, 1.0};
//+
Line(8) = {7, 8};
//+
Transfinite Curve {8} = 10 Using Progression 1;
