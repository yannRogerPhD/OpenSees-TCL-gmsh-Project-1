"""
// Supports MANY main volumes.

// (1) identify the total soil height (z total value of the soil: hTotal)
hTotal = 8;
// !!! note that we always consider ground level to be at z = 0 --> soil at z < 0

// (2) define xTOT and yTOT that do not normally change for the whole soil profile
xTOT = 16.0; yTOT = 8.0;

// We define our main geometry; however, we want (one box, stacked soil boxes, CAD import, etc.).
// We MUST define the bounding box of the "main domain union" via parameters:

// Global bounding box of *all* main regions (union)
// xMinMain = DefineNumber[ 0.0, Name "Parameters/xMinMain" ];
// xMaxMain = DefineNumber[ xTOT, Name "Parameters/xMaxMain" ];
// yMinMain = DefineNumber[ 0.0, Name "Parameters/yMinMain" ];
// yMaxMain = DefineNumber[ yTOT, Name "Parameters/yMaxMain" ];
// zMinMain = DefineNumber[ - hTotal, Name "Parameters/zMinMain" ];
// zMaxMain = DefineNumber[ 0.0, Name "Parameters/zMaxMain" ];
xMinMain = 0.0; yMinMain = 0.0; zMaxMain = 0.0;
xMaxMain = xTOT; yMaxMain = yTOT;
zMinMain = - hTotal;

// Thicknesses
thickASD = DefineNumber[ 0.2, Name "Parameters/thickASD" ];
thickDRM = DefineNumber[ 0.0, Name "Parameters/thickDRM" ]; // 0 disables DRM

SetFactory("OpenCASCADE");

// Then you create your main volumes (examples):
dxMain = xMaxMain - xMinMain;
dyMain = yMaxMain - yMinMain;

// (3) define dz0i for each layer (make sure that the sum of dz0i = hTotal)
z01 = zMinMain; dz01 = 3;
z02 = z01 + dz01; dz02 = 5;

// (4) define Boxes for all soil layers
Box(1) = {xMinMain, yMinMain, z01, dxMain, dyMain, dz01};
Box(2) = {xMinMain, yMinMain, z02, dxMain, dyMain, dz02};
// etc...

// (5) when call the function (bottom code), mention the number of boxes/volumes defined (mainVolIDs = [1, 2, ...])

// Finally, the generated layer boxes are appended and BooleanFragments are called
// on: Volume{mainVols[]} + Volume{layerVols[]}.

// we must also provide a list of main volume ids (mainVolIDs) when calling the Python generator.
"""


def layer_boxes_lateral_bottom_from_bounds(xMin, xMax, yMin, yMax, zMin, zMax, tVar, prefix):
    """
    Build the lateral+bottom layer around a bounding box given as min/max coords.
    No top layer.

    All inputs are strings (Gmsh symbols/expressions).
    """
    t = tVar
    lx = f"({xMax} - {xMin})"
    ly = f"({yMax} - {yMin})"
    lz = f"({zMax} - {zMin})"

    # Use x0 = xMin, y0 = yMin, z0 = zMin, and lengths lx,ly,lz
    x0, y0, z0 = xMin, yMin, zMin

    return [
        # faces
        (f"{prefix}_zMIN", f"{{{x0}, {y0}, ({z0}-{t}), {lx}, {ly}, {t}}}"),
        (f"{prefix}_xMIN", f"{{({x0}-{t}), {y0}, {z0}, {t}, {ly}, {lz}}}"),
        (f"{prefix}_xMAX", f"{{({x0}+{lx}), {y0}, {z0}, {t}, {ly}, {lz}}}"),
        (f"{prefix}_yMIN", f"{{{x0}, ({y0}-{t}), {z0}, {lx}, {t}, {lz}}}"),
        (f"{prefix}_yMAX", f"{{{x0}, ({y0}+{ly}), {z0}, {lx}, {t}, {lz}}}"),

        # bottom edges (with zMIN)
        (f"{prefix}_xMINzMIN", f"{{({x0}-{t}), {y0}, ({z0}-{t}), {t}, {ly}, {t}}}"),
        (f"{prefix}_xMAXzMIN", f"{{({x0}+{lx}), {y0}, ({z0}-{t}), {t}, {ly}, {t}}}"),
        (f"{prefix}_yMINzMIN", f"{{{x0}, ({y0}-{t}), ({z0}-{t}), {lx}, {t}, {t}}}"),
        (f"{prefix}_yMAXzMIN", f"{{{x0}, ({y0}+{ly}), ({z0}-{t}), {lx}, {t}, {t}}}"),

        # vertical edges (x± with y±), full height lz
        (f"{prefix}_xMINyMIN", f"{{({x0}-{t}), ({y0}-{t}), {z0}, {t}, {t}, {lz}}}"),
        (f"{prefix}_xMINyMAX", f"{{({x0}-{t}), ({y0}+{ly}), {z0}, {t}, {t}, {lz}}}"),
        (f"{prefix}_xMAXyMIN", f"{{({x0}+{lx}), ({y0}-{t}), {z0}, {t}, {t}, {lz}}}"),
        (f"{prefix}_xMAXyMAX", f"{{({x0}+{lx}), ({y0}+{ly}), {z0}, {t}, {t}, {lz}}}"),

        # bottom corners
        (f"{prefix}_xMINyMINzMIN", f"{{({x0}-{t}), ({y0}-{t}), ({z0}-{t}), {t}, {t}, {t}}}"),
        (f"{prefix}_xMINyMAXzMIN", f"{{({x0}-{t}), ({y0}+{ly}), ({z0}-{t}), {t}, {t}, {t}}}"),
        (f"{prefix}_xMAXyMINzMIN", f"{{({x0}+{lx}), ({y0}-{t}), ({z0}-{t}), {t}, {t}, {t}}}"),
        (f"{prefix}_xMAXyMAXzMIN", f"{{({x0}+{lx}), ({y0}+{ly}), ({z0}-{t}), {t}, {t}, {t}}}"),
    ]


def generate_DRM_ASD_geo_many_main(
    main_VolIDs,
    lastVolumeID,
    drm_var="thickDRM",
    asd_var="thickASD",
    bounds_vars=("xMinMain", "xMaxMain", "yMinMain", "yMaxMain", "zMinMain", "zMaxMain"),
):
    """
    mainVolIDs: list[int] of ALL main volumes (your stacked soil volumes, etc.)
    lastVolumeID: max existing volume id before adding layer boxes
    bounds_vars: names of .geo vars giving union bounding box of all main volumes

    Produces:
      - DRM boxes only if thickDRM>0
      - ASD boxes always, wrapping DRM-expanded bounds (symbolic)
      - BooleanFragments on Volume{mainVols[]} + Volume{layerVols[]}
    """
    if not main_VolIDs:
        raise ValueError("mainVolIDs must be a non-empty list of main volume IDs.")

    xMin, xMax, yMin, yMax, zMin, zMax = bounds_vars

    start = lastVolumeID + 1
    lines = [
        "// Automatically generated 3D DRM + ASD boundary boxes (multi-main-volume)\n",
        f"// Main volumes: {main_VolIDs}\n",
        f"// Starting new volume ID: {start}\n\n",
    ]

    next_id = start
    created_ids = []

    # DRM bounds = main bounds expanded by thickDRM laterally + bottom
    # (top is unchanged)
    xMin_drm = f"({xMin} - {drm_var})"
    xMax_drm = f"({xMax} + {drm_var})"
    yMin_drm = f"({yMin} - {drm_var})"
    yMax_drm = f"({yMax} + {drm_var})"
    zMin_drm = f"({zMin} - {drm_var})"
    zMax_drm = f"{zMax}"  # no top expansion

    # DRM boxes only if thickDRM > 0
    lines.append(f"If ({drm_var} > 0)\n")
    drm_boxes = layer_boxes_lateral_bottom_from_bounds(xMin, xMax, yMin, yMax, zMin, zMax, drm_var, "DRM")
    for label, coords in drm_boxes:
        lines.append(f"  Box({next_id}) = {coords}; // {label}\n")
        created_ids.append(next_id)
        next_id += 1
    lines.append("EndIf\n\n")

    # ASD always wraps DRM-expanded bounds (and collapses when thickDRM=0)
    asd_boxes = layer_boxes_lateral_bottom_from_bounds(
        xMin_drm, xMax_drm, yMin_drm, yMax_drm, zMin_drm, zMax_drm, asd_var, "ASD"
    )
    for label, coords in asd_boxes:
        lines.append(f"Box({next_id}) = {coords}; // {label}\n")
        created_ids.append(next_id)
        next_id += 1

    # BooleanFragments using explicit lists
    lines.append("\n// Coherence OR Fragment main + layer volumes\n")
    # lines.append("mainVols[] = {")
    # lines.append(",".join(str(v) for v in main_VolIDs))
    # lines.append("};\n")
    #
    # lines.append("layerVols[] = {")
    # lines.append(",".join(str(v) for v in created_ids))
    # lines.append("};\n")

    # lines.append("BooleanFragments{ Volume{mainVols[]}; Volume{layerVols[]}; Delete; }{};\n")
    lines.append("Coherence;\n")

    return "".join(lines)


# Example usage:
if __name__ == "__main__":
    # Suppose you have 3 stacked soil volumes already defined as Volume(1), Volume(2), Volume(3)
    # mainVolIDs = [1, 2, 3]
    mainVolIDs = [1]
    lastVolID = max(mainVolIDs)  # or whatever your geometry used last
    geoText = generate_DRM_ASD_geo_many_main(main_VolIDs=mainVolIDs, lastVolumeID=lastVolID)
    print(geoText)
