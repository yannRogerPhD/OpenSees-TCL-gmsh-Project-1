//
//+
transX = DefineNumber[ 5, Name "Parameters/transX" ];
//+
transY = DefineNumber[ 4, Name "Parameters/transY" ];
//+
transZ = DefineNumber[ 3, Name "Parameters/transZ" ];
//+
SetFactory("OpenCASCADE");
Box(1) = {0, 0, 0, 1, 1, 1};
//+
//+
Box(2) = {1, 0, 0, 0.2, 1, 1};
//+
Box(3) = {0, 0, 0, -0.2, 1, 1};
Coherence;
//+
Transfinite Curve {2, 4, 24, 22, 6, 8, 14, 16} = transY Using Progression 1;
//+
Transfinite Curve {10, 9, 12, 11} = transX Using Progression 1;
//+
Transfinite Curve {1, 21, 3, 23, 7, 15, 13, 5} = transX Using Progression 1;
//+
Transfinite Curve {28, 27, 25, 26, 18, 17, 20, 19} = 2 Using Progression 1;
//+
Transfinite Surface {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16};
//+
Recombine Surface {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16};
//+
Transfinite Volume{1, 2, 3};
//+
Point(17) = {0.5, 0, 1, 1.0};
//+
Point(18) = {0.5, 1, 1, 1.0};
//+
Line(29) = {17, 18};
//+
Transfinite Curve {29} = 4 Using Progression 1;
//+
//+
Point(19) = {0.75, 1.25, 0.25, 1.0};
//+
Point(20) = {0.75, 1.25, 0.75, 1.0};
//+
Point(21) = {0.75, 1.45, 0.75, 1.0};
//+
Point(22) = {0.75, 1.45, 0.25, 1.0};
//+
Point(23) = {0.25, 1.45, 0.25, 1.0};
//+
Point(24) = {0.25, 1.25, 0.25, 1.0};
//+
Point(25) = {0.25, 1.25, 0.75, 1.0};
//+
Point(26) = {0.25, 1.45, 0.75, 1.0};
//+
Point(27) = {0.25, 1.0, 0.75, 1.0};
//+
Point(28) = {0.25, 1.0, 0.25, 1.0};
//+
Point(29) = {0.75, 1.0, 0.25, 1.0};
//+
Point(30) = {0.75, 1.0, 0.75, 1.0};
//+
Line(30) = {27, 25};
//+
Line(31) = {25, 26};
//+
Line(32) = {26, 23};
//+
Line(33) = {28, 24};
//+
Line(34) = {24, 23};
//+
Line(35) = {26, 21};
//+
Line(36) = {23, 22};
//+
Line(37) = {22, 21};
//+
Line(38) = {30, 20};
//+
Line(39) = {20, 21};
//+
Line(40) = {29, 19};
//+
Line(41) = {19, 22};
//+
Line(42) = {24, 25};
//+
Line(43) = {19, 20};
//+
Line(44) = {24, 19};
//+
Line(45) = {25, 20};
//+
Transfinite Curve {30, 38, 40, 33, 39, 41, 31, 34} = 4 Using Progression 1;
//+
Transfinite Curve {37, 32, 42, 43} = 2 Using Progression 1;
//+
Transfinite Curve {45, 44, 35, 36} = 5 Using Progression 1;
