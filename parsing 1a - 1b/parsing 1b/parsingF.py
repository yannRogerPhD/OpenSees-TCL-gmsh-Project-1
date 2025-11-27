import os
from meshHelpF import (detectMaxPhyGroup, both2and3DOFs, threeDOFs, fourDOFs3D, twentyEightBrickDOFs,  # noqa: F401
sortNodesByX, sortNodesByY, sortNodesByZ, writeNodesTcl, writeSeparatedNodeFiles, writeElementsTcl, outputFolder,
only2DOFs, parseElementsFromMsh, parseNodesFromMsh, getBoundaryNodesFromMsh, writeMainTclGlobal, elementProfiles,
filterElementsByDIM, remapElementTypes, summarizeRemaps, detect_ndm_ndf, classifyNodeDOFs, classifyChosenNodesByDOF,
FuzzyFloat, selectNodes, defaultTolerance, _roundFunc, soilFaceNodesAroundPile)

meshFile = "model3D.msh"
outDir = outputFolder(meshFile)

beam2DGrp = {}  # physical groups for 2D beam elements
beam3DGrp = {13, 14}  # physical groups for 3D beam elements

sspBrickUPGrp = {1}
sspBrickGrp = {}
bbarQuadUPGrp = {}
quadUPGrp = {}
bbarBrickUPGrp = {}
# sspBrickUPGrp = {1, 2, 3}, bbarBrickUPGrp = {} is for volumes instead

ASDLeftGrp, ASDRightGrp = {}, {}
ASDBottomGrp = {}
ASDBottomLeftGrp, ASDBottomRightGrp = {}, {}

lastVol = 1000043
ASD3DBGrp = {lastVol}
ASD3DLGrp, ASD3DRGrp, ASD3DFGrp, ASD3DKGrp = {lastVol + 1}, {lastVol + 2}, {lastVol + 3}, {lastVol + 4}
ASD3DBLGrp, ASD3DBRGrp, ASD3DBFGrp, ASD3DBKGrp = {lastVol + 5}, {lastVol + 6}, {lastVol + 7}, {lastVol + 8}
ASD3DLFGrp, ASD3DLKGrp, ASD3DRFGrp, ASD3DRKGrp = {lastVol + 9}, {lastVol + 10}, {lastVol + 11}, {lastVol + 12}
ASD3DBLFGrp, ASD3DBLKGrp, ASD3DBRFGrp, ASD3DBRKGrp = {lastVol + 13}, {lastVol + 14}, {lastVol + 15}, {lastVol + 16}

gVal = 9.806
elements = parseElementsFromMsh(meshFile)

# -------------------------------------------------------------------------------------------------------------------
# Filter out and remap elements based on dimensionality and groups
# -------------------------------------------------------------------------------------------------------------------
elements, has3D = filterElementsByDIM(elements, beam2DGrp, beam3DGrp)
groupSets = {
    "beam2DGrp": beam2DGrp, "beam3DGrp": beam3DGrp, "bbarQuadUPGrp": bbarQuadUPGrp, "quadUPGrp": quadUPGrp,
    "bbarBrickUPGrp": bbarBrickUPGrp, "sspBrickUPGrp": sspBrickUPGrp, "sspBrickGrp": sspBrickGrp,
    "ASDLeftGrp": ASDLeftGrp, "ASDBottomGrp": ASDBottomGrp, "ASDRightGrp": ASDRightGrp,
    "ASDBottomLeftGrp": ASDBottomLeftGrp, "ASDBottomRightGrp": ASDBottomRightGrp, "ASD3DBGrp": ASD3DBGrp,
    "ASD3DLGrp": ASD3DLGrp, "ASD3DRGrp": ASD3DRGrp, "ASD3DKGrp": ASD3DKGrp, "ASD3DFGrp": ASD3DFGrp,
    "ASD3DBLGrp": ASD3DBLGrp, "ASD3DBRGrp": ASD3DBRGrp, "ASD3DBKGrp": ASD3DBKGrp, "ASD3DBFGrp": ASD3DBFGrp,
    "ASD3DLKGrp": ASD3DLKGrp, "ASD3DBLKGrp": ASD3DBLKGrp, "ASD3DRKGrp": ASD3DRKGrp, "ASD3DBRKGrp": ASD3DBRKGrp,
    "ASD3DLFGrp": ASD3DLFGrp, "ASD3DBLFGrp": ASD3DBLFGrp, "ASD3DRFGrp": ASD3DRFGrp, "ASD3DBRFGrp": ASD3DBRFGrp
}

elements = remapElementTypes(elements, groupSets)
summarizeRemaps(elements)

# -------------------------------------------------------------------------------------------------------------------
# automatic soil group detection
# -------------------------------------------------------------------------------------------------------------------
soil2D_types = {3, 10, 103, 1003}
soil3D_types = {5, 17, 105, 1005, 1055}
soilTypes = soil3D_types if has3D else soil2D_types

# extract only soil groups from the mesh
soilGroups = {el["group"] for el in elements if el["type"] in soilTypes}

# -------------------------------------------------------------------------------------------------------------------
# !!! node sets for soil and structure (for SSI purposes) !!!
# all nodes that belong to soil elements
soilNodeSet = {n for el in elements if el["type"] in soilTypes for n in el["nodes"]}

# elements that are 3D beams (piles) – using physical groups in beam3DGrp
pileElemts = [el for el in elements if el["type"] == 101 and el["group"] in beam3DGrp]

# node set on piles
pileNodeSet = {n for el in pileElemts for n in el["nodes"]}
# -------------------------------------------------------------------------------------------------------------------


# build mainSoilTags automatically
mainSoilTags = {g: g for g in sorted(soilGroups)}

print("\n[INFO] auto-detected soil physical groups:", sorted(soilGroups))
print("[INFO] mainSoilTags auto-built as:", mainSoilTags, "\n")


# --------------------------------------------------------------------------------------------------------------------
# USER MATERIAL REMAPPING: physical group --> material tag
# --------------------------------------------------------------------------------------------------------------------
customMaterialMap = {
    1: 5,
    2: 4,
    3: 2,
    # etc.
}

for phy, mat in customMaterialMap.items():
    if phy in mainSoilTags:
        mainSoilTags[phy] = mat
    else:
        print(f"[Warning] physical group {phy} not found in mesh/not soil; ignoring.")

# ------------------------------------------------------------------------------------------------------------------
# Detect ndm/ndf and classify node DOFs
# ------------------------------------------------------------------------------------------------------------------
ndmGlobal, ndfGlobal = detect_ndm_ndf(elements, elementProfiles)
nodeDOFs_soil, nodeDOFs_struct, nodeDOFs = classifyNodeDOFs(elements, elementProfiles, beam2DGrp, beam3DGrp)

twoDOFNodes = [n for n, d in nodeDOFs.items() if d == 2]
threeDOFNodes = [n for n, d in nodeDOFs.items() if d == 3]
fourDOFNodes = [n for n, d in nodeDOFs.items() if d == 4]

print(f"\nTotal nodes detected: {len(nodeDOFs)}")
print(f"  2-DOF nodes: {len(twoDOFNodes)}")
print(f"  3-DOF nodes: {len(threeDOFNodes)}")
print(f"  4-DOF nodes: {len(fourDOFNodes)}")

# ------------------------------------------------------------------------------------------------------------------
# Read node coordinates from Gmsh
# ------------------------------------------------------------------------------------------------------------------
nodeCoords = parseNodesFromMsh(meshFile)
print(f"Parsed {len(nodeCoords)} nodes from {meshFile}")

# ------------------------------------------------------------------------------------------------------------------
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Writing Outputs !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# ------------------------------------------------------------------------------------------------------------------
os.makedirs(outDir, exist_ok=True)

writeNodesTcl(nodeCoords, ndmGlobal, nodeDOFs, filePrefix="allSoilNodes",
              outputDir=outDir, elements=elements, elementProfileS=elementProfiles)

# soil nodes
if nodeDOFs_soil:
    writeSeparatedNodeFiles(nodeCoords, nodeDOFs_soil, ndmGlobal, outputDir=outDir, labelPrefix="soil")
#
# structure nodes
if nodeDOFs_struct:
    writeSeparatedNodeFiles(nodeCoords, nodeDOFs_struct, ndmGlobal, outputDir=outDir, labelPrefix="structure")

writeElementsTcl(elements, elementProfiles, mainSoilTags, gVal, outputDir=outDir)

# !!!!----
# select some particular group of nodes
phyGroupID = 29
boundaryNodes = getBoundaryNodesFromMsh(meshFile, phyGroupID=phyGroupID, dim=1)  # for example
boundaryNodes = sortNodesByZ(sortNodesByY(sortNodesByX(boundaryNodes, nodeCoords), nodeCoords), nodeCoords)
# print(f"Test nodes: {sortNodesByX(sortNodesByY(sortNodesByX(boundaryNodes, nodeCoords), nodeCoords), nodeCoords)}")
# !!!!----

# !!!!----
# leftASDElements = [el["id"] for el in elements if el["type"] in {10031, 10032, 10033, 10034, 10035}]
# ASD3DElements = [el["id"] for el in elements if el["type"] in
#                  {10031, 10032, 10033, 10034, 10035, 10051, 10052, 10053, 10054, 10055, 10056, 10057,
#                  10058, 10059, 10060, 10061, 10062, 10063, 10064, 10065, 10066, 10067}]
# !!!!----

print(sortNodesByY(pileNodeSet, nodeCoords))

tol = defaultTolerance

soilByY, pileByY = {}, {}

for n in soilNodeSet:
    x_, y_, z_ = nodeCoords[n]
    yKey = _roundFunc(y_, tol)
    soilByY.setdefault(yKey, []).append(n)

for n in pileNodeSet:
    x_, y_, z_ = nodeCoords[n]
    yKey = _roundFunc(y_, tol)
    pileByY.setdefault(yKey, []).append(n)

print(f"[SSI] z-layers with soil: {len(soilByY)}")
print(f"[SSI] z-layers with pile: {len(pileByY)}")


# SSI_map: pileNode --> list of surrounding soil node IDs
SSI_map = {}

for pNode in pileNodeSet:
    ring_nodes = soilFaceNodesAroundPile(
        pNode,
        elements,
        soilTypes,
        nodeCoords,
    )
    SSI_map[pNode] = ring_nodes

print("[SSI] mapping pile --> soil (pile node -> soil face nodes):")
for pNode, sNodes in SSI_map.items():
    print(f"  pile node {pNode}: {sNodes}")
