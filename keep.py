"""
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
"""

'''
Gmsh .geo generator for:
  - optional DRM layer (disabled when thickDRM = 0)
  - mandatory ASD layer
Both layers are: lateral (+/-x, +/-y) + bottom (-z), NO top (+z).

Put these in your .geo parameter section (or your .geo header you concatenate):
//+
thickASD = DefineNumber[ 0.2, Name "Parameters/thickASD" ];
//+
thickDRM = DefineNumber[ 0.0, Name "Parameters/thickDRM" ]; // 0 disables DRM
//+
x0 = 0; y0 = 0; z0 = 0;
//+
lTx = DefineNumber[ 1.0, Name "Parameters/lx" ];
lTy = DefineNumber[ 1.0, Name "Parameters/ly" ];
lTz = DefineNumber[ 1.0, Name "Parameters/lz" ];
//+
SetFactory("OpenCASCADE");
Box(1) = {x0, y0, z0, lTx, lTy, lTz};
"""


def layer_boxes_lateral_bottom(x0, y0, z0, lx, ly, lz, tVar, prefix):
    """
    Build boxes for a shell layer around [x0,x0+lx]x[y0,y0+ly]x[z0,z0+lz] with:
      - lateral faces: xMin, xMax, yMin, yMax
      - bottom face: zMin
      - NO top face

    Parameters are strings (Gmsh symbols/expressions), e.g. "x0", "(x0-thickDRM)".
    Returns: list of (label, coords_string)
    """
    t = tVar
    return [
        # faces
        (f"{prefix}_zMIN", f"{{{x0}, {y0}, ({z0}-{t}), {lx}, {ly}, {t}}}"),
        (f"{prefix}_xMIN", f"{{({x0}-{t}), {y0}, {z0}, {t}, {ly}, {lz}}}"),
        (f"{prefix}_xMAX", f"{{({x0}+{lx}), {y0}, {z0}, {t}, {ly}, {lz}}}"),
        (f"{prefix}_yMIN", f"{{{x0}, ({y0}-{t}), {z0}, {lx}, {t}, {lz}}}"),
        (f"{prefix}_yMAX", f"{{{x0}, ({y0}+{ly}), {z0}, {lx}, {t}, {lz}}}"),

        # bottom edges (with zMIN)
        (f"{prefix}_xMINzMIN", f"{{({x0}-{t}), {y0}, ({z0}-{t}), {t}, {ly}, {t}}}"),
        (f"{prefix}_xMAXzMIN", f"{{({x0}+{lx}), {y0}, ({z0}-{t}), {t}, {ly}, {t}}}"),
        (f"{prefix}_yMINzMIN", f"{{{x0}, ({y0}-{t}), ({z0}-{t}), {lx}, {t}, {t}}}"),
        (f"{prefix}_yMAXzMIN", f"{{{x0}, ({y0}+{ly}), ({z0}-{t}), {lx}, {t}, {t}}}"),

        # vertical edges (x+- with y+-), full height lz
        (f"{prefix}_xMINyMIN", f"{{({x0}-{t}), ({y0}-{t}), {z0}, {t}, {t}, {lz}}}"),
        (f"{prefix}_xMINyMAX", f"{{({x0}-{t}), ({y0}+{ly}), {z0}, {t}, {t}, {lz}}}"),
        (f"{prefix}_xMAXyMIN", f"{{({x0}+{lx}), ({y0}-{t}), {z0}, {t}, {t}, {lz}}}"),
        (f"{prefix}_xMAXyMAX", f"{{({x0}+{lx}), ({y0}+{ly}), {z0}, {t}, {t}, {lz}}}"),

        # bottom corners (x+-, y+-, zMin)
        (f"{prefix}_xMINyMINzMIN", f"{{({x0}-{t}), ({y0}-{t}), ({z0}-{t}), {t}, {t}, {t}}}"),
        (f"{prefix}_xMINyMAXzMIN", f"{{({x0}-{t}), ({y0}+{ly}), ({z0}-{t}), {t}, {t}, {t}}}"),
        (f"{prefix}_xMAXyMINzMIN", f"{{({x0}+{lx}), ({y0}-{t}), ({z0}-{t}), {t}, {t}, {t}}}"),
        (f"{prefix}_xMAX_yMAXzMIN", f"{{({x0}+{lx}), ({y0}+{ly}), ({z0}-{t}), {t}, {t}, {t}}}"),
    ]


def generate_DRM_ASD_geo(lastVolumeID=1, drm_var="thickDRM", asd_var="thickASD",
                         base_volume_id=1, use_occ_factory=False):
    """
    Generates .geo text:
      - DRM layer boxes are created only if thickDRM > 0
      - ASD layer boxes are ALWAYS created, wrapping the DRM-expanded bounds
        (which collapses to the base bounds when thickDRM = 0).

    lastVolumeID: last used Box/Volume id before adding layers (e.g., 1 if base is Volume(1))
    base_volume_id: the main domain volume id to fragment with (default 1)
    use_occ_factory: optionally emit SetFactory("OpenCASCADE");
    """
    start = lastVolumeID + 1
    lines = [
        "// Automatically generated 3D DRM + ASD boundary boxes\n",
        f"// Base volume ID: {base_volume_id}\n",
        f"// Starting new volume ID: {start}\n",
    ]
    if use_occ_factory:
        lines.append('SetFactory("OpenCASCADE");\n')
    lines.append("\n")

    next_id = start
    created_ids = []  # only what is actually instantiated (DRM, optional)

    # DRM: only when thickDRM > 0 (avoid zero-thickness boxes)
    lines.append(f"If ({drm_var} > 0)\n")
    drm_boxes = layer_boxes_lateral_bottom("x0", "y0", "z0", "lTx", "lTy", "lTz", drm_var, "DRM")
    for label, coords in drm_boxes:
        lines.append(f"  Box({next_id}) = {coords}; // {label}\n")
        created_ids.append(next_id)
        next_id += 1
    lines.append("EndIf\n\n")

    # ASD always wraps DRM-expanded bounds (symbolically)
    # If thickDRM=0, these expressions reduce to the original bounds.
    x0_eff = f"(x0 - {drm_var})"
    y0_eff = f"(y0 - {drm_var})"
    z0_eff = f"(z0 - {drm_var})"
    lx_eff = f"(lTx + 2*{drm_var})"
    ly_eff = f"(lTy + 2*{drm_var})"
    lz_eff = f"(lTz + {drm_var})"  # bottom-only expansion

    asd_boxes = layer_boxes_lateral_bottom(x0_eff, y0_eff, z0_eff, lx_eff, ly_eff, lz_eff, asd_var, "ASD")
    for label, coords in asd_boxes:
        lines.append(f"Box({next_id}) = {coords}; // {label}\n")
        created_ids.append(next_id)
        next_id += 1

    # BooleanFragments: use an explicit list (DRM may be absent)
    lines.append("\n// Coherence OR Fragment base + layer volumes\n")
    # lines.append("layerVols[] = {")
    # lines.append(",".join(str(i) for i in created_ids))
    # lines.append("};\n")
    # lines.append(f"BooleanFragments{{ Volume{{{base_volume_id}}}; Volume{{layerVols[]}}; Delete; }}{{}};\n")
    lines.append("Coherence;\n")

    return "".join(lines)


# Example usage:
if __name__ == "__main__":
    lastVolID = 1
    geoText = generate_DRM_ASD_geo(lastVolumeID=lastVolID, drm_var="thickDRM", asd_var="thickASD")
    print(geoText)
'''