from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Optional
import math
import pathlib


@dataclass(frozen=True)
class BoxSpec:
    # geometry
    name: str
    x0: float
    y0: float
    z0: float  # top level (ground) of the box
    Lx: float
    Ly: float
    Hz: float  # depth downward (bottom at z0 - Hz)

    # Mesh sizing for transfinite counts
    XMesh: float
    YMesh: float
    ZMesh: float

    # Characteristic length used in Point(..., lc)
    lc: float = 1.0

    # Optional progression factors (keep 1.0 to match your current template)
    progX: float = 1.0
    progY: float = 1.0
    progZ: float = 1.0

    # If True, add Transfinite Surface/Volume + Recombine
    structured_hex: bool = True


def _ceil_div_count(length: float, h: float) -> int:
    """
    returns transfinite point count: ceil(length / h) + 1, with a minimum of 2
    """
    if h <= 0:
        raise ValueError(f"Mesh size must be > 0, got {h}")
    n = int(math.ceil(length / h)) + 1
    return max(n, 2)


def emitBoxGeoF(box: BoxSpec, box_idx: int) -> str:
    """
    Emit one box using your explicit template, with per-entity-type contiguous numbering.

    Numbering convention per box index k:
      Points:        8 per box   -> Point(8k+1 ... 8k+8)
      Lines:        12 per box   -> Line(12k+1 ... 12k+12)
      Curve Loops:   6 per box   -> Curve Loop(6k+1 ... 6k+6)
      Plane Surfs:   6 per box   -> Plane Surface(6k+1 ... 6k+6)
      Surface Loop:  1 per box   -> Surface Loop(k+1)
      Volume:        1 per box   -> Volume(k+1)
    """
    # hx = box.Lx / 2.0
    # hy = box.Ly / 2.0
    # h1z = box.Hz

    # Transfinite counts
    # transX = _ceil_div_count(box.Lx, box.XMesh)
    # transY = _ceil_div_count(box.Ly, box.YMesh)
    # transZ = _ceil_div_count(h1z, box.ZMesh)

    # Per-entity-type offsets
    op = box_idx * 8  # points
    ol = box_idx * 12  # lines
    ocl = box_idx * 6  # curve loops
    os = box_idx * 6  # plane surfaces
    sl1 = box_idx + 1  # surface loop
    v1 = box_idx + 1  # volume

    box_id = box_idx + 1

    # Tags (aliases, like your .geo)
    p1, p2, p3, p4, p5, p6, p7, p8 = (op + i for i in range(1, 9))

    l1, l2, l3, l4 = (ol + i for i in range(1, 5))
    l5, l6, l7, l8 = (ol + i for i in range(5, 9))
    l9, l10, l11, l12 = (ol + i for i in range(9, 13))

    cl1, cl2, cl3, cl4, cl5, cl6 = (ocl + i for i in range(1, 7))
    s1, s2, s3, s4, s5, s6 = (os + i for i in range(1, 7))

    out: List[str] = []

    out += [
        f"// ===================== box{box_id} =====================",
        f"// box_idx = {box_idx} (Point offset={op}, Line offset={ol}, Surface offset={os})",
        "",
        f"x0{box_id} = {box.x0}; y0{box_id} = {box.y0}; z0{box_id} = {box.z0};",
        f"Lx{box_id} = {box.Lx}; Ly{box_id} = {box.Ly}; Hz{box_id} = {box.Hz};",
        f"lc{box_id} = {box.lc};",
        f"XMesh{box_id} = {box.XMesh}; YMesh{box_id} = {box.YMesh}; ZMesh{box_id} = {box.ZMesh};",
        "",
        f"hx{box_id} = Lx{box_id}/2;",
        f"hy{box_id} = Ly{box_id}/2;",
        f"h1z{box_id} = Hz{box_id};",
        "",
        "// Transfinite properties (formulas, editable in .geo)",
        f"transX{box_id} = Ceil(Lx{box_id}/XMesh{box_id}) + 1;",
        f"transY{box_id} = Ceil(Ly{box_id}/YMesh{box_id}) + 1;",
        f"transZ{box_id} = Ceil(Hz{box_id}/ZMesh{box_id}) + 1;",
        f"If (transX{box_id} < 2) transX{box_id} = 2; EndIf",
        f"If (transY{box_id} < 2) transY{box_id} = 2; EndIf",
        f"If (transZ{box_id} < 2) transZ{box_id} = 2; EndIf",
        "",
    ]
    # Points (top at z0, bottom at z0 - h1z)
    out += [
        "// Points",
        f"Point({p1}) = {{x0{box_id} - hx{box_id}, y0{box_id} - hy{box_id}, z0{box_id} - h1z{box_id}, lc{box_id}}};",
        f"Point({p2}) = {{x0{box_id} + hx{box_id}, y0{box_id} - hy{box_id}, z0{box_id} - h1z{box_id}, lc{box_id}}};",
        f"Point({p3}) = {{x0{box_id} + hx{box_id}, y0{box_id} + hy{box_id}, z0{box_id} - h1z{box_id}, lc{box_id}}};",
        f"Point({p4}) = {{x0{box_id} - hx{box_id}, y0{box_id} + hy{box_id}, z0{box_id} - h1z{box_id}, lc{box_id}}};",
        f"Point({p5}) = {{x0{box_id} - hx{box_id}, y0{box_id} - hy{box_id}, z0{box_id}, lc{box_id}}};",
        f"Point({p6}) = {{x0{box_id} + hx{box_id}, y0{box_id} - hy{box_id}, z0{box_id}, lc{box_id}}};",
        f"Point({p7}) = {{x0{box_id} + hx{box_id}, y0{box_id} + hy{box_id}, z0{box_id}, lc{box_id}}};",
        f"Point({p8}) = {{x0{box_id} - hx{box_id}, y0{box_id} + hy{box_id}, z0{box_id}, lc{box_id}}};",
        "",
    ]

    # Lines
    out += [
        "// Lines",
        f"Line({l1}) = {{{p1}, {p5}}};  Line({l2}) = {{{p2}, {p6}}};",
        f"Line({l3}) = {{{p3}, {p7}}};  Line({l4}) = {{{p4}, {p8}}};",
        f"Line({l5}) = {{{p1}, {p2}}};  Line({l6}) = {{{p4}, {p3}}};",
        f"Line({l7}) = {{{p5}, {p6}}};  Line({l8}) = {{{p8}, {p7}}};",
        f"Line({l9}) = {{{p1}, {p4}}};  Line({l10}) = {{{p2}, {p3}}};",
        f"Line({l11}) = {{{p5}, {p8}}}; Line({l12}) = {{{p6}, {p7}}};",
        "",
    ]

    # Plane surfaces (your exact loop definitions)
    out += [
        "// Plane surfaces",
        f"Curve Loop({cl1}) = {{{l9},  {l4},  -{l11}, -{l1}}};",
        f"Plane Surface({s1}) = {{{cl1}}};",

        f"Curve Loop({cl2}) = {{{l5},  {l2},  -{l7},  -{l1}}};",
        f"Plane Surface({s2}) = {{{cl2}}};",

        f"Curve Loop({cl3}) = {{{l10}, {l3},  -{l12}, -{l2}}};",
        f"Plane Surface({s3}) = {{{cl3}}};",

        f"Curve Loop({cl4}) = {{{l6},  {l3},  -{l8},  -{l4}}};",
        f"Plane Surface({s4}) = {{{cl4}}};",

        f"Curve Loop({cl5}) = {{{l5},  {l10}, -{l6},  -{l9}}};",
        f"Plane Surface({s5}) = {{{cl5}}};",

        f"Curve Loop({cl6}) = {{{l7},  {l12}, -{l8},  -{l11}}};",
        f"Plane Surface({s6}) = {{{cl6}}};",
        "",
    ]

    # Volume
    out += [
        "// Volume",
        f"Surface Loop({sl1}) = {{{s6}, {s2}, {s5}, {s3}, {s4}, {s1}}};",
        f"Volume({v1}) = {{{sl1}}};",
        "",
    ]

    # Transfinite constraints (box-specific)
    out += [
        "// Transfinite constraints (box-specific)",
        f"Transfinite Curve {{{l1}:{l4}}} = transZ{box_id} Using Progression {box.progZ};",
        f"Transfinite Curve {{{l5}:{l8}}} = transX{box_id} Using Progression {box.progX};",
        f"Transfinite Curve {{{l9}:{l12}}} = transY{box_id} Using Progression {box.progY};",
    ]

    if box.structured_hex:
        out += [
            f"Transfinite Surface {{{s1}:{s6}}};",
            f"Transfinite Volume {{{v1}}};",
            f"Recombine Surface {{{s1}:{s6}}};",
            # f"Coherence;",
        ]

    out.append("")
    return "\n".join(out)


def write_many_boxes_geo(
        box_specs: Iterable[BoxSpec],
        out_path: str | pathlib.Path,
        header: Optional[str] = None,
) -> pathlib.Path:
    """
    Write a .geo containing many boxes with contiguous tag numbering.

    Each box uses tags o+1...o+12 (max tag touched is o+12), so the next box
    starts at o += 12.
    """
    out_path = pathlib.Path(out_path)

    chunks: List[str] = [
        (header.rstrip() + "\n") if header else
        "// Generated by Python: many boxes, explicit template, per-box mesh.\n"
    ]

    # o = 0
    # BOX_TAG_SPAN = 12

    for box_idx, box in enumerate(box_specs):
        chunks.append(emitBoxGeoF(box, box_idx))

    out_path.write_text("\n".join(chunks), encoding="utf-8")
    return out_path


z0, x0, y0 = 0.0, 0.0, 0.0
Lx, Ly = 12, 40

hA, hB, hC, hD, hE = 6, 6, 8, 10, 5
if __name__ == "__main__":
    boxes = [
        BoxSpec(
            name="boxA",
            x0=x0, y0=y0, z0=z0,
            Lx=Lx, Ly=Ly, Hz=hA,
            XMesh=1.0, YMesh=1.0, ZMesh=1.0,
            lc=1.0,
        ),
        BoxSpec(
            name="boxB",
            x0=x0, y0=y0, z0=-hA,
            Lx=Lx, Ly=Ly, Hz=hB,
            XMesh=1.0, YMesh=1.0, ZMesh=1.5,
            lc=1.0,
        ),
        BoxSpec(
            name="boxC",
            x0=x0, y0=y0, z0=-hA-hB,
            Lx=Lx, Ly=Ly, Hz=hC,
            XMesh=1.0, YMesh=1.0, ZMesh=2.0,
            lc=1.0,
        ),
        BoxSpec(
            name="boxD",
            x0=x0, y0=y0, z0=-hA - hB - hC,
            Lx=Lx, Ly=Ly, Hz=hD,
            XMesh=1.0, YMesh=1.0, ZMesh=2.5,
            lc=1.0,
        ),
        BoxSpec(
            name="boxE",
            x0=x0, y0=y0, z0=-hA - hB - hC - hD,
            Lx=Lx, Ly=Ly, Hz=hE,
            XMesh=1.0, YMesh=1.0, ZMesh=5.0,
            lc=1.0,
        ),
    ]

    path = write_many_boxes_geo(boxes, "many_boxes.geo")
    print(f"Wrote: {path.resolve()}")
