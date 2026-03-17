import os
import meshHelper as mh

# meshFile = os.path.join("testing functions", "G18", "G18-5-2.msh")
meshFile = "model.msh"
outDir = mh.outputFolder(meshFile)

# define each group category
groupCategories = {
    # structural 2D
    "elBeam2D": set(), "dispBeam2D": set(),

    # structural 3D
    "elBeam3D": set(), "dispBeam3D": set(),

    # soil 2D
    "quad": set(), "bbarQuadUP": set(), "quadUP": set(),

    # soil 3D
    "brickUP": set(range(1, 181)), "bbarBrickUP": set(), "SSPbrickUP": set(), "SSPbrick": set(),

    # ASD absorbing boundaries 2D
    "ASD2D_B": set(), "ASD2D_L": set(), "ASD2D_R": set(), "ASD2D_BL": set(), "ASD2D_BR": set(),

    # ASD absorbing boundaries 3D
    "ASD3D_B": set(range(181, 241)),
    "ASD3D_L": set(range(241, 259)),
    "ASD3D_R": set(range(259, 277)),
    "ASD3D_F": set(range(277, 307)),
    "ASD3D_K": set(range(307, 337)),
    "ASD3D_BL": set(range(337, 343)),
    "ASD3D_BR": set(range(343, 349)),
    "ASD3D_BF": set(range(349, 359)),
    "ASD3D_BK": set(range(359, 369)),
    "ASD3D_LF": set(range(369, 372)),
    "ASD3D_LK": set(range(372, 375)),
    "ASD3D_RF": set(range(375, 378)),
    "ASD3D_RK": set(range(378, 381)),
    "ASD3D_BLF": set(range(381, 382)),
    "ASD3D_BLK": set(range(382, 383)),
    "ASD3D_BRF": set(range(383, 384)),
    "ASD3D_BRK": set(range(384, 385)),
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

materialProps = {
    # ----------------------------------------------------------------
    # global parameters
    # ----------------------------------------------------------------
    "gravity":      9.81,
    "alphaAngle":   0.0,        # slope angle in degrees

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
        "porosity": 0.40,
        "permX":    5.0e-4,
        "permY":    5.0e-4,
        "permZ":    5.0e-4,
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
        1: {                     # upper layer Dr=55% (Table 2)
            "porosity": 0.409,
            "permX": 6.05e-5,
            "permY": 6.05e-5,
            "permZ": 6.05e-5,
        },
        2: {                     # lower layer Dr=80% (Table 2)
            "porosity": 0.377,
            "permX": 3.7e-5,
            "permY": 3.7e-5,
            "permZ": 3.7e-5,
        },
    },
}

# print(mh.sortNodesByY(mh.sortNodesByZ(mh.sortNodesByX(nodesLine, nodeCoords), nodeCoords), nodeCoords))
# mainSoilTags = mh.buildMainSoilTags(meshFile, overrides={
#     **{i: 3 for i in range(31, 51)},     # groups 31-50 --> material 3
#     2: 5,                                # group 2 --> material 5
# })

mainSoilTags = mh.buildMainSoilTags(meshFile, overrides={
    **{i: 1 for i in range(1, 61)},
    **{i: 2 for i in range(61, 181)},
})

maxPhyGroup = mh.detectMaxPhyGroup(meshFile)

mh.writeElementsTCL(elmtsRemapped, materialProps, mainSoilTags,
                    nodeCoords=nodeCoords, filePrefix="elements_", outputDir=outDir)
# print(maxPhyGroup)
