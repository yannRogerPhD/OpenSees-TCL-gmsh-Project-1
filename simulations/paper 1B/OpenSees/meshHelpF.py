import os
import numpy as np


def outputFolder(meshFilE):
    baseName = os.path.splitext(os.path.basename(meshFilE))[0]
    outPutFolder = os.path.join("TCL-Files", baseName)
    os.makedirs(outPutFolder, exist_ok=True)
    return outPutFolder


defaultTol = 1e-6


# --------------------------------------------------------------------------------------------------------------
# Node sorting helpers
# --------------------------------------------------------------------------------------------------------------
def sortNodesByX(nodes, nodeCoords):
    # return nodes sorted by their x-coordinate
    return sorted(nodes, key=lambda n: nodeCoords[n][0])


def sortNodesByY(nodes, nodeCoords):
    # return nodes sorted by their y-coordinate
    return sorted(nodes, key=lambda n: nodeCoords[n][1])


def sortNodesByZ(nodes, nodeCoords):
    # return nodes sorted by their z-coordinate (for 3D)
    return sorted(nodes, key=lambda n: nodeCoords[n][2])


# inside meshHelpF.py
def filterElementsByDIM(elements, beam2DGrp, beam3DGrp):
    gmsh3DTypes = {
        5, 17
    }
    other3DDerivatives = {
        105, 1005, 1055, 10051, 10052, 10053, 10054, 10055, 10056, 10057, 10058,
        10059, 10060, 10061, 10062, 10063, 10064, 10065, 10066, 10067
    }

    gmsh2DTypes = {
        1, 3, 10
    }
    other2DDerivatives = {
        103, 1003, 10031, 10032, 10033, 10034, 10035
    }

    # Correct: use union ("|"), NOT 'or'
    has3D = any(el["type"] in (gmsh3DTypes | other3DDerivatives) for el in elements)

    if has3D:
        filtered = \
            [
                el for el in elements
                if el["type"] in (gmsh3DTypes | other3DDerivatives)
                or (el["type"] == 1 and (el["group"] in beam2DGrp or el["group"] in beam3DGrp))
            ]
        print("Detected 3D mesh --> ignoring surface elements (type 3)...")

    else:
        filtered = \
            [
                el for el in elements
                if el["type"] in (gmsh2DTypes | other2DDerivatives)
                and (el["type"] != 1 or el["group"] in beam2DGrp)
            ]
        print("Detected 2D mesh --> keeping quads and beam line groups only...")

    return filtered, has3D


# inside meshHelpF.py
def remapElementTypes(elements, groupSets):
    """
    Applies type remapping rules to elements based on their physical group.
    groupSets: dict of named sets like bbarQuadUPGrp, quadUPGrp, etc.
    """
    for el in elements:
        t, g = el["type"], el["group"]

        # Beam remapping
        if t == 1:
            if g in groupSets.get("dispBeam2DGrp", set()):
                el["type"] = 201
            elif g in groupSets.get("dispBeam3DGrp", set()):
                el["type"] = 202
            elif g in groupSets["beam2DGrp"]:
                el["type"] = 1
            elif g in groupSets["beam3DGrp"]:
                el["type"] = 101
            else:
                continue

        # 2D types
        elif t == 3:
            mapping2D = {
                "bbarQuadUPGrp": 103,
                "quadUPGrp": 1003,
                "ASDLeftGrp": 10031,
                "ASDBottomGrp": 10032,
                "ASDRightGrp": 10033,
                "ASDBottomLeftGrp": 10034,
                "ASDBottomRightGrp": 10035,
            }
            for name, newType in mapping2D.items():
                if g in groupSets.get(name, set()):
                    el["type"] = newType
                    break

        # 3D types
        elif t == 5:
            mapping3D = {
                "bbarBrickUPGrp": 105,
                "sspBrickUPGrp": 1005,
                "sspBrickGrp": 1055,
                "ASD3DLGrp": 10051, "ASD3DRGrp": 10052, "ASD3DKGrp": 10053, "ASD3DFGrp": 10054,
                "ASD3DBLGrp": 10055, "ASD3DBRGrp": 10056, "ASD3DBKGrp": 10057, "ASD3DBFGrp": 10058,
                "ASD3DLKGrp": 10059, "ASD3DBLKGrp": 10060, "ASD3DRKGrp": 10061, "ASD3DBRKGrp": 10062,
                "ASD3DLFGrp": 10063, "ASD3DBLFGrp": 10064, "ASD3DRFGrp": 10065, "ASD3DBRFGrp": 10066,
                "ASD3DBGrp": 10067,
            }
            for name, newType in mapping3D.items():
                if g in groupSets.get(name, set()):
                    el["type"] = newType
                    break
    return elements


# compact summary of the remapping (2D + 3D)
def summarizeRemaps(elements):
    total = len(elements)
    if total == 0:
        print("No elements to summarize.")
        return

    counts = {}
    for el in elements:
        t = el["type"]
        counts[t] = counts.get(t, 0) + 1

    labels = {
        # 1D beams
        1: "elasticBeamColumn2D",
        101: "elasticBeamColumn3D",
        201: "displacementBeam2D",
        202: "displacementBeam3D",

        # 2D elements
        3: "quad (plain 2D)",
        10: "plane element (generic)",
        103: "bbarQuadUP",
        1003: "quadUP",
        10031: "ASD Left",
        10032: "ASD Bottom",
        10033: "ASD Right",
        10034: "ASD Bottom-Left",
        10035: "ASD Bottom-Right",

        # 3D elements
        5: "brick (plain 3D)",
        105: "bbarBrickUP",
        1005: "SSPbrickUP",
        1055: "SSPbrick",
        10051: "ASD3DL",
        10052: "ASD3DR",
        10053: "ASD3DK",
        10054: "ASD3DF",
        10055: "ASD3DBL",
        10056: "ASD3DBR",
        10057: "ASD3DBK",
        10058: "ASD3DBF",
        10059: "ASD3DLK",
        10060: "ASD3DBLK",
        10061: "ASD3DRK",
        10062: "ASD3DBRK",
        10063: "ASD3DLF",
        10064: "ASD3DBLF",
        10065: "ASD3DRF",
        10066: "ASD3DBRF",
        10067: "ASD3DB",
    }

    print(f"\nSummary of element remaps ({total} total):")
    for t, label in labels.items():
        if t in counts:
            pct = (counts[t] / total) * 100
            print(f"  {counts[t]:6d} --> {label:25s} ({t:6d})   [{pct:6.2f}%]")

    # (NEW): total percentage check
    total_pct = sum((counts[t] / total) * 100 for t in counts)
    print(f"Total percentage = {total_pct:.2f}%")

    # (optional): report any unexpected type numbers
    known = set(labels)
    leftovers = {t: c for t, c in counts.items() if t not in known}
    if leftovers:
        print("\n[Info] Unrecognized or extra types detected:")
        for t, c in leftovers.items():
            pct = (c / total) * 100
            print(f"  {c:6d} elements of type {t:6d}   [{pct:6.2f}%]")


def detect_ndm_ndf(elements, elementProfiles_):
    """
    Determine ndmGlobal and ndfGlobal based on active element types.
    """
    usedProfiles = {el["type"] for el in elements if el["type"] in elementProfiles_}
    print()
    print("usedProfiles:", usedProfiles)

    if not usedProfiles:
        return 2, 2  # default if nothing is mapped

    ndmGlobal = max(elementProfiles_[t]["ndm"] for t in usedProfiles)
    hasUP = any(elementProfiles_[t]["needsP"] for t in usedProfiles)
    hasBeam2D = any(elementProfiles_[t]["key"] == "elasticBeamColumn2D" for t in usedProfiles)
    hasBeam3D = any(elementProfiles_[t]["key"] == "elasticBeamColumn3D" for t in usedProfiles)

    if ndmGlobal == 2:
        if hasBeam2D or hasUP:
            ndfGlobal = 3
        else:
            ndfGlobal = 2
    elif ndmGlobal == 3:
        if hasBeam3D:
            ndfGlobal = 6
        elif hasUP:
            ndfGlobal = 4
        else:
            ndfGlobal = 3
    else:
        ndmGlobal, ndfGlobal = 2, 2

    return ndmGlobal, ndfGlobal


def classifyNodeDOFs(elements, elementProfiles_, beam2DGrp, beam3DGrp):
    """
    Build dictionaries of DOFs for soil and structure nodes.
    Returns: nodeDOFs_soil, nodeDOFs_struct, nodeDOFs
    """
    nodeDOFs_soil = {}
    nodeDOFs_struct = {}

    for el in elements:
        eType = el["type"]
        if eType not in elementProfiles_:
            continue

        ruleFunc = elementProfiles_[eType]["dofRule"]
        dofMap = ruleFunc(el["nodes"])

        # classify as structure or soil by group membership
        if eType in (1, 101, 201, 202) or el["group"] in beam2DGrp or el["group"] in beam3DGrp:
            target = nodeDOFs_struct
        else:
            target = nodeDOFs_soil

        for nodeTag, dofCount in dofMap.items():
            if nodeTag not in target or dofCount > target[nodeTag]:
                target[nodeTag] = dofCount

    nodeDOFs = {**nodeDOFs_soil, **nodeDOFs_struct}
    return nodeDOFs_soil, nodeDOFs_struct, nodeDOFs


def _axis_pair_indices(vertical_axis: int):
    """
    For a chosen vertical axis (0=x,1=y,2=z), returns the two in-plane axis indices.
    Example: vertical_axis=2 (z up) --> in-plane axes are x(0), y(1).
    """
    axes = [0, 1, 2]
    axes.remove(vertical_axis)
    return axes[0], axes[1]


def _get_coord(node_id, nodeCoords):
    if nodeCoords is None:
        raise ValueError("nodeCoords is required for coordinate-based hex reordering.")

    assert nodeCoords is not None

    if isinstance(nodeCoords, dict):
        coords = nodeCoords.get(node_id)
        if coords is None:
            raise KeyError(f"Node id {node_id} not found in nodeCoords.")
        return coords

    # list/tuple-like
    return nodeCoords[node_id]


def classify_hex8_nodes(nodeList, nodeCoords, vertical_axis: int = 2, tol: float = 1e-9):
    """
    Reorders an 8-node hex to match the provided diagram convention:

    Bottom face (min vertical):
      1: (max a min b)
      2: (max a max b)
      3: (min a max b)
      4: (min a min b)

    Top face (max vertical), directly above:
      5 above 1, 6 above 2, 7 above 3, 8 above 4.

    where (a,b) are the two axes orthogonal to vertical_axis.
    """
    if len(nodeList) != 8:
        raise ValueError(f"Expected 8 nodes for Hex8, got {len(nodeList)}")

    a_axis, b_axis = _axis_pair_indices(vertical_axis)

    # Collect (node_id, coords)
    pts = []
    for nid in nodeList:
        x, y, z = _get_coord(nid, nodeCoords)
        pts.append((nid, (x, y, z)))

    # Split into bottom/top by vertical coordinate
    v_vals = [p[1][vertical_axis] for p in pts]
    v_min = min(v_vals)
    v_max = max(v_vals)

    bottom = [p for p in pts if abs(p[1][vertical_axis] - v_min) <= tol]
    top = [p for p in pts if abs(p[1][vertical_axis] - v_max) <= tol]

    # If tolerance is too strict, fall back to sorting by vertical coordinate
    if len(bottom) != 4 or len(top) != 4:
        pts_sorted = sorted(pts, key=lambda p: p[1][vertical_axis])
        bottom = pts_sorted[:4]
        top = pts_sorted[4:]

    if len(bottom) != 4 or len(top) != 4:
        raise ValueError("Could not split hex nodes into 4 bottom + 4 top. Check geometry/tol.")

    # On each face, classify corners by (a,b)
    def ab(p):
        return p[1][a_axis], p[1][b_axis]

    a_vals = [ab(p)[0] for p in bottom]
    b_vals = [ab(p)[1] for p in bottom]
    a_min, a_max = min(a_vals), max(a_vals)
    b_min, b_max = min(b_vals), max(b_vals)

    def pick(face, a_target, b_target):
        # pick the closest node on that face to the target (a,b) corner
        best = None
        best_d2 = None
        for p in face:
            pa, pb = ab(p)
            d2 = (pa - a_target) ** 2 + (pb - b_target) ** 2
            if best is None or d2 < best_d2:
                best = p
                best_d2 = d2
        return best[0]  # node id

    # Bottom nodes in diagram order
    n1 = pick(bottom, a_min, b_min)
    n2 = pick(bottom, a_max, b_min)
    n3 = pick(bottom, a_max, b_max)
    n4 = pick(bottom, a_min, b_max)

    # Top nodes: prefer vertical pairing (closest in a, b to the corresponding bottom node)
    top_ids = [p[0] for p in top]
    # top_map = {}

    def closest_top_to(n_bottom):
        bx, by, bz = _get_coord(n_bottom, nodeCoords)
        ba = (bx, by, bz)[a_axis]
        bb = (bx, by, bz)[b_axis]
        best = None
        best_d2 = None
        for tid in top_ids:
            tx, ty, tz = _get_coord(tid, nodeCoords)
            ta = (tx, ty, tz)[a_axis]
            tb = (tx, ty, tz)[b_axis]
            d2 = (ta - ba) ** 2 + (tb - bb) ** 2
            if best is None or d2 < best_d2:
                best = tid
                best_d2 = d2
        return best

    n5 = closest_top_to(n1)
    n6 = closest_top_to(n2)
    n7 = closest_top_to(n3)
    n8 = closest_top_to(n4)

    # Ensure uniqueness (if degeneracy causes duplicates, fall back to corner picking on top)
    if len({n5, n6, n7, n8}) != 4:
        ta_vals = [ab(p)[0] for p in top]
        tb_vals = [ab(p)[1] for p in top]
        ta_min, ta_max = min(ta_vals), max(ta_vals)
        tb_min, tb_max = min(tb_vals), max(tb_vals)
        n5 = pick(top, ta_max, tb_min)
        n6 = pick(top, ta_max, tb_max)
        n7 = pick(top, ta_min, tb_max)
        n8 = pick(top, ta_min, tb_min)

    return [n1, n2, n3, n4, n5, n6, n7, n8]


def gmsh_hex8_to_canonical(nodeList, nodeCoords=None, vertical_axis: int = 2, tol: float = 1e-9):
    """
    Preferred: coordinate-based reorder if nodeCoords is provided.
    Fallback: old hard-coded permutation (your existing behavior) if nodeCoords is None.
    """
    if nodeCoords is not None:
        return classify_hex8_nodes(nodeList, nodeCoords, vertical_axis=vertical_axis, tol=tol)

    # Fallback to your legacy mapping if no coordinates available
    # (This preserves current behavior, so we can switch call sites gradually.)
    return [nodeList[2], nodeList[6], nodeList[7], nodeList[3],
            nodeList[1], nodeList[5], nodeList[4], nodeList[0]]


# --------------------------------------------------------------------------------------------------------------
# Tcl writing utilities
# --------------------------------------------------------------------------------------------------------------
def writeNodesTcl(nodeCoordS, ndmGLOBAL, nodeDOFS=None,
                  filePrefix="nodes", outputDir=".",
                  elements=None, elementProfileS=None):
    """
    Writes a unified .tcl file defining all nodes

    Each node line includes coordinates (2D or 3D) and a comment indicating the DOF set,
    e.g. '# 3 DOFs (u,v,p)'

    Parameters:
        nodeCoordS (dict): mapping nodeTag --> (x, y, z)
        ndmGLOBAL (int): number of spatial dimensions (2 or 3)
        nodeDOFS (dict, optional): mapping nodeTag --> DOF count
        filePrefix (str): output file prefix (default "nodes")
        outputDir (str): folder where file is written
        elements
        elementProfileS

    This produces one file (nodes2D.tcl or nodes3D.tcl), unlike writeSeparatedNodeFiles(),
    which generates one per DOF category.
    """

    if nodeDOFS is None:
        nodeDOFS = {}

    # ------------------------------------------------------------------------------------------------------------
    # Build per-node domain classification from element types
    # ------------------------------------------------------------------------------------------------------------
    nodeDomain = {}
    if elements and elementProfileS:
        structureTypes = {1, 101, 201, 202}
        for el in elements:
            eType = el["type"]
            domain = "structure" if eType in structureTypes else "soil"
            for n in el["nodes"]:
                # if node belongs to both, structure overrides soil
                if n not in nodeDomain or domain == "structure":
                    nodeDomain[n] = domain

    # choose filename
    fileName = os.path.join(
        outputDir, f"{filePrefix}{'3D' if ndmGLOBAL == 3 else '2D'}.tcl"
    )

    with open(fileName, "w") as f__:
        f__.write(f"# !!!!!!!!!!!!!!!!!! Node definitions ({'3D' if ndmGLOBAL == 3 else '2D'}) !!!!!!!!!!!!!!!!!!\n\n")

        for n, coords in sorted(nodeCoordS.items()):
            # write node line depending on dimension
            if ndmGLOBAL == 2:
                x__, y__, _ = coords
                f__.write(f"node {n:<6} {x__:.6f} {y__:.6f}")
            elif ndmGLOBAL == 3:
                x__, y__, z__ = coords
                f__.write(f"node {n:<6} {x__:.6f} {y__:.6f} {z__:.6f}")
            else:
                continue  # skip if dimension undefined

            # add comment showing DOFs if available
            dofCountT = nodeDOFS.get(n, None)
            if dofCountT:
                domain = nodeDomain.get(n, "soil")  # default to soil if unknown
                if dofCountT == 2:
                    label = "(u,v)"
                elif dofCountT == 3 and ndmGLOBAL == 2:
                    if domain == "structure":
                        label = "(u,v,θz)"
                    else:
                        label = "(u,v,p)"
                elif dofCountT == 3 and ndmGLOBAL == 3:
                    label = "(u,v,w)"
                elif dofCountT == 4:
                    label = "(u,v,w,p)"
                else:
                    label = ""

                f__.write(f"    # {dofCountT} DOFs {label}")
            f__.write("\n")

    print(f"Wrote {fileName} with {len(nodeCoordS)} nodes "
          f"(comments show detected DOFs)")


def writeSeparatedNodeFiles(nodeCoords_, nodeDOFs_, ndmGlobal_,
                            filePrefix="nodesByDOF", outputDir=".",
                            labelPrefix=""):
    """
    Separates nodes into groups by DOF count (2, 3, 4, 6, etc.) and writes separate .tcl files

    Automatically handles correct ndm/ndf for each group

    Parameters:
        nodeCoords_ (dict): mapping nodeTag --> (x, y, z)
        nodeDOFs_ (dict): mapping nodeTag --> DOF count
        ndmGlobal_ (int): spatial dimension (2 or 3)
        filePrefix (str): output file prefix (default "nodesByDOF")
        outputDir (str): directory for written files
        labelPrefix (str): to distinguish soil and structure elements

    Automatically handles correct ndm/ndf for each file.
    """

    # dofGroups = {2: [], 3: [], 4: []}

    uniqueDOFs = sorted(set(nodeDOFs_.values()))
    written = []

    # for n, dof in nodeDOFs_.items():
    #     if dof in dofGroups:
    #         dofGroups[dof].append(n)

    for dofCountT in uniqueDOFs:
        nodeList = [n for n, d in nodeDOFs_.items() if d == dofCountT]
        if not nodeList:
            continue  # skip the empty group

        # prefix structural/soil labels if provided
        prefixPart = f"{labelPrefix}_" if labelPrefix else ""
        fileName = os.path.join(outputDir, f"{prefixPart}{filePrefix}_{dofCountT}DOF.tcl")
        # modelHeader = os.path.join(outputDir, f"{prefixPart}modelHeader_{dofCountT}DOF.tcl")

        # determine appropriate ndf per DOF group
        # ndf = dofCountT
        ndm = ndmGlobal_  # assume the same ndm for now (you can adjust later if hybrid 2D/3D)

        # # write model header for this DOF group
        # with open(modelHeader, "w") as fHeader:
        #     fHeader.write(f"model BasicBuilder -ndm {ndm} -ndf {ndf}\n")
        # written.append(modelHeader)

        # build node lines first (prepare node lines)
        nodeLines = []
        for n in sorted(nodeList):
            x_, y_, z_ = nodeCoords_.get(n, (0.0, 0.0, 0.0))
            if ndm == 2:
                line = f"node {n:<6} {x_:.6f} {y_:.6f}"
            else:
                line = f"node {n:<6} {x_:.6f} {y_:.6f} {z_:.6f}"
            nodeLines.append(line)

        maxLen = max(len(line) for line in nodeLines)

        # write node definitions with aligned comments
        with open(fileName, "w") as f__:
            f__.write(f"# !!!!!!!!!!!!!!!!!!! Nodes with {dofCountT} DOFs !!!!!!!!!!!!!!!!!!!\n\n")

            for line, n in zip(nodeLines, sorted(nodeList)):
                if dofCountT == 2:
                    label = "(u,v)"
                elif dofCountT == 3 and ndm == 2:
                    label = "(u,v,rz)"
                elif dofCountT == 3 and ndm == 3:
                    label = "(u,v,w)"  # could also be (u,v,w) for solid nodes
                elif dofCountT == 4:
                    label = "(u,v,w,p)"
                elif dofCountT == 6:
                    label = "(u,v,w,rx,ry,rz)"
                else:
                    label = ""

                comment = f"# {dofCountT} DOFs {label}"
                f__.write(f"{line.ljust(maxLen + 4)}{comment}\n")

        written.append(fileName)

    # summary print that perhaps could be useful
    print("\nSummary by DOF group:")
    for dofCountT in uniqueDOFs:
        count = sum(1 for d in nodeDOFs_.values() if d == dofCountT)
        print(f"  {dofCountT}-DOF nodes: {count}")

    print("Wrote separated node files for all DOF groups detected.")


def writeElementsTcl(elements_, profiles_, mainSoilTags_, gVal_,
                     nodeCoords=None,
                     filePrefix="elements_", outputDir='.'):

    """
    Writes .tcl files grouped by element type.

    Each file contains OpenSees element definitions using the appropriate formulation
    (e.g., quadUP, brickUP, SSPbrickUP).
    Files are named with the prefix 'elements_' followed by the element key, e.g., elements_quadUP.tcl.

    Parameters:
        nodeCoords: node coordinates
        elements_ (list[dict]): each with keys: 'id', 'type', 'group', 'nodes'
        profiles_ (dict[int, dict]): element type --> profile dict
        mainSoilTags_ (dict[int, int]): per-physical-group soil tag mapping
        gVal_ (float): gravity magnitude used in body force terms
        filePrefix (str): filename prefix (default: "elements_")
        outputDir (str): directory for output files
    """

    print("\n[DEBUG] Material mapping being used:")
    for k, v in mainSoilTags_.items():
        print(f"  Physical group {k} --> material {v}")
    print()

    written = []
    for eType_ in {el["type"] for el in elements_ if el["type"] in profiles_}:
        profile = profiles_[eType_]
        fileName = os.path.join(outputDir, f"{filePrefix}{profile['key']}.tcl")

        with open(fileName, "w") as f__:
            # !!!!!!!!! 2D cases !!!!!!!!!

            f__.write(f"# !!!!!!!!!!! {profile['key']} elements !!!!!!!!!!!\n\n")

            for el in [e for e in elements_ if e["type"] == eType_]:
                phy = el["group"]
                nodes = " ".join(str(n) for n in el["nodes"])
                key = profile["key"]

                if key == "quad4":
                    # 2D plan strain, we rename to OpenSees "quad'
                    keyOut = "quad"
                    # massDen, fluidDen = 1755, 1000
                    # alpha = np.atan(2.0 / 100)  # 2% slope
                    # alphaRads = alpha

                    alphaDeg = 0.0
                    alphaRads = np.deg2rad(alphaDeg)

                    thicknessQuad4 = {i: 1.0 for i in mainSoilTags_}

                    xW = - gVal_ * np.sin(alphaRads)
                    yW = - gVal_ * np.cos(alphaRads)

                    f__.write(
                        f"element "
                        f"{keyOut} "
                        f"{el['id']} "
                        f"{nodes} "
                        f"{thicknessQuad4[phy]} "
                        f"PlaneStrain "
                        f"{mainSoilTags_[phy]} "
                        f"0.0 "
                        f"0.0 "
                        f"{xW:.4f} "
                        f"{yW:.4f}\n"
                    )

                elif key == "ASDLeft":
                    # 2D plan strain, we rename to OpenSees "ASDAbsorbingBoundary2D"
                    keyOut = "ASDAbsorbingBoundary2D"

                    E_ASD = 3.0e9
                    poissASD = 0.3
                    G_ASD = E_ASD / (2.0 * (1.0 + poissASD))
                    thicknessASD = 1.0

                    rhoASD = 2100.0

                    bType = "L"

                    f__.write(
                        f"element "
                        f"{keyOut} "
                        f"{el['id']} "
                        f"{nodes} "
                        f"{G_ASD} "
                        f"{poissASD} "
                        f"{rhoASD} "
                        f"{thicknessASD} "
                        f"{bType}\n"
                    )

                elif key == "ASDRight":
                    # 2D plan strain, we rename to OpenSees "ASDAbsorbingBoundary2D"
                    keyOut = "ASDAbsorbingBoundary2D"

                    E_ASD = 3.0e9
                    poissASD = 0.3
                    G_ASD = E_ASD / (2.0 * (1.0 + poissASD))
                    thicknessASD = 1.0

                    rhoASD = 2100.0

                    bType = "R"

                    f__.write(
                        f"element "
                        f"{keyOut} "
                        f"{el['id']} "
                        f"{nodes} "
                        f"{G_ASD} "
                        f"{poissASD} "
                        f"{rhoASD} "
                        f"{thicknessASD} "
                        f"{bType}\n"
                    )

                elif key == "ASDBottom":
                    # 2D plan strain, we rename to OpenSees "ASDAbsorbingBoundary2D"
                    keyOut = "ASDAbsorbingBoundary2D"

                    E_ASD = 3.0e9
                    poissASD = 0.3
                    G_ASD = E_ASD / (2.0 * (1.0 + poissASD))
                    thicknessASD = 1.0

                    rhoASD = 2100.0

                    bType = "B"

                    # tsX = tsX

                    f__.write(
                        f"element "
                        f"{keyOut} "
                        f"{el['id']} "
                        f"{nodes} "
                        f"{G_ASD} "
                        f"{poissASD} "
                        f"{rhoASD} "
                        f"{thicknessASD} "
                        f"{bType} "
                        f"-fx "
                        f"$tsX\n"
                    )

                elif key == "ASDBottomL":
                    # 2D plan strain, we rename to OpenSees "ASDAbsorbingBoundary2D"
                    keyOut = "ASDAbsorbingBoundary2D"

                    E_ASD = 3.0e9
                    poissASD = 0.3
                    G_ASD = E_ASD / (2.0 * (1.0 + poissASD))
                    thicknessASD = 1.0

                    rhoASD = 2100.0

                    bType = "LB"

                    f__.write(
                        f"element "
                        f"{keyOut} "
                        f"{el['id']} "
                        f"{nodes} "
                        f"{G_ASD} "
                        f"{poissASD} "
                        f"{rhoASD} "
                        f"{thicknessASD} "
                        f"{bType} "
                        f"-fx "
                        f"$tsX\n"
                    )

                elif key == "ASDBottomR":
                    # 2D plan strain, we rename to OpenSees "ASDAbsorbingBoundary2D"
                    keyOut = "ASDAbsorbingBoundary2D"

                    E_ASD = 3.0e9
                    poissASD = 0.3
                    G_ASD = E_ASD / (2.0 * (1.0 + poissASD))
                    thicknessASD = 1.0

                    rhoASD = 2100.0

                    bType = "RB"

                    f__.write(
                        f"element "
                        f"{keyOut} "
                        f"{el['id']} "
                        f"{nodes} "
                        f"{G_ASD} "
                        f"{poissASD} "
                        f"{rhoASD} "
                        f"{thicknessASD} "
                        f"{bType} "
                        f"-fx "
                        f"$tsX\n"
                    )

                elif key == "quadUP":  # OK VERIFIED

                    # porosity = {i: 1.0 for i in mainSoilTags_}
                    # see the physical group in which we want the "quadUP" element in gmsh (here, Plane 4 and 5)
                    # in this case, only "Planes 4 and 5" will have customized porosity (perhaps different from 1.0)
                    #
                    porosityCustom = {
                        4: 1.09,
                        5: 1.05
                    }

                    # ensure all other groups get default 1.0 if not explicitly listed
                    # Build the full porosity map (default 1.0 if not listed)
                    porosity = {}
                    for i in mainSoilTags_:
                        porosity[i] = float(porosityCustom.get(int(i), 1.0))

                    Bf = 2.2e6  # kN/m^2 (for pure water)

                    # thickness, bulk, fluid mass per physical group
                    thicknessQuadUP = {i: 1.0 for i in mainSoilTags_}

                    bulkQuadUP = {i: Bf / porosity[i] for i in mainSoilTags_}
                    fMassQuadUP = {i: 1 for i in mainSoilTags_}  # fluid density (for ex., 1.0 t/m^3)

                    hPermRaw = 5.0e-4
                    vPermRaw = 5.0e-4

                    hPermQuadUP = {i: hPermRaw / (gVal_ * fMassQuadUP[i]) for i in mainSoilTags_}
                    vPermQuadUP = {i: vPermRaw / (gVal_ * fMassQuadUP[i]) for i in mainSoilTags_}

                    alpha_ = 4  # in degrees already! always convert in radians
                    alpha_V = np.deg2rad(alpha_)
                    b1QuadUP = + gVal_ * np.sin(alpha_V)
                    b2QuadUP = - gVal_ * np.cos(alpha_V)

                    tQuadUP = 0.0  # normal traction if needed

                    f__.write(
                        f"element "
                        f"{key} "
                        f"{el['id']} "
                        f"{nodes} "
                        f"{thicknessQuadUP[phy]} "
                        f"{mainSoilTags_[phy]} "
                        f"{bulkQuadUP[phy]} "
                        f"{fMassQuadUP[phy]} "
                        f"{hPermQuadUP[phy]} "
                        f"{vPermQuadUP[phy]} "
                        f"{b1QuadUP} "
                        f"{b2QuadUP} "
                        f"{tQuadUP}\n"
                    )

                elif key == "bbarQuadUP":  # OK VERIFIED

                    # see the physical group in which we want the "quadUP" element in gmsh (here, Plane 2 and Plane 3)
                    # in this case, only "Planes 2 and 3" will have customized porosity (perhaps different from 1.0)

                    porosityCustom = {
                        2: 1.01,
                        3: 1.02
                    }

                    # ensure all other groups get default 1.0 if not explicitly listed
                    # Build the full porosity map (default 1.0 if not listed)
                    porosity = {}
                    for i in mainSoilTags_:
                        porosity[i] = float(porosityCustom.get(int(i), 1.0))

                    Bf = 2.2e6  # kN/m^2 (for pure water)

                    thicknessBbarQuadUP = {i: 1.0 for i in mainSoilTags_}

                    bulkBbarQuadUP = {i: Bf / porosity[i] for i in mainSoilTags_}
                    fMassBbarQuadUP = {i: 1 for i in mainSoilTags_}

                    hPermBbarQuadUP = 5.0e-4
                    vPermBbarQuadUP = 5.0e-4
                    hPermBbarQuadUP = {i: hPermBbarQuadUP / (gVal_ * fMassBbarQuadUP[i]) for i in mainSoilTags_}
                    vPermBbarQuadUP = {i: vPermBbarQuadUP / (gVal_ * fMassBbarQuadUP[i]) for i in mainSoilTags_}

                    alpha_ = 4  # in degrees already! always convert in radian
                    alpha_V = np.deg2rad(alpha_)
                    b1BbarQuadUP = + gVal_ * np.sin(alpha_V)
                    b2BbarQuadUP = - gVal_ * np.cos(alpha_V)

                    tBbarQuadUP = 0.0

                    f__.write(
                        f"element "
                        f"{key} "
                        f"{el['id']} "
                        f"{nodes} "
                        f"{thicknessBbarQuadUP[phy]} "
                        f"{mainSoilTags_[phy]} "
                        f"{bulkBbarQuadUP[phy]} "
                        f"{fMassBbarQuadUP[phy]} "
                        f"{hPermBbarQuadUP[phy]} "
                        f"{vPermBbarQuadUP[phy]} "
                        f"{b1BbarQuadUP} "
                        f"{b2BbarQuadUP} "
                        f"{tBbarQuadUP}\n"
                    )

                elif key == "9_4_QuadUP":  # OK VERIFIED

                    # see the physical group in which we want the "quadUP" element in gmsh (here, Plane 4 and 5)
                    # in this case, only "Planes 2 and 3" will have customized porosity (perhaps different from 1.0)

                    porosityCustom = {
                        2: 1.01,
                        3: 1.02
                    }

                    # ensure all other groups get default 1.0 if not explicitly listed
                    # Build the full porosity map (default 1.0 if not listed)
                    porosity = {}
                    for i in mainSoilTags_:
                        porosity[i] = float(porosityCustom.get(int(i), 1.0))

                    Bf = 2.2e6  # kN/m^2 (for pure water)

                    thickness9_4_QuadUP = {i: 1.0 for i in mainSoilTags_}

                    bulk9_4_QuadUP = {i: Bf / porosity[i] for i in mainSoilTags_}
                    fMass9_4_QuadUP = {i: 1 for i in mainSoilTags_}

                    hPerm9_4_QuadUP = 5.0e-4
                    vPerm9_4_QuadUP = 5.0e-4

                    hPerm9_4_QuadUP = {i: hPerm9_4_QuadUP / (gVal_ * fMass9_4_QuadUP[i]) for i in mainSoilTags_}
                    vPerm9_4_QuadUP = {i: vPerm9_4_QuadUP / (gVal_ * fMass9_4_QuadUP[i]) for i in mainSoilTags_}

                    alpha_ = 4  # in degrees already! always convert in radians
                    alpha_V = np.deg2rad(alpha_)
                    b19_4_QuadUP = + gVal_ * np.sin(alpha_V)
                    b29_4_QuadUP = - gVal_ * np.cos(alpha_V)

                    f__.write(
                        f"element "
                        f"{key} "
                        f"{el['id']} "
                        f"{nodes} "
                        f"{thickness9_4_QuadUP[phy]} "
                        f"{mainSoilTags_[phy]} "
                        f"{bulk9_4_QuadUP[phy]} "
                        f"{fMass9_4_QuadUP[phy]} "
                        f"{hPerm9_4_QuadUP[phy]} "
                        f"{vPerm9_4_QuadUP[phy]} "
                        f"{b19_4_QuadUP} "
                        f"{b29_4_QuadUP}\n"
                    )

                # !!!!!!!!! 3D cases !!!!!!!!!

                elif key == "SSPbrick":  # displacement-only SSPbrick
                    # slope angle (if needed)
                    alpha__ = 0.0  # degrees
                    alphaVal = np.deg2rad(alpha__)
                    gx = + gVal_ * np.sin(alphaVal)
                    gy = 0.0
                    gz = - gVal_ * np.cos(alphaVal)

                    nodeList = el["nodes"]

                    # Same node reordering you use for other 8-node bricks
                    # nodesF = [nodeList[2], nodeList[6], nodeList[7], nodeList[3],
                    #           nodeList[1], nodeList[5], nodeList[4], nodeList[0]]

                    nodesF = gmsh_hex8_to_canonical(nodeList, nodeCoords=nodeCoords, vertical_axis=2, tol=1e-9)

                    nodes = " ".join(str(n) for n in nodesF)

                    f__.write(
                        f"element SSPbrick {el['id']} {nodes} {mainSoilTags_[phy]} "
                        f"{gx} {gy} {gz}\n"
                    )

                elif key == "brickUP":  # OK VERIFIED

                    # see the physical group in which we want the "quadUP" element in gmsh (here, Plane 4 and 5)
                    # in this case, only "Planes 2 and 3" will have customized porosity (perhaps different from 1.0)

                    porosityCustom = {
                        2: 1.01,
                        3: 1.02
                    }

                    # ensure all other groups get default 1.0 if not explicitly listed
                    # Build the full porosity map (default 1.0 if not listed)
                    porosity = {}
                    for i in mainSoilTags_:
                        porosity[i] = float(porosityCustom.get(int(i), 1.0))

                    Bf = 2.2e6  # kN/m^2 (for pure water)

                    bulkBrickUP = {i: Bf / porosity[i] for i in mainSoilTags_}
                    fMassBrickUP = {i: 1 for i in mainSoilTags_}

                    PermXBrickUP = 5.0e-4
                    PermYBrickUP = 5.0e-4
                    PermZBrickUP = 5.0e-4

                    # alpha_ = 4 # in degrees already! always convert in degrees
                    PermXBrickUP = {i: PermXBrickUP / (gVal_ * fMassBrickUP[i]) for i in mainSoilTags_}
                    PermYBrickUP = {i: PermYBrickUP / (gVal_ * fMassBrickUP[i]) for i in mainSoilTags_}
                    PermZBrickUP = {i: PermZBrickUP / (gVal_ * fMassBrickUP[i]) for i in mainSoilTags_}

                    alpha__ = 0.0  # in degrees
                    alphaVal = np.deg2rad(alpha__)
                    gx = + gVal_ * np.sin(alphaVal)
                    gy = 0.0
                    gz = - gVal_ * np.cos(alphaVal)

                    bXBrickUP = gx
                    bYBrickUP = gy
                    bZBrickUP = gz

                    nodeList = el["nodes"]  # actual list of integers from the mesh
                    # nodesF = [nodeList[5], nodeList[6], nodeList[2], nodeList[1],
                    #           nodeList[4], nodeList[7], nodeList[3], nodeList[0]]
                    nodesF = gmsh_hex8_to_canonical(nodeList, nodeCoords=nodeCoords, vertical_axis=2, tol=1e-9)

                    nodes = " ".join(str(n) for n in nodesF)

                    f__.write(
                        f"element "
                        f"{key} "
                        f"{el['id']} "
                        f"{nodes} "
                        f"{mainSoilTags_[phy]} "
                        f"{bulkBrickUP[phy]} "
                        f"{fMassBrickUP[phy]} "
                        f"{PermXBrickUP[phy]} "
                        f"{PermYBrickUP[phy]} "
                        f"{PermZBrickUP[phy]} "
                        f"{bXBrickUP} "
                        f"{bYBrickUP} "
                        f"{bZBrickUP}\n"
                    )

                elif key == "bbarBrickUP":  # OK VERIFIED

                    # see the physical group in which we want the "quadUP" element in gmsh (here, Plane 4 and 5)
                    # in this case, only "Planes 2 and 3" will have customized porosity (perhaps different from 1.0)

                    porosityCustom = {
                        2: 1.01,
                        3: 1.02
                    }

                    # ensure all other groups get default 1.0 if not explicitly listed
                    # Build the full porosity map (default 1.0 if not listed)
                    porosity = {}
                    for i in mainSoilTags_:
                        porosity[i] = float(porosityCustom.get(int(i), 1.0))

                    Bf = 2.2e6  # kN/m^2 (for pure water)

                    bulkBbarBrickUP = {i: Bf / porosity[i] for i in mainSoilTags_}
                    fMassBbarBrickUP = {i: 1 for i in mainSoilTags_}

                    PermXBbarBrickUP = 5.0e-4
                    PermYBbarBrickUP = 5.0e-4
                    PermZBbarBrickUP = 5.0e-4
                    # alpha_ = 4 # in degrees already! always convert in degrees
                    PermXBbarBrickUP = {i: PermXBbarBrickUP / (gVal_ * fMassBbarBrickUP[i]) for i in mainSoilTags_}
                    PermYBbarBrickUP = {i: PermYBbarBrickUP / (gVal_ * fMassBbarBrickUP[i]) for i in mainSoilTags_}
                    PermZBbarBrickUP = {i: PermZBbarBrickUP / (gVal_ * fMassBbarBrickUP[i]) for i in mainSoilTags_}

                    alpha__ = 0.0  # in degrees
                    alphaVal = np.deg2rad(alpha__)
                    gx = + gVal_ * np.sin(alphaVal)
                    gy = 0.0
                    gz = - gVal_ * np.cos(alphaVal)

                    bXBbarBrickUP = gx
                    bYBbarBrickUP = gy
                    bZBbarBrickUP = gz

                    nodeList = el["nodes"]  # actual list of integers from the mesh
                    # nodesF = [nodeList[5], nodeList[6], nodeList[2], nodeList[1],
                    #           nodeList[4], nodeList[7], nodeList[3], nodeList[0]]

                    nodesF = gmsh_hex8_to_canonical(nodeList, nodeCoords=nodeCoords, vertical_axis=2, tol=1e-9)

                    nodes = " ".join(str(n) for n in nodesF)

                    f__.write(
                        f"element "
                        f"{key} "
                        f"{el['id']} "
                        f"{nodes} "
                        f"{mainSoilTags_[phy]} "
                        f"{bulkBbarBrickUP[phy]} "
                        f"{fMassBbarBrickUP[phy]} "
                        f"{PermXBbarBrickUP[phy]} "
                        f"{PermYBbarBrickUP[phy]} "
                        f"{PermZBbarBrickUP[phy]} "
                        f"{bXBbarBrickUP} "
                        f"{bYBbarBrickUP} "
                        f"{bZBbarBrickUP}\n"
                    )

                elif key == "SSPbrickUP":  # VERIFIED BUT BE CAREFUL ABOUT "alphaParamSSPbrickUP"
                    # for 3D SSPbrickUP
                    # best and largely stabilized for a dynamic-only,
                    # single-point, high-performance version of brickUP

                    # see the physical group in which we want the "quadUP" element in gmsh (here, Plane 4 and 5)
                    # in this case, only "Planes 2 and 3" will have customized porosity (perhaps different from 1.0)

                    porosityCustom = {
                        1: 0.409,
                        2: 0.377
                    }

                    # ensure all other groups get default 1.0 if not explicitly listed
                    # Build the full porosity map (default 1.0 if not listed)
                    porosity = {}
                    for i in mainSoilTags_:
                        porosity[i] = float(porosityCustom.get(int(i), 1.0))

                    Bf = 2.2e6  # kN/m^2 (for pure water)

                    bulkSSPbrickUP = {i: Bf for i in mainSoilTags_}  # fluid bulk modulus
                    fMassSSPbrickUP = {i: 1.0 for i in mainSoilTags_}  # fluid density

                    # permeability defined per physical group (same pattern as porosity)
                    # default raw permeability (m/s) for any group not explicitly listed
                    permDefaultX, permDefaultY, permDefaultZ = 6.05e-5, 6.05e-5, 6.05e-5

                    # Override specific physical groups (example values)
                    permCustomX = {
                        1: 6.05e-5,  # layer 1 (e.g. loose)
                        2: 3.70e-5   # layer 2 (e.g. dense)
                    }
                    permCustomY = {
                        1: 6.05e-5,
                        2: 3.70e-5
                    }
                    permCustomZ = {
                        1: 6.05e-5,
                        2: 3.70e-5
                    }

                    # Build full permeability maps for all groups in mainSoilTags_
                    permRawX, permRawY, permRawZ = {}, {}, {}
                    for i in mainSoilTags_:
                        ii = int(i)
                        permRawX[ii] = float(permCustomX.get(ii, permDefaultX))
                        permRawY[ii] = float(permCustomY.get(ii, permDefaultY))
                        permRawZ[ii] = float(permCustomZ.get(ii, permDefaultZ))

                    # voids (or void ratio / void fraction): defined per physical group like porosity
                    voidsDefault = 0.7

                    # recall: void ratio e = n / (1 - n); n = porosity
                    voidsCustom = {
                        1: 0.692,  # layer 1 (e.g. loose)
                        2: 0.605   # layer 2 (e.g. dense)
                    }

                    voidsSSPbrickUP = {}
                    for i in mainSoilTags_:
                        voidsSSPbrickUP[i] = float(voidsCustom.get(int(i), voidsDefault))

                    alphaParamSSPbrickUP = {i: 2.0e-6 for i in mainSoilTags_}  # stabilization parameter

                    alpha__ = 0.0  # in degrees
                    alphaVal = np.deg2rad(alpha__)
                    gx = + gVal_ * np.sin(alphaVal)
                    gy = 0.0
                    gz = - gVal_ * np.cos(alphaVal)

                    nodeList = el["nodes"]  # actual list of integers from the mesh
                    # nodesF = [nodeList[5], nodeList[6], nodeList[2], nodeList[1],
                    #           nodeList[4], nodeList[7], nodeList[3], nodeList[0]]
                    nodesF = gmsh_hex8_to_canonical(nodeList, nodeCoords=nodeCoords, vertical_axis=2, tol=1e-9)

                    nodes = " ".join(str(n) for n in nodesF)

                    permXSSPbrickUP = {i: permRawX[i] / (gVal_ * fMassSSPbrickUP[i]) for i in mainSoilTags_}
                    permYSSPbrickUP = {i: permRawY[i] / (gVal_ * fMassSSPbrickUP[i]) for i in mainSoilTags_}
                    permZSSPbrickUP = {i: permRawZ[i] / (gVal_ * fMassSSPbrickUP[i]) for i in mainSoilTags_}

                    f__.write(
                        f"element "
                        f"SSPbrickUP "
                        f"{el['id']} "
                        f"{nodes} "
                        f"{mainSoilTags_[phy]} "
                        f"{bulkSSPbrickUP[phy]} "
                        f"{fMassSSPbrickUP[phy]} "
                        f"{permXSSPbrickUP[phy]} "
                        f"{permYSSPbrickUP[phy]} "
                        f"{permZSSPbrickUP[phy]} "
                        f"{voidsSSPbrickUP[phy]} "
                        f"{alphaParamSSPbrickUP[phy]} "
                        f"{gx} "
                        f"{gy} "
                        f"{gz}\n"
                    )

                elif key.startswith("ASD3D"):

                    keyOut = "ASDAbsorbingBoundary3D"

                    E_ASD = 3.0e9
                    poissASD = 0.3

                    G_ASD = E_ASD / (2.0 * (1.0 + poissASD))
                    rhoASD = 2100.0

                    bType = key.replace("ASD3D", "")

                    nodeList = el["nodes"]

                    # nodesF = [nodeList[5], nodeList[6], nodeList[2], nodeList[1],
                    #           nodeList[4], nodeList[7], nodeList[3], nodeList[0]]

                    nodesF = gmsh_hex8_to_canonical(nodeList, nodeCoords=nodeCoords, vertical_axis=2, tol=1e-9)

                    nodes = " ".join(str(n) for n in nodesF)

                    f__.write(f"element {keyOut} {el['id']} {nodes} {G_ASD} {poissASD} {rhoASD} {bType}")

                    if "B" in bType:
                        f__.write(" -fx $tsX")
                    if "F" in bType or "K" in bType:
                        f__.write(" -fy $tsY")
                    if "T" in bType:
                        f__.write(" -fz $tsZ")

                    f__.write("\n")

                elif key == "20_8_BrickUP":  # OK VERIFIED
                    # see the physical group in which we want the "quadUP" element in gmsh (here, Plane 4 and 5)
                    # in this case, only "Planes 2 and 3" will have customized porosity (perhaps different from 1.0)

                    porosityCustom = {
                        2: 1.01,
                        3: 1.02
                    }

                    # ensure all other groups get default 1.0 if not explicitly listed
                    # Build the full porosity map (default 1.0 if not listed)
                    porosity = {}
                    for i in mainSoilTags_:
                        porosity[i] = float(porosityCustom.get(int(i), 1.0))

                    Bf = 2.2e6  # kN/m^2 (for pure water)

                    bulk_20_8_BrickUP = {i: Bf / porosity[i] for i in mainSoilTags_}
                    fMass_20_8_BrickUP = {i: 1 for i in mainSoilTags_}

                    PermX_20_8_BrickUP = 5.0e-4
                    PermY_20_8_BrickUP = 5.0e-4
                    PermZ_20_8_BrickUP = 5.0e-4

                    # alpha_ = 4 # in degrees already! always convert in degrees
                    PermX_20_8_BrickUP = {i: PermX_20_8_BrickUP / (gVal_ * fMass_20_8_BrickUP[i]) for i in
                                          mainSoilTags_}
                    PermY_20_8_BrickUP = {i: PermY_20_8_BrickUP / (gVal_ * fMass_20_8_BrickUP[i]) for i in
                                          mainSoilTags_}
                    PermZ_20_8_BrickUP = {i: PermZ_20_8_BrickUP / (gVal_ * fMass_20_8_BrickUP[i]) for i in
                                          mainSoilTags_}

                    alpha__ = 0.0  # in degrees
                    alphaVal = np.deg2rad(alpha__)
                    gx = + gVal_ * np.sin(alphaVal)
                    gy = 0.0
                    gz = - gVal_ * np.cos(alphaVal)

                    bX_20_8_BrickUP = gx
                    bY_20_8_BrickUP = gy
                    bZ_20_8_BrickUP = gz

                    nodeList = el["nodes"]  # actual list of integers from the mesh

                    # nodesF = [nodeList[5], nodeList[6], nodeList[2], nodeList[1],
                    #           nodeList[4], nodeList[7], nodeList[3], nodeList[0],
                    #           nodeList[12], nodeList[18], nodeList[14], nodeList[11],
                    #           nodeList[10], nodeList[17], nodeList[15], nodeList[9],
                    #           nodeList[8], nodeList[16], nodeList[19], nodeList[13]]

                    nodesF = [nodeList[2], nodeList[6], nodeList[7], nodeList[3],  # OK
                              nodeList[1], nodeList[5], nodeList[4], nodeList[0],  # OK
                              nodeList[14], nodeList[19], nodeList[15], nodeList[13],  # OK
                              nodeList[12], nodeList[16], nodeList[10], nodeList[8],  # OK
                              nodeList[11], nodeList[18], nodeList[17], nodeList[9]]  # OK

                    nodes = " ".join(str(n) for n in nodesF)

                    f__.write(
                        f"element "
                        f"{key} "
                        f"{el['id']} "
                        f"{nodes} "
                        f"{mainSoilTags_[phy]} "
                        f"{bulk_20_8_BrickUP[phy]} "
                        f"{fMass_20_8_BrickUP[phy]} "
                        f"{PermX_20_8_BrickUP[phy]} "
                        f"{PermY_20_8_BrickUP[phy]} "
                        f"{PermZ_20_8_BrickUP[phy]} "
                        f"{bX_20_8_BrickUP} "
                        f"{bY_20_8_BrickUP} "
                        f"{bZ_20_8_BrickUP}\n"
                    )

                elif key == "elasticBeamColumn2D":

                    keyOut = "elasticBeamColumn"

                    # Define typical material and section properties
                    A = 0.25
                    E = 2.1e11
                    Iz = 3.0e-4
                    transfTag = 1
                    massDens = 7850.0
                    useCMass = True

                    line = (
                        f"element {keyOut} {el['id']} {nodes} "
                        f"{A} {E} {Iz} {transfTag}"
                    )

                    if massDens:
                        line += f" -mass {massDens}"
                    if useCMass:
                        line += " -cMass"

                    f__.write(line + "\n")

                elif key == "elasticBeamColumn3D":

                    keyOut = "elasticBeamColumn"

                    # Define typical material and section properties
                    A = 0.25
                    E = 2.1e11
                    G = 8.1e10
                    J = 1.0e-4
                    Iy = 2.0e-4
                    Iz = 3.0e-4
                    transfTag = 1
                    massDens = 7850.0
                    useCMass = True

                    line = (
                        f"element {keyOut} {el['id']} {nodes} "
                        f"{A} {E} {G} {J} {Iy} {Iz} {transfTag}"
                    )

                    if massDens:
                        line += f" -mass {massDens}"
                    if useCMass:
                        line += " -cMass"

                    f__.write(line + "\n")

                elif key in ("dispBeamColumn2D", "dispBeamColumn3D"):

                    keyOut = "dispBeamColumn"

                    # REQUIRED by OpenSees for dispBeamColumn:
                    # element dispBeamColumn $eleTag $iNode $jNode $numIntgrPts $secTag $transfTag ...
                    numIntgrPts = 5
                    secTag = 1
                    transfTag = 1

                    rhoPile = 2.4
                    outerDiamP = 0.67
                    thickPile = 0.019

                    pileArea = (np.pi/4) * ((outerDiamP ** 2) - (outerDiamP - 2 * thickPile) ** 2)

                    massDens = pileArea * rhoPile    # optional: set > 0.0 to activate -mass
                    useCMass = False                 # optional: True --> add -cMass
                    intType = None                   # optional: e.g., "Legendre", "Lobatto", ...

                    line = (
                        f"element {keyOut} {el['id']} {nodes} "
                        f"{numIntgrPts} {secTag} {transfTag}"
                    )

                    if massDens:
                        line += f" -mass {massDens}"
                    if useCMass:
                        line += " -cMass"
                    if intType:
                        line += f" -integration {intType}"

                    f__.write(line + "\n")

        written.append(fileName)
    print(f"Wrote element definition files: {', '.join(written)}")


# ----------------------------------------------------------------------------------------------------------------
# DOF rules functions (we define here so the dictionary can use them)
# ----------------------------------------------------------------------------------------------------------------
def beam2D_DOFs(ns_):
    # 2D beam nodes: u, v, and rotation θz
    return {n: 3 for n in ns_}


def beam3D_DOFs(ns_):
    # 3D beam nodes: u, v, w, and rotations θx, θy, θz
    return {n: 6 for n in ns_}


def only2DOFs(ns_):
    # every nodes get 2 DOFs: u, v
    return {n: 2 for n in ns_}


def both2and3DOFs(ns_):
    # 9_4_QuadUP: 4 corner nodes = 3 DOFs, middle nodes = 2 DOFs
    return {**{n: 3 for n in ns_[:4]}, **{n: 2 for n in ns_[4:]}}


def threeDOFs(ns_):
    # every node gets 3 DOFs (u, v, p)
    return {n: 3 for n in ns_}


def threeDOFs3D(ns_):
    # 3D displacement-only nodes: u, v, w
    return {n: 3 for n in ns_}


def fourDOFs3D(ns_):
    # for BrickUP: u, v, w, p; that is 4 DOFs per node
    return {n: 4 for n in ns_}


def twentyEightBrickDOFs(ns_):
    # 20_8_Node_BrickUP (Gmsh type 17): 1st-8 nodes (corners) have 4 DOFs (u,v,w,p), rest 12 nodes have 3 DOFs (u,v,w)
    return {**{n: 4 for n in ns_[:8]}, **{n: 3 for n in ns_[8:]}}


# --------------------------------------------------------------------------------------------------------------
# ELEMENT PROFILE MAP (GMSH element type --> metadata)
# --------------------------------------------------------------------------------------------------------------
elementProfiles = {
    # BEAM ELEMENTS (1D structural members)
    # GMSH TYPE 1 = 2-node line element
    1: {"key": "elasticBeamColumn2D", "ndm": 2, "needsP": False, "dofRule": beam2D_DOFs},
    101: {"key": "elasticBeamColumn3D", "ndm": 3, "needsP": False, "dofRule": beam3D_DOFs},
    201: {"key": "dispBeamColumn2D", "ndm": 2, "needsP": False, "dofRule": beam2D_DOFs},
    202: {"key": "dispBeamColumn3D", "ndm": 3, "needsP": False, "dofRule": beam3D_DOFs},

    # SOIL ELEMENTS NOW
    3: {"key": "quad4", "ndm": 2, "needsP": False, "dofRule": only2DOFs},
    103: {"key": "bbarQuadUP", "ndm": 2, "needsP": True, "dofRule": threeDOFs},
    1003: {"key": "quadUP", "ndm": 2, "needsP": True, "dofRule": threeDOFs},

    # !!! 2D boundary absorbing START !!!
    10031: {"key": "ASDLeft", "ndm": 2, "needsP": False, "dofRule": only2DOFs},  # ASDBoundary Left
    10032: {"key": "ASDBottom", "ndm": 2, "needsP": False, "dofRule": only2DOFs},  # ASDBoundary Bottom
    10033: {"key": "ASDRight", "ndm": 2, "needsP": False, "dofRule": only2DOFs},  # ASDBoundary Right
    10034: {"key": "ASDBottomL", "ndm": 2, "needsP": False, "dofRule": only2DOFs},  # ASDBoundary Bottom left
    10035: {"key": "ASDBottomR", "ndm": 2, "needsP": False, "dofRule": only2DOFs},  # ASDBoundary Bottom right
    # !!! 2D boundary absorbing END !!!

    10: {"key": "9_4_QuadUP", "ndm": 2, "needsP": True, "dofRule": both2and3DOFs},

    # !!!
    5: {"key": "brickUP", "ndm": 3, "needsP": True, "dofRule": fourDOFs3D},  # 8-node 3D u-p
    105: {"key": "bbarBrickUP", "ndm": 3, "needsP": True, "dofRule": fourDOFs3D},
    1005: {"key": "SSPbrickUP", "ndm": 3, "needsP": True, "dofRule": fourDOFs3D},  # best for huge 3D dynamic pbs
    1055: {"key": "SSPbrick", "ndm": 3, "needsP": False, "dofRule": threeDOFs3D},

    # !!! 3D boundary absorbing START !!!
    10051: {"key": "ASD3DL", "ndm": 3, "needsP": False, "dofRule": threeDOFs3D},
    10052: {"key": "ASD3DR", "ndm": 3, "needsP": False, "dofRule": threeDOFs3D},
    10053: {"key": "ASD3DK", "ndm": 3, "needsP": False, "dofRule": threeDOFs3D},
    10054: {"key": "ASD3DF", "ndm": 3, "needsP": False, "dofRule": threeDOFs3D},
    10055: {"key": "ASD3DBL", "ndm": 3, "needsP": False, "dofRule": threeDOFs3D},
    10056: {"key": "ASD3DBR", "ndm": 3, "needsP": False, "dofRule": threeDOFs3D},
    10057: {"key": "ASD3DBK", "ndm": 3, "needsP": False, "dofRule": threeDOFs3D},
    10058: {"key": "ASD3DBF", "ndm": 3, "needsP": False, "dofRule": threeDOFs3D},
    10059: {"key": "ASD3DLK", "ndm": 3, "needsP": False, "dofRule": threeDOFs3D},
    10060: {"key": "ASD3DBLK", "ndm": 3, "needsP": False, "dofRule": threeDOFs3D},
    10061: {"key": "ASD3DRK", "ndm": 3, "needsP": False, "dofRule": threeDOFs3D},
    10062: {"key": "ASD3DBRK", "ndm": 3, "needsP": False, "dofRule": threeDOFs3D},
    10063: {"key": "ASD3DLF", "ndm": 3, "needsP": False, "dofRule": threeDOFs3D},
    10064: {"key": "ASD3DBLF", "ndm": 3, "needsP": False, "dofRule": threeDOFs3D},
    10065: {"key": "ASD3DRF", "ndm": 3, "needsP": False, "dofRule": threeDOFs3D},
    10066: {"key": "ASD3DBRF", "ndm": 3, "needsP": False, "dofRule": threeDOFs3D},
    10067: {"key": "ASD3DB", "ndm": 3, "needsP": False, "dofRule": threeDOFs3D},
    # 10068: {"key": "ASD3DF",       "ndm": 3, "needsP": True, "dofRule": fourDOFs3D},
    # 10069: {"key": "ASD3DF",       "ndm": 3, "needsP": True, "dofRule": fourDOFs3D},
    # 10070: {"key": "ASD3DF",       "ndm": 3, "needsP": True, "dofRule": fourDOFs3D},
    # !!! 3D boundary absorbing END !!!
    17: {"key": "20_8_BrickUP", "ndm": 3, "needsP": True, "dofRule": twentyEightBrickDOFs},
}


# --------------------------------------------------------------------------------------------------------------
# MESH PARSING UTILITIES
# --------------------------------------------------------------------------------------------------------------
def parseElementsFromMsh(meshFile):
    """
    Parse the $Elements section from a Gmsh .msh file.

    Returns:
        list of dicts, each with:
            {
                "id": int,
                "type": int,
                "group": int,
                "nodes": list[int]
            }
    """
    elements = []

    with open(meshFile) as f:
        lines = f.readlines()

    inElements = False

    for line in lines:
        line = line.strip()

        if line == "$Elements":
            inElements = True
            continue

        elif line == "$EndElements":
            break

        if inElements:
            parts = line.split()

            if len(parts) > 4:
                try:
                    eleTag = int(parts[0])
                    elementType = int(parts[1])
                    numTags = int(parts[2])
                    phyGroup = int(parts[4])
                    ns = [int(n) for n in parts[3 + numTags:]]

                    elements.append(
                        {
                            "id": eleTag,
                            "type": elementType,
                            "group": phyGroup,
                            "nodes": ns
                        }
                    )

                except (ValueError, IndexError):
                    continue

    return elements


def getBoundaryNodesFromMsh(meshFile, phyGroupIDs=None, dim=None):
    """
    returns the nodes belonging to elements of a specified geometric dimension
    (1=line, 2=surface, 3=volume); if no dimension is given, defaults to the
    'before last' element type (for backward compatibility).

    :param meshFile: (str) path to .msh file
    :param phyGroupIDs: (list[int]|None) if given, restricts nodes to these (or this) physical group(s)
    :param dim: (int, optional) geometric dimension to extract (1=line, 2=surface, 3=volume)

    :return: (set) node tags associated with the chosen element type(s)
    """

    # empty list mean "return empty"
    if not phyGroupIDs:
        return set()

    phyGroupSet = None if phyGroupIDs is None else set(phyGroupIDs)

    # map common element types to their geometric dimensions
    eleTypeToDim = {
        1: 1,    # 2-node line
        2: 2,    # 3-node triangle
        3: 2,    # 4-node quadrilateral
        4: 3,    # 4-node tetrahedron
        5: 3,    # 8-node hexahedron
        6: 3,    # 6-node prism
        7: 3,    # 5-node pyramid
        8: 1,    # 3-node quadratic line
        9: 2,    # 6-node quadratic triangle
        10: 2,   # 9-node quadratic quad
        11: 3,   # 10-node quadratic tetra
        16: 2,   # 8-node serendipity quad
        17: 3,   # 20-node serendipity hex
    }

    # step 1: collect element types from the mesh
    with open(meshFile) as f:
        lines = f.readlines()

    eleTypesRaw = []
    inElements = False

    for line in lines:
        line = line.strip()

        if line == "$Elements":
            inElements = True
            continue
        elif line == "$EndElements":
            break

        if inElements:
            parts = line.split()
            if len(parts) > 1:
                try:
                    eleType = int(parts[1])
                    eleTypesRaw.append(eleType)
                except ValueError:
                    continue

    # get distinct types in order of appearance
    distinctTypes = []
    for t in eleTypesRaw:
        if not distinctTypes or t != distinctTypes[-1]:
            distinctTypes.append(t)

    if not distinctTypes:
        raise RuntimeError(f"no elements found in {meshFile}")

    # step 2: determine which element types to target
    if dim is not None:
        # filter element types by requested dimension
        targetTypes = [t for t in distinctTypes if eleTypeToDim.get(t) == dim]
        if not targetTypes:
            raise ValueError(f"no elements of dimension {dim} found in {meshFile}")
    else:
        # default behavior: before-last distinct type
        eleTypeBL = distinctTypes[-2] if len(distinctTypes) >= 2 else distinctTypes[0]
        targetTypes = [eleTypeBL]

    # step 3: collect nodes from matching elements
    boundaryNodes = set()

    # with open(meshFile) as f:
    #     lines = f.readlines()

    inElements = False

    for line in lines:
        line = line.strip()

        if line == "$Elements":
            inElements = True
            continue
        elif line == "$EndElements":
            break

        if inElements:
            parts = line.split()
            if len(parts) >= 7:
                try:
                    eleType = int(parts[1])
                    phyGroup = int(parts[4])

                    groupOK = (phyGroupSet is None) or (phyGroup in phyGroupSet)

                    if eleType in targetTypes and groupOK:
                        nodesB = [int(n) for n in parts[5:]]
                        boundaryNodes.update(nodesB)
                except ValueError:
                    continue

    return boundaryNodes


def parseNodesFromMsh(meshFile, precision=6):
    """
    Parse the $Nodes section from a Gmsh .msh file.

    Parameters:
        meshFile (str): Path to the .msh file
        precision (int): Decimal rounding for node coordinates

    Returns:
        dict: {nodeTag: (xC, yC, zC)}
    """
    nodeCoords = {}
    with open(meshFile) as f:
        lines = f.readlines()

    inNodes = False
    for line in lines:
        line = line.strip()
        if line == "$Nodes":
            inNodes = True
            continue
        elif line == "$EndNodes":
            break

        if inNodes:
            parts = line.split()
            if len(parts) >= 4:
                try:
                    nodeTag = int(parts[0])
                    x, y, *z = map(float, parts[1:])
                    x = round(x, precision)
                    y = round(y, precision)
                    z_val = round(z[0], precision) if z else 0.0
                    nodeCoords[nodeTag] = (x, y, z_val)
                except ValueError:
                    continue

    return nodeCoords


def detectMaxPhyGroup(meshFile):
    """
    Scan a Gmsh .msh file and detect the maximum physical group ID
    present in the $Elements section.

    Parameters:
        meshFile (str): Path to the Gmsh .msh file.

    Returns:
        int: Maximum physical group ID found (0 if none).
    """
    maxPhyGroup = 0
    with open(meshFile) as f:
        lines = f.readlines()

    inElementSection = False
    for line in lines:
        line = line.strip()
        if line == "$Elements":
            inElementSection = True
            continue
        elif line == "$EndElements":
            break

        if inElementSection:
            parts = line.split()
            if len(parts) > 4:
                try:
                    elementType = int(parts[1])
                    phyGroup = int(parts[4])
                    # include both 2D and 3D element types
                    if elementType in (1, 101,  # newly added
                                       3, 103, 1003, 10031, 10032, 10033, 10034, 10035, 10,
                                       5, 105, 1005, 1055, 10051, 10052, 10053, 10054, 10055, 10056, 10057, 10058,
                                       10059, 10060, 10061, 10062, 10063, 10064, 10065, 10066, 10067,
                                       17):
                        if phyGroup > maxPhyGroup:
                            maxPhyGroup = phyGroup
                except (ValueError, IndexError):
                    continue
    return maxPhyGroup


def getElementsTagByType(elements_, targetTypes):
    return [el["id"] for el in elements_ if el["type"] in targetTypes]


def classifyChosenNodesByDOF(nodeList, nodeDOFs):
    """
    Classify an existing list of nodes according to their DOF count.

    nodeList : list of node tags (e.g. from getBoundaryNodesFromMsh)
    nodeDOFs : dict {nodeTag: dofCount}

    Returns dict {dofCount: [nodeTags]}
    """
    groups = {}
    for node in nodeList:
        dof = nodeDOFs.get(node)
        if dof is None:
            continue
        groups.setdefault(dof, []).append(node)
    return groups


class FuzzyFloat(float):
    """
    A float that compares equal within tolerance
    """
    __slots__ = ("tol",)

    def __new__(cls, value, tol):
        obj = float.__new__(cls, value)
        obj.tol = tol
        return obj

    def __eq__(self, other):
        return abs(float(self) - float(other)) < self.tol

    def __lt__(self, other):
        return float(self) < float(other) - self.tol

    def __le__(self, other):
        return float(self) <= float(other) + self.tol

    def __gt__(self, other):
        return float(self) > float(other) + self.tol

    def __ge__(self, other):
        return float(self) >= float(other) - self.tol


def _roundFunc(x_, tol=defaultTol):
    # round a coordinate to the decimal precision implied by the tolerance
    return round(x_, int(abs(np.log10(tol))))


# ---------------------------------------------------------------------------------------------------------------
# Node selection helper functions (using coordinates)
# ---------------------------------------------------------------------------------------------------------------
def selectNodes(condition, nodeCoords, tol=defaultTol, debug=False):
    """
    Select nodes satisfying a user-defined Boolean condition on (x, y, z).

    Args:
        condition: callable (x, y, z) --> bool
        nodeCoords (dict): mapping nodeTag --> (x, y, z)
        tol: numerical tolerance for coordinate rounding
        debug: if True, prints the number of matched nodes

    Returns:
        list of node IDs satisfying the condition.

    Example:
        selectNodes(lambda x, y, z: x == 0.083333 and y < 0.25)
    """
    selected = []
    for n, (x_, y_, z_) in nodeCoords.items():
        xR = _roundFunc(x_, tol)
        yR = _roundFunc(y_, tol)
        zR = _roundFunc(z_, tol)
        xF = FuzzyFloat(xR, tol)
        yF = FuzzyFloat(yR, tol)
        zF = FuzzyFloat(zR, tol)
        try:
            if condition(xF, yF, zF):
                selected.append(n)
        except (ValueError, TypeError):
            continue

    if debug:
        print(f"Matched {len(selected)} nodes for condition {condition}")
    return selected


def writeMainTclGlobal(tclRootDir, modelName,
                       damp, fLower, fHigher, gamma, beta,
                       orderedSections=None):
    """
    Create a global main.tcl in TCL-Files/ that sources the subfiles
    inside the model-specific folder (e.g., model4/).

    Parameters:
        tclRootDir (str): Path to 'TCL-Files' directory.
        modelName (str): Model folder name (e.g., 'model4').
        damp (float): damping value considered
        fLower (float): lower Rayleigh frequency considered
        fHigher (float): higher Rayleigh frequency considered
        gamma (float): Rayleigh gamma coefficient
        beta (float): Rayleigh beta coefficient
        orderedSections (list[str], optional): Custom ordering of sections.
            Default order: ['modelHeader', 'nodes', 'elements', 'fixity', 'equalDOF'].
    """
    tol = 1.0e-5
    maxNumIter = 25
    printFlag = 1

    omega1 = 2 * np.pi * fLower
    omega2 = 2 * np.pi * fHigher

    a0 = 2 * damp * omega1 * omega2 / (omega1 + omega2)
    a1 = 2 * damp / (omega1 + omega2)

    os.makedirs(tclRootDir, exist_ok=True)
    modelDir = os.path.join(tclRootDir, modelName)

    if not os.path.isdir(modelDir):
        raise FileNotFoundError(f"Model folder '{modelDir}' not found.")

    if orderedSections is None:
        orderedSections = ['modelHeader', 'nodes', 'elements', 'fixity', 'equalDOF']

    # collect all .tcl files in the model folder
    tclFiles = [f_ for f_ in sorted(os.listdir(modelDir)) if f_.endswith(".tcl")]

    # order by logical prefix
    orderedFiles = []
    for prefix in orderedSections:
        # add files matching this prefix (case-insensitive)
        orderedFiles.extend([f_ for f_ in tclFiles if f_.lower().startswith(prefix.lower())])

    # add any remaining files (not matched by known prefixes)
    orderedFiles.extend([f_ for f_ in tclFiles if f_ not in orderedFiles])

    # path to the global main.tcl
    mainPath = os.path.join(tclRootDir, "mainInit.tcl")

    with open(mainPath, "w") as f_:
        f_.write("# ============================================================\n")
        f_.write(f"# mainInit.tcl for {modelName}\n")
        # f_.write("# loaded automatically from/by Python\n")
        f_.write("# ============================================================\n\n")
        # f_.write(f"puts '==== Running main.tcl for {modelName} ===='\n\n')

        f_.write(f"set a0 {round(a0, 6)}\n")
        f_.write(f"set a1 {round(a1, 6)}\n")
        f_.write(f"set gamma {gamma}\n")
        f_.write(f"set beta {beta}\n")

        f_.write(f"# timeSeries Path $tsX - filePath 'vx_record.txt' - factor 1.0\n")
        f_.write(f"# timeSeries Path $tsY - filePath 'vy_record.txt' - factor 1.0\n\n")

        # automatically source subfiles inside model folder
        f_.write(f"# writing main code HERE\n")

        f_.write(f"wipe\n"
                 f"model BasicBuilder -ndm 2 -ndf 3\n")

        f_.write("\n")

        f_.write("constraints Transformation\n")
        f_.write("# Plain\n")
        f_.write("# Penalty 1.e18 1.e18\n")
        f_.write("# Lagrange\n")
        f_.write("# Transformation\n")

        f_.write("numberer RCM\n")
        f_.write("# Plain\n")

        f_.write("system ProfileSPD\n")
        f_.write("# BandGeneral\n")
        f_.write("# BandSPD\n")
        f_.write("# ProfileSPD\n")
        f_.write("# SparseGeneral\n")
        f_.write("# UmfPack\n")
        f_.write("# SparseSPD\n")

        f_.write(f"test NormDispIncr {tol} {maxNumIter} {printFlag}\n")

        f_.write(f"algorithm Newton\n")
        f_.write("# Linear\n")
        f_.write("# Newton\n")
        f_.write("# NewtonLineSearch $ratio\n")
        f_.write("# ModifiedNewton\n")
        f_.write("# KrylovNewton\n")
        f_.write("# BFGS $count\n")
        f_.write("# Broyden $count\n")

        f_.write("integrator LoadControl 1.0\n")
        f_.write("analysis Static\n\n")

        f_.write("\n\n\n\n")

        f_.write("constraints Transformation\n")
        f_.write("# Plain\n")
        f_.write("# Penalty 1.e18 1.e18\n")
        f_.write("# Lagrange\n")
        f_.write("# Transformation\n")

        f_.write("numberer RCM\n")
        f_.write("# Plain\n")

        f_.write("system ProfileSPD\n")
        f_.write("# BandGeneral\n")
        f_.write("# BandSPD\n")
        f_.write("# ProfileSPD\n")
        f_.write("# SparseGeneral\n")
        f_.write("# UmfPack\n")
        f_.write("# SparseSPD\n")

        f_.write(f"test NormDispIncr {tol} {maxNumIter} {printFlag}\n")

        f_.write(f"algorithm Newton\n")
        f_.write("# Linear\n")
        f_.write("# Newton\n")
        f_.write("# NewtonLineSearch $ratio\n")
        f_.write("# ModifiedNewton\n")
        f_.write("# KrylovNewton\n")
        f_.write("# BFGS $count\n")
        f_.write("# Broyden $count\n")

        f_.write("integrator LoadControl 1.0\n")
        f_.write("analysis Static\n\n")

        f_.write("\n")

        # more details HERE (link down) for the selection of analysis commands
        # https://opensees.berkeley.edu/OpenSees/manuals/usermanual/toc187244.htm

        # f_.write("constraints Transformation\n")
        # - Plain
        # - Penalty
        # - Lagrange
        # - Transformation
        #

        # f_.write("numberer RCM\n")
        # - Plain
        # - RCM
        #

        # f_.write("system ProfileSPD\n")
        # - BandGeneral
        # - BandSPD
        # - ProfileSPD
        # - SparseGeneral
        # - UmfPack
        # - SparseSPD
        #

        # f_.write(f"test NormUnbalance {tol} {maxNumIter} {printFlag}\n")
        # - NormUnbalance
        # - NormDispIncr
        # - EnergyIncr

        # f_.write(f"algorithm Newton\n")
        # - Linear
        # - Newton
        # - NewtonLineSearch $ratio # HERE we MUST define the ratio (see Berkeley website for more info)
        # - ModifiedNewton
        # - KrylovNewton
        # - BFGS $count # HERE we MUST define the count int (see Berkeley website for more info)
        # - Broyden # HERE we MUST define the count int (see Berkeley website for more info)
        #

        # f_.write("integrator LoadControl 1.0\n")
        # A) For static analysis
        #   - LoadControl $dLambda1 <$Jd $minLambda $maxLambda>
        #   - DisplacementControl $nodeTag $dofTag $dU1 <$Jd $minDu $maxDu>
        #   - MinUnbalDispNorm $dLambda11 <$Jd $minLambda $maxLambda>
        #   - ArcLength $arcLength $alpha

        # B) For transient analysis
        #   - Newmark $gamma $beta
        #   - HHT $gamma <$alphaM $betaK $betaKInit $betaKComm>
        #

        # f_.write("analysis Static\n\n")
        # Transient
        # VariableTransient

        # f_.write(f' puts "==== {modelName} TCL model loaded successfully ===="\n')

    print(f"Global main.tcl written at: {mainPath}")
    print("Contains source calls for:")
    for f_ in orderedFiles:
        print(f"   • {modelName}/{f_}")


def soilFaceNodesAroundPile(pileNode, elements_, soilTypes_, nodeCoords_,
                            verticalAxis="y", tol_=1e-6):
    """
    For a given pile node, find all soil nodes that belong to the horizontal
    faces of soil elements that surround the pile at that depth.

    Works for any vertical axis: "x", "y", or "z".

    Parameters
    ----------
    pileNode : int
        Pile node ID.
    elements_ : list[dict]
        All mesh elements.
    soilTypes_ : set[int]
        Soil element types (3D bricks) to consider.
    nodeCoords_ : dict[int, tuple]
        Mapping nodeTag -> (x, y, z).
    verticalAxis : {"x","y","z"}
        Which coordinate is considered vertical.
    tol_ : float
        Tolerance for matching coordinates.

    Returns
    -------
    list[int]
        Sorted the list of soil node IDs on faces surrounding this pile node
        at the given depth.
    """

    axisIndex = {"x": 0, "y": 1, "z": 2}
    v = axisIndex[verticalAxis]  # vertical axis index
    # the two horizontal axes
    h1, h2 = [i for i in (0, 1, 2) if i != v]

    # coordinates of the pile node
    P = nodeCoords_[pileNode]
    pv = P[v]  # vertical coordinate
    ph1 = P[h1]  # horizontal coord 1
    ph2 = P[h2]  # horizontal coord 2

    face_nodes = set()

    for el in elements_:
        if el["type"] not in soilTypes_:
            continue

        el_nodes = el["nodes"]

        # vertical coordinates of this element
        vs = [nodeCoords_[n][v] for n in el_nodes]
        v_min = min(vs)
        v_max = max(vs)

        # quick reject: pile depth not within element's vertical span
        if pv < v_min - tol_ or pv > v_max + tol_:
            continue

        # nodes on the horizontal face at v ≈ pv
        face = [
            n for n in el_nodes
            if abs(nodeCoords_[n][v] - pv) <= tol_
        ]
        if len(face) < 3:
            # less than 3 nodes -> cannot form a meaningful face
            continue

        # horizontal coordinates for this face
        h1s = [nodeCoords_[n][h1] for n in face]
        h2s = [nodeCoords_[n][h2] for n in face]

        h1_min, h1_max = min(h1s), max(h1s)
        h2_min, h2_max = min(h2s), max(h2s)

        # check if the pile horizontal position lies inside this face
        if (ph1 < h1_min - tol_ or ph1 > h1_max + tol_ or
                ph2 < h2_min - tol_ or ph2 > h2_max + tol_):
            continue

        # this element contributes nodes on the surrounding face
        face_nodes.update(face)

    # return the sorted list for reproducibility / debugging
    return sorted(face_nodes)


def detectSoilGroups(elements, has3D,
                     soil2D_types=None,
                     soil3D_types=None):
    """
    Decide which element types are considered 'soil', and
    return both the active soilTypes set and the physical groups
    that contain soil elements.

    Parameters
    ----------
    elements : list[dict]
        Parsed elements from the .msh file.
    has3D : bool
        True if the mesh is treated as 3D (from filterElementsByDIM).
    soil2D_types : set[int] or None
        Optional override for 2D soil element types.
    soil3D_types : set[int] or None
        Optional override for 3D soil element types.

    Returns
    -------
    soilTypes : set[int]
        The element types that are considered soil in this run.
    soilGroups : set[int]
        Physical group IDs that contain soil elements.
    """
    if soil2D_types is None:
        soil2D_types = {3, 10, 103, 1003}
    if soil3D_types is None:
        soil3D_types = {5, 17, 105, 1005, 1055}

    soilTypes = soil3D_types if has3D else soil2D_types

    soilGroups = {el["group"] for el in elements
                  if el["type"] in soilTypes}

    return soilTypes, soilGroups


def classifySoilAndPileNodes(elements, soilTypes, beam3DGrp):
    """
    Extract the soil node set and the pile node set.

    Parameters
    ----------
    elements : list[dict]
        Parsed and filtered mesh elements.
    soilTypes : set[int]
        Element types that we consider 'soil'.
    beam3DGrp : set[int]
        Physical groups associated with 3D beam (pile) elements.

    Returns
    -------
    soilNodeSet : set[int]
        All nodes belonging to soil elements.
    pileNodeSet : set[int]
        All nodes belonging to pile (3D beam) elements.
    """

    # nodes from soil elements
    soilNodeSet = {
        n for el in elements if el["type"] in soilTypes for n in el["nodes"]
    }

    # elements that are 3D beams belonging to selected groups
    pileElemts = [
        el for el in elements
        if el["type"] == 101 and el["group"] in beam3DGrp
    ]

    # nodes from pile elements
    pileNodeSet = {
        n for el in pileElemts for n in el["nodes"]
    }

    return soilNodeSet, pileNodeSet


def groupNodesByCoordinate(nodeSet, nodeCoords, axis="y", tol=1e-6):
    """
    Group node tags by a rounded coordinate key.

    Parameters
    ----------
    nodeSet : iterable[int]
        Collection of node IDs to group.
    nodeCoords : dict[int, tuple]
        Mapping nodeTag --> (x, y, z).
    axis : str
        One of "x", "y", "z".
        It determines which coordinate is used.
    tol : float
        Rounding tolerance.

    Returns
    -------
    dict[float, list[int]]
        Mapping coordinateKey --> list of nodeTags.
    """

    # axis index
    idx = {"x": 0, "y": 1, "z": 2}[axis]

    groups = {}
    for n in nodeSet:
        coord = nodeCoords[n][idx]
        key = round(coord / tol) * tol
        groups.setdefault(key, []).append(n)

    return groups


def buildSSImap(pileNodeSet, elements, soilTypes, nodeCoords,
                verticalAxis="y", tol_=1e-6):
    """
    Build a mapping: pileNode --> soil face nodes surrounding it.

    Parameters
    ----------
    pileNodeSet : set[int]
        Set of node IDs belonging to pile (2D/3D beam) elements.
    elements : list[dict]
        All mesh elements.
    soilTypes : set[int]
        Soil element types used to guide the search.
    nodeCoords : dict[int, tuple]
        Node coordinates from parseNodesFromMsh.
    verticalAxis : {"x","y","z"}
        Which coordinate is considered vertical.
    tol_ : float
        Tolerance for geometric checks.

    Returns
    -------
    dict[int, list[int]]
        Mapping: pile node ID --> list of surrounding soil node IDs.
    """

    SSI_map = {}

    for pNode in pileNodeSet:
        ring_nodes = soilFaceNodesAroundPile(
            pNode,
            elements,
            soilTypes,
            nodeCoords,
            verticalAxis=verticalAxis,
            tol_=tol_,
        )
        SSI_map[pNode] = ring_nodes

    return SSI_map


def getAndSortGroupNodes(meshFile, phyGroupID, nodeCoords, axes=("x", "y", "z"), dim=None):
    """
    Extract nodes belonging to a physical group and sort them
    according to a user-specified sequence of axes.

    Parameters
    ----------
    meshFile : str
        Path to the .msh file.
    phyGroupID : int
        Physical group ID to extract nodes from
    nodeCoords : dict[int, tuple]
        Mapping nodeTag --> (x, y, z).
    axes : tuple[str]
        Sequence of axes to sort by, each in {"x","y","z"}
        Example: ("x", "z"), ("y"), ("x","y","z")
    dim : int or None
        If provided, restrict nodes to entities of this dimension
        If None, auto-detect from the .msh file.

    Returns
    -------
    list[int]
        The sorted node IDs.
    """

    # step 1: extract raw group nodes
    rawNodes = getBoundaryNodesFromMsh(meshFile, phyGroupIDs=[phyGroupID], dim=dim)

    # step 2: sort according to user-defined axis sequence
    sortedNodes = rawNodes
    for ax in axes:
        if ax == "x":
            sortedNodes = sortNodesByX(sortedNodes, nodeCoords)
        elif ax == "y":
            sortedNodes = sortNodesByY(sortedNodes, nodeCoords)
        elif ax == "z":
            sortedNodes = sortNodesByZ(sortedNodes, nodeCoords)

    return sortedNodes


def summarizeNodeDOFs(nodeDOFs):
    """
    Prints a clean, automatic summary of DOF categories.
    Does not modify any data structures.
    """
    print("\n------------------------------------------------------------------------------------------")
    print(" Node DOF Summary")
    print("------------------------------------------------------------------------------------------")

    if not nodeDOFs:
        print("No nodes found.")
        print("------------------------------------------------------------------------------------\n")
        return

    uniqueDOFs = sorted(set(nodeDOFs.values()))
    print(f"Total nodes detected: {len(nodeDOFs)}\n")

    dofLabels = {
        2: "u, v (2D soils / ASD boundaries)",
        3: "u, v, p   or   u, v, w (UP soils / 3D solids)",
        4: "u, v, w, p (3D UP solids)",
        6: "u, v, w, rx, ry, rz (3D beams)"
    }

    for dof in uniqueDOFs:
        nodesOfThisDOF = [n for n, d in nodeDOFs.items() if d == dof]
        label = dofLabels.get(dof, "")
        print(f"  {dof}-DOF nodes: {len(nodesOfThisDOF):6d}   {label}")

    print("------------------------------------------------------------------------------------------\n")


def countINTBraces(text):
    # find the boundaries
    start = text.find('{')
    end = text.find('}', start)
    if start == -1 or end == -1:
        return 0

    # extract the content inside the braces
    inside = text[start + 1:end]

    # split by commas and clean each piece
    items = [x.strip() for x in inside.split(',') if x.strip()]

    return len(items)


def computeSoilBoundingBox(soilNodeSet, nodeCoords):
    xs = [nodeCoords[n][0] for n in soilNodeSet]
    ys = [nodeCoords[n][1] for n in soilNodeSet]
    zs = [nodeCoords[n][2] for n in soilNodeSet]

    return {
        "xMin": min(xs), "xMax": max(xs),
        "yMin": min(ys), "yMax": max(ys),
        "zMin": min(zs), "zMax": max(zs),
    }


def selectBuriedStructuralNodes(structuralNodeSet, soil_bbox, nodeCoords, tol):
    buried = set()
    for n in structuralNodeSet:
        x, y, z = nodeCoords[n]
        if (soil_bbox["xMin"] - tol <= x <= soil_bbox["xMax"] + tol and
                soil_bbox["yMin"] - tol <= y <= soil_bbox["yMax"] + tol and
                soil_bbox["zMin"] - tol <= z <= soil_bbox["zMax"] + tol):
            buried.add(n)
    return buried


# test
s = "Transfinite Curves {1, 3, 4, 5};"
print(countINTBraces(s))


def isPointInTetrahedron(point, tet_nodes, nodeCoords):
    """
    Check if a point is inside a tetrahedron.

    INPUTS:
    -------
    point : numpy array (3),
        The point coordinates [x, y, z]

    tet_nodes : list of 4 integers
        The 4 node IDs forming the tetrahedron

    nodeCoords : dict
        Node coordinates {nodeID: (x, y, z)}

    OUTPUTS:
    --------
    bool : True if point is inside tetrahedron, False otherwise

    HOW IT WORKS:
    -------------
    Uses barycentric coordinates. If all 4 barycentric coordinates are >= 0,
    the point is inside (or on the boundary of) the tetrahedron.
    """

    # Get coordinates of the 4 tetrahedron vertices
    v0 = np.array(nodeCoords[tet_nodes[0]])
    v1 = np.array(nodeCoords[tet_nodes[1]])
    v2 = np.array(nodeCoords[tet_nodes[2]])
    v3 = np.array(nodeCoords[tet_nodes[3]])

    # Compute vectors
    vec0 = v1 - v0
    vec1 = v2 - v0
    vec2 = v3 - v0
    # vecp = point - v0

    # Compute dot products
    dot00 = np.dot(vec0, vec0)
    dot01 = np.dot(vec0, vec1)
    dot02 = np.dot(vec0, vec2)
    dot11 = np.dot(vec1, vec1)
    dot12 = np.dot(vec1, vec2)
    dot22 = np.dot(vec2, vec2)
    # dot0p = np.dot(vec0, vecp)
    # dot1p = np.dot(vec1, vecp)
    # dot2p = np.dot(vec2, vecp)

    # Compute matrix determinant (6x volume of tetrahedron)
    M = np.array([
        [dot00, dot01, dot02],
        [dot01, dot11, dot12],
        [dot02, dot12, dot22]
    ])

    det = np.linalg.det(M)

    # Check for degenerate tetrahedron
    if abs(det) < 1e-12:
        return False

    # Solve for barycentric coordinates
    # We use a simplified check: compute signed volumes
    def signedVolume(a, b, c, d):
        """Compute signed volume of tetrahedron abcd"""
        mat = np.column_stack([b - a, c - a, d - a])
        return np.linalg.det(mat) / 6.0

    V = signedVolume(v0, v1, v2, v3)
    if abs(V) < 1e-12:
        return False  # Degenerate tetrahedron

    V0 = signedVolume(point, v1, v2, v3)
    V1 = signedVolume(v0, point, v2, v3)
    V2 = signedVolume(v0, v1, point, v3)
    V3 = signedVolume(v0, v1, v2, point)

    # Barycentric coordinates
    u0 = V0 / V
    u1 = V1 / V
    u2 = V2 / V
    u3 = V3 / V

    # Check if all barycentric coordinates are >= -tolerance
    tol = -1e-6  # Small negative tolerance for numerical errors
    return u0 >= tol and u1 >= tol and u2 >= tol and u3 >= tol


# ==============================================================================
# decompose 8-node brick into 5 tetrahedra
# ==============================================================================

def decomposeBrickIntoTetrahedra(brickNodes):
    """
    Decompose an 8-node brick into 5 tetrahedra.

    INPUTS:
    -------
    brickNodes : list of 8 integers
        The 8 node IDs of the brick element, ordered as:

              7--------6
             /|       /|
            / |      / |
           4--------5  |
           |  3-----|--2
           | /      | /
           |/       |/
           0--------1

    OUTPUTS:
    --------
    tetrahedra : list of 5 lists
        Each inner list contains 4 node IDs forming a tetrahedron

    DECOMPOSITION SCHEME:
    ---------------------
    There are multiple ways to decompose a brick into tetrahedra.
    We use a standard scheme that creates 5 tetrahedra:

    Tet 1: [0, 1, 2, 5]
    Tet 2: [0, 2, 7, 5]
    Tet 3: [0, 2, 3, 7]
    Tet 4: [0, 5, 7, 4]
    Tet 5: [2, 7, 5, 6]
    """

    # Extract node IDs
    n0, n1, n2, n3, n4, n5, n6, n7 = brickNodes

    # Define 5 tetrahedra
    tetrahedra = [
        [n0, n1, n2, n5],
        [n0, n2, n7, n5],
        [n0, n2, n3, n7],
        [n0, n5, n7, n4],
        [n2, n7, n5, n6]
    ]

    return tetrahedra


# ==============================================================================
# find tetrahedron containing pile node
# ==============================================================================

def findTetrahedronForPileNode(pileNode, nodeCoords, elements, soilTypes, searchRadius=5.0):
    """
    Find the tetrahedron (4 nodes) from nearby soil bricks that contains the pile node.

    PURPOSE:
    --------
    For 8-node brick soil elements, we need to:
    1. Find nearby brick elements
    2. Decompose each brick into 5 tetrahedra
    3. Test which tetrahedron contains the pile node
    4. Return those 4 nodes for ASDEmbeddedNodeElement

    INPUTS:
    -------
    pileNode : int
        The pile node ID

    nodeCoords : dict
        Node coordinates {nodeID: (x, y, z)}

    elements : list of dict
        All mesh elements

    soilTypes : set of int
        Soil element types (e.g., {5, 17, 105})

    searchRadius : float
        How far to search for soil elements (meters)
        Default: 5.0 m

    OUTPUTS:
    --------
    tetNodes : list of 4 integers or None
        The 4 node IDs forming the tetrahedron that contains the pile node.
        Returns None if no containing tetrahedron found.

    EXAMPLE:
    --------
    # >>> tetNodes1 = findTetrahedronForPileNode(1001, nodeCoords, elements, {5, 17})
    # >>> if tetNodes1:
    # >>>     print(f"Found tetrahedron: {tetNodes1}")
    # >>> else:
    # >>>     print("No tetrahedron found!")
    """

    # Get pile node coordinates
    pileCoord = np.array(nodeCoords[pileNode])

    # Find all soil brick elements
    soilBricks = [el for el in elements if el['type'] in soilTypes]

    # Search for containing tetrahedron
    for brick in soilBricks:
        # Get brick nodes (should be 8 nodes)
        brickNodes = brick['nodes']

        if len(brickNodes) != 8:
            print(f"WARNING: Soil element {brick['id']} has {len(brickNodes)} nodes, expected 8. Skipping.")
            continue

        # Compute brick centroid to check distance
        brickCoords = [nodeCoords[n] for n in brickNodes]
        centroid = np.mean(brickCoords, axis=0)
        distance = np.linalg.norm(pileCoord - centroid)

        # Skip if brick is too far
        if distance > searchRadius:
            continue

        # Decompose brick into 5 tetrahedra
        tetrahedra = decomposeBrickIntoTetrahedra(brickNodes)

        # Check each tetrahedron
        for tetNodes in tetrahedra:
            if isPointInTetrahedron(pileCoord, tetNodes, nodeCoords):
                # Found it!
                return tetNodes

    # No containing tetrahedron found
    return None


# ==============================================================================
# write ASDEmbeddedNodeElement for brick meshes
# ==============================================================================

def writeEmbeddedElementsForBricks(pileNodes, nodeCoords, elements, soilTypes,
                                   penaltyStiffness, searchRadius, outputFile):
    """
    Generate ASDEmbeddedNodeElement commands for pile nodes in 8-node brick mesh.

    PURPOSE:
    --------
    This is the modified version of writeEmbeddedElements specifically for
    8-node brick soil elements. It automatically finds the correct 4 nodes
    (tetrahedron) for each pile node.

    INPUTS:
    -------
    pileNodes : set or list of int
        All pile node IDs

    nodeCoords : dict
        Node coordinates {nodeID: (x, y, z)}

    elements : list of dict
        All mesh elements

    soilTypes : set of int
        Soil element types (e.g., {5, 17, 105, 1005, 1055})

    penaltyStiffness : float
        Penalty parameter K (typical: E_soil * 1e4)

    searchRadius : float
        Search radius for soil elements (meters)

    outputFile : str
        Path to output TCL file

    OUTPUTS:
    --------
    nCreated : int
        Number of elements created

    EXAMPLE:
    --------
    # >>> nCreated1 = writeEmbeddedElementsForBricks(
    # ...     pileNodes={1001, 1002, 1003},
    # ...     nodeCoords=nodeCoords,
    # ...     elements=elements,
    # ...     soilTypes={5, 17, 105},
    # ...     penaltyStiffness=2e12,
    # ...     searchRadius=5.0,
    # ...     outputFile="embedded_pile_elements.tcl"
    # ... )
    # >>> print(f"Created {nCreated1} embedded elements")
    """

    eleTag = 9000000  # Start element IDs from high number
    nCreated = 0
    nFailed = 0

    print(f"  Processing {len(pileNodes)} pile nodes...")

    with open(outputFile, 'w') as f:
        f.write("# ==============================================================================================\n")
        f.write("# ASDEmbeddedNodeElement for Pile Nodes\n")
        f.write("# automatically finds tetrahedra from 8-node bricks\n")
        f.write("# ==============================================================================================\n\n")

        f.write(f"set K_penalty {penaltyStiffness:.6e}\n\n")

        for pileNode in sorted(pileNodes):
            # Find the tetrahedron containing this pile node
            tetNodes = findTetrahedronForPileNode(
                pileNode, nodeCoords, elements, soilTypes, searchRadius
            )

            if tetNodes is None:
                print(f"  WARNING: No tetrahedron found for pile node {pileNode}")
                nFailed += 1
                continue

            # Write the TCL command
            f.write(f"# Pile node {pileNode} embedded in tetrahedron {tetNodes}\n")
            f.write(f"element ASDEmbeddedNodeElement {eleTag} {pileNode}")

            # Write the 4 tetrahedron nodes
            for node in tetNodes:
                f.write(f" {node}")

            f.write(f" -K $K_penalty\n\n")

            eleTag += 1
            nCreated += 1

    print(f"  ✓ Created {nCreated} ASDEmbeddedNodeElement")
    if nFailed > 0:
        print(f"  Failed for {nFailed} pile nodes (increase searchRadius?)")

    return nCreated


def computePileNormal(pileNode, pileNodes, nodeCoords, verticalAxis='z'):
    """
    Compute outward normal vector for a pile node.

    For a vertical pile, this is the radial direction (perpendicular to pile axis).
    """

    axis_idx = {'x': 0, 'y': 1, 'z': 2}
    vert_idx = axis_idx[verticalAxis]
    horiz_indices = [i for i in [0, 1, 2] if i != vert_idx]

    # Get all pile node coordinates
    pileCoords = np.array([nodeCoords[n] for n in pileNodes])

    # Compute pile axis center (average horizontal position)
    center = np.mean(pileCoords[:, horiz_indices], axis=0)

    # Get this node's horizontal position
    thisCoord = np.array(nodeCoords[pileNode])
    thisHoriz = thisCoord[horiz_indices]

    # Vector from axis to this node (in horizontal plane)
    radial = thisHoriz - center

    # Normalize
    radial_norm = np.linalg.norm(radial)
    if radial_norm < 1e-10:
        # Node is on axis - use arbitrary radial direction
        radial_unit = np.array([1.0, 0.0])
    else:
        radial_unit = radial / radial_norm

    # Build 3D normal vector
    normal = np.zeros(3)
    normal[horiz_indices] = radial_unit
    # Vertical component is zero for cylinder

    return normal


def writeContactElements(pileNodes, nodeCoords, elements, soilTypes,
                         Kn, Kt, mu, verticalAxis, outputFile):
    """
    Generate TCL file with ZeroLengthContactASDimplex commands.

    PURPOSE:
    --------
    This creates the second layer of interface: friction, gap, and slip.
    Each pile node gets a contact element with friction coefficient mu.

    INPUTS:
    -------
    pileNodes : set or list of int
        All pile node IDs

    nodeCoords : dict
        Node coordinates

    elements : list of dict
        Element list

    soilTypes : set of int
        Soil element types

    Kn : float
        Normal stiffness (typical: E_soil * 1000)

    Kt : float
        Tangential stiffness (typical: E_soil * 100)

    mu : float
        Friction coefficient
        Typical: (2/3) * tan(phi_soil)
        For phi=35°: mu ≈ 0.47

    verticalAxis : str
        'x', 'y', or 'z'

    outputFile : str
        Path to output TCL file

    OUTPUTS:
    --------
    Creates a .tcl file with contact element commands
    Returns: number of elements created

    EXAMPLE:
    --------
    # >>> nCreated1 = writeContactElements(
    # ...     pileNodes={1001, 1002, 1003},
    # ...     nodeCoords=nodeCoords,
    # ...     elements=elements,
    # ...     soilTypes={5, 17},
    # ...     Kn=2e11,
    # ...     Kt=2e10,
    # ...     mu=0.47,
    # ...     verticalAxis='z',
    # ...     outputFile="contact_elements.tcl"
    # ... )
    """

    eleTag = 8000000  # Different range from embedded elements
    nCreated = 0

    # Get all soil nodes
    soilElements = [el for el in elements if el['type'] in soilTypes]
    allSoilNodes = set()
    for el in soilElements:
        allSoilNodes.update(el['nodes'])

    soilNodesList = sorted(list(allSoilNodes))
    soilCoords = np.array([nodeCoords[n] for n in soilNodesList])

    with open(outputFile, 'w') as f:
        f.write("# ================================================================================================\n")
        f.write("# ZeroLengthContactASDimplex for Pile Interface\n")
        f.write("# Adds friction, gap opening, slip behavior\n")
        f.write("# ===============================================================================================\n\n")

        f.write(f"set Kn {Kn:.6e}  ;# Normal stiffness\n")
        f.write(f"set Kt {Kt:.6e}  ;# Tangential stiffness\n")
        f.write(f"set mu {mu:.6f}      ;# Friction coefficient\n\n")

        for pileNode in sorted(pileNodes):
            # Get pile node coordinate
            pileCoord = np.array(nodeCoords[pileNode])

            # Find nearest soil node (simple approach)
            distances = np.linalg.norm(soilCoords - pileCoord, axis=1)
            nearestIdx = np.argmin(distances)
            nearestSoilNode = soilNodesList[nearestIdx]

            # Compute normal direction
            normal = computePileNormal(pileNode, pileNodes, nodeCoords, verticalAxis)

            # Write TCL command
            f.write(f"element zeroLengthContactASDimplex {eleTag} ")
            f.write(f"{pileNode} {nearestSoilNode} ")
            f.write(f"$Kn $Kt $mu ")  # ← Move BEFORE -orient
            f.write(f"-orient {normal[0]:.6f} {normal[1]:.6f} {normal[2]:.6f}\n\n")
            # f.write(f'-orient "from link direction"\n\n')

            eleTag += 1
            nCreated += 1

    print(f"[INFO] Created {nCreated} ZeroLengthContactASDimplex in {outputFile}")
    return nCreated


def generatePileInterfaceForBricks(pileNodes, nodeCoords, elements, soilTypes,
                                   E_soil, phi_soil, verticalAxis='z',
                                   searchRadius=5.0, outputDir='.'):
    """MAIN FUNCTION for generating pile interface."""

    import os

    print("\n" + "=" * 70)
    print("GENERATING PILE INTERFACE ELEMENTS (8-Node Brick Mesh)")
    print("=" * 70)

    K_penalty = E_soil * 1e1
    E_interface = 2000
    alpha = 5.0  # alpha in [1, 10]
    beta = 0.05  # [0.01, 0.2]
    Kn = alpha * E_interface
    Kt = beta * Kn
    mu = (2.0 / 3.0) * np.tan(np.radians(phi_soil))

    print(f"\nPile nodes: {len(pileNodes)}")
    print(f"Soil E: {E_soil / 1e6:.1f} MPa")
    print(f"Soil φ: {phi_soil:.1f}°")
    print(f"Interface μ: {mu:.3f}")
    print(f"Search radius: {searchRadius:.1f} m")

    embeddedFile = os.path.join(outputDir, "embeddedPileElements.tcl")
    contactFile = os.path.join(outputDir, "contactPileElements.tcl")

    print("\n[STEP 1] Generating ASDEmbeddedNodeElement...")
    nEmbedded = writeEmbeddedElementsForBricks(
        pileNodes, nodeCoords, elements, soilTypes,
        K_penalty, searchRadius, embeddedFile
    )

    print("\n[STEP 2] Generating ZeroLengthContactASDimplex...")
    nContact = writeContactElements(
        pileNodes, nodeCoords, elements, soilTypes,
        Kn, Kt, mu, verticalAxis, contactFile
    )

    print("\n" + "=" * 70)
    print("PILE INTERFACE GENERATION COMPLETE")
    print("=" * 70)
    print(f"ASDEmbeddedNodeElement:      {nEmbedded}")
    print(f"ZeroLengthContactASDimplex:  {nContact}")
    print(f"\nOutput files:")
    print(f"  - {embeddedFile}")
    print(f"  - {contactFile}")
    print("=" * 70 + "\n")

    return nEmbedded, nContact


def computeElementCentroid(elemNodes, nodeCoords):
    """
    Compute the centroid (center point) of an element.
    Goal: assign each element a representative point in space so as to estimate its depth
          and eventually compute the initial vertical effective stress

    Parameters:
    -----------
    elemNodes : list of int
        Node IDs of the element (e.g., [1, 609, 2318, 598, 589, 2302, 3234, 2294])
    nodeCoords : dict
        Dictionary mapping node ID to (x, y, z) coordinates

    Returns:
    --------
    tuple : (cx, cy, cz) centroid coordinates

    Example:
    --------
    # >>> nodes = [1, 609, 2318, 598, 589, 2302, 3234, 2294]
    # >>> centroid = computeElementCentroid(nodes, nodeCoords)
    # >>> print(centroid)
    (0.5, 0.5, -5.5)
    """
    coords = [nodeCoords[n] for n in elemNodes if n in nodeCoords]
    if not coords:
        return 0.0, 0.0, 0.0

    cx = sum(c[0] for c in coords) / len(coords)
    cy = sum(c[1] for c in coords) / len(coords)
    cz = sum(c[2] for c in coords) / len(coords) if len(coords[0]) > 2 else 0.0

    return cx, cy, cz


def computeInitialEffectiveStress(depth, gammaSat, gammaWater=10.0, waterTableDepth=0.0, gammaUnsat=None):
    """
    Compute initial effective vertical stress at a given depth.

    sigma'v0 = gamma' x depth (below water table)

    where gamma' = gammaSat - gammaWater (submerged unit weight)

    Parameters:
    -----------
    depth : float
        Depth below ground surface (positive value, in meters)
    gammaSat : float
        Saturated unit weight of soil (kN/m^3), e.g., 19.87 for Nevada Sand
    gammaWater : float
        Unit weight of water (kN/m^3), default = 10.0
    waterTableDepth : float
        Depth of water table below surface (m), default = 0.0 (at surface)

    Returns:
    --------
    float : Initial effective vertical stress σ'v0 (sigma'v0) in kPa

    Example:
    --------
    # >>> sigma = computeInitialEffectiveStress(depth=5.0, gammaSat=19.87)
    # >>> print(sigma)
    49.35  # kPa
    """
    if depth <= 0:
        return 1.0  # minimum to avoid division by zero

    gammaSub = gammaSat - gammaWater  # submerged unit weight

    # default: if you don't know unsat unit weight, fall back to gammaSat
    if gammaUnsat is None:
        gammaUnsat = gammaSat

    if depth <= waterTableDepth:
        # above water table: use total unit weight
        sigma_v0 = gammaUnsat * depth
    else:
        sigma_v0 = gammaUnsat * waterTableDepth + gammaSub * (depth - waterTableDepth)

    return max(sigma_v0, 1.0)  # minimum 1 kPa to avoid division issues


# ==============================================================================================================
# VARIABLE PERMEABILITY FUNCTIONS
# ==============================================================================================================

def generateVariablePermeabilityFiles(
        elements,
        nodeCoords,
        mainSoilTags,
        verticalAxis,
        outputDir,
        # material parameters (dict: matTag -> value)
        gamma_sat_dict,
        kInit_dict,
        gamma_water=10.0,
        waterTableDepth=0.0,
        surfaceElevation=0.0,
        # Shahir and Pak model parameters
        alpha=20.0,
        beta1=1.0,
        beta2=8.9,
):
    """
    Generate variable permeability TCL data file for SSPbrickUP elements.

    Based on Shahir & Pak (2009) / Rahmani & Pak (2012):
    Article: Dynamic behavior of pile foundations under cyclic loading in liquefiable soils
        k/k_init = 1 + (alpha - 1) * ru^beta
        where ru = Δu / σ'v0 (excess pore pressure ratio)

    This function generates ONLY the data file (variablePermeabilityData.tcl).
    For the analysis script, use generateAdaptiveAnalysisTcl().

    Parameters:
    -----------
    elements : list of dict
        Element list from parseElementsFromMsh()
    nodeCoords : dict
        Node coordinates {nodeId: (x, y, z)}
    mainSoilTags : dict
        Mapping physical group -> material tag
    verticalAxis : str
        'x', 'y', or 'z'
    outputDir : str
        Output directory for TCL files
    gamma_sat_dict : dict
        Saturated unit weight per material {matTag: gamma_sat in kN/m³}
        Example: {1: 19.87, 2: 20.41}
    kInit_dict : dict
        Initial permeability per material {matTag: k_init}
        Example: {1: 6.17e-06, 2: 3.77e-06}
    gamma_water : float
        Unit weight of water (kN/m³), default 10.0
    waterTableDepth : float
        Depth of water table below surface (m), default 0.0
    surfaceElevation : float
        Elevation of ground surface (m), default 0.0
    alpha : float
        Maximum permeability ratio at full liquefaction, default 20.0
    beta1 : float
        Exponent during pore pressure buildup, default 1.0
    beta2 : float
        Exponent during consolidation, default 8.9

    Returns:
    --------
    str : Path to generated varPermFile, or None if no SSPbrickUP elements found
    """

    print("\n" + "=" * 70)
    print("variable permeability data")
    print("based on Shahir & Pak (2009) / Rahmani & Pak (2012)")
    print("=" * 70)

    # find SSPbrickUP elements (type 1005)
    sspElements = [el for el in elements if el["type"] == 1005]
    print(f"\n[INFO] Found {len(sspElements)} SSPbrickUP elements")

    if not sspElements:
        print("[WARNING] No SSPbrickUP elements found. Skipping variable permeability generation.")
        return None

    # Determine axis index
    axisIdx = {"x": 0, "y": 1, "z": 2}[verticalAxis.lower()]

    # Print info
    print(f"[INFO] Surface elevation: {surfaceElevation:.2f} m")
    print(f"[INFO] Vertical axis: {verticalAxis}")
    print(f"[INFO] Water table depth: {waterTableDepth} m")
    for matTag, gamma_sat in gamma_sat_dict.items():
        gamma_sub = gamma_sat - gamma_water
        print(f"[INFO] Material {matTag}: γ_sat={gamma_sat} kN/m³, γ'={gamma_sub:.2f} kN/m³")

    # ========================================================================
    # generation of variablePermeabilityData.tcl
    # ========================================================================
    varPermFile = os.path.join(outputDir, "variablePermeabilityData.tcl")

    with open(varPermFile, "w") as f:
        # header
        f.write("# ============================================================================\n")
        f.write("# variable permeability data\n")
        f.write("# ============================================================================\n")
        f.write("# Based on Shahir & Pak (2009) / Rahmani & Pak (2012)\n")
        f.write("#\n")
        f.write("# Formula: k/k_init = 1 + (alpha - 1) * ru^beta\n")
        f.write("#   where ru = Δu / σ'v0 (excess pore pressure ratio)\n")
        f.write("#\n")
        f.write(f"# Soil parameters:\n")
        for matTag, gamma_sat in gamma_sat_dict.items():
            gamma_sub = gamma_sat - gamma_water
            f.write(f"#   material {matTag}: gamma_sat={gamma_sat} kN/m³, gamma'={gamma_sub:.2f} kN/m³\n")
        f.write(f"#   gamma_water = {gamma_water} kN/m³\n")
        f.write(f"#   surface elevation = {surfaceElevation:.2f} m\n")
        f.write(f"#   water table depth = {waterTableDepth} m\n")
        f.write("# ============================================================================\n\n")

        # Shahir & Pak parameters
        f.write("# parameters\n")
        f.write(f"set alpha  {alpha}     ;# maximum permeability ratio at full liquefaction\n")
        f.write(f"set beta1   {beta1}    ;# exponent during pore pressure buildup\n")
        f.write(f"set beta2   {beta2}    ;# exponent during consolidation\n\n")

        # Element range
        elemIds = sorted([el["id"] for el in sspElements])
        f.write("# SSPbrickUP element range\n")
        f.write(f"set firstSSPelem {min(elemIds)}\n")
        f.write(f"set lastSSPelem {max(elemIds)}\n")
        f.write(f"set numSSPelems {len(elemIds)}\n\n")

        # Element data header
        f.write("# ============================================================================\n")
        f.write("# element data\n")
        f.write("# ============================================================================\n\n")

        # process each element
        for el in sspElements:
            elemId = el["id"]
            nodes = el["nodes"]

            # Get material tag
            matTag = mainSoilTags.get(el["group"], 1)

            # Get material properties (with fallback to first available)
            if matTag in kInit_dict:
                kInit = kInit_dict[matTag]
            else:
                kInit = list(kInit_dict.values())[0]
                print(f"[WARNING] No kInit for material {matTag}, using default")

            if matTag in gamma_sat_dict:
                gamma_sat = gamma_sat_dict[matTag]
            else:
                gamma_sat = list(gamma_sat_dict.values())[0]
                print(f"[WARNING] No gamma_sat for material {matTag}, using default")

            # compute element centroid
            centroid = computeElementCentroid(nodes, nodeCoords)

            # compute depth
            elemVertCoord = centroid[axisIdx]
            depth = surfaceElevation - elemVertCoord

            # compute initial effective stress
            sigmaV0 = computeInitialEffectiveStress(depth, gamma_sat, gamma_water, waterTableDepth)

            # write element data
            nodeStr = " ".join(str(n) for n in nodes)
            f.write(f"# Element {elemId}: depth={depth:.2f}m, sigma_v0={sigmaV0:.2f}kPa, mat={matTag}\n")
            f.write(f"set elemNodes({elemId}) {{{nodeStr}}}\n")
            f.write(f"set elemKinit({elemId}) {kInit:.15e}\n")
            f.write(f"set sigmaV0({elemId}) {sigmaV0:.6f}\n")
            f.write(f"set ruPrev({elemId}) 0.0\n\n")

        # Write procedures
        f.write("# ============================================================================\n")
        f.write("# PROCEDURES\n")
        f.write("# ============================================================================\n\n")

        f.write("""proc getElementPWP {elemTag} {
    global elemNodes
    if {![info exists elemNodes($elemTag)]} { return 0.0 }
    set nodeList $elemNodes($elemTag)
    set sumPWP 0.0
    set count 0
    foreach nd $nodeList {
        if {[catch {set pwp [nodeVel $nd 4]} err]} { continue }
        set sumPWP [expr $sumPWP + $pwp]
        incr count
    }
    if {$count > 0} { return [expr $sumPWP / $count] }
    return 0.0
}

proc updateElementPermeability {elemTag} {
    global alpha beta1 beta2 sigmaV0 ruPrev elemKinit
    if {![info exists sigmaV0($elemTag)]} { return [list 0.0 1.0 0.0] }

    # STEP 1: Get pore pressure
    set pwp [getElementPWP $elemTag]

    # STEP 2: Calculate ru
    if {$sigmaV0($elemTag) > 0.0} {
        set ru [expr abs($pwp) / $sigmaV0($elemTag)]
    } else {
        set ru 0.0
    }
    if {$ru < 0.0} {set ru 0.0}
    if {$ru > 1.0} {set ru 1.0}

    # STEP 3: Calculate new permeability
    if {$ru >= $ruPrev($elemTag)} {
        set beta $beta1
    } else {
        set beta $beta2
    }
    if {$ru < 0.001} {
        set kRatio 1.0
    } else {
        set kRatio [expr 1.0 + ($alpha - 1.0) * pow($ru, $beta)]
    }
    set kNew [expr $elemKinit($elemTag) * $kRatio]

    # STEP 4: Update element
    setParameter -value $kNew -ele $elemTag xPerm
    setParameter -value $kNew -ele $elemTag yPerm
    setParameter -value $kNew -ele $elemTag zPerm
    set ruPrev($elemTag) $ru

    return [list $ru $kRatio $kNew]
}

proc updateAllPermeabilities {} {
    global firstSSPelem lastSSPelem
    for {set e $firstSSPelem} {$e <= $lastSSPelem} {incr e} {
        updateElementPermeability $e
    }
}

puts "\\[INFO\\] Variable permeability data loaded: $numSSPelems SSPbrickUP elements"
puts "\\[INFO\\] Parameters: alpha=$alpha, beta1=$beta1, beta2=$beta2"
""")

    print(f"[INFO] Generated: {varPermFile}")

    print("\n" + "=" * 70)
    print("variable permeability data generated")
    print("=" * 70)
    print(f"\nFile created: {varPermFile}")
    print("  - Element data (nodes, kInit, sigmaV0)")
    print("  - Procedures (getElementPWP, updateElementPermeability, updateAllPermeabilities)")
    print("\nUsage in main.tcl:")
    print(f"  source {varPermFile}")
    print("=" * 70 + "\n")

    return varPermFile


# ==============================================================================================================
# ADAPTIVE TIME STEPPING
# ==============================================================================================================

def writeAdaptiveAnalysisProcedure(f):
    """
    Write the adaptive time stepping TCL procedure to an open file handle.

    This procedure handles:
    - Automatic time step reduction on convergence failure
    - Time step recovery after consecutive successes
    - Minimum time step threshold to avoid infinite reduction
    - Progress reporting

    Parameters:
    -----------
    f : file handle
        Open file to write to
    """
    f.write("""
# ============================================================================
# ADAPTIVE TIME STEPPING PROCEDURE
# ============================================================================
# Features:
#   - Reduces dT on convergence failure (halves each time)
#   - Increases dT after N consecutive successes (doubles, up to dT_max)
#   - Stops if dT falls below dT_min
#   - Reports progress every 100 steps
#
# Usage:
#   set ok [adaptiveAnalyze $totalTime $dT_initial $dT_min $dT_max $N_success]
#   - totalTime:    total duration to analyze (s)
#   - dT_initial:   starting time step (s)
#   - dT_min:       minimum allowed time step (default: dT_initial/64)
#   - dT_max:       maximum allowed time step (default: dT_initial)
#   - N_success:    consecutive successes before increasing dT (default: 10)
# ============================================================================

proc adaptiveAnalyze {totalTime dT_initial {dT_min ""} {dT_max ""} {N_success 10}} {

    # set defaults if not provided
    if {$dT_min eq ""} {set dT_min [expr $dT_initial / 64.0]}
    if {$dT_max eq ""} {set dT_max $dT_initial}

    set dT $dT_initial
    set currentTime [getTime]
    set startTime $currentTime
    set targetTime [expr $currentTime + $totalTime]
    set successCount 0
    set totalSteps 0
    set reductions 0
    set increases 0

    puts ""
    puts "=============================================="
    puts "ADAPTIVE TIME STEPPING"
    puts "=============================================="
    puts "Start time:     [format %.4f $currentTime] s"
    puts "Target time:    [format %.4f $targetTime] s"
    puts "Duration:       $totalTime s"
    puts "Initial dT:     [format %.2e $dT_initial] s"
    puts "Min dT:         [format %.2e $dT_min] s"
    puts "Max dT:         [format %.2e $dT_max] s"
    puts "Success threshold: $N_success steps"
    puts "=============================================="
    puts ""

    set analysisStartT [clock seconds]

    while {$currentTime < [expr $targetTime - 1.0e-12]} {

        # don't overshoot the target time
        if {[expr $currentTime + $dT] > $targetTime} {
            set dT [expr $targetTime - $currentTime]
        }

        # try one step
        set ok [analyze 1 $dT]

        if {$ok == 0} {
            # SUCCESS
            set currentTime [getTime]
            incr successCount
            incr totalSteps

            # try to increase dT after N consecutive successes
            if {$successCount >= $N_success && $dT < [expr $dT_max - 1.0e-12]} {
                set dT_new [expr $dT * 2.0]
                if {$dT_new > $dT_max} {set dT_new $dT_max}
                if {$dT_new > [expr $dT + 1.0e-12]} {
                    set dT $dT_new
                    incr increases
                    puts "  t=[format %.4f $currentTime]s: increasing dT to [format %.2e $dT]"
                }
                set successCount 0
            }

            # progress report every 100 steps
            if {[expr $totalSteps % 100] == 0} {
                set elapsed [expr [clock seconds] - $analysisStartT]
                set pct [expr int(100.0 * ($currentTime - $startTime) / $totalTime)]
                puts "  Progress: $pct% | t=[format %.4f $currentTime]s | dT=[format %.2e $dT] | steps=$totalSteps | ${elapsed}s"
            }

        } else {
            # FAILURE - reduce time step
            set successCount 0
            set dT [expr $dT / 2.0]
            incr reductions

            puts "  t=[format %.4f $currentTime]s: no convergence, reducing dT to [format %.2e $dT]"

            # check if dT is too small
            if {$dT < $dT_min} {
                puts ""
                puts "ERROR: dT below minimum ([format %.2e $dT_min]). Analysis aborted."
                puts "  Total steps completed: $totalSteps"
                puts "  Time reached: [format %.4f $currentTime] s"
                puts ""
                return -1
            }
        }
    }

    set analysisEndT [clock seconds]
    set wallTime [expr $analysisEndT - $analysisStartT]

    # final report
    puts ""
    puts "=============================================="
    puts "ADAPTIVE ANALYSIS COMPLETE"
    puts "=============================================="
    puts "Final time:     [format %.4f $currentTime] s"
    puts "Total steps:    $totalSteps"
    puts "dT reductions:  $reductions"
    puts "dT increases:   $increases"
    puts "Final dT:       [format %.2e $dT] s"
    puts "Wall time:      $wallTime seconds"
    puts "=============================================="
    puts ""

    return 0
}

""")


def generateAdaptiveAnalysisTcl(
        outputDir,
        totalTime,
        dT_initial,
        dT_min=None,
        dT_max=None,
        N_success=10,
        # analysis setup parameters
        constraints_type="Transformation",
        test_type="NormDispIncr",
        test_tol=1.0e-3,
        test_iter=30,
        algorithm="KrylovNewton",
        numberer="RCM",
        system="UmfPack",
        integrator_gamma=0.5,
        integrator_beta=0.25,
        rayleigh_a0="$a0",
        rayleigh_a1="$a1",
        # optional: variable permeability
        useVariablePerm=False,
        permUpdateInterval=50,
        filename="dynamicAnalysis_adaptive.tcl"
):
    """
    Generate a TCL file for dynamic analysis with adaptive time stepping.

    Parameters:
    -----------
    outputDir : str
        Output directory for the TCL file
    totalTime : float
        Total analysis duration (seconds)
    dT_initial : float
        Initial time step (seconds)
    dT_min : float, optional
        Minimum allowed time step (default: dT_initial/64)
    dT_max : float, optional
        Maximum allowed time step (default: dT_initial)
    N_success : int
        Consecutive successes before increasing dT (default: 10)
    constraints_type : str
        Constraints handler type (default: "Transformation")
    test_type : str
        Convergence test type (default: "NormDispIncr")
    test_tol : float
        Convergence tolerance (default: 1.0e-3)
    test_iter : int
        Maximum iterations (default: 30)
    algorithm : str
        Solution algorithm (default: "KrylovNewton")
    numberer : str
        DOF numberer (default: "RCM")
    system : str
        System of equations (default: "UmfPack")
    integrator_gamma : float
        Newmark gamma (default: 0.5)
    integrator_beta : float
        Newmark beta (default: 0.25)
    rayleigh_a0 : str
        Rayleigh damping a0 (default: "$a0", assumes variable defined elsewhere)
    rayleigh_a1 : str
        Rayleigh damping a1 (default: "$a1", assumes variable defined elsewhere)
    useVariablePerm : bool
        Include variable permeability updates (default: False)
    permUpdateInterval : int
        Steps between permeability updates (default: 50)
    filename : str
        Output filename (default: "dynamicAnalysis_adaptive.tcl")

    Returns:
    --------
    str : Path to generated file
    """

    if dT_min is None:
        dT_min = dT_initial / 64.0
    if dT_max is None:
        dT_max = dT_initial

    outFile = os.path.join(outputDir, filename)

    with open(outFile, "w") as f:
        # header
        f.write("# !!!!!!!!!!!!!=======================================================================!!!!!!!!!!!!!\n")
        f.write("#                    DYNAMIC ANALYSIS WITH ADAPTIVE TIME STEPPING\n")
        f.write("# !!!!!!!!!!!!!=======================================================================!!!!!!!!!!!!!\n")
        f.write("#\n")
        f.write("# Features:\n")
        f.write("#   - Automatic time step reduction on convergence failure\n")
        f.write("#   - Time step recovery after consecutive successes\n")
        f.write("#   - Progress reporting\n")
        if useVariablePerm:
            f.write("#   - Variable permeability updates (Shahir & Pak model)\n")
        f.write("#\n")
        f.write("# ============================================================================\n\n")

        # write the adaptive procedure
        writeAdaptiveAnalysisProcedure(f)

        # analysis parameters
        f.write("# ============================================================================\n")
        f.write("# ANALYSIS PARAMETERS\n")
        f.write("# ============================================================================\n\n")
        f.write(f"set totalTime    {totalTime}       ;# total analysis duration (s)\n")
        f.write(f"set dT_initial   {dT_initial}   ;# initial time step (s)\n")
        f.write(f"set dT_min       {dT_min:.2e}   ;# minimum time step (s)\n")
        f.write(f"set dT_max       {dT_max:.2e}   ;# maximum time step (s)\n")
        f.write(f"set N_success    {N_success}          ;# successes before increasing dT\n\n")

        # analysis setup
        f.write("# ============================================================================\n")
        f.write("# ANALYSIS SETUP\n")
        f.write("# ============================================================================\n\n")
        f.write(f"constraints {constraints_type}\n")
        f.write(f"test {test_type} {test_tol} {test_iter} 1\n")
        f.write(f"algorithm {algorithm}\n")
        f.write(f"numberer {numberer}\n")
        f.write(f"system {system}\n")
        f.write(f"integrator Newmark {integrator_gamma} {integrator_beta}\n")
        f.write(f"rayleigh {rayleigh_a0} 0.0 {rayleigh_a1} 0.0\n")
        f.write("analysis Transient\n\n")

        # variable permeability wrapper (if enabled)
        if useVariablePerm:
            f.write("# ============================================================================\n")
            f.write("# ADAPTIVE ANALYSIS WITH VARIABLE PERMEABILITY\n")
            f.write("# ============================================================================\n\n")
            f.write(f"set permUpdateInterval {permUpdateInterval}\n\n")
            f.write("""# wrapper procedure that combines adaptive stepping with permeability updates
proc adaptiveAnalyzeWithPerm {totalTime dT_initial dT_min dT_max N_success permInterval} {
    global firstSSPelem lastSSPelem

    set dT $dT_initial
    set currentTime [getTime]
    set startTime $currentTime
    set targetTime [expr $currentTime + $totalTime]
    set successCount 0
    set totalSteps 0
    set reductions 0
    set increases 0
    set permUpdates 0
    set stepsSincePermUpdate 0

    puts ""
    puts "=============================================="
    puts "ADAPTIVE ANALYSIS + VARIABLE PERMEABILITY"
    puts "=============================================="
    puts "Start time:         [format %.4f $currentTime] s"
    puts "Target time:        [format %.4f $targetTime] s"
    puts "Initial dT:         [format %.2e $dT_initial] s"
    puts "Perm update every:  $permInterval steps"
    puts "=============================================="
    puts ""

    set analysisStartT [clock seconds]

    # output file for permeability evolution
    file mkdir results
    set permLog [open "results/permeability_evolution.csv" w]
    puts $permLog "Time,Steps,dT,Reductions,SampleRu"
    set sampleElem [expr ($firstSSPelem + $lastSSPelem) / 2]

    while {$currentTime < [expr $targetTime - 1.0e-12]} {

        # don't overshoot
        if {[expr $currentTime + $dT] > $targetTime} {
            set dT [expr $targetTime - $currentTime]
        }

        # try one step
        set ok [analyze 1 $dT]

        if {$ok == 0} {
            # SUCCESS
            set currentTime [getTime]
            incr successCount
            incr totalSteps
            incr stepsSincePermUpdate

            # update permeabilities periodically
            if {$stepsSincePermUpdate >= $permInterval} {
                updateAllPermeabilities
                incr permUpdates
                set stepsSincePermUpdate 0
            }

            # try to increase dT
            if {$successCount >= $N_success && $dT < [expr $dT_max - 1.0e-12]} {
                set dT_new [expr $dT * 2.0]
                if {$dT_new > $dT_max} {set dT_new $dT_max}
                if {$dT_new > [expr $dT + 1.0e-12]} {
                    set dT $dT_new
                    incr increases
                    puts "  t=[format %.4f $currentTime]s: increasing dT to [format %.2e $dT]"
                }
                set successCount 0
            }

            # progress report
            if {[expr $totalSteps % 100] == 0} {
                set elapsed [expr [clock seconds] - $analysisStartT]
                set pct [expr int(100.0 * ($currentTime - $startTime) / $totalTime)]

                # get sample ru value
                global ruPrev
                if {[info exists ruPrev($sampleElem)]} {
                    set sampleRu $ruPrev($sampleElem)
                    puts "  Progress: $pct% | t=[format %.4f $currentTime]s | dT=[format %.2e $dT] | ru=[format %.3f $sampleRu] | ${elapsed}s"
                    puts $permLog "[format %.4f $currentTime],$totalSteps,[format %.2e $dT],$reductions,[format %.4f $sampleRu]"
                } else {
                    puts "  Progress: $pct% | t=[format %.4f $currentTime]s | dT=[format %.2e $dT] | ${elapsed}s"
                    puts $permLog "[format %.4f $currentTime],$totalSteps,[format %.2e $dT],$reductions,0.0"
                }
                flush $permLog
            }

        } else {
            # FAILURE
            set successCount 0
            set dT [expr $dT / 2.0]
            incr reductions

            puts "  t=[format %.4f $currentTime]s: no convergence, reducing dT to [format %.2e $dT]"

            if {$dT < $dT_min} {
                puts ""
                puts "ERROR: dT below minimum. Analysis aborted."
                close $permLog
                return -1
            }
        }
    }

    close $permLog
    set wallTime [expr [clock seconds] - $analysisStartT]

    puts ""
    puts "=============================================="
    puts "ANALYSIS COMPLETE"
    puts "=============================================="
    puts "Final time:         [format %.4f $currentTime] s"
    puts "Total steps:        $totalSteps"
    puts "dT reductions:      $reductions"
    puts "dT increases:       $increases"
    puts "Perm updates:       $permUpdates"
    puts "Wall time:          $wallTime seconds"
    puts "=============================================="
    puts ""

    return 0
}

# run the analysis
puts "Starting adaptive analysis with variable permeability..."
set ok [adaptiveAnalyzeWithPerm $totalTime $dT_initial $dT_min $dT_max $N_success $permUpdateInterval]

if {$ok != 0} {
    puts "Analysis failed to complete!"
} else {
    puts "Analysis completed successfully."
}
""")
        else:
            # simple adaptive analysis without variable permeability
            f.write("# ============================================================================\n")
            f.write("# RUN ADAPTIVE ANALYSIS\n")
            f.write("# ============================================================================\n\n")
            f.write("puts \"Starting adaptive analysis...\"\n")
            f.write("set ok [adaptiveAnalyze $totalTime $dT_initial $dT_min $dT_max $N_success]\n\n")
            f.write("if {$ok != 0} {\n")
            f.write("    puts \"Analysis failed to complete!\"\n")
            f.write("} else {\n")
            f.write("    puts \"Analysis completed successfully.\"\n")
            f.write("}\n")

    print(f"[INFO] Generated: {outFile}")
    return outFile
