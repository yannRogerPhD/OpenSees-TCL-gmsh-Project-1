import os
from meshHelpF import (detectMaxPhyGroup, both2and3DOFs, threeDOFs, fourDOFs3D, twentyEightBrickDOFs,  # noqa: F401
    sortNodesByX, sortNodesByY, sortNodesByZ, writeNodesTcl, writeSeparatedNodeFiles, writeElementsTcl, outputFolder,
    only2DOFs, parseElementsFromMsh, parseNodesFromMsh, getBoundaryNodesFromMsh, writeMainTclGlobal, elementProfiles,
    filterElementsByDIM, remapElementTypes, summarizeRemaps, detect_ndm_ndf, classifyNodeDOFs, classifyChosenNodesByDOF,
    FuzzyFloat, selectNodes)

meshFile = "mod2.msh"
outDir = outputFolder(meshFile)

beam2DGrp = {50}  # physical groups for 2D beam elements
beam3DGrp = {}  # physical groups for 3D beam elements

sspBrickGrp = {}
bbarQuadUPGrp = {}
quadUPGrp = {}
bbarBrickGrp = {}
# sspBrickGrp = {1, 2, 3}, bbarBrickGrp = {} is for volumes instead

ASDLeftGrp, ASDRightGrp = {}, {}
ASDBottomGrp = {}
ASDBottomLeftGrp, ASDBottomRightGrp = {}, {}

lastVolume = 100
ASD3DBGrp = {lastVolume}
ASD3DLGrp, ASD3DRGrp = {lastVolume + 1}, {lastVolume + 2}
ASD3DFGrp, ASD3DKGrp = {lastVolume + 3}, {lastVolume + 4}
ASD3DBLGrp, ASD3DBRGrp = {lastVolume + 5}, {lastVolume + 6}
ASD3DBFGrp, ASD3DBKGrp = {lastVolume + 7}, {lastVolume + 8}
ASD3DLFGrp, ASD3DLKGrp = {lastVolume + 9}, {lastVolume + 10}
ASD3DRFGrp, ASD3DRKGrp = {lastVolume + 11}, {lastVolume + 12}
ASD3DBLFGrp, ASD3DBLKGrp = {lastVolume + 13}, {lastVolume + 14}
ASD3DBRFGrp, ASD3DBRKGrp = {lastVolume + 15}, {lastVolume + 16}

gVal = 9.806

maxPhyGroup = detectMaxPhyGroup(meshFile)
mainSoilTags = {i: i for i in range(1, maxPhyGroup + 1)}  # auto-build physical group tags based on mesh content
elements = parseElementsFromMsh(meshFile)

# -----------------------------------------------------------------------------------------------------------------
# Filter out and remap elements based on dimensionality and groups
# -----------------------------------------------------------------------------------------------------------------
elements, has3D = filterElementsByDIM(elements, beam2DGrp, beam3DGrp)
groupSets = {
    "beam2DGrp": beam2DGrp, "beam3DGrp": beam3DGrp, "bbarQuadUPGrp": bbarQuadUPGrp, "quadUPGrp": quadUPGrp,
    "bbarBrickGrp": bbarBrickGrp, "sspBrickGrp": sspBrickGrp, "ASDLeftGrp": ASDLeftGrp, "ASDBottomGrp": ASDBottomGrp,
    "ASDRightGrp": ASDRightGrp, "ASDBottomLeftGrp": ASDBottomLeftGrp, "ASDBottomRightGrp": ASDBottomRightGrp,
    "ASD3DLGrp": ASD3DLGrp, "ASD3DRGrp": ASD3DRGrp, "ASD3DKGrp": ASD3DKGrp, "ASD3DFGrp": ASD3DFGrp,
    "ASD3DBLGrp": ASD3DBLGrp, "ASD3DBRGrp": ASD3DBRGrp, "ASD3DBKGrp": ASD3DBKGrp, "ASD3DBFGrp": ASD3DBFGrp,
    "ASD3DLKGrp": ASD3DLKGrp, "ASD3DBLKGrp": ASD3DBLKGrp, "ASD3DRKGrp": ASD3DRKGrp, "ASD3DBRKGrp": ASD3DBRKGrp,
    "ASD3DLFGrp": ASD3DLFGrp, "ASD3DBLFGrp": ASD3DBLFGrp, "ASD3DRFGrp": ASD3DRFGrp, "ASD3DBRFGrp": ASD3DBRFGrp,
    "ASD3DBGrp": ASD3DBGrp
}

elements = remapElementTypes(elements, groupSets)
summarizeRemaps(elements)

# ----------------------------------------------------------------------------------------------------------------
# Detect ndm/ndf and classify node DOFs
# ----------------------------------------------------------------------------------------------------------------
ndmGlobal, ndfGlobal = detect_ndm_ndf(elements, elementProfiles)
nodeDOFs_soil, nodeDOFs_struct, nodeDOFs = classifyNodeDOFs(elements, elementProfiles, beam2DGrp, beam3DGrp)

twoDOFNodes = [n for n, d in nodeDOFs.items() if d == 2]
threeDOFNodes = [n for n, d in nodeDOFs.items() if d == 3]
fourDOFNodes = [n for n, d in nodeDOFs.items() if d == 4]

print(f"\nTotal nodes detected: {len(nodeDOFs)}")
print(f"  2-DOF nodes: {len(twoDOFNodes)}")
print(f"  3-DOF nodes: {len(threeDOFNodes)}")
print(f"  4-DOF nodes: {len(fourDOFNodes)}")

# -----------------------------------------------------------------------------------------------------------------
# Read node coordinates from Gmsh
# -----------------------------------------------------------------------------------------------------------------
nodeCoords = parseNodesFromMsh(meshFile)
print(f"Parsed {len(nodeCoords)} nodes from {meshFile}")

# -----------------------------------------------------------------------------------------------------------------
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Writing Outputs !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# -----------------------------------------------------------------------------------------------------------------
os.makedirs(outDir, exist_ok=True)

writeNodesTcl(nodeCoords, ndmGlobal, nodeDOFs, filePrefix="allSoilNodes",
              outputDir=outDir, elements=elements, elementProfileS=elementProfiles)

# soil nodes
if nodeDOFs_soil:
    # writeNodesTcl(nodeCoords, ndmGlobal, nodeDOFs_soil, filePrefix="AllSoilNodes", outputDir=outDir)
    writeSeparatedNodeFiles(nodeCoords, nodeDOFs_soil, ndmGlobal, outputDir=outDir, labelPrefix="soil")
#
# Structure nodes
if nodeDOFs_struct:
    # writeNodesTcl(nodeCoords, ndmGlobal, nodeDOFs_struct, filePrefix="structure_nodes", outputDir=outDir)
    writeSeparatedNodeFiles(nodeCoords, nodeDOFs_struct, ndmGlobal, outputDir=outDir, labelPrefix="structure")

# writeElementsTcl(elements, elementProfiles, mainSoilTags, gVal, outputDir=outDir)

# !!!!----
# select some particular group of nodes
phyGroupID = 29
boundaryNodes = getBoundaryNodesFromMsh(meshFile, phyGroupID=phyGroupID, dim=1)  # for example
boundaryNodes = sortNodesByZ(sortNodesByY(sortNodesByX(boundaryNodes, nodeCoords), nodeCoords), nodeCoords)
# print(f"Test nodes: {sortNodesByX(sortNodesByY(sortNodesByX(boundaryNodes, nodeCoords), nodeCoords), nodeCoords)}")
# !!!!----

# !!!!----
# select some particular group of nodes w.r.t. the DOF
dofOfSelectedNodes = 3
selectNodesDOF = classifyChosenNodesByDOF(boundaryNodes, nodeDOFs)
boundaryNodes3DOFs = selectNodesDOF.get(dofOfSelectedNodes, [])
# !!!!----

# !!!!----
# leftASDElements = [el["id"] for el in elements if el["type"] in {10031, 10032, 10033, 10034, 10035}]
# ASD3DElements = [el["id"] for el in elements
#                  if el["type"] in
#                  {10031, 10032, 10033, 10034, 10035, 10051, 10052, 10053, 10054, 10055, 10056, 10057, 10058, 10059,
#                   10060, 10061, 10062, 10063, 10064, 10065, 10066, 10067}]
#
# outputPath = os.path.join(outDir, 'leftASDUpdate.tcl')
#
# with open(outputPath, 'w') as f:
#     for i in leftASDElements:
#         f.write(f"setParameter -val 1 -ele {i} stage\n")
# !!!!----

# !!!!----
tryNodes = selectNodes(lambda x, y, z: x == 0.125, nodeCoords)
# !!!!----

# !!!!----
leftNodesT = getBoundaryNodesFromMsh(meshFile, phyGroupID=4, dim=1)
nodesDOFsLeftNodesT = classifyChosenNodesByDOF(leftNodesT, nodeDOFs)
# now extract 3-DOFs nodes
nodes3DOFsLeftNodesT = nodesDOFsLeftNodesT.get(3, [])
# print(nodes3DOFsLeftNodesT)

# now extract 2-DOFs nodes
nodes2DOFsLeftNodesT = nodesDOFsLeftNodesT.get(2, [])
# print(nodes2DOFsLeftNodesT)
# !!!!----
