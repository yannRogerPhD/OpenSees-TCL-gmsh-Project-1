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
Point(5) = {0, 0, 1, 1.0};
//+
Point(6) = {1, 0, 1, 1.0};
//+
Point(7) = {1, 1, 1, 1.0};
//+
Point(8) = {0, 1, 1, 1.0};
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
Line(5) = {5, 6};
//+
Line(6) = {6, 7};
//+
Line(7) = {8, 7};
//+
Line(8) = {5, 8};
//+
Curve Loop(2) = {5, 6, -7, -8};
//+
Plane Surface(2) = {2};
//+
Line(9) = {2, 6};
//+
Line(10) = {3, 7};
//+
Curve Loop(3) = {9, 6, -10, -2};
//+
Plane Surface(3) = {3};
//+
Line(11) = {1, 5};
//+
Line(12) = {4, 8};
//+
Curve Loop(4) = {11, 8, -12, -4};
//+
Plane Surface(4) = {4};
//+
Curve Loop(5) = {1, 9, -5, -11};
//+
Plane Surface(5) = {5};
//+
Curve Loop(6) = {3, 10, -7, -12};
//+
Plane Surface(6) = {6};
//+
Surface Loop(1) = {1, 2, 3, 4, 5, 6};
//+
Volume(1) = {1};

//
//+
Transfinite Curve {8, 6, 2, 4} = 2 Using Progression 1;
//+
Transfinite Curve {7, 5, 1, 3} = 2 Using Progression 1;
//+
Transfinite Curve {12, 10, 9, 11} = 2 Using Progression 1;
//+
Transfinite Surface {1};
//+
Transfinite Surface {2};
//+
Transfinite Surface {3};
//+
Transfinite Surface {4};
//+
Transfinite Surface {5};
//+
Transfinite Surface {6};
//+
Transfinite Volume{1};
//+
Recombine Surface {1, 2, 3, 4, 5, 6};
