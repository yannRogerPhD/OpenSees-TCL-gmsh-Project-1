import abc


# update material to stage 0 or stage 1?
stage = 0


class Material(abc.ABC):
    # abstract base class for a material model
    def __init__(self, layerTag, params):
        self.layerTag = layerTag
        self.params = params
        self.nd = params.get("nd", 2)
        self.rho = params["rho"]
        self.refShearModul = params["refShearModul"]
        self.refBulkModul = params["refBulkModul"]

    @abc.abstractmethod
    def toTCL(self):
        # returns the nDMaterial command string for the material.
        pass

    def validateParams(self, requiredKeys):
        # checks if all required keys are present in the params dictionary
        for key in requiredKeys:
            if key not in self.params:
                raise ValueError(f"Missing required parameter '{key}' for layer {self.layerTag}")


class PdmyMaterial(Material):
    # for PressureDependMultiYield material
    def toTCL(self):
        if "modulusReductionCurve" in self.params:
            # mode: User-defined backbone curve
            required = ["rho", "refShearModul", "refBulkModul", "phi", "gammaPeak", "refPress",
                        "modulusReductionCurve"]
            self.validateParams(required)

            curve = self.params["modulusReductionCurve"]
            numYield = len(curve)
            curveStr = " ".join([f"{gamma} {gRatio}" for gamma, gRatio in curve])
            return (
                f"nDMaterial PressureDependMultiYield {self.layerTag} {self.nd} {self.rho} {self.refShearModul:.4f} "
                f"{self.refBulkModul:.4f} {self.params['phi']} {self.params['gammaPeak']} "
                f"{self.params['refPress']} -{numYield} {curveStr}")
        else:
            # Mode: Automatic backbone generation
            required = ["rho", "refShearModul", "refBulkModul", "phi", "gammaPeak", "refPress", "pressCoef",
                        "phaseAng",
                        "contract", "dilate1", "dilate2", "liq1", "liq2", "liq3"]
            self.validateParams(required)

            return (
                f"nDMaterial PressureDependMultiYield {self.layerTag} {self.nd} {self.rho} {self.refShearModul:.4f} "
                f"{self.refBulkModul:.4f} {self.params['phi']} {self.params['gammaPeak']} "
                f"{self.params['refPress']} {self.params['pressCoef']} {self.params['phaseAng']} "
                f"{self.params['contract']} {self.params['dilate1']} {self.params['dilate2']} "
                f"{self.params['liq1']} {self.params['liq2']} {self.params['liq3']} "
                f"{self.params.get('numYield', 20)}")


class PimyMaterial(Material):
    """
    represents the PressureIndependMultiYield material
    """

    def toTCL(self):
        if "modulusReductionCurve" in self.params:
            # Mode: User-defined backbone curve
            required = ["rho", "refShearModul", "refBulkModul", "cohesion", "gammaPeak", "phi", "refPress",
                        "pressCoef", "modulusReductionCurve"]
            self.validateParams(required)

            curve = self.params["modulusReductionCurve"]
            numYield = len(curve)
            curveStr = " ".join([f"{gamma} {gRatio}" for gamma, gRatio in curve])
            return (
                f"nDMaterial PressureIndependMultiYield {self.layerTag} {self.nd} {self.rho} {self.refShearModul:.4f} "
                f"{self.refBulkModul:.4f} {self.params['cohesion']} {self.params['gammaPeak']} "
                f"{self.params['phi']} {self.params['refPress']} "
                f"{self.params['pressCoef']} -{numYield} {curveStr}")
        else:
            # Mode: Automatic backbone generation
            required = ["rho", "refShearModul", "refBulkModul", "cohesion", "gammaPeak", "phi", "refPress",
                        "pressCoef"]
            self.validateParams(required)
            return (
                f"nDMaterial PressureIndependMultiYield {self.layerTag} {self.nd} {self.rho} {self.refShearModul:.4f} "
                f"{self.refBulkModul:.4f} {self.params['cohesion']} {self.params['gammaPeak']} "
                f"{self.params['phi']} {self.params['refPress']} "
                f"{self.params['pressCoef']} {self.params.get('numYield', 20)}")


class Layer:
    # for a single soil layer
    def __init__(self, layerTag, layerData):
        self.layerTag = layerTag
        self.name = layerData.get("name", f"Layer-{layerTag}")

        params = layerData

        # Basic properties required for all materials
        if not all(k in params for k in ["rho", "refShearModul", "refBulkModul"]):
            raise ValueError(
                f"Layer {self.layerTag} "
                f"is missing one of the basic required keys: 'rho', 'refShearModul', or 'refBulkModul'.")

        # Material instantiation
        materialType = params.get("materialType")
        if not materialType:
            raise ValueError(f"Missing required parameter 'materialType' for layer {self.layerTag}")

        if materialType.upper() == "PDMY":
            self.material = PdmyMaterial(self.layerTag, params)
        elif materialType.upper() == "PIMY":
            self.material = PimyMaterial(self.layerTag, params)
        else:
            raise ValueError(f"Unknown material type '{materialType}' for layer {self.layerTag}")

    def getMaterialTCL(self):
        return self.material.toTCL()


class SoilProfile:
    # manages the entire soil profile and file generation
    def __init__(self, layersDefinition):
        self.layers = []
        for i, layerDef in enumerate(layersDefinition, 1):
            layer = Layer(i, layerDef)
            self.layers.append(layer)

    def generateTCLFiles(self, materialsFile="materials.tcl", updateMatFile="updateMat.tcl"):
        with open(materialsFile, 'w') as f:
            f.write("# Generated nDMaterial definitions for the soil profile\n\n")
            for layer in self.layers:
                f.write(f"# Material for {layer.name}\n")
                f.write(f"{layer.getMaterialTCL()}" + " \n")
                f.write("\n")
        print(f"Successfully generated '{materialsFile}'")

        with open(updateMatFile, 'w') as f:
            f.write("# Generated updateMaterialStage commands\n\n")
            for layer in self.layers:
                f.write(f"updateMaterialStage -material {layer.layerTag} -stage {stage}\n")
        print(f"Successfully generated '{updateMatFile}'")


# =================================================================================================
#
#                                      USER INPUT SECTION
#
# =================================================================================================

if __name__ == "__main__":

    # DEFINE EXAMPLE MODULUS REDUCTION CURVE (for convenience)
    modReductionCurve = [
        (1.00e-6, 1.000), (2.00e-6, 0.999), (5.00e-6, 0.998), (1.00e-5, 0.995),
        (2.00e-5, 0.985), (5.00e-5, 0.955), (1.00e-4, 0.905), (2.00e-4, 0.815),
        (5.00e-4, 0.635), (1.00e-3, 0.475), (2.00e-3, 0.325), (5.00e-3, 0.185),
        (1.00e-2, 0.115), (2.00e-2, 0.075), (5.00e-2, 0.045), (1.00e-1, 0.030)
    ]

    E1, poisson1 = 90000, 0.40
    G1 = E1 / (2 * (1 + poisson1))
    K1 = E1 / (3 * (1 - 2 * poisson1))
    cohesion = 30
    peakShearStrain = 0.1

    phiRef, refPressRef, pressCoefRef = 0.0, 100.0, 0.0
    # DEFINE SOIL LAYERS
    # Each dictionary MUST be a complete definition for the material.
    soilLayersDefinition = [
        {
            "name": "Layer 1",
            "materialType": "PIMY",
            "rho": 2.000,
            "refShearModul": G1,
            "refBulkModul": K1,
            "cohesion": cohesion,
            "gammaPeak": peakShearStrain,
            "phi": phiRef,
            "refPress": refPressRef,
            "pressCoef": pressCoefRef
        },
        # {
        #     "name": "directInputPDMYLayer",
        #     "materialType": "PDMY",
        #     "rho": 2.0,
        #     "refShearModul": 80000.0,
        #     "refBulkModul": 133333.3,
        #     "phi": 30.0,
        #     "gammaPeak": 0.1,
        #     "refPress": 101.3,
        #     "pressCoef": 0.5,
        #     "phaseAng": 25.0,
        #     "contract": 0.05,
        #     "dilate1": 0.1,
        #     "dilate2": 2.0,
        #     "liq1": 0.0, "liq2": 0.0, "liq3": 0.0,
        #     "numYield": 20
        # },
        # {
        #     "name": "directInputPIMYLayerWithCurve",
        #     "materialType": "PIMY",
        #     "rho": 1.8,
        #     "refShearModul": 58320.0,
        #     "refBulkModul": 97200.0,
        #     "cohesion": 60.0,
        #     "gammaPeak": 0.08,
        #     "phi": 0.0,
        #     "refPress": 101.3,
        #     "pressCoef": 0.0,
        #     "modulusReductionCurve": modReductionCurve
        # },
    ]

    # CREATE THE SOIL PROFILE AND GENERATE TCL FILES
    try:
        soilProfile = SoilProfile(soilLayersDefinition)
        soilProfile.generateTCLFiles()
    except (KeyError, ValueError) as e:
        print(f"\nERROR: Could not generate files. Please check your layer definitions.")
        print(f"DETAILS: {e}")
