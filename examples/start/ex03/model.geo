//
//+
trans1 = DefineNumber[ 141, Name "Parameters/trans1" ];
//+
trans2 = DefineNumber[ 27, Name "Parameters/trans2" ];
//+
Point(1) = {-130, 0, 0, 1.0};
//+
Point(2) = {130, 0, 0, 1.0};
//+
Point(3) = {130, 140, 0, 1.0};

//+
Point(4) = {-130, 140, 0, 1.0};
//+
Point(5) = {-150, 140, 0, 1.0};
//+
Point(6) = {150, 140, 0, 1.0};
//+
Point(7) = {150, 0, 0, 1.0};
//+
Point(8) = {-150, 0, 0, 1.0};
//+
Point(9) = {-150, -20, 0, 1.0};
//+
Point(10) = {-130, -20, 0, 1.0};
//+
Point(11) = {130, -20, 0, 1.0};
//+
Point(12) = {150, -20, 0, 1.0};
//+
Line(1) = {1, 2};
//+
Line(2) = {2, 3};
//+
Line(3) = {4, 3};
//+
Line(4) = {1, 4};
//+
Line(5) = {8, 1};
//+
Line(6) = {8, 5};
//+
Line(7) = {5, 4};
//+
Line(8) = {9, 10};
//+
Line(9) = {10, 1};
//+
Line(10) = {9, 8};
//+
Line(11) = {10, 11};
//+
Line(12) = {11, 2};
//+
Line(13) = {2, 7};
//+
Line(14) = {11, 12};
//+
Line(15) = {12, 7};
//+
Line(16) = {7, 6};
//+
Line(17) = {3, 6};
//+
Curve Loop(1) = {11, 12, -1, -9};
//+
Plane Surface(1) = {1};
//+
Curve Loop(2) = {14, 15, -13, -12};
//+
Plane Surface(2) = {2};
//+
Curve Loop(3) = {13, 16, -17, -2};
//+
Plane Surface(3) = {3};
//+
Curve Loop(4) = {8, 9, -5, -10};
//+
Plane Surface(4) = {4};
//+
Curve Loop(5) = {5, 4, -7, -6};
//+
Plane Surface(5) = {5};
//+
Curve Loop(6) = {1, 2, -3, -4};
//+
Plane Surface(6) = {6};
//+
Physical Surface("L", 18) = {5};
//+
Physical Surface("R", 19) = {3};
//+
Physical Surface("B", 20) = {1};
//+
Physical Surface("LB", 21) = {4};
//+
Physical Surface("RB", 22) = {2};
//+
Physical Surface("mainS", 23) = {6};
//+
Transfinite Curve {6, 4, 2, 16} = trans1 Using Progression 1;
//+
Transfinite Curve {3, 1, 11} = trans2 Using Progression 1;
//+
Transfinite Curve {7, 5, 8, 10, 9, 12, 15, 14, 13, 17} = 2 Using Progression 1;
//+
Transfinite Surface {4};
//+
Transfinite Surface {1};
//+
Transfinite Surface {2};
//+
Transfinite Surface {3};
//+
Transfinite Surface {6};
//+
Transfinite Surface {5};
//+
Recombine Surface {4, 1, 2, 3, 6, 5};

