"""
please note that:
    1. (3D) equalDOFs do not start from the bottom-line nodes since it is assumed fixity conditions are applied there;
       therefore, it needs to be included manually, for example, equalDOF in a special direction (x-only)
    2. for code line 22:
       leftX is the minimum x-value (which here x = 0) needed to get the vertical left boundary
       rightX HAS TO BE CHANGED GENERALLY, please modify rightX accordingly, it's the largest x-coord value
       bottomY is the line characterizing the bottom BC, here, y = 0
"""
import sys

meshFile = 'model1.msh'

nodes3D_File = 'nodes3D.tcl'
nodes2D_File = 'nodes2D.tcl'

fixity2D_File = 'fixity2D.tcl'
fixity3D_File = 'fixity3D.tcl'

equalDOFs3D_File = 'equalDOFs3D.tcl'
equalDOFs2D_File = 'equalDOFs2D.tcl'

elements_File = 'elements.tcl'

# Try to import the material properties
try:
    from quadUP_properties import quadUP_materials
    from quad_properties import quad_materials
except ImportError:
    print("ERROR: A properties file was not found. "
          "Please ensure quadUP_properties.py and quad_properties.py are in the same directory.")
    sys.exit(1)

nodeCoords = {}
nodeDOFs = {}

leftX, rightX, bottomY = 0.0, 1.5, 0.0
leftBound, rightBound, bottomBound = [], [], []


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

            # uncomment the line below for debug if necessary
            # print(f"Processed element {eleTag}: unknown elementType {elementType}")

# print(nodeDOFs)

# we can now separate 2DOFs and 3DOFs nodes
node3DOFs = {tag: coords for tag, coords in nodeCoords.items()
             if nodeDOFs.get(tag) == 3}
node2DOFs = {tag: coords for tag, coords in nodeCoords.items()
             if nodeDOFs.get(tag) == 2}

# write output of 3DOFs nodes
with open(nodes3D_File, 'w') as f3:

    if node3DOFs:  # only write this section if it’s not empty
        f3.write('# !!!!!!!! 3DOFs nodes !!!!!!!!!\n\n')
        f3.write('model BasicBuilder -ndm 2 -ndf 3\n\n')
        for nodeTAGS, coordS in sorted(node3DOFs.items()):
            f3.write(f"node {nodeTAGS} {coordS[0]:.3f} {coordS[1]:.3f}\n")
        # f3.write("\n")

# write output of 2DOFs nodes
with open(nodes2D_File, 'w') as f2:
    if node2DOFs:  # only write this section if it’s not empty
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

print('left 2D nodes:', leftNodes2D)
print('right 2D nodes:', rightNodes2D)
print('bottom 2D nodes:', bottomNodes2D)

print('left 3D nodes:', leftNodes3D)
print('right 3D nodes:', rightNodes3D)
print('bottom 3D nodes:', bottomNodes3D)

# 3DOFs nodes fixities
with open(fixity3D_File, 'w') as f3Fix:
    # for nodeTag in sorted(bottomNodesB | leftNodesB | rightNodesB):
    for nodeTag in bottomNodes3D:
        if nodeTag in node3DOFs:
            f3Fix.write(f"fix {nodeTag} 0 1 0\n")

# 2DOFs nodes fixities
with open(fixity2D_File, 'w') as f2Fix:
    # for nodeTag in sorted(bottomNodesB | leftNodesB | rightNodesB):
    for nodeTag in bottomNodes2D:
        if nodeTag in node2DOFs:
            f2Fix.write(f"fix {nodeTag} 0 1\n")

# 3DOFs equalDOFs
with open(equalDOFs3D_File, 'w') as f3Equal:
    # Left–Right equalDOFs (1 & 2 only)
    for i, j in zip(leftNodes3D[1:], rightNodes3D[1:]):
        if i in node3DOFs and j in node3DOFs:
            f3Equal.write(f"equalDOF {i} {j} 1 2\n")

# 2DOFs equalDOFs
with open(equalDOFs2D_File, 'w') as f2Equal:
    # Left–Right equalDOFs (1 & 2 only)
    for i, j in zip(leftNodes2D[0:], rightNodes2D[0:]):
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
                    physicalTag = int(parts[3])  # Assuming the first tag is the physical group
                    ns = [int(n) for n in parts[3 + numOfTags:]]
                except (ValueError, IndexError):
                    continue

                if elementType == 10:  # 9-node quad
                    if physicalTag in quadUP_materials:
                        mat = quadUP_materials[physicalTag]
                        nodes = ' '.join(map(str, ns))
                        f_ele.write(f"element 9_4_QuadUP "
                                    f"{eleTag} "
                                    f"{nodes} "
                                    f"{mat['thick']} "
                                    f"{mat['matTag']} "
                                    f"{mat['bulk']} "
                                    f"{mat['fmass']} "
                                    f"{mat['hPerm']} "
                                    f"{mat['vPerm']}\n")
                    else:
                        print("Warning: quadUP properties not found for physical tag {} in element {}. "
                              "Element not created.".format(physicalTag, eleTag))

                elif elementType == 3:  # 4-node quad
                    if physicalTag in quad_materials:
                        mat = quad_materials[physicalTag]
                        nodes = ' '.join(map(str, ns))
                        f_ele.write(f"element quad "
                                    f"{eleTag} "
                                    f"{nodes} "
                                    f"{mat['thick']} "
                                    f"{mat['type']} "
                                    f"{mat['matTag']} "
                                    f"{mat['pressure']} "
                                    f"{mat['rho']} "
                                    f"{mat['b1']} "
                                    f"{mat['b2']}\n")
                    else:
                        print("Warning: quad properties not found for physical tag {} in element {}. "
                              "Element not created.".format(physicalTag, eleTag))
