from __future__ import annotations

from typing import Any


def emit_define_number(var: str, value: float, gui_path: str) -> str:
    return f'{var} = DefineNumber[ {value}, Name "{gui_path}" ];'


def emit_bbox_transfinite_for_box(
    i: int,
    *,
    X0: str, Y0: str, Z0: str,
    Lx: str, Ly: str, Lz: str,
    eps_sym: str,
    transX: str, transY: str, transZ: str,
    debug: bool = False,
) -> list[str]:
    """
    Robustly select the 12 edges of Box(i) using Curve In BoundingBox, then apply
    transfinite constraints. Boundary surfaces are obtained from Boundary{Volume{i};}
    so we never assume surface IDs.

    Intended to be emitted AFTER a global Coherence; (when touching boxes are merged).
    """
    # Local bounds (symbolic)
    xMin = f"({X0} - {Lx}/2)"
    xMax = f"({X0} + {Lx}/2)"
    yMin = f"({Y0} - {Ly}/2)"
    yMax = f"({Y0} + {Ly}/2)"
    zMin = f"({Z0} - {Lz})"
    zMax = f"({Z0})"

    e = eps_sym

    cX = f"cX_{i}"
    cY = f"cY_{i}"
    cZ = f"cZ_{i}"
    s = f"s_{i}"

    L_: list[str] = []
    L_.append(f"// --- Robust selection + transfinite for Volume {i} ---")
    L_.append(f"xMin_{i} = {xMin}; xMax_{i} = {xMax};")
    L_.append(f"yMin_{i} = {yMin}; yMax_{i} = {yMax};")
    L_.append(f"zMin_{i} = {zMin}; zMax_{i} = {zMax};")

    L_.append(f"{cX}[] = {{}}; {cY}[] = {{}}; {cZ}[] = {{}};")

    # X edges: y fixed at yMin/yMax, z fixed at zMin/zMax, x spans [xMin, xMax]
    L_.append(f"{cX}[] += Curve In BoundingBox {{ xMin_{i}-{e}, yMin_{i}-{e}, zMin_{i}-{e}, xMax_{i}+{e}, "
              f"yMin_{i}+{e}, zMin_{i}+{e} }};")
    L_.append(f"{cX}[] += Curve In BoundingBox {{ xMin_{i}-{e}, yMin_{i}-{e}, zMax_{i}-{e}, xMax_{i}+{e}, "
              f"yMin_{i}+{e}, zMax_{i}+{e} }};")
    L_.append(f"{cX}[] += Curve In BoundingBox {{ xMin_{i}-{e}, yMax_{i}-{e}, zMin_{i}-{e}, xMax_{i}+{e}, "
              f"yMax_{i}+{e}, zMin_{i}+{e} }};")
    L_.append(f"{cX}[] += Curve In BoundingBox {{ xMin_{i}-{e}, yMax_{i}-{e}, zMax_{i}-{e}, xMax_{i}+{e}, "
              f"yMax_{i}+{e}, zMax_{i}+{e} }};")

    # Y edges: x fixed at xMin/xMax, z fixed at zMin/zMax, y spans [yMin, yMax]
    L_.append(f"{cY}[] += Curve In BoundingBox {{ xMin_{i}-{e}, yMin_{i}-{e}, zMin_{i}-{e}, xMin_{i}+{e}, "
              f"yMax_{i}+{e}, zMin_{i}+{e} }};")
    L_.append(f"{cY}[] += Curve In BoundingBox {{ xMin_{i}-{e}, yMin_{i}-{e}, zMax_{i}-{e}, xMin_{i}+{e}, "
              f"yMax_{i}+{e}, zMax_{i}+{e} }};")
    L_.append(f"{cY}[] += Curve In BoundingBox {{ xMax_{i}-{e}, yMin_{i}-{e}, zMin_{i}-{e}, xMax_{i}+{e}, "
              f"yMax_{i}+{e}, zMin_{i}+{e} }};")
    L_.append(f"{cY}[] += Curve In BoundingBox {{ xMax_{i}-{e}, yMin_{i}-{e}, zMax_{i}-{e}, xMax_{i}+{e}, "
              f"yMax_{i}+{e}, zMax_{i}+{e} }};")

    # Z edges: x fixed at xMin/xMax, y fixed at yMin/yMax, z spans [zMin, zMax]
    L_.append(f"{cZ}[] += Curve In BoundingBox {{ xMin_{i}-{e}, yMin_{i}-{e}, zMin_{i}-{e}, xMin_{i}+{e}, "
              f"yMin_{i}+{e}, zMax_{i}+{e} }};")
    L_.append(f"{cZ}[] += Curve In BoundingBox {{ xMin_{i}-{e}, yMax_{i}-{e}, zMin_{i}-{e}, xMin_{i}+{e}, "
              f"yMax_{i}+{e}, zMax_{i}+{e} }};")
    L_.append(f"{cZ}[] += Curve In BoundingBox {{ xMax_{i}-{e}, yMin_{i}-{e}, zMin_{i}-{e}, xMax_{i}+{e}, "
              f"yMin_{i}+{e}, zMax_{i}+{e} }};")
    L_.append(f"{cZ}[] += Curve In BoundingBox {{ xMax_{i}-{e}, yMax_{i}-{e}, zMin_{i}-{e}, xMax_{i}+{e}, "
              f"yMax_{i}+{e}, zMax_{i}+{e} }};")

    # Post-process: Abs() to remove any orientation sign, Unique() to deduplicate.
    # (Abs(list) is elementwise in .geo expressions.)
    L_.append(f"{cX}[] = Abs({cX}[]); {cX}[] = Unique({cX}[]);")
    L_.append(f"{cY}[] = Abs({cY}[]); {cY}[] = Unique({cY}[]);")
    L_.append(f"{cZ}[] = Abs({cZ}[]); {cZ}[] = Unique({cZ}[]);")

    if debug:
        L_.append(f'Printf("Box/Vol {i}: #cX=%g #cY=%g #cZ=%g", #{cX}[], #{cY}[], #{cZ}[]);')
        L_.append(f'For k In {{0:#{cX}[]-1}} Printf("  {cX}[%g]=%g", k, {cX}[k]); EndFor')
        L_.append(f'For k In {{0:#{cY}[]-1}} Printf("  {cY}[%g]=%g", k, {cY}[k]); EndFor')
        L_.append(f'For k In {{0:#{cZ}[]-1}} Printf("  {cZ}[%g]=%g", k, {cZ}[k]); EndFor')

    # Apply curve constraints (transX/transY/transZ are symbolic counts)
    L_.append(f"Transfinite Curve {{{cX}[]}} = {transX} Using Progression 1;")
    L_.append(f"Transfinite Curve {{{cY}[]}} = {transY} Using Progression 1;")
    L_.append(f"Transfinite Curve {{{cZ}[]}} = {transZ} Using Progression 1;")

    # Boundary surfaces: get from volume, remove orientation sign, then transfinite+recombine
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
    Two-pass .geo emitter designed for ALWAYS-touching boxes PLUS mandatory "Coherence".

    Pass A: define parameters + create all Box(i)
    Coherence;
    Pass B: for each Volume i, do bounding-box selection and apply transfinite constraints.

    boxes_: list of dicts describing each box.
      Required per box: x0, y0, z0, lTx, lTy, lTz, XMeshSize, YMeshSize, ZMeshSize
      Optional overrides:
        transX_name, transY_name, transZ_name (symbolic names)
        define_transX, define_transY, define_transZ (bool)
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

    # -------------------------
    # PASS A: geometry creation
    # -------------------------
    for i, b in enumerate(boxes_, start=1):
        # numeric defaults for DefineNumber values
        XMeshSize = float(b.get("XMeshSize", 1.0))
        YMeshSize = float(b.get("YMeshSize", 1.0))
        ZMeshSize = float(b.get("ZMeshSize", 1.0))
        lTx = float(b.get("lTx", 20.0))
        lTy = float(b.get("lTy", 10.0))
        lTz = float(b.get("lTz", 10.0))
        x0 = float(b.get("x0", 0.0))
        y0 = float(b.get("y0", 0.0))
        z0 = float(b.get("z0", 0.0))

        # variable names for this box
        Xms = f"XMeshSize_{i}"
        Yms = f"YMeshSize_{i}"
        Zms = f"ZMeshSize_{i}"
        Lx = f"lTx_{i}"
        Ly = f"lTy_{i}"
        Lz = f"lTz_{i}"
        X0 = f"x0_{i}"
        Y0 = f"y0_{i}"
        Z0 = f"z0_{i}"

        # store back for pass B (symbolic variable names)
        b["_sym"] = dict(Xms=Xms, Yms=Yms, Zms=Zms, Lx=Lx, Ly=Ly, Lz=Lz, X0=X0, Y0=Y0, Z0=Z0)

        # GUI-grouped parameters
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

        # Geometry: centered in x/y, anchored at top in z (same as your original)
        lines.append("//+")
        lines.append(f"Box({i}) = {{{X0} - {Lx}/2, {Y0} - {Ly}/2, {Z0} - {Lz}, {Lx}, {Ly}, {Lz}}};")

    # Merge coincident topology across touching partitions
    lines.append("//+")
    lines.append("Coherence;")

    # --------------------------------------
    # PASS B: transfinite counts + constraints
    # --------------------------------------
    for i, b in enumerate(boxes_, start=1):
        sym = b["_sym"]
        Xms, Yms, Zms = sym["Xms"], sym["Yms"], sym["Zms"]
        Lx, Ly, Lz = sym["Lx"], sym["Ly"], sym["Lz"]
        X0, Y0, Z0 = sym["X0"], sym["Y0"], sym["Z0"]

        # default transfinite variable names (per-box)
        default_tX = f"transX_{i}"
        default_tY = f"transY_{i}"
        default_tZ = f"transZ_{i}"

        # allow overrides (shared symbolic names)
        tX_ = str(b.get("transX_name", default_tX))
        tY_ = str(b.get("transY_name", default_tY))
        tZ_ = str(b.get("transZ_name", default_tZ))

        # whether to define the corresponding transfinite symbol in this pass
        define_tX = bool(b.get("define_transX", tX_ == default_tX))
        define_tY = bool(b.get("define_transY", tY_ == default_tY))
        define_tZ = bool(b.get("define_transZ", tZ_ == default_tZ))

        # Derived transfinite counts (symbolic)
        if define_tZ:
            lines.append("//+")
            lines.append(f"{tZ_} = Ceil({Lz}/{Zms}) + 1;")
        if define_tX:
            lines.append("//+")
            lines.append(f"{tX_} = Ceil({Lx}/{Xms}) + 1;")
        if define_tY:
            lines.append("//+")
            lines.append(f"{tY_} = Ceil({Ly}/{Yms}) + 1;")

        # Robust selection + transfinite constraints (after Coherence)
        lines.append("//+")
        lines.extend(emit_bbox_transfinite_for_box(
            i,
            X0=X0, Y0=Y0, Z0=Z0,
            Lx=Lx, Ly=Ly, Lz=Lz,
            eps_sym="eps",
            transX=tX_, transY=tY_, transZ=tZ_,
            debug=debug_select,
        ))

    return "\n".join(lines)


def make_layer_x_partitions(
    *,
    xCenter: float,
    yCenter: float,
    zTop: float,
    lTy: float,
    thickness_: float,
    xWidths: list[float],
    # mesh controls
    XMeshSizes_: list[float] | float,
    YMeshSize_: float,
    ZMeshSize_: float,
    # shared transfinite names to enforce conformity
    transY_name: str,
    transZ_name: str,
) -> list[dict[str, Any]]:
    """
    Build boxes that tile the x-direction for ONE layer (same z_top, same thickness).
    The boxes are adjacent in the x-direction by construction.

    Interface conformity between x-neighbors:
      - they share a YZ face -> they must share transY and transZ
      - we enforce this by passing the same transY_name and transZ_name to every partition box
    """
    if isinstance(XMeshSizes_, (int, float)):
        XMeshSizes_ = [float(XMeshSizes_)] * len(xWidths)
    if len(XMeshSizes_) != len(xWidths):
        raise ValueError("XMeshSizes must be a single number or a list of same length as x_widths")

    total_Lx = float(sum(xWidths))
    x_min = xCenter - total_Lx / 2.0

    boxes_: list[dict[str, Any]] = []
    cursor = x_min
    for w, xms in zip(xWidths, XMeshSizes_):
        w = float(w)
        x0 = cursor + w / 2.0  # center of this subdomain
        cursor += w

        boxes_.append(dict(
            x0=x0,
            y0=yCenter,
            z0=zTop,
            lTx=w,
            lTy=lTy,
            lTz=thickness_,
            XMeshSize=float(xms),
            YMeshSize=float(YMeshSize_),
            ZMeshSize=float(ZMeshSize_),

            # enforce conformity on shared vertical faces:
            transY_name=transY_name,
            transZ_name=transZ_name,
            define_transY=False,  # define once in preamble
            define_transZ=False,  # define once per-layer in preamble
        ))

    return boxes_


if __name__ == "__main__":
    # Global shared Y subdivision for the whole model (interfaces in x need transY same)
    lTy_global = 10.0
    YMeshSize_global = 1.0
    transY_global = "transY_global"

    # Example: 2 layers, each layer gets its own transZ symbol (interfaces in x within a layer share transZ)
    layers = [
        dict(name="Layer1", z_top=0.0,  thickness=5.0,  ZMeshSize=0.5, transZ="transZ_L1"),
        dict(name="Layer2", z_top=-5.0, thickness=7.0,  ZMeshSize=1.0, transZ="transZ_L2"),
    ]

    # X partitions (same pattern for both layers here)
    x_center = 0.0
    y_center = 0.0
    x_widths = [8.0, 4.0, 8.0]          # sum = 20
    XMeshSizes = [0.5, 0.25, 0.5]       # refine the middle strip

    boxes: list[dict[str, Any]] = []

    # PREAMBLE: define shared transY once, plus each layer's transZ once
    preamble: list[str] = []
    preamble.append("//+")
    preamble.append(emit_define_number("lTy_global", lTy_global, "Global/Geometry/lTy"))
    preamble.append("//+")
    preamble.append(emit_define_number("YMeshSize_global", YMeshSize_global, "Global/Mesh/YMeshSize"))
    preamble.append("//+")
    preamble.append(f"{transY_global} = Ceil(lTy_global/YMeshSize_global) + 1;")

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

        # build x partitions for this layer (all share transY_global and this layer's transZ)
        layer_boxes = make_layer_x_partitions(
            xCenter=x_center,
            yCenter=y_center,
            zTop=z_top,
            lTy=lTy_global,
            thickness_=thickness,
            xWidths=x_widths,
            XMeshSizes_=XMeshSizes,
            YMeshSize_=YMeshSize_global,
            ZMeshSize_=zms,
            transY_name=transY_global,
            transZ_name=tZ,
        )

        # enforce transY_global symbolically (and don't define it per-box)
        for bb in layer_boxes:
            bb["transY_name"] = transY_global
            bb["define_transY"] = False

        boxes.extend(layer_boxes)

    geo = multi_box_geo(
        boxes,
        preamble_lines=preamble,
        eps=1e-6,          # adjust if your model scale is huge/small
        debug_select=False  # set True to print counts and selected curve tags
    )

    with open("model.geo", "w") as f:
        f.write(geo)
