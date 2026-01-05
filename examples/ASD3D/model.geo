//
// Start: 07h40
//+
lTx = DefineNumber[ 160, Name "Parameters/lTx" ];
//+
lTy = DefineNumber[ 160, Name "Parameters/lTy" ];
//+
lTz = DefineNumber[ 80, Name "Parameters/lTz" ];
//+
XmeshSize = DefineNumber[ 10, Name "Parameters/XmeshSize" ];
//+
YmeshSize = DefineNumber[ 10, Name "Parameters/YmeshSize" ];
//+
ZmeshSize = DefineNumber[ 5.0, Name "Parameters/ZmeshSize" ];
//+
thickASD = DefineNumber[ 20.0, Name "Parameters/thickASD" ];
//+
x0 = 0; y0 = 0; z0 = 0;
// XmeshSize = 10; YmeshSize = 10; ZmeshSize = 5.0;
//+
transX = Ceil(lTx/XmeshSize) + 1;
transY = Ceil(lTy/YmeshSize) + 1;
transZ = Ceil(lTz/ZmeshSize) + 1;
//+
SetFactory("OpenCASCADE");
Box(1) = {x0 - lTx/2, y0 - lTy/2, z0 - lTz, lTx, lTy, lTz};
//+
Transfinite Curve {9, 11, 10, 12} = transX Using Progression 1;
//+
Transfinite Curve {4, 8, 2, 6} = transY Using Progression 1;
//+
Transfinite Curve {1, 5, 7, 3} = transZ Using Progression 1;
//+
Transfinite Surface {1:6};
//+
Recombine Surface {1:6};
//+
Transfinite Volume {1};
//+
Extrude {0, 0, - thickASD} {
  Surface{5}; Layers {1}; Recombine;
}
//+
Extrude {- thickASD, 0, 0} {
  Surface{1}; Layers {1}; Recombine;
}
//+
Extrude {thickASD, 0, 0} {
  Surface{2}; Layers {1}; Recombine;
}
//+
Extrude {0, - thickASD, 0} {
  Surface{3}; Layers {1}; Recombine;
}
//+
Extrude {0, thickASD, 0} {
  Surface{4}; Layers {1}; Recombine;
}
//+
Extrude {- thickASD, 0, 0} {
  Surface{7}; Layers {1}; Recombine;
}
//+
Extrude {thickASD, 0, 0} {
  Surface{9}; Layers {1}; Recombine;
}
//+
Extrude {0, - thickASD, 0} {
  Surface{10}; Layers {1}; Recombine;
}
//+
Extrude {0, thickASD, 0} {
  Surface{8}; Layers {1}; Recombine;
}
//+
Extrude {0, - thickASD, 0} {
  Surface{12}; Layers {1}; Recombine;
}
//+
Extrude {- thickASD, 0, 0} {
  Surface{30}; Layers {1}; Recombine;
}
//+
Extrude {0, - thickASD, 0} {
  Surface{17}; Layers {1}; Recombine;
}
//+
Extrude {0, thickASD, 0} {
  Surface{19}; Layers {1}; Recombine;
}
//+
Extrude {0, - thickASD, 0} {
  Surface{33}; Layers {1}; Recombine;
}
//+
Extrude {0, thickASD, 0} {
  Surface{32}; Layers {1}; Recombine;
}
//+
Extrude {thickASD, 0, 0} {
  Surface{42}; Layers {1}; Recombine;
}
//+
Extrude {0, thickASD, 0} {
  Surface{37}; Layers {1}; Recombine;
}
Coherence;
