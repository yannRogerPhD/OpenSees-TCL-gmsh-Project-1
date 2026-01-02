//
transZ = DefineNumber[ 5, Name "Parameters/transZ" ];
//+
transX = DefineNumber[ 4, Name "Parameters/transX" ];
//+
transY = DefineNumber[ 4, Name "Parameters/transY" ];
//+
hSoil = 1.45; dZ = 0.35;
//+
lX = 4.0; lY = 4.0; lZ = hSoil;
//+
posXD = 0.85; posYD = 0.85;
//+
posX = (lX - posXD) / 2; posY = (lY - posYD) / 2; 
//+
SetFactory("OpenCASCADE");
Box(1) = {0, 0, -0.15, lX, lY, hSoil};
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
Point(9) = {posX, posY, 0, 1.0};
//+
Point(10) = {posX, posY, hSoil + dZ, 1.0};
//+
Point(11) = {posX, posY, hSoil + dZ/4, 1.0};
//+
Line(13) = {9, 10};
//+
Line(14) = {10, 11};
//+
Transfinite Curve {13} = transZ Using Progression 1;
//+
Transfinite Curve {14} = 4 Using Progression 1;
//+
Point(12) = {posX, posY + posYD, 0, 1.0};
//+
Point(13) = {posX, posY + posYD, hSoil + dZ/4, 1.0};
//+
Point(14) = {posX, posY + posYD, hSoil + dZ, 1.0};
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
//+
Line(18) = {10, 14};
//+
Point(15) = {posX, posY, hSoil + 2 * dZ, 1.0};
//+
Point(16) = {posX, posY + posYD, hSoil + 2 * dZ, 1.0};
//+
Point(17) = {posX + posXD, posY + posYD, hSoil + 2 * dZ, 1.0};
//+
Point(18) = {posX + posXD, posY, hSoil + 2 * dZ, 1.0};
//+
Point(19) = {posX + posXD, posY, hSoil + dZ, 1.0};
//+
Point(20) = {posX + posXD, posY, hSoil + dZ/4, 1.0};
//+
Point(21) = {posX + posXD, posY, 0, 1.0};
//+
Point(22) = {posX + posXD, posY + posYD, 0, 1.0};
//+
Point(23) = {posX + posXD, posY + posYD, hSoil + dZ/4, 1.0};
//+
Line(19) = {14, 16};
//+
Point(24) = {posX + posXD, posY + posYD, hSoil + dZ, 1.0};
//+
Line(20) = {15, 16};
//+
Line(21) = {11, 15};
//+
Line(22) = {20, 19};
//+
Line(23) = {19, 18};
//+
Line(24) = {18, 17};
//+
Line(25) = {23, 24};
//+
Line(26) = {24, 17};
//+
Line(27) = {10, 19};
//+
Line(28) = {14, 24};
//+
Line(29) = {15, 18};
//+
Line(30) = {16, 17};
//+
Line(31) = {19, 24};
//+
Line(32) = {21, 20};
//+
Line(33) = {22, 23};
//+
Line(34) = {21, 22};
//+
Line(35) = {9, 21};
//+
Line(36) = {12, 22};
//+
Line(37) = {13, 23};
//+
Line(38) = {11, 20};
//+
Line(39) = {20, 23};
//+
Line(40) = {11, 13};
