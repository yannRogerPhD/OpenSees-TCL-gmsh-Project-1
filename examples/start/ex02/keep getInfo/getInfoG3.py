"""
please note that:
    1. (3D) equalDOFs do not start from the bottom-line nodes since it is assumed fixity conditions are applied there;
       therefore, it needs to be included manually, for example, equalDOF in a special direction (x-only)
    2. for code line 22:
       leftX is the minimum x-value (which here x = 0) needed to get the vertical left boundary
       rightX HAS TO BE CHANGED GENERALLY, please modify rightX accordingly, it's the largest x-coord value
       bottomY is the line characterizing the bottom BC, here, y = 0
"""
import numpy as np

# for base nodes, fix both x and y
fixX = 1
fixY = 1
fixP = 0

nodeCoords = {}
nodeDOFs = {}

leftX, rightX, bottomY = 0.0, 1.0, 0.0
leftBound, rightBound, bottomBound = [], [], []

meshFile = 'model.msh'

nodes3D_File = 'nodes3D.tcl'
nodes2D_File = 'nodes2D.tcl'

fixity2D_File = 'fixity2D.tcl'
fixity3D_File = 'fixity3D.tcl'

fixityWT3D_File = 'fixity3DWT.tcl'

equalDOFs3D_File = 'equalDOFs3D.tcl'
equalDOFs2D_File = 'equalDOFs2D.tcl'

elements_File = 'elements.tcl'

# find max phyGroup for elementType 3 and 10
maxPhyGroup = 0
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
                    elementType = int(parts[1])
                    if elementType == 3:
                        phyGroup = int(parts[4])
                        if phyGroup > maxPhyGroup:
                            maxPhyGroup = phyGroup
                    elif elementType == 10:
                        phyGroup = int(parts[4])
                        if phyGroup > maxPhyGroup:
                            maxPhyGroup = phyGroup
                except (ValueError, IndexError):
                    continue

'''
!!! quad4 elements !!!
    (1) define a list of rhoVals values, make sure its len, that is len(rhoVals) is equal to maxPhyGroup + 1 else ERROR!
        !!! len(rhoVals) >= maxPhyGroup + 1
    (2) replace massDen and fluidDen with appropriate values
    (3) change, if necessary, the list of thickness values, presently its '1' for all soil layers
    (4) list of:
        (a) rhoVals
        (b) thickness values for each layer
    (5) no need of the mainSoilTags since it is adaptative from number of soil layers in gmsh
'''

gVal = 9.806
massDen, fluidDen = 2.202, 0.000
alpha = 0.0
alphaRads = np.deg2rad(alpha)
mainSoilTags = {i: i for i in range(1, maxPhyGroup + 1)}
thickness = {i: 1.0 for i in mainSoilTags}
rhoVals = {i: massDen - fluidDen for i in mainSoilTags}

# # Added print statement for debugging
print(f"Max phyGroup found in pre-pass: {maxPhyGroup}")
print(len(rhoVals))
print(len(mainSoilTags))
print(len(thickness))

'''
!!! quad9 elements !!!
    (1) list of fmass values for each soil layer, such that len(fmass) = maxPhyGroup
    (2) check physical group for the water table; if not water table, choose 0
        phyGroupWT = 0
        phyGroupWT = put the "plane surface" number from gmsh
'''

bulkVals = {i: 5.06e6 for i in mainSoilTags}
fmassVals = {i: 1 for i in mainSoilTags}
hPermVals = {i: 1.0e-4 for i in mainSoilTags}
vPermVals = {i: 1.0e-4 for i in mainSoilTags}
# print("fmass values are:", fmassVals)
# print(len(fmassVals))

# physical group to store WT tables as this will helo for pore pressure fixities
phyGroupWT = 0
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

# we next parse node coordinates
with open(meshFile) as f:
    lines = f.readlines()

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
            nx, ny, nz = float(parts[1]), float(parts[2]), float(parts[3])
            nodeCoords[nodeTag] = (nx, ny)  # keep only x,y since 2D for the moment
        else:
            print(f"warning: skipped malformed node line: '{line}' ")

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

        if len(parts) < 4:
            print(f"warning: skipped malformed line in gmsh's $Element definition: '{line}'")
            continue

        try:
            eleTag = int(parts[0])
            elementType = int(parts[1])
            numOfTags = int(parts[2])
            ns = [int(n) for n in parts[3 + numOfTags:]]

        except ValueError:
            print(f"warning: could not parse element line: '{line}'")
            continue

        if elementType in DOFsRules:
            nodeDOFs.update(DOFsRules[elementType](ns))

            if elementType == 10:
                phyGroup = int(parts[4])

                if phyGroup == phyGroupWT:
                    nodesWT.update(DOFsRules[elementType](ns))

            # uncomment the line below for debug if necessary
            # print(f"Processed element {eleTag}: unknown elementType {elementType}")

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

# write output of 3DOFs nodes
if node3DOFs:  # only write this section if it’s not empty
    with open(nodes3D_File, 'w') as f3:
        f3.write('# !!!!!!!! 3DOFs nodes !!!!!!!!!\n\n')
        f3.write('model BasicBuilder -ndm 2 -ndf 3\n\n')
        for nodeTAGS, coordS in sorted(node3DOFs.items()):
            f3.write(f"node {nodeTAGS} {coordS[0]:.3f} {coordS[1]:.3f}\n")

# write output of 2DOFs nodes
if node2DOFs:  # only write this section if it’s not empty
    with open(nodes2D_File, 'w') as f2:
        f2.write('# !!!!!!!! 2DOFs nodes !!!!!!!!!\n\n')
        f2.write('model BasicBuilder -ndm 2 -ndf 2\n\n')
        for nodeTAGS, coordS in sorted(node2DOFs.items()):
            f2.write(f"node {nodeTAGS} {coordS[0]:.3f} {coordS[1]:.3f}\n")


# we then parse boundary elements
with open(meshFile) as f:
    lines = f.readlines()

    inNodeSection = False

    for line in lines:
        line = line.strip()

        if line == '$Nodes':
            inNodeSection = True
            continue

        elif line == '$EndNodes':
            inNodeSection = False
            break

        if inNodeSection:
            parts = line.split()
            nodeTag = int(parts[0])

            if len(parts) == 4:
                xBoundLeft = float(parts[1])
                xBoundRight = float(parts[1])
                yBoundBottom = float(parts[2])

                if xBoundLeft == leftX:
                    leftBound.append(nodeTag)

                if xBoundRight == rightX:
                    rightBound.append(nodeTag)

                if yBoundBottom == bottomY:
                    bottomBound.append(nodeTag)

# print(leftBound)
leftBound = sorted(leftBound, key=lambda it: nodeCoords[it][1])
rightBound = sorted(rightBound, key=lambda it: nodeCoords[it][1])
bottomBound = sorted(bottomBound, key=lambda it: nodeCoords[it][0])

leftNodes2D = [n for n in leftBound if n in node2DOFs]
rightNodes2D = [n for n in rightBound if n in node2DOFs]
bottomNodes2D = [n for n in bottomBound if n in node2DOFs]

leftNodes3D = [n for n in leftBound if n in node3DOFs]
rightNodes3D = [n for n in rightBound if n in node3DOFs]
bottomNodes3D = [n for n in bottomBound if n in node3DOFs]

if node2DOFs:
    print('left 2D nodes:', leftNodes2D)
    print('right 2D nodes:', rightNodes2D)
    print('bottom 2D nodes:', bottomNodes2D)

if node3DOFs:
    print('left 3D nodes:', leftNodes3D)
    print('right 3D nodes:', rightNodes3D)
    print('bottom 3D nodes:', bottomNodes3D)

titleFixities2D = False
titleFixities3D = False

# 3DOFs nodes fixities
if node3DOFs:
    with open(fixity3D_File, 'w') as f3Fix:
        for nodeTag in bottomNodes3D:
            if nodeTag in node3DOFs:
                if not titleFixities3D:
                    f3Fix.write("# !!!!!!! fixities for 3DOFs nodes !!!!!!!\n")
                    titleFixities3D = True
                f3Fix.write(f"fix {nodeTag} {fixX} {fixY} {fixP}\n")

# 2DOFs nodes fixities
if node2DOFs:
    with open(fixity2D_File, 'w') as f2Fix:
        # for nodeTag in sorted(bottomNodesB | leftNodesB | rightNodesB):
        for nodeTag in bottomNodes2D:
            if nodeTag in node2DOFs:
                if not titleFixities2D:
                    f2Fix.write("# !!!!!!! fixities for 2DOFs nodes !!!!!!!\n")
                    titleFixities2D = True
                f2Fix.write(f"fix {nodeTag} {fixX} {fixY}\n")


# fix output of 3rd DOF (pressure) nodes for those above the WT
if node3DOFsWT:
    with open(fixityWT3D_File, 'w') as f3WT:
        f3WT.write("# fix the 3rd DOF, the pressure DOFs, for nodes above the water table\n")
        for nodeTAGS, coordS in sorted(node3DOFsWT.items()):
            f3WT.write(f"fix {nodeTAGS} 0 0 1\n")


# 3DOFs equalDOFs
if node3DOFs:
    with open(equalDOFs3D_File, 'w') as f3Equal:
        # Left–Right equalDOFs (1 & 2 only)
        for i, j in zip(leftNodes3D[1:], rightNodes3D[1:]):
            if i in node3DOFs and j in node3DOFs:
                f3Equal.write(f"equalDOF {i} {j} 1 2\n")

# 2DOFs equalDOFs
if node2DOFs:
    with open(equalDOFs2D_File, 'w') as f2Equal:
        # Left–Right equalDOFs (1 & 2 only)
        for i, j in zip(leftNodes2D[1:], rightNodes2D[1:]):
            if i in node2DOFs and j in node2DOFs:
                f2Equal.write(f"equalDOF {i} {j} 1 2\n")

with open(elements_File, 'w') as f_ele:
    with open(meshFile) as f:
        lines = f.readlines()

        inElementSection = False
        f_ele.write('''# !!!!!!!! Elements !!!!!!!!! \n''')

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
                if len(parts) < 4:
                    continue

                try:
                    eleTag = int(parts[0])
                    elementType = int(parts[1])
                    numOfTags = int(parts[2])
                    nodes_ = ' '.join(parts[5:])
                except (ValueError, IndexError):
                    continue

                if elementType == 10:  # 9-node quad

                    if len(parts) == 14:
                        # print(eleTag)
                        try:
                            phyGroup = int(parts[4])
                            # print(phyGroup)

                            if phyGroup in mainSoilTags:
                                xWgt = - gVal * np.sin(alphaRads)
                                yWgt = - gVal * np.cos(alphaRads)

                                f_ele.write(f"element 9_4_QuadUP "
                                            f"{eleTag} "
                                            f"{nodes_} "
                                            f"{thickness[phyGroup]} "
                                            # f"{mat['matTag']} "
                                            f"{phyGroup} "
                                            f"{bulkVals[phyGroup]} "
                                            f"{fmassVals[phyGroup]} "
                                            f"{hPermVals[phyGroup]} "
                                            f"{vPermVals[phyGroup]} "
                                            f"{xWgt} "
                                            f"{yWgt}\n")
                        except (ValueError, IndexError):
                            continue

                elif elementType == 3:  # 4-node quad
                    # relaxed condition to check for at least 5 parts
                    if len(parts) == 9:
                        try:
                            phyGroup = int(parts[4])
                            # print(phyGroup)
                            if phyGroup in mainSoilTags:
                                wtX = gVal * rhoVals[phyGroup] * np.sin(alphaRads)
                                wtY = - gVal * rhoVals[phyGroup] * np.cos(alphaRads)
                                f_ele.write(f"element "
                                            f"quad "
                                            f"{eleTag} "
                                            f"{nodes_} "
                                            f"{thickness[phyGroup]} "
                                            f"PlaneStrain "
                                            f"{mainSoilTags[phyGroup]} "
                                            f"0.0 "
                                            f"0.0 "
                                            f"{wtX} "
                                            f"{wtY}\n")
                        except (ValueError, IndexError):
                            continue
