import os
from meshHelpF import (sortNodesByX, sortNodesByY, both2and3DOFs, threeDOFs, fourDOFs3D, buildSSImap,  # noqa: F401
sortNodesByZ, writeNodesTcl, writeSeparatedNodeFiles, writeElementsTcl, outputFolder, twentyEightBrickDOFs, only2DOFs,
parseElementsFromMsh, parseNodesFromMsh, elementProfiles, filterElementsByDIM, remapElementTypes, summarizeRemaps,
detect_ndm_ndf, classifyNodeDOFs, classifyChosenNodesByDOF, selectNodes, defaultTol, detectSoilGroups,
classifySoilAndPileNodes, getAndSortGroupNodes, summarizeNodeDOFs, computeSoilBoundingBox, selectBuriedStructuralNodes)

meshFile = "modelISS.msh"
verticalAxis = "z"
outDir = outputFolder(meshFile)
tol = defaultTol

beam2DGrp = {}
beam3DGrp = {13, 14, 15, 16, 17, 20}

sspBrickUPGrp = {1}
sspBrickGrp = {}
bbarQuadUPGrp = {}
quadUPGrp = {}
bbarBrickUPGrp = {}

# 2D absorbing Boundary conditions, order: B, L, R, BL, BR
lastVol2 = 1000042
ASDBottomGrp, ASDLeftGrp, ASDRightGrp, ASDBottomLeftGrp, ASDBottomRightGrp = {}, {}, {}, {}, {}

# 3D absorbing conditions, order: B, L, R, F, K, BL, BR, BF, BK, LF, LK, RF, RK, BLF, BLK, BRF, BRK
lastVol3 = 1000043
ASD3DBGrp = {lastVol3}
ASD3DLGrp, ASD3DRGrp, ASD3DFGrp, ASD3DKGrp = {lastVol3 + 1}, {lastVol3 + 2}, {lastVol3 + 3}, {lastVol3 + 4}
ASD3DBLGrp, ASD3DBRGrp, ASD3DBFGrp, ASD3DBKGrp = {lastVol3 + 5}, {lastVol3 + 6}, {lastVol3 + 7}, {lastVol3 + 8}
ASD3DLFGrp, ASD3DLKGrp, ASD3DRFGrp, ASD3DRKGrp = {lastVol3 + 9}, {lastVol3 + 10}, {lastVol3 + 11}, {lastVol3 + 12}
ASD3DBLFGrp, ASD3DBLKGrp, ASD3DBRFGrp, ASD3DBRKGrp = {lastVol3 + 13}, {lastVol3 + 14}, {lastVol3 + 15}, {lastVol3 + 16}

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

writeElementsTcl(elements, elementProfiles, mainSoilTags, gVal, outputDir=outDir)

# !!!!----
# leftASDElements = [el["id"] for el in elements if el["type"] in {10031, 10032, 10033, 10034, 10035}]
# ASD3DElements = [el["id"] for el in elements if el["type"] in
#                  {10031, 10032, 10033, 10034, 10035, 10051, 10052, 10053, 10054, 10055, 10056, 10057,
#                  10058, 10059, 10060, 10061, 10062, 10063, 10064, 10065, 10066, 10067}]
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
