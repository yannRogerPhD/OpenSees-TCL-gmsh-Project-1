from __future__ import annotations
from typing import Any


def emit_define_number(var: str, value: float, gui_path: str) -> str:
    return f'{var} = DefineNumber[ {value}, Name "{gui_path}" ];'


def bbox_curve_queries_for_box(i: int, eps_name: str, transX: str, transY: str, transZ: str) -> str:
    """
    Build robust curve groups for a box using Curve In BoundingBox queries.

    For an axis-aligned box, edges split into:
      - 4 X-directed edges: (y=ymin/ymax) x (z=zmin/zmax)
      - 4 Y-directed edges: (x=xmin/xmax) x (z=zmin/zmax)
      - 4 Z-directed edges: (x=xmin/xmax) x (y=ymin/ymax)

    We compute xmin/xmax/ymin/ymax/zmin/zmax symbolically from parameters.
    """
    X0 = f"x0_{i}"
    Y0 = f"y0_{i}"
    Z0 = f"z0_{i}"
    Lx = f"lTx_{i}"
    Ly = f"lTy_{i}"
    Lz = f"lTz_{i}"

    xmin = f"({X0} - {Lx}/2)"
    xmax = f"({X0} + {Lx}/2)"
    ymin = f"({Y0} - {Ly}/2)"
    ymax = f"({Y0} + {Ly}/2)"
    zmax = f"({Z0})"
    zmin = f"({Z0} - {Lz})"

    # Lists of curves selected by small bounding boxes around each edge
    lines = []
    lines.append(f"// ---- Robust curve selection for Box({i}) using bounding boxes ----")
    lines.append(f"cX_{i}[] = {{}};")
    lines.append(f"cY_{i}[] = {{}};")
    lines.append(f"cZ_{i}[] = {{}};")

    # X edges: y fixed at ymin/ymax, z fixed at zmin/zmax, x spans [xmin,xmax]
    for yfix in (ymin, ymax):
        for zfix in (zmin, zmax):
            lines.append(
                f"cX_{i}[] += Curve In BoundingBox "
                f"{{{xmin}-{eps_name}, {yfix}-{eps_name}, {zfix}-{eps_name}, "
                f"{xmax}+{eps_name}, {yfix}+{eps_name}, {zfix}+{eps_name}}};"
            )

    # Y edges: x fixed at xmin/xmax, z fixed at zmin/zmax, y spans [ymin,ymax]
    for xfix in (xmin, xmax):
        for zfix in (zmin, zmax):
            lines.append(
                f"cY_{i}[] += Curve In BoundingBox "
                f"{{{xfix}-{eps_name}, {ymin}-{eps_name}, {zfix}-{eps_name}, "
                f"{xfix}+{eps_name}, {ymax}+{eps_name}, {zfix}+{eps_name}}};"
            )

    # Z edges: x fixed at xmin/xmax, y fixed at ymin/ymax, z spans [zmin,zmax]
    for xfix in (xmin, xmax):
        for yfix in (ymin, ymax):
            lines.append(
                f"cZ_{i}[] += Curve In BoundingBox "
                f"{{{xfix}-{eps_name}, {yfix}-{eps_name}, {zmin}-{eps_name}, "
                f"{xfix}+{eps_name}, {yfix}+{eps_name}, {zmax}+{eps_name}}};"
            )

    # Apply transfinite constraints to the lists (robust: no explicit IDs)
    lines.append(f"Transfinite Curve {{cX_{i}[]}} = {transX} Using Progression 1;")
    lines.append(f"Transfinite Curve {{cY_{i}[]}} = {transY} Using Progression 1;")
    lines.append(f"Transfinite Curve {{cZ_{i}[]}} = {transZ} Using Progression 1;")

    return "\n".join(lines)


def multi_box_geo_robust(boxes: list[dict[str, Any]]) -> str:
    """
    Robust .geo generator:
      - Uses Curve In BoundingBox to find curves (no numbering assumptions)
      - Uses Boundary{ Volume{...}; } to get surfaces for Transfinite/Recombine
      - Inserts Coherence right before querying/applying constraints

    NOTE on your earlier preference:
      There is no true "after meshing" stage in a .geo script; the script executes
      before meshing. Putting Coherence at the physical end of the file is OK,
      but it must be executed before the queries/constraints if you want them to
      refer to merged entities.
    """
    lines: list[str] = []
    lines.append("//")
    lines.append('SetFactory("OpenCASCADE");')

    # tolerance used for bounding box selection of edges
    lines.append("//+")
    lines.append('eps = DefineNumber[ 1e-7, Name "Global/Selection/eps" ];')

    # PASS 1: define parameters + create all boxes + define trans counts
    for i, b in enumerate(boxes, start=1):
        XMeshSize = float(b.get("XMeshSize", 1.0))
        YMeshSize = float(b.get("YMeshSize", 1.0))
        ZMeshSize = float(b.get("ZMeshSize", 1.0))
        lTx = float(b.get("lTx", 20.0))
        lTy = float(b.get("lTy", 10.0))
        lTz = float(b.get("lTz", 10.0))
        x0 = float(b.get("x0", 0.0))
        y0 = float(b.get("y0", 0.0))
        z0 = float(b.get("z0", 0.0))

        # per-box variable names
        Xms = f"XMeshSize_{i}"
        Yms = f"YMeshSize_{i}"
        Zms = f"ZMeshSize_{i}"
        Lx = f"lTx_{i}"
        Ly = f"lTy_{i}"
        Lz = f"lTz_{i}"
        X0 = f"x0_{i}"
        Y0 = f"y0_{i}"
        Z0 = f"z0_{i}"

        tX = f"transX_{i}"
        tY = f"transY_{i}"
        tZ = f"transZ_{i}"

        lines.append("//+")
        lines.append(emit_define_number(Xms, XMeshSize, f"Box {i}/Mesh/XMeshSize"))
        lines.append("//+")
        lines.append(emit_define_number(Yms, YMeshSize, f"Box {i}/Mesh/YMeshSize"))
        lines.append("//+")
        lines.append(emit_define_number(Zms, ZMeshSize, f"Box {i}/Mesh/ZMeshSize"))

        lines.append("//+")
        lines.append(emit_define_number(Lx, lTx, f"Box {i}/Geometry/lTx"))
        lines.append("//+")
        lines.append(emit_define_number(Ly, lTy, f"Box {i}/Geometry/lTy"))
        lines.append("//+")
        lines.append(emit_define_number(Lz, lTz, f"Box {i}/Geometry/lTz"))

        lines.append("//+")
        lines.append(emit_define_number(X0, x0, f"Box {i}/Geometry/x0"))
        lines.append("//+")
        lines.append(emit_define_number(Y0, y0, f"Box {i}/Geometry/y0"))
        lines.append("//+")
        lines.append(emit_define_number(Z0, z0, f"Box {i}/Geometry/z0"))

        # Geometry: centered in x/y, anchored at top in z
        lines.append("//+")
        lines.append(
            f"Box({i}) = {{{X0} - {Lx}/2, {Y0} - {Ly}/2, {Z0} - {Lz}, {Lx}, {Ly}, {Lz}}};"
        )

        # transfinite counts (symbolic)
        lines.append("//+")
        lines.append(f"{tX} = Ceil({Lx}/{Xms}) + 1;")
        lines.append("//+")
        lines.append(f"{tY} = Ceil({Ly}/{Yms}) + 1;")
        lines.append("//+")
        lines.append(f"{tZ} = Ceil({Lz}/{Zms}) + 1;")

    # Merge coincident entities (do this before querying edges/surfaces)
    lines.append("//+")
    lines.append("Coherence;")

    # PASS 2: robust constraints using queries
    for i in range(1, len(boxes) + 1):
        tX = f"transX_{i}"
        tY = f"transY_{i}"
        tZ = f"transZ_{i}"

        # Curves by geometric selection (robust)
        lines.append("//+")
        lines.append(bbox_curve_queries_for_box(i, "eps", tX, tY, tZ))

        # Surfaces of this volume (robust) and apply transfinite + recombine
        # Boundary{ Volume{...}; } returns the bounding surfaces. :contentReference[oaicite:3]{index=3}
        lines.append("//+")
        lines.append(f"s_{i}[] = Boundary{{ Volume{{{i}}}; }};")
        lines.append("//+")
        lines.append(f"Transfinite Surface {{s_{i}[]}};")
        lines.append("//+")
        lines.append(f"Recombine Surface {{s_{i}[]}};")
        lines.append("//+")
        lines.append(f"Transfinite Volume {{{i}}};")

    return "\n".join(lines)


if __name__ == "__main__":
    geo = multi_box_geo_robust([
        dict(x0=0,  y0=0, z0=0,  lTx=20, lTy=10, lTz=10, XMeshSize=1,   YMeshSize=1,   ZMeshSize=1),
        dict(x0=10, y0=0, z0=0,  lTx=10, lTy=10, lTz=10, XMeshSize=0.5, YMeshSize=1.0, ZMeshSize=1.0),
    ])

    with open("model4.geo", "w") as f:
        f.write(geo)
