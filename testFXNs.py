import os

import numpy as np

import meshHelper as mh

# meshFile = os.path.join("testing functions", "G18", "G18-5-2.msh")
path = "/Users/yannroger-ft/Desktop/gitHub/OpenSees-Geotechnical/simulations/test input GM"
meshFile = os.path.join(path, "model.msh")
outDir = os.path.join(os.path.dirname(meshFile), "TCL-Files", os.path.splitext(os.path.basename(meshFile))[0])

# define each group category
groupCategories = {
    # structural 2D
    "elBeam2D": set(), "dispBeam2D": set(),

    # structural 3D
    "elBeam3D": set(), "dispBeam3D": set(),

    # soil 2D
    "quad": set(), "bbarQuadUP": set(), "quadUP": set(),

    # soil 3D
    "brickUP": set(), "bbarBrickUP": set(), "SSPbrickUP": set(range(1, 4)), "SSPbrick": set(),
    "20_8_BrickUP": set(),

    # ASD absorbing boundaries 2D
    # "ASD2D_B": set(), "ASD2D_L": set(), "ASD2D_R": set(), "ASD2D_BL": set(), "ASD2D_BR": set(),
    #
    # # ASD absorbing boundaries 3D
    # "ASD3D_B": set(range(181, 241)),
    # "ASD3D_L": set(range(241, 259)),
    # "ASD3D_R": set(range(259, 277)),
    # "ASD3D_F": set(range(277, 307)),
    # "ASD3D_K": set(range(307, 337)),
    # "ASD3D_BL": set(range(337, 343)),
    # "ASD3D_BR": set(range(343, 349)),
    # "ASD3D_BF": set(range(349, 359)),
    # "ASD3D_BK": set(range(359, 369)),
    # "ASD3D_LF": set(range(369, 372)),
    # "ASD3D_LK": set(range(372, 375)),
    # "ASD3D_RF": set(range(375, 378)),
    # "ASD3D_RK": set(range(378, 381)),
    # "ASD3D_BLF": set(range(381, 382)),
    # "ASD3D_BLK": set(range(382, 383)),
    # "ASD3D_BRF": set(range(383, 384)),
    # "ASD3D_BRK": set(range(384, 385)),
}

# 1: parse elements [check GMSH stats and SUM all elmts (lines, triangles, quadrangles, tetrahedra, etc.)
# to see if PRINT results match]
elements = mh.parseELMTsFromGMSH(meshFile)
print(f"[1] PARSED {len(elements)} ELEMENTS: PLEASE check GMSH stats to see if RESULT corresponds")

# 2: filter (separate soil element from structural ones) [check if the lenght of the filtered elements is the SUM of
# SOIL ELMTS (triangles, quadrangles, tetrahedra, hexahedra, etc... NOT lines!!!) AND STRUCTURAL ELMTS (count in GMSH)]
structuralGroups = {k: v for k, v in groupCategories.items() if k.startswith(("elBeam", "disp", "shell", "solid"))}
allStructuralGroups = set().union(*structuralGroups.values())
filteredELMTS, has3D = mh.filterELMTsByDIM(elements, structuralGroups)
print(f"[2] length of both SOIL and STRUCTURE elements is: {len(filteredELMTS)}")

# 3: remap and summarize
elmtsRemapped = mh.remapELMTSType(filteredELMTS, groupCategories)
mh.summarizeRemaps(elmtsRemapped)

nodesLine = mh.getBoundaryNodesFromMsh(meshFile, phyGroupIDs=[5], dim=1)
nodeCoords = mh.parseNodesFromGMSH(meshFile)
# print(mh.sortNodesByY(mh.sortNodesByZ(mh.sortNodesByX(nodesLine, nodeCoords), nodeCoords), nodeCoords))

# 4. nodes: detect ndm/ndf, classify node DOFs, and summarize node DOFs [here use "elmtsRemapped" instead of "elements"]
ndmGlobal, ndfGlobal = mh.detect_ndm_ndf(elmtsRemapped)
nodeDOFS_soil, nodeDOFS_struct, nodeDOFs = mh.classifyNodeDOFs(elmtsRemapped, structuralGroups)
mh.summarizeNodeDOFs(nodeDOFs)

# 5. read and write nodes (nodeCoords is already defined previously)
# nodeCoords = mh.parseNodesFromGMSH(meshFile)
os.makedirs(outDir, exist_ok=True)
mh.writeNodesTCL(nodeCoords, ndmGlobal, nodeDOFs, filePrefix="allSoilNodes", outputDir=outDir,
                 elements=elmtsRemapped, structuralGroups=structuralGroups)
if nodeDOFS_soil:
    mh.writeSeparatedNodeFiles(nodeCoords, nodeDOFS_soil, ndmGlobal, outputDir=outDir, labelPrefix="soil")
if nodeDOFS_struct:
    mh.writeSeparatedNodeFiles(nodeCoords, nodeDOFS_struct, ndmGlobal, outputDir=outDir, labelPrefix="structure")

elasticBCELMTs = mh.getElementsTagByType(elmtsRemapped, {1})
# print(elasticBCELMTs)

soilTypes, soilGroups = mh.detectSoilGroups(elmtsRemapped, has3D)
soilTypesUsed = {el["type"] for el in elmtsRemapped if el["group"] not in allStructuralGroups}
# print(soilTypesUsed)

"""
# classify soil and structure nodes in two different sets
soilNodesSet, structureNodesSet = mh.classifySoilAndStructureNodes(elements, soilTypes, structuralGroups)
# print(f"soil node set is: {structureNodesSet}")
# print(f"soil node set is: {soilNodesSet}")

# locate the bounds of soil layer (e.g., for soil do not include ASDAbsorbing conditions)
soilBox = mh.computeSoilBoundingBox(soilNodesSet, nodeCoords)
# print(soilBox)

# for SSI map we do NOT need all structural nodes, but only those interacting with the structure
structNodesSSI = mh.selectBuriedStructuralNodes(structureNodesSet, soilBox, nodeCoords, 1e-6)

# now build SSI map
SSI_map = mh.buildSSIMap(structNodesSSI, elmtsRemapped, soilTypes, nodeCoords,
                         "nearest", 4, "y", 1e-6)
# print(SSI_map)
print("[SSI] node --> soil faces mapping:")
for sNode, soilNodes in SSI_map.items():
    print(f"      structural node {sNode}: {soilNodes}")

nEmbedded, nContact = mh.generateStructureInterface(structNodesSSI, nodeCoords, elmtsRemapped, soilTypes, 1e9,
                                                    35, "y", 4, outDir, 2, "nearest")
"""

# print(structNodesSSI)

alphaRad = np.arctan(0.02)
materialProps = {
    # ----------------------------------------------------------------
    # global parameters
    # ----------------------------------------------------------------
    "gravity":      9.81,
    "alphaAngle":   np.rad2deg(alphaRad),        # slope angle in degrees

    # fluid properties
    "fluidBulk":    2.2e6,      # kN/m^2 (water)
    "fluidDensity": 1.0,        # t/m^3

    # ----------------------------------------------------------------
    # default soil properties (fallback for all layers)
    # ----------------------------------------------------------------
    "soil2D": {
        "thickness": 1.0,
        "porosity":  0.40,
        "hPerm":     5.0e-4,
        "vPerm":     5.0e-4,
    },

    "soil3D": {
        "void": 0.77,
        "alphaStab": 1.5e-6,
        "porosity":  0.40,
        "permX":     5.0e-4,
        "permY":     5.0e-4,
        "permZ":     5.0e-4,
        # SSPbrickUP stabilization parameter: alpha = h^2 / (4*(Ks + 4/3*Gs))
        # This default is used when no per-group override is provided.
        # Ks and Gs below refer to the solid skeleton bulk and shear moduli [kPa].
        # Adjust these to match your nDMaterial definition.
        "Ks":        1.0e5,     # solid skeleton bulk modulus  [kPa]
        "Gs":        5.0e4,     # solid skeleton shear modulus [kPa]
        # Alternatively, supply alphaStab directly to bypass Ks/Gs computation:
        # "alphaStab": 6.0e-5,
    },

    # ----------------------------------------------------------------
    # ASD absorbing boundaries (2D and 3D)
    # ----------------------------------------------------------------
    "ASD": {
        "E":         3.0e9,
        "poisson":   0.3,
        "density":   2100.0,
        "thickness": 1.0,       # 2D only
    },

    # ----------------------------------------------------------------
    # structural elements
    # ----------------------------------------------------------------
    "elBeam2D": {
        "A":        0.25,
        "E":        2.1e11,
        "Iz":       3.0e-4,
        "transfTag": 1,
        "massDens": 7850.0,
        "useCMass": True,
    },

    "dispBeam2D": {
        "A":        0.25,
        "E":        2.1e11,
        "Iz":       3.0e-4,
        "transfTag": 1,
        "massDens": 7850.0,
        "useCMass": True,
    },

    "elBeam3D": {
        "A":        0.25,
        "E":        2.1e11,
        "G":        8.1e10,
        "J":        1.0e-4,
        "Iy":       2.0e-4,
        "Iz":       3.0e-4,
        "transfTag": 1,
        "massDens": 7850.0,
        "useCMass": True,
    },

    "dispBeam3D": {
        "A":        0.25,
        "E":        2.1e11,
        "G":        8.1e10,
        "J":        1.0e-4,
        "Iy":       2.0e-4,
        "Iz":       3.0e-4,
        "transfTag": 1,
        "massDens": 7850.0,
        "useCMass": True,
    },

    # ----------------------------------------------------------------
    # per-layer overrides (physical group ID --> properties)
    # only specify what differs from the defaults above
    # ----------------------------------------------------------------
    "groupOverrides": {
        1: {                            # upper layer  Dr=90%
            "void": 0.47,
            "porosity":  0.47 / (1 + 0.47),
            "permX":     1.0,           # 1.0e-2,
            "permY":     1.0,
            "permZ":     1.0,
            # SSPbrickUP: solid skeleton moduli for this layer [kPa]
            # alpha = h^2 / (4*(Ks + 4/3*Gs)) --> computed automatically
            "Ks":        1.2e5,         # adjust to match your nDMaterial
            "Gs":        6.0e4,         # adjust to match your nDMaterial
            # or supply directly:
            # "alphaStab": 6.0e-5,
        },
        2: {                            # middle layer Dr=40%
            "void": 0.77,
            "porosity":  0.77 / (1 + 0.77),
            "permX":     1.0,           # 1.0e-5
            "permY":     1.0,
            "permZ":     1.0,
            # softer layer --> larger alpha
            "Ks":        4.0e4,         # adjust to match your nDMaterial
            "Gs":        2.0e4,         # adjust to match your nDMaterial
            # "alphaStab": 2.0e-4,
        },
        3: {                            # lower layer  Dr=90%
            "void": 0.77,
            "porosity":  0.77 / (1 + 0.77),
            "permX":     1.0,           # 1.0e-2
            "permY":     1.0,
            "permZ":     1.0,
            "Ks":        1.2e5,         # adjust to match your nDMaterial
            "Gs":        6.0e4,         # adjust to match your nDMaterial
            # "alphaStab": 6.0e-5,
        },
    },
}

# print(mh.sortNodesByY(mh.sortNodesByZ(mh.sortNodesByX(nodesLine, nodeCoords), nodeCoords), nodeCoords))
# mainSoilTags = mh.buildMainSoilTags(meshFile, overrides={
#     **{i: 3 for i in range(31, 51)},     # groups 31-50 --> material 3
#     2: 5,                                # group 2 --> material 5
# })

mainSoilTags = mh.buildMainSoilTags(meshFile, overrides={
    **{i: 1 for i in range(1, 2)},
    **{i: 2 for i in range(2, 3)},
    **{i: 3 for i in range(3, 4)},
})

maxPhyGroup = mh.detectMaxPhyGroup(meshFile)

mh.writeElementsTCL(elmtsRemapped, materialProps, mainSoilTags,
                    nodeCoords=nodeCoords, filePrefix="elements_", outputDir=outDir)

# print(maxPhyGroup)

baseNodes = mh.getCustomBoundaryNodesFromMsh(meshFile, nodeDOFs, phyGroupIDs=[5], dim=2,
                                                  returnGrouped=False)
baseNodes = mh.sortNodesByZ(mh.sortNodesByY(list(baseNodes), nodeCoords), nodeCoords)

with open(os.path.join(outDir, "fixBaseNodes.tcl"), "w") as fBaseN:
    for i in baseNodes:
        fBaseN.write(f"fix {i} 0 1 1 0\n") 

equalMasterNodes = mh.sortNodesByZ(mh.getBoundaryNodesFromMsh(meshFile, phyGroupIDs=[1, 13, 21], dim=1), nodeCoords)
equalSlaveNodes1 = mh.sortNodesByZ(mh.getBoundaryNodesFromMsh(meshFile, phyGroupIDs=[5, 16, 24], dim=1), nodeCoords)
equalSlaveNodes2 = mh.sortNodesByZ(mh.getBoundaryNodesFromMsh(meshFile, phyGroupIDs=[7, 18, 26], dim=1), nodeCoords)
equalSlaveNodes3 = mh.sortNodesByZ(mh.getBoundaryNodesFromMsh(meshFile, phyGroupIDs=[3, 15, 23], dim=1), nodeCoords)

with open(os.path.join(outDir, "baseEqualDOFs.tcl"), "w") as fEqualDOF:
    i, j, k, l = equalMasterNodes[0], equalSlaveNodes1[0], equalSlaveNodes2[0], equalSlaveNodes3[0]
    fEqualDOF.write(f"equalDOF {i} {j} 1\nequalDOF {i} {k} 1\nequalDOF {i} {l} 1\n")

with open(os.path.join(outDir, "baseEqualDOFs.tcl"), "w") as fBaseEqualDOF:
    fBaseEqualDOF.write(f"equalDOF {equalMasterNodes[0]} {equalSlaveNodes1[0]} 1\n")
    fBaseEqualDOF.write(f"equalDOF {equalMasterNodes[0]} {equalSlaveNodes2[0]} 1\n")
    fBaseEqualDOF.write(f"equalDOF {equalMasterNodes[0]} {equalSlaveNodes3[0]} 1\n")

with open(os.path.join(outDir, "equalDOFs.tcl"), "w") as fEqualDOF:
    for i, j, k, l in zip(equalMasterNodes[1:], equalSlaveNodes1[1:], equalSlaveNodes2[1:], equalSlaveNodes3[1:]):
        fEqualDOF.write(f"equalDOF {i} {j} 1 2 3\nequalDOF {i} {k} 1 2 3\nequalDOF {i} {l} 1 2 3\n")
        # print(f"equalDOF {i} {k} 1 2 3")
        # print(f"equalDOF {i} {l} 1 2 3")

# print(maxPhyGroup)

dryNodes = mh.sortNodesByZ(mh.getBoundaryNodesFromMsh(meshFile, phyGroupIDs=[3], dim=3), nodeCoords)

with open(os.path.join(outDir, "fixDryNodes.tcl"), "w") as fDryNodes:
    for i in dryNodes:
        fDryNodes.write(f"fix {i} 0 0 0 1\n")

elePhyGroup3 = mh.getElementsByGroup(elmtsRemapped, 3)
elePhyGrp3_ID = mh.getElementsTagByGroup(elmtsRemapped, 3)
elePhyGrp2and3_ID = mh.getElementsTagByGroup(elmtsRemapped, {2, 3})

elePhyGrp2_ID = mh.getElementsTagByGroup(elmtsRemapped, 2)
elePhyGrp1_ID = mh.getElementsTagByGroup(elmtsRemapped, 1)

# print(elePhyGrp2and3_ID)
with open(os.path.join(outDir, "updatePerm.tcl"), "w") as fUpdatePerm:
    fUpdatePerm.write(f"setParameter -value $xPerm3 -eleRange {elePhyGrp3_ID[0]} {elePhyGrp3_ID[-1]} xPerm\n")
    fUpdatePerm.write(f"setParameter -value $yPerm3 -eleRange {elePhyGrp3_ID[0]} {elePhyGrp3_ID[-1]} yPerm\n")
    fUpdatePerm.write(f"setParameter -value $zPerm3 -eleRange {elePhyGrp3_ID[0]} {elePhyGrp3_ID[-1]} zPerm\n")
    fUpdatePerm.write(f"setParameter -value $xPerm2 -eleRange {elePhyGrp2_ID[0]} {elePhyGrp2_ID[-1]} xPerm\n")
    fUpdatePerm.write(f"setParameter -value $yPerm2 -eleRange {elePhyGrp2_ID[0]} {elePhyGrp2_ID[-1]} yPerm\n")
    fUpdatePerm.write(f"setParameter -value $zPerm2 -eleRange {elePhyGrp2_ID[0]} {elePhyGrp2_ID[-1]} zPerm\n")
    fUpdatePerm.write(f"setParameter -value $xPerm1 -eleRange {elePhyGrp1_ID[0]} {elePhyGrp1_ID[-1]} xPerm\n")
    fUpdatePerm.write(f"setParameter -value $yPerm1 -eleRange {elePhyGrp1_ID[0]} {elePhyGrp1_ID[-1]} yPerm\n")
    fUpdatePerm.write(f"setParameter -value $zPerm1 -eleRange {elePhyGrp1_ID[0]} {elePhyGrp1_ID[-1]} zPerm\n")

elePhyGrp1and2and3_ID = mh.getElementsTagByGroup(elmtsRemapped, {1, 2, 3})
# print(elePhyGrp1and2and3_ID)

