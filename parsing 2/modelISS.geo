//
transZ = DefineNumber[ 5, Name "Parameters/transZ" ];
//+
transX = DefineNumber[ 4, Name "Parameters/transX" ];
//+
transY = DefineNumber[ 4, Name "Parameters/transY" ];
//+
SetFactory("OpenCASCADE");
Box(1) = {0, 0, 0, 1, 1, 1};
//+
Transfinite Curve {3, 7, 5, 1} = transZ Using Progression 1;  // transZ
//+
Transfinite Curve {9, 11, 10, 12} = transX Using Progression 1; // transX
//+
Transfinite Curve {4, 8, 2, 6} = transY Using Progression 1; // transY
//+
Transfinite Surface {1:6};
//+
Transfinite Volume {1};
//+
Recombine Surface {1:6};
//+
Point(9) = {0.375, 0.275, 0, 1.0};
//+
Point(10) = {0.375, 0.275, 1, 1.0};
//+
Point(11) = {0.375, 0.275, 1.25, 1.0};
//+
Line(13) = {9, 10};
//+
Line(14) = {10, 11};
//+
Transfinite Curve {13} = transZ Using Progression 1;
//+
Transfinite Curve {14} = 4 Using Progression 1;
//+
Point(12) = {0.375, 0.775, 0, 1.0};
//+
Point(13) = {0.375, 0.775, 1, 1.0};
//+
Point(14) = {0.375, 0.775, 1.25, 1.0};
//+
Line(15) = {12, 13};
//+
Line(16) = {13, 14};
//+
Line(17) = {12, 9};
//+
Transfinite Curve {16, 16} = 4 Using Progression 1;
//+
Transfinite Curve {15} = transZ Using Progression 1;
//+
Transfinite Curve {17} = 3 Using Progression 1;
