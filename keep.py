# !!!!----
# !!!!!!!!!!!!!!!!!!!!!!!!!!!! SELECTING A GROUP OF NODES IN A UNION MANNER !!!!!!!!!!!!!!!!!!!!!!!!!!!!
masterNodes = sortNodesByY(getBoundaryNodesFromMsh(meshFile, phyGroupID=4, dim=1) |
                           getBoundaryNodesFromMsh(meshFile, phyGroupID=15, dim=1) |
                           getBoundaryNodesFromMsh(meshFile, phyGroupID=23, dim=1), nodeCoords)
slaveNodes1 = sortNodesByY(getBoundaryNodesFromMsh(meshFile, phyGroupID=2, dim=1) |
                           getBoundaryNodesFromMsh(meshFile, phyGroupID=13, dim=1) |
                           getBoundaryNodesFromMsh(meshFile, phyGroupID=21, dim=1), nodeCoords)
slaveNodes2 = sortNodesByY(getBoundaryNodesFromMsh(meshFile, phyGroupID=6, dim=1) |
                           getBoundaryNodesFromMsh(meshFile, phyGroupID=16, dim=1) |
                           getBoundaryNodesFromMsh(meshFile, phyGroupID=24, dim=1), nodeCoords)
slaveNodes3 = sortNodesByY(getBoundaryNodesFromMsh(meshFile, phyGroupID=8, dim=1) |
                           getBoundaryNodesFromMsh(meshFile, phyGroupID=18, dim=1) |
                           getBoundaryNodesFromMsh(meshFile, phyGroupID=26, dim=1), nodeCoords)
# !!!!----


# outputPath = os.path.join(outDir, 'leftASDUpdate.tcl')
#
# with open(outputPath, 'w') as f:
#     for i in leftASDElements:
#         f.write(f"setParameter -val 1 -ele {i} stage\n")


# -------------------------------------------------------------------------------------------------------------------
# automatic soil group detection
# -------------------------------------------------------------------------------------------------------------------
soil2D_types = {3, 10, 103, 1003}
soil3D_types = {5, 17, 105, 1005, 1055}
soilTypes = soil3D_types if has3D else soil2D_types

# extract only soil groups from the mesh
soilGroups = {el["group"] for el in elements if el["type"] in soilTypes}

# -------------------------------------------------------------------------------------------------------------------
# !!! node sets for soil and structure (for SSI purposes) !!!
# all nodes that belong to soil elements
soilNodeSet = {n for el in elements if el["type"] in soilTypes for n in el["nodes"]}

# elements that are 3D beams (piles) – using physical groups in beam3DGrp
pileElemts = [el for el in elements if el["type"] == 101 and el["group"] in beam3DGrp]

# node set on piles
pileNodeSet = {n for el in pileElemts for n in el["nodes"]}
# -------------------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------------------
# Filter out and remap elements based on dimensionality and groups
# -------------------------------------------------------------------------------------------------------------------
elements, has3D = filterElementsByDIM(elements, beam2DGrp, beam3DGrp)
groupSets = {
    "beam2DGrp": beam2DGrp, "beam3DGrp": beam3DGrp, "bbarQuadUPGrp": bbarQuadUPGrp, "quadUPGrp": quadUPGrp,
    "bbarBrickUPGrp": bbarBrickUPGrp, "sspBrickUPGrp": sspBrickUPGrp, "sspBrickGrp": sspBrickGrp,
    "ASDLeftGrp": ASDLeftGrp, "ASDBottomGrp": ASDBottomGrp, "ASDRightGrp": ASDRightGrp,
    "ASDBottomLeftGrp": ASDBottomLeftGrp, "ASDBottomRightGrp": ASDBottomRightGrp, "ASD3DBGrp": ASD3DBGrp,
    "ASD3DLGrp": ASD3DLGrp, "ASD3DRGrp": ASD3DRGrp, "ASD3DKGrp": ASD3DKGrp, "ASD3DFGrp": ASD3DFGrp,
    "ASD3DBLGrp": ASD3DBLGrp, "ASD3DBRGrp": ASD3DBRGrp, "ASD3DBKGrp": ASD3DBKGrp, "ASD3DBFGrp": ASD3DBFGrp,
    "ASD3DLKGrp": ASD3DLKGrp, "ASD3DBLKGrp": ASD3DBLKGrp, "ASD3DRKGrp": ASD3DRKGrp, "ASD3DBRKGrp": ASD3DBRKGrp,
    "ASD3DLFGrp": ASD3DLFGrp, "ASD3DBLFGrp": ASD3DBLFGrp, "ASD3DRFGrp": ASD3DRFGrp, "ASD3DBRFGrp": ASD3DBRFGrp
}

# !!!!----
# select some particular group of nodes
phyGroupID = 29
boundaryNodes = getBoundaryNodesFromMsh(meshFile, phyGroupID=phyGroupID, dim=1)  # for example
boundaryNodes = sortNodesByZ(sortNodesByY(sortNodesByX(boundaryNodes, nodeCoords), nodeCoords), nodeCoords)
# print(f"Test nodes: {sortNodesByX(sortNodesByY(sortNodesByX(boundaryNodes, nodeCoords), nodeCoords), nodeCoords)}")
# !!!!----

# !!!!----
# (1)
# select some particular group of nodes w.r.t. the DOF
dofOfSelectedNodes = 3
selectNodesDOF = classifyChosenNodesByDOF(boundaryNodes, nodeDOFs)
boundaryNodes3DOFs = selectNodesDOF.get(dofOfSelectedNodes, [])

# (2)
leftNodesT = getBoundaryNodesFromMsh(meshFile, phyGroupID=4, dim=1)
nodesDOFsLeftNodesT = classifyChosenNodesByDOF(leftNodesT, nodeDOFs)
# now extract 3-DOFs nodes
nodes3DOFsLeftNodesT = nodesDOFsLeftNodesT.get(3, [])
# print(nodes3DOFsLeftNodesT)

# now extract 2-DOFs nodes
nodes2DOFsLeftNodesT = nodesDOFsLeftNodesT.get(2, [])
# print(nodes2DOFsLeftNodesT)
# !!!!----

# !!!!----
tryNodes = selectNodes(lambda x, y, z: x == 0.125, nodeCoords)
# !!!!----

# maxPhyGroup = detectMaxPhyGroup(meshFile)
# mainSoilTags = {i: i for i in range(1, maxPhyGroup + 1)} # auto-build physical group tags based on mesh content

# soil nodes
if nodeDOFs_soil:
    # writeNodesTcl(nodeCoords, ndmGlobal, nodeDOFs_soil, filePrefix="AllSoilNodes", outputDir=outDir)
    writeSeparatedNodeFiles(nodeCoords, nodeDOFs_soil, ndmGlobal, outputDir=outDir, labelPrefix="soil")
#
# structure nodes
if nodeDOFs_struct:
    # writeNodesTcl(nodeCoords, ndmGlobal, nodeDOFs_struct, filePrefix="structure_nodes", outputDir=outDir)
    writeSeparatedNodeFiles(nodeCoords, nodeDOFs_struct, ndmGlobal, outputDir=outDir, labelPrefix="structure")


# -------------------------------------------------------------------------------------------------------------------
# automatic soil group detection
# -------------------------------------------------------------------------------------------------------------------
soilTypes, soilGroups = detectSoilGroups(elements, has3D)
soilNodeSet, pileNodeSet = classifySoilAndPileNodes(elements, soilTypes, beam3DGrp)
# -------------------------------------------------------------------------------------------------------------------
