from __future__ import annotations

from dataclasses import dataclass
# from typing import Any, Iterable


# -----------------------------
# Data model (simple + explicit)
# -----------------------------

@dataclass(frozen=True)
class BoxSpec:
    # geometry (centered in x/y, top at z0, thickness downward)
    x0: float
    y0: float
    z0: float
    Lx: float
    Ly: float
    Lz: float

    # mesh size controls (used only to compute transfinite counts)
    XMeshSize: float
    YMeshSize: float
    ZMeshSize: float

    # symbolic transfinite names (for conformity)
    transX: str
    transY: str
    transZ: str


@dataclass(frozen=True)
class SymmetrySpec:
    enabled: bool
    # plane: a*x + b*y + c*z + d = 0
    a: float
    b: float
    c: float
    d: float
    # mirror which original volumes (1...N), default: all
    volumes: str = "all"  # "all" or "list"
    volume_list: tuple[int, ...] = ()


# -----------------------------
# Helpers for emitting .geo
# -----------------------------

def _fmt(x: float) -> str:
    # compact float formatting for .geo
    return f"{x:.16g}"


def _emit_bbox_curve_constraints(
    tag: str,
    *,
    X0: str, Y0: str, Z0: str,
    Lx: str, Ly: str, Lz: str,
    eps: str,
    transX: str, transY: str, transZ: str,
) -> list[str]:
    """
    Emit ONLY:
      - Curve In BoundingBox selections (cX_tag, cY_tag, cZ_tag)
      - Transfinite Curve constraints

    This is robust to entity renumbering and works after Coherence.
    """
    xMin = f"({X0} - {Lx}/2)"
    xMax = f"({X0} + {Lx}/2)"
    yMin = f"({Y0} - {Ly}/2)"
    yMax = f"({Y0} + {Ly}/2)"
    zMin = f"({Z0} - {Lz})"
    zMax = f"({Z0})"

    cX = f"cX_{tag}"
    cY = f"cY_{tag}"
    cZ = f"cZ_{tag}"

    L_: list[str] = []
    L_.append(f"xMin_{tag} = {xMin}; xMax_{tag} = {xMax};")
    L_.append(f"yMin_{tag} = {yMin}; yMax_{tag} = {yMax};")
    L_.append(f"zMin_{tag} = {zMin}; zMax_{tag} = {zMax};")

    L_.append(f"{cX}[] = {{}}; {cY}[] = {{}}; {cZ}[] = {{}};")

    # X edges
    L_.append(
        f"{cX}[] += Curve In BoundingBox {{ xMin_{tag}-{eps}, yMin_{tag}-{eps}, zMin_{tag}-{eps}, "
        f"xMax_{tag}+{eps}, yMin_{tag}+{eps}, zMin_{tag}+{eps} }};"
    )
    L_.append(
        f"{cX}[] += Curve In BoundingBox {{ xMin_{tag}-{eps}, yMin_{tag}-{eps}, zMax_{tag}-{eps}, "
        f"xMax_{tag}+{eps}, yMin_{tag}+{eps}, zMax_{tag}+{eps} }};"
    )
    L_.append(
        f"{cX}[] += Curve In BoundingBox {{ xMin_{tag}-{eps}, yMax_{tag}-{eps}, zMin_{tag}-{eps}, "
        f"xMax_{tag}+{eps}, yMax_{tag}+{eps}, zMin_{tag}+{eps} }};"
    )
    L_.append(
        f"{cX}[] += Curve In BoundingBox {{ xMin_{tag}-{eps}, yMax_{tag}-{eps}, zMax_{tag}-{eps}, "
        f"xMax_{tag}+{eps}, yMax_{tag}+{eps}, zMax_{tag}+{eps} }};"
    )

    # Y edges
    L_.append(
        f"{cY}[] += Curve In BoundingBox {{ xMin_{tag}-{eps}, yMin_{tag}-{eps}, zMin_{tag}-{eps}, "
        f"xMin_{tag}+{eps}, yMax_{tag}+{eps}, zMin_{tag}+{eps} }};"
    )
    L_.append(
        f"{cY}[] += Curve In BoundingBox {{ xMin_{tag}-{eps}, yMin_{tag}-{eps}, zMax_{tag}-{eps}, "
        f"xMin_{tag}+{eps}, yMax_{tag}+{eps}, zMax_{tag}+{eps} }};"
    )
    L_.append(
        f"{cY}[] += Curve In BoundingBox {{ xMax_{tag}-{eps}, yMin_{tag}-{eps}, zMin_{tag}-{eps}, "
        f"xMax_{tag}+{eps}, yMax_{tag}+{eps}, zMin_{tag}+{eps} }};"
    )
    L_.append(
        f"{cY}[] += Curve In BoundingBox {{ xMax_{tag}-{eps}, yMin_{tag}-{eps}, zMax_{tag}-{eps}, "
        f"xMax_{tag}+{eps}, yMax_{tag}+{eps}, zMax_{tag}+{eps} }};"
    )

    # Z edges
    L_.append(
        f"{cZ}[] += Curve In BoundingBox {{ xMin_{tag}-{eps}, yMin_{tag}-{eps}, zMin_{tag}-{eps}, "
        f"xMin_{tag}+{eps}, yMin_{tag}+{eps}, zMax_{tag}+{eps} }};"
    )
    L_.append(
        f"{cZ}[] += Curve In BoundingBox {{ xMin_{tag}-{eps}, yMax_{tag}-{eps}, zMin_{tag}-{eps}, "
        f"xMin_{tag}+{eps}, yMax_{tag}+{eps}, zMax_{tag}+{eps} }};"
    )
    L_.append(
        f"{cZ}[] += Curve In BoundingBox {{ xMax_{tag}-{eps}, yMin_{tag}-{eps}, zMin_{tag}-{eps}, "
        f"xMax_{tag}+{eps}, yMin_{tag}+{eps}, zMax_{tag}+{eps} }};"
    )
    L_.append(
        f"{cZ}[] += Curve In BoundingBox {{ xMax_{tag}-{eps}, yMax_{tag}-{eps}, zMin_{tag}-{eps}, "
        f"xMax_{tag}+{eps}, yMax_{tag}+{eps}, zMax_{tag}+{eps} }};"
    )

    # Dedup + abs
    L_.append(f"{cX}[] = Unique(Abs({cX}[]));")
    L_.append(f"{cY}[] = Unique(Abs({cY}[]));")
    L_.append(f"{cZ}[] = Unique(Abs({cZ}[]));")

    # Transfinite
    L_.append(f"Transfinite Curve {{{cX}[]}} = {transX} Using Progression 1;")
    L_.append(f"Transfinite Curve {{{cY}[]}} = {transY} Using Progression 1;")
    L_.append(f"Transfinite Curve {{{cZ}[]}} = {transZ} Using Progression 1;")

    return L_


def _emit_mirrored_center_def(
    tag: str,
    *,
    X0: str, Y0: str, Z0: str,
    a: str, b: str, c: str, d: str,
) -> tuple[str, str, str, list[str]]:
    """
    Symbolic reflection of a point across plane a*x + b*y + c*z + d = 0.
    p' = p - 2 * (a*x+b*y+c*z+d)/(a^2+b^2+c^2) * (a,b,c)
    """
    denom = f"(({a})*({a}) + ({b})*({b}) + ({c})*({c}))"
    dist = f"(({a})*({X0}) + ({b})*({Y0}) + ({c})*({Z0}) + ({d}))/{denom}"

    Xm = f"{X0}_mir_{tag}"
    Ym = f"{Y0}_mir_{tag}"
    Zm = f"{Z0}_mir_{tag}"

    defS = [
        f"{Xm} = ({X0}) - 2*({dist})*({a});",
        f"{Ym} = ({Y0}) - 2*({dist})*({b});",
        f"{Zm} = ({Z0}) - 2*({dist})*({c});",
    ]
    return Xm, Ym, Zm, defS


# -----------------------------
# Partition builders (X - Y grid)
# -----------------------------

def build_layer_xy(
    *,
    xCenter: float,
    yCenter: float,
    zTop: float,
    thickness: float,
    xWidths: list[float],
    yWidths: list[float],
    XMeshSizes_: list[float] | float,
    YMeshSizes_: list[float] | float,
    ZMeshSize: float,
    transXCols: list[str],
    transYRows: list[str],
    transZ: str,
) -> list[BoxSpec]:
    nx, ny = len(xWidths), len(yWidths)
    if len(transXCols) != nx:
        raise ValueError("transX_cols must have len(xWidths)")
    if len(transYRows) != ny:
        raise ValueError("transY_rows must have len(yWidths)")

    if isinstance(XMeshSizes_, (int, float)):
        XMeshSizes_ = [float(XMeshSizes_)] * nx
    if isinstance(YMeshSizes_, (int, float)):
        YMeshSizes_ = [float(YMeshSizes_)] * ny
    if len(XMeshSizes_) != nx:
        raise ValueError("XMeshSizes must be a float or list with len(xWidths)")
    if len(YMeshSizes_) != ny:
        raise ValueError("YMeshSizes must be a float or list with len(yWidths)")

    total_Lx = float(sum(xWidths))
    total_Ly = float(sum(yWidths))
    x_min = xCenter - total_Lx / 2.0
    y_min = yCenter - total_Ly / 2.0

    boxes: list[BoxSpec] = []
    y_cursor = y_min
    for row, (Ly, yms, tY) in enumerate(zip(yWidths, YMeshSizes_, transYRows), start=1):
        Ly = float(Ly)
        y0 = y_cursor + Ly / 2.0
        y_cursor += Ly

        x_cursor = x_min
        for col, (Lx, xms, tX) in enumerate(zip(xWidths, XMeshSizes_, transXCols), start=1):
            Lx = float(Lx)
            x0 = x_cursor + Lx / 2.0
            x_cursor += Lx

            boxes.append(
                BoxSpec(
                    x0=x0, y0=y0, z0=zTop,
                    Lx=Lx, Ly=Ly, Lz=thickness,
                    XMeshSize=float(xms),
                    YMeshSize=float(yms),
                    ZMeshSize=float(ZMeshSize),
                    transX=tX, transY=tY, transZ=transZ,
                )
            )
    return boxes


# -----------------------------
# Main emitter
# -----------------------------

def emit_geo(
    boxes: list[BoxSpec],
    *,
    eps: float = 1e-6,
    symmetry_: SymmetrySpec | None = None,
) -> str:
    """
    Clean .geo:
      - plain assignments (no DefineNumber)
      - optional Symmetry + DUPLICATA before Coherence
      - Coherence
      - curve constraints via bounding boxes for original + mirrored regions (if enabled)
      - apply transfinite surface/recombine/volume to all volumes found post-Coherence
    """
    L_: list[str] = []
    L_.append('//')
    L_.append('SetFactory("OpenCASCADE");')
    L_.append(f"eps = {_fmt(eps)};")
    L_.append("")

    # Geometry: create boxes with direct numeric params
    for i, b in enumerate(boxes, start=1):
        L_.append(
            f"Box({i}) = {{{_fmt(b.x0 - b.Lx/2)}, {_fmt(b.y0 - b.Ly/2)}, {_fmt(b.z0 - b.Lz)}, "
            f"{_fmt(b.Lx)}, {_fmt(b.Ly)}, {_fmt(b.Lz)}}};"
        )

    n_orig = len(boxes)

    # Optional symmetry (pre-Coherence)
    sym_enabled = bool(symmetry_ and symmetry_.enabled)
    if sym_enabled:
        a, b_, c, d = symmetry_.a, symmetry_.b, symmetry_.c, symmetry_.d
        L_.append("")
        L_.append(f"sym_a = {_fmt(a)}; sym_b = {_fmt(b_)}; sym_c = {_fmt(c)}; sym_d = {_fmt(d)};")

        if symmetry_.volumes == "list" and symmetry_.volume_list:
            vol_sel = ", ".join(str(int(v)) for v in symmetry_.volume_list)
        else:
            vol_sel = f"1:{n_orig}"

        L_.append(f"symDup[] = Symmetry {{sym_a, sym_b, sym_c, sym_d}} {{ Duplicata {{ Volume{{{vol_sel}}}; }} }};")

    # Coherence mandatory (touching boxes)
    L_.append("")
    L_.append("Coherence;")
    L_.append("")

    # Define transfinite counts as plain variables (deduplicate by symbol name)
    # We compute them from (Lx/Ly/Lz)/(mesh size) + 1 using Ceil.
    # Even though Lx etc. are numeric here, we keep it explicit and readable.
    seen: set[str] = set()
    for b in boxes:
        if b.transX not in seen:
            seen.add(b.transX)
            L_.append(f"{b.transX} = Ceil({_fmt(b.Lx)}/{_fmt(b.XMeshSize)}) + 1;")
        if b.transY not in seen:
            seen.add(b.transY)
            L_.append(f"{b.transY} = Ceil({_fmt(b.Ly)}/{_fmt(b.YMeshSize)}) + 1;")
        if b.transZ not in seen:
            seen.add(b.transZ)
            L_.append(f"{b.transZ} = Ceil({_fmt(b.Lz)}/{_fmt(b.ZMeshSize)}) + 1;")

    L_.append("")

    # Curve constraints for each ORIGINAL region (by geometry)
    for i, b in enumerate(boxes, start=1):
        # define per-region center/size as variables (keeps .geo readable and mirrorable)
        X0 = f"x0_{i}"
        Y0 = f"y0_{i}"
        Z0 = f"z0_{i}"
        Lx = f"Lx_{i}"
        Ly = f"Ly_{i}"
        Lz = f"Lz_{i}"

        L_.append(f"{X0} = {_fmt(b.x0)}; {Y0} = {_fmt(b.y0)}; {Z0} = {_fmt(b.z0)};")
        L_.append(f"{Lx} = {_fmt(b.Lx)}; {Ly} = {_fmt(b.Ly)}; {Lz} = {_fmt(b.Lz)};")

        L_.extend(_emit_bbox_curve_constraints(
            str(i),
            X0=X0, Y0=Y0, Z0=Z0,
            Lx=Lx, Ly=Ly, Lz=Lz,
            eps="eps",
            transX=b.transX, transY=b.transY, transZ=b.transZ,
        ))
        L_.append("")

        # Mirrored region constraints (symbolic) if symmetry enabled
        if sym_enabled:
            Xm, Ym, Zm, defS = _emit_mirrored_center_def(
                str(i),
                X0=X0, Y0=Y0, Z0=Z0,
                a="sym_a", b="sym_b", c="sym_c", d="sym_d",
            )
            L_.extend(defS)
            L_.extend(_emit_bbox_curve_constraints(
                f"{i}_mir",
                X0=Xm, Y0=Ym, Z0=Zm,
                Lx=Lx, Ly=Ly, Lz=Lz,
                eps="eps",
                transX=b.transX, transY=b.transY, transZ=b.transZ,
            ))
            L_.append("")

    # Surface/Volume constraints: apply to ALL volumes found after Coherence
    L_.append("// Apply surface/volume transfinite + recombine to all volumes")
    L_.append("allVols[] = Unique(Abs(Volume{:}));")
    L_.append("For vi In {0:#allVols[]-1}")
    L_.append("  vtag = allVols[vi];")
    L_.append("  ss[] = Unique(Abs(Boundary{ Volume{vtag}; }));")
    L_.append("  Transfinite Surface {ss[]};")
    L_.append("  Recombine Surface {ss[]};")
    L_.append("  Transfinite Volume {vtag};")
    L_.append("EndFor")

    return "\n".join(L_)


# -----------------------------
# Example usage (edit this only)
# -----------------------------

if __name__ == "__main__":
    # Domain center
    x_center = 0.0
    y_center = 0.0

    # Partitioning in X (columns) and Y (rows)
    x_widths = [3*5, 1*2.68, 2*1.34, 1*0.5, 1*0.335]
    y_widths = [2*2.68, 1*0.5, 1*0.335]

    # Mesh sizes (can refine per column/row)
    XMeshSizes = [5, 2.68, 1.34, 0.5, 0.335]
    YMeshSizes = [2.68, 0.5, 0.335]

    # Z layers (stacked). Each layer has its own ZMeshSize and transZ symbol.
    layers = [
        dict(z_top=0.0,  thickness=5*1.0, ZMeshSize=1.0, transZ="transZ_L1"),
        dict(z_top=-(5*1.0), thickness=4*1.5, ZMeshSize=1.5, transZ="transZ_L2"),
        dict(z_top=-(5*1.0+4*1.5), thickness=5*2.0, ZMeshSize=2.0, transZ="transZ_L3"),
    ]

    # Conformity naming:
    # - transX per column
    # - transY per row
    transX_cols = [f"transX_col{j+1}" for j in range(len(x_widths))]
    transY_rows = [f"transY_row{k+1}" for k in range(len(y_widths))]

    # Build all boxes (all layers)
    all_boxes: list[BoxSpec] = []
    for L in layers:
        all_boxes.extend(
            build_layer_xy(
                xCenter=x_center,
                yCenter=y_center,
                zTop=float(L["z_top"]),
                thickness=float(L["thickness"]),
                xWidths=x_widths,
                yWidths=y_widths,
                XMeshSizes_=XMeshSizes,
                YMeshSizes_=YMeshSizes,
                ZMeshSize=float(L["ZMeshSize"]),
                transXCols=transX_cols,
                transYRows=transY_rows,
                transZ=str(L["transZ"]),
            )
        )

    # Optional symmetry (Option A): mirror pre-Coherence, then mesh robustly
    symmetry = SymmetrySpec(
        enabled=True,
        a=1.0, b=0.0, c=0.0, d=-10.5975,  # x = d (AX + BY + CZ + D = 0)
        volumes="all",
    )

    geo_text = emit_geo(
        all_boxes,
        eps=1e-6,
        symmetry_=symmetry,
    )

    with open("model.geo", "w", encoding="utf-8") as f:
        f.write(geo_text)
