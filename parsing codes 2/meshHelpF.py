import os
import numpy as np


def outputFolder(meshFilE):
    baseName = os.path.splitext(os.path.basename(meshFilE))[0]
    outPutFolder = os.path.join("TCL-Files", baseName)
    os.makedirs(outPutFolder, exist_ok=True)
    return outPutFolder


defaultTolerance = 1e-6


# -------------------------------------------------------
# Node sorting helpers
# -------------------------------------------------------
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
        105, 1005, 10051, 10052, 10053, 10054, 10055, 10056, 10057, 10058, 10059,
        10060, 10061, 10062, 10063, 10064, 10065, 10066, 10067
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
            if g in groupSets["beam2DGrp"]:
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
                "bbarBrickGrp": 105,
                "sspBrickGrp": 1005,
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
            print(f"  {counts[t]:6d} -> {label:25s} ({t:6d})   [{pct:6.2f}%]")

    # Optional: report any unexpected type numbers
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
        if eType in (1, 101) or el["group"] in beam2DGrp or el["group"] in beam3DGrp:
            target = nodeDOFs_struct
        else:
            target = nodeDOFs_soil

        for nodeTag, dofCount in dofMap.items():
            if nodeTag not in target or dofCount > target[nodeTag]:
                target[nodeTag] = dofCount

    nodeDOFs = {**nodeDOFs_soil, **nodeDOFs_struct}
    return nodeDOFs_soil, nodeDOFs_struct, nodeDOFs


# -------------------------------------------------------
# Tcl writing utilities
# -------------------------------------------------------

def writeNodesTcl(nodeCoordS, ndmGLOBAL, nodeDOFS=None,
                  filePrefix="nodes", outputDir=".",
                  elements=None, elementProfileS=None):
    """
    Writes a unified .tcl file defining all nodes

    Each node line includes coordinates (2D or 3D) and a comment indicating the DOF set,
    e.g. '# 3 DOFs (u,v,p)'

    Parameters:
        nodeCoordS (dict): mapping nodeTag -> (x, y, z)
        ndmGLOBAL (int): number of spatial dimensions (2 or 3)
        nodeDOFS (dict, optional): mapping nodeTag -> DOF count
        filePrefix (str): output file prefix (default "nodes")
        outputDir (str): folder where file is written
        elements
        elementProfileS

    This produces one file (nodes2D.tcl or nodes3D.tcl), unlike writeSeparatedNodeFiles(),
    which generates one per DOF category.
    """

    if nodeDOFS is None:
        nodeDOFS = {}

    # -----------------------------------------------------
    # Build per-node domain classification from element types
    # -----------------------------------------------------
    nodeDomain = {}
    if elements and elementProfileS:
        structureTypes = {1, 101}
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

    print(f"✅ Wrote {fileName} with {len(nodeCoordS)} nodes "
          f"(comments show detected DOFs)")


def writeSeparatedNodeFiles(nodeCoords_, nodeDOFs_, ndmGlobal_,
                            filePrefix="nodesByDOF", outputDir=".",
                            labelPrefix=""):
    """
    Separates nodes into groups by DOF count (2, 3, 4, 6, etc.) and writes separate .tcl files

    Automatically handles correct ndm/ndf for each group

    Parameters:
        nodeCoords_ (dict): mapping nodeTag -> (x, y, z)
        nodeDOFs_ (dict): mapping nodeTag -> DOF count
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
                    label = "(u,v,p)"  # could also be (u,v,w) for solid nodes
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
                     filePrefix="elements_", outputDir='.'):
    """
    Writes .tcl files grouped by element type.

    Each file contains OpenSees element definitions using the appropriate formulation
    (e.g., quadUP, brickUP, SSPbrickUP).
    Files are named with the prefix 'elements_' followed by the element key, e.g., elements_quadUP.tcl.

    Parameters:
        elements_ (list[dict]): each with keys: 'id', 'type', 'group', 'nodes'
        profiles_ (dict[int, dict]): element type -> profile dict
        mainSoilTags_ (dict[int, int]): per-physical-group soil tag mapping
        gVal_ (float): gravity magnitude used in body force terms
        filePrefix (str): filename prefix (default: "elements_")
        outputDir (str): directory for output files
    """

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

                elif key == "brickUP":  # OK VERIFIED
                    # !!!!!!!!! 3D cases !!!!!!!!!

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
                    nodesF = [nodeList[5], nodeList[6], nodeList[2], nodeList[1],
                              nodeList[4], nodeList[7], nodeList[3], nodeList[0]]
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
                    nodesF = [nodeList[5], nodeList[6], nodeList[2], nodeList[1],
                              nodeList[4], nodeList[7], nodeList[3], nodeList[0]]
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
                        2: 1.01,
                        3: 1.02
                    }

                    # ensure all other groups get default 1.0 if not explicitly listed
                    # Build the full porosity map (default 1.0 if not listed)
                    porosity = {}
                    for i in mainSoilTags_:
                        porosity[i] = float(porosityCustom.get(int(i), 1.0))

                    Bf = 2.2e6  # kN/m^2 (for pure water)

                    bulkSSPbrickUP = {i: Bf / porosity[i] for i in mainSoilTags_}  # fluid bulk modulus
                    fMassSSPbrickUP = {i: 1.0 for i in mainSoilTags_}  # fluid density

                    permXSSPbrickUP = 5.0e-4  # isotropic permeability (m/s)
                    permYSSPbrickUP = 5.0e-4
                    permZSSPbrickUP = 5.0e-4

                    voidsSSPbrickUP = {i: 0.7 for i in mainSoilTags_}
                    alphaParamSSPbrickUP = {i: 2.4e-6 for i in mainSoilTags_}  # stabilization parameter

                    alpha__ = 0.0  # in degrees
                    alphaVal = np.deg2rad(alpha__)
                    gx = + gVal_ * np.sin(alphaVal)
                    gy = 0.0
                    gz = - gVal_ * np.cos(alphaVal)

                    nodeList = el["nodes"]  # actual list of integers from the mesh
                    nodesF = [nodeList[5], nodeList[6], nodeList[2], nodeList[1],
                              nodeList[4], nodeList[7], nodeList[3], nodeList[0]]
                    nodes = " ".join(str(n) for n in nodesF)

                    permXSSPbrickUP = {i: permXSSPbrickUP / (gVal_ * fMassSSPbrickUP[i]) for i in mainSoilTags_}
                    permYSSPbrickUP = {i: permYSSPbrickUP / (gVal_ * fMassSSPbrickUP[i]) for i in mainSoilTags_}
                    permZSSPbrickUP = {i: permZSSPbrickUP / (gVal_ * fMassSSPbrickUP[i]) for i in mainSoilTags_}

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
                    nodesF = [nodeList[5], nodeList[6], nodeList[2], nodeList[1],
                              nodeList[4], nodeList[7], nodeList[3], nodeList[0]]

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
                    nodesF = [nodeList[5], nodeList[6], nodeList[2], nodeList[1],
                              nodeList[4], nodeList[7], nodeList[3], nodeList[0],
                              nodeList[12], nodeList[18], nodeList[14], nodeList[11],
                              nodeList[10], nodeList[17], nodeList[15], nodeList[9],
                              nodeList[8], nodeList[16], nodeList[19], nodeList[13]]
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

        written.append(fileName)
    print(f"Wrote element definition files: {', '.join(written)}")


# --------------------------------------------------------------------
# DOF rules functions (we define here so the dictionary can use them)
# --------------------------------------------------------------------
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


def fourDOFs3D(ns_):
    # for BrickUP: u, v, w, p; that is 4 DOFs per node
    return {n: 4 for n in ns_}


def twentyEightBrickDOFs(ns_):
    # 20_8_Node_BrickUP (Gmsh type 17): 1st-8 nodes (corners) have 4 DOFs (u,v,w,p), rest 12 nodes have 3 DOFs (u,v,w)
    return {**{n: 4 for n in ns_[:8]}, **{n: 3 for n in ns_[8:]}}


# -------------------------------------------------------
# ELEMENT PROFILE MAP (GMSH element type → metadata)
# -------------------------------------------------------
elementProfiles = {
    # BEAM ELEMENTS (1D structural members)
    # GMSH TYPE 1 = 2-node line element
    1: {"key": "elasticBeamColumn2D", "ndm": 2, "needsP": False, "dofRule": beam2D_DOFs},
    101: {"key": "elasticBeamColumn3D", "ndm": 3, "needsP": False, "dofRule": beam3D_DOFs},

    # SOIL ELEMENTS NOW
    3: {"key": "quad4", "ndm": 2, "needsP": False, "dofRule": only2DOFs},
    103: {"key": "bbarQuadUP", "ndm": 2, "needsP": True, "dofRule": threeDOFs},
    1003: {"key": "quadUP", "ndm": 2, "needsP": True, "dofRule": threeDOFs},
    # !!! 2D boundary absorbing START !!!
    10031: {"key": "ASDLeft", "ndm": 2, "needsP": False, "dofRule": only2DOFs},  # For ASDBoundary Left
    10032: {"key": "ASDBottom", "ndm": 2, "needsP": False, "dofRule": only2DOFs},  # For ASDBoundary Bottom
    10033: {"key": "ASDRight", "ndm": 2, "needsP": False, "dofRule": only2DOFs},  # For ASDBoundary Right
    10034: {"key": "ASDBottomL", "ndm": 2, "needsP": False, "dofRule": only2DOFs},  # For ASDBoundary Bottom left
    10035: {"key": "ASDBottomR", "ndm": 2, "needsP": False, "dofRule": only2DOFs},  # For ASDBoundary Bottom right
    # !!! 2D boundary absorbing END !!!
    10: {"key": "9_4_QuadUP", "ndm": 2, "needsP": True, "dofRule": both2and3DOFs},

    # !!!
    5: {"key": "brickUP", "ndm": 3, "needsP": True, "dofRule": fourDOFs3D},  # 8-node 3D u-p
    105: {"key": "bbarBrickUP", "ndm": 3, "needsP": True, "dofRule": fourDOFs3D},
    1005: {"key": "SSPbrickUP", "ndm": 3, "needsP": True, "dofRule": fourDOFs3D},  # best for large 3D dynamic pbs
    # !!! 3D boundary absorbing START !!!
    10051: {"key": "ASD3DL", "ndm": 3, "needsP": False, "dofRule": fourDOFs3D},
    10052: {"key": "ASD3DR", "ndm": 3, "needsP": False, "dofRule": fourDOFs3D},
    10053: {"key": "ASD3DK", "ndm": 3, "needsP": False, "dofRule": fourDOFs3D},
    10054: {"key": "ASD3DF", "ndm": 3, "needsP": False, "dofRule": fourDOFs3D},
    10055: {"key": "ASD3DBL", "ndm": 3, "needsP": False, "dofRule": fourDOFs3D},
    10056: {"key": "ASD3DBR", "ndm": 3, "needsP": False, "dofRule": fourDOFs3D},
    10057: {"key": "ASD3DBK", "ndm": 3, "needsP": False, "dofRule": fourDOFs3D},
    10058: {"key": "ASD3DBF", "ndm": 3, "needsP": False, "dofRule": fourDOFs3D},
    10059: {"key": "ASD3DLK", "ndm": 3, "needsP": False, "dofRule": fourDOFs3D},
    10060: {"key": "ASD3DBLK", "ndm": 3, "needsP": False, "dofRule": fourDOFs3D},
    10061: {"key": "ASD3DRK", "ndm": 3, "needsP": False, "dofRule": fourDOFs3D},
    10062: {"key": "ASD3DBRK", "ndm": 3, "needsP": False, "dofRule": fourDOFs3D},
    10063: {"key": "ASD3DLF", "ndm": 3, "needsP": False, "dofRule": fourDOFs3D},
    10064: {"key": "ASD3DBLF", "ndm": 3, "needsP": False, "dofRule": fourDOFs3D},
    10065: {"key": "ASD3DRF", "ndm": 3, "needsP": False, "dofRule": fourDOFs3D},
    10066: {"key": "ASD3DBRF", "ndm": 3, "needsP": False, "dofRule": fourDOFs3D},
    10067: {"key": "ASD3DB", "ndm": 3, "needsP": False, "dofRule": fourDOFs3D},
    # 10068: {"key": "ASD3DF",       "ndm": 3, "needsP": True, "dofRule": fourDOFs3D},
    # 10069: {"key": "ASD3DF",       "ndm": 3, "needsP": True, "dofRule": fourDOFs3D},
    # 10070: {"key": "ASD3DF",       "ndm": 3, "needsP": True, "dofRule": fourDOFs3D},
    # !!! 3D boundary absorbing END !!!
    17: {"key": "20_8_BrickUP", "ndm": 3, "needsP": True, "dofRule": twentyEightBrickDOFs},
}


# -------------------------------------------------------
# MESH PARSING UTILITIES
# -------------------------------------------------------
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


def getBoundaryNodesFromMsh(meshFile_, phyGroupID=None, dim=None):
    """
    Returns the nodes belonging to elements of a specified geometric dimension
    (1=line, 2=surface, 3=volume); If no dimension is given, defaults to the
    'before last' element type (for backward compatibility).

    Args:
        meshFile_ (str): path to .msh file
        phyGroupID (int, optional): if given, restricts nodes to this physical group
        dim (int, optional): geometric dimension to extract (1=line, 2=surface, 3=volume)

    Returns:
        set[int]: node tags associated with the chosen element type(s)
    """

    # !!! Map common element types to their geometric dimensions !!!
    eleType_to_dim = {
        1: 1,  # 2-node line
        2: 2,  # 3-node triangle
        3: 2,  # 4-node quadrilateral
        4: 3,  # 4-node tetrahedron
        5: 3,  # 8-node hexahedron
        6: 3,  # 6-node prism
        7: 3,  # 5-node pyramid
        8: 1,  # 3-node quadratic line
        9: 2,  # 6-node quadratic triangle
        10: 2,  # 9-node quadratic quad
        11: 3,  # 10-node quadratic tetra
        16: 2,  # 8-node serendipity quad
        17: 3,  # 20-node serendipity hex
    }

    # !!! Step 1. Collect element types from the mesh !!!
    eleTypesRaw = []
    with open(meshFile_) as f_:
        lines_ = f_.readlines()
        inElem = False
        for line_ in lines_:
            line_ = line_.strip()
            if line_ == "$Elements":
                inElem = True
                continue
            elif line_ == "$EndElements":
                break
            if inElem:
                parts_ = line_.split()
                if len(parts_) > 1:
                    try:
                        eleType_ = int(parts_[1])
                        eleTypesRaw.append(eleType_)
                    except ValueError:
                        continue

    distinctTypes = []
    for t in eleTypesRaw:
        if not distinctTypes or t != distinctTypes[-1]:
            distinctTypes.append(t)

    if not distinctTypes:
        raise RuntimeError(f"No elements found in {meshFile_}")

    # !!! Step 2. Determine which element types to target !!!
    if dim is not None:
        # Filter element types by requested dimension
        targetTypes = [t for t in distinctTypes if eleType_to_dim.get(t) == dim]
        if not targetTypes:
            raise ValueError(f"No elements of dimension {dim} found in {meshFile_}")
    else:
        # Default behavior: before-last distinct type
        eleTypeBL = distinctTypes[-2] if len(distinctTypes) >= 2 else distinctTypes[0]
        targetTypes = [eleTypeBL]

    # !!! Step 3. Collect nodes from matching elements !!!
    boundaryNodes = set()
    with open(meshFile_) as f_:
        lines_ = f_.readlines()
        inElem = False
        for line_ in lines_:
            line_ = line_.strip()
            if line_ == "$Elements":
                inElem = True
                continue
            elif line_ == "$EndElements":
                break
            if inElem:
                parts_ = line_.split()
                if len(parts_) >= 7:
                    try:
                        eleType = int(parts_[1])
                        phyGroup = int(parts_[4])
                        if eleType in targetTypes and (phyGroupID is None or phyGroup == phyGroupID):
                            nodesB = [int(n) for n in parts_[5:]]
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
                                       5, 105, 1005, 10051, 10052, 10053, 10054, 10055, 10056, 10057, 10058, 10059,
                                       10060, 10061, 10062, 10063, 10064, 10065, 10066, 10067,
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
