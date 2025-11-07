"""
//+
lTx = DefineNumber[ 1.0, Name "Parameters/lx" ];
//+
lTy = DefineNumber[ 1.0, Name "Parameters/ly" ];
//+
lTz = DefineNumber[ 1.0, Name "Parameters/lz" ];
//+
thickASD = DefineNumber[ 0.2, Name "Parameters/thickASD" ];
//+
x0 = 0; y0 = 0; z0 = 0;
//+
"""


def generateASDGeo(lastVolumeID=1):
    start = lastVolumeID + 1  # first absorbing volume
    lines = [
        '// Automatically generated 3D absorbing boundary boxes\n',
        f'// Starting volume ID: {start}\n',
        '// SetFactory("OpenCASCADE");\n'
    ]

    # Define all boxes relative to the main domain
    boxes = [
        ("B",  "{x0, y0 - thickASD, z0, lTx, thickASD, lTz}"),
        ("L",  "{x0 - thickASD, y0, z0, thickASD, lTy, lTz}"),
        ("R",  "{x0 + lTx, y0, z0, thickASD, lTy, lTz}"),
        ("F",  "{x0, y0, z0 + lTz, lTx, lTy, thickASD}"),
        ("K",  "{x0, y0, z0 - thickASD, lTx, lTy, thickASD}"),
        ("BL", "{x0 - thickASD, y0 - thickASD, z0, thickASD, thickASD, lTz}"),
        ("BR", "{x0 + lTx, y0 - thickASD, z0, thickASD, thickASD, lTz}"),
        ("BF", "{x0, y0 - thickASD, z0 + lTz, lTx, thickASD, thickASD}"),
        ("BK", "{x0, y0 - thickASD, z0 - thickASD, lTx, thickASD, thickASD}"),
        ("LF", "{x0 - thickASD, y0, z0 + lTz, thickASD, lTy, thickASD}"),
        ("LK", "{x0 - thickASD, y0, z0 - thickASD, thickASD, lTy, thickASD}"),
        ("RF", "{x0 + lTx, y0, z0 + lTz, thickASD, lTy, thickASD}"),
        ("RK", "{x0 + lTx, y0, z0 - thickASD, thickASD, lTy, thickASD}"),
        ("BLF", "{x0 - thickASD, y0 - thickASD, z0 + lTz, thickASD, thickASD, thickASD}"),
        ("BLK", "{x0 - thickASD, y0 - thickASD, z0 - thickASD, thickASD, thickASD, thickASD}"),
        ("BRF", "{x0 + lTx, y0 - thickASD, z0 + lTz, thickASD, thickASD, thickASD}"),
        ("BRK", "{x0 + lTx, y0 - thickASD, z0 - thickASD, thickASD, thickASD, thickASD}")
    ]

    # Generate boxes
    for i, (label, coords) in enumerate(boxes, start=start):
        lines.append(f'Box({i}) = {coords}; // {label}\n')

    # Boolean merge step
    end = start + len(boxes) - 1
    lines.append(f'BooleanFragments{{ Volume{{1:{end}}}; Delete; }}{{}}\n')
    lines.append(f'Coherence;\n')

    return ''.join(lines)


# usage:
lastVolID = 3
geoText = generateASDGeo(lastVolumeID=lastVolID)
print(geoText)
