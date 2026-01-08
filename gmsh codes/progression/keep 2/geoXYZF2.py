from __future__ import annotations

from dataclasses import dataclass
# from typing import Iterable


# --------------------------------------------------------------------------------------------------------------------
# Data model
# --------------------------------------------------------------------------------------------------------------------

@dataclass(frozen=True)
class BoxSpec:
    # geometry (centered in x/y, top at z0, thickness downward)
    x0: float
    y0: float
    z0: float
    Lx: float
    Ly: float
    Lz: float

    # mesh sizes (used to compute transfinite counts)
    XMeshSize: float
    YMeshSize: float
    ZMeshSize: float

    # shared transfinite symbol names (for conformity)
    transX: str
    transY: str
    transZ: str


@dataclass(frozen=True)
class SymmetryPlane:
    # plane: a*x + b*y + c*z + d = 0
    a: float
    b: float
    c: float
    d: float


# --------------------------------------------------------------------------------------------------------------------
# Formatting helpers
# --------------------------------------------------------------------------------------------------------------------

def _fmt(x: float) -> str:
    return f"{x:.16g}"


# --------------------------------------------------------------------------------------------------------------------
# Gmsh emission helpers
# --------------------------------------------------------------------------------------------------------------------

def _emit_bbox_curve_constraints(
    tag: str,
    *,
    X0: str, Y0: str, Z0: str,
    Lx: str, Ly: str, Lz: str,
    eps: str,
    transX: str, transY: str, transZ: str,
) -> list[str]:
    """
    Select edges by bounding boxes + apply Transfinite Curve.
    Works after Coherence and is robust to renumbering.
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

    L_.append(f"{cX}[] = Unique(Abs({cX}[]));")
    L_.append(f"{cY}[] = Unique(Abs({cY}[]));")
    L_.append(f"{cZ}[] = Unique(Abs({cZ}[]));")

    L_.append(f"Transfinite Curve {{{cX}[]}} = {transX} Using Progression 1;")
    L_.append(f"Transfinite Curve {{{cY}[]}} = {transY} Using Progression 1;")
    L_.append(f"Transfinite Curve {{{cZ}[]}} = {transZ} Using Progression 1;")

    return L_


def _emit_reflected_center(
    new_tag: str,
    *,
    X_in: str, Y_in: str, Z_in: str,
    a: str, b: str, c: str, d: str,
) -> tuple[str, str, str, list[str]]:
    """
    Symbolic point reflection across plane a*x + b*y + c*z + d = 0.

    p' = p - 2 * (a*x+b*y+c*z+d)/(a^2+b^2+c^2) * (a,b,c)
    """
    denom = f"(({a})*({a}) + ({b})*({b}) + ({c})*({c}))"
    dist = f"(({a})*({X_in}) + ({b})*({Y_in}) + ({c})*({Z_in}) + ({d}))/{denom}"

    X_out = f"X_{new_tag}"
    Y_out = f"Y_{new_tag}"
    Z_out = f"Z_{new_tag}"

    defS = [
        f"{X_out} = ({X_in}) - 2*({dist})*({a});",
        f"{Y_out} = ({Y_in}) - 2*({dist})*({b});",
        f"{Z_out} = ({Z_in}) - 2*({dist})*({c});",
    ]
    return X_out, Y_out, Z_out, defS


# --------------------------------------------------------------------------------------------------------------------
# Partition builder: X–Y grid per layer
# --------------------------------------------------------------------------------------------------------------------

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

    boxes_: list[BoxSpec] = []
    y_cursor = y_min
    for Ly, yms, tY in zip(yWidths, YMeshSizes_, transYRows):
        Ly = float(Ly)
        y0 = y_cursor + Ly / 2.0
        y_cursor += Ly

        x_cursor = x_min
        for Lx, xms, tX in zip(xWidths, XMeshSizes_, transXCols):
            Lx = float(Lx)
            x0 = x_cursor + Lx / 2.0
            x_cursor += Lx

            boxes_.append(
                BoxSpec(
                    x0=x0, y0=y0, z0=zTop,
                    Lx=Lx, Ly=Ly, Lz=thickness,
                    XMeshSize=float(xms),
                    YMeshSize=float(yms),
                    ZMeshSize=float(ZMeshSize),
                    transX=tX, transY=tY, transZ=transZ,
                )
            )
    return boxes_


# --------------------------------------------------------------------------------------------------------------------
# Main emitter with MULTI-symmetry
# --------------------------------------------------------------------------------------------------------------------

def emit_geo(
    boxes_: list[BoxSpec],
    *,
    eps: float = 1e-6,
    symmetries_: list[SymmetryPlane] | None = None,
) -> str:
    """
    Clean .geo that supports sequential symmetries:

      1) Create seed boxes: Box(1...N)
      2) Apply each symmetry in order:
           curVols[] mirrored with Duplicata, then curVols recomputed
      3) Coherence;
      4) Define transfinite counts
      5) Apply curve constraints to ALL symmetry images of each seed box region
      6) Apply surface/volume constraints to ALL volumes discovered post-Coherence
    """
    symmetries_ = symmetries_ or []

    L_: list[str] = []
    L_.append('//')
    L_.append('SetFactory("OpenCASCADE");')
    L_.append(f"eps = {_fmt(eps)};")
    L_.append("")

    # Seed geometry
    for i, b in enumerate(boxes_, start=1):
        L_.append(
            f"Box({i}) = {{{_fmt(b.x0 - b.Lx/2)}, {_fmt(b.y0 - b.Ly/2)}, {_fmt(b.z0 - b.Lz)}, "
            f"{_fmt(b.Lx)}, {_fmt(b.Ly)}, {_fmt(b.Lz)}}};"
        )
    n_seed = len(boxes_)

    # Sequential symmetries (pre-Coherence)
    if symmetries_:
        L_.append("")
        # L_.append(f"curVols[] = Volume{{1:{n_seed}}};")
        L_.append(f"curVols[] = {{1:{n_seed}}};")
        for k, sp in enumerate(symmetries_, start=1):
            L_.append(f"sym_a{k} = {_fmt(sp.a)}; sym_b{k} = {_fmt(sp.b)}; "
                      f"sym_c{k} = {_fmt(sp.c)}; sym_d{k} = {_fmt(sp.d)};")
            L_.append(
                f"dup{k}[] = Symmetry {{sym_a{k}, sym_b{k}, sym_c{k}, sym_d{k}}} "
                f"{{ Duplicata {{ Volume{{curVols[]}}; }} }};"
            )
            # Update the working set for the next symmetry: all volumes currently in the model
            L_.append("curVols[] = Unique(Abs(Volume{:}));")
        L_.append("")

    # Coherence once at the end
    L_.append("Coherence;")
    L_.append("")

    # Define transfinite counts (deduplicate by symbol)
    seen: set[str] = set()
    for b in boxes_:
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

    # Curve constraints for every symmetry image of every seed box
    #
    # We generate centers symbolically in the .geo:
    # start from (X_seed, Y_seed, Z_seed)
    # and for each symmetry plane, reflect all current instances to create new ones.
    for i, b in enumerate(boxes_, start=1):
        # Seed instance tag is "i_0"
        seed_tag = f"{i}_0"
        X_seed = f"X_{seed_tag}"
        Y_seed = f"Y_{seed_tag}"
        Z_seed = f"Z_{seed_tag}"

        L_.append(f"{X_seed} = {_fmt(b.x0)}; {Y_seed} = {_fmt(b.y0)}; {Z_seed} = {_fmt(b.z0)};")
        L_.append(f"Lx_{i} = {_fmt(b.Lx)}; Ly_{i} = {_fmt(b.Ly)}; Lz_{i} = {_fmt(b.Lz)};")

        # Keep a list of instance tags generated so far (in Python), but emit definitions in .geo
        instance_tags: list[str] = [seed_tag]

        # Apply curve constraints for the seed instance
        L_.extend(_emit_bbox_curve_constraints(
            seed_tag,
            X0=X_seed, Y0=Y_seed, Z0=Z_seed,
            Lx=f"Lx_{i}", Ly=f"Ly_{i}", Lz=f"Lz_{i}",
            eps="eps",
            transX=b.transX, transY=b.transY, transZ=b.transZ,
        ))
        L_.append("")

        # Generate all reflected instances symbolically, step by step
        for k in range(1, len(symmetries_) + 1):
            # reflect *all* instances currently in the list, append new ones
            prev = list(instance_tags)
            for t in prev:
                new_tag = f"{t}_S{k}"  # apply symmetry k to instance t
                X_new, Y_new, Z_new, defS = _emit_reflected_center(
                    new_tag,
                    X_in=f"X_{t}", Y_in=f"Y_{t}", Z_in=f"Z_{t}",
                    a=f"sym_a{k}", b=f"sym_b{k}", c=f"sym_c{k}", d=f"sym_d{k}",
                )
                L_.extend(defS)
                L_.extend(_emit_bbox_curve_constraints(
                    new_tag,
                    X0=X_new, Y0=Y_new, Z0=Z_new,
                    Lx=f"Lx_{i}", Ly=f"Ly_{i}", Lz=f"Lz_{i}",
                    eps="eps",
                    transX=b.transX, transY=b.transY, transZ=b.transZ,
                ))
                L_.append("")
                instance_tags.append(new_tag)

    # Surface/volume constraints: apply to ALL volumes after Coherence
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


# --------------------------------------------------------------------------------------------------------------------
# Example usage
# --------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    x_center = 0.0
    y_center = 0.0

    x_widths = [3*5.0, 1*2.68, 2*1.34, 1*0.5, 1*0.335]
    y_widths = [2*2.68, 1*0.5, 1*0.335]

    XMeshSizes = [5.0, 2.68, 1.34, 0.5, 0.335]
    YMeshSizes = [2.68, 0.5, 0.335]

    layers = [
        dict(z_top=0.0,  thickness=5*1.0, ZMeshSize=1.0, transZ="transZ_L1"),
        dict(z_top=-(5*1.0), thickness=4*1.5, ZMeshSize=1.5, transZ="transZ_L2"),
        dict(z_top=-((5*1.0)+(4*1.5)), thickness=5*2.0, ZMeshSize=2.0, transZ="transZ_L3"),
    ]

    transX_cols = [f"transX_col{j+1}" for j in range(len(x_widths))]
    transY_rows = [f"transY_row{k+1}" for k in range(len(y_widths))]

    boxes: list[BoxSpec] = []
    for L in layers:
        boxes.extend(
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

    # MULTI-symmetry example:
    # 1) mirror across x = a  ->  x - a = 0  => (1, 0, 0, a)
    # 2) then mirror the result across y = 0 --> y = 0 ==> (0, 1, 0, 0)
    symmetries = [
        SymmetryPlane(1.0, 0.0, 0.0, -10.5975),
        SymmetryPlane(0.0, 1.0, 0.0, -3.0975),
    ]

    geo = emit_geo(
        boxes,
        eps=1e-6,
        symmetries_=symmetries,
        # symmetries_=[], # in case of no symmetry, for example
    )

    with open("model.geo", "w", encoding="utf-8") as f:
        f.write(geo)
