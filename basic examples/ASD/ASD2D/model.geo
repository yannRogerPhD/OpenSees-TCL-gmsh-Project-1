//
//+
Point(1) = {0, 0, 0, 1.0};
//+
Point(2) = {260, 0, 0, 1.0};
//+
Point(3) = {260, 50, 0, 1.0};
//+
Point(4) = {0, 50, 0, 1.0};
//+
Point(5) = {0, 90, 0, 1.0};
//+
Point(6) = {260, 90, 0, 1.0};
//+
Point(7) = {260, 120, 0, 1.0};
//+
Point(8) = {0, 120, 0, 1.0};
//+
Point(9) = {0, 140, 0, 1.0};
//+
Point(10) = {260, 140, 0, 1.0};
//+
Point(11) = {280, 140, 0, 1.0};
//+
Point(12) = {280, 120, 0, 1.0};
//+
Point(13) = {280, 90, 0, 1.0};
//+
Point(14) = {280, 50, 0, 1.0};
//+
Point(15) = {280, 0, 0, 1.0};
//+
Point(16) = {-20, 140, 0, 1.0};
//+
Point(17) = {-20, 120, 0, 1.0};
//+
Point(18) = {-20, 90, 0, 1.0};
//+
Point(19) = {-20, 50, 0, 1.0};
//+
Point(20) = {-20, 0, 0, 1.0};
//+
Point(21) = {-20, -20, 0, 1.0};
//+
Point(22) = {0, -20, 0, 1.0};
//+
Point(23) = {260, -20, 0, 1.0};
//+
Point(24) = {280, -20, 0, 1.0};
//+
Line(1) = {1, 2};
//+
Line(2) = {4, 3};
//+
Line(3) = {5, 6};
//+
Line(4) = {8, 7};
//+
Line(5) = {9, 10};
//+
Line(6) = {22, 23};
//+
Line(7) = {2, 15};
//+
Line(8) = {3, 14};
//+
Line(9) = {6, 13};
//+
Line(10) = {7, 12};
//+
Line(11) = {10, 11};
//+
Line(12) = {23, 24};
//+
Line(13) = {21, 22};
//+
Line(14) = {20, 1};
//+
Line(15) = {19, 4};
//+
Line(16) = {18, 5};
//+
Line(17) = {17, 8};
//+
Line(18) = {16, 9};
//+
Line(19) = {21, 20};
//+
Line(20) = {20, 19};
//+
Line(21) = {19, 18};
//+
Line(22) = {18, 17};
//+
Line(23) = {17, 16};
//+
Line(24) = {22, 1};
//+
Line(25) = {1, 4};
//+
Line(26) = {4, 5};
//+
Line(27) = {5, 8};
//+
Line(28) = {8, 9};
//+
Line(29) = {23, 2};
//+
Line(30) = {2, 3};
//+
Line(31) = {3, 6};
//+
Line(32) = {6, 7};
//+
Line(33) = {7, 10};
//+
Line(34) = {24, 15};
//+
Line(35) = {15, 14};
//+
Line(36) = {14, 13};
//+
Line(37) = {13, 12};
//+
Line(38) = {12, 11};
//+
Curve Loop(1) = {1, 30, -2, -25};
//+
Plane Surface(1) = {1};
//+
Curve Loop(2) = {2, 31, -3, -26};
//+
Plane Surface(2) = {2};
//+
Curve Loop(3) = {3, 32, -4, -27};
//+
Plane Surface(3) = {3};
//+
Curve Loop(4) = {4, 33, -5, -28};
//+
Plane Surface(4) = {4};
//+
Curve Loop(5) = {6, 29, -1, -24};
//+
Plane Surface(5) = {5};
//+
Curve Loop(6) = {14, 25, -15, -20};
//+
Plane Surface(6) = {6};
//+
Curve Loop(7) = {15, 26, -16, -21};
//+
Plane Surface(7) = {7};
//+
Curve Loop(8) = {16, 27, -17, -22};
//+
Plane Surface(8) = {8};
//+
Curve Loop(9) = {17, 28, -18, -23};
//+
Plane Surface(9) = {9};
//+
Curve Loop(10) = {7, 35, -8, -30};
//+
Plane Surface(10) = {10};
//+
Curve Loop(11) = {8, 36, -9, -31};
//+
Plane Surface(11) = {11};
//+
Curve Loop(12) = {9, 37, -10, -32};
//+
Plane Surface(12) = {12};
//+
Curve Loop(13) = {10, 38, -11, -33};
//+
Plane Surface(13) = {13};
//+
Curve Loop(14) = {13, 24, -14, -19};
//+
Plane Surface(14) = {14};
//+
Curve Loop(15) = {12, 34, -7, -29};
//+
Plane Surface(15) = {15};
//+
Transfinite Curve {20, 25, 30, 35} = 39 Using Progression 1;  // 50 m --> 41
//+
Transfinite Curve {21, 26, 31, 36} = 31 Using Progression 1;  // 40 m --> 31
//+
Transfinite Curve {22, 27, 32, 37} = 21 Using Progression 1;  // 30 m --> 21
//+
Transfinite Curve {23, 28, 33, 38} = 17 Using Progression 1;  // 20 m --> 21
//+
Transfinite Curve {18, 17, 16, 15, 14, 13, 19, 24, 29, 34, 12, 7, 8, 9, 10, 11} = 2 Using Progression 1;
//+
Transfinite Curve {6, 1, 2, 3, 4, 5} = 6 Using Progression 1;  // 10
//+
Transfinite Surface {1:15};
//+
Recombine Surface {1:15};
