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

// -------------------------------
// Pile axis inside soil, but toe can be above soil bottom
// -------------------------------
xp = -20;
yp = -20;

// Choose pile head and toe elevations (must lie within soil for embedding)
zHead = z0;     // usually ground surface
zToe  = -55;    // example: toe is above bottom (soil bottom is z0 - lTz)

// Snap endpoints to soil layer planes
iHead = Round((z0 - zHead)/ZmeshSize);
iToe  = Round((z0 - zToe )/ZmeshSize);

// Clamp to soil layer index range [0, transZ-1]
If(iHead < 0) iHead = 0; EndIf
If(iHead > transZ-1) iHead = transZ-1; EndIf
If(iToe  < 0) iToe  = 0; EndIf
If(iToe  > transZ-1) iToe  = transZ-1; EndIf

// Ensure toe is deeper than head (iToe >= iHead)
If(iToe < iHead)
  tmp = iHead; iHead = iToe; iToe = tmp;
EndIf

// Create pile points only between head and toe indices
p0 = newp;
np = iToe - iHead + 1;

For j In {0:np-1}
  i = iHead + j;
  Point(p0 + j) = {xp, yp, z0 - i*ZmeshSize, ZmeshSize};
EndFor

// Create line segments along the pile
l0 = newl;
For j In {0:np-2}
  Line(l0 + j) = {p0 + j, p0 + j + 1};
EndFor

pileAxis[] = {l0 : l0 + np - 2};

// Embed only this in-soil portion
Curve{ pileAxis[] } In Volume{1};

// -------------------------------
// Above-ground extension (NOT embedded)
// -------------------------------
Hsup = 45;   // extension height above z0
nSup = 6;    // number of above-ground segments (choose what you want)
dSup = Hsup/nSup;

// Reuse pile head point (this is p0+0 from your in-soil loop)
pHead = p0;

// Create points above ground
pSup0 = newp;
For k In {1:nSup}
  Point(pSup0 + (k-1)) = {xp, yp, z0 + k*dSup, dSup};
EndFor

// Connect pile head to first above point, then chain up
lSup0 = newl;
Line(lSup0) = {pHead, pSup0};

For k In {0:nSup-2}
  Line(lSup0 + 1 + k) = {pSup0 + k, pSup0 + k + 1};
EndFor

superAxis[] = {lSup0 : lSup0 + nSup - 1};

//+
Translate {40, 0, 0} {
  Duplicata { Curve{111}; Curve{110}; Curve{109}; Curve{108}; Curve{107}; Curve{106}; Curve{105}; Curve{112}; Curve{113}; Curve{114}; Curve{115}; Curve{116}; Curve{117}; }
}
//+
Translate {0, 40, 0} {
  Duplicata { Curve{117}; Curve{116}; Curve{115}; Curve{114}; Curve{113}; Curve{112}; Curve{105}; Curve{106}; Curve{107}; Curve{108}; Curve{109}; Curve{110}; Curve{111}; Curve{118}; Curve{119}; Curve{120}; Curve{121}; Curve{122}; Curve{123}; Curve{124}; Curve{125}; Curve{126}; Curve{127}; Curve{128}; Curve{129}; Curve{130}; }
}
