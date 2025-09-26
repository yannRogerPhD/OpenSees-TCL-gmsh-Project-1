//
thickness = DefineNumber[ 0.2, Name "Parameters/thickness" ];
//+
Point(1) = {0, 0, 0, 1.0};
//+
Point(2) = {thickness, 0, 0, 1.0};
//+
Point(3) = {thickness, 30, 0, 1.0};
//+
Point(4) = {0, 30, 0, 1.0};

//+
Line(1) = {1, 2};
//+
Line(2) = {2, 3};
//+
Line(3) = {3, 4};
//+
Line(4) = {4, 1};
//+
Curve Loop(1) = {1, 2, 3, 4};
//+
Plane Surface(1) = {1};
//+
Transfinite Curve {4, 2} = 25 Using Progression 1;
//+
Transfinite Curve {1, 3} = 2 Using Progression 1;
//+
Transfinite Surface {1};
//+
Recombine Surface {1};
