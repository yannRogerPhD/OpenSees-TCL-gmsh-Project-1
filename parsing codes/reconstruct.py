import numpy as np

"""
Custom elementType remapping.
    - !! For ex: Gmsh uses type=3 for all 4-node quads, but we want to distinguish "bbarQuadUP" using our own ID (103)
    - !! change "bbarGroups" (line 10) to actual group IDs (numbers associated to physical surfaces) from Gmsh
    - "bbarGroups" defines which physical groups correspond to bbarQuadUP regions
"""

bbarGroups = {}
# bbarGroups = {1, 2}

quadUPGroups = {}

bbarBrickGroups = {}  # now for volumes instead


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


def threeDOFs3D(ns_):
    # for BrickUP: u, v, w, p; that is 4 DOFs per node
    return {n: 4 for n in ns_}


def twentyEightBrickDOFs(ns_):
    # 20_8_Node_BrickUP (Gmsh type 17): 1st-8 nodes (corners) have 4 DOFs (u,v,w,p), rest 12 nodes have 3 DOFs (u,v,w)
    return {**{n: 4 for n in ns_[:8]}, **{n: 3 for n in ns_[8:]}}


# -------------------------------------------------------
# Default material/physical parameters per group
# -------------------------------------------------------
gVal = 9.806
massDen, fluidDen = 1755, 1000
alpha = np.atan(2.0 / 100)  # 2% slope
alphaRads = alpha

# define base group-dependent values
mainSoilTags = {1: 1, 2: 2, 3: 3}
thickness = {i: 1.0 for i in mainSoilTags}
bulkVals = {i: 5.0e6 for i in mainSoilTags}
fmassVals = {i: 1.0 for i in mainSoilTags}
hPermVals = {i: 1.0e-4 for i in mainSoilTags}
vPermVals = {i: 1.0e-4 for i in mainSoilTags}

# -------------------------------------------------------
# !!!!! Element profiles !!!!!
# -------------------------------------------------------
elementProfiles = {
    3:   {"key": "quad4",        "ndm": 2,  "needsP": False, "dofRule": only2DOFs},
    103: {"key": "bbarQuadUP",   "ndm": 2,  "needsP": True,  "dofRule": threeDOFs},
    1003: {"key": "quadUP",       "ndm": 2,  "needsP": True,  "dofRule": threeDOFs},
    10:  {"key": "9_4_QuadUP",   "ndm": 2,  "needsP": True,  "dofRule": both2and3DOFs},
    5:   {"key": "brickUP",      "ndm": 3,  "needsP": True,  "dofRule": threeDOFs3D},  # 8-node 3D u-p
    105: {"key": "bbarBrickUP",  "ndm": 3,  "needsP": True,  "dofRule": threeDOFs3D},
    17:  {"key": "20_8_BrickUP", "ndm": 3,  "needsP": True,  "dofRule": twentyEightBrickDOFs},
}

# -------------------------------------------------------
# Load Gmsh mesh (only the Elements section is needed)
# -------------------------------------------------------
meshFile = "model2.msh"
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
has3D = any(el["type"] in (5, 105, 17) for el in elements)
if has3D:
    elements = [el for el in elements if el["type"] in (5, 105, 17)]
    print("Detected 3D mesh → ignoring surface elements (type 3).")

for el in elements:
    if el["type"] == 3:
        if el["group"] in bbarGroups:
            el["type"] = 103  # 2D bbarQuadUP
        elif el["group"] in quadUPGroups:
            el["type"] = 1003  # 2D quadUP
    elif el["type"] == 5 and el["group"] in bbarBrickGroups:
        el["type"] = 105  # 3D bbarBrickUP

mappedBbar = sum(el["type"] == 103 for el in elements)
mappedQuadUP = sum(el["type"] == 1003 for el in elements)
mappedBbarBrickUP = sum(el["type"] == 105 for el in elements)
print(f"Remapped {mappedBbar} elements → bbarQuadUP (103)")
print(f"Remapped {mappedQuadUP} elements → quadUP (1003)")
print(f"Remapped {mappedBbarBrickUP} elements → bbarBrickUP (105)")

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

print(f"Detected ndmGlobal = {ndmGlobal}, ndfGlobal = {ndfGlobal}")

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
with open("modelHeader.tcl", "w") as f:
    f.write(f"model BasicBuilder -ndm {ndmGlobal} -ndf {ndfGlobal}\n")

print(f"!! OpenSees model header: ndm={ndmGlobal}, ndf={ndfGlobal} "
      f"({', '.join(elementProfiles[t]['key'] for t in usedProfiles)})")
print("✅ modelHeader.tcl written.")


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
                    if len(z) == 0:
                        nodeCoords[nodeTag] = (x, y, 0.0)
                    else:
                        nodeCoords[nodeTag] = (x, y, z[0])
                except ValueError:
                    continue

print(f"✅ Parsed {len(nodeCoords)} nodes from {meshFile}")


def writeElementsTcl(elements_, profiles_, filePrefix="elements_"):
    """
    function that writes .tcl element definition files grouped by element type, according to OpenSees ELMT formulations
    """
    written = []
    for eType_ in {el["type"] for el in elements_ if el["type"] in profiles_}:
        profile = profiles_[eType_]
        fileName = f"{filePrefix}{profile['key']}.tcl"
        with open(fileName, "w") as f__:
            f__.write(f"# ----- {profile['key']} elements -----\n\n")
            for el in [e for e in elements_ if e["type"] == eType_]:
                phy = el["group"]
                nodes = " ".join(str(n) for n in el["nodes"])
                key = profile["key"]

                if key == "quad4":
                    # !!!!!!!!! 2D cases !!!!!!!!!
                    xW = - gVal * np.sin(alphaRads)
                    yW = - gVal * np.cos(alphaRads)
                    f__.write(
                        f"element "
                        f"{key} "
                        f"{el['id']} "
                        f"{nodes} "
                        f"{thickness[phy]} "
                        f"PlaneStrain "
                        f"{mainSoilTags[phy]} "
                        f"0.0 "
                        f"0.0 "
                        f"{xW:.4f} "
                        f"{yW:.4f}\n"
                    )

                elif key == "quadUP":
                    thicknessQuadUP = {i: 1.0 for i in mainSoilTags}
                    bulkQuadUP = {i: 2.2e6 for i in mainSoilTags}
                    fMassQuadUP = {i: 1 for i in mainSoilTags}
                    hPerm = 5.0e-4
                    vPerm = 5.0e-4
                    alpha_ = 4  # in degrees already! always convert in radians
                    alpha_V = np.deg2rad(alpha_)
                    hPermQuadUP = {i: hPerm/(gVal * fMassQuadUP[i]) for i in mainSoilTags}
                    vPermQuadUP = {i: vPerm / (gVal * fMassQuadUP[i]) for i in mainSoilTags}
                    b1QuadUP = - gVal
                    b2QuadUP = - gVal * np.sin(alpha_V)
                    tQuadUP = 0.0
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

                elif key == "bbarQuadUP":
                    thicknessBbarQuadUP = {i: 1.0 for i in mainSoilTags}
                    bulkBbarQuadUP = {i: 2.2e6 for i in mainSoilTags}
                    fMassBbarQuadUP = {i: 1 for i in mainSoilTags}
                    hPermBbarQuadUP = 5.0e-4
                    vPermBbarQuadUP = 5.0e-4
                    alpha_ = 4  # in degrees already! always convert in radian
                    alpha_V = np.deg2rad(alpha_)
                    hPermBbarQuadUP = {i: hPermBbarQuadUP / (gVal * fMassBbarQuadUP[i]) for i in mainSoilTags}
                    vPermBbarQuadUP = {i: vPermBbarQuadUP / (gVal * fMassBbarQuadUP[i]) for i in mainSoilTags}
                    b1BbarQuadUP = - gVal
                    b2BbarQuadUP = - gVal * np.sin(alpha_V)
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

                elif key == "9_4_QuadUP":
                    thickness9_4_QuadUP = {i: 1.0 for i in mainSoilTags}
                    bulk9_4_QuadUP = {i: 2.2e6 for i in mainSoilTags}
                    fMass9_4_QuadUP = {i: 1 for i in mainSoilTags}
                    hPerm9_4_QuadUP = 5.0e-4
                    vPerm9_4_QuadUP = 5.0e-4
                    alpha_ = 4  # in degrees already! always convert in radians
                    alpha_V = np.deg2rad(alpha_)
                    hPerm9_4_QuadUP = {i: hPerm9_4_QuadUP / (gVal * fMass9_4_QuadUP[i]) for i in mainSoilTags}
                    vPerm9_4_QuadUP = {i: vPerm9_4_QuadUP / (gVal * fMass9_4_QuadUP[i]) for i in mainSoilTags}
                    b19_4_QuadUP = - gVal
                    b29_4_QuadUP = - gVal * np.sin(alpha_V)
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
                        f"{b29_4_QuadUP} "
                    )

                elif key == "brickUP":
                    # !!!!!!!!! 3D cases !!!!!!!!!
                    alpha__ = 0.0  # in degrees
                    alphaVal = np.deg2rad(alpha__)
                    bulkBrickUP = {i: 2.2e6 for i in mainSoilTags}
                    fMassBrickUP = {i: 1 for i in mainSoilTags}
                    PermXBrickUP = 5.0e-4
                    PermYBrickUP = 5.0e-4
                    PermZBrickUP = 5.0e-4
                    # alpha_ = 4 # in degrees already! always convert in degrees
                    PermXBrickUP = {i: PermXBrickUP / (gVal * fMassBrickUP[i]) for i in mainSoilTags}
                    PermYBrickUP = {i: PermYBrickUP / (gVal * fMassBrickUP[i]) for i in mainSoilTags}
                    PermZBrickUP = {i: PermZBrickUP / (gVal * fMassBrickUP[i]) for i in mainSoilTags}
                    gx = gVal * np.sin(alphaVal)
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

                elif key == "bbarBrickUP":
                    """
                    # !!!!!!!!! 3D cases !!!!!!!!!
                    """
                    alpha__ = 0.0  # in degrees
                    alphaVal = np.deg2rad(alpha__)
                    bulkBbarBrickUP = {i: 2.2e6 for i in mainSoilTags}
                    fMassBbarBrickUP = {i: 1 for i in mainSoilTags}
                    PermXBbarBrickUP = 5.0e-4
                    PermYBbarBrickUP = 5.0e-4
                    PermZBbarBrickUP = 5.0e-4
                    # alpha_ = 4 # in degrees already! always convert in degrees
                    PermXBbarBrickUP = {i: PermXBbarBrickUP / (gVal * fMassBbarBrickUP[i]) for i in mainSoilTags}
                    PermYBbarBrickUP = {i: PermYBbarBrickUP / (gVal * fMassBbarBrickUP[i]) for i in mainSoilTags}
                    PermZBbarBrickUP = {i: PermZBbarBrickUP / (gVal * fMassBbarBrickUP[i]) for i in mainSoilTags}
                    gx = gVal * np.sin(alphaVal)
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

                elif key == "20_8_BrickUP":
                    alpha__ = 0.0  # in degrees
                    alphaVal = np.deg2rad(alpha__)
                    bulk_20_8_BrickUP = {i: 2.2e6 for i in mainSoilTags}
                    fMass_20_8_BrickUP = {i: 1 for i in mainSoilTags}
                    PermX_20_8_BrickUP = 5.0e-4
                    PermY_20_8_BrickUP = 5.0e-4
                    PermZ_20_8_BrickUP = 5.0e-4
                    # alpha_ = 4 # in degrees already! always convert in degrees
                    PermX_20_8_BrickUP = {i: PermX_20_8_BrickUP / (gVal * fMass_20_8_BrickUP[i]) for i in mainSoilTags}
                    PermY_20_8_BrickUP = {i: PermY_20_8_BrickUP / (gVal * fMass_20_8_BrickUP[i]) for i in mainSoilTags}
                    PermZ_20_8_BrickUP = {i: PermZ_20_8_BrickUP / (gVal * fMass_20_8_BrickUP[i]) for i in mainSoilTags}
                    gx = gVal * np.sin(alphaVal)
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


def writeNodesTcl(nodeCoords_, ndmGlobal_, nodeDOFs_=None, filePrefix="nodes"):
    if nodeDOFs_ is None:
        nodeDOFs_ = {}
    """
    Writes node definition Tcl files for 2D or 3D models.
    Adds inline DOF info as comments, e.g. "# 3 DOFs (u,v,p)".
    """
    # choose filename
    fileName = f"{filePrefix}{'3D' if ndmGlobal_ == 3 else '2D'}.tcl"

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
          f"(comments show detected DOFs).")


def writeSeparatedNodeFiles(nodeCoords_, nodeDOFs_, ndmGlobal_, filePrefix="nodesByDOF"):
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

        fileName = f"{filePrefix}_{dofCountT}DOF.tcl"
        modelHeader = f"modelHeader_{dofCountT}DOF.tcl"

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
                    f__.write(f"node {n:<6} {x_:.6f} {y_:.6f}\n")
                else:
                    f__.write(f"node {n:<6} {x_:.6f} {y_:.6f} {z_:.6f}\n")

                # optional DOF comment
                label = {2: "(u,v)", 3: "(u,v,p)" if ndm == 2 else "(u,v,w)", 4: "(u,v,w,p)"}.get(dofCountT, "")
                f__.write(f"    # {dofCountT} DOFs {label}\n")

        written.append(fileName)

    # summary print that perhaps could be useful
    print("\nSummary by DOF group:")
    for k, v in dofGroups.items():
        print(f"  {k}-DOF nodes: {len(v)}")

    if any(len(v) for v in dofGroups.values()):
        print(f"✅ Wrote separated node files: {', '.join(written)}")
    else:
        print("⚠️ No node groups detected for separation.")


writeElementsTcl(elements, elementProfiles)
writeNodesTcl(nodeCoords, ndmGlobal, nodeDOFs)
writeSeparatedNodeFiles(nodeCoords, nodeDOFs, ndmGlobal)
