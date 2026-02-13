//
//+
SetFactory("OpenCASCADE");
Box(1) = {0, 0, 0, 1, 1, 1};
//+
Transfinite Curve {8, 4, 6, 2} = 5 Using Progression 1;
//+
Transfinite Curve {1, 5, 3, 7} = 4 Using Progression 1;
//+
Transfinite Curve {9, 10, 11, 12} = 3 Using Progression 1;
//+
Transfinite Surface{:};
//+
Recombine Surface{:};
//+
Transfinite Volume{:};
//+
Point(9) = {0.25, 0.75, 0.75, 1.0};
//+
Point(10) = {0.25, 0.75, 0.25, 1.0};
//+
Point(11) = {0.75, 0.75, 0.25, 1.0};
//+
Point(12) = {0.75, 0.75, 0.75, 1.0};
//+
Point(13) = {0.75, 1.25, 0.75, 1.0};
//+
Point(14) = {0.25, 1.25, 0.75, 1.0};
//+
Point(15) = {0.25, 1.25, 0.25, 1.0};
//+
Point(16) = {0.75, 1.25, 0.25, 1.0};
//+
Line(13) = {9, 14};
//+
Line(14) = {10, 15};
//+
Line(15) = {11, 16};
//+
Line(16) = {12, 13};
//+
Line(17) = {15, 14};
//+
Line(18) = {16, 13};
//+
Line(19) = {14, 13};
//+
Line(20) = {15, 16};
//+
Transfinite Curve {13, 14, 15, 16} = 5 Using Progression 1;
//+
Transfinite Curve {19, 18, 20, 17} = 3 Using Progression 1;
