import numpy as np

# for base nodes, fix both x and y
fixX = 0
fixY = 1
fixP = 0

nodeCoords = {}
nodeDOFs = {}

leftX, rightX, bottomY = 0.0, 1.0, 0.0
middleX, OneDimAnalysis = (rightX - leftX) / 2, True
leftBound, rightBound, bottomBound = [], [], []
middleBound = []

# meshFile = 'model.msh'
meshFile = 'model.msh'

nodes3D_File = 'nodes3D.tcl'
nodes2D_File = 'nodes2D.tcl'

fixity2D_File = 'fixity2D.tcl'
fixity3D_File = 'fixity3D.tcl'

fixityWT3D_File = 'fixity3DWT.tcl'

equalDOFs3D_File = 'equalDOFs3D.tcl'
equalDOFs2D_File = 'equalDOFs2D.tcl'
equalDOFs2DBottom_File = 'equalDOFs2DBottom.tcl'

equalDOFs2DMiddle_File = 'equalDOFs2DMiddle.tcl'

elementsFile = 'elements.tcl'

# !!!!!!!!!!! #
elements = []
with open(meshFile) as f:
    lines = f.readlines()
    inElementSection = False

    for line in lines:
        line = line.strip()

        if line == '$Elements':
            inElementSection = True
            continue

        elif line == '$EndElements':
            inElementSection = False
            break

        if inElementSection:
            parts = line.split()

            if len(parts) > 4:
                try:
                    eleTag = int(parts[0])
                    elementType = int(parts[1])
                    numOfTags = int(parts[2])
                    phyGroup = int(parts[4])
                    ns = [int(n) for n in parts[3 + numOfTags:]]

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

phyGroups = [el["group"] for el in elements if el["type"] in (3, 10)]

# find max phyGroup for elementType 3 and 10
maxPhyGroup = max(phyGroups) if phyGroups else 0

gVal = 9.806
massDen, fluidDen = 1755, 0.000
alpha = np.atan(2.0/100)
# alphaRads = np.deg2rad(alpha)
alphaRads = alpha
mainSoilTags = {i: i for i in range(1, maxPhyGroup + 1)}
thickness = {i: 1.0 for i in mainSoilTags}
rhoVals = {i: massDen - fluidDen for i in mainSoilTags}

# # Added print statement for debugging
print(f"Max phyGroup found in pre-pass: {maxPhyGroup}")
print(len(rhoVals))
print(len(mainSoilTags))
print(len(thickness))

# bulkVals = {i: 5.06e6 for i in mainSoilTags}
# bulkVals2 = {1: 3, 2: 4, 3: 5.06e6}
bulkVals = {1: 6.88e6, 2: 5.06e6, 3: 5.0e-6}

# fmassVals = {i: 1 for i in mainSoilTags}
fmassVals = {i: 1.0 for i in mainSoilTags}
# print(f"fMass values: ", fmassVals)

# hPermVals = {i: 1.0e-4 for i in mainSoilTags}
hPermVals = {i: 1.0 for i in mainSoilTags}

vPermVals = {i: 1.0 for i in mainSoilTags}
# print("fmass values are:", fmassVals)
# print(len(fmassVals))

# physical group to store WT tables as this will helo for pore pressure fixities
phyGroupWT = 3
nodesWT = {}


# helper functions for DOF rules
def only2DOFs(ns_):
    """
    Here, every/ALL node/nodes gets 2 DOFs,
    for example, QUAD
    """
    return {n: 2 for n in ns_}


def both2and3DOFs(ns_):
    """
    Here, a typical example is the nine-four node quad u-p element (OpenSees), where:
    first four nodes (corners) -> 3 DOFs, rest -> 2 DOFs...

    1st-4 nodes (from gmsh format) are corner nodes (in OpenSees documentation that corresponds to 1, 2, 3, and 4 ):
        - these nodes are three-DOFs nodes (displacement in x, displacement in y, and pressure)

    the rest of the nodes are interior nodes and these are two-DOF nodes
    """
    return {**{n: 3 for n in ns_[:4]},
            **{n: 2 for n in ns_[4:]}}


# mapping: elementType --> DOF rule
DOFsRules = {
    # page 357 of the gmsh documentation (can be extended easily)
    3: only2DOFs,  # for 4-node quad
    10: both2and3DOFs  # for 9-node quad
}

for el in elements:
    if el["type"] in DOFsRules:
        for n, dof in DOFsRules[el["type"]](el["nodes"]).items():
            if n not in nodeDOFs or dof > nodeDOFs[n]:
                nodeDOFs[n] = dof

        if el["type"] == 10 and el["group"] == phyGroupWT:
            for n, dof in DOFsRules[el["type"]](el["nodes"]).items():
                if n not in nodesWT or dof > nodesWT[n]:
                    nodesWT[n] = dof


inNodeSection = False
for line in lines:
    line = line.strip()
    if line == '$Nodes':
        inNodeSection = True
        continue
    elif line == '$EndNodes':
        inNodeSection = False
        continue

    if inNodeSection:
        parts = line.split()
        if len(parts) >= 4:
            nodeTag = int(parts[0])
            # nx, ny, nz = float(parts[1]), float(parts[2]), float(parts[3])
            nx, ny, nz = round(float(parts[1]), 4), round(float(parts[2]), 4), round(float(parts[3]), 4)
            nodeCoords[nodeTag] = (nx, ny)  # keep only x,y since 2D for the moment
        else:
            print(f"warning: skipped malformed node line: '{line}' ")

# print(nodeDOFs)
# print(f"nodes of water table are:", nodesWT)

# we can now separate 2DOFs and 3DOFs nodes
node3DOFs = {tag: coords for tag, coords in nodeCoords.items()
             if nodeDOFs.get(tag) == 3}
node2DOFs = {tag: coords for tag, coords in nodeCoords.items()
             if nodeDOFs.get(tag) == 2}

node3DOFsWT = {tag: coords for tag, coords in nodeCoords.items()
               if nodesWT.get(tag) == 3}
node2DOFsWT = {tag: coords for tag, coords in nodeCoords.items()
               if nodesWT.get(tag) == 2}

if phyGroupWT:
    print(f"3 DOFs water table nodes are:", node3DOFsWT)
    print(f"2 DOFs water table nodes are:", node2DOFsWT)

if phyGroupWT:
    print(f"length of 3 DOFs water table nodes are:", len(node3DOFsWT))
    print(f"length of 2 DOFs water table nodes are:", len(node2DOFsWT))


def writeNodesToFile(fileName, nodeDict, ndm, ndf):
    # write a set of nodes and their coordinates to a TCL file
    if not nodeDict:
        return
    with open(fileName, 'w') as f_:
        f_.write(f"# !!!!!!!! {ndf}DOFs nodes !!!!!!!!!\n\n")
        f_.write(f"model BasicBuilder -ndm {ndm} -ndf {ndf}\n\n")
        for nodeTAG, (x, y) in sorted(nodeDict.items()):
            f_.write(f"node {nodeTAG} {x:.4f} {y:.4f}\n")


def nodesNearX(xTarget, tol=1e-5):
    # return all nodes with x approx equal to xTarget within tolerance
    return [tag for tag, (x, y) in nodeCoords.items() if abs(x - xTarget) < tol]


def nodesNearY(yTarget, tol=1e-5):
    # return all nodes with y approx equal to yTarget within tolerance
    return [tag for tag, (x, y) in nodeCoords.items() if abs(y - yTarget) < tol]


def selectNodes(condition):
    # select all nodes satisfying a custom generic condition: condition(x, y) -> bool
    return [tag for tag, (x, y) in nodeCoords.items() if condition(x, y)]


def sortNodesByX(nodes):
    # sort a list of node tags by their x-coordinates
    return sorted(nodes, key=lambda tag: nodeCoords[tag][0])


def sortNodesByY(nodes):
    # sort a list of node tags by their y-coordinates
    return sorted(nodes, key=lambda tag: nodeCoords[tag][1])


def filter2DOFs(nodes):
    # return only nodes with 2 DOFs
    return [n for n in nodes if nodeDOFs.get(n) == 2]


def filter3DOFs(nodes):
    # return only nodes with 3 DOFs
    return [n for n in nodes if nodeDOFs.get(n) == 3]


leftBound = nodesNearX(leftX)
rightBound = nodesNearX(rightX)
bottomBound = nodesNearY(bottomY)

# all nodes in a central vertical strip (0.45 < x < 0.55)
# centerStrip = selectNodes(lambda x, y: 0.45 < x < 0.55)

if OneDimAnalysis:
    middleBound = nodesNearX(middleX)

# print(leftBound)
leftBound = sortNodesByY(leftBound)
rightBound = sortNodesByY(rightBound)
bottomBound = sortNodesByX(bottomBound)


leftNodes2D = filter2DOFs(leftBound)
rightNodes2D = filter2DOFs(rightBound)
bottomNodes2D = filter2DOFs(bottomBound)

leftNodes3D = filter3DOFs(leftBound)
rightNodes3D = filter3DOFs(rightBound)
bottomNodes3D = filter3DOFs(bottomBound)

# can perform combinations such as ... at once
# leftNodes2D = filter2DOFs(sortNodesByY(nodesNearX(leftX)))
# all 2DOF nodes on left boundary sorted vertically
# leftNodes2D = filter2DOFs(sortNodesByY(nodesNearX(leftX)))

# all 3DOF nodes on bottom boundary sorted horizontally
# bottomNodes3D = filter3DOFs(sortNodesByX(nodesNearY(bottomY)))

# all 3DOF nodes in a vertical strip (0.45 < x < 0.55), bottom to top
# centerStrip3D = filter3DOFs(sortNodesByY(selectNodes(lambda x, y: 0.45 < x < 0.55)))

middleBound = sortNodesByY(middleBound)
middleBound2D = filter2DOFs(middleBound)
middleBound3D = filter3DOFs(middleBound)

# alternate nodes in a middle strip: used to match left 2D and left 3D lists later
middleBound2D_1 = middleBound2D[1::2]  # 2nd, 4th, 6th, ...
middleBound2D_2 = middleBound2D[0::2]  # 1st, 3rd, 5th, ...


print('\n')

print('middle bound 2D: ', middleBound2D)
print('middle bound 2D I: ', middleBound2D_1)
print('middle bound 2D II: ', middleBound2D_2)

print('\n')

# check this to make sure it only holds for 1D SRAs

if node2DOFs:
    print('left 2D nodes:', leftNodes2D)
    print('right 2D nodes:', rightNodes2D)
    print('bottom 2D nodes:', bottomNodes2D)
    # print('middle 2D nodes:', middleBound2D)

print('\n')

if node3DOFs:
    print('left 3D nodes:', leftNodes3D)
    print('right 3D nodes:', rightNodes3D)
    print('bottom 3D nodes:', bottomNodes3D)
    # print('middle 3D nodes:', middleBound3D)

print('\n')

titleFixities2D = False
titleFixities3D = False


def writeFixities(fileName, nodes, fixValues, header):

    if not nodes:
        return
    with open(fileName, 'w') as f_:
        f_.write(f"# {header}\n\n")

        for ns_ in nodes:
            f_.write(f"fix {ns_} {' '.join(str(v) for v in fixValues)}\n")


def writeEqualDOFs(fileName, nodePairs, dofList, header):
    """
    write equalDOF commands to file;
    (1) nodePairs can be either:
        - a list of (i, j) tuples for paired nodes
        - or a list of single node IDs (for one-reference equalDOFs)
    (2) dofList is a list of DOF indices, e.g. [1, 2] or [1]
    """
    if not nodePairs:
        return

    with open(fileName, 'w') as f_:
        f_.write(f"# {header}\n\n")

        for pair in nodePairs:
            if isinstance(pair, tuple) and len(pair) == 2:
                i_, j_ = pair
                f_.write(f"equalDOF {i_} {j_} {' '.join(map(str, dofList))}\n")
            else:
                # for cases like "equalDOF refNode node 1"
                refNode = nodePairs[0]
                if pair != refNode:
                    f_.write(f"equalDOF {refNode} {pair} {' '.join(map(str, dofList))}\n")


def writeElements(fileName, elements_, mainSoilTags_, thickness_, bulkVals_,
                  fmassVals_, hPermVals_, vPermVals_, gVal_, alphaRads_):
    """
    write element definition to file;
    handles both 9_4_QuadUP (type 10) and quad (type 3) elements automatically
    """
    with open(fileName, 'w') as f_:
        f_.write("# !!!!!!!!! elements !!!!!!!!! \n\n")

        for el in elements_:
            eleTag_ = el["id"]
            elementType_ = el["type"]
            phyGroup_ = el["group"]
            nodes = " ".join(str(n) for n in el["nodes"])

            # 9_4_QuadUP elements
            if elementType_ == 10 and phyGroup_ in mainSoilTags_:
                xWgt_ = - gVal_ * np.sin(alphaRads_)
                yWgt_ = - gVal_ * np.cos(alphaRads_)

                f_.write(f"element 9_4_QuadUP "
                         f"{eleTag_} "
                         f"{nodes} "
                         f"{thickness_[phyGroup_]} "
                         f"{phyGroup_} "
                         f"{bulkVals_[phyGroup_]} "
                         f"{fmassVals_[phyGroup_]} "
                         f"{hPermVals_[phyGroup_]} "
                         f"{vPermVals_[phyGroup_]} "
                         f"{xWgt_} "
                         f"{yWgt_}\n")

            elif elementType_ == 3 and phyGroup_ in mainSoilTags_:
                rhoV_ = 1.7
                wtX_ = gVal_ * rhoV_ * np.sin(alphaRads_)
                wtY_ = - gVal_ * rhoV_ * np.cos(alphaRads_)

                f_.write(f"element "
                         f"quad "
                         f"{eleTag_} "
                         f"{nodes} "
                         f"{thickness_[phyGroup_]} "
                         f"PlaneStrain "
                         f"{mainSoilTags_[phyGroup_]} "
                         f"0.0 "
                         f"0.0 "
                         f"{wtX_} "
                         f"{wtY_}\n")


def writingOutputs(writingNodes=True,
                   writingFixities=True,
                   writingEqualDOFs=True,
                   writingElements=True):
    """
    Generate selected TCL output files.

    Parameters:
        writingNodes: nodes3D.tcl, nodes2D.tcl
        writingFixities: fixity*.tcl
        writingEqualDOFs: equalDOFs*.tcl
        writingElements: elements.tcl
    """

    if writingNodes:
        if node3DOFs:
            writeNodesToFile(nodes3D_File, node3DOFs, 2, 3)
        if node2DOFs:
            writeNodesToFile(nodes2D_File, node2DOFs, 2, 2)
        print("✅ Wrote node files")

    if writingFixities:
        writeFixities(fixity3D_File, bottomNodes3D, [fixX, fixY, fixP],
                      "Fixities for 3DOFs nodes (bottom boundary)")
        writeFixities(fixity2D_File, bottomNodes2D, [fixX, fixY],
                      "Fixities for 2DOFs nodes (bottom boundary)")
        writeFixities(fixityWT3D_File, node3DOFsWT.keys(), [0, 0, 1],
                      "Fix the 3rd DOF (pressure) for nodes above the water table")
        print("✅ Wrote fixities")

    if writingEqualDOFs:
        pairs3D_ = [(i, j) for i, j in zip(leftNodes3D, rightNodes3D)
                    if i in node3DOFs and j in node3DOFs]
        writeEqualDOFs(equalDOFs3D_File, pairs3D_, [1, 2],
                       "Left–Right equalDOFs for 3DOFs nodes")

        pairs2D_ = [(i, j) for i, j in zip(leftNodes2D, rightNodes2D)
                    if i in node2DOFs and j in node2DOFs]
        writeEqualDOFs(equalDOFs2D_File, pairs2D_, [1, 2],
                       "Left–Right equalDOFs for 2DOFs nodes")

        writeEqualDOFs(equalDOFs2DBottom_File, bottomNodes2D, [1],
                       "Bottom boundary equalDOFs (2DOFs)")

        if middleBound2D and len(middleBound) == (len(leftNodes2D) + len(leftNodes3D)):
            pairs2DMid_ = list(zip(leftNodes2D, middleBound2D_1))
            pairs3DMid_ = list(zip(leftNodes3D, middleBound2D_2))
            writeEqualDOFs(equalDOFs2DMiddle_File, pairs2DMid_ + pairs3DMid_, [1, 2],
                           "EqualDOFs between left and middle nodes (2D + 3D)")
        print("✅ Wrote equalDOFs")

    if writingElements:
        writeElements(elementsFile,
                      elements,
                      mainSoilTags,
                      thickness,
                      bulkVals,
                      fmassVals,
                      hPermVals,
                      vPermVals,
                      gVal,
                      alphaRads)
        print("✅ Wrote elements")

    print("\n───────────── Summary ─────────────")
    print(f"Nodes:        {'✅' if writingNodes else '❌'}")
    print(f"Fixities:     {'✅' if writingFixities else '❌'}")
    print(f"EqualDOFs:    {'✅' if writingEqualDOFs else '❌'}")
    print(f"Elements:     {'✅' if writingElements else '❌'}")
    print("───────────────────────────────────\n")

    print("\n✅ Selected outputs successfully written.")


if __name__ == "__main__":
    # example uses:
    # writingOutputs(writingNodes=False, writingFixities=True) # only fixities
    # writingOutputs(writingEqualDOFs=True) # only equalDOFs
    writingOutputs(writingNodes=False, writingFixities=False, writingEqualDOFs=False, writingElements=True)

"""
centerStrip = sortByY(selectNodes(lambda x, y: 0.45 < x < 0.55))  # one direct step
centerStrip = selectNodes(lambda x, y: 0.0 <= y <= 1.0 and x >= 0.5)
centerStrip = sorted(centerStrip, key=lambda tag: nodeCoords[tag][1])
centerStrip = sorted(centerStrip, key=lambda tag: nodeCoords[tag][0])
print(f"nodes defined such that: 0.45 < x < 0.55\n")
print(centerStrip[:10])
print(centerStrip[10:20])
print(centerStrip[20:30])
print(centerStrip[30:40])
print(centerStrip[40:50])
"""
