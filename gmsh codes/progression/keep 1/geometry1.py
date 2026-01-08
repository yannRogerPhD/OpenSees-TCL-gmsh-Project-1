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


def multi_box_geo(boxes: list[dict]) -> str:
    lines: list[str] = []
    lines.append("//")
    lines.append('SetFactory("OpenCASCADE");')

    for i, b in enumerate(boxes, start=1):
        # defaults
        XMeshSize = float(b.get("XMeshSize", 1.0))
        YMeshSize = float(b.get("YMeshSize", 1.0))
        ZMeshSize = float(b.get("ZMeshSize", 1.0))
        lTx = float(b.get("lTx", 20.0))
        lTy = float(b.get("lTy", 10.0))
        lTz = float(b.get("lTz", 10.0))
        x0 = float(b.get("x0", 0.0))
        y0 = float(b.get("y0", 0.0))
        z0 = float(b.get("z0", 0.0))

        # unique variable names per box
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

        # Parameters grouped per box
        lines.append("//+")
        lines.append(f'{Xms} = DefineNumber[ {XMeshSize}, Name "Box {i}/Mesh/XMeshSize" ];')
        lines.append("//+")
        lines.append(f'{Yms} = DefineNumber[ {YMeshSize}, Name "Box {i}/Mesh/YMeshSize" ];')
        lines.append("//+")
        lines.append(f'{Zms} = DefineNumber[ {ZMeshSize}, Name "Box {i}/Mesh/ZMeshSize" ];')

        lines.append("//+")
        lines.append(f'{Lx} = DefineNumber[ {lTx}, Name "Box {i}/Geometry/lTx" ];')
        lines.append("//+")
        lines.append(f'{Ly} = DefineNumber[ {lTy}, Name "Box {i}/Geometry/lTy" ];')
        lines.append("//+")
        lines.append(f'{Lz} = DefineNumber[ {lTz}, Name "Box {i}/Geometry/lTz" ];')

        lines.append("//+")
        lines.append(f'{X0} = DefineNumber[ {x0}, Name "Box {i}/Geometry/x0" ];')
        lines.append("//+")
        lines.append(f'{Y0} = DefineNumber[ {y0}, Name "Box {i}/Geometry/y0" ];')
        lines.append("//+")
        lines.append(f'{Z0} = DefineNumber[ {z0}, Name "Box {i}/Geometry/z0" ];')

        # Geometry: centered in x/y, anchored at top in z
        lines.append("//+")
        lines.append(
            f"Box({i}) = {{{X0} - {Lx}/2, {Y0} - {Ly}/2, {Z0} - {Lz}, {Lx}, {Ly}, {Lz}}};"
        )

        # Transfinite counts (computed in .geo)
        lines.append("//+")
        lines.append(f"{tZ} = Ceil({Lz}/{Zms}) + 1;")
        lines.append("//+")
        lines.append(f"{tX} = Ceil({Lx}/{Xms}) + 1;")
        lines.append("//+")
        lines.append(f"{tY} = Ceil({Ly}/{Yms}) + 1;")

        # Transfinite constraints
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


x01, y01, z01 = 0.0, 0.0, 0.0
Lx, Ly, Lz = 20, 10, 10
xM1, yM1, zM1 = 1, 1, 1
if __name__ == "__main__":
    geo = multi_box_geo([
        dict(x0=x01,  y0=y01, z0=z01,  lTx=Lx, lTy=Ly, lTz=Lz, XMeshSize=xM1, YMeshSize=yM1, ZMeshSize=zM1),
        dict(x0=25, y0=0, z0=0,  lTx=10, lTy=10, lTz=5,  XMeshSize=0.5, YMeshSize=1.0, ZMeshSize=0.5),
    ])

    with open("model.geo", "w") as f:
        f.write(geo)
