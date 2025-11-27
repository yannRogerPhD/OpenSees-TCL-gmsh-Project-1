import os

from meshHelpF import (
    outputFolder, sortNodesByX, sortNodesByY, sortNodesByZ, writeNodesTcl, writeSeparatedNodeFiles, writeElementsTcl,
    only2DOFs, parseElementsFromMsh, parseNodesFromMsh, detectMaxPhyGroup, getBoundaryNodesFromMsh,  # noqa: F401
    writeMainTclGlobal, both2and3DOFs, threeDOFs, fourDOFs3D, twentyEightBrickDOFs, elementProfiles  # noqa: F401
)

# noqa: F401
meshFile = "model3D.msh"

# time series in both directions
tsX = 1
tsY = 2

# prepare output folder once
outDir = outputFolder(meshFile)

beam2DGrp = {}  # physical groups for 2D beam elements
beam3DGrp = {30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45}  # physical groups for 3D beam elements

sspBrickGrp = {}
bbarQuadUPGrp = {}
quadUPGrp = {}
bbarBrickGrp = {}
# sspBrickGrp = {1, 2, 3}, bbarBrickGrp = {} is for volumes instead

ASDLeftGrp = {}
ASDRightGrp = {}
ASDBottomGrp = {}
ASDBottomLeftGrp = {}
ASDBottomRightGrp = {}

ASD3DBGrp = {}
ASD3DLGrp = {}
ASD3DRGrp = {}
ASD3DFGrp = {}
ASD3DKGrp = {}
ASD3DBLGrp = {}
ASD3DBRGrp = {}
ASD3DBFGrp = {}
ASD3DBKGrp = {}
ASD3DLFGrp = {}
ASD3DLKGrp = {}
ASD3DRFGrp = {}
ASD3DRKGrp = {}
ASD3DBLFGrp = {}
ASD3DBLKGrp = {}
ASD3DBRFGrp = {}
ASD3DBRKGrp = {}

gVal = 9.806

maxPhyGroup = detectMaxPhyGroup(meshFile)  # detect the maximum physical group ID directly from mesh

mainSoilTags = {i: i for i in range(1, maxPhyGroup + 1)}  # auto-build physical group tags based on mesh content

elements = parseElementsFromMsh(meshFile)

# -----------------------------------------------------------
# Filter out 2D surface elements when 3D volumes are present
# -----------------------------------------------------------

has3D = any(el["type"] in (5, 105, 1005,
                           10051, 10052, 10053, 10054, 10055, 10056, 10057, 10058, 10059,
                           10060, 10061, 10062, 10063, 10064, 10065, 10066, 10067,
                           17
                           )
            for el in elements)

if has3D:
    elements = [
        el for el in elements
        if el["type"] in (5, 105, 1005,
                          10051, 10052, 10053, 10054, 10055, 10056, 10057, 10058, 10059,
                          10060, 10061, 10062, 10063, 10064, 10065, 10066, 10067,
                          17
                          )
        # keep beam lines (type 1) only if their group is listed
        or (el["type"] == 1 and (el["group"] in beam2DGrp or el["group"] in beam3DGrp))
    ]
    print("Detected 3D mesh -> ignoring surface elements (type 3)...")

else:
    # purely 2D model: keep all 2D elements and any beam2D groups
    elements = [
        el for el in elements
        if el["type"] in (1, 3, 10, 103, 1003)
        and (el["type"] != 1 or el["group"] in beam2DGrp)
    ]
    print("Detected 2D mesh -> keeping quads and beam line groups only...")

for el in elements:

    # beam elements (1D)
    if el["type"] == 1:
        if el["group"] in beam2DGrp:
            el["type"] = 1  # 2D elasticBeamColumn
        elif el["group"] in beam3DGrp:
            el["type"] = 101  # 3D elasticBeamColumn
        else:
            # skip other 2-node lines (edges, boundaries, etc.)
            continue

    # general 2D elements
    if el["type"] == 3:
        if el["group"] in bbarQuadUPGrp:
            el["type"] = 103  # 2D bbarQuadUP
        elif el["group"] in quadUPGrp:
            el["type"] = 1003  # 2D quadUP

        # 2D ASD absorbing boundaries
        elif el["group"] in ASDLeftGrp:
            el["type"] = 10031
        elif el["group"] in ASDBottomGrp:
            el["type"] = 10032
        elif el["group"] in ASDRightGrp:
            el["type"] = 10033
        elif el["group"] in ASDBottomLeftGrp:
            el["type"] = 10034
        elif el["group"] in ASDBottomRightGrp:
            el["type"] = 10035

    # general 3D elements
    elif el["type"] == 5 and el["group"] in bbarBrickGrp:
        el["type"] = 105  # 3D bbarBrickUP
    elif el["type"] == 5 and el["group"] in sspBrickGrp:
        el["type"] = 1005  # 3D SSPbrickUP
    elif el["type"] == 5 and el["group"] in ASD3DLGrp:
        el["type"] = 10051  # 3D ASD3DLGrp
    elif el["type"] == 5 and el["group"] in ASD3DRGrp:
        el["type"] = 10052  # 3D ASD3DRGrp
    elif el["type"] == 5 and el["group"] in ASD3DKGrp:
        el["type"] = 10053  # 3D ASD3DKGrp
    elif el["type"] == 5 and el["group"] in ASD3DFGrp:
        el["type"] = 10054  # 3D ASD3DFGrp
    elif el["type"] == 5 and el["group"] in ASD3DBLGrp:
        el["type"] = 10055  # 3D ASD3DBLGrp
    elif el["type"] == 5 and el["group"] in ASD3DBRGrp:
        el["type"] = 10056  # 3D ASD3DBRGrp
    elif el["type"] == 5 and el["group"] in ASD3DBKGrp:
        el["type"] = 10057  # 3D ASD3DBKGrp
    elif el["type"] == 5 and el["group"] in ASD3DBFGrp:
        el["type"] = 10058  # 3D ASD3DBFGrp
    elif el["type"] == 5 and el["group"] in ASD3DLKGrp:
        el["type"] = 10059  # 3D ASD3DLKGrp
    elif el["type"] == 5 and el["group"] in ASD3DBLKGrp:
        el["type"] = 10060  # 3D ASD3DBLKGrp
    elif el["type"] == 5 and el["group"] in ASD3DRKGrp:
        el["type"] = 10061  # 3D ASD3DRKGrp
    elif el["type"] == 5 and el["group"] in ASD3DBRKGrp:
        el["type"] = 10062  # 3D ASD3DBRKGrp
    elif el["type"] == 5 and el["group"] in ASD3DLFGrp:
        el["type"] = 10063  # 3D ASD3DLFGrp
    elif el["type"] == 5 and el["group"] in ASD3DBLFGrp:
        el["type"] = 10064  # 3D ASD3DBLFGrp
    elif el["type"] == 5 and el["group"] in ASD3DRFGrp:
        el["type"] = 10065  # 3D ASD3DRFGrp
    elif el["type"] == 5 and el["group"] in ASD3DBRFGrp:
        el["type"] = 10066  # 3D ASD3DBRFGrp
    elif el["type"] == 5 and el["group"] in ASD3DBGrp:
        el["type"] = 10067  # 3D ASD3DBGrp

# summary mappings 2D
mappedBbar = sum(el["type"] == 103 for el in elements)
mappedQuadUP = sum(el["type"] == 1003 for el in elements)
mappedASDLeft = sum(el["type"] == 10031 for el in elements)
mappedASDBottom = sum(el["type"] == 10032 for el in elements)
mappedASDRight = sum(el["type"] == 10033 for el in elements)
mappedASDBottomLeft = sum(el["type"] == 10034 for el in elements)
mappedASDBottomRight = sum(el["type"] == 10035 for el in elements)

# summary mappings 3D
mappedBbarBrickUP = sum(el["type"] == 105 for el in elements)
mappedSSPBrickUP = sum(el["type"] == 1005 for el in elements)
mappedASD3DL = sum(el["type"] == 10051 for el in elements)

if mappedBbar:
    print(f"Remapped {mappedBbar} elements → bbarQuadUP (103)")
if mappedQuadUP:
    print(f"Remapped {mappedQuadUP} elements → quadUP (1003)")
if mappedASDLeft:
    print(f"Remapped {mappedASDLeft} elements → ASDAbsorbingBoundary Left (10031)")
if mappedASDBottom:
    print(f"Remapped {mappedASDBottom} elements → ASDAbsorbingBoundary Bottom (10032)")
if mappedASDRight:
    print(f"Remapped {mappedASDRight} elements → ASDAbsorbingBoundary Right (10033)")
if mappedASDBottomLeft:
    print(f"Remapped {mappedASDBottomLeft} elements → ASDAbsorbingBoundary BottomLeft (10034)")
if mappedASDBottomRight:
    print(f"Remapped {mappedASDBottomRight} elements → ASDAbsorbingBoundary BottomRight (10035)")

if mappedBbarBrickUP:
    print(f"Remapped {mappedBbarBrickUP} elements → bbarBrickUP (105)")
if mappedSSPBrickUP:
    print(f"Remapped {mappedSSPBrickUP} elements → SSPbrickUP (1005)")

# Detect element types and compute ndm / ndf
usedProfiles = {el["type"] for el in elements if el["type"] in elementProfiles}
print()
print("usedProfiles:", usedProfiles)

if usedProfiles:
    ndmGlobal = max(elementProfiles[t]["ndm"] for t in usedProfiles)

    # Check the presence of element families
    hasUP = any(elementProfiles[t]["needsP"] for t in usedProfiles)
    hasBeam2D = any(elementProfiles[t]["key"] == "elasticBeamColumn2D" for t in usedProfiles)
    hasBeam3D = any(elementProfiles[t]["key"] == "elasticBeamColumn3D" for t in usedProfiles)

    # print(hasBeam2D)

    # Decide ndfGlobal
    if ndmGlobal == 2:
        if hasBeam2D:
            ndfGlobal = 3  # (u, v, θz)
        elif hasUP:
            ndfGlobal = 3  # (u, v, p)
        else:
            ndfGlobal = 2  # (u, v)
    elif ndmGlobal == 3:
        if hasBeam3D:
            ndfGlobal = 6  # (u, v, w, θx, θy, θz)
        elif hasUP:
            ndfGlobal = 4  # (u, v, w, p)
        else:
            ndfGlobal = 3  # (u, v, w)
    else:
        ndmGlobal, ndfGlobal = 2, 2
else:
    ndmGlobal, ndfGlobal = 2, 2


# print(f"Detected ndmGlobal = {ndmGlobal}, ndfGlobal = {ndfGlobal}")

nodeDOFs_soil = {}
nodeDOFs_struct = {}

for el in elements:
    eType = el["type"]
    if eType not in elementProfiles:
        continue

    ruleFunc = elementProfiles[eType]["dofRule"]
    dofMap = ruleFunc(el["nodes"])

    # classify as structure or soil by group membership
    if el["group"] in beam2DGrp or el["group"] in beam3DGrp:
        for nodeTag, dofCount in dofMap.items():
            if nodeTag not in nodeDOFs_struct or dofCount > nodeDOFs_struct[nodeTag]:
                nodeDOFs_struct[nodeTag] = dofCount
    else:
        for nodeTag, dofCount in dofMap.items():
            if nodeTag not in nodeDOFs_soil or dofCount > nodeDOFs_soil[nodeTag]:
                nodeDOFs_soil[nodeTag] = dofCount

# merge them only for reporting total counts
nodeDOFs = {**nodeDOFs_soil, **nodeDOFs_struct}


# summarize
twoDOFNodes = [n for n, d in nodeDOFs.items() if d == 2]
threeDOFNodes = [n for n, d in nodeDOFs.items() if d == 3]
fourDOFNodes = [n for n, d in nodeDOFs.items() if d == 4]

print(f"\nTotal nodes detected: {len(nodeDOFs)}")
print(f"  2-DOF nodes: {len(twoDOFNodes)}")
print(f"  3-DOF nodes: {len(threeDOFNodes)}")
print(f"  4-DOF nodes: {len(fourDOFNodes)}")

# -------------------------------------------------------
# Read node coordinates from Gmsh
# -------------------------------------------------------
nodeCoords = parseNodesFromMsh(meshFile)
print(f"✅ Parsed {len(nodeCoords)} nodes from {meshFile}")

# ============================================================
# Write main TCL files
# ============================================================

print("\n─────────────────────────────────────── Writing Outputs ───────────────────────────────────────")
os.makedirs(outDir, exist_ok=True)

# nodes
# Soil nodes
if nodeDOFs_soil:
    writeNodesTcl(nodeCoords, ndmGlobal, nodeDOFs_soil, filePrefix="AllSoilNodes", outputDir=outDir)
    writeSeparatedNodeFiles(nodeCoords, nodeDOFs_soil, ndmGlobal, outputDir=outDir, labelPrefix="soil")

# Structure nodes
if nodeDOFs_struct:
    # writeNodesTcl(nodeCoords, ndmGlobal, nodeDOFs_struct, filePrefix="structure_nodes", outputDir=outDir)
    writeSeparatedNodeFiles(nodeCoords, nodeDOFs_struct, ndmGlobal, outputDir=outDir, labelPrefix="structure")

print("✅ Node files written.")

writeElementsTcl(elements, elementProfiles, mainSoilTags, gVal,
                 outputDir=outDir)


print("───────────────────────────────────────────────────────────────────────────────────────────────")
print("✅ Essential outputs successfully written.\n")

# ============================================================
# Guides: Defining boundaries and constraints (examples)
# ============================================================


# if __name__ == "__main__":
#     writeMainTclGlobal(
#         tclRootDir="TCL-Files",
#         modelName=os.path.splitext(os.path.basename(meshFile))[0],
#         damp=0.02,
#         fLower=0.2,
#         fHigher=20.0,
#         gamma=0.5,
#         beta=0.25
#     )

phyGroupID = 29
boundaryNodes = getBoundaryNodesFromMsh(meshFile, phyGroupID=phyGroupID, dim=1)  # for example
boundaryNodes = sortNodesByZ(sortNodesByY(sortNodesByX(boundaryNodes, nodeCoords), nodeCoords), nodeCoords)
print(f"Test nodes are: {sortNodesByX(sortNodesByY(sortNodesByX(boundaryNodes, nodeCoords), nodeCoords), nodeCoords)}")

# leftASDElements = [el["id"] for el in elements if el["type"] == 10031]
#
# outputPath = os.path.join(outDir, 'leftASDUpdate.tcl')
#
# with open(outputPath, 'w') as f:
#     for i in leftASDElements:
#         f.write(f"setParameter -val 1 -ele {i} stage\n")
