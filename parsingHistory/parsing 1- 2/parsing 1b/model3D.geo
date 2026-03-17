//+
transX = DefineNumber[ 8, Name "Parameters/transX" ];
//+
transY = DefineNumber[ 11, Name "Parameters/transY" ];
//+
transZ = DefineNumber[ 5, Name "Parameters/transZ" ];
//+
SetFactory("OpenCASCADE");
Box(1) = {0, 0, 0, 1, 1, 1};
//+
Transfinite Curve {2, 4, 8, 6} = transY Using Progression 1;
//+
Transfinite Curve {10, 9, 12, 11} = transZ Using Progression 1;
//+
Transfinite Curve {5, 7, 3, 1} = transX Using Progression 1;
//+
Transfinite Surface {1:6};
//+
Transfinite Volume {1};
//+
Recombine Surface {1:6};
//+
Point(9) = {0.375, 0, 0.375, 1.0};
//+
Point(10) = {0.375, 1.0, 0.375, 1.0};
//+
Line(13) = {9, 10};
//+
Point(11) = {0.375, 1.25, 0.375, 1.0};
//+
Line(14) = {10, 11};
//+
Transfinite Curve {13} = transY Using Progression 1;
//+
Transfinite Curve {14} = 4 Using Progression 1;
