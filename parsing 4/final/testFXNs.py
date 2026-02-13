import os
import meshHelper as mh

# meshFile = os.path.join("testing functions", "G18", "G18-5-2.msh")
meshFile = "model.msh"
outDir = mh.outputFolder(meshFile)

# define each group category
groupCategories = {
    # structural 2D
    "elBeam2D": set(), "dispBeam2D": {5, 6, 7},

    # structural 3D
    "elBeam3D": set(), "dispBeam3D": set(),

    # soil 2D
    "quad (plain 2D)": {1}, "bbarQuadUP": set(), "quadUP": set(),

    # soil 3D
    "SSPbrickUP": set(), "SSPbrick": set(), "bbarBrickUP": set(),
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
                                                    35, "y", 4, outDir, 2,
                                                    "nearest")

print(structNodesSSI)

"""
'''
--------------------------------
material properties dictionary
--------------------------------
'''
materialProps = {
    # global/general/universal parameters
    "gravity": 9.81,
    "alphaAngle": 0.0,  # slope angles in degrees

    # fluid props (fluid bulk for water is 2.2e6 kN/m^2, and fluidDensity is 1.0 t/m^3)
    "fluidBulk": 2.2e6,
    "fluidDensity": 1.0,

    # for 2D soil elements (quadUP, bbarQuadUP)
    "soil2D": {
        "thickness": 1.0,
        "porosity": 1.0,  # default, BUT can be overridden per phyGroup
        "hPerm": 5.0e-4,
        "vPerm": 5.0e-4,
    },

    # 3D soil elements (SSPbrickUP, bbarBrickUP)
    "soil3D": {
        "porosity": 1.0,
        "permX": 5.0e-4,
        "permY": 5.0e-4,
        "permZ": 5.0e-4,
    },

    # ASD absorbing boundaryies
    "ASD": {
        "E": 3.0e9,
        "poisson": 0.3,
        "density": 2100.0,
        "thickness": 1.0,  # for 2D only
    },

    # beam elements
    "beam2D": {
        "A": 0.25,
        "E": 2.1e11,
        "Iz": 3.0e-4,
        "transfTag": 1,
        "massDens": 7850.0,
        "useCMass": True,
    },

    "beam3D": {
        "A": 0.25,
        "E": 2.1e11,
        "G": 8.1e10,
        "J": 1.0e-4,
        "Iy": 2.0e-4,
        "Iz": 3.0e-4,
        "transfTag": 1,
        "massDens": 7850.0,
        "useCMass": True,
    },

    # per-group overrides (physical group ID --> properties)
    "groupOverrides": {
        # example: group 2 has a different porosity
        # 2: {"porosity": 0.4},
    },
}
"""

# print(mh.sortNodesByY(mh.sortNodesByZ(mh.sortNodesByX(nodesLine, nodeCoords), nodeCoords), nodeCoords))
