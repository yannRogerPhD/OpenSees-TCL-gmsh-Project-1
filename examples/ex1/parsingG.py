import os
import numpy as np

# lines

meshFile = "ex1.msh"

transX, transY, transZ = 2, 2, 0
xMin, xMax = 0.0, 1.0
yMin, yMax = 0.0, 1.0
zMin, zMax = 0.0, 0.0

thickX, thickY, thickZ = (xMax - xMin) / (transX - 1), (yMax - yMin) / (transY - 1), (zMax - zMin) / (transZ - 1)


def outputFolder(meshFile_):
    # Create a dedicated output folder for actual mesh and return its path
    baseName = os.path.splitext(os.path.basename(meshFile_))[0]
    outDir_ = os.path.join("TCL-Files", baseName)
    os.makedirs(outDir_, exist_ok=True)
    print(f"📁 Output directory prepared: {outDir_}")
    return outDir_


# prepare the folder once
outDir = outputFolder(meshFile)


class FuzzyFloat(float):
    """A float that compares equal within tolerance."""
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


# -------------------------------------------------------
# Boundary-selection helper functions (using coordinates)
# -------------------------------------------------------

defaultTolerance = 1e-6


def _roundFunc(x_, tol=defaultTolerance):
    # round a coordinate to the decimal precision implied by the tolerance
    return round(x_, int(abs(np.log10(tol))))


def nodesNearX(xTarget, tol=defaultTolerance):
    # return all node tags whose x-coordinate is approximately xTarget
    xTargetR = FuzzyFloat(_roundFunc(xTarget, tol), tol)
    return [n for n, (x_, y_, z_) in nodeCoords.items()
            if FuzzyFloat(_roundFunc(x_, tol), tol) == xTargetR]


def nodesNearY(yTarget, tol=defaultTolerance):
    # return all node tags whose y-coordinate approximately yTarget
    yTargetR = FuzzyFloat(_roundFunc(yTarget, tol), tol)
    return [n for n, (x_, y_, z_) in nodeCoords.items()
            if FuzzyFloat(_roundFunc(y_, tol), tol) == yTargetR]


def nodesNearZ(zTarget, tol=defaultTolerance):
    # return all node tags whose z-coordinate ≈ zTarget (useful in 3D)
    zTargetR = FuzzyFloat(_roundFunc(zTarget, tol), tol)
    return [n for n, (x_, y_, z_) in nodeCoords.items()
            if FuzzyFloat(_roundFunc(z_, tol), tol) == zTargetR]


def selectNodes(condition, tol=defaultTolerance, debug=False):
    """
    Select nodes satisfying a user-defined Boolean condition on (x, y, z).

    Args:
        condition: callable (x, y, z) -> bool
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
def sortNodesByX(nodes):
    # return nodes sorted by their x-coordinate
    return sorted(nodes, key=lambda n: nodeCoords[n][0])


def sortNodesByY(nodes):
    # return nodes sorted by their y-coordinate
    return sorted(nodes, key=lambda n: nodeCoords[n][1])


def sortNodesByZ(nodes):
    # return nodes sorted by their z-coordinate (for 3D)
    return sorted(nodes, key=lambda n: nodeCoords[n][2])


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

sspBrickGroups = {}  # example physical volume IDs
# sspBrickGroups = {1, 2, 3}

bbarQuadUPGroups = {}
# bbarQuadUPGroups = {1, 2}

quadUPGroups = {}
# QuadUPGroups = {1, 2, 3, 4}

bbarBrickGroups = {}  # now for volumes instead
# bbarBrickGroups = {1, 2}


# -------------------------------------------------------
# Tcl writing utilities for fixities and equalDOFs
# -------------------------------------------------------

def writeFixities(fileName, nodes, fixValues, header="Fixities", outputDir='.'):
    """
    Write a TCL file of fix commands.
    Example: writeFixities('fixityBottom.tcl', bottomNodes, [1,1,1])
    """
    fullPath = os.path.join(outputDir, fileName)
    if not nodes:
        print(f"⚠️ No nodes to fix for {fileName}")
        return
    with open(fullPath, 'w') as f_:
        f_.write(f"# {header}\n\n")
        for n in nodes:
            f_.write(f"fix {n} {' '.join(map(str, fixValues))}\n")
    print(f"✅ Wrote {fileName} ({len(nodes)} nodes)")


def writeEqualDOFs(fileName, nodePairs, dofS, header="EqualDOF pairs", outputDir="."):
    """
    Write a TCL file of equalDOF commands.
    nodePairs: list of (master, slave) node tuples
    DOs: list of DOFs to link, e.g. [1,2] for u,v
    """
    fullPath = os.path.join(outputDir, fileName)
    if not nodePairs:
        print(f"⚠️ No node pairs for {fileName}")
        return
    with open(fullPath, 'w') as f_:
        f_.write(f"# {header}\n\n")
        for i, j in nodePairs:
            f_.write(f"equalDOF {i} {j} {' '.join(map(str, dofS))}\n")
    print(f"✅ Wrote {fileName} ({len(nodePairs)} pairs)")


# -------------------------------------------------------
# DOF rules (define here so the dictionary can use them)
# -------------------------------------------------------
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


# ------------------------------------------------------------------------------
# Default material/physical parameters per group (auto-detected from mesh file)
# ------------------------------------------------------------------------------

gVal = 9.806

# detect the maximum physical group ID directly from mesh
maxPhyGroup = 0
with open(meshFile) as f:
    lines = f.readlines()
    inElementSection = False
    for line in lines:
        line = line.strip()
        if line == '$Elements':
            inElementSection = True
            continue
        elif line == '$EndElements':
            break
        if inElementSection:
            parts = line.split()
            if len(parts) > 4:
                try:
                    elementType = int(parts[1])
                    phyGroup = int(parts[4])
                    # include both 2D and 3D element types
                    if elementType in (3, 5, 10, 17, 105, 1005, 103, 1003):
                        if phyGroup > maxPhyGroup:
                            maxPhyGroup = phyGroup
                except (ValueError, IndexError):
                    continue

# stop if no physical groups were found
if maxPhyGroup == 0:
    raise RuntimeError("No physical groups detected in the .msh file. Check that file has a valid $Elements section.")


# auto-build physical group tags based on mesh content
mainSoilTags = {i: i for i in range(1, maxPhyGroup + 1)}

# define default per-group material parameters
# thickness = {i: 1.0 for i in mainSoilTags}
# bulkVals = {i: 5.0e6 for i in mainSoilTags}
# fmassVals = {i: 1.0 for i in mainSoilTags}
# hPermVals = {i: 1.0e-4 for i in mainSoilTags}
# vPermVals = {i: 1.0e-4 for i in mainSoilTags}

print(f"✅ Detected {maxPhyGroup} physical groups in mesh → mainSoilTags = {list(mainSoilTags.keys())}")

# -------------------------------------------------------
# !!!!! Element profiles !!!!!
# -------------------------------------------------------
elementProfiles = {
    3: {"key": "quad4", "ndm": 2, "needsP": False, "dofRule": only2DOFs},
    103: {"key": "bbarQuadUP", "ndm": 2, "needsP": True, "dofRule": threeDOFs},
    1003: {"key": "quadUP", "ndm": 2, "needsP": True, "dofRule": threeDOFs},
    10: {"key": "9_4_QuadUP", "ndm": 2, "needsP": True, "dofRule": both2and3DOFs},
    5: {"key": "brickUP", "ndm": 3, "needsP": True, "dofRule": fourDOFs3D},  # 8-node 3D u-p
    105: {"key": "bbarBrickUP", "ndm": 3, "needsP": True, "dofRule": fourDOFs3D},
    1005: {"key": "SSPbrickUP", "ndm": 3, "needsP": True, "dofRule": fourDOFs3D},  # best for large 3D dynamic pbs
    17: {"key": "20_8_BrickUP", "ndm": 3, "needsP": True, "dofRule": twentyEightBrickDOFs},
}

# -------------------------------------------------------
# only the Elements section is needed HERE
# -------------------------------------------------------
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

# -----------------------------------------------------------
# Filter out 2D surface elements when 3D volumes are present
# -----------------------------------------------------------
has3D = any(el["type"] in (5, 105, 1005, 17) for el in elements)
if has3D:
    elements = [el for el in elements if el["type"] in (5, 105, 1005, 17)]
    print("Detected 3D mesh → ignoring surface elements (type 3).")

for el in elements:
    if el["type"] == 3:
        if el["group"] in bbarQuadUPGroups:
            el["type"] = 103  # 2D bbarQuadUP
        elif el["group"] in quadUPGroups:
            el["type"] = 1003  # 2D quadUP
    elif el["type"] == 5 and el["group"] in bbarBrickGroups:
        el["type"] = 105  # 3D bbarBrickUP
    elif el["type"] == 5 and el["group"] in sspBrickGroups:
        el["type"] = 1005  # 3D SSPbrickUP

mappedBbar = sum(el["type"] == 103 for el in elements)
mappedQuadUP = sum(el["type"] == 1003 for el in elements)
mappedBbarBrickUP = sum(el["type"] == 105 for el in elements)
mappedSSPBrickUP = sum(el["type"] == 1005 for el in elements)

if mappedBbar:
    print(f"Remapped {mappedBbar} elements → bbarQuadUP (103)")

if mappedQuadUP:
    print(f"Remapped {mappedQuadUP} elements → quadUP (1003)")

if mappedBbarBrickUP:
    print(f"Remapped {mappedBbarBrickUP} elements → bbarBrickUP (105)")

if mappedSSPBrickUP:
    print(f"Remapped {mappedSSPBrickUP} elements → SSPbrickUP (1005)")

# -------------------------------------------------------
# Detect element types and compute ndm / ndf
# -------------------------------------------------------
usedProfiles = {el["type"] for el in elements if el["type"] in elementProfiles}
print()
print("usedProfiles:", usedProfiles)

if usedProfiles:
    # determine ndm and ndf correctly for 2D / 3D u-p
    ndmGlobal = max(elementProfiles[t]["ndm"] for t in usedProfiles)
    if ndmGlobal == 2:
        ndfGlobal = 3 if any(elementProfiles[t]["needsP"] for t in usedProfiles) else 2
    elif ndmGlobal == 3:
        ndfGlobal = 4 if any(elementProfiles[t]["needsP"] for t in usedProfiles) else 3
    else:
        ndfGlobal = 2  # fallback

else:
    ndmGlobal, ndfGlobal = 2, 2

# print(f"Detected ndmGlobal = {ndmGlobal}, ndfGlobal = {ndfGlobal}")

nodeDOFs = {}

for el in elements:
    eType = el["type"]
    if eType in elementProfiles:
        ruleFunc = elementProfiles[eType]["dofRule"]
        for nodeTag, dofCount in ruleFunc(el["nodes"]).items():
            # keep the maximum DOF for nodes shared by multiple elements
            if nodeTag not in nodeDOFs or dofCount > nodeDOFs[nodeTag]:
                nodeDOFs[nodeTag] = dofCount

# summarize
twoDOFNodes = [n for n, d in nodeDOFs.items() if d == 2]
threeDOFNodes = [n for n, d in nodeDOFs.items() if d == 3]
fourDOFNodes = [n for n, d in nodeDOFs.items() if d == 4]

print(f"\nTotal nodes detected: {len(nodeDOFs)}")
print(f"  2-DOF nodes: {len(twoDOFNodes)}")
print(f"  3-DOF nodes: {len(threeDOFNodes)}")
print(f"  4-DOF nodes: {len(fourDOFNodes)}")

# -------------------------------------------------------
# Write the header file
# -------------------------------------------------------
headerPath = os.path.join(outDir, "modelHeader.tcl")
with open(headerPath, "w") as f:
    f.write(f"model BasicBuilder -ndm {ndmGlobal} -ndf {ndfGlobal}\n")
print(f"✅ modelHeader.tcl written at: {headerPath}")

print(f"!! OpenSees model header: ndm={ndmGlobal}, ndf={ndfGlobal} "
      f"({', '.join(elementProfiles[t]['key'] for t in usedProfiles)})\n")
# print("✅ modelHeader.tcl written.")

# -------------------------------------------------------
# Read node coordinates from Gmsh
# -------------------------------------------------------
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
                    precision = 6  # adjust to what your mesh resolution tolerates
                    x = round(float(x), precision)
                    y = round(float(y), precision)
                    z_val = round(float(z[0]), precision) if z else 0.0
                    nodeCoords[nodeTag] = (x, y, z_val)
                except ValueError:
                    continue

print(f"✅ Parsed {len(nodeCoords)} nodes from {meshFile}")


def writeElementsTcl(elements_, profiles_, filePrefix="elements_", outputDir='.'):
    """
    Writes .tcl files grouped by element type.

    Each file contains OpenSees element definitions using the appropriate formulation
    (e.g., quadUP, brickUP, SSPbrickUP).
    Files are named with the prefix 'elements_' followed by the element key, e.g., elements_quadUP.tcl.

    Args:
        elements_: list of dicts with keys 'id', 'type', 'group', 'nodes'
        profiles_: dict mapping element type IDs to property dictionaries
        filePrefix: output file prefix (default 'elements_')
        outputDir: directory path where .tcl files will be written (default current directory)
    """

    written = []
    for eType_ in {el["type"] for el in elements_ if el["type"] in profiles_}:
        profile = profiles_[eType_]
        fileName = os.path.join(outputDir, f"{filePrefix}{profile['key']}.tcl")
        with open(fileName, "w") as f__:
            f__.write(f"# ----- {profile['key']} elements -----\n\n")
            for el in [e for e in elements_ if e["type"] == eType_]:
                phy = el["group"]
                nodes = " ".join(str(n) for n in el["nodes"])
                key = profile["key"]

                if key == "quad4":
                    # massDen, fluidDen = 1755, 1000
                    # alpha = np.atan(2.0 / 100)  # 2% slope
                    # alphaRads = alpha

                    alpha = 0.0
                    alphaRads = np.deg2rad(alpha)

                    thicknessQuad4 = {i: 1.0 for i in mainSoilTags}
                    # !!!!!!!!! 2D cases !!!!!!!!!
                    xW = - gVal * np.sin(alphaRads)
                    yW = - gVal * np.cos(alphaRads)
                    f__.write(
                        f"element "
                        f"{key} "
                        f"{el['id']} "
                        f"{nodes} "
                        f"{thicknessQuad4[phy]} "
                        f"PlaneStrain "
                        f"{mainSoilTags[phy]} "
                        f"0.0 "
                        f"0.0 "
                        f"{xW:.4f} "
                        f"{yW:.4f}\n"
                    )

                elif key == "quadUP":  # OK VERIFIED
                    porosity = {i: 1.0 for i in mainSoilTags}
                    Bf = 2.2e6  # kN/m^2 (for pure water)

                    # thickness, bulk, fluid mass per physical group
                    thicknessQuadUP = {i: 1.0 for i in mainSoilTags}

                    bulkQuadUP = {i: Bf / porosity[i] for i in mainSoilTags}
                    fMassQuadUP = {i: 1 for i in mainSoilTags}  # fluid density (for ex., 1.0 t/m^3)

                    hPermRaw = 5.0e-4
                    vPermRaw = 5.0e-4

                    hPermQuadUP = {i: hPermRaw / (gVal * fMassQuadUP[i]) for i in mainSoilTags}
                    vPermQuadUP = {i: vPermRaw / (gVal * fMassQuadUP[i]) for i in mainSoilTags}

                    alpha_ = 4  # in degrees already! always convert in radians
                    alpha_V = np.deg2rad(alpha_)
                    b1QuadUP = + gVal * np.sin(alpha_V)
                    b2QuadUP = - gVal * np.cos(alpha_V)

                    tQuadUP = 0.0  # normal traction if needed

                    f__.write(
                        f"element "
                        f"{key} "
                        f"{el['id']} "
                        f"{nodes} "
                        f"{thicknessQuadUP[phy]} "
                        f"{mainSoilTags[phy]} "
                        f"{bulkQuadUP[phy]} "
                        f"{fMassQuadUP[phy]} "
                        f"{hPermQuadUP[phy]} "
                        f"{vPermQuadUP[phy]} "
                        f"{b1QuadUP} "
                        f"{b2QuadUP} "
                        f"{tQuadUP}\n"
                    )

                elif key == "bbarQuadUP":  # OK VERIFIED
                    porosity = {i: 1.0 for i in mainSoilTags}
                    Bf = 2.2e6  # kN/m^2 (for pure water)

                    thicknessBbarQuadUP = {i: 1.0 for i in mainSoilTags}

                    bulkBbarQuadUP = {i: Bf / porosity[i] for i in mainSoilTags}
                    fMassBbarQuadUP = {i: 1 for i in mainSoilTags}

                    hPermBbarQuadUP = 5.0e-4
                    vPermBbarQuadUP = 5.0e-4
                    hPermBbarQuadUP = {i: hPermBbarQuadUP / (gVal * fMassBbarQuadUP[i]) for i in mainSoilTags}
                    vPermBbarQuadUP = {i: vPermBbarQuadUP / (gVal * fMassBbarQuadUP[i]) for i in mainSoilTags}

                    alpha_ = 4  # in degrees already! always convert in radian
                    alpha_V = np.deg2rad(alpha_)
                    b1BbarQuadUP = + gVal * np.sin(alpha_V)
                    b2BbarQuadUP = - gVal * np.cos(alpha_V)

                    tBbarQuadUP = 0.0

                    f__.write(
                        f"element "
                        f"{key} "
                        f"{el['id']} "
                        f"{nodes} "
                        f"{thicknessBbarQuadUP[phy]} "
                        f"{mainSoilTags[phy]} "
                        f"{bulkBbarQuadUP[phy]} "
                        f"{fMassBbarQuadUP[phy]} "
                        f"{hPermBbarQuadUP[phy]} "
                        f"{vPermBbarQuadUP[phy]} "
                        f"{b1BbarQuadUP} "
                        f"{b2BbarQuadUP} "
                        f"{tBbarQuadUP}\n"
                    )

                elif key == "9_4_QuadUP":  # OK VERIFIED
                    porosity = {i: 1.0 for i in mainSoilTags}
                    Bf = 2.2e6  # kN/m^2 (for pure water)

                    thickness9_4_QuadUP = {i: 1.0 for i in mainSoilTags}

                    bulk9_4_QuadUP = {i: Bf / porosity[i] for i in mainSoilTags}
                    fMass9_4_QuadUP = {i: 1 for i in mainSoilTags}

                    hPerm9_4_QuadUP = 5.0e-4
                    vPerm9_4_QuadUP = 5.0e-4

                    hPerm9_4_QuadUP = {i: hPerm9_4_QuadUP / (gVal * fMass9_4_QuadUP[i]) for i in mainSoilTags}
                    vPerm9_4_QuadUP = {i: vPerm9_4_QuadUP / (gVal * fMass9_4_QuadUP[i]) for i in mainSoilTags}

                    alpha_ = 4  # in degrees already! always convert in radians
                    alpha_V = np.deg2rad(alpha_)
                    b19_4_QuadUP = + gVal * np.sin(alpha_V)
                    b29_4_QuadUP = - gVal * np.cos(alpha_V)

                    f__.write(
                        f"element "
                        f"{key} "
                        f"{el['id']} "
                        f"{nodes} "
                        f"{thickness9_4_QuadUP[phy]} "
                        f"{mainSoilTags[phy]} "
                        f"{bulk9_4_QuadUP[phy]} "
                        f"{fMass9_4_QuadUP[phy]} "
                        f"{hPerm9_4_QuadUP[phy]} "
                        f"{vPerm9_4_QuadUP[phy]} "
                        f"{b19_4_QuadUP} "
                        f"{b29_4_QuadUP}\n"
                    )

                elif key == "brickUP":  # OK VERIFIED
                    # !!!!!!!!! 3D cases !!!!!!!!!

                    porosity = {i: 1.0 for i in mainSoilTags}
                    Bf = 2.2e6  # kN/m^2 (for pure water)

                    bulkBrickUP = {i: Bf / porosity[i] for i in mainSoilTags}
                    fMassBrickUP = {i: 1 for i in mainSoilTags}

                    PermXBrickUP = 5.0e-4
                    PermYBrickUP = 5.0e-4
                    PermZBrickUP = 5.0e-4
                    # alpha_ = 4 # in degrees already! always convert in degrees
                    PermXBrickUP = {i: PermXBrickUP / (gVal * fMassBrickUP[i]) for i in mainSoilTags}
                    PermYBrickUP = {i: PermYBrickUP / (gVal * fMassBrickUP[i]) for i in mainSoilTags}
                    PermZBrickUP = {i: PermZBrickUP / (gVal * fMassBrickUP[i]) for i in mainSoilTags}

                    alpha__ = 0.0  # in degrees
                    alphaVal = np.deg2rad(alpha__)
                    gx = + gVal * np.sin(alphaVal)
                    gy = 0.0
                    gz = - gVal * np.cos(alphaVal)

                    bXBrickUP = gx
                    bYBrickUP = gy
                    bZBrickUP = gz

                    f__.write(
                        f"element "
                        f"{key} "
                        f"{el['id']} "
                        f"{nodes} "
                        f"{mainSoilTags[phy]} "
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
                    porosity = {i: 1.0 for i in mainSoilTags}
                    Bf = 2.2e6  # kN/m^2 (for pure water)

                    bulkBbarBrickUP = {i: Bf / porosity[i] for i in mainSoilTags}
                    fMassBbarBrickUP = {i: 1 for i in mainSoilTags}

                    PermXBbarBrickUP = 5.0e-4
                    PermYBbarBrickUP = 5.0e-4
                    PermZBbarBrickUP = 5.0e-4
                    # alpha_ = 4 # in degrees already! always convert in degrees
                    PermXBbarBrickUP = {i: PermXBbarBrickUP / (gVal * fMassBbarBrickUP[i]) for i in mainSoilTags}
                    PermYBbarBrickUP = {i: PermYBbarBrickUP / (gVal * fMassBbarBrickUP[i]) for i in mainSoilTags}
                    PermZBbarBrickUP = {i: PermZBbarBrickUP / (gVal * fMassBbarBrickUP[i]) for i in mainSoilTags}

                    alpha__ = 0.0  # in degrees
                    alphaVal = np.deg2rad(alpha__)
                    gx = + gVal * np.sin(alphaVal)
                    gy = 0.0
                    gz = - gVal * np.cos(alphaVal)

                    bXBbarBrickUP = gx
                    bYBbarBrickUP = gy
                    bZBbarBrickUP = gz

                    f__.write(
                        f"element "
                        f"{key} "
                        f"{el['id']} "
                        f"{nodes} "
                        f"{mainSoilTags[phy]} "
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

                    porosity = {i: 1.0 for i in mainSoilTags}
                    Bf = 2.2e6  # kN/m^2 (for pure water)

                    bulkSSPbrickUP = {i: Bf / porosity[i] for i in mainSoilTags}  # fluid bulk modulus
                    fMassSSPbrickUP = {i: 1.0 for i in mainSoilTags}  # fluid density

                    permXSSPbrickUP = 5.0e-4  # isotropic permeability (m/s)
                    permYSSPbrickUP = 5.0e-4
                    permZSSPbrickUP = 5.0e-4

                    voidsSSPbrickUP = {i: 0.7 for i in mainSoilTags}
                    alphaParamSSPbrickUP = {i: 2.4e-6 for i in mainSoilTags}  # stabilization parameter

                    alpha__ = 0.0  # in degrees
                    alphaVal = np.deg2rad(alpha__)
                    gx = + gVal * np.sin(alphaVal)
                    gy = 0.0
                    gz = - gVal * np.cos(alphaVal)

                    permXSSPbrickUP = {i: permXSSPbrickUP / (gVal * fMassSSPbrickUP[i]) for i in mainSoilTags}
                    permYSSPbrickUP = {i: permYSSPbrickUP / (gVal * fMassSSPbrickUP[i]) for i in mainSoilTags}
                    permZSSPbrickUP = {i: permZSSPbrickUP / (gVal * fMassSSPbrickUP[i]) for i in mainSoilTags}

                    f__.write(
                        f"element "
                        f"SSPbrickUP "
                        f"{el['id']} "
                        f"{nodes} "
                        f"{mainSoilTags[phy]} "
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
                    porosity = {i: 1.0 for i in mainSoilTags}
                    Bf = 2.2e6  # kN/m^2 (for pure water)

                    bulk_20_8_BrickUP = {i: Bf / porosity[i] for i in mainSoilTags}
                    fMass_20_8_BrickUP = {i: 1 for i in mainSoilTags}

                    PermX_20_8_BrickUP = 5.0e-4
                    PermY_20_8_BrickUP = 5.0e-4
                    PermZ_20_8_BrickUP = 5.0e-4
                    # alpha_ = 4 # in degrees already! always convert in degrees
                    PermX_20_8_BrickUP = {i: PermX_20_8_BrickUP / (gVal * fMass_20_8_BrickUP[i]) for i in mainSoilTags}
                    PermY_20_8_BrickUP = {i: PermY_20_8_BrickUP / (gVal * fMass_20_8_BrickUP[i]) for i in mainSoilTags}
                    PermZ_20_8_BrickUP = {i: PermZ_20_8_BrickUP / (gVal * fMass_20_8_BrickUP[i]) for i in mainSoilTags}

                    alpha__ = 0.0  # in degrees
                    alphaVal = np.deg2rad(alpha__)
                    gx = + gVal * np.sin(alphaVal)
                    gy = 0.0
                    gz = - gVal * np.cos(alphaVal)

                    bX_20_8_BrickUP = gx
                    bY_20_8_BrickUP = gy
                    bZ_20_8_BrickUP = gz

                    f__.write(
                        f"element "
                        f"{key} "
                        f"{el['id']} "
                        f"{nodes} "
                        f"{mainSoilTags[phy]} "
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


def writeNodesTcl(nodeCoords_, ndmGlobal_, nodeDOFs_=None, filePrefix="nodes", outputDir="."):
    """
    Writes a unified .tcl file defining all nodes.

    Each node line includes coordinates (2D or 3D) and a comment indicating the DOF set,
    e.g. '# 3 DOFs (u,v,p)'.

    This produces one file (nodes2D.tcl or nodes3D.tcl), unlike writeSeparatedNodeFiles(),
    which generates one per DOF category.
    """

    if nodeDOFs_ is None:
        nodeDOFs_ = {}

    # choose filename
    fileName = os.path.join(outputDir, f"{filePrefix}{'3D' if ndmGlobal_ == 3 else '2D'}.tcl")

    with open(fileName, "w") as f__:
        f__.write(f"# ----- Node definitions ({'3D' if ndmGlobal_ == 3 else '2D'}) -----\n\n")

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


def writeSeparatedNodeFiles(nodeCoords_, nodeDOFs_, ndmGlobal_, filePrefix="nodesByDOF", outputDir="."):
    """
    Separates nodes into groups by DOF count (2, 3, 4) and writes separate .tcl files.
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
            f__.write(f"# ----- Nodes with {dofCountT} DOFs -----\n\n")
            for n in sorted(nodeList):
                x_, y_, z_ = nodeCoords_.get(n, (0.0, 0.0, 0.0))
                if ndm == 2:
                    f__.write(f"node {n:<6} {x_:.6f} {y_:.6f}")
                else:
                    f__.write(f"node {n:<6} {x_:.6f} {y_:.6f} {z_:.6f}")

                # optional DOF comment
                label = {2: "(u,v)", 3: "(u,v,p)" if ndm == 2 else "(u,v,w)", 4: "(u,v,w,p)"}.get(dofCountT, "")
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


def writingOutputs(writingNodes=True,
                   writingFixities=True,
                   writingEqualDOFs=True,
                   writingElements=True,
                   outDir_="."):
    """
    Generate selected TCL output files into the target output folder.

    Parameters:
        writingNodes: bool
            Write node definition files (nodes2D.tcl, nodes3D.tcl, nodesByDOF_*.tcl)
        writingFixities: bool
            Write fixity constraint files (fixity*.tcl)
        writingEqualDOFs: bool
            Write equalDOF link files (equalDOFs*.tcl)
        writingElements: bool
            Write element definition files (elements_*.tcl)
        outDir_ (str):
            Directory path where all files will be written (default: current directory ".").
    """

    print("\n─────────────────────────────────────── Writing Outputs ───────────────────────────────────────")
    os.makedirs(outDir_, exist_ok=True)

    # 1️⃣ NODES
    if writingNodes:
        writeNodesTcl(nodeCoords, ndmGlobal, nodeDOFs, outputDir=outDir_)
        writeSeparatedNodeFiles(nodeCoords, nodeDOFs, ndmGlobal, outputDir=outDir_)
        print("✅ Node files written.")
    else:
        print("❌ Node files skipped.")

    # 2️⃣ FIXITIES
    if writingFixities:
        bottomNodes__ = sortNodesByX(nodesNearY(0.0))
        writeFixities("fixityBottom.tcl", bottomNodes__, [1, 1],
                      "Bottom boundary fixities (u,v,p fixed)", outputDir=outDir_)
        print("✅ Fixity files written.")
    else:
        print("❌ Fixities skipped.")

    # 3️⃣ EQUAL DOFs
    if writingEqualDOFs:
        leftNodes__ = sortNodesByY(nodesNearX(0.0))
        rightNodes__ = sortNodesByY(nodesNearX(1.0))
        minLen_ = min(len(leftNodes__), len(rightNodes__))
        nodePairs = list(zip(leftNodes__[:minLen_], rightNodes__[:minLen_]))
        writeEqualDOFs("equalDOFsSides.tcl", nodePairs, [1, 2],
                       "Left–Right equalDOFs for u,v", outputDir=outDir_)
        print("✅ EqualDOF files written.")
    else:
        print("❌ EqualDOFs skipped.")

    # 4️⃣ ELEMENTS
    if writingElements:
        writeElementsTcl(elements, elementProfiles, outputDir=outDir_)
        print("✅ Element files written.")
    else:
        print("❌ Elements skipped.")

    # 5️⃣ MODEL HEADER
    headerPath_ = os.path.join(outDir_, "modelHeader.tcl")
    with open(headerPath_, "w") as f_:
        f_.write(f"model BasicBuilder -ndm {ndmGlobal} -ndf {ndfGlobal}\n")
    # print(f"✅ modelHeader.tcl written at: {headerPath_}")

    # 6️⃣ SUMMARY
    print("\n─────────────────────────────────────── Summary ───────────────────────────────────────")
    print(f"Nodes:        {'✅' if writingNodes else '❌'}")
    print(f"Fixities:     {'✅' if writingFixities else '❌'}")
    print(f"EqualDOFs:    {'✅' if writingEqualDOFs else '❌'}")
    print(f"Elements:     {'✅' if writingElements else '❌'}")
    print("─────────────────────────────────────────────────────────────────────────────────────────\n")
    print("✅ Selected outputs successfully written.\n")


# writeElementsTcl(elements, elementProfiles, outputDir=outDir)
# writeNodesTcl(nodeCoords, ndmGlobal, nodeDOFs, outputDir=outDir)
# writeSeparatedNodeFiles(nodeCoords, nodeDOFs, ndmGlobal, outputDir=outDir)

bottomNodes_ = nodesNearY(0.0)
rightNodes_ = nodesNearX(1.0)
middleNodes_ = selectNodes(lambda x_, y_, z_: 0.45 < x_ < 0.55)

test1 = nodesNearY((1 / 8) * 0.5)
test2 = selectNodes(lambda x2, y2, z2: ((1/6)*0.5) <= x2 <= ((5/6)*0.5) and ((1/4)*0.5) <= y2 <= ((3/4)*0.5))
# print(sortNodesByX(test1))

# -------------------------------------------------------
# Example: detect boundaries and apply constraints
# -------------------------------------------------------

# bottom boundary (y=0)
bottomNodes = sortNodesByX(nodesNearY(0.0))
# writeFixities("fixityBottom.tcl", bottomNodes, [1, 1, 1],
#               "Bottom boundary fixities (u,v,p fixed)")

# left and right boundaries (x=0, x=1)
leftNodes = sortNodesByY(nodesNearX(0.0))
rightNodes = sortNodesByY(nodesNearX(1.0))

# ensure both lists have the same length before pairing
# minLen = min(len(leftNodes), len(rightNodes))
minLen = 1
pairs = list(zip(leftNodes[:minLen], rightNodes[:minLen]))

# writeEqualDOFs("equalDOFsSides.tcl", pairs, [1, 2],
#                "Left–Right equalDOFs for u,v")

# print(leftNodes)
# for n in sortNodesByY(sortNodesByX(test2)):
#     x, y, z = nodeCoords[n]
#     print(f"{n:5d}: x={x:8.6f}, y={y:8.6f}")

# print(sortNodesByY(sortNodesByX(test2))[:9])

# xs = sorted({round(x, 6) for (x, _, _) in nodeCoords.values()})
# print(xs[:20])      # first few
# print(xs[-20:])     # last few

if __name__ == "__main__":
    writingOutputs(writingNodes=False,
                   writingFixities=True,
                   writingEqualDOFs=False,
                   writingElements=False, outDir_=outDir)


def writeMainTcl_global(tclRootDir, modelName, orderedSections=None):
    """
    Create a global main.tcl in TCL-Files/ that sources the subfiles
    inside the model-specific folder (e.g., model4/).

    Parameters:
        tclRootDir (str): Path to 'TCL-Files' directory.
        modelName (str): Model folder name (e.g. 'model4').
        orderedSections (list[str], optional): Custom ordering of sections.
            Default order: ['modelHeader', 'nodes', 'elements', 'fixity', 'equalDOF']
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
        f_.write(f"# main.tcl for {modelName}\n")
        # f_.write("# loaded automatically from/by Python\n")
        f_.write("# ============================================================\n\n")
        f_.write(f'puts "==== Running main.tcl for {modelName} ===="\n\n')

        f_.write(f"set thickX {round(thickX, 6)}\n")
        f_.write(f"set thickY {round(thickY, 6)}\n")
        f_.write(f"set thickZ {round(thickZ, 6)}\n\n")

        # automatically source subfiles inside model folder
        f_.write(f"# writing main code HERE\n")

        f_.write(f"wipe\n"
                 f"model BasicBuilder -ndm 2 -ndf 3\n"
                 f"\n"
                 f""
                 )

        f_.write(f"\n"
                 f"source {modelName}")

        f_.write("\n\n")

        # more details HERE (link down) for the selection of analysis commands
        # https://opensees.berkeley.edu/OpenSees/manuals/usermanual/toc187244.htm

        f_.write("constraints Transformation\n")
        # - Plain
        # - Penalty
        # - Lagrange
        # - Transformation
        #

        f_.write("numberer RCM\n")
        # - Plain
        # - RCM
        #

        f_.write("system ProfileSPD\n")
        # - BandGeneral
        # - BandSPD
        # - ProfileSPD
        # - SparseGeneral
        # - UmfPack
        # - SparseSPD
        #

        f_.write(f"test NormUnbalance {tol} {maxNumIter} {printFlag}\n")
        # - NormDispIncr
        # - EnergyIncr

        f_.write(f"algorithm Newton\n")
        # - Linear
        # - Newton
        # - NewtonLineSearch $ratio # HERE we MUST define the ratio (see Berkeley website for more info)
        # - ModifiedNewton
        # - KrylovNewton
        # - BFGS $count # HERE we MUST define the count int (see Berkeley website for more info)
        # - Broyden # HERE we MUST define the count int (see Berkeley website for more info)
        #

        f_.write("integrator LoadControl 1.0\n")
        # A) For static analysis
        #   - LoadControl $dLambda1 <$Jd $minLambda $maxLambda>
        #   - DisplacementControl $nodeTag $dofTag $dU1 <$Jd $minDu $maxDu>
        #   - MinUnbalDispNorm $dLambda11 <$Jd $minLambda $maxLambda>
        #   - ArcLength $arcLength $alpha

        # B) For transient analysis
        #   - Newmark $gamma $beta
        #   - HHT $gamma <$alphaM $betaK $betaKInit $betaKComm>
        #

        f_.write("analysis Static\n\n")
        # Transient
        # VariableTransient

        f_.write(f'puts "==== {modelName} TCL model loaded successfully ===="\n')

    print(f"✅ Global main.tcl written at: {mainPath}")
    print("   Contains source calls for:")
    for f_ in orderedFiles:
        print(f"   • {modelName}/{f_}")


writeMainTcl_global(
    tclRootDir="TCL-Files",
    modelName=os.path.splitext(os.path.basename(meshFile))[0]
)
