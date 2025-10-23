import os
import numpy as np

"""
Custom elementType remapping.
    - !! For ex: Gmsh uses type=3 for all 4-node quads, but we want to distinguish "bbarQuadUP" using our own ID (103)
        - !! change "bbarGroups" (line 10) to actual group IDs (numbers associated to physical surfaces) from Gmsh
        - "bbarGroups" defines which physical groups correspond to bbarQuadUP regions
    - !! do same for:
        - sspBricks
        - quadUP
        - bbarQuadUP
        - bbarBrickUP
"""


def outputFolder(meshFile_):
    """
    Create a dedicated output folder for the mesh and return its path.

    Example:
        out_dir = outputFolder("model4.msh") # location: TCL-Files/"modelName"
    """
    baseName = os.path.splitext(os.path.basename(meshFile_))[0]
    outDir_ = os.path.join("TCL-Files", baseName)
    os.makedirs(outDir_, exist_ok=True)
    print(f"📁 Output directory prepared: {outDir_}")
    return outDir_


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


defaultTolerance = 1e-6


def _roundFunc(x_, tol=defaultTolerance):
    # round a coordinate to the decimal precision implied by the tolerance
    return round(x_, int(abs(np.log10(tol))))


# -------------------------------------------------------
# Boundary-selection helper functions (using coordinates)
# -------------------------------------------------------
def nodesNearX(xTarget, nodeCoords, tol=defaultTolerance):
    # return all node tags whose x-coordinate is approximately xTarget
    xTargetR = FuzzyFloat(_roundFunc(xTarget, tol), tol)
    return [n for n, (x_, y_, z_) in nodeCoords.items()
            if FuzzyFloat(_roundFunc(x_, tol), tol) == xTargetR]


def nodesNearY(yTarget, nodeCoords, tol=defaultTolerance):
    # return all node tags whose y-coordinate approximately yTarget
    yTargetR = FuzzyFloat(_roundFunc(yTarget, tol), tol)
    return [n for n, (x_, y_, z_) in nodeCoords.items()
            if FuzzyFloat(_roundFunc(y_, tol), tol) == yTargetR]


def nodesNearZ(zTarget, nodeCoords, tol=defaultTolerance):
    # return all node tags whose z-coordinate ≈ zTarget (useful in 3D)
    zTargetR = FuzzyFloat(_roundFunc(zTarget, tol), tol)
    return [n for n, (x_, y_, z_) in nodeCoords.items()
            if FuzzyFloat(_roundFunc(z_, tol), tol) == zTargetR]


def selectNodes(condition, nodeCoords, tol=defaultTolerance, debug=False):
    """
    Select nodes satisfying a user-defined Boolean condition on (x, y, z).

    Args:
        condition: callable (x, y, z) -> bool
        nodeCoords (dict): mapping nodeTag -> (x, y, z)
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


# -------------------------------------------------------
# Tcl writing utilities
# -------------------------------------------------------

def writeFixities(fileName, nodes, fixValues, header="Fixities", outputDir='.'):
    """
    Write a TCL file of fix commands

    Parameters:
        fileName (str): output filename (e.g., "fixityBottom.tcl")
        nodes (Iterable[int]): node tags to constrain
        fixValues (Iterable[int]): DOF flags, e.g. [1,1,1] or [1,1,0]
        header (str): comment header written at the top of the file
        outputDir (str): directory where the file is written

    Example: writeFixities('fixityBottom.tcl', bottomNodes, [1,1,1])
    """
    fullPath = os.path.join(outputDir, fileName)
    nodes = list(nodes)
    if not nodes:
        print(f"⚠️ No nodes to fix for {fileName}")
        return
    with open(fullPath, 'w') as f_:
        f_.write(f"# {header}\n\n")
        for n in nodes:
            f_.write(f"fix {n:>3} {' '.join(map(str, fixValues))}\n")
    print(f"✅ Wrote {fileName} ({len(nodes)} nodes)")


def writeSeparatedFixities(nodes_to_fix, nodeDOFs, fixValuesPerDOF,
                           outputDir='.', filePrefix="fixity", headerPrefix="Fixities"):
    """
    Split a *specific* set of nodes into DOF groups and write separate fixity files.

    Parameters
    ----------
    nodes_to_fix : Iterable[int]
        Only these nodes will be fixed (e.g., bottom boundary nodes).
    nodeDOFs : dict[int, int]
        Node -> DOF count (2, 3, 4...).
        Source this from your existing build step.
    fixValuesPerDOF: dict[int, list[int]]
        DOF count -> fix vector to use for that DOF count.
        Define manually per call.
        Example: {2: [1,1], 3: [1,1,0], 4: [1,1,1,0]}
    outputDir : str
        Target folder for the TCL files.
    filePrefix : str
        Prefix for generated files, e.g. "fixity_bottom" → "fixity_bottom_3DOF.tcl".
    headerPrefix : str
        Prefix for the header comment inside each file.
    """
    # bucket the requested nodes by their DOF count
    buckets = {}
    for n in nodes_to_fix:
        d = nodeDOFs.get(n, None)
        if d is None:
            continue  # node not present in nodeDOFs map
        if d not in fixValuesPerDOF:
            # caller did not provide a fix vector for this DOF count → skip safely
            continue
        buckets.setdefault(d, []).append(n)

    # write one file per DOF bucket present in the subset
    for dofCount, ns in buckets.items():
        fName = f"{filePrefix}_{dofCount}DOF.tcl"
        header = f"{headerPrefix} — {dofCount}-DOF nodes"
        writeFixities(fName, ns, fixValuesPerDOF[dofCount], header=header, outputDir=outputDir)


def writeEqualDOFs(fileName, nodePairs, dofS, header="EqualDOF pairs", outputDir="."):
    """
    Write a TCL file of equalDOF commands

    Parameters:
        fileName (str): output filename (e.g., "equalDOFsSides.tcl")
        nodePairs (Iterable[tuple[int, int]]): list of (master, slave) node pairs
        dofS (Iterable[int]): list of DOFs to link, e.g. [1,2]
        header (str): comment header written at the top of the file
        outputDir (str): directory where the file is written

    nodePairs: list of (master, slave) node tuples
    DOs: list of DOFs to link, e.g. [1,2] for u,v
    """
    fullPath = os.path.join(outputDir, fileName)
    nodePairs = list(nodePairs)
    if not nodePairs:
        print(f"⚠️ No node pairs for {fileName}")
        return
    with open(fullPath, 'w') as f_:
        f_.write(f"# {header}\n\n")
        for i, j in nodePairs:
            f_.write(f"equalDOF {i} {j} {' '.join(map(str, dofS))}\n")
    print(f"✅ Wrote {fileName} ({len(nodePairs)} pairs)")


def writeNodesTcl(nodeCoords_, ndmGlobal_, nodeDOFs_=None, filePrefix="nodes", outputDir="."):
    """
    Writes a unified .tcl file defining all nodes

    Each node line includes coordinates (2D or 3D) and a comment indicating the DOF set,
    e.g. '# 3 DOFs (u,v,p)'

    Parameters:
        nodeCoords_ (dict): mapping nodeTag -> (x, y, z)
        ndmGlobal_ (int): number of spatial dimensions (2 or 3)
        nodeDOFs_ (dict, optional): mapping nodeTag -> DOF count
        filePrefix (str): output file prefix (default "nodes")
        outputDir (str): folder where file is written

    This produces one file (nodes2D.tcl or nodes3D.tcl), unlike writeSeparatedNodeFiles(),
    which generates one per DOF category.
    """

    if nodeDOFs_ is None:
        nodeDOFs_ = {}

    # choose filename
    fileName = os.path.join(
        outputDir, f"{filePrefix}{'3D' if ndmGlobal_ == 3 else '2D'}.tcl")

    with open(fileName, "w") as f__:
        f__.write(f"# !!!!!!!!!!!!!!!!!! Node definitions ({'3D' if ndmGlobal_ == 3 else '2D'}) !!!!!!!!!!!!!!!!!!\n\n")

        for n, coords in sorted(nodeCoords_.items()):
            # write node line depending on dimension
            if ndmGlobal_ == 2:
                x__, y__, _ = coords
                f__.write(f"node {n:<6} {x__:.6f} {y__:.6f}")
            elif ndmGlobal_ == 3:
                x__, y__, z__ = coords
                f__.write(f"node {n:<6} {x__:.6f} {y__:.6f} {z__:.6f}")
            else:
                continue  # skip if dimension undefined

            # add comment showing DOFs if available
            dofCount_ = nodeDOFs_.get(n, None)
            if dofCount_:
                if dofCount_ == 2:
                    label = "(u,v)"
                elif dofCount_ == 3 and ndmGlobal_ == 2:
                    label = "(u,v,p)"
                elif dofCount_ == 3 and ndmGlobal_ == 3:
                    label = "(u,v,w)"
                elif dofCount_ == 4:
                    label = "(u,v,w,p)"
                else:
                    label = ""
                f__.write(f"    # {dofCount_} DOFs {label}")
            f__.write("\n")

    print(f"✅ Wrote {fileName} with {len(nodeCoords_)} nodes "
          f"(comments show detected DOFs)")


def writeSeparatedNodeFiles(nodeCoords_, nodeDOFs_, ndmGlobal_,
                            filePrefix="nodesByDOF", outputDir="."):
    """
    Separates nodes into groups by DOF count (2, 3, 4) and writes separate .tcl files

    Parameters:
        nodeCoords_ (dict): mapping nodeTag -> (x, y, z)
        nodeDOFs_ (dict): mapping nodeTag -> DOF count
        ndmGlobal_ (int): spatial dimension (2 or 3)
        filePrefix (str): output file prefix (default "nodesByDOF")
        outputDir (str): directory for written files

    Automatically handles correct ndm/ndf for each file.
    """

    dofGroups = {2: [], 3: [], 4: []}
    for n, dof in nodeDOFs_.items():
        if dof in dofGroups:
            dofGroups[dof].append(n)

    written = []

    for dofCountT, nodeList in dofGroups.items():
        if not nodeList:
            continue  # skip the empty group

        fileName = os.path.join(outputDir, f"{filePrefix}_{dofCountT}DOF.tcl")
        modelHeader = os.path.join(outputDir, f"modelHeader_{dofCountT}DOF.tcl")

        # determine appropriate ndf per DOF group
        ndf = dofCountT
        ndm = ndmGlobal_  # assume the same ndm for now (you can adjust later if hybrid 2D/3D)

        # write model header for this DOF
        with open(modelHeader, "w") as fHeader:
            fHeader.write(f"model BasicBuilder -ndm {ndm} -ndf {ndf}\n")
        written.append(modelHeader)

        # write node definitions
        with open(fileName, "w") as f__:
            f__.write(f"# !!!!!!!!!!!!!!!!!!! Nodes with {dofCountT} DOFs !!!!!!!!!!!!!!!!!!!\n\n")
            for n in sorted(nodeList):
                x_, y_, z_ = nodeCoords_.get(n, (0.0, 0.0, 0.0))
                if ndm == 2:
                    f__.write(f"node {n:<6} {x_:.6f} {y_:.6f}")
                else:
                    f__.write(f"node {n:<6} {x_:.6f} {y_:.6f} {z_:.6f}")

                # optional DOF comment
                label = {2: "(u,v)",
                         3: "(u,v,p)" if ndm == 2 else "(u,v,w)",
                         4: "(u,v,w,p)"
                         }.get(dofCountT, "")

                f__.write(f"    # {dofCountT} DOFs {label}\n")

        written.append(fileName)

    # summary print that perhaps could be useful
    print("\nSummary by DOF group:")

    for k, v in dofGroups.items():
        print(f"  {k}-DOF nodes: {len(v)}")

    if any(len(v) for v in dofGroups.values()):
        # print(f"✅ Wrote separated node files: {', '.join(written)}")
        print(f"✅ Wrote separated node files")
    else:
        print("⚠️ No node groups detected for separation.")


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
                    porosity = {i: 1.0 for i in mainSoilTags_}
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
                    porosity = {i: 1.0 for i in mainSoilTags_}
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
                    porosity = {i: 1.0 for i in mainSoilTags_}
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

                    porosity = {i: 1.0 for i in mainSoilTags_}
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
                    porosity = {i: 1.0 for i in mainSoilTags_}
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

                    porosity = {i: 1.0 for i in mainSoilTags_}
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

                elif key == "20_8_BrickUP":  # OK VERIFIED
                    porosity = {i: 1.0 for i in mainSoilTags_}
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

        written.append(fileName)
    print(f"✅ Wrote element definition files: {', '.join(written)}")


# --------------------------------------------------------------------
# DOF rules functions (we define here so the dictionary can use them)
# --------------------------------------------------------------------
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
    3:     {"key": "quad4",        "ndm": 2, "needsP": False, "dofRule": only2DOFs},
    103:   {"key": "bbarQuadUP",   "ndm": 2, "needsP": True,  "dofRule": threeDOFs},
    1003:  {"key": "quadUP",       "ndm": 2, "needsP": True,  "dofRule": threeDOFs},
    10031: {"key": "ASDLeft",      "ndm": 2, "needsP": False, "dofRule": only2DOFs},  # For ASDBoundary Left
    10032: {"key": "ASDBottom",    "ndm": 2, "needsP": False, "dofRule": only2DOFs},  # For ASDBoundary Bottom
    10033: {"key": "ASDRight",     "ndm": 2, "needsP": False, "dofRule": only2DOFs},  # For ASDBoundary Right
    10034: {"key": "ASDBottomL",   "ndm": 2, "needsP": False, "dofRule": only2DOFs},  # For ASDBoundary Bottom left
    10035: {"key": "ASDBottomR",   "ndm": 2, "needsP": False, "dofRule": only2DOFs},  # For ASDBoundary Bottom right
    10:    {"key": "9_4_QuadUP",   "ndm": 2, "needsP": True,  "dofRule": both2and3DOFs},
    5:     {"key": "brickUP",      "ndm": 3, "needsP": True,  "dofRule": fourDOFs3D},  # 8-node 3D u-p
    105:   {"key": "bbarBrickUP",  "ndm": 3, "needsP": True,  "dofRule": fourDOFs3D},
    1005:  {"key": "SSPbrickUP",   "ndm": 3, "needsP": True,  "dofRule": fourDOFs3D},  # best for large 3D dynamic pbs
    17:    {"key": "20_8_BrickUP", "ndm": 3, "needsP": True,  "dofRule": twentyEightBrickDOFs},
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
                    if elementType in (3, 5, 10, 17, 105, 1005, 103, 1003, 10031, 10032, 10033, 10034, 10035):
                        if phyGroup > maxPhyGroup:
                            maxPhyGroup = phyGroup
                except (ValueError, IndexError):
                    continue
    return maxPhyGroup


def writeMainTclGlobal(tclRootDir, modelName, thickX, thickY, thickZ, tsX, tsY, orderedSections=None):
    """
    Create a global main.tcl in TCL-Files/ that sources the subfiles
    inside the model-specific folder (e.g., model4/).

    Parameters:
        tclRootDir (str): Path to 'TCL-Files' directory.
        modelName (str): Model folder name (e.g., 'model4').
        thickX (float): X-direction thickness value.
        thickY (float): Y-direction thickness value.
        thickZ (float): Z-direction thickness value.
        tsX (int): timeSeries in x-direction
        tsY (int): timeSeries in y-direction
        orderedSections (list[str], optional): Custom ordering of sections.
            Default order: ['modelHeader', 'nodes', 'elements', 'fixity', 'equalDOF'].
    """
    tol = 1.0e-5
    maxNumIter = 25
    printFlag = 1

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

        f_.write(f"set tsX {tsX}\n")
        f_.write(f"set tsY {tsY} 2\n")
        f_.write(f"set thickX {round(thickX, 6)}\n")
        f_.write(f"set thickY {round(thickY, 6)}\n")
        f_.write(f"set thickZ {round(thickZ, 6)}\n\n")

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

        f_.write(f"test NormUnbalance {tol} {maxNumIter} {printFlag}\n")

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

    print(f"✅ Global main.tcl written at: {mainPath}")
    print("   Contains source calls for:")
    for f_ in orderedFiles:
        print(f"   • {modelName}/{f_}")
