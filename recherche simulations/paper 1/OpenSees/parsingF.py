import os
from meshHelpF import (sortNodesByX, sortNodesByY, both2and3DOFs, threeDOFs, fourDOFs3D, buildSSImap,  # noqa: F401
sortNodesByZ, writeNodesTcl, writeSeparatedNodeFiles, writeElementsTcl, outputFolder, twentyEightBrickDOFs, only2DOFs,
parseElementsFromMsh, parseNodesFromMsh, elementProfiles, filterElementsByDIM, remapElementTypes, summarizeRemaps,
detect_ndm_ndf, classifyNodeDOFs, classifyChosenNodesByDOF, selectNodes, detectSoilGroups, findTetrahedronForPileNode,
classifySoilAndPileNodes, getAndSortGroupNodes, summarizeNodeDOFs, computeSoilBoundingBox, selectBuriedStructuralNodes,
isPointInTetrahedron, decomposeBrickIntoTetrahedra, writeEmbeddedElementsForBricks, generatePileInterfaceForBricks,
computePileNormal, writeContactElements, defaultTol, generateVariablePermeabilityFiles, generateAdaptiveAnalysisTcl)

meshFile = "model.msh"
verticalAxis = "z"
outDir = outputFolder(meshFile)
tol = defaultTol

beam2DGrp = set()
beam3DGrp = set()
dispBeam2DGrp = set()
dispBeam3DGrp = {1630, 1631}

sspBrickUPGrp = set(range(1, 181))
sspBrickGrp = set()
bbarQuadUPGrp = set()
quadUPGrp = set()
bbarBrickUPGrp = set()

# 2D absorbing Boundary conditions, order: B, L, R, BL, BR
lastVol2 = 1000042
ASDBottomGrp, ASDLeftGrp, ASDRightGrp, ASDBottomLeftGrp, ASDBottomRightGrp = set(), set(), set(), set(), set()

# 3D absorbing conditions, order: B, L, R, F, K, BL, BR, BF, BK, LF, LK, RF, RK, BLF, BLK, BRF, BRK
lastVol3 = 2
# 3D absorbing conditions, order: B, L, R, F, K, BL, BR, BF, BK, LF, LK, RF, RK, BLF, BLK, BRF, BRK
ASD3DBGrp = set(range(181, 241))
ASD3DLGrp = set(range(241, 259))
ASD3DRGrp = set(range(259, 277))
ASD3DFGrp = set(range(277, 307))
ASD3DKGrp = set(range(307, 337))
ASD3DBLGrp = set(range(337, 343))
ASD3DBRGrp = set(range(343, 349))
ASD3DBFGrp = set(range(349, 359))
ASD3DBKGrp = set(range(359, 369))
ASD3DLFGrp = set(range(369, 372))
ASD3DLKGrp = set(range(372, 375))
ASD3DRFGrp = set(range(375, 378))
ASD3DRKGrp = set(range(378, 381))
ASD3DBLFGrp = set(range(381, 382))
ASD3DBLKGrp = set(range(382, 383))
ASD3DBRFGrp = set(range(383, 384))
ASD3DBRKGrp = set(range(384, 385))

gVal = 9.806
elements = parseElementsFromMsh(meshFile)

beam2D_all = set(beam2DGrp) | set(dispBeam2DGrp)
beam3D_all = set(beam3DGrp) | set(dispBeam3DGrp)
elements, has3D = filterElementsByDIM(elements, beam2D_all, beam3D_all)

groupSets = {
    "beam2DGrp": beam2DGrp, "beam3DGrp": beam3DGrp, "bbarQuadUPGrp": bbarQuadUPGrp, "bbarBrickUPGrp": bbarBrickUPGrp,
    "sspBrickUPGrp": sspBrickUPGrp, "sspBrickGrp": sspBrickGrp, "quadUPGrp": quadUPGrp, "ASDLeftGrp": ASDLeftGrp,
    "ASDBottomGrp": ASDBottomGrp, "ASDRightGrp": ASDRightGrp, "ASDBottomLeftGrp": ASDBottomLeftGrp, "ASDBottomRightGrp":
    ASDBottomRightGrp, "ASD3DBGrp": ASD3DBGrp, "ASD3DLGrp": ASD3DLGrp, "ASD3DRGrp": ASD3DRGrp, "ASD3DKGrp": ASD3DKGrp,
    "ASD3DFGrp": ASD3DFGrp, "ASD3DBLGrp": ASD3DBLGrp, "ASD3DBRGrp": ASD3DBRGrp, "ASD3DBKGrp": ASD3DBKGrp, "ASD3DBFGrp":
    ASD3DBFGrp, "ASD3DLKGrp": ASD3DLKGrp, "ASD3DBLKGrp": ASD3DBLKGrp, "ASD3DRKGrp": ASD3DRKGrp, "ASD3DBRKGrp":
    ASD3DBRKGrp, "ASD3DLFGrp": ASD3DLFGrp, "ASD3DBLFGrp": ASD3DBLFGrp, "ASD3DRFGrp": ASD3DRFGrp, "ASD3DBRFGrp":
    ASD3DBRFGrp, "dispBeam2DGrp": dispBeam2DGrp, "dispBeam3DGrp": dispBeam3DGrp,
}

elements = remapElementTypes(elements, groupSets)
summarizeRemaps(elements)

soilTypes, soilGroups = detectSoilGroups(elements, has3D)
soilNodeSet, pileNodeSet = classifySoilAndPileNodes(elements, soilTypes, beam3D_all)

# build mainSoilTags automatically
mainSoilTags = {g: g for g in sorted(soilGroups)}

print("\n[INFO] auto-detected soil physical groups:", sorted(soilGroups))
print("[INFO] mainSoilTags auto-built as:", mainSoilTags, "\n")

# --------------------------------------------------------------------------------------------------------------------
# USER MATERIAL REMAPPING: physical group --> material tag
# --------------------------------------------------------------------------------------------------------------------
matLoose = {i: 1 for i in range(1, 61)}
matDense = {j: 2 for j in range(61, 181)}
customMaterialMap = matLoose | matDense

for phy, mat in customMaterialMap.items():
    if phy in mainSoilTags:
        mainSoilTags[phy] = mat
    else:
        print(f"[Warning] physical group {phy} not found in mesh/not soil; ignoring.")

# ------------------------------------------------------------------------------------------------------------------
# Detect ndm/ndf and classify node DOFs
# ------------------------------------------------------------------------------------------------------------------
ndmGlobal, ndfGlobal = detect_ndm_ndf(elements, elementProfiles)
nodeDOFs_soil, nodeDOFs_struct, nodeDOFs = classifyNodeDOFs(elements, elementProfiles, beam2D_all, beam3D_all)

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
with open("updateASD.tcl", "w") as fUpdateASD:
    for i in ASD3DElements:
        fUpdateASD.write(f"setParameter -val 1 -ele {i} stage\n")
# !!!!----

phyGroupID = 2
axesToSort = ("x", "y", "z")
boundaryNodes = getAndSortGroupNodes(meshFile, phyGroupID, nodeCoords, axes=axesToSort, dim=1)

# ------------------------------------------------------------------------------------------------------------------
# SSI preparation: soil bounding box + selecting buried structural nodes
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

generatePileInterfaceForBricks(
    pileNodes=buriedStructuralNodes,
    nodeCoords=nodeCoords,
    elements=elements,
    soilTypes=soilTypes,
    # E_soil=3150000000,
    E_soil=1e8,
    phi_soil=35.0,
    verticalAxis="z",
    searchRadius=5.0,
    outputDir=outDir
)

print(buriedStructuralNodes)

# ------------------------------------------------------------------------------------------------------------------
# variable permeability data generation
# ------------------------------------------------------------------------------------------------------------------

# material parameters (per material tag)
gamma_sat_dict = {
    1: 19.87,  # loose sand (kN/^3)
    2: 20.41,  # dense sand (kN/m^3)
}

kInit_dict = {
    1: 6.169692025290639e-06,  # loose sand
    2: 3.773200081582705e-06,  # dense sand
}

# generate variable permeability files
generateVariablePermeabilityFiles(
    elements=elements,
    nodeCoords=nodeCoords,
    mainSoilTags=mainSoilTags,
    verticalAxis=verticalAxis,
    outputDir=outDir,
    gamma_sat_dict=gamma_sat_dict,
    kInit_dict=kInit_dict,
    gamma_water=9.81,  # unit weight of water (kN/m³)
    waterTableDepth=0.0,
    surfaceElevation=0.0,
    alpha=20.0,
    beta1=1.0,
    beta2=8.9,
)

# ------------------------------------------------------------------------------------------------------------------
# adaptive dynamic analysis generation
# ------------------------------------------------------------------------------------------------------------------

# generate adaptive analysis TCL (with variable permeability)
generateAdaptiveAnalysisTcl(
    outputDir=outDir,
    totalTime=15.0,
    dT_initial=0.0025,
    dT_min=0.005 / 64.0,     # minimum: initial/64
    dT_max=0.005,            # maximum: initial (don't exceed input dT)
    N_success=100,           # increase dT after 10 consecutive successes
    # analysis setup
    constraints_type="Transformation",
    test_type="NormDispIncr",
    test_tol=5.0e-3,
    test_iter=10,
    algorithm="KrylovNewton",
    numberer="RCM",
    system="UmfPack",
    integrator_gamma=0.5,
    integrator_beta=0.25,
    rayleigh_a0="$a0",
    rayleigh_a1="$a1",
    # variable permeability
    useVariablePerm=True,
    permUpdateInterval=60,
    filename="dynamicAnalysis_adaptive.tcl"
)
