from __future__ import annotations

from typing import Any


def emit_define_number(var: str, value: float, gui_path: str) -> str:
    return f'{var} = DefineNumber[ {value}, Name "{gui_path}" ];'


def emit_bbox_transfinite_for_box(
    i: int,
    *,
    X0: str, Y0: str, Z0: str,
    Lx: str, Ly: str, Lz: str,
    epsSym: str,
    transX: str, transY: str, transZ: str,
    debug: bool = False,
) -> list[str]:
    """
    Robustly select the 12 edges of Box(i) using Curve In BoundingBox, then apply
    transfinite constraints. Boundary surfaces are obtained from Boundary{Volume{i};}
    so we DO NOT (and never) assume surface IDs.

    Intended to be emitted AFTER a global Coherence; (when touching boxes are merged).
    """
    # local bounds (purely symbolic)
    xMin = f"({X0} - {Lx}/2)"
    xMax = f"({X0} + {Lx}/2)"
    yMin = f"({Y0} - {Ly}/2)"
    yMax = f"({Y0} + {Ly}/2)"
    zMin = f"({Z0} - {Lz})"
    zMax = f"({Z0})"

    e = epsSym

    cX = f"cX_{i}"
    cY = f"cY_{i}"
    cZ = f"cZ_{i}"
    s = f"s_{i}"

    L_: list[str] = []
    L_.append(f"// !!!!===!!!! Robust selection + transfinite for Volume {i} !!!!===!!!!")
    L_.append(f"xMin_{i} = {xMin}; xMax_{i} = {xMax};")
    L_.append(f"yMin_{i} = {yMin}; yMax_{i} = {yMax};")
    L_.append(f"zMin_{i} = {zMin}; zMax_{i} = {zMax};")

    L_.append(f"{cX}[] = {{}}; {cY}[] = {{}}; {cZ}[] = {{}};")

    # X edges: y fixed at yMin/yMax, z fixed at zMin/zMax, x spans [xMin, xMax]
    L_.append(
        f"{cX}[] += Curve In BoundingBox {{ xMin_{i}-{e}, yMin_{i}-{e}, zMin_{i}-{e}, "
        f"xMax_{i}+{e}, yMin_{i}+{e}, zMin_{i}+{e} }};"
    )
    L_.append(
        f"{cX}[] += Curve In BoundingBox {{ xMin_{i}-{e}, yMin_{i}-{e}, zMax_{i}-{e}, "
        f"xMax_{i}+{e}, yMin_{i}+{e}, zMax_{i}+{e} }};"
    )
    L_.append(
        f"{cX}[] += Curve In BoundingBox {{ xMin_{i}-{e}, yMax_{i}-{e}, zMin_{i}-{e}, "
        f"xMax_{i}+{e}, yMax_{i}+{e}, zMin_{i}+{e} }};"
    )
    L_.append(
        f"{cX}[] += Curve In BoundingBox {{ xMin_{i}-{e}, yMax_{i}-{e}, zMax_{i}-{e}, "
        f"xMax_{i}+{e}, yMax_{i}+{e}, zMax_{i}+{e} }};"
    )

    # Y edges: x fixed at xMin/xMax, z fixed at zMin/zMax, y spans [yMin, yMax]
    L_.append(
        f"{cY}[] += Curve In BoundingBox {{ xMin_{i}-{e}, yMin_{i}-{e}, zMin_{i}-{e}, "
        f"xMin_{i}+{e}, yMax_{i}+{e}, zMin_{i}+{e} }};"
    )
    L_.append(
        f"{cY}[] += Curve In BoundingBox {{ xMin_{i}-{e}, yMin_{i}-{e}, zMax_{i}-{e}, "
        f"xMin_{i}+{e}, yMax_{i}+{e}, zMax_{i}+{e} }};"
    )
    L_.append(
        f"{cY}[] += Curve In BoundingBox {{ xMax_{i}-{e}, yMin_{i}-{e}, zMin_{i}-{e}, "
        f"xMax_{i}+{e}, yMax_{i}+{e}, zMin_{i}+{e} }};"
    )
    L_.append(
        f"{cY}[] += Curve In BoundingBox {{ xMax_{i}-{e}, yMin_{i}-{e}, zMax_{i}-{e}, "
        f"xMax_{i}+{e}, yMax_{i}+{e}, zMax_{i}+{e} }};"
    )

    # Z edges: x fixed at xMin/xMax, y fixed at yMin/yMax, z spans [zMin, zMax]
    L_.append(
        f"{cZ}[] += Curve In BoundingBox {{ xMin_{i}-{e}, yMin_{i}-{e}, zMin_{i}-{e}, "
        f"xMin_{i}+{e}, yMin_{i}+{e}, zMax_{i}+{e} }};"
    )
    L_.append(
        f"{cZ}[] += Curve In BoundingBox {{ xMin_{i}-{e}, yMax_{i}-{e}, zMin_{i}-{e}, "
        f"xMin_{i}+{e}, yMax_{i}+{e}, zMax_{i}+{e} }};"
    )
    L_.append(
        f"{cZ}[] += Curve In BoundingBox {{ xMax_{i}-{e}, yMin_{i}-{e}, zMin_{i}-{e}, "
        f"xMax_{i}+{e}, yMin_{i}+{e}, zMax_{i}+{e} }};"
    )
    L_.append(
        f"{cZ}[] += Curve In BoundingBox {{ xMax_{i}-{e}, yMax_{i}-{e}, zMin_{i}-{e}, "
        f"xMax_{i}+{e}, yMax_{i}+{e}, zMax_{i}+{e} }};"
    )

    # Post-process: Abs() to remove any orientation sign, Unique() to deduplicate.
    L_.append(f"{cX}[] = Abs({cX}[]); {cX}[] = Unique({cX}[]);")
    L_.append(f"{cY}[] = Abs({cY}[]); {cY}[] = Unique({cY}[]);")
    L_.append(f"{cZ}[] = Abs({cZ}[]); {cZ}[] = Unique({cZ}[]);")

    if debug:
        L_.append(f'Printf("Vol {i}: #cX=%g #cY=%g #cZ=%g", #{cX}[], #{cY}[], #{cZ}[]);')
        L_.append(f'For k In {{0:#{cX}[]-1}} Printf("  {cX}[%g]=%g", k, {cX}[k]); EndFor')
        L_.append(f'For k In {{0:#{cY}[]-1}} Printf("  {cY}[%g]=%g", k, {cY}[k]); EndFor')
        L_.append(f'For k In {{0:#{cZ}[]-1}} Printf("  {cZ}[%g]=%g", k, {cZ}[k]); EndFor')

    # Apply curve constraints
    L_.append(f"Transfinite Curve {{{cX}[]}} = {transX} Using Progression 1;")
    L_.append(f"Transfinite Curve {{{cY}[]}} = {transY} Using Progression 1;")
    L_.append(f"Transfinite Curve {{{cZ}[]}} = {transZ} Using Progression 1;")

    # Surfaces from volume boundary
    L_.append(f"{s}[] = Abs(Boundary{{ Volume{{{i}}}; }});")
    L_.append(f"{s}[] = Unique({s}[]);")
    L_.append(f"Transfinite Surface {{{s}[]}};")
    L_.append(f"Recombine Surface {{{s}[]}};")
    L_.append(f"Transfinite Volume {{{i}}};")

    return L_


def multi_box_geo(
    boxes_: list[dict[str, Any]],
    *,
    preamble_lines: list[str] | None = None,
    eps: float = 1e-6,
    debug_select: bool = False,
) -> str:
    """
    Two-pass .geo emitter designed for ALWAYS-touching boxes plus mandatory Coherence;.

    Pass A: define parameters + create all Box(i)
    Coherence;
    Pass B: for each Volume i, do bounding-box selection and apply transfinite constraints.
    """
    lines: list[str] = []
    lines.append("//")
    lines.append('SetFactory("OpenCASCADE");')

    # Global eps (selection tolerance)
    lines.append("//+")
    lines.append(emit_define_number("eps", float(eps), "Global/Selection/eps"))

    if preamble_lines:
        lines.append("// PREAMBLE (shared parameters / derived counts) ")
        lines.extend(preamble_lines)

    # PASS A: geometry creation
    for i, b in enumerate(boxes_, start=1):
        XMeshSize = float(b.get("XMeshSize", 1.0))
        YMeshSize = float(b.get("YMeshSize", 1.0))
        ZMeshSize = float(b.get("ZMeshSize", 1.0))
        lTx = float(b.get("lTx", 20.0))
        lTy = float(b.get("lTy", 10.0))
        lTz = float(b.get("lTz", 10.0))
        x0 = float(b.get("x0", 0.0))
        y0 = float(b.get("y0", 0.0))
        z0 = float(b.get("z0", 0.0))

        Xms = f"XMeshSize_{i}"
        Yms = f"YMeshSize_{i}"
        Zms = f"ZMeshSize_{i}"
        Lx = f"lTx_{i}"
        Ly = f"lTy_{i}"
        Lz = f"lTz_{i}"
        X0 = f"x0_{i}"
        Y0 = f"y0_{i}"
        Z0 = f"z0_{i}"

        b["_sym"] = dict(Xms=Xms, Yms=Yms, Zms=Zms, Lx=Lx, Ly=Ly, Lz=Lz, X0=X0, Y0=Y0, Z0=Z0)

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
        lines.append(f"Box({i}) = {{{X0} - {Lx}/2, {Y0} - {Ly}/2, {Z0} - {Lz}, {Lx}, {Ly}, {Lz}}};")

    # Merge coincident topology across touching partitions
    lines.append("//+")
    lines.append("Coherence;")

    # PASS B: derived counts plus constraints
    for i, b in enumerate(boxes_, start=1):
        sym = b["_sym"]
        Xms, Yms, Zms = sym["Xms"], sym["Yms"], sym["Zms"]
        Lx, Ly, Lz = sym["Lx"], sym["Ly"], sym["Lz"]
        X0, Y0, Z0 = sym["X0"], sym["Y0"], sym["Z0"]

        default_tX = f"transX_{i}"
        default_tY = f"transY_{i}"
        default_tZ = f"transZ_{i}"

        tX_ = str(b.get("transX_name", default_tX))
        tY_ = str(b.get("transY_name", default_tY))
        tZ_ = str(b.get("transZ_name", default_tZ))

        define_tX = bool(b.get("define_transX", tX_ == default_tX))
        define_tY = bool(b.get("define_transY", tY_ == default_tY))
        define_tZ = bool(b.get("define_transZ", tZ_ == default_tZ))

        if define_tZ:
            lines.append("//+")
            lines.append(f"{tZ_} = Ceil({Lz}/{Zms}) + 1;")
        if define_tX:
            lines.append("//+")
            lines.append(f"{tX_} = Ceil({Lx}/{Xms}) + 1;")
        if define_tY:
            lines.append("//+")
            lines.append(f"{tY_} = Ceil({Ly}/{Yms}) + 1;")

        lines.append("//+")
        lines.extend(emit_bbox_transfinite_for_box(
            i,
            X0=X0, Y0=Y0, Z0=Z0,
            Lx=Lx, Ly=Ly, Lz=Lz,
            epsSym="eps",
            transX=tX_, transY=tY_, transZ=tZ_,
            debug=debug_select,
        ))

    return "\n".join(lines)


def make_layer_xy_partitions(
    *,
    xCenter: float,
    yCenter: float,
    zTop: float,
    thickness_: float,
    xWidths: list[float],
    yWidths: list[float],
    # mesh controls
    XMeshSizes_: list[float] | float,
    YMeshSizes_: list[float] | float,
    ZMeshSize_: float,
    # shared transfinite names
    transX_cols_: list[str],   # len == len(xWidths)
    transY_rows_: list[str],   # len == len(yWidths)
    transZ_name: str,
) -> list[dict[str, Any]]:
    """
    Build an X–Y grid of boxes for ONE Z-layer.

    Conformity rules:
      - along X interfaces (between columns): share transY_row and transZ
      - along Y interfaces (between rows):   share transX_col and transZ

    Therefore:
      - transX depends on column
      - transY depends on row
      - transZ depends on layer
    """
    nx = len(xWidths)
    ny = len(yWidths)
    if len(transX_cols_) != nx:
        raise ValueError("transX_cols must have same length as xWidths")
    if len(transY_rows_) != ny:
        raise ValueError("transY_rows must have same length as yWidths")

    if isinstance(XMeshSizes_, (int, float)):
        XMeshSizes_ = [float(XMeshSizes_)] * nx
    if isinstance(YMeshSizes_, (int, float)):
        YMeshSizes_ = [float(YMeshSizes_)] * ny
    if len(XMeshSizes_) != nx:
        raise ValueError("XMeshSizes_ must be a number or a list with len(xWidths)")
    if len(YMeshSizes_) != ny:
        raise ValueError("YMeshSizes_ must be a number or a list with len(yWidths)")

    total_Lx = float(sum(xWidths))
    total_Ly = float(sum(yWidths))
    x_min = xCenter - total_Lx / 2.0
    y_min = yCenter - total_Ly / 2.0

    boxes_: list[dict[str, Any]] = []

    y_cursor = y_min
    for h_, yms_, tY_ in zip(yWidths, YMeshSizes_, transY_rows_):
        h_ = float(h_)
        y0 = y_cursor + h_ / 2.0
        y_cursor += h_

        x_cursor = x_min
        for w_, xms_, tX_ in zip(xWidths, XMeshSizes_, transX_cols_):
            w_ = float(w_)
            x0 = x_cursor + w_ / 2.0
            x_cursor += w_

            boxes_.append(dict(
                x0=x0,
                y0=y0,
                z0=zTop,
                lTx=w_,
                lTy=h_,
                lTz=thickness_,
                XMeshSize=float(xms_),
                YMeshSize=float(yms_),
                ZMeshSize=float(ZMeshSize_),

                transX_name=tX_,
                transY_name=tY_,
                transZ_name=transZ_name,

                # define once in preamble, not per-box
                define_transX=False,
                define_transY=False,
                define_transZ=False,
            ))

    return boxes_


if __name__ == "__main__":
    # ------------------------------------------------------------------------------------
    # USER CONTROLS (PARTITIONING)
    # ------------------------------------------------------------------------------------

    # Domain center
    x_center = 0.0
    y_center = 0.0

    # X partitions (columns): widths plus desired X mesh sizes per column
    x_widths = [3 * 5, 1 * 2.68, 2 * 1.34, 1 * 0.5, 1 * 0.335]
    XMeshSizes = [5, 2.68, 1.34, 0.5, 0.335]

    # Y partitions (rows): heights + desired Y mesh sizes per row
    y_widths = [2 * 2.68, 1 * 0.5, 1 * 0.335]
    YMeshSizes = [2.68, 0.5, 0.335]

    # Z partitions (layers): each layer can have its own thickness plus Z mesh size
    layers = [
        dict(name="Layer1", z_top=0.0, thickness=5*1, ZMeshSize=1.0, transZ="transZ_L1"),
        dict(name="Layer2", z_top=-(5*1),  thickness=4*1.5,  ZMeshSize=1.5, transZ="transZ_L2"),
        dict(name="Layer3", z_top=-((4*1.5)+(5*1)), thickness=5*2,  ZMeshSize=2.0, transZ="transZ_L3"),
    ]

    # Shared transfinite symbols for X and Y:
    # - transX per column
    # - transY per row
    transX_cols = [f"transX_col{j+1}" for j in range(len(x_widths))]
    transY_rows = [f"transY_row{k+1}" for k in range(len(y_widths))]

    # ----------------------------------------------------------------------------------------------------------------
    # PREAMBLE: DEFINE COUNTS ONCE
    # ----------------------------------------------------------------------------------------------------------------
    preamble: list[str] = []

    # Define transX per column
    for j, (w, xms, tX) in enumerate(zip(x_widths, XMeshSizes, transX_cols), start=1):
        preamble.append("//+")
        preamble.append(emit_define_number(f"lTx_{tX}", float(w), f"X/Col {j}/Geometry/width"))
        preamble.append("//+")
        preamble.append(emit_define_number(f"XMeshSize_{tX}", float(xms), f"X/Col {j}/Mesh/XMeshSize"))
        preamble.append("//+")
        preamble.append(f"{tX} = Ceil(lTx_{tX}/XMeshSize_{tX}) + 1;")

    # Define transY per row
    for k, (h, yms, tY) in enumerate(zip(y_widths, YMeshSizes, transY_rows), start=1):
        preamble.append("//+")
        preamble.append(emit_define_number(f"lTy_{tY}", float(h), f"Y/Row {k}/Geometry/height"))
        preamble.append("//+")
        preamble.append(emit_define_number(f"YMeshSize_{tY}", float(yms), f"Y/Row {k}/Mesh/YMeshSize"))
        preamble.append("//+")
        preamble.append(f"{tY} = Ceil(lTy_{tY}/YMeshSize_{tY}) + 1;")

    # ----------------------------------------------------------------------------------------------------------------
    # BUILD BOXES (ALL LAYERS)
    # ----------------------------------------------------------------------------------------------------------------
    boxes: list[dict[str, Any]] = []

    for L in layers:
        z_top = float(L["z_top"])
        thickness = float(L["thickness"])
        zms = float(L["ZMeshSize"])
        tZ = str(L["transZ"])

        # define this layer's transZ once in preamble
        preamble.append("//+")
        preamble.append(emit_define_number(f"lTz_{tZ}", thickness, f'{L["name"]}/Geometry/thickness'))
        preamble.append("//+")
        preamble.append(emit_define_number(f"ZMeshSize_{tZ}", zms, f'{L["name"]}/Mesh/ZMeshSize'))
        preamble.append("//+")
        preamble.append(f"{tZ} = Ceil(lTz_{tZ}/ZMeshSize_{tZ}) + 1;")

        # build X–Y grid for this layer
        layer_boxes = make_layer_xy_partitions(
            xCenter=x_center,
            yCenter=y_center,
            zTop=z_top,
            thickness_=thickness,
            xWidths=x_widths,
            yWidths=y_widths,
            XMeshSizes_=XMeshSizes,
            YMeshSizes_=YMeshSizes,
            ZMeshSize_=zms,
            transX_cols_=transX_cols,
            transY_rows_=transY_rows,
            transZ_name=tZ,
        )
        boxes.extend(layer_boxes)

    # ----------------------------------------------------------------------------------------------------------------
    # EMIT .GEO
    # ----------------------------------------------------------------------------------------------------------------
    geo = multi_box_geo(
        boxes,
        preamble_lines=preamble,
        eps=1e-6,            # consider scaling this with geometry if needed
        debug_select=False,  # True prints selected curve tags in gmsh console
    )

    with open("modelDEL.geo", "w") as f:
        f.write(geo)
