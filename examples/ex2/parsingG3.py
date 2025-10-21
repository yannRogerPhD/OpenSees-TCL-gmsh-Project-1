import os

from meshHelper import (
    outputFolder, FuzzyFloat, defaultTolerance, _roundFunc, nodesNearX, nodesNearY, nodesNearZ,  # noqa: F401
    selectNodes, sortNodesByX, sortNodesByY, sortNodesByZ, writeFixities, writeEqualDOFs, writeNodesTcl,  # noqa: F401
    writeSeparatedNodeFiles, writeElementsTcl, writeMainTclGlobal, parseElementsFromMsh, parseNodesFromMsh,
    detectMaxPhyGroup, getBoundaryNodesFromMsh, writeSeparatedFixities,  # noqa: F401
    only2DOFs, both2and3DOFs, threeDOFs, fourDOFs3D, twentyEightBrickDOFs, elementProfiles  # noqa: F401
)

# noqa: F401
meshFile = "model.msh"

# basic geometry setup
transX, transY, transZ = 2, 2, 2
xMin, xMax = 0.0, 1.0
yMin, yMax = 0.0, 1.0
zMin, zMax = 0.0, 1.0

# time series in both directions
tsX = 1
tsY = 2

# compute the thickness increments
thickX = (xMax - xMin) / (transX - 1)
thickY = (yMax - yMin) / (transY - 1)
thickZ = (zMax - zMin) / (transZ - 1)

# prepare output folder once
outDir = outputFolder(meshFile)

sspBrickGrp, bbarQuadUPGrp, quadUPGrp, bbarBrickGrp = {}, {}, {}, {}
# sspBrickGrp = {1, 2, 3}, bbarBrickGrp = {} is for volumes instead

ASDLeftGrp, ASDBottomGrp, ASDRightGrp, ASDBottomLeftGrp, ASDBottomRightGrp = {}, {}, {}, {}, {}

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

    # general 2D elements
    if el["type"] == 3:
        if el["group"] in bbarQuadUPGrp:
            el["type"] = 103  # 2D bbarQuadUP
        elif el["group"] in quadUPGrp:
            el["type"] = 1003  # 2D quadUP

        # 2D ASD absorbing boundaries
        elif el["group"] in ASDLeftGrp:
            el["type"] = 10031
        elif el["group"] in ASDBottomGrp:
            el["type"] = 10032
        elif el["group"] in ASDRightGrp:
            el["type"] = 10033
        elif el["group"] in ASDBottomLeftGrp:
            el["type"] = 10034
        elif el["group"] in ASDBottomRightGrp:
            el["type"] = 10035

    # general 3D elements
    elif el["type"] == 5 and el["group"] in bbarBrickGrp:
        el["type"] = 105  # 3D bbarBrickUP

    elif el["type"] == 5 and el["group"] in sspBrickGrp:
        el["type"] = 1005  # 3D SSPbrickUP

# summary mappings 2D
mappedBbar = sum(el["type"] == 103 for el in elements)
mappedQuadUP = sum(el["type"] == 1003 for el in elements)
mappedASDLeft = sum(el["type"] == 10031 for el in elements)
mappedASDBottom = sum(el["type"] == 10032 for el in elements)
mappedASDRight = sum(el["type"] == 10033 for el in elements)
mappedASDBottomLeft = sum(el["type"] == 10034 for el in elements)
mappedASDBottomRight = sum(el["type"] == 10035 for el in elements)

# summary mappings 3D
mappedBbarBrickUP = sum(el["type"] == 105 for el in elements)
mappedSSPBrickUP = sum(el["type"] == 1005 for el in elements)

if mappedBbar:
    print(f"Remapped {mappedBbar} elements → bbarQuadUP (103)")
if mappedQuadUP:
    print(f"Remapped {mappedQuadUP} elements → quadUP (1003)")
if mappedASDLeft:
    print(f"Remapped {mappedASDLeft} elements → ASDAbsorbingBoundary Left (10031)")
if mappedASDBottom:
    print(f"Remapped {mappedASDBottom} elements → ASDAbsorbingBoundary Bottom (10032)")
if mappedASDRight:
    print(f"Remapped {mappedASDRight} elements → ASDAbsorbingBoundary Right (10033)")
if mappedASDBottomLeft:
    print(f"Remapped {mappedASDBottomLeft} elements → ASDAbsorbingBoundary BottomLeft (10034)")
if mappedASDBottomRight:
    print(f"Remapped {mappedASDBottomRight} elements → ASDAbsorbingBoundary BottomRight (10035)")

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

# ============================================================
# Write main TCL files
# ============================================================

print("\n─────────────────────────────────────── Writing Outputs ───────────────────────────────────────")
os.makedirs(outDir, exist_ok=True)

# nodes
writeNodesTcl(nodeCoords, ndmGlobal, nodeDOFs, outputDir=outDir)
writeSeparatedNodeFiles(nodeCoords, nodeDOFs, ndmGlobal, outputDir=outDir)
print("✅ Node files written.")

# elements
writeElementsTcl(elements, elementProfiles, mainSoilTags, gVal, outputDir=outDir)
print("✅ Element files written.")

# model header
headerPath_ = os.path.join(outDir, "modelHeader.tcl")
with open(headerPath_, "w") as f_:
    f_.write(f"model BasicBuilder -ndm {ndmGlobal} -ndf {ndfGlobal}\n")
print(f"✅ modelHeader.tcl written at: {headerPath_}")

print("───────────────────────────────────────────────────────────────────────────────────────────────")
print("✅ Essential outputs successfully written.\n")

# ============================================================
# Guides: Defining boundaries and constraints (examples)
# ============================================================

# Example 1 — Define bottom fixities
# ------------------------------------------------------------
# bottomNodes = sortNodesByX(nodesNearY(0.0, nodeCoords), nodeCoords)
# writeFixities("fixityBottom.tcl", bottomNodes, [1,1,1],
#               "Bottom boundary fixities (u,v,p fixed)", outputDir=outDir)


# Example 2 — Define left-right equalDOFs (u,v)
# ------------------------------------------------------------
# leftNodes = sortNodesByY(nodesNearX(0.0, nodeCoords), nodeCoords)
# rightNodes = sortNodesByY(nodesNearX(1.0, nodeCoords), nodeCoords)
# nodePairs = list(zip(leftNodes, rightNodes))
# writeEqualDOFs("equalDOFsSides.tcl", nodePairs, [1, 2],
#                "Left–Right equalDOFs for u,v", outputDir=outDir)


# Example 3 — Apply constraints on custom regions
# ------------------------------------------------------------
# centerNodes = selectNodes(lambda x, y, z: (0.2 < x < 0.3) and (0.1 < y < 0.2), nodeCoords)
# writeFixities("fixityCenter.tcl", centerNodes, [1,1,0],
#               "Center patch fixities (u,v fixed)", outputDir=outDir)


# Example 4 — Define constraints using surfaces
# ------------------------------------------------------------
# surfaceA = selectNodes(lambda x, y, z: y == 0.0, nodeCoords)
# surfaceB = selectNodes(lambda x, y, z: y == 0.5, nodeCoords)
# surfacePairs = list(zip(surfaceA, surfaceB))
# writeEqualDOFs("equalDOFs_SurfaceAB.tcl", surfacePairs, [1,2],
#                "Surface–Surface equalDOFs", outputDir=outDir)


# Example 5 — Define vertical or inclined boundaries
# ------------------------------------------------------------
# inclined = selectNodes(lambda x, y, z: abs(y - 2*x) < 1e-4, nodeCoords)
# writeFixities("fixityInclined.tcl", inclined, [1,1,1],
#               "Inclined boundary fixities", outputDir=outDir)

if __name__ == "__main__":
    writeMainTclGlobal(
        tclRootDir="TCL-Files",
        modelName=os.path.splitext(os.path.basename(meshFile))[0],
        thickX=thickX,
        thickY=thickY,
        thickZ=thickZ,
        tsX=tsX,
        tsY=tsY
    )

phyGroupID = 1
boundaryNodes = getBoundaryNodesFromMsh(meshFile, phyGroupID=phyGroupID, dim=2)  # for example
boundaryNodes = sortNodesByZ(sortNodesByY(sortNodesByX(boundaryNodes, nodeCoords), nodeCoords), nodeCoords)
print(f"Boundary nodes: {boundaryNodes}")

fixValuesPerDOF = {
    2: [1, 1],  # u,v fixed
    3: [1, 1, 1],  # u,v,p fixed
    4: [1, 1, 1, 1]  # u,v,w,p fixed
}

# write for the chosen subset
writeSeparatedFixities(boundaryNodes, nodeDOFs, fixValuesPerDOF,
                       outputDir=outDir, filePrefix="fixity_bottom")
