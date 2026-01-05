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
        shared_: dict[str, Any] | None = None,
) -> str:
    """
    shared (optional) can define shared plan dimensions + mesh sizes + shared transfinite names.
    Example:
      shared = {
        "lTx": 20.0, "lTy": 10.0,
        "XMeshSize": 1.0, "YMeshSize": 1.0,
        "names": {"lTx": "lTx_stack", "lTy": "lTy_stack",
                  "XMeshSize": "XMeshSize_stack", "YMeshSize": "YMeshSize_stack",
                  "transX": "transX_stack", "transY": "transY_stack"}
      }

    If shared is provided, we emit those parameters at the top and compute transX/transY once.
    Individual boxes can then reference them via box dict entries:
      transX_name="transX_stack", transY_name="transY_stack"
    """
    lines: list[str] = []
    lines.append("//")
    lines.append('SetFactory("OpenCASCADE");')

    # ----- Shared header (optional) -----
    if shared_ is not None:
        names = shared_.get("names", {})
        lTx_name = names.get("lTx", "lTx_stack")
        lTy_name = names.get("lTy", "lTy_stack")
        Xms_name = names.get("XMeshSize", "XMeshSize_stack")
        Yms_name = names.get("YMeshSize", "YMeshSize_stack")
        tX_name = names.get("transX", "transX_stack")
        tY_name = names.get("transY", "transY_stack")

        lTx_val = float(shared_["lTx"])
        lTy_val = float(shared_["lTy"])
        Xms_val = float(shared_["XMeshSize"])
        Yms_val = float(shared_["YMeshSize"])

        lines.append("//+")
        lines.append(emit_define_number(lTx_name, lTx_val, "Stack/Geometry/lTx"))
        lines.append("//+")
        lines.append(emit_define_number(lTy_name, lTy_val, "Stack/Geometry/lTy"))
        lines.append("//+")
        lines.append(emit_define_number(Xms_name, Xms_val, "Stack/Mesh/XMeshSize"))
        lines.append("//+")
        lines.append(emit_define_number(Yms_name, Yms_val, "Stack/Mesh/YMeshSize"))

        # shared transfinite counts
        lines.append("//+")
        lines.append(f"{tX_name} = Ceil({lTx_name}/{Xms_name}) + 1;")
        lines.append("//+")
        lines.append(f"{tY_name} = Ceil({lTy_name}/{Yms_name}) + 1;")

    # ----- Boxes -----
    for i, b in enumerate(boxes_, start=1):
        # defaults
        ZMeshSize = float(b.get("ZMeshSize", 1.0))
        lTz = float(b.get("lTz", 10.0))
        x0 = float(b.get("x0", 0.0))
        y0 = float(b.get("y0", 0.0))
        z0 = float(b.get("z0", 0.0))

        # If shared exists, layers may omit lTx/lTy and X/Y mesh sizes
        if shared_ is None:
            XMeshSize = float(b.get("XMeshSize", 1.0))
            YMeshSize = float(b.get("YMeshSize", 1.0))
            lTx = float(b.get("lTx", 20.0))
            lTy = float(b.get("lTy", 10.0))
        else:
            # Not used for Box definition if you point Box to shared variable names; we do that below.
            XMeshSize = float(b.get("XMeshSize", shared_["XMeshSize"]))
            YMeshSize = float(b.get("YMeshSize", shared_["YMeshSize"]))
            lTx = float(b.get("lTx", shared_["lTx"]))
            lTy = float(b.get("lTy", shared_["lTy"]))

        # unique variable names per box
        Zms = f"ZMeshSize_{i}"
        Lz = f"lTz_{i}"
        X0 = f"x0_{i}"
        Y0 = f"y0_{i}"
        Z0 = f"z0_{i}"

        # either per-box names or shared names for plan dims / mesh
        if shared_ is None:
            Xms = f"XMeshSize_{i}"
            Yms = f"YMeshSize_{i}"
            Lx = f"lTx_{i}"
            Ly = f"lTy_{i}"
        else:
            names = shared_.get("names", {})
            Xms = names.get("XMeshSize", "XMeshSize_stack")
            Yms = names.get("YMeshSize", "YMeshSize_stack")
            Lx = names.get("lTx", "lTx_stack")
            Ly = names.get("lTy", "lTy_stack")

        # transfinite names
        # default per-layer transZ_i always
        tZ = f"transZ_{i}"
        # X/Y can be shared if the caller requests it
        tX = b.get("transX_name", (f"transX_{i}" if shared_ is None else shared_.get("names", {}).get("transX",
                                                                                                      "transX_stack")))
        tY = b.get("transY_name", (f"transY_{i}" if shared_ is None else shared_.get("names", {}).get("transY",
                                                                                                      "transY_stack")))

        # ---- Parameters ----
        # Only define per-box plan parameters if not shared
        if shared_ is None:
            lines.append("//+")
            lines.append(emit_define_number(Xms, XMeshSize, f"Box {i}/Mesh/XMeshSize"))
            lines.append("//+")
            lines.append(emit_define_number(Yms, YMeshSize, f"Box {i}/Mesh/YMeshSize"))
            lines.append("//+")
            lines.append(emit_define_number(f"lTx_{i}", lTx, f"Box {i}/Geometry/lTx"))
            lines.append("//+")
            lines.append(emit_define_number(f"lTy_{i}", lTy, f"Box {i}/Geometry/lTy"))

        # always per-box vertical mesh + thickness + location
        lines.append("//+")
        lines.append(emit_define_number(Zms, ZMeshSize, f"Box {i}/Mesh/ZMeshSize"))
        lines.append("//+")
        lines.append(emit_define_number(Lz, lTz, f"Box {i}/Geometry/lTz"))
        lines.append("//+")
        lines.append(emit_define_number(X0, x0, f"Box {i}/Geometry/x0"))
        lines.append("//+")
        lines.append(emit_define_number(Y0, y0, f"Box {i}/Geometry/y0"))
        lines.append("//+")
        lines.append(emit_define_number(Z0, z0, f"Box {i}/Geometry/z0"))

        # ---- Geometry (centered in x/y, anchored at top in z) ----
        lines.append("//+")
        lines.append(
            f"Box({i}) = {{{X0} - {Lx}/2, {Y0} - {Ly}/2, {Z0} - {Lz}, {Lx}, {Ly}, {Lz}}};"
        )

        # ---- Transfinite counts ----
        lines.append("//+")
        lines.append(f"{tZ} = Ceil({Lz}/{Zms}) + 1;")

        # If X/Y are not shared (per-box), define them. If they’re shared, they were defined in header.
        if shared_ is None:
            lines.append("//+")
            lines.append(f"{tX} = Ceil({Lx}/{Xms}) + 1;")
            lines.append("//+")
            lines.append(f"{tY} = Ceil({Ly}/{Yms}) + 1;")

        # ---- Transfinite constraints ----
        lines.append("//+")
        lines.append(transfinite_lines_for_box(i, tX, tY, tZ))

        s0, s1 = surface_range_for_box(i)
        lines.append("//+")
        lines.append(f"Transfinite Surface {{{s0}:{s1}}};")
        lines.append("//+")
        lines.append(f"Recombine Surface {{{s0}:{s1}}};")
        lines.append("//+")
        lines.append(f"Transfinite Volume {{{i}}};")

    return "\n".join(lines)


def make_layer_stack(
        *,
        x0: float,
        y0: float,
        z_top: float,
        layer_thicknesses: list[float],
        ZMeshSizes: list[float] | float = 1.0,
        transX_name: str = "transX_stack",
        transY_name: str = "transY_stack",
) -> list[dict[str, Any]]:
    """
    Creates adjacent vertical layers. Plan dimensions are assumed shared and provided via multi_box_geo(shared=...).

    Each layer:
      - shares transX/transY names for conforming interfaces
      - gets its own z0 (top) and lTz (thickness) and ZMeshSize
    """
    if isinstance(ZMeshSizes, (int, float)):
        ZMeshSizes = [float(ZMeshSizes)] * len(layer_thicknesses)
    if len(ZMeshSizes) != len(layer_thicknesses):
        raise ValueError("ZMeshSizes must be a single number or a list with same length as layer_thicknesses")

    boxes_: list[dict[str, Any]] = []
    current_z_top = z_top

    for thk, zms in zip(layer_thicknesses, ZMeshSizes):
        boxes_.append(dict(
            x0=x0, y0=y0, z0=current_z_top,
            lTz=float(thk),
            ZMeshSize=float(zms),
            transX_name=transX_name,
            transY_name=transY_name,
        ))
        current_z_top -= float(thk)

    return boxes_


if __name__ == "__main__":
    # Shared plan parameters for the whole soil column
    shared = {
        "lTx": 20.0,
        "lTy": 10.0,
        "XMeshSize": 1.0,
        "YMeshSize": 1.0,
        "names": {
            "lTx": "lTx_stack",
            "lTy": "lTy_stack",
            "XMeshSize": "XMeshSize_stack",
            "YMeshSize": "YMeshSize_stack",
            "transX": "transX_stack",
            "transY": "transY_stack",
        }
    }

    boxes = make_layer_stack(
        x0=0.0, y0=0.0, z_top=0.0,
        layer_thicknesses=[2.0, 5.0, 3.0],
        ZMeshSizes=[0.5, 1.0, 0.5],
    )

    geo = multi_box_geo(boxes, shared_=shared)

    with open("model.geo", "w") as f:
        f.write(geo)
