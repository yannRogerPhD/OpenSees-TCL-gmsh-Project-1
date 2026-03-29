import os
import numpy as np

import meshHelper as mh

# meshFile = os.path.join("testing functions", "G18", "G18-5-2.msh")
# path = "/Users/yannroger-ft/Desktop/gitHub/OpenSees-Geotechnical/simulations/test SP and MP"
# path = "/home/yafeu/Desktop/GitHub/OpenSees-Geotechnical/simulations/the conf paper"
path = "/Users/yannroger-ft/Desktop/gitHub/OpenSees-Geotechnical/simulations/the conf paper"
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
    "brickUP": set(), "bbarBrickUP": set(), "SSPbrickUP": set(range(1, 8)), "SSPbrick": set(),
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

alphaRad = np.arctan(0.0)
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
        1: {                            
            "void": 0.77,
            "porosity":  0.77 / (1 + 0.77),
            "permX":     1.0,           
            "permY":     1.0,
            "permZ":     1.0,
            # SSPbrickUP: solid skeleton moduli for this layer [kPa]
            # alpha = h^2 / (4*(Ks + 4/3*Gs)) --> computed automatically
            "Ks":        1.2e5,         
            "Gs":        6.0e4,         
            # or supply directly:
            # "alphaStab": 6.0e-5,
            "fluidBulk":    8.8e6,      # kN/m^2 (ice)
            "fluidDensity": 0.917,
        },
        2: {                            
            "void": 0.77,
            "porosity":  0.77 / (1 + 0.77),
            "permX":     1.0,           
            "permY":     1.0,
            "permZ":     1.0,
            # softer layer --> larger alpha
            "Ks":        4.0e4,         
            "Gs":        2.0e4,         
            # "alphaStab": 2.0e-4,
            "fluidBulk":    8.8e6,      # kN/m^2 (ice)
            "fluidDensity": 0.917,
        },
        3: {                            
            "void": 0.77,
            "porosity":  0.77 / (1 + 0.77),
            "permX":     1.0,           
            "permY":     1.0,
            "permZ":     1.0,
            "Ks":        1.2e5,         
            "Gs":        6.0e4,         
            # "alphaStab": 6.0e-5,
            "fluidBulk":    8.8e6,      # kN/m^2 (ice)
            "fluidDensity": 0.917,
        },
        4: {                            
            "void": 0.77,
            "porosity":  0.77 / (1 + 0.77),
            "permX":     1.0,           
            "permY":     1.0,
            "permZ":     1.0,
            "Ks":        1.2e5,         
            "Gs":        6.0e4,         
            # "alphaStab": 6.0e-5,
            "fluidBulk":    8.8e6,      # kN/m^2 (ice)
            "fluidDensity": 0.917,
        },
        5: {                            
            "void": 0.77,
            "porosity":  0.77 / (1 + 0.77),
            "permX":     1.0,           
            "permY":     1.0,
            "permZ":     1.0,
            "Ks":        1.2e5,         
            "Gs":        6.0e4,         
            # "alphaStab": 6.0e-5,
        },
        6: {                            
            "void": 0.65,
            "porosity":  0.65 / (1 + 0.65),
            "permX":     1.0,           
            "permY":     1.0,
            "permZ":     1.0,
            "Ks":        1.2e5,         
            "Gs":        6.0e4,         
            # "alphaStab": 6.0e-5,
        },
        7: {                            
            "void": 0.45,
            "porosity":  0.45 / (1 + 0.45),
            "permX":     1.0,           
            "permY":     1.0,
            "permZ":     1.0,
            "Ks":        1.2e5,         
            "Gs":        6.0e4,         
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
    **{i: 4 for i in range(4, 5)},
    **{i: 5 for i in range(5, 6)},
    **{i: 6 for i in range(6, 7)},
    **{i: 7 for i in range(7, 8)},
})

# mainSoilTags = mh.buildMainSoilTags(meshFile, overrides={
#     **{i: 1 for i in list(range(102, 116)) + list(range(200, 212))},
#     **{i: 2 for i in list(range(88, 102)) + list(range(188, 200))},
#     **{i: 3 for i in list(range(74, 88)) + list(range(176, 188))},
#     **{i: 4 for i in list(range(60, 74)) + list(range(164, 176))},
#     **{i: 5 for i in list(range(31, 46)) + list(range(46, 60)) + list(range(140, 152)) + list(range(152, 164))},
#     **{i: 6 for i in list(range(16, 31)) + list(range(128, 140))},
#     **{i: 7 for i in list(range(1, 16)) + list(range(116, 128))},
# })


maxPhyGroup = mh.detectMaxPhyGroup(meshFile)

mh.writeElementsTCL(elmtsRemapped, materialProps, mainSoilTags,
                    nodeCoords=nodeCoords, filePrefix="elements_", outputDir=outDir)

# print(maxPhyGroup)

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!! fix base nodes !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# """
### fix base nodes
# baseNodes = mh.getCustomBoundaryNodesFromMsh(meshFile, nodeDOFs, phyGroupIDs=[5], dim=2, returnGrouped=False)
# baseNodes = mh.sortNodesByZ(mh.sortNodesByY(list(baseNodes), nodeCoords), nodeCoords)

# with open(os.path.join(outDir, "fixBaseNodes.tcl"), "w") as fBaseN:
#     for i in baseNodes:
#         fBaseN.write(f"fix {i} 1 1 1 0\n") 

baseNodes = mh.selectBoundaryNodes(nodeCoords, axis="z", face="min")
baseNodes = mh.sortNodesByZ(mh.sortNodesByY(mh.sortNodesByX(baseNodes, nodeCoords), nodeCoords), nodeCoords)

with open(os.path.join(outDir, "fixBaseNodes.tcl"), "w") as fBaseN:
    for i in baseNodes:
        fBaseN.write(f"fix {i} 1 1 1 0\n")

topNodes = mh.selectBoundaryNodes(nodeCoords, axis="z", face="max")
topNodes = mh.sortNodesByZ(mh.sortNodesByY(mh.sortNodesByX(topNodes, nodeCoords), nodeCoords), nodeCoords)
with open(os.path.join(outDir, "drainageTopNodes.tcl"), "w") as fTopN:
    for i in topNodes:
        fTopN.write(f"fix {i} 0 0 0 1\n")

# """
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!! equal DOFs at lateral boundaries for 3D soil column !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# """
### equal DOFs at lateral boundaries for 3D soil column (left right)
# equalMasterLateral = mh.sortNodesByY(mh.getBoundaryNodesFromMsh(meshFile, phyGroupIDs=[1, 7, 12], dim=2), nodeCoords)
# equalMasterLateral = mh.sortNodesByZ(mh.sortNodesByX(equalMasterLateral, nodeCoords), nodeCoords)

equalMasterLateral = mh.selectBoundaryNodes(nodeCoords, axis="x", face="min")
equalMasterLateral = [n for n in equalMasterLateral if n not in baseNodes]
equalMasterLateral = mh.sortNodesByZ(mh.sortNodesByY(equalMasterLateral, nodeCoords), nodeCoords)

equalSlaveLateral = mh.selectBoundaryNodes(nodeCoords, axis="x", face="max")
equalSlaveLateral = [n for n in equalSlaveLateral if n not in baseNodes]
equalSlaveLateral = mh.sortNodesByZ(mh.sortNodesByY(equalSlaveLateral, nodeCoords), nodeCoords)

with open(os.path.join(outDir, "equalDOFs.tcl"), "w") as fBaseN:
    for i, j in zip(equalMasterLateral, equalSlaveLateral):
        fBaseN.write(f"equalDOF {i} {j} 1 2\n")

### fix symmetry plane nodes (BCs for symmetry plane nodes and its parallel) (font back)
symmetryPlaneF = mh.selectBoundaryNodes(nodeCoords, axis="y", face="min")
symmetryPlaneF = [n for n in symmetryPlaneF if n not in baseNodes]
symmetryPlaneF = mh.sortNodesByZ(mh.sortNodesByX(symmetryPlaneF, nodeCoords), nodeCoords)

symmetryPlaneB = mh.selectBoundaryNodes(nodeCoords, axis="y", face="max")
symmetryPlaneB = [n for n in symmetryPlaneB if n not in baseNodes]
symmetryPlaneB = mh.sortNodesByZ(mh.sortNodesByX(symmetryPlaneB, nodeCoords), nodeCoords)

with open(os.path.join(outDir, "symmetryPlaneBCs.tcl"), "w") as fBaseN:
    for i in symmetryPlaneF:
        fBaseN.write(f"fix {i} 0 1 0 0\n")
    for i in symmetryPlaneB:
        fBaseN.write(f"fix {i} 0 1 0 0\n")

# """
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


### equal DOFs at basesymmer
# with open(os.path.join(outDir, "baseEqualDOFs.tcl"), "w") as fEqualDOF:
#     i, j, k, l = equalMasterNodes[0], equalSlaveNodes1[0], equalSlaveNodes2[0], equalSlaveNodes3[0]
#     fEqualDOF.write(f"equalDOF {i} {j} 1\nequalDOF {i} {k} 1\nequalDOF {i} {l} 1\n")

# with open(os.path.join(outDir, "baseEqualDOFs.tcl"), "w") as fBaseEqualDOF:
#     fBaseEqualDOF.write(f"equalDOF {equalMasterNodes[0]} {equalSlaveNodes1[0]} 1\n")
#     fBaseEqualDOF.write(f"equalDOF {equalMasterNodes[0]} {equalSlaveNodes2[0]} 1\n")
#     fBaseEqualDOF.write(f"equalDOF {equalMasterNodes[0]} {equalSlaveNodes3[0]} 1\n")

## equal DOFs at lateral boundaries for 1D soil column
equalMasterNodes = mh.sortNodesByZ(mh.getBoundaryNodesFromMsh(meshFile, phyGroupIDs=[53, 45, 37, 29, 21, 13, 1], dim=1), nodeCoords)
equalSlaveNodes1 = mh.sortNodesByZ(mh.getBoundaryNodesFromMsh(meshFile, phyGroupIDs=[56, 48, 40, 32, 24, 16, 5], dim=1), nodeCoords)
equalSlaveNodes2 = mh.sortNodesByZ(mh.getBoundaryNodesFromMsh(meshFile, phyGroupIDs=[57, 49, 41, 33, 25, 17, 7], dim=1), nodeCoords)
equalSlaveNodes3 = mh.sortNodesByZ(mh.getBoundaryNodesFromMsh(meshFile, phyGroupIDs=[54, 46, 38, 30, 22, 14, 3], dim=1), nodeCoords)

with open(os.path.join(outDir, "equalDOFs1D.tcl"), "w") as fEqualDOF:
    for i, j, k, l in zip(equalMasterNodes[1:], equalSlaveNodes1[1:], equalSlaveNodes2[1:], equalSlaveNodes3[1:]):
        fEqualDOF.write(f"equalDOF {i} {j} 1 2 3\nequalDOF {i} {k} 1 2 3\nequalDOF {i} {l} 1 2 3\n")
        # print(f"equalDOF {i} {k} 1 2 3")
        # print(f"equalDOF {i} {l} 1 2 3")


# print(maxPhyGroup)

dryNodes = mh.sortNodesByZ(mh.getBoundaryNodesFromMsh(meshFile, phyGroupIDs=[3], dim=3), nodeCoords)

with open(os.path.join(outDir, "fixDryNodes.tcl"), "w") as fDryNodes:
    for i in dryNodes:
        fDryNodes.write(f"fix {i} 0 0 0 1\n")

# auto-generate updatePerm.tcl from mainSoilTags

# 1. invert mainSoilTags: matTag --> list of phyGroup IDs
from collections import defaultdict
matTagToGroups = defaultdict(list)
for grpID, matTag in mainSoilTags.items():
    matTagToGroups[matTag].append(grpID)

# 2. for each matTag, collect all element IDs belonging to those groups
with open(os.path.join(outDir, "updatePerm.tcl"), "w") as fUpdatePerm:
    for matTag in sorted(matTagToGroups.keys()):
        grpIDs = set(matTagToGroups[matTag])
        eleIDs = mh.getElementsTagByGroup(elmtsRemapped, grpIDs)
        if not eleIDs:
            continue
        fUpdatePerm.write(f"setParameter -value $xPerm{matTag} -eleRange {eleIDs[0]} {eleIDs[-1]} xPerm\n")
        fUpdatePerm.write(f"setParameter -value $yPerm{matTag} -eleRange {eleIDs[0]} {eleIDs[-1]} yPerm\n")
        fUpdatePerm.write(f"setParameter -value $zPerm{matTag} -eleRange {eleIDs[0]} {eleIDs[-1]} zPerm\n")

elePhyGrp1and2and3_ID = mh.getElementsTagByGroup(elmtsRemapped, {1, 2, 3})

# print(equalMasterLateral)

