import os

from meshHelper import (
    outputFolder, FuzzyFloat, defaultTolerance, _roundFunc, nodesNearX, nodesNearY, nodesNearZ,  # noqa: F401
    selectNodes, sortNodesByX, sortNodesByY, sortNodesByZ, writeFixities, writeEqualDOFs, writeNodesTcl,  # noqa: F401
    writeSeparatedNodeFiles,
    writeElementsTcl, writeMainTclGlobal, parseElementsFromMsh, parseNodesFromMsh, detectMaxPhyGroup,
    only2DOFs, both2and3DOFs, threeDOFs, fourDOFs3D, twentyEightBrickDOFs, elementProfiles  # noqa: F401
)

meshFile = "model4.msh"

# basic geometry setup
transX, transY, transZ = 7, 5, 0
xMin, xMax = 0.0, 0.5
yMin, yMax = 0.0, 0.5
zMin, zMax = 0.0, 0.0

# compute the thickness increments
thickX = (xMax - xMin) / (transX - 1)
thickY = (yMax - yMin) / (transY - 1)
thickZ = (zMax - zMin) / (transZ - 1)

# prepare output folder once
outDir = outputFolder(meshFile)


sspBrickGroups, bbarQuadUPGroups, quadUPGroups, bbarBrickGroups = {}, {}, {}, {}  # example physical volume IDs
# sspBrickGroups = {1, 2, 3}, bbarBrickGroups = {} is for volumes instead

gVal = 9.806

maxPhyGroup = detectMaxPhyGroup(meshFile)  # detect the maximum physical group ID directly from mesh

if maxPhyGroup == 0:  # stop if no physical groups were found
    raise RuntimeError("No physical groups detected in the .msh file. Check that file has a valid $Elements section.")

mainSoilTags = {i: i for i in range(1, maxPhyGroup + 1)}  # auto-build physical group tags based on mesh content

print(f"✅ Detected {maxPhyGroup} physical groups in mesh → mainSoilTags = {list(mainSoilTags.keys())}")

elements = parseElementsFromMsh(meshFile)

# -----------------------------------------------------------
# Filter out 2D surface elements when 3D volumes are present
# -----------------------------------------------------------

has3D = any(el["type"] in (5, 105, 1005, 17) for el in elements)
if has3D:
    elements = [el for el in elements if el["type"] in (5, 105, 1005, 17)]
    print("Detected 3D mesh → ignoring surface elements (type 3)...")

for el in elements:

    if el["type"] == 3:
        if el["group"] in bbarQuadUPGroups:
            el["type"] = 103  # 2D bbarQuadUP
        elif el["group"] in quadUPGroups:
            el["type"] = 1003  # 2D quadUP

    elif el["type"] == 5 and el["group"] in bbarBrickGroups:
        el["type"] = 105  # 3D bbarBrickUP

    elif el["type"] == 5 and el["group"] in sspBrickGroups:
        el["type"] = 1005  # 3D SSPbrickUP

mappedBbar = sum(el["type"] == 103 for el in elements)
mappedQuadUP = sum(el["type"] == 1003 for el in elements)
mappedBbarBrickUP = sum(el["type"] == 105 for el in elements)
mappedSSPBrickUP = sum(el["type"] == 1005 for el in elements)

if mappedBbar:
    print(f"Remapped {mappedBbar} elements → bbarQuadUP (103)")

if mappedQuadUP:
    print(f"Remapped {mappedQuadUP} elements → quadUP (1003)")

if mappedBbarBrickUP:
    print(f"Remapped {mappedBbarBrickUP} elements → bbarBrickUP (105)")

if mappedSSPBrickUP:
    print(f"Remapped {mappedSSPBrickUP} elements → SSPbrickUP (1005)")

# Detect element types and compute ndm / ndf
usedProfiles = {el["type"] for el in elements if el["type"] in elementProfiles}
print()
print("usedProfiles:", usedProfiles)

if usedProfiles:
    # determine ndm and ndf correctly for 2D / 3D u-p
    ndmGlobal = max(elementProfiles[t]["ndm"] for t in usedProfiles)
    if ndmGlobal == 2:
        ndfGlobal = 3 if any(elementProfiles[t]["needsP"] for t in usedProfiles) else 2
    elif ndmGlobal == 3:
        ndfGlobal = 4 if any(elementProfiles[t]["needsP"] for t in usedProfiles) else 3
    else:
        ndfGlobal = 2  # fallback

else:
    ndmGlobal, ndfGlobal = 2, 2

# print(f"Detected ndmGlobal = {ndmGlobal}, ndfGlobal = {ndfGlobal}")

nodeDOFs = {}
for el in elements:
    eType = el["type"]
    if eType in elementProfiles:
        ruleFunc = elementProfiles[eType]["dofRule"]
        for nodeTag, dofCount in ruleFunc(el["nodes"]).items():
            # keep the maximum DOF for nodes shared by multiple elements
            if nodeTag not in nodeDOFs or dofCount > nodeDOFs[nodeTag]:
                nodeDOFs[nodeTag] = dofCount

# summarize
twoDOFNodes = [n for n, d in nodeDOFs.items() if d == 2]
threeDOFNodes = [n for n, d in nodeDOFs.items() if d == 3]
fourDOFNodes = [n for n, d in nodeDOFs.items() if d == 4]

print(f"\nTotal nodes detected: {len(nodeDOFs)}")
print(f"  2-DOF nodes: {len(twoDOFNodes)}")
print(f"  3-DOF nodes: {len(threeDOFNodes)}")
print(f"  4-DOF nodes: {len(fourDOFNodes)}")

# -------------------------------------------------------
# Write the header file
# -------------------------------------------------------
headerPath = os.path.join(outDir, "modelHeader.tcl")
with open(headerPath, "w") as f:
    f.write(f"model BasicBuilder -ndm {ndmGlobal} -ndf {ndfGlobal}\n")
print(f"✅ modelHeader.tcl written at: {headerPath}")

print(f"!! OpenSees model header: ndm={ndmGlobal}, ndf={ndfGlobal} "
      f"({', '.join(elementProfiles[t]['key'] for t in usedProfiles)})\n")
# print("✅ modelHeader.tcl written.")

# -------------------------------------------------------
# Read node coordinates from Gmsh
# -------------------------------------------------------
nodeCoords = parseNodesFromMsh(meshFile)
print(f"✅ Parsed {len(nodeCoords)} nodes from {meshFile}")


def writingOutputs(writingNodes=True, writingFixities=True, writingEqualDOFs=True, writingElements=True, outDir_="."):
    """
    Generate selected TCL output files into the target output folder.

    Parameters:
        writingNodes: bool
            Write node definition files (nodes2D.tcl, nodes3D.tcl, nodesByDOF_*.tcl)
        writingFixities: bool
            Write fixity constraint files (fixity*.tcl)
        writingEqualDOFs: bool
            Write equalDOF link files (equalDOFs*.tcl)
        writingElements: bool
            Write element definition files (elements_*.tcl)
        outDir_ (str):
            Directory path where all files will be written (default: current directory ".").
    """

    print("\n─────────────────────────────────────── Writing Outputs ───────────────────────────────────────")
    os.makedirs(outDir_, exist_ok=True)

    # NODES
    if writingNodes:
        writeNodesTcl(nodeCoords, ndmGlobal, nodeDOFs, outputDir=outDir_)
        writeSeparatedNodeFiles(nodeCoords, nodeDOFs, ndmGlobal, outputDir=outDir_)
        print("✅ Node files written.")
    else:
        print("❌ Node files skipped.")

    # FIXITIES
    if writingFixities:
        bottomNodes__ = sortNodesByX(nodesNearY(0.0, nodeCoords), nodeCoords)
        writeFixities("fixityBottom.tcl", bottomNodes__, [1, 1, 1],
                      "Bottom boundary fixities (u,v,p fixed)", outputDir=outDir_)
        print("✅ Fixity files written.")
    else:
        print("❌ Fixities skipped.")

    # EQUAL DOFs
    if writingEqualDOFs:
        leftNodes__ = sortNodesByY(nodesNearX(0.0, nodeCoords), nodeCoords)
        rightNodes__ = sortNodesByY(nodesNearX(1.0, nodeCoords), nodeCoords)
        minLen_ = min(len(leftNodes__), len(rightNodes__))
        nodePairs = list(zip(leftNodes__[:minLen_], rightNodes__[:minLen_]))
        writeEqualDOFs("equalDOFsSides.tcl", nodePairs, [1, 2],
                       "Left–Right equalDOFs for u,v", outputDir=outDir_)
        print("✅ EqualDOF files written.")
    else:
        print("❌ EqualDOFs skipped.")

    # ELEMENTS
    if writingElements:
        writeElementsTcl(elements, elementProfiles, mainSoilTags, gVal, outputDir=outDir_)
        print("✅ Element files written.")
    else:
        print("❌ Elements skipped.")

    # MODEL HEADER
    headerPath_ = os.path.join(outDir_, "modelHeader.tcl")
    with open(headerPath_, "w") as f_:
        f_.write(f"model BasicBuilder -ndm {ndmGlobal} -ndf {ndfGlobal}\n")
    # print(f"✅ modelHeader.tcl written at: {headerPath_}")

    # SUMMARY
    print("\n─────────────────────────────────────── Summary ───────────────────────────────────────")
    print(f"Nodes:        {'✅' if writingNodes else '❌'}")
    print(f"Fixities:     {'✅' if writingFixities else '❌'}")
    print(f"EqualDOFs:    {'✅' if writingEqualDOFs else '❌'}")
    print(f"Elements:     {'✅' if writingElements else '❌'}")
    print("─────────────────────────────────────────────────────────────────────────────────────────\n")
    print("✅ Selected outputs successfully written.\n")


# writeElementsTcl(elements, elementProfiles, outputDir=outDir)
# writeNodesTcl(nodeCoords, ndmGlobal, nodeDOFs, outputDir=outDir)
# writeSeparatedNodeFiles(nodeCoords, nodeDOFs, ndmGlobal, outputDir=outDir)

bottomNodes_ = nodesNearY(0.0, nodeCoords)
rightNodes_ = nodesNearX(1.0, nodeCoords)
middleNodes_ = selectNodes(lambda x_, y_, z_: 0.45 < x_ < 0.55, nodeCoords)

test1 = nodesNearY((1 / 8) * 0.5, nodeCoords)
test2 = selectNodes(lambda x2, y2, z2:
                    ((1/6)*0.5) <= x2 <= ((5/6)*0.5) and ((1/4)*0.5) <= y2 <= ((3/4)*0.5), nodeCoords)
# print(sortNodesByX(test1))

# -------------------------------------------------------
# Example: detect boundaries and apply constraints
# -------------------------------------------------------

# bottom boundary (y=0)
bottomNodes = sortNodesByX(nodesNearY(0.0, nodeCoords), nodeCoords)
# writeFixities("fixityBottom.tcl", bottomNodes, [1, 1, 1],
#               "Bottom boundary fixities (u,v,p fixed)")

# left and right boundaries (x=0, x=1)
leftNodes = sortNodesByY(nodesNearX(0.0, nodeCoords), nodeCoords)
rightNodes = sortNodesByY(nodesNearX(1.0, nodeCoords), nodeCoords)

# ensure both lists have the same length before pairing
# minLen = min(len(leftNodes), len(rightNodes))
minLen = 1
pairs = list(zip(leftNodes[:minLen], rightNodes[:minLen]))

# writeEqualDOFs("equalDOFsSides.tcl", pairs, [1, 2],
#                "Left–Right equalDOFs for u,v")

# print(leftNodes)
# for n in sortNodesByY(sortNodesByX(test2)):
#     x, y, z = nodeCoords[n]
#     print(f"{n:5d}: x={x:8.6f}, y={y:8.6f}")

# print(sortNodesByY(sortNodesByX(test2))[:9])

# xs = sorted({round(x, 6) for (x, _, _) in nodeCoords.values()})
# print(xs[:20])      # first few
# print(xs[-20:])     # last few

if __name__ == "__main__":
    writingOutputs(writingNodes=True,
                   writingFixities=False,
                   writingEqualDOFs=False,
                   writingElements=False,
                   outDir_=outDir)

    writeMainTclGlobal(
        tclRootDir="TCL-Files",
        modelName=os.path.splitext(os.path.basename(meshFile))[0],
        thickX=thickX,
        thickY=thickY,
        thickZ=thickZ
    )
