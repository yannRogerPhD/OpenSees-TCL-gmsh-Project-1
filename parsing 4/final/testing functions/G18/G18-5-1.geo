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
