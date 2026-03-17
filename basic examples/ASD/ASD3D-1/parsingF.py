import os
from meshHelpF import (sortNodesByX, sortNodesByY, both2and3DOFs, threeDOFs, fourDOFs3D, buildSSImap,  # noqa: F401
sortNodesByZ, writeNodesTcl, writeSeparatedNodeFiles, writeElementsTcl, outputFolder, twentyEightBrickDOFs, only2DOFs,
parseElementsFromMsh, parseNodesFromMsh, elementProfiles, filterElementsByDIM, remapElementTypes, summarizeRemaps,
detect_ndm_ndf, classifyNodeDOFs, classifyChosenNodesByDOF, selectNodes, defaultTol, detectSoilGroups,
classifySoilAndPileNodes, getAndSortGroupNodes, summarizeNodeDOFs, computeSoilBoundingBox, selectBuriedStructuralNodes)

meshFile = "model.msh"
verticalAxis = "z"
outDir = outputFolder(meshFile)
tol = defaultTol

beam2DGrp = {}
# beam3DGrp = {13, 14, 15, 16, 17}
beam3DGrp = {20335634}

sspBrickUPGrp = {}
sspBrickGrp = set(range(1, 101))
bbarQuadUPGrp = {}
quadUPGrp = {}
bbarBrickUPGrp = {}

# 2D absorbing Boundary conditions, order: B, L, R, BL, BR
lastVol2 = 1000042
ASDBottomGrp, ASDLeftGrp, ASDRightGrp, ASDBottomLeftGrp, ASDBottomRightGrp = {}, {}, {}, {}, {}

# 3D absorbing conditions, order: B, L, R, F, K, BL, BR, BF, BK, LF, LK, RF, RK, BLF, BLK, BRF, BRK
ASD3DBGrp = set(range(101, 126))
ASD3DLGrp = set(range(126, 146))
ASD3DRGrp = set(range(146, 166))
ASD3DFGrp = set(range(166, 186))
ASD3DKGrp = set(range(186, 206))
ASD3DBLGrp = set(range(206, 211))
ASD3DBRGrp = set(range(211, 216))
ASD3DBFGrp = set(range(216, 221))
ASD3DBKGrp = set(range(221, 226))
ASD3DLFGrp = set(range(226, 230))
ASD3DLKGrp = set(range(230, 234))
ASD3DRFGrp = set(range(234, 238))
ASD3DRKGrp = set(range(238, 242))
ASD3DBLFGrp = set(range(242, 243))
ASD3DBLKGrp = set(range(243, 244))
ASD3DBRFGrp = set(range(244, 245))
ASD3DBRKGrp = set(range(245, 246))

gVal = 9.806
elements = parseElementsFromMsh(meshFile)

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

soilTypes, soilGroups = detectSoilGroups(elements, has3D)
soilNodeSet, pileNodeSet = classifySoilAndPileNodes(elements, soilTypes, beam3DGrp)

# build mainSoilTags automatically
mainSoilTags = {g: g for g in sorted(soilGroups)}

print("\n[INFO] auto-detected soil physical groups:", sorted(soilGroups))
print("[INFO] mainSoilTags auto-built as:", mainSoilTags, "\n")

# --------------------------------------------------------------------------------------------------------------------
# USER MATERIAL REMAPPING: physical group --> material tag
# --------------------------------------------------------------------------------------------------------------------
customMaterialMap = {i: 1 for i in range(1, 101)}


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

summarizeNodeDOFs(nodeDOFs)

# ------------------------------------------------------------------------------------------------------------------
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Read node coordinates from Gmsh !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
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

writeElementsTcl(elements, elementProfiles, mainSoilTags, gVal, nodeCoords=nodeCoords, outputDir=outDir)

# !!!!----
# ASD2DElements = [el["id"] for el in elements if el["type"] in {10031, 10032, 10033, 10034, 10035}]
ASD3DElements = [el["id"] for el in elements if el["type"] in
                 {10031, 10032, 10033, 10034, 10035, 10051, 10052, 10053, 10054, 10055, 10056, 10057,
                 10058, 10059, 10060, 10061, 10062, 10063, 10064, 10065, 10066, 10067}]

# print(ASD3DElements)

with open("updateASD.tcl", "w") as fUpdate:
    for i in ASD3DElements:
        fUpdate.write(f"setParameter -val 1 -ele {i} stage\n")
# !!!!----

phyGroupID = 2
axesToSort = ("x", "y", "z")
boundaryNodes = getAndSortGroupNodes(meshFile, phyGroupID, nodeCoords, axes=axesToSort, dim=1)

# ------------------------------------------------------------------------------------------------------------------
# SSI PREPARATION: soil bounding box + selecting buried structural nodes
# ------------------------------------------------------------------------------------------------------------------

soil_bbox = computeSoilBoundingBox(soilNodeSet, nodeCoords)
print("[DEBUG] Soil bounding box:", soil_bbox)

structuralNodeSet = set(nodeDOFs_struct.keys())
print("[DEBUG] structural nodes:", len(structuralNodeSet))

buriedStructuralNodes = selectBuriedStructuralNodes(structuralNodeSet, soil_bbox, nodeCoords, tol)
print("[DEBUG] buried structural nodes:", len(buriedStructuralNodes))

# !!
SSI_map = buildSSImap(buriedStructuralNodes, elements, soilTypes, nodeCoords, verticalAxis=verticalAxis, tol_=tol)

print("[SSI] node --> soil faces mapping:")
for sNode, soilNodes in SSI_map.items():
    print(f"  structural node {sNode}: {soilNodes}")

# print(ASD3DBGrp)
