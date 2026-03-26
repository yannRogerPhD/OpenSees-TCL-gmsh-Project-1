import os
import numpy as np

"""
STEP to add new elements (non-native GMSH). In such case we will need a custon interger code.
(1) in "derivativesType" add the element (e.g., "brickUP": {205});
(2) add this new element in "elementRemapping" --> (5, "brickUP"): 205;
(3) add to "elementLabels" as well --> 205: "brickUP";
(4) add to "elementProfiles" --> 205: {"ndm": 3, "ndf": 4, "needsP": True, "dofRule": _fourDOFs3D}
(5) write the writer function --> def write_brickUP(el, f, matProps, materialTag, nodeCoords=None)
(6) finally, register in "elementWriters"

___________________________________________________________________________________
AVAILABLE FUNCTIONS (grouped for efficient testing strategies)
___________________________________________________________________________________

G0) leaf helpers (mostly deterministic --> we prefer indirect tests unless reused broadly): 17
    (1)  _axis_pair_indices
    (2)  _get_coord
    (3)  _roundFunc
    (4)  only2DOFs
    (5)  threeDOFs
    (6)  threeDOFs3D
    (7)  fourDOFs3D
    (8)  beam2D_DOFs
    (9)  beam3D_DOFs
    (10) both2and3DOFs
    (11) twentyEightBrickDOFs
    (12) outputFolder
    (13) sortNodesByX
    (14) sortNodesByY
    (15) sortNodesByZ
    (16) countINTBraces
    (17) computeElementCentroid

G1) parsing / filtering / remapping (directly test with Gmsh .msh fixtures): 8
    (18) parseELMTsFromGMSH         (OK)
    (19) parseNodesFromGMSH         (OK)
    (20) filterELMTsByDIM           (OK)
    (21) remapELMTSType             (OK)
    (22) summarizeRemaps            (OK)
    (23) getBoundaryNodesFromMsh    (OK)
    (24) detectMaxPhyGroup          (NOT NECESSARY FOR MOST CASES)
    (25) detectSoilGroups           (NOT NECESSARY FOR MOST CASES)

G2) global model classification + node/element selection utilities (directly test on mixed meshes): 9
    (26) detect_ndm_ndf
    (27) classifyNodeDOFs
    (28) summarizeNodeDOFs
    (29) getElementsTagByType
    (30) classifyChosenNodesByDOF
    (31) selectNodes
    (32) getAndSortGroupNodes
    (33) groupNodesByCoordinate
    (34) FuzzyFloat (class)

G3) canonical ordering + geometry kernels (must be tested explicitly; high risk if wrong): 12
    (35) classify_hex8_nodes
    (36) gmsh_hex8_to_canonical
    (37) gmsh_hex20_to_canonical
    (38) computeSoilBoundingBox
    (39) computeStructureNormal
    (40) computeStructureNormal2D          <-- NEW
    (41) isPointInTetrahedron
    (42) decomposeBrickIntoTetrahedra
    (43) findTetrahedronForStructNode
    (44) isPointInTriangle                 <-- NEW
    (45) decomposeQuadIntoTriangles        <-- NEW
    (46) findTriangleForStructNode         <-- NEW

G4) writers (Tcl output; test by exact/regex comparison of emitted lines + sanity checks): 15
    (47) writeNodesTCL
    (48) writeSeparatedNodeFiles
    (49) write_bbarQuadUP
    (50) write_quadUP
    (51) write_ASD2D
    (52) write_beam2D
    (53) write_beam3D
    (54) write_SSPbrickUP
    (55) write_bbarBrickUP
    (56) write_SSPbrick
    (57) write_ASD3D
    (58) write_20_8_BrickUP
    (59) writeElementsTCL
    (60) writeEmbeddedElements
    (61) writeContactElements

G5) SSI mapping / soil–structure coupling helpers (test with interface-rich meshes): 5
    (62) selectBuriedStructuralNodes
    (63) classifySoilAndStructureNodes
    (64) soilNodesNearStructure
    (65) buildSSIMap
    (66) generateStructureInterface

G6) soil mechanics / material utilities (test with known depth/stress values): 3
    (67) computeInitialEffectiveStress
    (68) generateVariablePermeabilityFiles
    (69) _getVariablePermProcedure

G7) analysis generation (test by output file inspection + TCL syntax validation): 3
    (70) writeAdaptiveAnalysisProcedure
    (71) generateAdaptiveAnalysisTcl
    (72) writeMainTclGlobal


OTHER UTILITIES (type systems / registries; not functions, but must be internally consistent):
    (a) gmshType
    (b) derivativesType
    (c) elementRemapping
    (d) elementLabels
    (e) elementProfiles
    (f) elementWriters
    (g) defaultTol (constant)

TOTAL: 72 functions + 1 class + 7 registries/constants
"""


defaultTol = 1e-6


# --------------!!!!!!!!!!!!!-----------!!!!!!!!!!!!!!!!!!!-----------!!!!!!!!!!!!!!!!!!!!!-------------------!!!!!
def _only2DOFs(ns):
    # every node gets 2 DOFs: u, v
    return {n: 2 for n in ns}


def _threeDOFs(ns):
    # every node gets 3 DOFs (u, v, p) for 2D UP elements
    return {n: 3 for n in ns}


def _threeDOFs3D(ns):
    # 3D displacement (only disp) nodes: u, v, w
    return {n: 3 for n in ns}


def _fourDOFs3D(ns):
    # this rule is for brickUP elements: u, v, w, p (i.e., 4 DOFs per nod)
    return {n: 4 for n in ns}


def _beam2D_DOFs(ns):
    # 2D beam nodes: u, v, thetaZ
    return {n: 3 for n in ns}


def _beam3D_DOFs(ns):
    # 3D beam nodes: u, v, w, thetaX, thetaY, thetaZ
    return {n: 6 for n in ns}


def _both2and3DOFs(ns):
    # for the specific case of 9_4_QuadUP:
    #   - first 04 nodes (corners) ==> 3 DOFs
    #   - remaining nodes ==> 2 DOFs
    return {**{n: 3 for n in ns[:4]}, **{n: 2 for n in ns[4:]}}


def _twentyEightBrickDOFs(ns):
    # for 20_8_BrickUP:
    #   - 1st 08 nodes (corners) ==> 4 DOFs
    #   - remaining 12 nodes ==> 3 DOFs
    return {**{n: 4 for n in ns[:8]}, **{n: 3 for n in ns[8:]}}

# --------------!!!!!!!!!!!!!-----------!!!!!!!!!!!!!!!!!!!-----------!!!!!!!!!!!!!!!!!!!!!-------------------!!!!!


# we start by defining gmsh native element types (see as from page 357 or 367/4566 in the gmsh.pdf doc)
gmshType = {
    "line": {1},         # 2-node line (e.g., beam elements) (1D)
    "triangle": {2},     # 3-node triangle (2D)
    "quadrangle": {
        3,               # 4-node quadrangle (2D)
        10               # 9-node 2nd order quadrangle (2D)
    },
    "tetrahedron": {4},  # 4-node tetrahedron (3D)
    "hexahedron": {
        5,               # 8-node hexahedron (3D)
        12,              # 27-node 2nd order hexahedron (3D)
        17               # 20-node 2nd order hexahedron (3D)
    }
}

derivativesType = {
    "bbarQuadUP": {103},   # 2D
    "quadUP": {1003},      # 2D
    "ASD2D": {             # 2D
        10031,             # B  - 2D
        10032,             # L  - 2D
        10033,             # R  - 2D
        10034,             # BL - 2D
        10035              # BR - 2D
    },
    "brickUP": {205},      # 3D
    "bbarBrickUP": {105},  # 3D
    "SSPbrickUP": {1005},  # 3D
    "SSPbrick": {1055},    # 3D
    "ASD3D": {
        10051,  # B   - 3D
        10052,  # L   - 3D
        10053,  # R   - 3D
        10054,  # F   - 3D
        10055,  # K   - 3D
        10056,  # BL  - 3D
        10057,  # BR  - 3D
        10058,  # BF  - 3D
        10059,  # BK  - 3D
        10060,  # LF  - 3D
        10061,  # LK  - 3D
        10062,  # RF  - 3D
        10063,  # RK  - 3D
        10064,  # BLF - 3D
        10065,  # BLK - 3D
        10066,  # BRF - 3D
        10067,  # BRK - 3D
    }
}

elementRemapping = {
    # beams (type 1) ------------------> 1D
    (1, "elBeam2D"): 1,
    (1, "elBeam3D"): 101,
    (1, "dispBeam2D"): 201,
    (1, "dispBeam3D"): 202,

    # quadrangles (quads), (type 3) ---> 2D
    (3, "quad"): 3,
    (3, "bbarQuadUP"): 103,
    (3, "quadUP"): 1003,
    (3, "ASD2D_B"): 10031,
    (3, "ASD2D_L"): 10032,
    (3, "ASD2D_R"): 10033,
    (3, "ASD2D_BL"): 10034,
    (3, "ASD2D_BR"): 10035,

    # hexahedrons (type 5) ------------> 3D
    # (5, "brick"): 105,
    (5, "brickUP"): 205,
    (5, "bbarBrickUP"): 105,
    (5, "SSPbrickUP"): 1005,
    (5, "SSPbrick"): 1055,

    (5, "ASD3D_B"): 10051,
    (5, "ASD3D_L"): 10052,
    (5, "ASD3D_R"): 10053,
    (5, "ASD3D_F"): 10054,
    (5, "ASD3D_K"): 10055,
    (5, "ASD3D_BL"): 10056,
    (5, "ASD3D_BR"): 10057,
    (5, "ASD3D_BF"): 10058,
    (5, "ASD3D_BK"): 10059,
    (5, "ASD3D_LF"): 10060,
    (5, "ASD3D_LK"): 10061,
    (5, "ASD3D_RF"): 10062,
    (5, "ASD3D_RK"): 10063,
    (5, "ASD3D_BLF"): 10064,
    (5, "ASD3D_BLK"): 10065,
    (5, "ASD3D_BRF"): 10066,
    (5, "ASD3D_BRK"): 10067,
}

elementLabels = {
    # for structural elements:
    1: "elasticBeamColumn2D",
    101: "elasticBeamColumn3D",
    201: "dispBeamColumn2D",
    202: "dispBeamColumn3D",

    # 2D soil
    3: "quad",
    10: "9_4_QuadUP",
    103: "bbarQuadUP",
    1003: "quadUP",

    10031: "ASD2D_B",
    10032: "ASD2D_L",
    10033: "ASD2D_R",
    10034: "ASD2D_BL",
    10035: "ASD2D_BR",

    # 3D soil
    5: "brick (plain 3D)",
    205: "brickUP",
    105: "bbarBrickUP",
    1005: "SSPbrickUP",
    1055: "SSPbrick",

    10051: "ASD3D_B",
    10052: "ASD3D_L",
    10053: "ASD3D_R",
    10054: "ASD3D_F",
    10055: "ASD3D_K",
    10056: "ASD3D_BL",
    10057: "ASD3D_BR",
    10058: "ASD3D_BF",
    10059: "ASD3D_BK",
    10060: "ASD3D_LF",
    10061: "ASD3D_LK",
    10062: "ASD3D_RF",
    10063: "ASD3D_RK",
    10064: "ASD3D_BLF",
    10065: "ASD3D_BLK",
    10066: "ASD3D_BRF",
    10067: "ASD3D_BRK",

    17: "20_8_BrickUP",
}

elementProfiles = {
    # structural elements, beam-type elements
    1:      {"ndm": 2, "ndf": 3, "needsP": False, "dofRule": _beam2D_DOFs},
    101:    {"ndm": 3, "ndf": 6, "needsP": False, "dofRule": _beam3D_DOFs},
    201:    {"ndm": 2, "ndf": 3, "needsP": False, "dofRule": _beam2D_DOFs},
    202:    {"ndm": 3, "ndf": 6, "needsP": False, "dofRule": _beam3D_DOFs},

    # 2D soil elements
    3:      {"ndm": 2, "ndf": 2, "needsP": False, "dofRule": _only2DOFs},
    10:     {"ndm": 2, "ndf": 3, "needsP": True, "dofRule": _both2and3DOFs},
    103:    {"ndm": 2, "ndf": 3, "needsP": True, "dofRule": _threeDOFs},
    1003:   {"ndm": 2, "ndf": 3, "needsP": True, "dofRule": _threeDOFs},

    # 2D ASD absorbing boundaries
    10031: {"ndm": 2, "ndf": 2, "needsP": False, "dofRule": _only2DOFs},  # ASD2D_B
    10032: {"ndm": 2, "ndf": 2, "needsP": False, "dofRule": _only2DOFs},  # ASD2D_L
    10033: {"ndm": 2, "ndf": 2, "needsP": False, "dofRule": _only2DOFs},  # ASD2D_R
    10034: {"ndm": 2, "ndf": 2, "needsP": False, "dofRule": _only2DOFs},  # ASD2D_BL
    10035: {"ndm": 2, "ndf": 2, "needsP": False, "dofRule": _only2DOFs},  # ASD2D_BR

    # 3D soil elements
    5:     {"ndm": 3, "ndf": 3, "needsP": False, "dofRule": _threeDOFs3D},  # plain brick: u, v, w
    205:   {"ndm": 3, "ndf": 4, "needsP": True, "dofRule": _fourDOFs3D},   # brickUP:     u, v, w, p
    105:   {"ndm": 3, "ndf": 4, "needsP": True, "dofRule": _fourDOFs3D},    # bbarBrickUP: u, v, w, p
    1005:  {"ndm": 3, "ndf": 4, "needsP": True, "dofRule": _fourDOFs3D},    # SSPbrickUP:  u, v, w, p
    1055:  {"ndm": 3, "ndf": 3, "needsP": False, "dofRule": _threeDOFs3D},  # SSPbrick:    u, v, w

    # 3D ASD absorbing boundaries
    10051: {"ndm": 3, "ndf": 3, "needsP": False, "dofRule": _threeDOFs3D},  # ASD3D_B
    10052: {"ndm": 3, "ndf": 3, "needsP": False, "dofRule": _threeDOFs3D},  # ASD3D_L
    10053: {"ndm": 3, "ndf": 3, "needsP": False, "dofRule": _threeDOFs3D},  # ASD3D_R
    10054: {"ndm": 3, "ndf": 3, "needsP": False, "dofRule": _threeDOFs3D},  # ASD3D_F
    10055: {"ndm": 3, "ndf": 3, "needsP": False, "dofRule": _threeDOFs3D},  # ASD3D_K
    10056: {"ndm": 3, "ndf": 3, "needsP": False, "dofRule": _threeDOFs3D},  # ASD3D_BL
    10057: {"ndm": 3, "ndf": 3, "needsP": False, "dofRule": _threeDOFs3D},  # ASD3D_BR
    10058: {"ndm": 3, "ndf": 3, "needsP": False, "dofRule": _threeDOFs3D},  # ASD3D_BF
    10059: {"ndm": 3, "ndf": 3, "needsP": False, "dofRule": _threeDOFs3D},  # ASD3D_BK
    10060: {"ndm": 3, "ndf": 3, "needsP": False, "dofRule": _threeDOFs3D},  # ASD3D_LF
    10061: {"ndm": 3, "ndf": 3, "needsP": False, "dofRule": _threeDOFs3D},  # ASD3D_LK
    10062: {"ndm": 3, "ndf": 3, "needsP": False, "dofRule": _threeDOFs3D},  # ASD3D_RF
    10063: {"ndm": 3, "ndf": 3, "needsP": False, "dofRule": _threeDOFs3D},  # ASD3D_RK
    10064: {"ndm": 3, "ndf": 3, "needsP": False, "dofRule": _threeDOFs3D},  # ASD3D_BLF
    10065: {"ndm": 3, "ndf": 3, "needsP": False, "dofRule": _threeDOFs3D},  # ASD3D_BLK
    10066: {"ndm": 3, "ndf": 3, "needsP": False, "dofRule": _threeDOFs3D},  # ASD3D_BRF
    10067: {"ndm": 3, "ndf": 3, "needsP": False, "dofRule": _threeDOFs3D},  # ASD3D_BRK

    17:    {"ndm": 3, "ndf": 4, "needsP": True, "dofRule": _twentyEightBrickDOFs},
}

"""elementProfiles = {
    # # type: (ndm, ndf, needsP)

    # structural elements, beam-type elements
    1:      (2, 3, False),  # elasticBeamColumn2D: u, v, theta
    101:    (3, 6, False),  # elasticBeamColumn3D: u, v, w, thetaX, thetaY, thetaZ
    201:    (2, 3, False),  # dispBeamColumn2D
    202:    (3, 6, False),  # dispBeamColumn3D

    # 2D soil elements
    3:      (2, 2, False),  # (4-node) plain quad: u, v
    10:     (2, 2, False),  # (9-node) quad: u, v
    103:    (2, 3, True),   # bbarQuadUP: u, v, p
    1003:   (2, 3, True),   # quadUP: u, v, p

    # 2D ASD absorbing boundaries
    10031:  (2, 2, False),  # ASD2D_B
    10032:  (2, 2, False),  # ASD2D_L
    10033:  (2, 2, False),  # ASD2D_R
    10034:  (2, 2, False),  # ASD2D_BL
    10035:  (2, 2, False),  # ASD2D_BR

    # 3D soil elements
    5:      (3, 3, False),  # plain brick: u, v, w
    105:    (3, 4, True),   # bbarBrickUP: u, v, w, p
    1005:   (3, 4, True),   # SSPbrickUP: u, v, w, p
    1055:   (3, 3, False),   # SSPbrick: u, v, w

    # 3D ASD absorbing boundaries
    10051:  (3, 3, False),  # ASD3D_B
    10052:  (3, 3, False),  # ASD3D_L
    10053:  (3, 3, False),  # ASD3D_R
    10054:  (3, 3, False),  # ASD3D_F
    10055:  (3, 3, False),  # ASD3D_K
    10056:  (3, 3, False),  # ASD3D_BL
    10057:  (3, 3, False),  # ASD3D_BR
    10058:  (3, 3, False),  # ASD3D_BF
    10059:  (3, 3, False),  # ASD3D_BK
    10060:  (3, 3, False),  # ASD3D_LF
    10061:  (3, 3, False),  # ASD3D_LK
    10062:  (3, 3, False),  # ASD3D_RF
    10063:  (3, 3, False),  # ASD3D_RK
    10064:  (3, 3, False),  # ASD3D_BLF
    10065:  (3, 3, False),  # ASD3D_BLK
    10066:  (3, 3, False),  # ASD3D_BRF
    10067:  (3, 3, False),  # ASD3D_BRK
}"""


def buildMainSoilTags(meshFile, overrides=None):
    """
    auto-build mainSoilTags from 1 to maxPhyGroup.
    optionally override specific entries.

    :param meshFile: (str) path to the .msh file
    :param overrides: (dict) optional {groupID: matTag} to override defaults

    :return: (dict) {groupID: matTag}
    """
    maxGroup = detectMaxPhyGroup(meshFile)
    mainSoilTags = {i: i for i in range(1, maxGroup + 1)}

    if overrides:
        mainSoilTags.update(overrides)

    return mainSoilTags


def outputFolder(meshFile):
    # this function takes as input "meshFile", a simple filename in the current directory
    # os.path.basename(meshFile)[0] --> removes/extracts just the filename, removing any folder path
    #                                   it strips away any/the directory and keeps only the file name
    # os.path.splitext(...)         --> splits the file name into 02 parts: the name[0] and the extension[1]
    #                                   (nameWithoutExtension, extension)
    #                               --> os.path.splitext(...)[0]: name without the extension
    baseName = os.path.splitext(os.path.basename(meshFile))[0]
    outPutFolder = os.path.join("TCL-Files", baseName)
    os.makedirs(outPutFolder, exist_ok=True)
    # exist_ok=False (the default): raises an error if the folder already exists
    # exist_ok=True: does nothing if the folder already exists, no error!
    return outPutFolder


def sortNodesByX(nodes, nodeCoords):
    # return nodes sorted by their x-coordinate
    return sorted(nodes, key=lambda n: nodeCoords[n][0])


def sortNodesByY(nodes, nodeCoords):
    # return nodes sorted by their y-coordinate
    return sorted(nodes, key=lambda n: nodeCoords[n][1])


def sortNodesByZ(nodes, nodeCoords):
    # return nodes sorted by their z-coordinates
    return sorted(nodes, key=lambda n: nodeCoords[n][2])


def filterELMTsByDIM(elements, structuralGroups):
    """
    this function detects whether the mesh contains any 3D soil elements; if yes, it keeps only 3D elements and always
    presevres structural elements (beams, interfaces) regardless of the dimension.

    if there are no 3D elements, it assumes a purely 2D model, and hence keeps only 2D soil elements, agaain always
    retaining structural groups

    :param elements:
    :param structuralGroups:

    :return: filteredELMTS --> a list of elemet dictionaries containing only the elements consistent with the detected
             dimensionality (2D or 3D) plus ALL structural elements
    """
    # we combine all structural groups into a single set for easier lookup and future completions
    allStructuralGroups = set()

    for groupSet in structuralGroups.values():
        # in python, A |= B ==> A = A | B
        allStructuralGroups |= groupSet

    #
    all3DTypes = (
            gmshType["tetrahedron"]
            | gmshType["hexahedron"]
            | derivativesType["bbarBrickUP"]
            | derivativesType["SSPbrickUP"]
            | derivativesType["SSPbrick"]
            | derivativesType["ASD3D"]
    )

    all2DTypes = (
            gmshType["quadrangle"]
            | gmshType["triangle"]
            | derivativesType["bbarQuadUP"]
            | derivativesType["quadUP"]
            | derivativesType["ASD2D"]
    )

    # detect if mesh has 3D elements
    has3D = any(el["type"] in all3DTypes for el in elements)

    if has3D:
        filteredELMTS = [
            el for el in elements
            if el["type"] in all3DTypes
            or el["group"] in allStructuralGroups
        ]

        # print("\n")
        # print("\ndetected 3D mesh --> ignoring surface elements (type 3) ...\n")

    else:
        filteredELMTS = [
            el for el in elements
            if el["type"] in all2DTypes
            # and (el["type"]) != 1 or el["group"]
            or el["group"] in allStructuralGroups
        ]

        # print("\n")
        # print("\ndetected 2D mesh --> keeping quads and beam line groups ONLY...\n")

    return filteredELMTS, has3D


def parseELMTsFromGMSH(meshFile):
    """
    parse the "$Elements" section from a GMSH .msh file

    :param meshFile:
    :return: elements

    :returns:
        list of dicts, each with:
            {
                "id": int,
                "type": int,
                "group": int,
                "nodes": list[int]
            }
    """
    elements = []

    with open(meshFile) as f:
        lines = f.readlines()

    inElements = False

    for line in lines:
        line = line.strip()

        if line == "$Elements":
            inElements = True
            continue

        elif line == "$EndElements":
            break

        if inElements:
            parts = line.split()

            if len(parts) > 4:
                try:
                    eleTag = int(parts[0])
                    elementType = int(parts[1])

                    # we NEED to ignore 0D point elements (gmsh type 15)
                    # we can keep record of the number of skipped points:

                    skippedPTS = 0

                    if elementType == 15:
                        skippedPTS += 1
                        # print(f"[INFO] skipping point element {eleTag}")
                        continue

                    # print(f"[INFO] skipped {skippedPTS} point elements (type-15 GMSH)")

                    numTags = int(parts[2])
                    phyGroup = int(parts[4])
                    ns = [int(n) for n in parts[3 + numTags:]]

                    elements.append(
                        {
                            "id": eleTag,
                            "type": elementType,
                            "group": phyGroup,
                            "nodes": ns
                        }
                    )

                except (ValueError, IndexError):
                    continue

    return elements


def remapELMTSType(elements, groupCategories):
    # applies remapping rules, previously defined, to elements based on their assigned physical groups
    # here we prefer to build a "reverse look-up" as: phyGroupID --> catergoryName

    groupToCategory = {}

    for categoryName, groupSet in groupCategories.items():
        for groupID in groupSet:
            groupToCategory[groupID] = categoryName

    # we then remap each element
    for el in elements:
        t = el["type"]  # original type from GMSH
        g = el["group"]  # original phy group ID from GMSH

        category = groupToCategory.get(g)

        if category is None:
            # if this group is NOT in any catergory then skip
            continue

        key = (t, category)
        if key in elementRemapping:
            el["type"] = elementRemapping[key]

    return elements


def summarizeRemaps(elements):
    total = len(elements)

    if total == 0:
        print("no elements to summarize!")
        return

    # count elements via type
    counts = {}

    for el in elements:
        t = el["type"]
        counts[t] = counts.get(t, 0) + 1

    # we then print the summary
    print("--------!!!!!!!!!!----------!!!!!!!!!!----------!!!!!!!!!!----------!!!!!!!!!!----------!!!!!!!!!!-------")
    print(f"summary of elements remaps ({total} total):")
    print("---------------------------------------------------------------------------------------------------------")

    for t, count in sorted(counts.items()):
        label = elementLabels.get(t, "unknown")
        pct = (count / total) * 100
        print(f"  {count:6d}  -->  {label:25s}  (type {t:5d})     [{pct:6.2f}%]")

    print(f"   {total:6d}   TOTAL                                                       [100.00%]")
    print("--------!!!!!!!!!!----------!!!!!!!!!!----------!!!!!!!!!!----------!!!!!!!!!!----------!!!!!!!!!!-------")


def detect_ndm_ndf(elements):
    """
    ! determine ndm global as well as ndf global based on active element types that are present
    ! returns (ndm, ndf)

    :param elements:

    :return: (ndm, ndf)
    """
    if not elements:
        return 2, 2  # dafualt output in case there are no elements

    usedTypes = {el["type"] for el in elements}

    # then we filter to only types we know about
    knownTypes = {t for t in usedTypes if t in elementProfiles}

    if not knownTypes:
        return 2, 2

    ndmGlobal = max(elementProfiles[t]["ndm"] for t in knownTypes)
    ndfGlobal = max(elementProfiles[t]["ndf"] for t in knownTypes)

    print("\n")
    print(f"[INFO] detected element types: {sorted(knownTypes)}")
    print(f"[INFO] ndmGlobal = {ndmGlobal}, ndfGlobal = {ndfGlobal}")

    return ndmGlobal, ndfGlobal


def classifyNodeDOFs(elements, structuralGroups):
    """
    build dictonaries of DOFs for both soil and the structure nodes

    for each element, it calls its dofRule function to get DOFs per node;
    if a node is used by multiple elements, it takes the maximum DOF count

    :param elements:
    :param structuralGroups:

    :return: (nodeDOFS_soil, nodeDOFS_struct, nodeDOFs)
    """

    allStructuralGroups = set()

    for groupSet in structuralGroups.values():
        allStructuralGroups |= groupSet

    nodeDOFS_soil = {}
    nodeDOFS_struct = {}

    for el in elements:
        eType = el["type"]

        # we skip if we don't have a profile for this element (we can extend this by adding some rule)
        if eType not in elementProfiles:
            continue

        dofRule = elementProfiles[eType]["dofRule"]
        dofMap = dofRule(el["nodes"])

        # check if this element is soil or structural
        if el["group"] in allStructuralGroups:
            target = nodeDOFS_struct
        else:
            target = nodeDOFS_soil

        # assigning DOFs to nodes then, and taking maximum if node already exists

        for nodeTag, dofCount in dofMap.items():
            if nodeTag not in target or dofCount > target[nodeTag]:
                target[nodeTag] = dofCount

    # combinaition of both dictionaries (structure overrides soil in case the node appears in both)
    nodeDOFs = {**nodeDOFS_soil, **nodeDOFS_struct}

    return nodeDOFS_soil, nodeDOFS_struct, nodeDOFs


def summarizeNodeDOFs(nodeDOFs):
    """
    !!! prints a summary of DOF categories
    !!! does NOT modify any data structures

    :param nodeDOFs:

    :return: summary of node DOFs
    """
    print("\n")
    print("--------!!!!!!!!!!----------!!!!!!!!!!----------!!!!!!!!!!----------!!!!!!!!!!----------!!!!!!!!!!-------")
    print("node DOF summary")
    print("---------------------------------------------------------------------------------------------------------")

    if not nodeDOFs:
        print("no nodes found")
        print(
            "--------!!!!!!!!!!----------!!!!!!!!!!----------!!!!!!!!!!----------!!!!!!!!!!----------!!!!!!!!!!-------")
        return

    uniqueDOFs = sorted(set(nodeDOFs.values()))
    print(f"total nodes detected: {len(nodeDOFs)}\n")

    dofLabels = {
        2: "u, v (2D soils / ASD boundaries)",
        3: "u, v, p  or  u, v, w (UP soils / 3D solids)",
        4: "u, v, w, p (3D UP solids)",
        6: "u, v, w, rX, rY, rZ (3D beams)"
    }

    for dof in uniqueDOFs:
        nodesOfThisDOF = [n for n, d in nodeDOFs.items() if d == dof]
        label = dofLabels.get(dof, "")
        print(f"    {dof}-DOF nodes: {len(nodesOfThisDOF):6d}   {label}")

    print("--------!!!!!!!!!!----------!!!!!!!!!!----------!!!!!!!!!!----------!!!!!!!!!!----------!!!!!!!!!!-------")


def _axis_pair_indices(vertical_axis):
    """
    for a chosen verticla axis (0=x, 1=y, 2=z), returns the two in-plane axis indices.
    example: vertical_axis=2 (z axip up) --> in-plane axes are x-axis(i.e., 0) and y-axis(i.e., 1)

    :param vertical_axis: (int) 0, 1, or 2

    :return: (tuple) two axis indices
    """

    axes = [0, 1, 2]
    axes.remove(vertical_axis)

    return axes[0], axes[1]


def _get_coord(nodeID, nodeCoords):
    """
    get the coordinates for a node ID dict

    :param nodeID: (int) node ID
    :param nodeCoords: (dict) mapping nodeID --> (x, y, z)

    :return: (tupple) coordinates: (x, y, z)
    """

    if nodeCoords is None:
        raise ValueError("nodeCoords is required for coordinate-based hex reordering")

    coords = nodeCoords.get(nodeID)

    if coords is None:
        raise KeyError(f"node ID {nodeID} NOT found in nodeCoords")

    return coords


def classify_hex8_nodes(nodeList, nodeCoords, vertical_axis=2, tol=1e-9):
    """
    re-ordering of a 08-node hex from GMSH ordering to conventional OpenSees canonical ordering.

    bottom face (min vertical):
        1: (min a, min b)
        2: (max a, min b)
        3: (max a, max b)
        4: (min a, max b)

    top face (max vertical), directly above:
        - 5 above 1,
        - 6 above 2
        - 7 above 3
        - 8 above 4

    :param nodeList: (list) 08 node IDs from GMHS
    :param nodeCoords: (dict) mapping node ID --> (x, y, z)
    :param vertical_axis: (int) 0=x, 1=y, 2=z (default z)
    :param tol: (float) tolerance for coordinate comparison

    :return: (list) reordered node IDs for OpenSees
    """

    if len(nodeList) != 8:
        raise ValueError(f"Expected 08 nodes for hex8, got instead {len(nodeList)}")

    a_axis, b_axis = _axis_pair_indices(vertical_axis)
    
    # we collect the pair (nodeIDs, coords)
    pts = []

    for nid in nodeList:
        coords = _get_coord(nid, nodeCoords)
        pts.append((nid, coords))

    # splitting into bottom/top by vertical coordinate
    v_vals = [p[1][vertical_axis] for p in pts]
    v_min = min(v_vals)
    v_max = max(v_vals)

    bottom = [p for p in pts if abs(p[1][vertical_axis] - v_min) <= tol]
    top = [p for p in pts if abs(p[1][vertical_axis] - v_max) <= tol]

    # in case the tolerance is too strict, we can fall back to sorting by vertical coordinate
    if len(bottom) != 4 or len(top) != 4:
        raise ValueError("could not unfortunately split hex nodes into 04 bottom + 04 top --> check geometry OR tol")

    # helper to get (a, b) coordinates
    def ab(p):
        return p[1][a_axis], p[1][b_axis]

    a_vals = [ab(p)[0] for p in bottom]
    b_vals = [ab(p)[1] for p in bottom]

    a_min, a_max = min(a_vals), max(a_vals)
    b_min, b_max = min(b_vals), max(b_vals)

    def pick(face, a_target, b_target):
        """
        we pick the closest node on that face to the target (a, b) corner

        :param face:
        :param a_target:
        :param b_target:

        :return:
        """

        best = None
        best_d2 = None

        for p in face:
            pa, pb = ab(p)
            d2 = (pa - a_target) ** 2 + (pb - b_target) ** 2

            if best is None or d2 < best_d2:
                best = p
                best_d2 = d2

        return best[0]

    # bottom nodes in diagram order
    n1 = pick(bottom, a_min, b_min)
    n2 = pick(bottom, a_max, b_min)
    n3 = pick(bottom, a_max, b_max)
    n4 = pick(bottom, a_min, b_max)

    # top nodes: find the closest top node to each bottom node (in a, b plane)
    def closest_top_to(n_bottom):
        bcoords = _get_coord(n_bottom, nodeCoords)
        ba = bcoords[a_axis]
        bb = bcoords[b_axis]
        best = None
        best_d2 = None

        for p in top:
            tid = p[0]
            ta = p[1][a_axis]
            tb = p[1][b_axis]
            d2 = (ta - ba) ** 2 + (tb - bb) ** 2

            if best is None or d2 < best_d2:
                best = tid
                best_d2 = d2

        return best

    n5 = closest_top_to(n1)
    n6 = closest_top_to(n2)
    n7 = closest_top_to(n3)
    n8 = closest_top_to(n4)

    # makeing sure it is unique (if duplicates then fall back to corner picking on the top)
    if len({n5, n6, n7, n8}) != 4:
        ta_vals = [ab(p)[0] for p in top]
        tb_vals = [ab(p)[1] for p in top]
        ta_min, ta_max = min(ta_vals), max(ta_vals)
        tb_min, tb_max = min(tb_vals), max(tb_vals)

        n5 = pick(top, ta_min, tb_min)
        n6 = pick(top, ta_max, tb_min)
        n7 = pick(top, ta_max, tb_max)
        n8 = pick(top, ta_min, tb_max)

    return [n1, n2, n3, n4, n5, n6, n7, n8]


def classify_hex20_nodes(nodeList, nodeCoords, vertical_axis=2, tol=1e-9):
    """
    Re-ordering of a 20-node hex from GMSH ordering to OpenSees 20_8_BrickUP canonical ordering.

    Corner nodes (bottom face, min vertical):
        1: (min a, min b)
        2: (max a, min b)
        3: (max a, max b)
        4: (min a, max b)

    Corner nodes (top face, max vertical):
        5: above 1,  6: above 2,  7: above 3,  8: above 4

    Mid-edge nodes (bottom face):
        9:  (a_mid, b_min)    10: (a_max, b_mid)
        11: (a_mid, b_max)    12: (a_min, b_mid)

    Mid-edge nodes (top face):
        13: (a_mid, b_min)    14: (a_max, b_mid)
        15: (a_mid, b_max)    16: (a_min, b_mid)

    Vertical mid-edge nodes:
        17: (a_min, b_min)    18: (a_max, b_min)
        19: (a_max, b_max)    20: (a_min, b_max)

    :param nodeList:      (list) 20 node IDs from GMSH
    :param nodeCoords:    (dict) mapping node ID --> (x, y, z)
    :param vertical_axis: (int) 0=x, 1=y, 2=z (default z)
    :param tol:           (float) tolerance for coordinate comparison

    :return: (list) reordered node IDs for OpenSees
    """

    if len(nodeList) != 20:
        raise ValueError(f"Expected 20 nodes for hex20, got instead {len(nodeList)}")

    a_axis, b_axis = _axis_pair_indices(vertical_axis)

    pts = []
    for nid in nodeList:
        coords = _get_coord(nid, nodeCoords)
        pts.append((nid, coords))

    # split by vertical coordinate into bottom / top / vertical-mid
    v_vals = [p[1][vertical_axis] for p in pts]
    v_min = min(v_vals)
    v_max = max(v_vals)

    bottom_all = [p for p in pts if abs(p[1][vertical_axis] - v_min) <= tol]
    top_all    = [p for p in pts if abs(p[1][vertical_axis] - v_max) <= tol]
    vert_mids  = [p for p in pts if abs(p[1][vertical_axis] - v_min) > tol
                                 and abs(p[1][vertical_axis] - v_max) > tol]

    if len(bottom_all) != 8 or len(top_all) != 8 or len(vert_mids) != 4:
        raise ValueError(
            f"Could not split 20 hex nodes into 8 bottom + 8 top + 4 vertical mids. "
            f"Got: {len(bottom_all)} bottom, {len(top_all)} top, {len(vert_mids)} vert_mids. "
            f"Check geometry or tol."
        )

    # helper to get (a, b) for a point
    def ab(p):
        return p[1][a_axis], p[1][b_axis]

    # compute a/b bounds from bottom face
    a_vals = [ab(p)[0] for p in bottom_all]
    b_vals = [ab(p)[1] for p in bottom_all]
    a_min, a_max = min(a_vals), max(a_vals)
    b_min, b_max = min(b_vals), max(b_vals)

    # split bottom/top into corners vs mid-edge nodes
    def is_corner(p):
        pa, pb = ab(p)
        a_on_edge = abs(pa - a_min) <= tol or abs(pa - a_max) <= tol
        b_on_edge = abs(pb - b_min) <= tol or abs(pb - b_max) <= tol
        return a_on_edge and b_on_edge

    bottom_corners = [p for p in bottom_all if is_corner(p)]
    bottom_mids    = [p for p in bottom_all if not is_corner(p)]
    top_corners    = [p for p in top_all    if is_corner(p)]
    top_mids       = [p for p in top_all    if not is_corner(p)]

    if len(bottom_corners) != 4 or len(bottom_mids) != 4:
        raise ValueError(
            f"Could not split bottom face into 4 corners + 4 mids. "
            f"Got: {len(bottom_corners)} corners, {len(bottom_mids)} mids."
        )
    if len(top_corners) != 4 or len(top_mids) != 4:
        raise ValueError(
            f"Could not split top face into 4 corners + 4 mids. "
            f"Got: {len(top_corners)} corners, {len(top_mids)} mids."
        )

    # pick helper: closest node in a face to a target (a, b)
    def pick(face, a_target, b_target):
        best, best_d2 = None, None
        for p in face:
            pa, pb = ab(p)
            d2 = (pa - a_target) ** 2 + (pb - b_target) ** 2
            if best is None or d2 < best_d2:
                best, best_d2 = p, d2
        return best[0]

    a_mid = (a_min + a_max) / 2.0
    b_mid = (b_min + b_max) / 2.0

    # corner nodes
    n1 = pick(bottom_corners, a_min, b_min)
    n2 = pick(bottom_corners, a_max, b_min)
    n3 = pick(bottom_corners, a_max, b_max)
    n4 = pick(bottom_corners, a_min, b_max)

    n5 = pick(top_corners, a_min, b_min)
    n6 = pick(top_corners, a_max, b_min)
    n7 = pick(top_corners, a_max, b_max)
    n8 = pick(top_corners, a_min, b_max)

    # bottom mid-edge nodes
    n9  = pick(bottom_mids, a_mid, b_min)
    n10 = pick(bottom_mids, a_max, b_mid)
    n11 = pick(bottom_mids, a_mid, b_max)
    n12 = pick(bottom_mids, a_min, b_mid)

    # top mid-edge nodes
    n13 = pick(top_mids, a_mid, b_min)
    n14 = pick(top_mids, a_max, b_mid)
    n15 = pick(top_mids, a_mid, b_max)
    n16 = pick(top_mids, a_min, b_mid)

    # vertical mid-edge nodes
    n17 = pick(vert_mids, a_min, b_min)
    n18 = pick(vert_mids, a_max, b_min)
    n19 = pick(vert_mids, a_max, b_max)
    n20 = pick(vert_mids, a_min, b_max)

    return [n1,  n2,  n3,  n4,
            n5,  n6,  n7,  n8,
            n9,  n10, n11, n12,
            n13, n14, n15, n16,
            n17, n18, n19, n20]


def gmsh_hex20_to_canonical(nodeList, nodeCoords=None, vertical_axis=2, tol=1e-9):
    """
    Re-order GMSH hex20 nodes to OpenSees 20_8_BrickUP canonical ordering.

    preferred --> coordinate-based re-order if nodeCoords is provided
    fall back  --> raises error (no reliable legacy permutation for hex20)

    :param nodeList:
    :param nodeCoords:
    :param vertical_axis:
    :param tol:
    :return:
    """

    if nodeCoords is None:
        raise ValueError(
            "nodeCoords is required for hex20 reordering. "
            "No reliable legacy permutation exists for 20-node elements."
        )

    return classify_hex20_nodes(nodeList, nodeCoords, vertical_axis=vertical_axis, tol=tol)


def gmsh_hex8_to_canonical(nodeList, nodeCoords=None, vertical_axis=2, tol=1e-9):
    """
    re-order GMSH hex8 nodes to OpenSees canonical ordering

    preffered --> coordinate-based re-order if nodeCoords is provided
    fall back --> hard-coded permutation if nodeCoords in None

    :param nodeList:
    :param nodeCoords:
    :param vertical_axis:
    :param tol:
    :return:
    """

    if nodeCoords is not None:
        return classify_hex8_nodes(nodeList, nodeCoords, vertical_axis=vertical_axis, tol=tol)

    # falling bakc to the lagacy mapping if no coordinates avialable
    return [nodeList[2], nodeList[6], nodeList[7], nodeList[3],
            nodeList[1], nodeList[5], nodeList[4], nodeList[0]]


def parseNodesFromGMSH(meshFile, precision=6):
    """
    parse the "$Nodes" section from a GMSH .msh file

    how does it work?
        1. opens the mesh file and read all lines
        2. look for "$Nodes" section (i.e., between "$Nodes" and "$EndNodes")
        3. for each line in that section:
            - split into parts: [nodeTag, x, y, z]
            - parse nodeTag as interger
            - parse x, y, z as floats and round to specified precision
            - store in dictionary: {nodeTag: (x, y, z)}
        4. return the dictionary

    :param meshFile: (str) --> path to the .msh file
    :param precision: (int) --> decimal rounding for node coordinates

    :return: {nodeTag: (x, y, z)}: (dict)
    """

    nodeCoords = {}

    with open(meshFile) as f:
        lines = f.readlines()

    inNodes = False

    for line in lines:
        line = line.strip()

        if line == "$Nodes":
            inNodes = True
            continue

        elif line == "$EndNodes":
            break

        if inNodes:
            parts = line.split()

            if len(parts) >= 4:
                try:
                    nodeTag = int(parts[0])
                    x, y, *z = map(float, parts[1:])

                    x = round(x, precision)
                    y = round(y, precision)
                    zVal = round(z[0], precision) if z else 0.0

                    nodeCoords[nodeTag] = (x, y, zVal)

                except ValueError:
                    continue

    return nodeCoords


def writeNodesTCL(nodeCoords, ndmGLOBAL, nodeDOFs=None, filePrefix="nodes",
                  outputDir=".", elements=None, structuralGroups=None):
    """
    writes a unified .tcl file defining all nodes.

    :param nodeCoords: (dict) node coordinates, mapping nodeTag --> (x, y, z)
    :param ndmGLOBAL: (int) number of spatial dimensions (2 or 3)
    :param nodeDOFs: (dict, optional) mapping nodeTag --> DOF count
    :param filePrefix: (str) the prefix of the file to be written (default "nodes")
    :param outputDir: (str) folder where the file is witten --> the output directory
    :param elements: (list, optional) element list for domain classification
    :param structuralGroups: (dict, optional) structural group categories

    :return: file node
    """

    if nodeDOFs is None:
        nodeDOFs = {}

    # building per-node domain classification (soil versus structure)
    nodeDomain = {}

    if elements and structuralGroups:
        allStructuralGroups = set()

        for groupSet in structuralGroups.values():
            allStructuralGroups |= groupSet

        for el in elements:
            domain = "structure" if el["group"] in allStructuralGroups else "soil"

            for n in el["nodes"]:
                # just in case (of course, very rare and almost impossible) node belongs to both, structure overrides
                if n not in nodeDomain or domain == "structure":
                    nodeDomain[n] = domain

    # file name
    fileName = os.path.join(
        outputDir, f"{filePrefix}{'3D' if ndmGLOBAL == 3 else '2D'}.tcl"
    )

    with open(fileName, "w") as f:
        f.write(f"# !!!!!!!!!!---------- node definitions ({'3D' if ndmGLOBAL == 3 else '2D'}) ----------!!!!!!!!!\n\n")

        for n, coords in sorted(nodeCoords.items()):
            # write node line depending on dimension
            if ndmGLOBAL == 2:
                x, y, _ = coords
                f.write(f"node {n:<6} {x:.6f} {y:.6f}")

            elif ndmGLOBAL == 3:
                x, y, z = coords
                f.write(f"node {n:<6} {x:.6f} {y:.6f} {z:.6f}")

            else:
                continue

            # (TEST) add comment showing DOFs if available
            dofCount = nodeDOFs.get(n)

            if dofCount:
                domain = nodeDomain.get(n, "soil")

                if dofCount == 2:
                    label = "(u, v)"

                elif dofCount == 3 and ndmGLOBAL == 2:
                    label = "(u, v, thetaZ)" if domain == "structure" else "(u, v, p)"

                elif dofCount == 3 and ndmGLOBAL == 3:
                    label = "(u, v, w)"

                elif dofCount == 4:
                    label = "(u, v, w, p)"

                elif dofCount == 6:
                    label = "(u, v, w, thetaX, thetaY, thetaZ)"

                else:
                    label = ""

                f.write(f"      # {dofCount} DOFs {label}")

            f.write("\n")

    print(f"wrote {fileName} with {len(nodeCoords)} nodes")


def writeSeparatedNodeFiles(nodeCoords, nodeDOFs, ndmGLOBAL, filePrefix="nodesByDOF", outputDir=".", labelPrefix=""):
    """

    :param nodeCoords: (dict) mapping nodeTag --> (x, y, z)
    :param nodeDOFs: (dict) mapping nodeTag --> DOF count
    :param ndmGLOBAL: (int) spatial dim which can either be 2 (for 2D problems) or 3 (for 3D problems)
    :param filePrefix: (str) output file prefix (default "nodesByDOF")
    :param outputDir: (str) directory for the written files
    :param labelPrefix: (str) to differentiate b/t soil and structure elements (e.g., "soil", "struct")

    :return: none (written files)
    """

    if not nodeDOFs:
        print("no nodes to write!!!")
        return

    uniqueDOFs = sorted(set(nodeDOFs.values()))
    written = []

    for dofCount in uniqueDOFs:
        # get all nodes with this particular DOF count
        nodeList = [n for n, d in nodeDOFs.items() if d == dofCount]

        if not nodeList:
            continue

        # construct fileName with optional prefix (if needed perhaps for clarity purposes)
        prefixPart = f"{labelPrefix}_" if labelPrefix else ""
        fileName = os.path.join(outputDir, f"{prefixPart}{filePrefix}_{dofCount}DOF.tcl")

        # build node lines 1st to calculate max length for alignment
        nodeLines = []

        for n in sorted(nodeList):
            x, y, z = nodeCoords.get(n, (0.0, 0.0, 0.0))

            if ndmGLOBAL == 2:
                line = f"node {n:<6} {x:.6f} {y:.6f}"

            else:
                line = f"node {n:<6} {x:.6f} {y:.6f} {z:.6f}"

            nodeLines.append(line)

        maxLen = max(len(line) for line in nodeLines)

        # write the file with aligned comments
        with open(fileName, "w") as f:
            f.write(f"# !!!!!!!!!!!!!!!!!!!!!!!!!!!! nodes with {dofCount} DOFs !!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")

            for line, n in zip(nodeLines, sorted(nodeList)):
                # determine the label based on DOF count
                if dofCount == 2:
                    label = "(u, v)"

                elif dofCount == 3 and ndmGLOBAL == 2:
                    # key fix: resolve soil versus structure meaning
                    if labelPrefix.lower().startswith("struct"):
                        label = "(u, v, thetaZ)"
                    else:
                        label = "(u, v, p)"

                elif dofCount == 3 and ndmGLOBAL == 3:
                    label = "(u, v, w)"

                elif dofCount == 4:
                    label = "(u, v, w, p)"

                elif dofCount == 6:
                    label = "(u, v, w, thetaX, thetaY, thetaZ)"

                else:
                    label = ""

                comment = f"# {dofCount} DOFs {label}"

                f.write(f"{line.ljust(maxLen + 4)}{comment}\n")

        written.append(fileName)

    # print summary just in case...
    print("\nsummary by DOF group:")

    for dofCount in uniqueDOFs:
        count = sum(1 for d in nodeDOFs.values() if d == dofCount)
        print(f"    {dofCount}-DOF nodes: {count}")

    print(f"wrote separated node files: {', '.join(written)}")


def getElementsTagByType(elements, targetTypes):
    """
    get element IDs for elements matching the specified types

    :param elements: (list) list of element dicts
    :param targetTypes: (set or list) element types to filter for

    :return: (list) element IDs matching the target types
    """
    return [el["id"] for el in elements if el["type"] in targetTypes]


def classifyChosenNodesByDOF(nodeList, nodeDOFs):
    """
    classify an already existing list of nodes according to their DOF count

    :param nodeList: (list) list of node tags
    :param nodeDOFs: (dict) mapping nodeTag --> dofCount

    :return: (dict) {dofCount: [nodeTags]}
    """

    groups = {}

    for node in nodeList:
        dof = nodeDOFs.get(node)

        if dof is None:
            continue

        groups.setdefault(dof, []).append(node)

    return groups


# ---------------------------- elements section ------------------------ elements section ----------------------------
# ---------------------------- elements section ------------------------ elements section ----------------------------
# ---------------------------- elements section ------------------------ elements section ----------------------------

def write_quad(el, f, matProps, materialTag, _nodeCoords=None):
    g = matProps["gravity"]
    alpha = np.deg2rad(matProps.get("alphaAngle", 0.0))

    soil = matProps["soil2D"]
    # groupOverrides = matProps.get("groupOverrides", {}).get(el["group"], {})
    groupOverrides = matProps.get("groupOverrides", {}).get(materialTag, {})
    thickness = groupOverrides.get("thickness", soil["thickness"])

    b1 = g * np.sin(alpha)
    b2 = -g * np.cos(alpha)

    nodes = " ".join(str(n) for n in el["nodes"])

    f.write(
        f"element quad {el['id']} {nodes} "
        f"{thickness} PlaneStrain {materialTag} "
        f"0.0 0.0 {b1} {b2}\n"
    )


def write_brickUP(el, f, matProps, materialTag, nodeCoords=None):
    """
    writes a single brickUP element to file

    :param el: element dict with 'id', 'nodes', 'group'
    :param f: file handle
    :param matProps: material properties dictionary
    :param materialTag: OpenSees material tag for this element's group
    :param nodeCoords: (dict) node coordinates for node reordering

    :return: None
    """

    g = matProps["gravity"]
    alpha = np.deg2rad(matProps.get("alphaAngle", 0.0))

    soil = matProps["soil3D"]
    groupOverrides = matProps.get("groupOverrides", {}).get(materialTag, {})

    porosity = groupOverrides.get("porosity", soil["porosity"])
    permX = groupOverrides.get("permX", soil["permX"])
    permY = groupOverrides.get("permY", soil["permY"])
    permZ = groupOverrides.get("permZ", soil["permZ"])

    fluidBulk = matProps["fluidBulk"]
    fluidDensity = matProps["fluidDensity"]

    # computed values
    bulk = fluidBulk / porosity
    # permXScaled = permX / (g * fluidDensity)
    permXScaled = permX
    # permYScaled = permY / (g * fluidDensity)
    permYScaled = permY
    # permZScaled = permZ / (g * fluidDensity)
    permZScaled = permZ

    # body forces
    bx = 0.0
    by = -g * np.sin(alpha)
    bz = -g * np.cos(alpha)

    # reorder nodes from Gmsh to OpenSees ordering
    nodesReordered = gmsh_hex8_to_canonical(el["nodes"], nodeCoords=nodeCoords)
    nodes = " ".join(str(n) for n in nodesReordered)

    f.write(
        f"element "
        f"brickUP "
        f"{el['id']} "
        f"{nodes} "
        f"{materialTag} "
        f"{bulk} "
        f"{fluidDensity} "
        f"{permXScaled} "
        f"{permYScaled} "
        f"{permZScaled} "
        f"{bx} "
        f"{by} "
        f"{bz}\n"
    )


def write_bbarQuadUP(el, f, matProps, materialTag, _nodeCoords=None):
    """
    writes a singel bbarQuadUP element to file...

    :param el: element dict with "ID", "nodes", "group"
    :param f: file handle
    :param matProps: material properties dictionary
    :param materialTag: OpenSees material tag for this element's group
    :param _nodeCoords: node coordinates

    :return:
    """

    g = matProps["gravity"]
    alpha = np.deg2rad(matProps.get("alphaAngle", 0.0))

    soil = matProps["soil2D"]
    groupOverrides = matProps.get("groupOverrides", {}).get(materialTag, {})

    thickness = groupOverrides.get("thickness", soil["thickness"])
    porosity = groupOverrides.get("porosity", soil["porosity"])
    hPerm = groupOverrides.get("hPerm", soil["hPerm"])
    vPerm = groupOverrides.get("vPerm", soil["vPerm"])

    fluidBulk = matProps["fluidBulk"]
    fluidDensity = matProps["fluidDensity"]

    # computed values
    bulk = fluidBulk / porosity
    hPermScaled = hPerm / (g * fluidDensity)
    vPermScaled = vPerm / (g * fluidDensity)
    b1 = g * np.sin(alpha)
    b2 = - g * np.cos(alpha)

    nodes = " ".join(str(n) for n in el["nodes"])

    f.write(
        f"element "
        f"bbarQuadUP "
        f"{el['id']} "
        f"{nodes} "
        f"{thickness} "
        f"{materialTag} "
        f"{bulk} "
        f"{fluidDensity} "
        f"{hPermScaled} "
        f"{vPermScaled} "
        f"{b1} "
        f"{b2} "
        f"0.0\n"
    )


def write_quadUP(el, f, matProps, materialTag, _nodeCoords=None):
    """
    writes a singel quadUP element to file...

    :param el: element dict with "ID", "nodes", "group"
    :param f: file handle
    :param matProps: material properties dictionary
    :param materialTag: OpenSees material tag for this element's group
    :param _nodeCoords: node coordinates

    :return:
    """

    # same logic as bbarQuadUP, but diff element name
    g = matProps["gravity"]
    alpha = np.deg2rad(matProps.get("alphaAngle", 0.0))

    soil = matProps["soil2D"]
    groupOverrides = matProps.get("groupOverrides", {}).get(materialTag, {})

    thickness = groupOverrides.get("thickness", soil["thickness"])
    porosity = groupOverrides.get("porosity", soil["porosity"])
    hPerm = groupOverrides.get("hPerm", soil["hPerm"])
    vPerm = groupOverrides.get("vPerm", soil["vPerm"])

    fluidBulk = matProps["fluidBulk"]
    fluidDensity = matProps["fluidDensity"]

    # computed values
    bulk = fluidBulk / porosity
    hPermScaled = hPerm / (g * fluidDensity)
    vPermScaled = vPerm / (g * fluidDensity)
    b1 = g * np.sin(alpha)
    b2 = - g * np.cos(alpha)

    nodes = " ".join(str(n) for n in el["nodes"])

    f.write(
        f"element "
        f"quadUP "
        f"{el['id']} "
        f"{nodes} "
        f"{thickness} "
        f"{materialTag} "
        f"{bulk} "
        f"{fluidDensity} "
        f"{hPermScaled} "
        f"{vPermScaled} "
        f"{b1} "
        f"{b2} "
        f"0.0\n"
    )


def write_ASD2D(el, f, matProps, boundaryType):
    """
    writing a single ASD2D absorbing boundary element

    :param el:
    :param f:
    :param matProps:
    :param boundaryType: "B", "L", "R", "BL", "BR"

    :return:
    """

    asd = matProps["ASD"]

    E = asd["E"]
    poisson = asd["poisson"]
    density = asd["density"]
    thickness = asd["thickness"]

    G = E / (2.0 * (1.0 + poisson))

    nodes = " ".join(str(n) for n in el["nodes"])

    line = (f"element "
            f"ASDAbsorbingBoundary2D "
            f"{el['id']} "
            f"{nodes} "
            f"{G} "
            f"{poisson} "
            f"{density} "
            f"{thickness} "
            f"{boundaryType}")

    # bottom boundaries need -fx for the input motion
    if "B" in boundaryType:
        line += " -fx $tsX"

    f.write(line + "\n")


def write_beam2D(el, f, matProps, _materialTag=None):
    """
    writes a single 2D beam element (elasticBeamColumn)

    :param el:
    :param f:
    :param matProps:
    :param _materialTag:
    :return:
    """

    beam = matProps["elBeam2D"]

    A = beam["A"]
    E = beam["E"]
    Iz = beam["Iz"]
    transfTag = beam["transfTag"]
    massDens = beam.get("massDens", 0.0)
    useCMass = beam.get("useCMass", False)

    nodes = " ".join(str(n) for n in el["nodes"])

    line = (f"element "
            f"elasticBeamColumn "
            f"{el['id']} "
            f"{nodes} "
            f"{A} "
            f"{E} "
            f"{Iz} "
            f"{transfTag} ")

    if massDens:
        line += f" -mass {massDens}"
    if useCMass:
        line += " -cMass"

    f.write(line + "\n")


def write_beam3D(el, f, matProps, _materialTag=None):
    """
    writes a single 3D beam element (elasticBeamColumn)

    :param el:
    :param f:
    :param matProps:
    :param _materialTag:
    :return:
    """

    beam = matProps["elBeam3D"]

    A = beam["A"]
    E = beam["E"]
    G = beam["G"]
    J = beam["J"]
    Iy = beam["Iy"]
    Iz = beam["Iz"]
    transfTag = beam["transfTag"]
    massDens = beam.get("massDens", 0.0)
    useCMass = beam.get("useCMass", False)

    nodes = " ".join(str(n) for n in el["nodes"])

    line = (f"element "
            f"elasticBeamColumn "
            f"{el['id']} "
            f"{nodes} "
            f"{A} "
            f"{E} "
            f"{G} "
            f"{J} "
            f"{Iy} "
            f"{Iz} "
            f"{transfTag} ")

    if massDens:
        line += f" -mass {massDens}"
    if useCMass:
        line += " -cMass"

    f.write(line + "\n")


# %%%%%%%%%%%%%%%%%%%%%%%%%% perhaps RE-WRITE as from HERE %%%%%%%%%%%%%%%%%%%%%%%%%% copied-pasted %%%%%%%%%%%%%%%%%%%%
def write_SSPbrickUP(el, f, matProps, materialTag, nodeCoords=None):
    """
    Writes a single SSPbrickUP element to file.

    OpenSees syntax:
        element SSPbrickUP $eleTag $n1...$n8 $matTag
                           $fBulk $fDen
                           $k1 $k2 $k3
                           $void $alpha
                           <$b1 $b2 $b3>

    Fixed vs. original:
        - $fBulk  : raw fluid bulk modulus (NOT divided by porosity)
        - $void   : voids ratio written to output        (was MISSING)
        - $alpha  : stabilization parameter written      (was MISSING)

    The stabilization parameter alpha is computed as:
        alpha = h^2 / (4 * (Ks + 4/3 * Gs))
    where h is the characteristic element size and Ks, Gs are the bulk
    and shear moduli of the solid skeleton.

    To supply these, add to materialProps["soil3D"] (and/or per-group
    overrides) the keys:
        "Ks"         -- solid skeleton bulk modulus  [same units as stress]
        "Gs"         -- solid skeleton shear modulus [same units as stress]
        "alphaStab"  -- (optional) override: supply alpha directly
                        if Ks/Gs are not known. Fallback default: 6e-5.

    :param el:          element dict with 'id', 'nodes', 'group'
    :param f:           file handle
    :param matProps:    material properties dictionary
    :param materialTag: OpenSees nDMaterial tag for this element's group
    :param nodeCoords:  (dict) node tag -> (x, y, z) for node reordering

    :return: None
    """

    g     = matProps["gravity"]
    slope = np.deg2rad(matProps.get("alphaAngle", 0.0))

    soil          = matProps["soil3D"]
    groupOverrides = matProps.get("groupOverrides", {}).get(materialTag, {})

    # fluid properties (passed raw to the element)
    fluidBulk    = matProps["fluidBulk"]       # $fBulk: raw bulk modulus of pore fluid
    fluidDensity = matProps["fluidDensity"]    # $fDen

    # soil layer properties (with per-group overrides)
    void = groupOverrides.get("void", soil["void"])   # $void (voids ratio)
    permX    = groupOverrides.get("permX",    soil["permX"])
    permY    = groupOverrides.get("permY",    soil["permY"])
    permZ    = groupOverrides.get("permZ",    soil["permZ"])

    # permeability scaling: k [m/s] --> k/(g*rho_f) [m^2/(kN*s)]
    # permXScaled = permX / (g * fluidDensity)
    # permYScaled = permY / (g * fluidDensity)
    # permZScaled = permZ / (g * fluidDensity)

    # stabilization parameter alpha
    # Prefer an explicit override, then try to compute from Ks/Gs + element
    # size, and finally fall back to a default of 6e-5 (from the wiki example).
    if "alphaStab" in groupOverrides:
        alphaStab = groupOverrides["alphaStab"]
    elif "alphaStab" in soil:
        alphaStab = soil["alphaStab"]
    elif "Ks" in soil and "Gs" in soil and nodeCoords is not None:
        Ks = groupOverrides.get("Ks", soil["Ks"])
        Gs = groupOverrides.get("Gs", soil["Gs"])
        # characteristic element size h = cube-root of element volume
        coords = np.array([nodeCoords[n] for n in el["nodes"]])
        x_span = coords[:, 0].max() - coords[:, 0].min()
        y_span = coords[:, 1].max() - coords[:, 1].min()
        z_span = coords[:, 2].max() - coords[:, 2].min()
        h = (x_span * y_span * z_span) ** (1.0 / 3.0)
        alphaStab = h**2 / (4.0 * (Ks + (4.0 / 3.0) * Gs))
    else:
        alphaStab = 6.0e-5   # wiki example default; user should supply Ks/Gs
        print(
            f"[WARNING] SSPbrickUP element {el['id']}: alphaStab not found in "
            f"materialProps. Using fallback value {alphaStab}. "
            f"Supply 'alphaStab', or 'Ks'+'Gs', in soil3D or groupOverrides."
        )

    # body forces (gravitational vector components)
    bx = 0.0                  # along-slope component
    by = -g * np.sin(slope)
    bz = -g * np.cos(slope)   # vertical component (downward)

    # node reordering: Gmsh hex8 --> OpenSees brickUP ordering ---
    nodesReordered = gmsh_hex8_to_canonical(el["nodes"], nodeCoords=nodeCoords)
    nodes = " ".join(str(n) for n in nodesReordered)

    # write element line
    f.write(
        f"element SSPbrickUP "
        f"{el['id']} "
        f"{nodes} "
        f"{materialTag} "
        f"{fluidBulk} "       # $fBulk  -- raw fluid bulk modulus
        f"{fluidDensity} "    # $fDen
        f"{permX} "     # $k1
        f"{permY} "     # $k2
        f"{permZ} "     # $k3
        f"{void} "        # $void   -- voids ratio 
        f"{alphaStab} "       # $alpha  -- stabilization param 
        f"{bx} "              # $b1
        f"{by} "              # $b2
        f"{bz}\n"             # $b3
    )


def write_bbarBrickUP(el, f, matProps, materialTag, nodeCoords=None):
    """
    writes a single bbarBrickUP element to file

    :param el: element dict with 'id', 'nodes', 'group'
    :param f: file handle
    :param matProps: material properties dictionary
    :param materialTag: OpenSees material tag for this element's group
    :param nodeCoords: (dict) node coordinates for node reordering

    :return: None
    """

    g = matProps["gravity"]
    alpha = np.deg2rad(matProps.get("alphaAngle", 0.0))

    soil = matProps["soil3D"]
    groupOverrides = matProps.get("groupOverrides", {}).get(materialTag, {})

    porosity = groupOverrides.get("porosity", soil["porosity"])
    permX = groupOverrides.get("permX", soil["permX"])
    permY = groupOverrides.get("permY", soil["permY"])
    permZ = groupOverrides.get("permZ", soil["permZ"])

    fluidBulk = matProps["fluidBulk"]
    fluidDensity = matProps["fluidDensity"]

    # computed values
    bulk = fluidBulk / porosity
    permXScaled = permX / (g * fluidDensity)
    permYScaled = permY / (g * fluidDensity)
    permZScaled = permZ / (g * fluidDensity)

    # body forces
    bx = g * np.sin(alpha)
    by = 0.0
    bz = -g * np.cos(alpha)

    # reorder nodes from Gmsh to OpenSees ordering
    nodesReordered = gmsh_hex8_to_canonical(el["nodes"], nodeCoords=nodeCoords)
    nodes = " ".join(str(n) for n in nodesReordered)

    f.write(
        f"element "
        f"bbarBrickUP "
        f"{el['id']} "
        f"{nodes} "
        f"{materialTag} "
        f"{bulk} "
        f"{fluidDensity} "
        f"{permXScaled} "
        f"{permYScaled} "
        f"{permZScaled} "
        f"{bx} "
        f"{by} "
        f"{bz}\n"
    )


def write_SSPbrick(el, f, matProps, materialTag, nodeCoords=None):
    """
    writes a single SSPbrick element (no pore pressure) to file

    :param el: element dict with 'id', 'nodes', 'group'
    :param f: file handle
    :param matProps: material properties dictionary
    :param materialTag: OpenSees material tag for this element's group
    :param nodeCoords: (dict) node coordinates for node reordering

    :return: None
    """

    g = matProps["gravity"]
    alpha = np.deg2rad(matProps.get("alphaAngle", 0.0))

    # body forces
    bx = g * np.sin(alpha)
    by = 0.0
    bz = -g * np.cos(alpha)

    # reorder nodes from Gmsh to OpenSees ordering
    nodesReordered = gmsh_hex8_to_canonical(el["nodes"], nodeCoords=nodeCoords)
    nodes = " ".join(str(n) for n in nodesReordered)

    f.write(
        f"element "
        f"SSPbrick "
        f"{el['id']} "
        f"{nodes} "
        f"{materialTag} "
        f"{bx} "
        f"{by} "
        f"{bz}\n"
    )


def write_ASD3D(el, f, matProps, boundaryType, nodeCoords=None):
    """
    writes a single ASD3D absorbing boundary element

    :param el: element dict with 'id', 'nodes', 'group'
    :param f: file handle
    :param matProps: material properties dictionary
    :param boundaryType: "B", "L", "R", "F", "K", "BL", "BR", "BF", "BK", "LF", "LK", "RF", "RK", "BLF", "BLK", "BRF", "BRK"
    :param nodeCoords: (dict) node coordinates for node reordering

    :return: None
    """

    asd = matProps["ASD"]

    E = asd["E"]
    poisson = asd["poisson"]
    density = asd["density"]

    G = E / (2.0 * (1.0 + poisson))

    # reorder nodes from Gmsh to OpenSees ordering
    nodesReordered = gmsh_hex8_to_canonical(el["nodes"], nodeCoords=nodeCoords)
    nodes = " ".join(str(n) for n in nodesReordered)

    line = (
        f"element ASDAbsorbingBoundary3D {el['id']} {nodes} "
        f"{G} {poisson} {density} {boundaryType}"
    )

    # add time series for input motion based on boundary type
    if "B" in boundaryType:
        line += " -fx $tsX"
    if "F" in boundaryType or "K" in boundaryType:
        line += " -fy $tsY"

    f.write(line + "\n")


# def gmsh_hex20_to_canonical(nodeList):
#     """
#     reorder Gmsh 20-node hex to OpenSees 20_8_BrickUP ordering
#
#     :param nodeList: (list) 20 node IDs from Gmsh
#
#     :return: (list) reordered node IDs for OpenSees
#     """
#
#     if len(nodeList) != 20:
#         raise ValueError(f"Expected 20 nodes for hex20, got {len(nodeList)}")
#
#     # hard-coded permutation based on verified mapping
#     return [
#         nodeList[2], nodeList[6], nodeList[7], nodeList[3],      # bottom corners
#         nodeList[1], nodeList[5], nodeList[4], nodeList[0],      # top corners
#         nodeList[14], nodeList[19], nodeList[15], nodeList[13],  # bottom mid-edge
#         nodeList[12], nodeList[16], nodeList[10], nodeList[8],   # top mid-edge
#         nodeList[11], nodeList[18], nodeList[17], nodeList[9]    # vertical mid-edge
#     ]


def write_20_8_BrickUP(el, f, matProps, materialTag, nodeCoords=None):
    """
    writes a single 20_8_BrickUP element to file

    :param el: element dict with 'id', 'nodes', 'group'
    :param f: file handle
    :param matProps: material properties dictionary
    :param materialTag: OpenSees material tag for this element's group
    :param nodeCoords: (dict) node coordinates (not used for 20-node, hard-coded mapping)

    :return: None
    """

    g = matProps["gravity"]
    alpha = np.deg2rad(matProps.get("alphaAngle", 0.0))

    soil = matProps["soil3D"]
    groupOverrides = matProps.get("groupOverrides", {}).get(materialTag, {})

    porosity = groupOverrides.get("porosity", soil["porosity"])
    permX = groupOverrides.get("permX", soil["permX"])
    permY = groupOverrides.get("permY", soil["permY"])
    permZ = groupOverrides.get("permZ", soil["permZ"])

    fluidBulk = matProps["fluidBulk"]
    fluidDensity = matProps["fluidDensity"]

    # computed values
    bulk = fluidBulk / porosity
    permXScaled = permX / (g * fluidDensity)
    permYScaled = permY / (g * fluidDensity)
    permZScaled = permZ / (g * fluidDensity)

    # body forces
    bx = g * np.sin(alpha)
    by = 0.0
    bz = -g * np.cos(alpha)

    # reorder nodes from Gmsh to OpenSees ordering (20-node specific)
    # nodesReordered = gmsh_hex20_to_canonical(el["nodes"])
    nodesReordered = gmsh_hex20_to_canonical(el["nodes"], nodeCoords=nodeCoords)
    nodes = " ".join(str(n) for n in nodesReordered)

    f.write(
        f"element 20_8_BrickUP {el['id']} {nodes} "
        f"{materialTag} {bulk} {fluidDensity} "
        f"{permXScaled} {permYScaled} {permZScaled} "
        f"{bx} {by} {bz}\n"
    )


elementWriters = {
    # 2D soil (no node reordering needed)
    3:      (write_quad, "quad"),
    103:    (write_bbarQuadUP, "bbarQuadUP"),
    1003:   (write_quadUP, "quadUP"),

    # 2D ASD boundaries (no node reordering needed)
    10031:  (lambda el, f, mp, mt, nc: write_ASD2D(el, f, mp, "B"), "ASD2D_B"),
    10032:  (lambda el, f, mp, mt, nc: write_ASD2D(el, f, mp, "L"), "ASD2D_L"),
    10033:  (lambda el, f, mp, mt, nc: write_ASD2D(el, f, mp, "R"), "ASD2D_R"),
    10034:  (lambda el, f, mp, mt, nc: write_ASD2D(el, f, mp, "BL"), "ASD2D_BL"),
    10035:  (lambda el, f, mp, mt, nc: write_ASD2D(el, f, mp, "BR"), "ASD2D_BR"),

    # 3D soil (node reordering needed)
    205:    (write_brickUP, "brickUP"),
    105:    (write_bbarBrickUP, "bbarBrickUP"),
    1005:   (write_SSPbrickUP, "SSPbrickUP"),
    1055:   (write_SSPbrick, "SSPbrick"),
    17:     (write_20_8_BrickUP, "20_8_BrickUP"),

    # 3D ASD boundaries (node reordering needed)
    10051:  (lambda el, f, mp, mt, nc: write_ASD3D(el, f, mp, "B", nc), "ASD3D_B"),
    10052:  (lambda el, f, mp, mt, nc: write_ASD3D(el, f, mp, "L", nc), "ASD3D_L"),
    10053:  (lambda el, f, mp, mt, nc: write_ASD3D(el, f, mp, "R", nc), "ASD3D_R"),
    10054:  (lambda el, f, mp, mt, nc: write_ASD3D(el, f, mp, "F", nc), "ASD3D_F"),
    10055:  (lambda el, f, mp, mt, nc: write_ASD3D(el, f, mp, "K", nc), "ASD3D_K"),
    10056:  (lambda el, f, mp, mt, nc: write_ASD3D(el, f, mp, "BL", nc), "ASD3D_BL"),
    10057:  (lambda el, f, mp, mt, nc: write_ASD3D(el, f, mp, "BR", nc), "ASD3D_BR"),
    10058:  (lambda el, f, mp, mt, nc: write_ASD3D(el, f, mp, "BF", nc), "ASD3D_BF"),
    10059:  (lambda el, f, mp, mt, nc: write_ASD3D(el, f, mp, "BK", nc), "ASD3D_BK"),
    10060:  (lambda el, f, mp, mt, nc: write_ASD3D(el, f, mp, "LF", nc), "ASD3D_LF"),
    10061:  (lambda el, f, mp, mt, nc: write_ASD3D(el, f, mp, "LK", nc), "ASD3D_LK"),
    10062:  (lambda el, f, mp, mt, nc: write_ASD3D(el, f, mp, "RF", nc), "ASD3D_RF"),
    10063:  (lambda el, f, mp, mt, nc: write_ASD3D(el, f, mp, "RK", nc), "ASD3D_RK"),
    10064:  (lambda el, f, mp, mt, nc: write_ASD3D(el, f, mp, "BLF", nc), "ASD3D_BLF"),
    10065:  (lambda el, f, mp, mt, nc: write_ASD3D(el, f, mp, "BLK", nc), "ASD3D_BLK"),
    10066:  (lambda el, f, mp, mt, nc: write_ASD3D(el, f, mp, "BRF", nc), "ASD3D_BRF"),
    10067:  (lambda el, f, mp, mt, nc: write_ASD3D(el, f, mp, "BRK", nc), "ASD3D_BRK"),

    # Beams (no node reordering needed)
    1:      (lambda el, f, mp, mt, nc: write_beam2D(el, f, mp, mt), "elasticBeamColumn2D"),
    101:    (lambda el, f, mp, mt, nc: write_beam3D(el, f, mp, mt), "elasticBeamColumn3D"),
    201:    (lambda el, f, mp, mt, nc: write_beam2D(el, f, mp, mt), "dispBeamColumn2D"),
    202:    (lambda el, f, mp, mt, nc: write_beam3D(el, f, mp, mt), "dispBeamColumn3D"),
}


def writeElementsTCL(elements, matProps, mainSoilTags, nodeCoords=None, filePrefix="elements_", outputDir="."):
    """
    write TCL files for all elements, grouped by type.

    :param elements: (list) element dicts with 'id', 'type', 'group', 'nodes'
    :param matProps: (dict) material properties
    :param mainSoilTags: (dict) physical group ID --> OpenSees material tag
    :param nodeCoords: (dict) node coordinates for 3D element node reordering
    :param filePrefix: (str) output file prefix
    :param outputDir: (str) output directory

    :return: (list) filenames written
    """

    print("\n[INFO] material mapping:")
    for groupID, matTag in mainSoilTags.items():
        print(f"    physical group {groupID} --> material tag {matTag}")

    # group elements by type
    elementsByType = {}

    for el in elements:
        eType = el["type"]
        if eType not in elementsByType:
            elementsByType[eType] = []
        elementsByType[eType].append(el)

    written = []

    for eType, elems in elementsByType.items():
        if eType not in elementWriters:
            print(f"[WARNING] no writer for element type {eType}, skipping {len(elems)} elements")
            continue

        writerFunc, elName = elementWriters[eType]
        fileName = os.path.join(outputDir, f"{filePrefix}{elName}.tcl")

        with open(fileName, "w") as f:
            f.write(f"# {elName} elements ({len(elems)} total)\n\n")

            for el in elems:
                # get material tag for this element's group
                matTag = mainSoilTags.get(el["group"], 1)  # default = 1 if not found
                writerFunc(el, f, matProps, matTag, nodeCoords)

        written.append(fileName)
        print(f"[INFO] wrote {fileName} ({len(elems)} elements)")

    return written


# ---------------------------- elements section ------------------------ elements section ----------------------------
# ---------------------------- elements section ------------------------ elements section ----------------------------
# ---------------------------- elements section ------------------------ elements section ----------------------------

def getBoundaryNodesFromMsh(meshFile, phyGroupIDs=None, dim=None):
    """
    returns the nodes belonging to elements of a specified geometric dimension
    (1=line, 2=surface, 3=volume); if no dimension is given, defaults to the
    'before last' element type (for backward compatibility).

    :param meshFile: (str) path to .msh file
    :param phyGroupIDs: (list[int]|None) if given, restricts nodes to these (or this) physical group(s)
    :param dim: (int, optional) geometric dimension to extract (1=line, 2=surface, 3=volume)

    :return: (set) node tags associated with the chosen element type(s)
    """

    # empty list mean "return empty"
    if not phyGroupIDs:
        return set()

    phyGroupSet = None if phyGroupIDs is None else set(phyGroupIDs)

    # map common element types to their geometric dimensions
    eleTypeToDim = {
        1: 1,    # 2-node line
        2: 2,    # 3-node triangle
        3: 2,    # 4-node quadrilateral
        4: 3,    # 4-node tetrahedron
        5: 3,    # 8-node hexahedron
        6: 3,    # 6-node prism
        7: 3,    # 5-node pyramid
        8: 1,    # 3-node quadratic line
        9: 2,    # 6-node quadratic triangle
        10: 2,   # 9-node quadratic quad
        11: 3,   # 10-node quadratic tetra
        16: 2,   # 8-node serendipity quad
        17: 3,   # 20-node serendipity hex
    }

    # step 1: collect element types from the mesh
    with open(meshFile) as f:
        lines = f.readlines()

    eleTypesRaw = []
    inElements = False

    for line in lines:
        line = line.strip()

        if line == "$Elements":
            inElements = True
            continue
        elif line == "$EndElements":
            break

        if inElements:
            parts = line.split()
            if len(parts) > 1:
                try:
                    eleType = int(parts[1])
                    eleTypesRaw.append(eleType)
                except ValueError:
                    continue

    # get distinct types in order of appearance
    distinctTypes = []
    for t in eleTypesRaw:
        if not distinctTypes or t != distinctTypes[-1]:
            distinctTypes.append(t)

    if not distinctTypes:
        raise RuntimeError(f"no elements found in {meshFile}")

    # step 2: determine which element types to target
    if dim is not None:
        # filter element types by requested dimension
        targetTypes = [t for t in distinctTypes if eleTypeToDim.get(t) == dim]
        if not targetTypes:
            raise ValueError(f"no elements of dimension {dim} found in {meshFile}")
    else:
        # default behavior: before-last distinct type
        eleTypeBL = distinctTypes[-2] if len(distinctTypes) >= 2 else distinctTypes[0]
        targetTypes = [eleTypeBL]

    # step 3: collect nodes from matching elements
    boundaryNodes = set()

    # with open(meshFile) as f:
    #     lines = f.readlines()

    inElements = False

    for line in lines:
        line = line.strip()

        if line == "$Elements":
            inElements = True
            continue
        elif line == "$EndElements":
            break

        if inElements:
            parts = line.split()
            if len(parts) >= 7:
                try:
                    eleType = int(parts[1])
                    phyGroup = int(parts[4])

                    groupOK = (phyGroupSet is None) or (phyGroup in phyGroupSet)

                    if eleType in targetTypes and groupOK:
                        nodesB = [int(n) for n in parts[5:]]
                        boundaryNodes.update(nodesB)
                except ValueError:
                    continue

    return boundaryNodes


def getCustomBoundaryNodesFromMsh(meshFile, nodeDOFs, phyGroupIDs=None, dim=None,
                                  keepDOFs=None, returnGrouped=False):
    """
    Extension of getBoundaryNodesFromMsh that additionally filters the returned
    nodes by their DOF count.  This is useful when a boundary plane contains a
    mix of node types (e.g., 3-DOF solid nodes and 4-DOF UP nodes) and you only
    need a subset of them.

    :param meshFile:     (str)            path to .msh file
    :param nodeDOFs:     (dict)           mapping nodeTag --> dofCount
                                          (as returned by classifyNodeDOFs)
    :param phyGroupIDs:  (list[int]|None) physical group IDs to restrict to
                                          (forwarded to getBoundaryNodesFromMsh)
    :param dim:          (int|None)       geometric dimension to extract
                                          (forwarded to getBoundaryNodesFromMsh)
    :param keepDOFs:     (int | list[int] | None)
                                          DOF count(s) to keep.
                                          • None  --> no DOF filtering, return all
                                            boundary nodes (same as the base call)
                                          • int   --> keep only nodes with that
                                            exact DOF count  (e.g. keepDOFs=3)
                                          • list  --> keep nodes whose DOF count
                                            is in the list  (e.g. keepDOFs=[3,4])
    :param returnGrouped:(bool)           if True, return a dict {dofCount: set}
                                          instead of a flat set; only DOF counts
                                          present in keepDOFs are included.

    :return: (set)  node tags that satisfy the DOF filter  -- if returnGrouped=False
             (dict) {dofCount: set_of_nodes}               -- if returnGrouped=True
    """

    # 1. get the raw boundary nodes (existing logic, untouched)
    rawNodes = getBoundaryNodesFromMsh(meshFile, phyGroupIDs=phyGroupIDs, dim=dim)

    # 2. normalise keepDOFs into a set (or None = keep everything)
    if keepDOFs is None:
        allowedDOFs = None
    elif isinstance(keepDOFs, int):
        allowedDOFs = {keepDOFs}
    else:
        allowedDOFs = set(keepDOFs)

    # 3. filter
    if allowedDOFs is None:
        filtered = rawNodes                           # no filter requested
    else:
        filtered = {n for n in rawNodes
                    if nodeDOFs.get(n) in allowedDOFs}

    # 4. optionally group by DOF count
    if not returnGrouped:
        return filtered

    grouped = {}
    for n in filtered:
        d = nodeDOFs.get(n)
        if d is not None:
            grouped.setdefault(d, set()).add(n)
    return grouped


# def detectMaxPhyGroup(meshFile):
#     """
#     scan a Gmsh .msh file and detect the maximum physical group ID
#     present in the $Elements section.
#
#     :param meshFile: (str) path to the Gmsh .msh file
#
#     :return: (int) maximum physical group ID found (0 if none)
#     """
#
#     # element types to consider (native gmsh + derivatives)
#     validTypes = (
#         # gmshType["line"] |
#         gmshType["quadrangle"]
#         | gmshType["hexahedron"]
#         | derivativesType["bbarQuadUP"]
#         | derivativesType["quadUP"]
#         | derivativesType["ASD2D"]
#         | derivativesType["bbarBrickUP"]
#         | derivativesType["SSPbrickUP"]
#         | derivativesType["SSPbrick"]
#         | derivativesType["ASD3D"]
#     )
#
#     maxPhyGroup = 0
#
#     with open(meshFile) as f:
#         lines = f.readlines()
#
#     inElements = False
#
#     for line in lines:
#         line = line.strip()
#
#         if line == "$Elements":
#             inElements = True
#             continue
#         elif line == "$EndElements":
#             break
#
#         if inElements:
#             parts = line.split()
#             if len(parts) > 4:
#                 try:
#                     elementType = int(parts[1])
#                     phyGroup = int(parts[4])
#
#                     if elementType in validTypes:
#                         if phyGroup > maxPhyGroup:
#                             maxPhyGroup = phyGroup
#                 except (ValueError, IndexError):
#                     continue
#
#     return maxPhyGroup


def detectMaxPhyGroup(meshFile):
    """
    scan a Gmsh .msh file and detect the maximum physical group ID
    for the LAST element type encountered in the $Elements section
    (typically the volumetric soil elements at the bottom of the file).

    :param meshFile: (str) path to the Gmsh .msh file
    :return: (int) maximum physical group ID found (0 if none)
    """
    with open(meshFile) as f:
        lines = f.readlines()

    # --- pass 1: find the last element type in the $Elements section ---
    lastEleType = None
    inElements = False

    for line in lines:
        line = line.strip()
        if line == "$Elements":
            inElements = True
            continue
        elif line == "$EndElements":
            break
        if inElements:
            parts = line.split()
            if len(parts) > 2:
                try:
                    lastEleType = int(parts[1])
                except ValueError:
                    continue

    if lastEleType is None:
        return 0

    # --- pass 2: find max physical group among elements of lastEleType only ---
    maxPhyGroup = 0
    inElements = False

    for line in lines:
        line = line.strip()
        if line == "$Elements":
            inElements = True
            continue
        elif line == "$EndElements":
            break
        if inElements:
            parts = line.split()
            if len(parts) > 4:
                try:
                    if int(parts[1]) == lastEleType:
                        phyGroup = int(parts[4])
                        if phyGroup > maxPhyGroup:
                            maxPhyGroup = phyGroup
                except (ValueError, IndexError):
                    continue

    return maxPhyGroup


class FuzzyFloat(float):
    """
    a float that compares equal within tolerance
    """

    __slots__ = ("tol",)

    def __new__(cls, value, tol):
        obj = float.__new__(cls, value)
        obj.tol = tol
        return obj

    def __eq__(self, other):
        return abs(float(self) - float(other)) < self.tol

    def __lt__(self, other):
        return float(self) < float(other) - self.tol

    def __le__(self, other):
        return float(self) <= float(other) + self.tol

    def __gt__(self, other):
        return float(self) > float(other) + self.tol

    def __ge__(self, other):
        return float(self) >= float(other) - self.tol


def _roundFunc(x, tol=defaultTol):
    """
    round a coordinate to the decimal precision implied by the tolerance

    :param x: (float) value to round
    :param tol: (float) tolerance (default 1e-6)

    :return: (float) rounded value
    """
    return round(x, int(abs(np.log10(tol))))


def selectNodes(condition, nodeCoords, tol=defaultTol, debug=False):
    """
    select nodes satisfying a user-defined boolean condition on (x, y, z).

    :param condition: callable (x, y, z) --> bool
    :param nodeCoords: (dict) mapping nodeTag --> (x, y, z)
    :param tol: (float) numerical tolerance for coordinate rounding
    :param debug: (bool) if True, prints the number of matched nodes

    :return: (list) node IDs satisfying the condition

    example:
        selectNodes(lambda x, y, z: x == 0.0 and y < 0.25, nodeCoords)
    """

    selected = []

    for n, (x, y, z) in nodeCoords.items():
        xR = _roundFunc(x, tol)
        yR = _roundFunc(y, tol)
        zR = _roundFunc(z, tol)

        xF = FuzzyFloat(xR, tol)
        yF = FuzzyFloat(yR, tol)
        zF = FuzzyFloat(zR, tol)

        try:
            if condition(xF, yF, zF):
                selected.append(n)
        except (ValueError, TypeError):
            continue

    if debug:
        print(f"matched {len(selected)} nodes for condition {condition}")

    return selected


"""
Drop-in additions for meshHelper.py

They follow the exact same style and use only functions already present:
    - parseNodesFromGMSH
    - selectNodes / FuzzyFloat
    - sortNodesByX / Y / Z

New functions added (3):
    (A) selectNodesByCoordRange  -- filter by one or more axis ranges
    (B) selectBoundaryNodes      -- auto-detect any face by axis + "min"/"max"/"value"
    (C) previewBoundaries        -- print a table of all 6 model faces and their node counts
                                    (handy diagnostic for any new mesh)

Usage in testFXNs.py (replaces the manual surface ID lists):
--------------------------------------------------------------------------------

    nodeCoords = mh.parseNodesFromGMSH(meshFile)

    # ------ base nodes (z = 0) ----------------------------------------
    baseNodes = mh.selectBoundaryNodes(nodeCoords, axis="z", face="min")

    # ------ top nodes (z = max) ----------------------------------------
    topNodes  = mh.selectBoundaryNodes(nodeCoords, axis="z", face="max")

    # ------ lateral faces ----------------------------------------------
    xMinNodes = mh.selectBoundaryNodes(nodeCoords, axis="x", face="min")
    xMaxNodes = mh.selectBoundaryNodes(nodeCoords, axis="x", face="max")
    yMinNodes = mh.selectBoundaryNodes(nodeCoords, axis="y", face="min")
    yMaxNodes = mh.selectBoundaryNodes(nodeCoords, axis="y", face="max")

    # ------ nodes inside a depth slice (e.g. z in [66, 76]) -----------
    layer3Nodes = mh.selectNodesByCoordRange(nodeCoords, zMin=66.0, zMax=76.0)

    # ------ diagnostic: print all 6 faces in one call -----------------
    mh.previewBoundaries(nodeCoords)

--------------------------------------------------------------------------------
"""

# ──────────────────────────────────────────────────────────────────────────────
# (A)  selectNodesByCoordRange
# ──────────────────────────────────────────────────────────────────────────────

def selectNodesByCoordRange(nodeCoords,
                            xMin=None, xMax=None,
                            yMin=None, yMax=None,
                            zMin=None, zMax=None,
                            tol=defaultTol):
    """
    select nodes whose coordinates fall within the specified axis-aligned range(s).

    any bound left as None is treated as ±∞ (i.e., no constraint on that side).
    uses FuzzyFloat so bounds are inclusive within tolerance.

    :param nodeCoords: (dict) mapping nodeTag --> (x, y, z)
    :param xMin: (float|None) lower x bound (inclusive)
    :param xMax: (float|None) upper x bound (inclusive)
    :param yMin: (float|None) lower y bound
    :param yMax: (float|None) upper y bound
    :param zMin: (float|None) lower z bound
    :param zMax: (float|None) upper z bound
    :param tol:  (float)      geometric tolerance

    :return: (list) node IDs satisfying all specified bounds

    examples:
        # all nodes in the top layer (z between 100 and 104)
        selectNodesByCoordRange(nodeCoords, zMin=100.0, zMax=104.0)

        # all nodes on the left face of that layer
        selectNodesByCoordRange(nodeCoords, xMin=0.0, xMax=0.0, zMin=100.0, zMax=104.0)
    """

    def _check(condition, selected, nodeCoords, tol):
        return selectNodes(condition, nodeCoords, tol=tol)

    # build the condition from whichever bounds were supplied
    def condition(x, y, z):
        if xMin is not None and x < FuzzyFloat(xMin, tol):
            return False
        if xMax is not None and x > FuzzyFloat(xMax, tol):
            return False
        if yMin is not None and y < FuzzyFloat(yMin, tol):
            return False
        if yMax is not None and y > FuzzyFloat(yMax, tol):
            return False
        if zMin is not None and z < FuzzyFloat(zMin, tol):
            return False
        if zMax is not None and z > FuzzyFloat(zMax, tol):
            return False
        return True

    return selectNodes(condition, nodeCoords, tol=tol)


# ──────────────────────────────────────────────────────────────────────────────
# (B)  selectBoundaryNodes
# ──────────────────────────────────────────────────────────────────────────────

def selectBoundaryNodes(nodeCoords, axis, face, tol=defaultTol, sortAxes=None):
    """
    select all nodes on a model boundary face identified by axis and position.

    no physical groups or surface IDs needed — works purely from coordinates.

    :param nodeCoords: (dict) mapping nodeTag --> (x, y, z)
    :param axis:       (str)  "x", "y", or "z" — the face normal axis
    :param face:       (str | float)
                           "min"  --> face at the minimum coordinate on that axis
                           "max"  --> face at the maximum coordinate on that axis
                           float  --> face at that exact coordinate value
    :param tol:        (float) geometric tolerance (default: meshHelper.defaultTol)
    :param sortAxes:   (tuple | None)
                           if given, sort the result by these axes in order
                           e.g. sortAxes=("x", "y") or sortAxes=("z",)
                           if None, return in arbitrary order (fastest)

    :return: (list) node IDs on the requested face

    examples:
        # base nodes (lowest z) → replaces the 27-surface manual list
        baseNodes = selectBoundaryNodes(nodeCoords, axis="z", face="min")

        # top nodes (highest z)
        topNodes  = selectBoundaryNodes(nodeCoords, axis="z", face="max")

        # left face (x = 0)
        leftNodes = selectBoundaryNodes(nodeCoords, axis="x", face="min")

        # a specific elevation plane
        nodes_z76 = selectBoundaryNodes(nodeCoords, axis="z", face=76.0)

        # sorted for equalDOF pairing
        baseNodes = selectBoundaryNodes(nodeCoords, "z", "min", sortAxes=("x", "y"))
    """

    axisIdx = {"x": 0, "y": 1, "z": 2}
    if axis not in axisIdx:
        raise ValueError(f"axis must be 'x', 'y', or 'z'; got '{axis}'")

    idx = axisIdx[axis]
    allCoords = [c[idx] for c in nodeCoords.values()]

    # resolve face value
    if face == "min":
        faceValue = min(allCoords)
    elif face == "max":
        faceValue = max(allCoords)
    elif isinstance(face, (int, float)):
        faceValue = float(face)
    else:
        raise ValueError(f"face must be 'min', 'max', or a float; got '{face}'")

    result = selectNodes(
        lambda x, y, z: [x, y, z][idx] == FuzzyFloat(faceValue, tol),
        nodeCoords,
        tol=tol
    )

    # optional sorting
    if sortAxes:
        for ax in reversed(sortAxes):   # sort by last axis first (stable sort)
            if ax == "x":
                result = sortNodesByX(result, nodeCoords)
            elif ax == "y":
                result = sortNodesByY(result, nodeCoords)
            elif ax == "z":
                result = sortNodesByZ(result, nodeCoords)

    return result


# ──────────────────────────────────────────────────────────────────────────────
# (C)  previewBoundaries
# ──────────────────────────────────────────────────────────────────────────────

def previewBoundaries(nodeCoords, tol=defaultTol):
    """
    print a diagnostic table of all 6 model boundary faces and their node counts.

    call this once on any new mesh to understand its geometry instantly — no
    manual coordinate inspection needed.

    :param nodeCoords: (dict) mapping nodeTag --> (x, y, z)
    :param tol:        (float) geometric tolerance

    :return: (dict) {face_label: list_of_node_ids}  (also printed to stdout)
    """

    allCoords = list(nodeCoords.values())
    xs = [c[0] for c in allCoords]
    ys = [c[1] for c in allCoords]
    zs = [c[2] for c in allCoords]

    faces = [
        ("x_min",       "x", min(xs), ""),
        ("x_max",       "x", max(xs), ""),
        ("y_min",       "y", min(ys), ""),
        ("y_max",       "y", max(ys), ""),
        ("z_min (BASE)", "z", min(zs), "  <-- base"),
        ("z_max (TOP)",  "z", max(zs), "  <-- top"),
    ]

    results = {}
    rows = []

    for label, axis, coord, note in faces:
        nodes = selectBoundaryNodes(nodeCoords, axis=axis, face=coord, tol=tol)
        results[label] = nodes
        rows.append((label, axis, coord, len(nodes), note))

    # print table
    print("\n")
    print("=" * 65)
    print(f"  boundary face preview  ({len(nodeCoords)} nodes total)")
    print("=" * 65)
    print(f"  {'face':<20} {'axis':^6} {'coord':>10}    {'nodes':>8}")
    print("-" * 65)

    for label, axis, coord, nNodes, note in rows:
        print(f"  {label:<20} {axis:^6} {coord:>10.4f}    {nNodes:>8}{note}")

    print("=" * 65 + "\n")

    return results


def getAndSortGroupNodes(meshFile, phyGroupID, nodeCoords, axes=("x", "y", "z"), dim=None):
    """
    extract nodes belonging to a physical group and sort them
    according to a user-specified sequence of axes.

    :param meshFile: (str) path to the .msh file
    :param phyGroupID: (int) physical group ID to extract nodes from
    :param nodeCoords: (dict) mapping nodeTag --> (x, y, z)
    :param axes: (tuple) sequence of axes to sort by, each in {"x", "y", "z"}
                 example: ("x", "z"), ("y",), ("x", "y", "z")
    :param dim: (int or None) if provided, restrict nodes to entities of this dimension
                if None, auto-detect from the .msh file

    :return: (list) the sorted node IDs
    """

    # step 1: extract raw group nodes
    rawNodes = getBoundaryNodesFromMsh(meshFile, phyGroupIDs=[phyGroupID], dim=dim)

    # step 2: sort according to user-defined axis sequence
    sortedNodes = rawNodes

    for ax in axes:
        if ax == "x":
            sortedNodes = sortNodesByX(sortedNodes, nodeCoords)
        elif ax == "y":
            sortedNodes = sortNodesByY(sortedNodes, nodeCoords)
        elif ax == "z":
            sortedNodes = sortNodesByZ(sortedNodes, nodeCoords)

    return sortedNodes


def groupNodesByCoordinate(nodeSet, nodeCoords, axis="y", tol=1e-6):
    """
    group node tags by a rounded coordinate key.

    :param nodeSet: (iterable) collection of node IDs to group
    :param nodeCoords: (dict) mapping nodeTag --> (x, y, z)
    :param axis: (str) one of "x", "y", "z" - determines which coordinate is used
    :param tol: (float) rounding tolerance

    :return: (dict) mapping coordinateKey --> list of nodeTags
    """

    # axis index
    idx = {"x": 0, "y": 1, "z": 2}[axis]

    groups = {}

    for n in nodeSet:
        coord = nodeCoords[n][idx]
        key = round(coord / tol) * tol
        groups.setdefault(key, []).append(n)

    return groups


def getElementsByGroup(elements, phyGroupIDs):
    """
    Return elements belonging to the specified physical group(s).

    :param elements:     (list) list of element dicts (e.g. elmtsRemapped)
    :param phyGroupIDs:  (int or set/list of ints) physical group ID(s) to select
    :return:             (list) matching element dicts
    """
    if isinstance(phyGroupIDs, int):
        phyGroupIDs = {phyGroupIDs}
    else:
        phyGroupIDs = set(phyGroupIDs)
    return [el for el in elements if el["group"] in phyGroupIDs]


def getElementsTagByGroup(elements, phyGroupIDs):
    """
    Return element IDs belonging to the specified physical group(s).

    :param elements:     (list) list of element dicts (e.g. elmtsRemapped)
    :param phyGroupIDs:  (int or set/list of ints) physical group ID(s) to select
    :return:             (list) element IDs (tags)
    """
    return [el["id"] for el in getElementsByGroup(elements, phyGroupIDs)]


def countINTBraces(text):
    """
    count the number of comma-separated items inside curly braces in a string.

    :param text: (str) input string containing {...}

    :return: (int) number of items inside braces

    example:
        countINTBraces("Transfinite Curves {1, 3, 4, 5};") --> 4
    """

    # find the boundaries
    start = text.find('{')
    end = text.find('}', start)

    if start == -1 or end == -1:
        return 0

    # extract the content inside the braces
    inside = text[start + 1:end]

    # split by commas and clean each piece
    items = [x.strip() for x in inside.split(',') if x.strip()]

    return len(items)


def computeSoilBoundingBox(soilNodeSet, nodeCoords):
    """
    compute the axis-aligned bounding box of a set of soil nodes.

    :param soilNodeSet: (set or list) collection of soil node IDs
    :param nodeCoords: (dict) mapping nodeTag --> (x, y, z)

    :return: (dict) bounding box with keys: xMin, xMax, yMin, yMax, zMin, zMax
    """

    xs = [nodeCoords[n][0] for n in soilNodeSet]
    ys = [nodeCoords[n][1] for n in soilNodeSet]
    zs = [nodeCoords[n][2] for n in soilNodeSet]

    return {
        "xMin": min(xs), "xMax": max(xs),
        "yMin": min(ys), "yMax": max(ys),
        "zMin": min(zs), "zMax": max(zs),
    }


def selectBuriedStructuralNodes(structuralNodeSet, soilBBox, nodeCoords, tol):
    """
    select structural nodes that lie within the soil bounding box (buried nodes).

    :param structuralNodeSet: (set or list) collection of structural node IDs
    :param soilBBox: (dict) bounding box from computeSoilBoundingBox
    :param nodeCoords: (dict) mapping nodeTag --> (x, y, z)
    :param tol: (float) tolerance for boundary check

    :return: (set) buried structural node IDs
    """

    buried = set()

    for n in structuralNodeSet:
        x, y, z = nodeCoords[n]

        if (soilBBox["xMin"] - tol <= x <= soilBBox["xMax"] + tol and
            soilBBox["yMin"] - tol <= y <= soilBBox["yMax"] + tol and
                soilBBox["zMin"] - tol <= z <= soilBBox["zMax"] + tol):
            buried.add(n)

    return buried


def classifySoilAndStructureNodes(elements, soilTypes, structuralGroups):
    """
    extract the soil node set and the structural node set.

    :param elements: (list) parsed and filtered mesh elements
    :param soilTypes: (set) element types that we consider 'soil'
    :param structuralGroups: (dict) structural group categories
                             e.g., {"elBeam2D": {1}, "elBeam3D": {2, 3}, "wall": {4}}

    :return: (tuple) (soilNodeSet, structNodeSet)
        - soilNodeSet: (set) all nodes belonging to soil elements
        - structNodeSet: (set) all nodes belonging to structural elements
    """

    # combine all structural groups into a single set
    allStructuralGroups = set()
    for groupSet in structuralGroups.values():
        allStructuralGroups |= groupSet

    # nodes from soil elements
    soilNodeSet = {
        n for el in elements
        if el["type"] in soilTypes
        for n in el["nodes"]
    }

    # nodes from structural elements (any element whose group is in structuralGroups)
    structNodeSet = {
        n for el in elements
        if el["group"] in allStructuralGroups
        for n in el["nodes"]
    }

    return soilNodeSet, structNodeSet


def soilNodesNearStructure(structNode, elements, soilTypes, nodeCoords,
                           method="radius", radius=None, verticalAxis="z", tol=1e-6):
    """
    for a given structural node, find nearby soil nodes using different search strategies.

    :param structNode: (int) structural node ID
    :param elements: (list) all mesh elements
    :param soilTypes: (set) soil element types to consider
    :param nodeCoords: (dict) mapping nodeTag --> (x, y, z)
    :param method: (str) search method:
                   - "radius": all soil nodes within specified radius
                   - "horizontal_slice": soil nodes at same depth (good for vertical piles)
                   - "nearest": find N nearest soil nodes (default N=8)
    :param radius: (float) search radius for "radius" method, or vertical tolerance for "horizontal_slice"
    :param verticalAxis: (str) "x", "y", or "z" - which axis is vertical (for horizontal_slice)
    :param tol: (float) tolerance for coordinate matching

    :return: (list) sorted list of nearby soil node IDs
    """

    # get structural node coordinates
    P = nodeCoords[structNode]

    # collect all soil nodes
    soilNodes = {
        n for el in elements
        if el["type"] in soilTypes
        for n in el["nodes"]
    }

    if method == "radius":
        # find all soil nodes within specified radius
        if radius is None:
            raise ValueError("radius must be specified for method='radius'")

        nearby = []
        for n in soilNodes:
            coords = nodeCoords[n]
            dist = np.sqrt(sum((P[i] - coords[i]) ** 2 for i in range(3)))
            if dist <= radius:
                nearby.append(n)

        return sorted(nearby)

    elif method == "horizontal_slice":
        # original pile-style search: find soil nodes at same depth
        axisIndex = {"x": 0, "y": 1, "z": 2}
        v = axisIndex[verticalAxis]
        h1, h2 = [i for i in (0, 1, 2) if i != v]

        pv = P[v]    # vertical coordinate
        ph1 = P[h1]  # horizontal coord 1
        ph2 = P[h2]  # horizontal coord 2

        sliceTol = radius if radius is not None else tol

        faceNodes = set()

        for el in elements:
            if el["type"] not in soilTypes:
                continue

            elNodes = el["nodes"]

            # vertical coordinates of this element
            vs = [nodeCoords[n][v] for n in elNodes]
            vMin, vMax = min(vs), max(vs)

            # quick reject: structural node depth not within element's vertical span
            if pv < vMin - tol or pv > vMax + tol:
                continue

            # nodes on the horizontal face at v ≈ pv
            face = [
                n for n in elNodes
                if abs(nodeCoords[n][v] - pv) <= sliceTol
            ]

            if len(face) < 3:
                continue

            # horizontal coordinates for this face
            h1s = [nodeCoords[n][h1] for n in face]
            h2s = [nodeCoords[n][h2] for n in face]

            h1Min, h1Max = min(h1s), max(h1s)
            h2Min, h2Max = min(h2s), max(h2s)

            # check if structural node horizontal position lies inside this face
            if (ph1 < h1Min - tol or ph1 > h1Max + tol or
                    ph2 < h2Min - tol or ph2 > h2Max + tol):
                continue

            faceNodes.update(face)

        return sorted(faceNodes)

    elif method == "nearest":
        # find N nearest soil nodes
        N = int(radius) if radius is not None else 8

        distances = []
        for n in soilNodes:
            coords = nodeCoords[n]
            dist = np.sqrt(sum((P[i] - coords[i]) ** 2 for i in range(3)))
            distances.append((dist, n))

        distances.sort(key=lambda x: x[0])

        return [n for _, n in distances[:N]]

    else:
        raise ValueError(f"unknown method: {method}. Use 'radius', 'horizontal_slice', or 'nearest'")


def buildSSIMap(structNodeSet, elements, soilTypes, nodeCoords,
                method="radius", radius=None, verticalAxis="z", tol=1e-6):
    """
    build a mapping: structural node --> nearby soil nodes.

    :param structNodeSet: (set) set of node IDs belonging to structural elements
    :param elements: (list) all mesh elements
    :param soilTypes: (set) soil element types to consider
    :param nodeCoords: (dict) mapping nodeTag --> (x, y, z)
    :param method: (str) search method ("radius", "horizontal_slice", or "nearest")
    :param radius: (float) search parameter (meaning depends on method)
    :param verticalAxis: (str) "x", "y", or "z" (for horizontal_slice method)
    :param tol: (float) tolerance for geometric checks

    :return: (dict) mapping: structural node ID --> list of nearby soil node IDs
    """

    ssiMap = {}

    for structNode in structNodeSet:
        nearbyNodes = soilNodesNearStructure(
            structNode,
            elements,
            soilTypes,
            nodeCoords,
            method=method,
            radius=radius,
            verticalAxis=verticalAxis,
            tol=tol
        )
        ssiMap[structNode] = nearbyNodes

    return ssiMap


def detectSoilGroups(elements, has3D, soil2DTypes=None, soil3DTypes=None):
    """
    determine which element types are considered 'soil' based on mesh dimensionality.
    and return both the active soilTypes set adn the physical groups that contains soil elements as well

    :param elements: (list) all mesh elements (can be None for type-only detection)
    :param has3D: (bool) whether the mesh contains 3D elements
    :param soil2DTypes: (set, optional) override 2D soil types
    :param soil3DTypes: (set, optional) override 3D soil types

    :return: (set) soil element types to use
             OR (tuple) (soilTypes, soilGroups) if elements provided
    """

    if has3D:
        soilTypes = set(soil3DTypes) if soil3DTypes is not None else {5, 17, 105, 1005, 1055}
    else:
        soilTypes = set(soil2DTypes) if soil2DTypes is not None else {3, 10, 103, 1003}

    # if no elements provided, just return the types
    if elements is None:
        return soilTypes

    # compute soil physical groups by scanning elements
    soilGroups = set()
    for el in elements:
        if el["type"] in soilTypes:
            soilGroups.add(el["group"])

    return soilTypes, soilGroups


def computeStructureNormal(structNode, structNodeSet, nodeCoords, method="radial", verticalAxis="z"):
    """
    compute outward normal vector for a structural node.

    :param structNode: (int) structural node ID
    :param structNodeSet: (set) all structural node IDs (for context)
    :param nodeCoords: (dict) mapping nodeTag --> (x, y, z)
    :param method: (str) normal computation method:
                   - "radial": radial direction from centroid (good for piles, circular structures)
                   - "vertical": vertical direction (good for footings)
                   - "auto": try to detect based on geometry
    :param verticalAxis: (str) "x", "y", or "z"

    :return: (numpy array) unit normal vector [nx, ny, nz]
    """

    axisIndex = {"x": 0, "y": 1, "z": 2}
    vIdx = axisIndex[verticalAxis]
    hIndices = [i for i in (0, 1, 2) if i != vIdx]

    P = np.array(nodeCoords[structNode])

    if method == "radial":
        # compute centroid of all structural nodes
        coords = np.array([nodeCoords[n] for n in structNodeSet])
        centroid = np.mean(coords, axis=0)

        # radial direction (in horizontal plane)
        radial = np.zeros(3)
        radial[hIndices[0]] = P[hIndices[0]] - centroid[hIndices[0]]
        radial[hIndices[1]] = P[hIndices[1]] - centroid[hIndices[1]]

        norm = np.linalg.norm(radial)
        if norm < 1e-12:
            # node is at centroid, return arbitrary horizontal direction
            radial[hIndices[0]] = 1.0
            return radial

        return radial / norm

    elif method == "vertical":
        # return vertical unit vector (pointing up)
        normal = np.zeros(3)
        normal[vIdx] = 1.0
        return normal

    elif method == "auto":
        # try to detect: if structure is thin in horizontal plane, use radial
        # otherwise use vertical
        coords = np.array([nodeCoords[n] for n in structNodeSet])

        hSpan1 = np.max(coords[:, hIndices[0]]) - np.min(coords[:, hIndices[0]])
        hSpan2 = np.max(coords[:, hIndices[1]]) - np.min(coords[:, hIndices[1]])
        vSpan = np.max(coords[:, vIdx]) - np.min(coords[:, vIdx])

        maxHSpan = max(hSpan1, hSpan2)

        if vSpan > 2 * maxHSpan:
            # tall and thin --> pile-like, use radial
            return computeStructureNormal(structNode, structNodeSet, nodeCoords,
                                          method="radial", verticalAxis=verticalAxis)
        else:
            # flat --> footing-like, use vertical
            return computeStructureNormal(structNode, structNodeSet, nodeCoords,
                                          method="vertical", verticalAxis=verticalAxis)

    else:
        raise ValueError(f"unknown method: {method}. Use 'radial', 'vertical', or 'auto'")


def writeEmbeddedElements(structNodes, nodeCoords, elements, soilTypes,
                          penaltyStiffness, searchRadius, outputFile,
                          ndm=3):
    """
    generate ASDEmbeddedNodeElement commands for structural nodes inside soil.

    3D: finds containing tetrahedron (4 retained nodes) from brick decomposition
    2D: finds containing triangle   (3 retained nodes) from quad decomposition

    ASDEmbeddedNodeElement supports both cases natively (see OpenSees docs).

    :param structNodes: (set or list) structural node IDs to embed
    :param nodeCoords: (dict) mapping nodeTag --> (x, y, z) or (x, y)
    :param elements: (list) all mesh elements
    :param soilTypes: (set) soil element types
    :param penaltyStiffness: (float) penalty parameter K
    :param searchRadius: (float) search radius for soil elements
    :param outputFile: (str) path to output TCL file
    :param ndm: (int) number of dimensions (2 or 3)

    :return: (int) number of elements created
    """

    eleTag = 9000000
    nCreated = 0
    nFailed = 0

    print(f"[INFO] processing {len(structNodes)} structural nodes for embedded elements (ndm={ndm})...")

    with open(outputFile, 'w') as f:
        f.write("# !!!!!!!!!!!===========================================================================!!!!!!!!!!!\n")

        if ndm == 3:
            f.write("# ASDEmbeddedNodeElement for Structural Nodes (3D)\n")
        else:
            f.write("# ASDEmbeddedNodeElement for Structural Nodes (2D)\n")

        f.write("# !!!!!!!!!!!=========================================================================!!!!!!!!!!!\n\n")

        if ndm == 3:
            # ---- 3D path: tetrahedron containment (original logic) ----
            f.write(f"set K_penalty {penaltyStiffness:.6e}\n\n")

            for structNode in sorted(structNodes):
                tetNodes = findTetrahedronForStructNode(
                    structNode, nodeCoords, elements, soilTypes, searchRadius
                )

                if tetNodes is None:
                    print(f"[WARNING] no tetrahedron found for structural node {structNode}")
                    nFailed += 1
                    continue

                f.write(f"# structural node {structNode} embedded in tetrahedron {tetNodes}\n")
                f.write(f"element ASDEmbeddedNodeElement {eleTag} {structNode}")

                for node in tetNodes:
                    f.write(f" {node}")

                f.write(" -K $K_penalty\n\n")

                eleTag += 1
                nCreated += 1

        else:
            # ---- 2D path: triangle containment ----
            # ASDEmbeddedNodeElement in 2D uses 3 retained nodes forming a triangle.
            # We decompose each 4-node soil quad into 2 triangles and find which
            # triangle contains the structural node (same logic as 3D with tetrahedra).
            f.write(f"set K_penalty {penaltyStiffness:.6e}\n\n")

            for structNode in sorted(structNodes):
                triNodes = findTriangleForStructNode(
                    structNode, nodeCoords, elements, soilTypes, searchRadius
                )

                if triNodes is None:
                    print(f"[WARNING] no triangle found for structural node {structNode}")
                    nFailed += 1
                    continue

                f.write(f"# structural node {structNode} embedded in triangle {triNodes}\n")
                f.write(f"element ASDEmbeddedNodeElement {eleTag} {structNode}")

                for node in triNodes:
                    f.write(f" {node}")

                f.write(" -K $K_penalty\n\n")

                eleTag += 1
                nCreated += 1

    print(f"[INFO] created {nCreated} ASDEmbeddedNodeElement(s)")
    if nFailed > 0:
        print(f"[WARNING] failed for {nFailed} structural nodes")

    return nCreated


def isPointInTetrahedron(point, tetNodes, nodeCoords):
    """
    check if a point is inside a tetrahedron using barycentric coordinates.

    :param point: (numpy array) point coordinates [x, y, z]
    :param tetNodes: (list) 4 node IDs forming the tetrahedron
    :param nodeCoords: (dict) mapping nodeTag --> (x, y, z)

    :return: (bool) True if point is inside tetrahedron, False otherwise
    """

    # get coordinates of the 4 tetrahedron vertices
    v0 = np.array(nodeCoords[tetNodes[0]])
    v1 = np.array(nodeCoords[tetNodes[1]])
    v2 = np.array(nodeCoords[tetNodes[2]])
    v3 = np.array(nodeCoords[tetNodes[3]])

    def signedVolume(a, b, c, d):
        """
        compute signed volume of tetrahedron abcd
        """
        mat = np.column_stack([b - a, c - a, d - a])
        return np.linalg.det(mat) / 6.0

    V = signedVolume(v0, v1, v2, v3)

    if abs(V) < 1e-12:
        return False  # degenerate tetrahedron

    V0 = signedVolume(point, v1, v2, v3)
    V1 = signedVolume(v0, point, v2, v3)
    V2 = signedVolume(v0, v1, point, v3)
    V3 = signedVolume(v0, v1, v2, point)

    # barycentric coordinates
    u0 = V0 / V
    u1 = V1 / V
    u2 = V2 / V
    u3 = V3 / V

    # check if all barycentric coordinates are >= -tolerance
    tol = -1e-6  # small negative tolerance for numerical errors

    return u0 >= tol and u1 >= tol and u2 >= tol and u3 >= tol


def decomposeBrickIntoTetrahedra(brickNodes):
    """
    decompose an 8-node brick into 5 tetrahedra.

    :param brickNodes: (list) 8 node IDs of the brick element, ordered as:

              7--------6
             /|       /|
            / |      / |
           4--------5  |
           |  3-----|--2
           | /      | /
           |/       |/
           0--------1

    :return: (list) 5 tetrahedra, each a list of 4 node IDs
    """

    n0, n1, n2, n3, n4, n5, n6, n7 = brickNodes

    tetrahedra = [
        [n0, n1, n2, n5],
        [n0, n2, n7, n5],
        [n0, n2, n3, n7],
        [n0, n5, n7, n4],
        [n2, n7, n5, n6]
    ]

    return tetrahedra


def findTetrahedronForStructNode(structNode, nodeCoords, elements, soilTypes, searchRadius=5.0):
    """
    find the tetrahedron (4 nodes) from nearby soil bricks that contains the structural node.

    for 8-node brick soil elements, we:
    1. find nearby brick elements
    2. decompose each brick into 5 tetrahedra
    3. test which tetrahedron contains the structural node
    4. return those 4 nodes for ASDEmbeddedNodeElement

    :param structNode: (int) structural node ID
    :param nodeCoords: (dict) mapping nodeTag --> (x, y, z)
    :param elements: (list) all mesh elements
    :param soilTypes: (set) soil element types (e.g., {5, 17, 105, 1005, 1055})
    :param searchRadius: (float) how far to search for soil elements (default 5.0)

    :return: (list or None) 4 node IDs forming the containing tetrahedron, or None if not found
    """

    # get structural node coordinates
    structCoord = np.array(nodeCoords[structNode])

    # find all soil brick elements
    soilBricks = [el for el in elements if el["type"] in soilTypes]

    for brick in soilBricks:
        brickNodes = brick["nodes"]

        if len(brickNodes) != 8:
            print(f"[WARNING] soil element {brick['id']} has {len(brickNodes)} nodes, expected 8. skipping.")
            continue

        # compute brick centroid to check distance
        brickCoords = [nodeCoords[n] for n in brickNodes]
        centroid = np.mean(brickCoords, axis=0)
        distance = np.linalg.norm(structCoord - centroid)

        # skip if brick is too far
        if distance > searchRadius:
            continue

        # decompose brick into 5 tetrahedra
        tetrahedra = decomposeBrickIntoTetrahedra(brickNodes)

        # check each tetrahedron
        for tetNodes in tetrahedra:
            if isPointInTetrahedron(structCoord, tetNodes, nodeCoords):
                return tetNodes

    # no containing tetrahedron found
    return None


def isPointInTriangle(point, triNodes, nodeCoords):
    """
    check if a 2D point is inside a triangle using barycentric coordinates.

    :param point: (numpy array) point coordinates [x, y]
    :param triNodes: (list) 3 node IDs forming the triangle
    :param nodeCoords: (dict) mapping nodeTag --> (x, y) or (x, y, z)

    :return: (bool) True if point is inside triangle, False otherwise
    """

    v0 = np.array(nodeCoords[triNodes[0]][:2])
    v1 = np.array(nodeCoords[triNodes[1]][:2])
    v2 = np.array(nodeCoords[triNodes[2]][:2])
    p = np.array(point[:2])

    # vectors from v0
    d0 = v1 - v0
    d1 = v2 - v0
    d2 = p - v0

    # 2D cross product (scalar)
    detT = d0[0] * d1[1] - d0[1] * d1[0]

    if abs(detT) < 1e-12:
        return False  # degenerate triangle

    # barycentric coordinates
    lam1 = (d2[0] * d1[1] - d2[1] * d1[0]) / detT
    lam2 = (d0[0] * d2[1] - d0[1] * d2[0]) / detT
    lam0 = 1.0 - lam1 - lam2

    tol = -1e-6
    return lam0 >= tol and lam1 >= tol and lam2 >= tol


def decomposeQuadIntoTriangles(quadNodes):
    """
    decompose a 4-node quadrilateral into 2 triangles.

    :param quadNodes: (list) 4 node IDs of the quad element, ordered as:

           3--------2
           |        |
           |        |
           0--------1

    :return: (list) 2 triangles, each a list of 3 node IDs
    """

    n0, n1, n2, n3 = quadNodes

    triangles = [
        [n0, n1, n2],
        [n0, n2, n3]
    ]

    return triangles


def findTriangleForStructNode(structNode, nodeCoords, elements, soilTypes, searchRadius=5.0):
    """
    find the triangle (3 nodes) from nearby soil quads that contains the structural node.

    2D analog of findTetrahedronForStructNode:
    1. find nearby quad soil elements
    2. decompose each quad into 2 triangles
    3. test which triangle contains the structural node
    4. return those 3 nodes for ASDEmbeddedNodeElement (2D mode)

    :param structNode: (int) structural node ID
    :param nodeCoords: (dict) mapping nodeTag --> (x, y) or (x, y, z)
    :param elements: (list) all mesh elements
    :param soilTypes: (set) soil element types (e.g., {3, 103, 1003})
    :param searchRadius: (float) how far to search for soil elements (default 5.0)

    :return: (list or None) 3 node IDs forming the containing triangle, or None if not found
    """

    structCoord = np.array(nodeCoords[structNode][:2])

    soilQuads = [el for el in elements if el["type"] in soilTypes]

    for quad in soilQuads:
        quadNodes = quad["nodes"]

        if len(quadNodes) != 4:
            # skip non-quad elements (e.g. 9-node quads would need different decomposition)
            continue

        # compute quad centroid to check distance
        quadCoords = np.array([nodeCoords[n][:2] for n in quadNodes])
        centroid = np.mean(quadCoords, axis=0)
        distance = np.linalg.norm(structCoord - centroid)

        if distance > searchRadius:
            continue

        # decompose quad into 2 triangles
        triangles = decomposeQuadIntoTriangles(quadNodes)

        for triNodes in triangles:
            if isPointInTriangle(structCoord, triNodes, nodeCoords):
                return triNodes

    return None


def computeElementCentroid(elemNodes, nodeCoords):
    """
    compute the centroid (center point) of an element.

    :param elemNodes: (list) node IDs of the element
    :param nodeCoords: (dict) mapping nodeTag --> (x, y, z)

    :return: (tuple) (cx, cy, cz) centroid coordinates
    """

    coords = [nodeCoords[n] for n in elemNodes if n in nodeCoords]

    if not coords:
        return 0.0, 0.0, 0.0

    cx = sum(c[0] for c in coords) / len(coords)
    cy = sum(c[1] for c in coords) / len(coords)
    cz = sum(c[2] for c in coords) / len(coords) if len(coords[0]) > 2 else 0.0

    return cx, cy, cz


def computeInitialEffectiveStress(depth, gammaSat, gammaWater=10.0, waterTableDepth=0.0, gammaUnsat=None):
    """
    compute initial effective vertical stress at a given depth.

    sigma'v0 = gamma' x depth (below water table)
    where gamma' = gammaSat - gammaWater (submerged unit weight)

    :param depth: (float) depth below ground surface (positive value, in meters)
    :param gammaSat: (float) saturated unit weight of soil (kN/m^3)
    :param gammaWater: (float) unit weight of water (kN/m^3), default 10.0
    :param waterTableDepth: (float) depth of water table below surface (m), default 0.0
    :param gammaUnsat: (float, optional) unsaturated unit weight above water table

    :return: (float) initial effective vertical stress σ'v0 in kPa

    example:
        sigma = computeInitialEffectiveStress(depth=5.0, gammaSat=19.87)
        # returns 49.35 kPa
    """

    if depth <= 0:
        return 1.0  # minimum to avoid division by zero

    gammaSub = gammaSat - gammaWater  # submerged unit weight

    # default: if you don't know unsat unit weight, fall back to gammaSat
    if gammaUnsat is None:
        gammaUnsat = gammaSat

    if depth <= waterTableDepth:
        # above water table: use total unit weight
        sigmaV0 = gammaUnsat * depth
    else:
        sigmaV0 = gammaUnsat * waterTableDepth + gammaSub * (depth - waterTableDepth)

    return max(sigmaV0, 1.0)  # minimum 1 kPa to avoid division issues


def generateVariablePermeabilityFiles(
        elements,
        nodeCoords,
        mainSoilTags,
        verticalAxis,
        outputDir,
        gammaSatDict,
        kInitDict,
        gammaWater=10.0,
        waterTableDepth=0.0,
        surfaceElevation=0.0,
        alpha=20.0,
        beta1=1.0,
        beta2=8.9,
):
    """
    generate variable permeability TCL data file for SSPbrickUP elements.

    based on Shahir & Pak (2009) / Rahmani & Pak (2012):
        k/k_init = 1 + (alpha - 1) * ru^beta
        where ru = Δu / sigma'v0 (excess pore pressure ratio)

    :param elements: (list) element list from parseELMTsFromGMSH()
    :param nodeCoords: (dict) node coordinates {nodeId: (x, y, z)}
    :param mainSoilTags: (dict) mapping physical group --> material tag
    :param verticalAxis: (str) 'x', 'y', or 'z'
    :param outputDir: (str) output directory for TCL files
    :param gammaSatDict: (dict) saturated unit weight per material {matTag: gamma_sat in kN/m³}
    :param kInitDict: (dict) initial permeability per material {matTag: k_init}
    :param gammaWater: (float) unit weight of water (kN/m³), default 10.0
    :param waterTableDepth: (float) depth of water table below surface (m), default 0.0
    :param surfaceElevation: (float) elevation of ground surface (m), default 0.0
    :param alpha: (float) maximum permeability ratio at full liquefaction, default 20.0
    :param beta1: (float) exponent during pore pressure buildup, default 1.0
    :param beta2: (float) exponent during consolidation, default 8.9

    :return: (str or None) path to generated varPermFile, or None if no SSPbrickUP elements found
    """

    print("\n" + "!=!" * 70)
    print("variable permeability data")
    print("based on Shahir & Pak (2009) / Rahmani & Pak (2012)")
    print("!=!" * 70)

    # find SSPbrickUP elements (type 1005)
    sspElements = [el for el in elements if el["type"] == 1005]
    print(f"\n[INFO] found {len(sspElements)} SSPbrickUP elements")

    if not sspElements:
        print("[WARNING] no SSPbrickUP elements found. skipping variable permeability generation.")
        return None

    # determine axis index
    axisIdx = {"x": 0, "y": 1, "z": 2}[verticalAxis.lower()]

    # print info
    print(f"[INFO] surface elevation: {surfaceElevation:.2f} m")
    print(f"[INFO] vertical axis: {verticalAxis}")
    print(f"[INFO] water table depth: {waterTableDepth} m")

    for matTag, gammaSat in gammaSatDict.items():
        gammaSub = gammaSat - gammaWater
        print(f"[INFO] material {matTag}: γ_sat={gammaSat} kN/m³, γ'={gammaSub:.2f} kN/m³")

    # generate variablePermeabilityData.tcl
    varPermFile = os.path.join(outputDir, "variablePermeabilityData.tcl")

    with open(varPermFile, "w") as f:
        # header
        f.write("# !!!!!!!!!=========!!!!!!!!!=========!!!!!!!!!=========!!!!!!!!!=========!!!!!!!!!=======!!!!!!!!!\n")
        f.write("# variable permeability data\n")
        f.write("# !!!!!!!!!=========!!!!!!!!!=========!!!!!!!!!=========!!!!!!!!!=========!!!!!!!!!=======!!!!!!!!!\n")
        f.write("# based on Shahir & Pak (2009) / Rahmani & Pak (2012)\n")
        f.write("#\n")
        f.write("# Formula: k/k_init = 1 + (alpha - 1) * ru^beta\n")
        f.write("#   where ru = Δu / σ'v0 (excess pore pressure ratio)\n")
        f.write("#\n")
        f.write(f"# Soil parameters:\n")

        for matTag, gammaSat in gammaSatDict.items():
            gammaSub = gammaSat - gammaWater
            f.write(f"#   material {matTag}: gamma_sat={gammaSat} kN/m³, gamma'={gammaSub:.2f} kN/m³\n")

        f.write(f"#   gamma_water = {gammaWater} kN/m³\n")
        f.write(f"#   surface elevation = {surfaceElevation:.2f} m\n")
        f.write(f"#   water table depth = {waterTableDepth} m\n")
        f.write("# !!!!!!!!!=========!!!!!!!!!=========!!!!!!!!!=========!!!!!!!!!=========!!!!!!!=======!!!!!!!!!\n\n")

        # Shahir & Pak parameters
        f.write("# parameters\n")
        f.write(f"set alpha  {alpha}     ;# maximum permeability ratio at full liquefaction\n")
        f.write(f"set beta1   {beta1}    ;# exponent during pore pressure buildup\n")
        f.write(f"set beta2   {beta2}    ;# exponent during consolidation\n\n")

        # element range
        elemIds = sorted([el["id"] for el in sspElements])
        f.write("# SSPbrickUP element range\n")
        f.write(f"set firstSSPelem {min(elemIds)}\n")
        f.write(f"set lastSSPelem {max(elemIds)}\n")
        f.write(f"set numSSPelems {len(elemIds)}\n\n")

        # element data header
        f.write("# !!!!!!!!!=========!!!!!!!!!=========!!!!!!!!!=========!!!!!!!!!=========!!!!!!!!!=======!!!!!!!!!\n")
        f.write("# element data\n")
        f.write("# !!!!!!!!!=========!!!!!!!!!=========!!!!!!!!!=========!!!!!!!!!=========!!!!!!!!!=======!!!!!!!\n\n")

        # process each element
        for el in sspElements:
            elemId = el["id"]
            nodes = el["nodes"]

            # get material tag
            matTag = mainSoilTags.get(el["group"], 1)

            # get material properties (with fallback to first available)
            if matTag in kInitDict:
                kInit = kInitDict[matTag]
            else:
                kInit = list(kInitDict.values())[0]
                print(f"[WARNING] no kInit for material {matTag}, using default")

            if matTag in gammaSatDict:
                gammaSat = gammaSatDict[matTag]
            else:
                gammaSat = list(gammaSatDict.values())[0]
                print(f"[WARNING] no gammaSat for material {matTag}, using default")

            # compute element centroid
            centroid = computeElementCentroid(nodes, nodeCoords)

            # compute depth
            elemVertCoord = centroid[axisIdx]
            depth = surfaceElevation - elemVertCoord

            # compute initial effective stress
            sigmaV0 = computeInitialEffectiveStress(depth, gammaSat, gammaWater, waterTableDepth)

            # write element data
            nodeStr = " ".join(str(n) for n in nodes)
            f.write(f"# Element {elemId}: depth={depth:.2f}m, sigma_v0={sigmaV0:.2f}kPa, mat={matTag}\n")
            f.write(f"set elemNodes({elemId}) {{{nodeStr}}}\n")
            f.write(f"set elemKinit({elemId}) {kInit:.15e}\n")
            f.write(f"set sigmaV0({elemId}) {sigmaV0:.6f}\n")
            f.write(f"set ruPrev({elemId}) 0.0\n\n")

        # write procedures
        f.write("# !!!!!!!!!=========!!!!!!!!!=========!!!!!!!!!=========!!!!!!!!!=========!!!!!!!!!=======!!!!!!!!!\n")
        f.write("# PROCEDURES\n")
        f.write("# !!!!!!!!!=========!!!!!!!!!=========!!!!!!!!!=========!!!!!!!!!=========!!!!!!!!!=======!!!!!!!\n\n")

        f.write("""proc getElementPWP {elemTag} {
    global elemNodes
    if {![info exists elemNodes($elemTag)]} { return 0.0 }
    set nodeList $elemNodes($elemTag)
    set sumPWP 0.0
    set count 0
    foreach nd $nodeList {
        if {[catch {set pwp [nodeVel $nd 4]} err]} { continue }
        set sumPWP [expr $sumPWP + $pwp]
        incr count
    }
    if {$count > 0} { return [expr $sumPWP / $count] }
    return 0.0
}

proc updateElementPermeability {elemTag} {
    global alpha beta1 beta2 sigmaV0 ruPrev elemKinit
    if {![info exists sigmaV0($elemTag)]} { return [list 0.0 1.0 0.0] }

    # STEP 1: Get pore pressure
    set pwp [getElementPWP $elemTag]

    # STEP 2: Calculate ru
    if {$sigmaV0($elemTag) > 0.0} {
        set ru [expr abs($pwp) / $sigmaV0($elemTag)]
    } else {
        set ru 0.0
    }
    if {$ru < 0.0} {set ru 0.0}
    if {$ru > 1.0} {set ru 1.0}

    # STEP 3: Calculate new permeability
    if {$ru >= $ruPrev($elemTag)} {
        set beta $beta1
    } else {
        set beta $beta2
    }
    if {$ru < 0.001} {
        set kRatio 1.0
    } else {
        set kRatio [expr 1.0 + ($alpha - 1.0) * pow($ru, $beta)]
    }
    set kNew [expr $elemKinit($elemTag) * $kRatio]

    # STEP 4: Update element
    setParameter -value $kNew -ele $elemTag xPerm
    setParameter -value $kNew -ele $elemTag yPerm
    setParameter -value $kNew -ele $elemTag zPerm
    set ruPrev($elemTag) $ru

    return [list $ru $kRatio $kNew]
}

proc updateAllPermeabilities {} {
    global firstSSPelem lastSSPelem
    for {set e $firstSSPelem} {$e <= $lastSSPelem} {incr e} {
        updateElementPermeability $e
    }
}

puts "\\[INFO\\] Variable permeability data loaded: $numSSPelems SSPbrickUP elements"
puts "\\[INFO\\] Parameters: alpha=$alpha, beta1=$beta1, beta2=$beta2"
""")

    print(f"[INFO] generated: {varPermFile}")
    print("=" * 70 + "\n")

    return varPermFile


def writeContactElements(structNodes, nodeCoords, elements, soilTypes,
                         Kn, Kt, mu, verticalAxis, outputFile,
                         ndm=3, ssiMap=None):
    """
    generate TCL file with ZeroLengthContactASDimplex commands.

    creates interface elements with friction, gap opening, and slip behavior.
    each structural node gets a contact element with the nearest soil node.

    ZeroLengthContactASDimplex works in both 2D and 3D. In 2D, all 3 orient
    components must still be provided, with the 3rd component set to 0.0.

    uses ssiMap (from buildSSIMap) to find the nearest soil node for each
    structural node, instead of doing its own search internally.

    :param structNodes: (set or list) structural node IDs
    :param nodeCoords: (dict) node coordinates
    :param elements: (list) element list
    :param soilTypes: (set) soil element types
    :param Kn: (float) normal stiffness
    :param Kt: (float) tangential stiffness
    :param mu: (float) friction coefficient
    :param verticalAxis: (str) 'x', 'y', or 'z'
    :param outputFile: (str) path to output TCL file
    :param ndm: (int) number of dimensions (2 or 3)
    :param ssiMap: (dict or None) precomputed mapping from buildSSIMap.
                   if None, falls back to brute-force nearest search (original behavior).

    :return: (int) number of elements created
    """

    eleTag = 8000000
    nCreated = 0

    # fallback: if no ssiMap, build a quick all-soil-nodes array for brute force
    allSoilNodes = []
    soilCoords = np.empty((0, 3))

    if ssiMap is None:
        print("[INFO] no ssiMap provided, falling back to brute-force nearest search")
        allSoilNodes = sorted({
            n for el in elements if el["type"] in soilTypes
            for n in el["nodes"]
        })
        nCoords = len(nodeCoords[next(iter(nodeCoords))])
        soilCoords = np.array([nodeCoords[n][:nCoords] for n in allSoilNodes])

    with open(outputFile, "w") as f:
        f.write("# !!!!!!!!!=========!!!!!!!!!=========!!!!!!!!!=========!!!!!!!!!=========!!!!!!!!!=======!!!!!!!!!\n")

        if ndm == 3:
            f.write("# ZeroLengthContactASDimplex for Structure-Soil Interface (3D)\n")
        else:
            f.write("# ZeroLengthContactASDimplex for Structure-Soil Interface (2D)\n")

        f.write("# !!!!!!!!!=========!!!!!!!!!=========!!!!!!!!!=========!!!!!!!!!=========!!!!!!!!!=======!!!!!!!\n\n")

        f.write(f"set Kn {Kn:.6e}  ;# Normal stiffness\n")
        f.write(f"set Kt {Kt:.6e}  ;# Tangential stiffness\n")
        f.write(f"set mu {mu:.6f}      ;# Friction coefficient\n\n")

        for structNode in sorted(structNodes):

            # find the nearest soil node
            if ssiMap is not None:
                nearbyNodes = ssiMap.get(structNode, [])
                if not nearbyNodes:
                    print(f"[WARNING] ssiMap has no soil nodes for struct node {structNode}, skipping")
                    continue

                # pick the closest from the ssiMap candidates
                dim = 3 if ndm == 3 else 2
                structCoord = np.array(nodeCoords[structNode][:dim])
                bestNode = None
                bestDist = float('inf')

                for sn in nearbyNodes:
                    d = np.linalg.norm(np.array(nodeCoords[sn][:dim]) - structCoord)
                    if d < bestDist:
                        bestDist = d
                        bestNode = sn

                nearestSoilNode = bestNode
            else:
                # brute-force fallback (original behavior)
                structCoord = np.array(nodeCoords[structNode][:soilCoords.shape[1]])
                distances = np.linalg.norm(soilCoords - structCoord, axis=1)
                nearestIdx = np.argmin(distances)
                nearestSoilNode = allSoilNodes[nearestIdx]

            # compute normal and write element
            # ZeroLengthContactASDimplex works for both 2D and 3D.
            # In 2D, all 3 orient components must be provided (3rd = 0.0).
            if ndm == 3:
                normal = computeStructureNormal(structNode, structNodes, nodeCoords,
                                                method="auto", verticalAxis=verticalAxis)
            else:
                normal2D = computeStructureNormal2D(structNode, structNodes, nodeCoords,
                                                    verticalAxis=verticalAxis)
                normal = np.array([normal2D[0], normal2D[1], 0.0])

            f.write(f"element zeroLengthContactASDimplex {eleTag} ")
            f.write(f"{structNode} {nearestSoilNode} ")
            f.write(f"$Kn $Kt $mu ")
            f.write(f"-orient {normal[0]:.6f} {normal[1]:.6f} {normal[2]:.6f}\n\n")

            eleTag += 1
            nCreated += 1

    print(f"[INFO] created {nCreated} contact elements in {outputFile}")

    return nCreated


def computeStructureNormal2D(structNode, structNodeSet, nodeCoords, verticalAxis="y"):
    """
    compute outward normal vector for a structural node in 2D.

    in 2D, the mesh lives in a plane (e.g., x-y). The "outward normal" is the
    horizontal direction pointing away from the structure centroid.

    :param structNode: (int) structural node ID
    :param structNodeSet: (set) all structural node IDs
    :param nodeCoords: (dict) mapping nodeTag --> (x, y) or (x, y, z)
    :param verticalAxis: (str) "x" or "y" — which axis is vertical in 2D

    :return: (numpy array) unit normal vector [nx, ny]
    """

    axisIndex = {"x": 0, "y": 1}
    vIdx = axisIndex[verticalAxis]
    hIdx = 1 - vIdx  # the horizontal axis

    P = np.array(nodeCoords[structNode][:2])  # take only first 2 coords

    # compute centroid of all structural nodes
    coords = np.array([nodeCoords[n][:2] for n in structNodeSet])
    centroid = np.mean(coords, axis=0)

    # horizontal direction away from centroid
    normal = np.zeros(2)
    normal[hIdx] = P[hIdx] - centroid[hIdx]

    norm = np.linalg.norm(normal)
    if norm < 1e-12:
        # node is at centroid horizontally, return arbitrary horizontal direction
        normal[hIdx] = 1.0
        return normal

    return normal / norm


def generateStructureInterface(structNodes, nodeCoords, elements, soilTypes,
                               E_soil, phi_soil, verticalAxis="z",
                               searchRadius=5.0, outputDir=".",
                               ndm=3, ssiMethod="radius", ssiRadius=None):
    """
    main function for generating structure-soil interface elements.

    NOW SUPPORTS BOTH 2D AND 3D meshes, and uses buildSSIMap as the
    centralized search engine for finding soil-structure node pairs.

    creates:
    - 3D: ASDEmbeddedNodeElement (tetrahedron)  + ZeroLengthContactASDimplex
    - 2D: ASDEmbeddedNodeElement (triangle)      + ZeroLengthContactASDimplex

    :param structNodes: (set or list) structural node IDs
    :param nodeCoords: (dict) node coordinates {nodeTag: (x, y, z) or (x, y)}
    :param elements: (list) element list
    :param soilTypes: (set) soil element types
    :param E_soil: (float) soil Young's modulus
    :param phi_soil: (float) soil friction angle (degrees)
    :param verticalAxis: (str) 'x', 'y', or 'z'
    :param searchRadius: (float) search radius for embedded element search (3D tetrahedra)
    :param outputDir: (str) output directory
    :param ndm: (int) number of dimensions: 2 or 3
    :param ssiMethod: (str) search method for buildSSIMap:
                      "radius", "horizontal_slice", or "nearest"
    :param ssiRadius: (float or None) radius/parameter for buildSSIMap.
                      - for "radius": the search radius in model units
                      - for "horizontal_slice": vertical tolerance
                      - for "nearest": number of nearest nodes (as int, e.g. 8)
                      if None, defaults to searchRadius for "radius"/"horizontal_slice",
                      or 8 for "nearest"

    :return: (tuple) (nEmbedded, nContact) number of elements created
    """

    print("\n" + "!=!" * 35)
    print("Generating structure-soil interface elements")
    print("!=!" * 35)

    # compute interface parameters
    K_penalty = E_soil * 1e1
    E_interface = 2000
    alpha = 5.0
    beta = 0.05
    Kn = alpha * E_interface
    Kt = beta * Kn
    mu = (2.0 / 3.0) * np.tan(np.radians(phi_soil))

    print(f"\nDimensionality: {'3D' if ndm == 3 else '2D'}")
    print(f"Structural nodes: {len(structNodes)}")
    print(f"Soil E: {E_soil / 1e6:.1f} MPa")
    print(f"Soil phi: {phi_soil:.1f} deg")
    print(f"Interface mu: {mu:.3f}")
    print(f"SSI search method: {ssiMethod}")
    print(f"Search radius: {searchRadius:.1f}")

    # ---------- build the SSI map (centralized search) ----------
    if ssiRadius is None:
        if ssiMethod == "nearest":
            ssiRadius = 8  # default: 8 nearest nodes
        else:
            ssiRadius = searchRadius

    print(f"\n[STEP 0] Building SSI map (method='{ssiMethod}', radius/N={ssiRadius})...")

    ssiMap = buildSSIMap(
        structNodeSet=set(structNodes),
        elements=elements,
        soilTypes=soilTypes,
        nodeCoords=nodeCoords,
        method=ssiMethod,
        radius=ssiRadius,
        verticalAxis=verticalAxis
    )

    # quick stats
    nMapped = sum(1 for v in ssiMap.values() if v)
    nEmpty = sum(1 for v in ssiMap.values() if not v)
    print(f"[INFO] SSI map: {nMapped} nodes mapped, {nEmpty} nodes with no nearby soil")

    # output files
    embeddedFile = os.path.join(outputDir, "embeddedStructureElements.tcl")
    contactFile = os.path.join(outputDir, "contactStructureElements.tcl")

    # step 1: embedded elements
    if ndm == 3:
        print("\n[STEP 1] Generating ASDEmbeddedNodeElement (3D)...")
    else:
        print("\n[STEP 1] Generating ASDEmbeddedNodeElement (2D, triangles)...")

    nEmbedded = writeEmbeddedElements(
        structNodes, nodeCoords, elements, soilTypes,
        K_penalty, searchRadius, embeddedFile,
        ndm=ndm
    )

    # step 2: contact elements
    if ndm == 3:
        print("\n[STEP 2] Generating ZeroLengthContactASDimplex (3D)...")
    else:
        print("\n[STEP 2] Generating ZeroLengthContactASDimplex (2D)...")

    nContact = writeContactElements(
        structNodes, nodeCoords, elements, soilTypes,
        Kn, Kt, mu, verticalAxis, contactFile,
        ndm=ndm, ssiMap=ssiMap
    )

    # summary
    print("\n" + "!=!" * 35)
    print("structure-soil interface generation complete")
    print("!=!" * 35)

    if ndm == 3:
        print(f"ASDEmbeddedNodeElement (3D):       {nEmbedded}")
        print(f"ZeroLengthContactASDimplex (3D):   {nContact}")
    else:
        print(f"ASDEmbeddedNodeElement (2D):       {nEmbedded}")
        print(f"ZeroLengthContactASDimplex (2D):   {nContact}")

    print(f"SSI method used:             {ssiMethod}")
    print(f"\nOutput files:")
    print(f"  - {embeddedFile}")
    print(f"  - {contactFile}")
    print("!=!" * 35 + "\n")

    return nEmbedded, nContact


def writeAdaptiveAnalysisProcedure(f):
    """
    write the adaptive time stepping TCL procedure to an open file handle.

    handles:
    - automatic time step reduction on convergence failure
    - time step recovery after consecutive successes
    - minimum time step threshold to avoid infinite reduction
    - progress reporting

    :param f: (file handle) open file to write to

    :return: None
    """

    f.write("""
# !!!!!!!!!!!!!!!!!!!!!!!========================================================================!!!!!!!!!!!!!!!!!!!!!!!
# ADAPTIVE TIME STEPPING PROCEDURE
# !!!!!!!!!!!!!!!!!!!!!!!========================================================================!!!!!!!!!!!!!!!!!!!!!!!
# Features:
#   - Reduces dT on convergence failure (halves each time)
#   - Increases dT after N consecutive successes (doubles, up to dT_max)
#   - Stops if dT falls below dT_min
#   - Reports progress every 100 steps
#
# Usage:
#   set ok [adaptiveAnalyze $totalTime $dT_initial $dT_min $dT_max $N_success]
#   - totalTime:    total duration to analyze (s)
#   - dT_initial:   starting time step (s)
#   - dT_min:       minimum allowed time step (default: dT_initial/64)
#   - dT_max:       maximum allowed time step (default: dT_initial)
#   - N_success:    consecutive successes before increasing dT (default: 10)
# !!!!!!!!!!!!!!!!!!!!!!!========================================================================!!!!!!!!!!!!!!!!!!!!!!!

proc adaptiveAnalyze {totalTime dT_initial {dT_min ""} {dT_max ""} {N_success 10}} {

    # set defaults if not provided
    if {$dT_min eq ""} {set dT_min [expr $dT_initial / 64.0]}
    if {$dT_max eq ""} {set dT_max $dT_initial}

    set dT $dT_initial
    set currentTime [getTime]
    set startTime $currentTime
    set targetTime [expr $currentTime + $totalTime]
    set successCount 0
    set totalSteps 0
    set reductions 0
    set increases 0

    puts ""
    puts "!!!!!!!!!!!!!!!!!==============================================!!!!!!!!!!!!!!!!!"
    puts "ADAPTIVE TIME STEPPING"
    puts "!!!!!!!!!!!!!!!!!==============================================!!!!!!!!!!!!!!!!!"
    puts "Start time:     [format %.4f $currentTime] s"
    puts "Target time:    [format %.4f $targetTime] s"
    puts "Duration:       $totalTime s"
    puts "Initial dT:     [format %.2e $dT_initial] s"
    puts "Min dT:         [format %.2e $dT_min] s"
    puts "Max dT:         [format %.2e $dT_max] s"
    puts "Success threshold: $N_success steps"
    puts "!!!!!!!!!!!!!!!!!==============================================!!!!!!!!!!!!!!!!!"
    puts ""

    set analysisStartT [clock seconds]

    while {$currentTime < [expr $targetTime - 1.0e-12]} {

        # don't overshoot the target time
        if {[expr $currentTime + $dT] > $targetTime} {
            set dT [expr $targetTime - $currentTime]
        }

        # try one step
        set ok [analyze 1 $dT]

        if {$ok == 0} {
            # SUCCESS
            set currentTime [getTime]
            incr successCount
            incr totalSteps

            # try to increase dT after N consecutive successes
            if {$successCount >= $N_success && $dT < [expr $dT_max - 1.0e-12]} {
                set dT_new [expr $dT * 2.0]
                if {$dT_new > $dT_max} {set dT_new $dT_max}
                if {$dT_new > [expr $dT + 1.0e-12]} {
                    set dT $dT_new
                    incr increases
                    puts "  t=[format %.4f $currentTime]s: increasing dT to [format %.2e $dT]"
                }
                set successCount 0
            }

            # progress report every 100 steps
            if {[expr $totalSteps % 100] == 0} {
                set elapsed [expr [clock seconds] - $analysisStartT]
                set pct [expr int(100.0 * ($currentTime - $startTime) / $totalTime)]
                puts "  Progress: $pct% | t=[format %.4f $currentTime]s | dT=[format %.2e $dT] | steps=$totalSteps | ${elapsed}s"
            }

        } else {
            # FAILURE - reduce time step
            set successCount 0
            set dT [expr $dT / 2.0]
            incr reductions

            puts "  t=[format %.4f $currentTime]s: no convergence, reducing dT to [format %.2e $dT]"

            # check if dT is too small
            if {$dT < $dT_min} {
                puts ""
                puts "ERROR: dT below minimum ([format %.2e $dT_min]). Analysis aborted."
                puts "  Total steps completed: $totalSteps"
                puts "  Time reached: [format %.4f $currentTime] s"
                puts ""
                return -1
            }
        }
    }

    set analysisEndT [clock seconds]
    set wallTime [expr $analysisEndT - $analysisStartT]

    # final report
    puts ""
    puts "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!==============================================!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    puts "ADAPTIVE ANALYSIS COMPLETE"
    puts "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!==============================================!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    puts "Final time:     [format %.4f $currentTime] s"
    puts "Total steps:    $totalSteps"
    puts "dT reductions:  $reductions"
    puts "dT increases:   $increases"
    puts "Final dT:       [format %.2e $dT] s"
    puts "Wall time:      $wallTime seconds"
    puts "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!==============================================!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    puts ""

    return 0
}

""")


def generateAdaptiveAnalysisTcl(
        outputDir,
        totalTime,
        dT_initial,
        dT_min=None,
        dT_max=None,
        N_success=10,
        constraintsType="Transformation",
        testType="NormDispIncr",
        testTol=1.0e-3,
        testIter=30,
        algorithm="KrylovNewton",
        numberer="RCM",
        system="UmfPack",
        integratorGamma=0.5,
        integratorBeta=0.25,
        rayleighA0="$a0",
        rayleighA1="$a1",
        useVariablePerm=False,
        permUpdateInterval=50,
        filename="dynamicAnalysis_adaptive.tcl"
):
    """
    generate a TCL file for dynamic analysis with adaptive time stepping.

    :param outputDir: (str) output directory for the TCL file
    :param totalTime: (float) total analysis duration (seconds)
    :param dT_initial: (float) initial time step (seconds)
    :param dT_min: (float, optional) minimum allowed time step (default: dT_initial/64)
    :param dT_max: (float, optional) maximum allowed time step (default: dT_initial)
    :param N_success: (int) consecutive successes before increasing dT (default: 10)
    :param constraintsType: (str) constraints handler type (default: "Transformation")
    :param testType: (str) convergence test type (default: "NormDispIncr")
    :param testTol: (float) convergence tolerance (default: 1.0e-3)
    :param testIter: (int) maximum iterations (default: 30)
    :param algorithm: (str) solution algorithm (default: "KrylovNewton")
    :param numberer: (str) DOF numberer (default: "RCM")
    :param system: (str) system of equations (default: "UmfPack")
    :param integratorGamma: (float) Newmark gamma (default: 0.5)
    :param integratorBeta: (float) Newmark beta (default: 0.25)
    :param rayleighA0: (str) Rayleigh damping a0 (default: "$a0")
    :param rayleighA1: (str) Rayleigh damping a1 (default: "$a1")
    :param useVariablePerm: (bool) include variable permeability updates (default: False)
    :param permUpdateInterval: (int) steps between permeability updates (default: 50)
    :param filename: (str) output filename (default: "dynamicAnalysis_adaptive.tcl")

    :return: (str) path to generated file
    """

    if dT_min is None:
        dT_min = dT_initial / 64.0
    if dT_max is None:
        dT_max = dT_initial

    outFile = os.path.join(outputDir, filename)

    with open(outFile, "w") as f:
        # header
        f.write("# !!!!!!!!!!==============================================================================!!!!!!!!!\n")
        f.write("#                    DYNAMIC ANALYSIS WITH ADAPTIVE TIME STEPPING\n")
        f.write("# !!!!!!!!!!==============================================================================!!!!!!!!!\n")
        f.write("#\n")
        f.write("# Features:\n")
        f.write("#   - Automatic time step reduction on convergence failure\n")
        f.write("#   - Time step recovery after consecutive successes\n")
        f.write("#   - Progress reporting\n")

        if useVariablePerm:
            f.write("#   - Variable permeability updates (Shahir & Pak model)\n")

        f.write("#\n")
        f.write("# !!!!!!!!!!!=========================================================================!!!!!!!!!!!\n\n")

        # write the adaptive procedure
        writeAdaptiveAnalysisProcedure(f)

        # analysis parameters
        f.write("# !!!!!!!!!!=============================================================================!!!!!!!!!!\n")
        f.write("# ANALYSIS PARAMETERS\n")
        f.write("# !!!!!!!!!!=============================================================================!!!!!!!!\n\n")
        f.write(f"set totalTime    {totalTime}       ;# total analysis duration (s)\n")
        f.write(f"set dT_initial   {dT_initial}   ;# initial time step (s)\n")
        f.write(f"set dT_min       {dT_min:.2e}   ;# minimum time step (s)\n")
        f.write(f"set dT_max       {dT_max:.2e}   ;# maximum time step (s)\n")
        f.write(f"set N_success    {N_success}          ;# successes before increasing dT\n\n")

        # analysis setup
        f.write("# !!!!!!!!!!=============================================================================!!!!!!!!!!\n")
        f.write("# ANALYSIS SETUP\n")
        f.write("# !!!!!!!!!!=============================================================================!!!!!!!!\n\n")
        f.write(f"constraints {constraintsType}\n")
        f.write(f"test {testType} {testTol} {testIter} 1\n")
        f.write(f"algorithm {algorithm}\n")
        f.write(f"numberer {numberer}\n")
        f.write(f"system {system}\n")
        f.write(f"integrator Newmark {integratorGamma} {integratorBeta}\n")
        f.write(f"rayleigh {rayleighA0} 0.0 {rayleighA1} 0.0\n")
        f.write("analysis Transient\n\n")

        # variable permeability wrapper (if enabled)
        if useVariablePerm:
            f.write("# !!!!!!!!!!=========================================================================!!!!!!!!!!\n")
            f.write("# ADAPTIVE ANALYSIS WITH VARIABLE PERMEABILITY\n")
            f.write("# !!!!!!!!!!=========================================================================!!!!!!!!\n\n")
            f.write(f"set permUpdateInterval {permUpdateInterval}\n\n")
            f.write(_getVariablePermProcedure())
        else:
            # simple adaptive analysis without variable permeability
            f.write("# !!!!!!!!!!=========================================================================!!!!!!!!!!\n")
            f.write("# RUN ADAPTIVE ANALYSIS\n")
            f.write("# !!!!!!!!!!=========================================================================!!!!!!!!\n\n")
            f.write('puts "Starting adaptive analysis..."\n')
            f.write("set ok [adaptiveAnalyze $totalTime $dT_initial $dT_min $dT_max $N_success]\n\n")
            f.write("if {$ok != 0} {\n")
            f.write('    puts "Analysis failed to complete!"\n')
            f.write("} else {\n")
            f.write('    puts "Analysis completed successfully."\n')
            f.write("}\n")

    print(f"[INFO] generated: {outFile}")

    return outFile


def _getVariablePermProcedure():
    """
    returns the TCL code for adaptive analysis with variable permeability.

    :return: (str) TCL procedure code
    """

    return """# wrapper procedure that combines adaptive stepping with permeability updates
proc adaptiveAnalyzeWithPerm {totalTime dT_initial dT_min dT_max N_success permInterval} {
    global firstSSPelem lastSSPelem

    set dT $dT_initial
    set currentTime [getTime]
    set startTime $currentTime
    set targetTime [expr $currentTime + $totalTime]
    set successCount 0
    set totalSteps 0
    set reductions 0
    set increases 0
    set permUpdates 0
    set stepsSincePermUpdate 0

    puts ""
    puts "=============================================="
    puts "ADAPTIVE ANALYSIS + VARIABLE PERMEABILITY"
    puts "=============================================="
    puts "Start time:         [format %.4f $currentTime] s"
    puts "Target time:        [format %.4f $targetTime] s"
    puts "Initial dT:         [format %.2e $dT_initial] s"
    puts "Perm update every:  $permInterval steps"
    puts "=============================================="
    puts ""

    set analysisStartT [clock seconds]

    # output file for permeability evolution
    file mkdir results
    set permLog [open "results/permeability_evolution.csv" w]
    puts $permLog "Time,Steps,dT,Reductions,SampleRu"
    set sampleElem [expr ($firstSSPelem + $lastSSPelem) / 2]

    while {$currentTime < [expr $targetTime - 1.0e-12]} {

        # don't overshoot
        if {[expr $currentTime + $dT] > $targetTime} {
            set dT [expr $targetTime - $currentTime]
        }

        # try one step
        set ok [analyze 1 $dT]

        if {$ok == 0} {
            # SUCCESS
            set currentTime [getTime]
            incr successCount
            incr totalSteps
            incr stepsSincePermUpdate

            # update permeabilities periodically
            if {$stepsSincePermUpdate >= $permInterval} {
                updateAllPermeabilities
                incr permUpdates
                set stepsSincePermUpdate 0
            }

            # try to increase dT
            if {$successCount >= $N_success && $dT < [expr $dT_max - 1.0e-12]} {
                set dT_new [expr $dT * 2.0]
                if {$dT_new > $dT_max} {set dT_new $dT_max}
                if {$dT_new > [expr $dT + 1.0e-12]} {
                    set dT $dT_new
                    incr increases
                    puts "  t=[format %.4f $currentTime]s: increasing dT to [format %.2e $dT]"
                }
                set successCount 0
            }

            # progress report
            if {[expr $totalSteps % 100] == 0} {
                set elapsed [expr [clock seconds] - $analysisStartT]
                set pct [expr int(100.0 * ($currentTime - $startTime) / $totalTime)]

                # get sample ru value
                global ruPrev
                if {[info exists ruPrev($sampleElem)]} {
                    set sampleRu $ruPrev($sampleElem)
                    puts "  Progress: $pct% | t=[format %.4f $currentTime]s | dT=[format %.2e $dT] | ru=[format %.3f $sampleRu] | ${elapsed}s"
                    puts $permLog "[format %.4f $currentTime],$totalSteps,[format %.2e $dT],$reductions,[format %.4f $sampleRu]"
                } else {
                    puts "  Progress: $pct% | t=[format %.4f $currentTime]s | dT=[format %.2e $dT] | ${elapsed}s"
                    puts $permLog "[format %.4f $currentTime],$totalSteps,[format %.2e $dT],$reductions,0.0"
                }
                flush $permLog
            }

        } else {
            # FAILURE
            set successCount 0
            set dT [expr $dT / 2.0]
            incr reductions

            puts "  t=[format %.4f $currentTime]s: no convergence, reducing dT to [format %.2e $dT]"

            if {$dT < $dT_min} {
                puts ""
                puts "ERROR: dT below minimum. Analysis aborted."
                close $permLog
                return -1
            }
        }
    }

    close $permLog
    set wallTime [expr [clock seconds] - $analysisStartT]

    puts ""
    puts "=============================================="
    puts "ANALYSIS COMPLETE"
    puts "=============================================="
    puts "Final time:         [format %.4f $currentTime] s"
    puts "Total steps:        $totalSteps"
    puts "dT reductions:      $reductions"
    puts "dT increases:       $increases"
    puts "Perm updates:       $permUpdates"
    puts "Wall time:          $wallTime seconds"
    puts "=============================================="
    puts ""

    return 0
}

# run the analysis
puts "Starting adaptive analysis with variable permeability..."
set ok [adaptiveAnalyzeWithPerm $totalTime $dT_initial $dT_min $dT_max $N_success $permUpdateInterval]

if {$ok != 0} {
    puts "Analysis failed to complete!"
} else {
    puts "Analysis completed successfully."
}
"""

def writeMainTclGlobal(tclRootDir, modelName, ndm, ndf,
                       damp=0.05, fLower=0.5, fHigher=10.0,
                       gamma=0.5, beta=0.25,
                       orderedSections=None,
                       analysisType="static",
                       constraints="Transformation",
                       numberer="RCM",
                       system="UmfPack",
                       algorithm="Newton",
                       testType="NormDispIncr",
                       testTol=1.0e-5,
                       testIter=25):
    """
    create a global main.tcl that sources all subfiles in the model folder.

    :param tclRootDir: (str) path to 'TCL-Files' directory
    :param modelName: (str) model folder name (e.g., 'model4')
    :param ndm: (int) number of dimensions (2 or 3)
    :param ndf: (int) number of DOFs per node
    :param damp: (float) damping ratio (default: 0.05)
    :param fLower: (float) lower Rayleigh frequency in Hz (default: 0.5)
    :param fHigher: (float) higher Rayleigh frequency in Hz (default: 10.0)
    :param gamma: (float) Newmark gamma coefficient (default: 0.5)
    :param beta: (float) Newmark beta coefficient (default: 0.25)
    :param orderedSections: (list, optional) custom ordering of file prefixes
    :param analysisType: (str) "static" or "transient" (default: "static")
    :param constraints: (str) constraints handler (default: "Transformation")
    :param numberer: (str) DOF numberer (default: "RCM")
    :param system: (str) system solver (default: "UmfPack")
    :param algorithm: (str) solution algorithm (default: "Newton")
    :param testType: (str) convergence test type (default: "NormDispIncr")
    :param testTol: (float) convergence tolerance (default: 1.0e-5)
    :param testIter: (int) max iterations (default: 25)

    :return: (str) path to generated main.tcl file
    """

    # compute Rayleigh damping coefficients
    omega1 = 2 * np.pi * fLower
    omega2 = 2 * np.pi * fHigher
    a0 = 2 * damp * omega1 * omega2 / (omega1 + omega2)
    a1 = 2 * damp / (omega1 + omega2)

    os.makedirs(tclRootDir, exist_ok=True)
    modelDir = os.path.join(tclRootDir, modelName)

    if not os.path.isdir(modelDir):
        raise FileNotFoundError(f"model folder '{modelDir}' not found.")

    # default section ordering
    if orderedSections is None:
        orderedSections = [
            "modelHeader",
            "nodes",
            "materials",
            "elements",
            "fixity",
            "equalDOF",
            "loads",
            "recorders"
        ]

    # collect all .tcl files in the model folder
    allFiles = os.listdir(str(modelDir))
    tclFiles = sorted([f for f in allFiles if f.endswith(".tcl")])

    # order by logical prefix
    orderedFiles = []
    for prefix in orderedSections:
        matching = [f for f in tclFiles if f.lower().startswith(prefix.lower())]
        orderedFiles.extend(matching)

    # add any remaining files not matched by known prefixes
    orderedFiles.extend([f for f in tclFiles if f not in orderedFiles])

    # path to the global main.tcl
    mainPath = os.path.join(tclRootDir, "main.tcl")

    with open(mainPath, "w") as f:
        # header
        f.write("# ==============================================================================\n")
        f.write(f"# main.tcl for {modelName}\n")
        f.write("# ==============================================================================\n\n")

        # wipe and model builder
        f.write("wipe\n")
        f.write(f"model BasicBuilder -ndm {ndm} -ndf {ndf}\n\n")

        # Rayleigh damping coefficients
        f.write("# ------------------------------------------------------------------------------\n")
        f.write("# Rayleigh Damping Coefficients\n")
        f.write("# ------------------------------------------------------------------------------\n")
        f.write(f"# damping ratio: {damp}\n")
        f.write(f"# frequency range: {fLower} - {fHigher} Hz\n")
        f.write(f"set a0 {a0:.6f}\n")
        f.write(f"set a1 {a1:.6f}\n\n")

        # Newmark coefficients
        f.write("# Newmark integration parameters\n")
        f.write(f"set gamma {gamma}\n")
        f.write(f"set beta {beta}\n\n")

        # time series placeholders
        f.write("# ------------------------------------------------------------------------------\n")
        f.write("# Time Series (uncomment and modify as needed)\n")
        f.write("# ------------------------------------------------------------------------------\n")
        f.write("# timeSeries Path 1 -dt 0.01 -filePath \"vx_record.txt\" -factor 1.0\n")
        f.write("# timeSeries Path 2 -dt 0.01 -filePath \"vy_record.txt\" -factor 1.0\n")
        f.write("# set tsX 1\n")
        f.write("# set tsY 2\n\n")

        # source subfiles
        f.write("# ------------------------------------------------------------------------------\n")
        f.write("# Source Model Files\n")
        f.write("# ------------------------------------------------------------------------------\n")

        for tclFile in orderedFiles:
            relativePath = f"{modelName}/{tclFile}"
            f.write(f'source "{relativePath}"\n')

        f.write("\n")

        # analysis setup
        f.write("# ------------------------------------------------------------------------------\n")
        f.write("# Analysis Setup\n")
        f.write("# ------------------------------------------------------------------------------\n")
        f.write(f"constraints {constraints}\n")
        f.write("# Plain\n")
        f.write("# Penalty 1.e18 1.e18\n")
        f.write("# Lagrange\n")
        f.write("# Transformation\n")

        f.write(f"numberer {numberer}\n")
        f.write("# Plain\n")

        f.write(f"system {system}\n")
        f.write("# BandGeneral\n")
        f.write("# BandSPD\n")
        f.write("# ProfileSPD\n")
        f.write("# SparseGeneral\n")
        f.write("# UmfPack\n")
        f.write("# SparseSPD\n")

        f.write(f"test {testType} {testTol} {testIter} 1\n")

        f.write(f"algorithm {algorithm}\n")
        f.write("# Linear\n")
        f.write("# Newton\n")
        f.write("# NewtonLineSearch $ratio\n")
        f.write("# ModifiedNewton\n")
        f.write("# KrylovNewton\n")
        f.write("# BFGS $count\n")
        f.write("# Broyden $count\n")

        if analysisType.lower() == "static":
            f.write("integrator LoadControl 1.0\n")
            f.write("analysis Static\n\n")
        else:
            f.write("integrator Newmark $gamma $beta\n")
            f.write("rayleigh $a0 0.0 $a1 0.0\n")
            f.write("analysis Transient\n\n")

        # analysis commands placeholder
        f.write("# ------------------------------------------------------------------------------\n")
        f.write("# Run Analysis (uncomment as needed)\n")
        f.write("# ------------------------------------------------------------------------------\n")

        if analysisType.lower() == "static":
            f.write("# analyze 1\n")
        else:
            f.write("# set totalTime 10.0\n")
            f.write("# set dT 0.01\n")
            f.write("# set nSteps [expr int($totalTime / $dT)]\n")
            f.write("# analyze $nSteps $dT\n")

        f.write("\n")
        f.write(f'puts "==== {modelName} model loaded successfully ===="\n')

        # more details HERE (link down) for the selection of analysis commands
        # https://opensees.berkeley.edu/OpenSees/manuals/usermanual/toc187244.htm

        # f_.write("constraints Transformation\n")
        # - Plain
        # - Penalty
        # - Lagrange
        # - Transformation
        #

        # f_.write("numberer RCM\n")
        # - Plain
        # - RCM
        #

        # f_.write("system ProfileSPD\n")
        # - BandGeneral
        # - BandSPD
        # - ProfileSPD
        # - SparseGeneral
        # - UmfPack
        # - SparseSPD
        #

        # f_.write(f"test NormUnbalance {tol} {maxNumIter} {printFlag}\n")
        # - NormUnbalance
        # - NormDispIncr
        # - EnergyIncr

        # f_.write(f"algorithm Newton\n")
        # - Linear
        # - Newton
        # - NewtonLineSearch $ratio # HERE we MUST define the ratio (see Berkeley website for more info)
        # - ModifiedNewton
        # - KrylovNewton
        # - BFGS $count # HERE we MUST define the count int (see Berkeley website for more info)
        # - Broyden # HERE we MUST define the count int (see Berkeley website for more info)
        #

        # f_.write("integrator LoadControl 1.0\n")
        # A) For static analysis
        #   - LoadControl $dLambda1 <$Jd $minLambda $maxLambda>
        #   - DisplacementControl $nodeTag $dofTag $dU1 <$Jd $minDu $maxDu>
        #   - MinUnbalDispNorm $dLambda11 <$Jd $minLambda $maxLambda>
        #   - ArcLength $arcLength $alpha

        # B) For transient analysis
        #   - Newmark $gamma $beta
        #   - HHT $gamma <$alphaM $betaK $betaKInit $betaKComm>
        #

        # f_.write("analysis Static\n\n")
        # Transient
        # VariableTransient

        # f_.write(f' puts "==== {modelName} TCL model loaded successfully ===="\n')

        print(f"Global main.tcl written at: {mainPath}")
        print("Contains source calls for:")
        for f_ in orderedFiles:
            print(f"   • {modelName}/{f_}")

    print(f"[INFO] main.tcl written at: {mainPath}")
    print("[INFO] contains source calls for:")

    for tclFile in orderedFiles:
        print(f"    - {modelName}/{tclFile}")

    return mainPath

def print_index_sets(X, Y, Z):
    Xs = X - 2
    Ys = Y - 2
    Zs = Z - 1

    if Xs <= 0 or Ys <= 0 or Zs <= 0:
        raise ValueError("Need X>=3, Y>=3, Z>=2")

    start = 1

    def show(name, n):
        nonlocal start
        a = start
        b = start + n - 1
        print(f'"ASD3D_{name}": set(range({a}, {b + 1})),')
        start = b + 1

    show("mainSoil",  Xs * Ys * Zs)
    show("B",  Xs * Ys * 1)
    show("L",  1  * Ys * Zs)
    show("R",  1  * Ys * Zs)
    show("F",  Xs * 1  * Zs)
    show("K",  Xs * 1  * Zs)

    show("BL", 1  * Ys * 1)
    show("BR", 1  * Ys * 1)
    show("BF", Xs * 1  * 1)
    show("BK", Xs * 1  * 1)

    show("LF", 1  * 1  * Zs)
    show("LK", 1  * 1  * Zs)
    show("RF", 1  * 1  * Zs)
    show("RK", 1  * 1  * Zs)

    show("BLF", 1)
    show("BLK", 1)
    show("BRF", 1)
    show("BRK", 1)

    print(f"TOTAL = set(range(1, {X*Y*Z + 1}))")

print_index_sets(12, 8, 4)
