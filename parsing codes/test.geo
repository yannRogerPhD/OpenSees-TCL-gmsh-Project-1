//
//+
Point(1) = {0, 0, 0, 1.0};
//+
Point(2) = {0, 0, 1, 1.0};
//+
Point(3) = {0, 1, 0, 1.0};
//+
Point(4) = {0, 1, 1, 1.0};
//+
Point(5) = {1, 0, 0, 1.0};
//+
Point(6) = {1, 0, 1, 1.0};
//+
Point(7) = {1, 1, 0, 1.0};
//+
Point(8) = {1, 1, 1, 1.0};
//+
Line(1) = {2, 6};
//+
Line(2) = {1, 5};
//+
Line(3) = {4, 8};
//+
Line(4) = {3, 7};
//+
Line(5) = {6, 8};
//+
Line(6) = {5, 7};
//+
Line(7) = {1, 3};
//+
Line(8) = {2, 4};
//+
Line(9) = {1, 2};
//+
Line(10) = {5, 6};
//+
Line(11) = {7, 8};
//+
Line(12) = {3, 4};
//+
Curve Loop(1) = {1, 5, -3, -8};
//+
Plane Surface(1) = {1};
//+
Curve Loop(2) = {10, 5, -11, -6};
//+
Plane Surface(2) = {2};
//+
Curve Loop(3) = {1, -10, -2, 9};
//+
Plane Surface(3) = {3};
//+
Curve Loop(4) = {2, 6, -4, -7};
//+
Plane Surface(4) = {4};
//+
Curve Loop(5) = {9, 8, -12, -7};
//+
Plane Surface(5) = {5};
//+
Curve Loop(6) = {3, -11, -4, 12};
//+
Plane Surface(6) = {6};
//+
Transfinite Curve {8, 5, 6, 7, 1, 2, 10, 9, 12, 11, 3, 4} = 3 Using Progression 1;
//+
Transfinite Surface {1};
//+
Transfinite Surface {2};
//+
Transfinite Surface {4};
//+
Transfinite Surface {5};
//+
Transfinite Surface {3};
//+
Transfinite Surface {6};
//+
Surface Loop(1) = {4, 3, 1, 2, 6, 5};
//+
Volume(1) = {1};
//+
Transfinite Volume{1};
//+
Recombine Surface {1, 2, 4, 5, 6, 3};
