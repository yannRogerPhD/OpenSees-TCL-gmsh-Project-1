//
//+
lc = DefineNumber[ 1.0, Name "Parameters/lc" ];
//+
hL = DefineNumber[ 1.0, Name "Parameters/hL" ];
//+
tL = DefineNumber[ 2.0, Name "Parameters/tL" ];

Point(1) = {0.0, 0.0, 0.0, lc};
//+
Point(2) = {tL, 0.0, 0.0, lc};
//+
Point(3) = {tL, hL, 0.0, lc};
//+
Point(4) = {0.0, hL, 0.0, lc};
//+
Point(5) = {0.0, 2.0*hL, 0.0, 1.0};
//+
Point(6) = {tL, 2.0*hL, 0.0, 1.0};
//+
Point(7) = {tL, 3.0*hL, 0.0, 1.0};
//+
Point(8) = {0.0, 3.0*hL, 0.0, 1.0};
//+
Point(9) = {0.0, 4.0*hL, 0.0, 1.0};
//+
Point(10) = {tL, 4.0*hL, 0.0, 1.0};
//+
Point(11) = {tL, 5.0*hL, 0.0, 1.0};
//+
Point(12) = {0.0, 5.0*hL, 0.0, 1.0};
//+
Point(13) = {0.0, 6.0*hL, 0.0, 1.0};
//+
Point(14) = {tL, 6.0*hL, 0.0, 1.0};
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
Line(6) = {12, 11};
//+
Line(7) = {13, 14};
//+
Line(8) = {1, 4};
//+
Line(9) = {4, 5};
//+
Line(10) = {5, 8};
//+
Line(11) = {8, 9};
//+
Line(12) = {9, 12};
//+
Line(13) = {12, 13};
//+
Line(14) = {2, 3};
//+
Line(15) = {3, 6};
//+
Line(16) = {6, 7};
//+
Line(17) = {7, 10};
//+
Line(18) = {10, 11};
//+
Line(19) = {11, 14};
//+
Curve Loop(1) = {1, 14, -2, -8};
//+
Plane Surface(1) = {1};
//+
Curve Loop(2) = {2, 15, -3, -9};
//+
Plane Surface(2) = {2};
//+
Curve Loop(3) = {3, 16, -4, -10};
//+
Plane Surface(3) = {3};
//+
Curve Loop(4) = {4, 17, -5, -11};
//+
Plane Surface(4) = {4};
//+
Curve Loop(5) = {5, 18, -6, -12};
//+
Plane Surface(5) = {5};
//+
Curve Loop(6) = {6, 19, -7, -13};
//+
Plane Surface(6) = {6};
//+
Transfinite Curve {1, 2, 3, 4, 5, 6, 7} = 2 Using Progression 1;
//+
Transfinite Curve {8, 14} = 7 Using Progression 1;
//+
Transfinite Curve {9, 15} = 6 Using Progression 1;
//+
Transfinite Curve {10, 16} = 5 Using Progression 1;
//+
Transfinite Curve {11, 17} = 4 Using Progression 1;
//+
Transfinite Curve {12, 18} = 4 Using Progression 1;
//+
Transfinite Curve {13, 19} = 3 Using Progression 1;
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
Recombine Surface {1, 2, 3, 4, 5, 6};
