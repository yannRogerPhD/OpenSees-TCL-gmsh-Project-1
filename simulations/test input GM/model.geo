//
//+
SetFactory("OpenCASCADE");
Box(1) = {-1, -1, -30, 2, 2, 20};
//+
Box(2) = {-1, -1, -10, 2, 2, 8};
//+
Box(3) = {-1, -1, -2, 2, 2, 2};
//+
Coherence;
//+
Transfinite Curve {5, 7, 1, 3} = 41 Using Progression 1;
//+
Transfinite Curve {16, 18, 13, 15} = 17 Using Progression 1;
//+
Transfinite Curve {24, 26, 21, 23} = 5 Using Progression 1;
//+
Transfinite Curve {25, 28, 22, 27, 17, 20, 14, 19, 6, 12, 2, 10, 8, 11, 4, 9} = 2 Using Progression 1;
//+
Transfinite Surface {:};
//+
Recombine Surface {:};
//+
Transfinite Volume {:};

