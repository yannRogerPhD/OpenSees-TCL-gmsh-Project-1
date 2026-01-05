from __future__ import annotations
from typing import Any


def transfinite_lines_for_box(box_index: int, transX_name: str, transY_name: str, transZ_name: str) -> str:
    base = 12 * (box_index - 1)

    z_curves = [base + i for i in (1, 3, 5, 7)]
    y_curves = [base + i for i in (2, 4, 6, 8)]
    x_curves = [base + i for i in (9, 10, 11, 12)]

    return "\n".join([
        f"Transfinite Curve {{{', '.join(map(str, z_curves))}}} = {transZ_name} Using Progression 1;",
        f"Transfinite Curve {{{', '.join(map(str, x_curves))}}} = {transX_name} Using Progression 1;",
        f"Transfinite Curve {{{', '.join(map(str, y_curves))}}} = {transY_name} Using Progression 1;",
    ])


def surface_range_for_box(box_index: int) -> tuple[int, int]:
    start = 6 * (box_index - 1) + 1
    end = start + 5
    return start, end


def emit_define_number(var: str, value: float, gui_path: str) -> str:
    return f'{var} = DefineNumber[ {value}, Name "{gui_path}" ];'


def multi_box_geo(
    boxes_: list[dict[str, Any]],
    *,
    preamble_lines: list[str] | None = None,
) -> str:
    """
    boxes: list of dicts describing each box.
      Required per box: x0, y0, z0, lTx, lTy, lTz, XMeshSize, YMeshSize, ZMeshSize
      Optional overrides:
        transX_name, transY_name, transZ_name  (symbolic names to use)
        define_transX, define_transY, define_transZ (bool) whether to emit the Ceil(...) line for that symbol

    preamble_lines: inserted after SetFactory, before boxes (for shared variables).
    """
    lines: list[str] = []
    lines.append("//")
    lines.append('SetFactory("OpenCASCADE");')

    if preamble_lines:
        lines.append("// PREAMBLE (shared parameters / derived counts) ")
        lines.extend(preamble_lines)

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

        # default transfinite variable names (per-box)
        default_tX = f"transX_{i}"
        default_tY = f"transY_{i}"
        default_tZ = f"transZ_{i}"

        # allow overrides (shared symbolic names)
        tX_ = str(b.get("transX_name", default_tX))
        tY_ = str(b.get("transY_name", default_tY))
        tZ_ = str(b.get("transZ_name", default_tZ))

        # whether to define the corresponding transfinite symbol in this box block
        define_tX = bool(b.get("define_transX", tX_ == default_tX))
        define_tY = bool(b.get("define_transY", tY_ == default_tY))
        define_tZ = bool(b.get("define_transZ", tZ_ == default_tZ))

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

        # Geometry: centered in x/y, anchored at top in z
        lines.append("//+")
        lines.append(
            f"Box({i}) = {{{X0} - {Lx}/2, {Y0} - {Ly}/2, {Z0} - {Lz}, {Lx}, {Ly}, {Lz}}};"
        )

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

        # Apply transfinite constraints
        lines.append("//+")
        lines.append(transfinite_lines_for_box(i, tX_, tY_, tZ_))

        s0, s1 = surface_range_for_box(i)
        lines.append("//+")
        lines.append(f"Transfinite Surface {{{s0}:{s1}}};")
        lines.append("//+")
        lines.append(f"Recombine Surface {{{s0}:{s1}}};")
        lines.append("//+")
        lines.append(f"Transfinite Volume {{{i}}};")

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

    # (check): we ended exactly at x_center + total/2 (up to floating error)
    return boxes_


if __name__ == "__main__":
    # global shared Y subdivision for the whole model (interfaces in x need transY same)
    # We'll define transY_global once in the preamble and force every box to use it.
    lTy_global = 10.0
    YMeshSize_global = 1.0
    transY_global = "transY_global"

    # layer-specific Z subdivision (interfaces in x within the same layer need the same transZ)
    # Example: 2 layers, each layer gets its own transZ symbol.
    layers = [
        dict(name="Layer1", z_top=0.0,  thickness=5.0,  ZMeshSize=0.5, transZ="transZ_L1"),
        dict(name="Layer2", z_top=-5.0, thickness=7.0,  ZMeshSize=1.0, transZ="transZ_L2"),
    ]

    # X partitions (same pattern for both layers here, but you can vary per layer)
    x_center = 0.0
    y_center = 0.0
    x_widths = [8.0, 4.0, 8.0]          # sum = 20
    XMeshSizes = [0.5, 0.25, 0.5]       # refine the middle strip

    # We will build boxes for each layer and concatenate.
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

        # also force all these boxes to use transY_global symbolically (and don't define it per-box)
        for bb in layer_boxes:
            bb["transY_name"] = transY_global
            bb["define_transY"] = False

        boxes.extend(layer_boxes)

    geo = multi_box_geo(boxes, preamble_lines=preamble)

    with open("model3.geo", "w") as f:
        f.write(geo)
