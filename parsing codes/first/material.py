import abc
# =================================================================================================
#
#  Generalized Python Script for Generating OpenSees nDMaterial Commands
#  (a) for PIMY (PressureIndependMultiYield) and PDMY (PressureDependMultiYield) Materials
#  (b) will be adding other materials progressively
#
#  Instructions:
#  1. Define default parameters in the `GLOBAL_PARAMS` dictionary. These will be used for all
#     layers unless overridden in a specific layer's definition;
#  2. Define your soil stratigraphy in the `SOIL_LAYERS_DEFINITION` list. Each item in the
#     list is a dictionary representing a layer;
#  3. You can override any global parameter by adding it to a layer's dictionary;
#  4. Run the script. It will generate 'materials.tcl' and 'updateMat.tcl' in the same directory.
#
# =================================================================================================


class Material(abc.ABC):
    """
    abstract base class for a material model:
        - notice that the parameters defined below are the same for both PDMY and PIMY
        - layerTag, nd, rho, refShearModul (gMod), and refBulkModul (bulkMod)
    """
    def __init__(self, layerTag, params):
        self.layerTag = layerTag
        self.nd = params.get("nd", 2)
        self.rho = params["rho"]
        self.gMod = params["gMod"]
        self.bulkMod = params["bulkMod"]

    @abc.abstractmethod
    def toTCL(self):
        """
        returns the nDMaterial command string for the material
        """
        pass


class PdmyMaterial(Material):
    """
    specific parameters for the PressureDependMultiYield material (see OpenSees wiki for more info):
    """
    def __init__(self, layerTag, params):
        super().__init__(layerTag, params)
        self.phi = params["phi"]
        self.gammaPeak = params.get("gammaPeak", 0.1)
        self.refPress = params.get("refPress", 101.3)
        self.pressCoef = params.get("pressCoef", 0.5)
        self.phaseAng = params.get("phaseAng", 27.0)
        self.contract = params.get("contract", 0.06)
        self.dilate1 = params.get("dilate1", 0.5)
        self.dilate2 = params.get("dilate2", 2.5)
        self.liq1 = params.get("liq1", 0.0)
        self.liq2 = params.get("liq2", 0.0)
        self.liq3 = params.get("liq3", 0.0)
        self.numYield = params.get("numYieldPDMY", 16)

    def toTCL(self):
        return (f"nDMaterial PressureDependMultiYield {self.layerTag} {self.nd} {self.rho} {self.gMod:.4f} "
                f"{self.bulkMod:.4f} {self.phi} {self.gammaPeak} {self.refPress} {self.pressCoef} "
                f"{self.phaseAng} {self.contract} {self.dilate1} {self.dilate2} {self.liq1} {self.liq2} "
                f"{self.liq3} {self.numYield}")


class PimyMaterial(Material):
    """
    for the PressureIndependMultiYield material
    """
    def __init__(self, layerTag, params):
        super().__init__(layerTag, params)
        self.cohesion = params["cohesion"]
        self.phi = params.get("phi", 0.0)
        self.gammaPeak = params.get("gammaPeak", 0.1)
        self.refPress = params.get("refPress", 101.3)
        self.pressCoef = params.get("pressCoef", 0.0)
        self.modReductCurve = params["modulusReductionCurve"]

    def toTCL(self):
        numYield = len(self.modReductCurve)
        curveStr = " ".join([f"{gamma} {gRatio}" for gamma, gRatio in self.modReductCurve])
        return (
            f"nDMaterial PressureIndependMultiYield {self.layerTag} {self.nd} {self.rho} {self.gMod:.4f} "
            f"{self.bulkMod:.4f} {self.cohesion} {self.gammaPeak} {self.phi} {self.refPress} "
            f"{self.pressCoef} -{numYield} {curveStr}"
        )


class Layer:
    """
    represents a single soil layer
    """
    def __init__(self, layerTag, layerData, globalParams):
        self.layerTag = layerTag
        self.name = layerData.get("name", f"Layer-{layerTag}")

        # combine global and layer-specific parameters
        params = {**globalParams, **layerData}

        # basic properties
        self.thickness = params["thickness"]
        self.vs = params["vs"]
        self.rho = params["rho"]
        self.nu = params["nu"]

        # calculated properties
        params["gMod"] = self.rho * self.vs ** 2
        params["bulkMod"] = (2 * params["gMod"] * (1 + self.nu)) / (3 * (1 - 2 * self.nu))

        # material instantiation
        materialType = params.get("materialType", "PDMY").upper()
        if materialType == "PDMY":
            self.material = PdmyMaterial(self.layerTag, params)
        elif materialType == "PIMY":
            self.material = PimyMaterial(self.layerTag, params)
        else:
            raise ValueError(f"Unknown material type '{materialType}' for layer {self.layerTag}")

    def getMaterialTCL(self):
        return self.material.toTCL()


class SoilProfile:
    """
    manages the entire soil profile and file generation.
    """
    def __init__(self, layersDefinition, globalParams):
        self.layers = []
        for i, layerDef in enumerate(layersDefinition, 1):
            layer = Layer(i, layerDef, globalParams)
            self.layers.append(layer)

    def generate_tcl_files(self, materialsFile="materials.tcl", updateMatFile="updateMat.tcl"):
        # generate materials.tcl
        with open(materialsFile, 'w') as f:
            f.write("# Generated nDMaterial definitions for the soil profile\n\n")
            for layer in self.layers:
                f.write(f"# Material for {layer.name}\n")
                f.write(f"{layer.getMaterialTCL()} \
")
                f.write("\n")
        print(f"Successfully generated '{materialsFile}'")

        # generate updateMat.tcl
        with open(updateMatFile, 'w') as f:
            f.write("# Generated updateMaterialStage commands\n\n")
            for layer in self.layers:
                f.write(f"updateMaterialStage -material {layer.layerTag} -stage 1\n")
        print(f"Successfully generated '{updateMatFile}'")


# =================================================================================================
#
#                                      USER INPUT SECTION
#
# =================================================================================================

if __name__ == "__main__":

    # 1. DEFINE GLOBAL PARAMETERS,
    # These parameters will be applied to all layers unless overridden in a specific layer's definition.
    GLOBAL_PARAMS = {
        "rho": 2.202,
        "nu": 0.0,
        # Default to PDMY material properties
        "materialType": "PDMY",
        "phi": 35.0,
        "gammaPeak": 0.1,
        "refPress": 80.0,
        "pressCoef": 0.0,
        "phaseAng": 27.0,
        "contract": 0.06,
        "dilate1": 0.5,
        "dilate2": 2.5,
        "liq1": 0.0,
        "liq2": 0.0,
        "liq3": 0.0,
    }

    # 2. DEFINE SOIL LAYERS
    # Each dictionary represents a layer. It must have 'thickness' and 'vs';
    # Other parameters can be added to override the GLOBAL_PARAMS for that specific layer...
    soilLayersDefinition = [
        {"name": "PIMY Layer 1", "thickness": 1.0, "vs": 170.9, "materialType": "PIMY", "cohesion": 95.0,
         "modulusReductionCurve": [
             (1.00e-6, 1.000), (2.00e-6, 1.000), (5.00e-6, 0.996), (1.00e-5, 0.984),
             (2.00e-5, 0.975), (5.00e-5, 0.922), (1.00e-4, 0.850), (2.00e-4, 0.734),
             (5.00e-4, 0.532), (1.00e-3, 0.367), (2.00e-3, 0.224), (5.00e-3, 0.139),
             (1.00e-2, 0.085), (2.00e-2, 0.051), (5.00e-2, 0.027), (1.00e-1, 0.021)
         ]},
    ]
    """
    soilLayersDefinition = [
        # Top 5 layers as PIMY material (example)
        {"name": "PIMY Layer 1", "thickness": 1.0, "vs": 170.9, "materialType": "PIMY", "cohesion": 95.0,
         "modulusReductionCurve": [
             (1.00e-6, 1.000), (2.00e-6, 1.000), (5.00e-6, 0.996), (1.00e-5, 0.984),
             (2.00e-5, 0.975), (5.00e-5, 0.922), (1.00e-4, 0.850), (2.00e-4, 0.734),
             (5.00e-4, 0.532), (1.00e-3, 0.367), (2.00e-3, 0.224), (5.00e-3, 0.139),
             (1.00e-2, 0.085), (2.00e-2, 0.051), (5.00e-2, 0.027), (1.00e-1, 0.021)
         ]},
        {"name": "PIMY Layer 2", "thickness": 1.0, "vs": 224.9, "materialType": "PIMY", "cohesion": 105.0,
         "modulusReductionCurve": [
             (1.00e-6, 1.000), (2.00e-6, 1.000), (5.00e-6, 0.996), (1.00e-5, 0.984),
             (2.00e-5, 0.975), (5.00e-5, 0.922), (1.00e-4, 0.850), (2.00e-4, 0.734),
             (5.00e-4, 0.532), (1.00e-3, 0.367), (2.00e-3, 0.224), (5.00e-3, 0.139),
             (1.00e-2, 0.085), (2.00e-2, 0.051), (5.00e-2, 0.027), (1.00e-1, 0.021)
         ]},
        {"name": "PIMY Layer 3", "thickness": 1.0, "vs": 255.6, "materialType": "PIMY", "cohesion": 115.0,
         "modulusReductionCurve": [
             (1.00e-6, 1.000), (2.00e-6, 1.000), (5.00e-6, 0.996), (1.00e-5, 0.984),
             (2.00e-5, 0.975), (5.00e-5, 0.922), (1.00e-4, 0.850), (2.00e-4, 0.734),
             (5.00e-4, 0.532), (1.00e-3, 0.367), (2.00e-3, 0.224), (5.00e-3, 0.139),
             (1.00e-2, 0.085), (2.00e-2, 0.051), (5.00e-2, 0.027), (1.00e-1, 0.021)
         ]},
        {"name": "PIMY Layer 4", "thickness": 1.0, "vs": 278.0, "materialType": "PIMY", "cohesion": 125.0,
         "modulusReductionCurve": [
             (1.00e-6, 1.000), (2.00e-6, 1.000), (5.00e-6, 0.996), (1.00e-5, 0.984),
             (2.00e-5, 0.975), (5.00e-5, 0.922), (1.00e-4, 0.850), (2.00e-4, 0.734),
             (5.00e-4, 0.532), (1.00e-3, 0.367), (2.00e-3, 0.224), (5.00e-3, 0.139),
             (1.00e-2, 0.085), (2.00e-2, 0.051), (5.00e-2, 0.027), (1.00e-1, 0.021)
         ]},
        {"name": "PIMY Layer 5", "thickness": 1.0, "vs": 296.0, "materialType": "PIMY", "cohesion": 135.0,
         "modulusReductionCurve": [
             (1.00e-6, 1.000), (2.00e-6, 1.000), (5.00e-6, 0.996), (1.00e-5, 0.984),
             (2.00e-5, 0.975), (5.00e-5, 0.922), (1.00e-4, 0.850), (2.00e-4, 0.734),
             (5.00e-4, 0.532), (1.00e-3, 0.367), (2.00e-3, 0.224), (5.00e-3, 0.139),
             (1.00e-2, 0.085), (2.00e-2, 0.051), (5.00e-2, 0.027), (1.00e-1, 0.021)
         ]},

        # remaining layers as PDMY material (default) ---
        # the 'materialType' is not specified, so it will use the default from GLOBAL_PARAMS.
        {"name": "PDMY Layer 6", "thickness": 1.0, "vs": 311.3},
        {"name": "PDMY Layer 7", "thickness": 1.0, "vs": 324.5},
        {"name": "PDMY Layer 8", "thickness": 1.0, "vs": 336.4},
        {"name": "PDMY Layer 9", "thickness": 1.0, "vs": 347.0},
        {"name": "PDMY Layer 10", "thickness": 1.0, "vs": 356.8},
        {"name": "PDMY Layer 11", "thickness": 1.0, "vs": 365.9},
        {"name": "PDMY Layer 12", "thickness": 1.0, "vs": 374.3},
        {"name": "PDMY Layer 13", "thickness": 1.0, "vs": 382.2},
        {"name": "PDMY Layer 14", "thickness": 1.0, "vs": 389.6},
        {"name": "PDMY Layer 15", "thickness": 1.0, "vs": 396.6},
        {"name": "PDMY Layer 16", "thickness": 1.0, "vs": 403.3},
        {"name": "PDMY Layer 17", "thickness": 1.0, "vs": 409.6},
        {"name": "PDMY Layer 18", "thickness": 1.0, "vs": 415.7},
        {"name": "PDMY Layer 19", "thickness": 1.0, "vs": 421.5},
        {"name": "PDMY Layer 20", "thickness": 1.0, "vs": 427.1},
        {"name": "PDMY Layer 21", "thickness": 1.0, "vs": 432.5},
        {"name": "PDMY Layer 22", "thickness": 1.0, "vs": 437.7},
        {"name": "PDMY Layer 23", "thickness": 1.0, "vs": 442.7},
        {"name": "PDMY Layer 24", "thickness": 1.0, "vs": 447.5},
        {"name": "PDMY Layer 25", "thickness": 1.0, "vs": 452.2},
        {"name": "PDMY Layer 26", "thickness": 1.0, "vs": 456.7},
        {"name": "PDMY Layer 27", "thickness": 1.0, "vs": 461.2},
        {"name": "PDMY Layer 28", "thickness": 1.0, "vs": 465.4},
        {"name": "PDMY Layer 29", "thickness": 1.0, "vs": 469.6},
        {"name": "PDMY Layer 30", "thickness": 1.0, "vs": 473.7, "phi": 40.0},  # example of overriding one param
    ]
    """

    # 3. CREATE THE SOIL PROFILE AND GENERATE TCL FILES
    try:
        soil_profile = SoilProfile(soilLayersDefinition, GLOBAL_PARAMS)
        soil_profile.generate_tcl_files()
    except KeyError as e:
        print(f"ERROR: A required parameter is missing. Please check your definitions. Missing key: {e}")
    except ValueError as e:
        print(f"ERROR: {e}")
