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


def _reflect_point_across_plane(x: float, y: float, z: float, sp: SymmetryPlane) -> tuple[float, float, float]:
    # p' = p - 2*(a*x+b*y+c*z+d)/(a^2+b^2+c^2) * (a,b,c)
    a, b, c, d = sp.a, sp.b, sp.c, sp.d
    denom = a * a + b * b + c * c
    dist = (a * x + b * y + c * z + d) / denom
    return x - 2 * dist * a, y - 2 * dist * b, z - 2 * dist * c


def _all_instance_centers(
        boxes_: list[BoxSpec],
        symmetries_: list[SymmetryPlane],
) -> list[tuple[float, float, float, BoxSpec]]:
    """
    List all box instances created by sequential symmetries:
    start with seed, then for each symmetry reflect all instances so far (doubling each step).
    Returns tuples (x0,y0,z0, boxspec-of-seed-size).
    """
    inst: list[tuple[float, float, float, BoxSpec]] = [(b.x0, b.y0, b.z0, b) for b in boxes_]
    for sp in symmetries_:
        prev = list(inst)
        for (x, y, z, b) in prev:
            xr, yr, zr = _reflect_point_across_plane(x, y, z, sp)
            inst.append((xr, yr, zr, b))
    return inst


def _global_bounds_with_symmetry(
        boxes_: list[BoxSpec],
        symmetries_: list[SymmetryPlane],
) -> tuple[float, float, float, float, float, float]:
    inst = _all_instance_centers(boxes_, symmetries_)
    xMin = yMin = zMin = float("inf")
    xMax = yMax = zMax = float("-inf")
    for (x0, y0, z0, b) in inst:
        xMin = min(xMin, x0 - b.Lx / 2.0)
        xMax = max(xMax, x0 + b.Lx / 2.0)
        yMin = min(yMin, y0 - b.Ly / 2.0)
        yMax = max(yMax, y0 + b.Ly / 2.0)
        zMin = min(zMin, z0 - b.Lz)  # bottom
        zMax = max(zMax, z0)  # top
    return xMin, xMax, yMin, yMax, zMin, zMax


# --------------------------------------------------------------------------------------------------------------------
# Main emitter with MULTI-symmetry
# --------------------------------------------------------------------------------------------------------------------

def emit_geo(
        boxes_: list[BoxSpec],
        *,
        eps: float = 1e-6,
        symmetries_: list[SymmetryPlane] | None = None,

        # NEW (preferred): one thickness PLUS one layers count for all sides
        abs_thickness: float | None = None,
        abs_layers: int = 1,

        # NEW (preferred): request any of the 17 combos by name, e.g. {"B","BL","BLF"}
        btypes: set[str] | None = None,

        # LEGACY (still supported for now)
        abs_bottom_thickness: float | None = None,
        abs_bottom_layers: int = 1,
        abs_left_thickness: float | None = None,
        abs_left_layers: int = 1,
        abs_right_thickness: float | None = None,
        abs_right_layers: int = 1,
        abs_front_thickness: float | None = None,
        abs_front_layers: int = 1,
        abs_back_thickness: float | None = None,
        abs_back_layers: int = 1,

        # LEGACY flags (still supported for now)
        abs_bl: bool = False,
        abs_br: bool = False,
        abs_bf: bool = False,
        abs_bk: bool = False,
        abs_lf: bool = False,
        abs_lk: bool = False,
        abs_rf: bool = False,
        abs_rk: bool = False,
        abs_blf: bool = False,
        abs_blk: bool = False,
        abs_brf: bool = False,
        abs_brk: bool = False,
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
            f"Box({i}) = {{{_fmt(b.x0 - b.Lx / 2)}, {_fmt(b.y0 - b.Ly / 2)}, {_fmt(b.z0 - b.Lz)}, "
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
    xmin, xmax, ymin, ymax, zmin, zmax = _global_bounds_with_symmetry(boxes_, symmetries_)
    L_.append(f"XMIN_SOIL = {_fmt(xmin)}; XMAX_SOIL = {_fmt(xmax)};")
    L_.append(f"YMIN_SOIL = {_fmt(ymin)}; YMAX_SOIL = {_fmt(ymax)};")
    L_.append(f"ZMIN_SOIL = {_fmt(zmin)}; ZMAX_SOIL = {_fmt(zmax)};")
    L_.append("")

    # ---------------------------------------------------------------------------------------------------
    # Absorbing boundary selection (NEW)
    # ---------------------------------------------------------------------------------------------------
    btypes = set(btypes or [])

    def _on(tag: str, legacy_bool: bool) -> bool:
        # New interface: btypes contains the tag (e.g. "B", "BLF", ...)
        # Legacy interface: old booleans still work
        return (tag in btypes) or legacy_bool

    # single faces
    useB = _on("B", abs_bottom_thickness is not None and abs_bottom_thickness > 0.0)
    useL = _on("L", abs_left_thickness is not None and abs_left_thickness > 0.0)
    useR = _on("R", abs_right_thickness is not None and abs_right_thickness > 0.0)
    useF = _on("F", abs_front_thickness is not None and abs_front_thickness > 0.0)
    useK = _on("K", abs_back_thickness is not None and abs_back_thickness > 0.0)

    # edges
    useBL = _on("BL", abs_bl)
    useBR = _on("BR", abs_br)
    useBF = _on("BF", abs_bf)
    useBK = _on("BK", abs_bk)
    useLF = _on("LF", abs_lf)
    useLK = _on("LK", abs_lk)
    useRF = _on("RF", abs_rf)
    useRK = _on("RK", abs_rk)

    # corners
    useBLF = _on("BLF", abs_blf)
    useBLK = _on("BLK", abs_blk)
    useBRF = _on("BRF", abs_brf)
    useBRK = _on("BRK", abs_brk)

    # If an edge/corner is requested, force its prerequisite parent(s)
    if useBL or useBR or useBF or useBK:
        useB = True
    if useLF or useLK:
        useL = True
    if useRF or useRK:
        useR = True
    if useBF or useLF or useRF or useBLF or useBRF:
        useF = True
    if useBK or useLK or useRK or useBLK or useBRK:
        useK = True
    if useBLF or useBLK:
        useBL = True
        useB = True
    if useBRF or useBRK:
        useBR = True
        useB = True

    # ---------------------------------------------------------------------------------------------------
    # Absorbing thickness/layers emitted ONCE (common thickness preferred)
    # ---------------------------------------------------------------------------------------------------
    if abs_thickness is not None:
        tB = tL = tR = tF = tK = float(abs_thickness)
        nB = nL = nR = nF = nK = int(abs_layers)

        # Make all thickness symbols available for any requested combo
        L_.append(f"tAbsB = {_fmt(tB)}; nAbsB = {nB};")
        L_.append(f"tAbsL = {_fmt(tL)}; nAbsL = {nL};")
        L_.append(f"tAbsR = {_fmt(tR)}; nAbsR = {nR};")
        L_.append(f"tAbsF = {_fmt(tF)}; nAbsF = {nF};")
        L_.append(f"tAbsK = {_fmt(tK)}; nAbsK = {nK};")
    else:
        # Legacy fallback (only emit what is actually enabled)
        if useB:
            L_.append(f"tAbsB = {_fmt(float(abs_bottom_thickness or 0.0))}; nAbsB = {int(abs_bottom_layers)};")
        if useL:
            L_.append(f"tAbsL = {_fmt(float(abs_left_thickness or 0.0))}; nAbsL = {int(abs_left_layers)};")
        if useR:
            L_.append(f"tAbsR = {_fmt(float(abs_right_thickness or 0.0))}; nAbsR = {int(abs_right_layers)};")
        if useF:
            L_.append(f"tAbsF = {_fmt(float(abs_front_thickness or 0.0))}; nAbsF = {int(abs_front_layers)};")
        if useK:
            L_.append(f"tAbsK = {_fmt(float(abs_back_thickness or 0.0))}; nAbsK = {int(abs_back_layers)};")

    L_.append("")

    # ---------------------------------------------------------------------------------------------------------------
    # ABSORBING LAYER: BOTTOM
    # ---------------------------------------------------------------------------------------------------------------
    if useB:
        L_.append("")
        L_.append("// bottom boundary faces: z = ZMIN_SOIL (within eps)")
        L_.append("sBottom[] = Surface In BoundingBox {"
                  "XMIN_SOIL-eps, YMIN_SOIL-eps, ZMIN_SOIL-eps, "
                  "XMAX_SOIL+eps, YMAX_SOIL+eps, ZMIN_SOIL+eps};")
        L_.append("sBottom[] = Unique(Abs(sBottom[]));")
        L_.append("")
        L_.append("// Extrude outward along -Z (Bottom)")
        L_.append("If (#sBottom[] > 0)")
        L_.append("  Extrude {0, 0, -tAbsB} {")
        L_.append("    Surface{sBottom[]}; Layers{nAbsB}; Recombine;")
        L_.append("  }")
        L_.append("EndIf")
        L_.append("")

    # ---------------------------------------------------------------------------------------------------------------
    # ABSORBING LAYER: LEFT
    # ---------------------------------------------------------------------------------------------------------------
    if useL:
        L_.append("")
        L_.append("// left boundary faces: x = XMIN_SOIL (within eps)")
        L_.append("sLeft[] = Surface In BoundingBox {"
                  "XMIN_SOIL-eps, YMIN_SOIL-eps, ZMIN_SOIL-eps, "
                  "XMIN_SOIL+eps, YMAX_SOIL+eps, ZMAX_SOIL+eps};")
        L_.append("sLeft[] = Unique(Abs(sLeft[]));")
        L_.append("")
        L_.append("// Extrude outward along -X (Left)")
        L_.append("If (#sLeft[] > 0)")
        L_.append("  Extrude {-tAbsL, 0, 0} {")
        L_.append("    Surface{sLeft[]}; Layers{nAbsL}; Recombine;")
        L_.append("  }")
        L_.append("EndIf")
        L_.append("")

    # ---------------------------------------------------------------------------------------------------------------
    # ABSORBING LAYER: RIGHT
    # ---------------------------------------------------------------------------------------------------------------
    if useR:
        L_.append("")
        L_.append("// right boundary faces: x = XMAX_SOIL (within eps)")
        L_.append("sRight[] = Surface In BoundingBox {"
                  "XMAX_SOIL-eps, YMIN_SOIL-eps, ZMIN_SOIL-eps, "
                  "XMAX_SOIL+eps, YMAX_SOIL+eps, ZMAX_SOIL+eps};")
        L_.append("sRight[] = Unique(Abs(sRight[]));")
        L_.append("")
        L_.append("// Extrude outward along +X (Right)")
        L_.append("If (#sRight[] > 0)")
        L_.append("  Extrude {tAbsR, 0, 0} {")
        L_.append("    Surface{sRight[]}; Layers{nAbsR}; Recombine;")
        L_.append("  }")
        L_.append("EndIf")
        L_.append("")

    # ---------------------------------------------------------------------------------------------------------------
    # ABSORBING LAYER: FRONT
    # ---------------------------------------------------------------------------------------------------------------
    if useF:
        L_.append("")
        L_.append("// front boundary faces: y = YMIN_SOIL (within eps)")
        L_.append("sFront[] = Surface In BoundingBox {"
                  "XMIN_SOIL-eps, YMIN_SOIL-eps, ZMIN_SOIL-eps, "
                  "XMAX_SOIL+eps, YMIN_SOIL+eps, ZMAX_SOIL+eps};")
        L_.append("sFront[] = Unique(Abs(sFront[]));")
        L_.append("")
        L_.append("// Extrude outward along -Y (Front)")
        L_.append("If (#sFront[] > 0)")
        L_.append("  Extrude {0, -tAbsF, 0} {")
        L_.append("    Surface{sFront[]}; Layers{nAbsF}; Recombine;")
        L_.append("  }")
        L_.append("EndIf")
        L_.append("")

    # ---------------------------------------------------------------------------------------------------------------
    # ABSORBING LAYER: BACK (K)
    # ---------------------------------------------------------------------------------------------------------------
    if useK:
        L_.append("")
        L_.append("// back boundary faces: y = YMAX_SOIL (within eps)")
        L_.append("sBack[] = Surface In BoundingBox {"
                  "XMIN_SOIL-eps, YMAX_SOIL-eps, ZMIN_SOIL-eps, "
                  "XMAX_SOIL+eps, YMAX_SOIL+eps, ZMAX_SOIL+eps};")
        L_.append("sBack[] = Unique(Abs(sBack[]));")
        L_.append("")
        L_.append("// Extrude outward along +Y (Back)")
        L_.append("If (#sBack[] > 0)")
        L_.append("  Extrude {0, tAbsK, 0} {")
        L_.append("    Surface{sBack[]}; Layers{nAbsK}; Recombine;")
        L_.append("  }")
        L_.append("EndIf")
        L_.append("")

    # ---------------------------------------------------------------------------------
    # ABSORBING LAYER COMBINATIONS (btypes-driven)
    # Order: BL, BR, BF, BK, LF, LK, RF, RK, BLF, BLK, BRF, BRK
    # ---------------------------------------------------------------------------------

    # BL: from B-layer left face --> extrude -X
    if useBL and useB:
        L_.append("// BL: take the left vertical face of the B layer and extrude it along -X")
        L_.append("sBL_fromB[] = Surface In BoundingBox {"
                  "XMIN_SOIL-eps, YMIN_SOIL-eps, (ZMIN_SOIL - tAbsB)-eps, "
                  "XMIN_SOIL+eps, YMAX_SOIL+eps,  ZMIN_SOIL+eps};")
        L_.append("sBL_fromB[] = Unique(Abs(sBL_fromB[]));")
        L_.append("")
        L_.append("If (#sBL_fromB[] > 0)")
        L_.append("  Extrude {-tAbsL, 0, 0} {")
        L_.append("    Surface{sBL_fromB[]}; Layers{nAbsL}; Recombine;")
        L_.append("  }")
        L_.append("EndIf")
        L_.append("")

    # BR: from B-layer right face --> extrude +X
    if useBR and useB:
        L_.append("// BR: take the right vertical face of the B layer and extrude it along +X")
        L_.append("sBR_fromB[] = Surface In BoundingBox {"
                  "XMAX_SOIL-eps, YMIN_SOIL-eps, (ZMIN_SOIL - tAbsB)-eps, "
                  "XMAX_SOIL+eps, YMAX_SOIL+eps,  ZMIN_SOIL+eps};")
        L_.append("sBR_fromB[] = Unique(Abs(sBR_fromB[]));")
        L_.append("")
        L_.append("If (#sBR_fromB[] > 0)")
        L_.append("  Extrude {tAbsR, 0, 0} {")
        L_.append("    Surface{sBR_fromB[]}; Layers{nAbsR}; Recombine;")
        L_.append("  }")
        L_.append("EndIf")
        L_.append("")

    # BF: from B-layer front face --> extrude -Y
    if useBF and useB:
        L_.append("// BF: take the front vertical face of the B layer and extrude it along -Y")
        L_.append("sBF_fromB[] = Surface In BoundingBox {"
                  "XMIN_SOIL-eps, YMIN_SOIL-eps, (ZMIN_SOIL - tAbsB)-eps, "
                  "XMAX_SOIL+eps, YMIN_SOIL+eps,  ZMIN_SOIL+eps};")
        L_.append("sBF_fromB[] = Unique(Abs(sBF_fromB[]));")
        L_.append("")
        L_.append("If (#sBF_fromB[] > 0)")
        L_.append("  Extrude {0, -tAbsF, 0} {")
        L_.append("    Surface{sBF_fromB[]}; Layers{nAbsF}; Recombine;")
        L_.append("  }")
        L_.append("EndIf")
        L_.append("")

    # BK: from B-layer back face --> extrude +Y
    if useBK and useB:
        L_.append("// BK: take the back vertical face of the B layer and extrude it along +Y")
        L_.append("sBK_fromB[] = Surface In BoundingBox {"
                  "XMIN_SOIL-eps, YMAX_SOIL-eps, (ZMIN_SOIL - tAbsB)-eps, "
                  "XMAX_SOIL+eps, YMAX_SOIL+eps,  ZMIN_SOIL+eps};")
        L_.append("sBK_fromB[] = Unique(Abs(sBK_fromB[]));")
        L_.append("")
        L_.append("If (#sBK_fromB[] > 0)")
        L_.append("  Extrude {0, tAbsK, 0} {")
        L_.append("    Surface{sBK_fromB[]}; Layers{nAbsK}; Recombine;")
        L_.append("  }")
        L_.append("EndIf")
        L_.append("")

    # LF: from L-layer front face --> extrude -Y
    if useLF and useL:
        L_.append("// LF: take the front face of the L layer and extrude it along -Y")
        L_.append("sLF_fromL[] = Surface In BoundingBox {"
                  "(XMIN_SOIL - tAbsL)-eps, YMIN_SOIL-eps, ZMIN_SOIL-eps, "
                  "XMIN_SOIL+eps,          YMIN_SOIL+eps, ZMAX_SOIL+eps};")
        L_.append("sLF_fromL[] = Unique(Abs(sLF_fromL[]));")
        L_.append("")
        L_.append("If (#sLF_fromL[] > 0)")
        L_.append("  Extrude {0, -tAbsF, 0} {")
        L_.append("    Surface{sLF_fromL[]}; Layers{nAbsF}; Recombine;")
        L_.append("  }")
        L_.append("EndIf")
        L_.append("")

    # LK: from L-layer back face --> extrude +Y
    if useLK and useL:
        L_.append("// LK: take the back face of the L layer and extrude it along +Y")
        L_.append("sLK_fromL[] = Surface In BoundingBox {"
                  "(XMIN_SOIL - tAbsL)-eps, YMAX_SOIL-eps, ZMIN_SOIL-eps, "
                  "XMIN_SOIL+eps,          YMAX_SOIL+eps, ZMAX_SOIL+eps};")
        L_.append("sLK_fromL[] = Unique(Abs(sLK_fromL[]));")
        L_.append("")
        L_.append("If (#sLK_fromL[] > 0)")
        L_.append("  Extrude {0, tAbsK, 0} {")
        L_.append("    Surface{sLK_fromL[]}; Layers{nAbsK}; Recombine;")
        L_.append("  }")
        L_.append("EndIf")
        L_.append("")

    # RF: from R-layer front face --> extrude -Y
    if useRF and useR:
        L_.append("// RF: take the front face of the R layer and extrude it along -Y")
        L_.append("sRF_fromR[] = Surface In BoundingBox {"
                  "XMAX_SOIL-eps,            YMIN_SOIL-eps, ZMIN_SOIL-eps, "
                  "(XMAX_SOIL + tAbsR)+eps,  YMIN_SOIL+eps, ZMAX_SOIL+eps};")
        L_.append("sRF_fromR[] = Unique(Abs(sRF_fromR[]));")
        L_.append("")
        L_.append("If (#sRF_fromR[] > 0)")
        L_.append("  Extrude {0, -tAbsF, 0} {")
        L_.append("    Surface{sRF_fromR[]}; Layers{nAbsF}; Recombine;")
        L_.append("  }")
        L_.append("EndIf")
        L_.append("")

    # RK: from R-layer back face --> extrude +Y
    if useRK and useR:
        L_.append("// RK: take the back face of the R layer and extrude it along +Y")
        L_.append("sRK_fromR[] = Surface In BoundingBox {"
                  "XMAX_SOIL-eps,            YMAX_SOIL-eps, ZMIN_SOIL-eps, "
                  "(XMAX_SOIL + tAbsR)+eps,  YMAX_SOIL+eps, ZMAX_SOIL+eps};")
        L_.append("sRK_fromR[] = Unique(Abs(sRK_fromR[]));")
        L_.append("")
        L_.append("If (#sRK_fromR[] > 0)")
        L_.append("  Extrude {0, tAbsK, 0} {")
        L_.append("    Surface{sRK_fromR[]}; Layers{nAbsK}; Recombine;")
        L_.append("  }")
        L_.append("EndIf")
        L_.append("")

    # BLF: from BL prism front face --> extrude -Y
    if useBLF and useBL:
        L_.append("// BLF: take the front face of the BL prism and extrude it along -Y")
        L_.append("sBLF_fromBL[] = Surface In BoundingBox {"
                  "(XMIN_SOIL - tAbsL)-eps, YMIN_SOIL-eps, (ZMIN_SOIL - tAbsB)-eps, "
                  "XMIN_SOIL+eps,          YMIN_SOIL+eps,  ZMIN_SOIL+eps};")
        L_.append("sBLF_fromBL[] = Unique(Abs(sBLF_fromBL[]));")
        L_.append("")
        L_.append("If (#sBLF_fromBL[] > 0)")
        L_.append("  Extrude {0, -tAbsF, 0} {")
        L_.append("    Surface{sBLF_fromBL[]}; Layers{nAbsF}; Recombine;")
        L_.append("  }")
        L_.append("EndIf")
        L_.append("")

    # BLK: from BL prism back face --> extrude +Y
    if useBLK and useBL:
        L_.append("// BLK: take the back face of the BL prism and extrude it along +Y")
        L_.append("sBLK_fromBL[] = Surface In BoundingBox {"
                  "(XMIN_SOIL - tAbsL)-eps, YMAX_SOIL-eps, (ZMIN_SOIL - tAbsB)-eps, "
                  "XMIN_SOIL+eps,          YMAX_SOIL+eps,  ZMIN_SOIL+eps};")
        L_.append("sBLK_fromBL[] = Unique(Abs(sBLK_fromBL[]));")
        L_.append("")
        L_.append("If (#sBLK_fromBL[] > 0)")
        L_.append("  Extrude {0, tAbsK, 0} {")
        L_.append("    Surface{sBLK_fromBL[]}; Layers{nAbsK}; Recombine;")
        L_.append("  }")
        L_.append("EndIf")
        L_.append("")

    # BRF: from BR prism front face --> extrude -Y
    if useBRF and useBR:
        L_.append("// BRF: take the front face of the BR prism and extrude it along -Y")
        L_.append("sBRF_fromBR[] = Surface In BoundingBox {"
                  "XMAX_SOIL-eps,           YMIN_SOIL-eps, (ZMIN_SOIL - tAbsB)-eps, "
                  "(XMAX_SOIL + tAbsR)+eps, YMIN_SOIL+eps,  ZMIN_SOIL+eps};")
        L_.append("sBRF_fromBR[] = Unique(Abs(sBRF_fromBR[]));")
        L_.append("")
        L_.append("If (#sBRF_fromBR[] > 0)")
        L_.append("  Extrude {0, -tAbsF, 0} {")
        L_.append("    Surface{sBRF_fromBR[]}; Layers{nAbsF}; Recombine;")
        L_.append("  }")
        L_.append("EndIf")
        L_.append("")

    # BRK: from BR prism back face --> extrude +Y
    if useBRK and useBR:
        L_.append("// BRK: take the back face of the BR prism and extrude it along +Y")
        L_.append("sBRK_fromBR[] = Surface In BoundingBox {"
                  "XMAX_SOIL-eps,           YMAX_SOIL-eps, (ZMIN_SOIL - tAbsB)-eps, "
                  "(XMAX_SOIL + tAbsR)+eps, YMAX_SOIL+eps,  ZMIN_SOIL+eps};")
        L_.append("sBRK_fromBR[] = Unique(Abs(sBRK_fromBR[]));")
        L_.append("")
        L_.append("If (#sBRK_fromBR[] > 0)")
        L_.append("  Extrude {0, tAbsK, 0} {")
        L_.append("    Surface{sBRK_fromBR[]}; Layers{nAbsK}; Recombine;")
        L_.append("  }")
        L_.append("EndIf")
        L_.append("")

    # second Coherence after absorbing layers
    L_.append("")
    L_.append("// Coherence after absorbing layers")
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

    x_widths = [260 / 5, 260 / 5, 260 / 5, 260 / 5, 260 / 5]
    y_widths = [260 / 5, 260 / 5, 260 / 5, 260 / 5, 260 / 5]

    XMeshSizes = [260 / 5, 260 / 5, 260 / 5, 260 / 5, 260 / 5]
    YMeshSizes = [260 / 5, 260 / 5, 260 / 5, 260 / 5, 260 / 5]

    # x_widths = [260 / 5, 260 / 5, 260 / 5]
    # y_widths = [260 / 5, 260 / 5, 260 / 5]
    #
    # XMeshSizes = [260 / 5, 260 / 5, 260 / 5]
    # YMeshSizes = [260 / 5, 260 / 5, 260 / 5]

    layers = [
        dict(z_top=0.0, thickness=20, ZMeshSize=1.25, transZ="transZ_L1"),  # 1.25
        dict(z_top=-20, thickness=30, ZMeshSize=1.25, transZ="transZ_L2"),  # 1.5
        dict(z_top=-50, thickness=40, ZMeshSize=1.25, transZ="transZ_L3"),  # 1.25
        dict(z_top=-90, thickness=50, ZMeshSize=1.25, transZ="transZ_L4"),  # 1.25
    ]

    transX_cols = [f"transX_col{j + 1}" for j in range(len(x_widths))]
    transY_rows = [f"transY_row{k + 1}" for k in range(len(y_widths))]

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
        # SymmetryPlane(1.0, 0.0, 0.0, -10.5975),
        # SymmetryPlane(0.0, 1.0, 0.0, -3.0975),
        # SymmetryPlane(1.0, 0.0, 0.0, -130),
    ]

    # order = ["B", "L", "R", "F", "K", "BL", "BR", "BF", "BK", "LF", "LK", "RF", "RK", "BLF", "BLK", "BRF", "BRK"]
    order = ["B", "L", "R", "F", "K", "BL", "BR", "BF", "BK", "LF", "LK", "RF", "RK", "BLF", "BLK", "BRF", "BRK"]
    # order = []
    geo = emit_geo(
        boxes,
        eps=1e-6,
        symmetries_=symmetries,
        abs_thickness=20.0,
        abs_layers=1,
        btypes=set(order),
    )

    with open("model.geo", "w", encoding="utf-8") as f:
        f.write(geo)
