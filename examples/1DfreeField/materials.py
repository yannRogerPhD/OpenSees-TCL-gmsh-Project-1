import sys

# A registry of material templates with required and optional parameters
MATERIAL_TPL = {
    "PressureIndependMultiYield":
        {
            "tpl":
                (
                    "nDMaterial PressureIndependMultiYield {matTag} {ndm} {rho} "
                    "{gRef} {kRef} {cohesion} {peakShearStra}"
                    "{frictionAng_str}{refPress_str}{pressDependCoe_str}{noYieldSurf_str}{mod_curve_str}"
                ),

            "required_params": ["matTag", "ndm", "rho", "gRef", "kRef", "cohesion", "peakShearStra"],

            "optional_params":
                {
                    "frictionAng": float,
                    "refPress": float,
                    "pressDependCoe": float,
                    "noYieldSurf": int,
                    "modulus_reduction_curve": list,
                },
        },

    "PressureDependMultiYield":
        {
            "tpl":
                (
                    "nDMaterial PressureDependMultiYield {matTag} {ndm} {rho} "
                    "{gRef} {kRef} {frictionAng} {peakShearStra} {refPress} {pressDependCoe} "
                    "{phaseTransformAng} {contract1} {dilate1} {dilate2} {liquefac1} "
                    "{liquefac2} {liquefac3}"
                    "{noYieldSurf_str}{mod_curve_str}{critical_state_str}"
                ),

            "required_params":
                [
                    "matTag", "ndm", "rho", "gRef", "kRef", "frictionAng", "peakShearStra",
                    "refPress", "pressDependCoe", "phaseTransformAng",
                    "contract1", "dilate1", "dilate2",
                    "liquefac1", "liquefac2", "liquefac3",
                ],

            "optional_params":
                {
                    "noYieldSurf": int,
                    "modulus_reduction_curve": list,
                    "e": float,
                    "cs1": float,
                    "cs2": float,
                    "cs3": float,
                    "pa": float,
                    "c": float,
                },
        },

    "PressureDependMultiYield02":
        {
            "tpl":
                (
                    "nDMaterial PressureDependMultiYield02 {matTag} {ndm} {rho} "
                    "{gRef} {kRef} {frictionAng} {peakShearStra} {refPress} {pressDependCoe} "
                    "{phaseTransformAng} {contract1} {contract3} {dilate1} {dilate3}"
                    "{noYieldSurf_str}{mod_curve_str}{optional_tail_str}"
                ),

            "required_params":
                [
                    "matTag", "ndm", "rho", "gRef", "kRef", "frictionAng", "peakShearStra",
                    "refPress", "pressDependCoe", "phaseTransformAng",
                    "contract1", "contract3", "dilate1", "dilate3",
                ],

            "optional_params":
                {
                    "noYieldSurf": int,
                    "modulus_reduction_curve": list,
                    "contract2": float,
                    "dilate2": float,
                    "liquefac1": float,
                    "liquefac2": float,
                    "e": float,
                    "cs1": float,
                    "cs2": float,
                    "cs3": float,
                    "pa": float,
                    "c": float,
                },
        },

    "PressureDependMultiYield03":
        {
            "tpl":
                (
                    "nDMaterial PressureDependMultiYield03 {matTag} {ndm} {rho} "
                    "{gRef} {kRef} {frictionAng} {peakShearStra} {refPress} {pressDependCoe} "
                    "{phaseTransformAng} {mType} {ca} {cb} {cc} {cd} {ce} {da} {db} {dc}"
                    "{noYieldSurf_str}{mod_curve_str}{optional_tail_str}"
                ),

            "required_params":
                [
                    "matTag", "ndm", "rho", "gRef", "kRef", "frictionAng", "peakShearStra",
                    "refPress", "pressDependCoe", "phaseTransformAng", "mType",
                    "ca", "cb", "cc", "cd", "ce", "da", "db", "dc"
                ],

            "optional_params":
                {
                    "noYieldSurf": int,
                    "modulus_reduction_curve": list,
                    "liquefac1": float,
                    "liquefac2": float,
                    "pa": float,
                    "s0": float
                },
        },

    "FluidSolidPorousMaterial":
        {
            "tpl": "nDMaterial FluidSolidPorousMaterial {matTag} {ndm} {soilMatTag} {combinedBulkModul}{pa_str}",
            "required_params": ["matTag", "ndm", "soilMatTag", "combinedBulkModul"],
            "optional_params": {"pa": float},
        },

    "ElasticIsotropic":
        {
            "tpl": "nDMaterial ElasticIsotropic {matTag} {E} {v}{rho_str}",
            "required_params": ["matTag", "E", "v"],
            "optional_params": {"rho": float},
        },

}


def format_gamma_gs_curve(curve, key):
    if len(curve) % 2 != 0:
        print(
            f"Warning: modulus_reduction_curve for '{key}' has odd length; values should come in gamma–Gs pairs.",
            file=sys.stderr,
        )
    n_pairs = len(curve) // 2
    header_comment = " \\\n# gamma–Gs modulus reduction pairs (user-defined backbone)\n    "
    pairs_per_line = 8
    chunks = [
        " ".join(map(str, curve[i:i + pairs_per_line]))
        for i in range(0, len(curve), pairs_per_line)
    ]
    return f" -{n_pairs}" + header_comment + " \\\n    ".join(chunks)


def write_material_def(key, params, file, registry):
    if key not in registry:
        print(f"Error: Material key '{key}' not found in the registry.", file=sys.stderr)
        return

    template_info = registry[key]
    template = template_info["tpl"]
    required_params = template_info["required_params"]

    # !!!!! 1. check required !!!!!
    missing_params = [p for p in required_params if p not in params]
    if missing_params:
        print(f"Error: Missing required parameters for material '{key}': {', '.join(missing_params)}", file=sys.stderr)
        return

    # !!!!! 2. prepare optional fields (only for PIMY) !!!!!
    if key == "PressureIndependMultiYield":
        # defaults
        frictionAng_str = f" {params['frictionAng']}" if "frictionAng" in params else ""
        refPress_str = f" {params['refPress']}" if "refPress" in params else ""
        pressDependCoe_str = f" {params['pressDependCoe']}" if "pressDependCoe" in params else ""

        mod_curve_str = ""  # noqa: F841 # used later in params.update()

        if "modulus_reduction_curve" in params and isinstance(params["modulus_reduction_curve"], list):
            mod_curve_str = format_gamma_gs_curve(params["modulus_reduction_curve"], key)
            noYieldSurf_str = ""
        else:
            mod_curve_str = ""
            noYieldSurf_str = f" {params['noYieldSurf']}" if "noYieldSurf" in params else " 20"

        # inject into params so .format() can use them
        params.update({
            "frictionAng_str": frictionAng_str,
            "refPress_str": refPress_str,
            "pressDependCoe_str": pressDependCoe_str,
            "noYieldSurf_str": noYieldSurf_str,
            "mod_curve_str": mod_curve_str,
        })

    if key == "PressureDependMultiYield":
        mod_curve_str = ""  # noqa: F841 # used later in params.update()
        critical_state_str = ""

        # Handle modulus reduction or yield surfaces
        if "modulus_reduction_curve" in params and isinstance(params["modulus_reduction_curve"], list):
            mod_curve_str = format_gamma_gs_curve(params["modulus_reduction_curve"], key)
            noYieldSurf_str = ""
        else:
            mod_curve_str = ""
            noYieldSurf_str = f" {params['noYieldSurf']}" if "noYieldSurf" in params else " 20"

        # Handle critical-state optional parameters
        crit_params = ["e", "cs1", "cs2", "cs3", "pa", "c"]
        crit_values = [str(params[p]) for p in crit_params if p in params]
        if crit_values:
            critical_state_str = " " + " ".join(crit_values)

        # inject
        params.update({
            "noYieldSurf_str": noYieldSurf_str,
            "mod_curve_str": mod_curve_str,
            "critical_state_str": critical_state_str,
        })

    if key == "PressureDependMultiYield02":
        mod_curve_str = ""  # noqa: F841 # used later in params.update()
        optional_tail_str = ""

        # Handle yield surfaces
        if "modulus_reduction_curve" in params and isinstance(params["modulus_reduction_curve"], list):
            mod_curve_str = format_gamma_gs_curve(params["modulus_reduction_curve"], key)
            noYieldSurf_str = ""
        else:
            mod_curve_str = ""
            noYieldSurf_str = f" {params['noYieldSurf']}" if "noYieldSurf" in params else " 20"

        # Handle optional tail parameters
        tail_params = ["contract2", "dilate2", "liquefac1", "liquefac2",
                       "e", "cs1", "cs2", "cs3", "pa", "c"]
        tail_values = [str(params[p]) for p in tail_params if p in params]
        if tail_values:
            optional_tail_str = " " + " ".join(tail_values)

        # Inject into params for template formatting
        params.update({
            "noYieldSurf_str": noYieldSurf_str,
            "mod_curve_str": mod_curve_str,
            "optional_tail_str": optional_tail_str,
        })

    if key == "PressureDependMultiYield03":
        mod_curve_str = ""  # noqa: F841 # used later in params.update()
        optional_tail_str = ""

        # Handle yield surfaces (gamma–Gs pairs)
        if "modulus_reduction_curve" in params and isinstance(params["modulus_reduction_curve"], list):
            mod_curve_str = format_gamma_gs_curve(params["modulus_reduction_curve"], key)
            noYieldSurf_str = ""
        else:
            mod_curve_str = ""
            noYieldSurf_str = f" {params['noYieldSurf']}" if "noYieldSurf" in params else " 20"

        # Handle optional tail parameters
        tail_params = ["liquefac1", "liquefac2", "pa", "s0"]
        tail_values = [str(params[p]) for p in tail_params if p in params]
        if tail_values:
            optional_tail_str = " " + " ".join(tail_values)

        params.update({
            "noYieldSurf_str": noYieldSurf_str,
            "mod_curve_str": mod_curve_str,
            "optional_tail_str": optional_tail_str,
        })

    if key == "FluidSolidPorousMaterial":
        pa_str = f" {params['pa']}" if "pa" in params else ""
        params.update({"pa_str": pa_str})

    if key == "ElasticIsotropic":
        rho_str = f" {params['rho']}" if "rho" in params else ""
        params.update({"rho_str": rho_str})

    # !!!!! 3. build material definition !!!!!
    try:
        material_def = template.format(**params)
    except KeyError as e:
        print(f"Error: Incorrect parameter '{e}' for material '{key}'.", file=sys.stderr)
        return

    # !!!!! 4. write !!!!!
    file.write(f"{material_def}\n")


paramsPIMY = {
    "matTag": 2,
    "ndm": 2,
    "rho": 1.8,
    "gRef": 1.3e4,
    "kRef": 6.5e4,
    "cohesion": 18,
    "peakShearStra": 0.1,
    # optional
    "frictionAng": 0,
    "refPress": 100,
    "pressDependCoe": 0,
    "modulus_reduction_curve":
        [
            1e-6, 0.999,
            3e-6, 0.995,
            1e-5, 0.99,
            3e-5, 0.96,
            1e-4, 0.85,
            3e-4, 0.64,
            1e-3, 0.37,
            3e-3, 0.18,
            1e-2, 0.08,
            3e-2, 0.03,
            1e-1, 0.01
        ],
}

paramsPDMY = {
    "matTag": 3,
    "ndm": 2,
    "rho": 1.9,
    "gRef": 7.5e4,
    "kRef": 2.0e5,
    "frictionAng": 33,
    "peakShearStra": 0.1,
    "refPress": 80,
    "pressDependCoe": 0.5,
    "phaseTransformAng": 27,
    "contract1": 0.07,
    "dilate1": 0.4,
    "dilate2": 2,
    "liquefac1": 10,
    "liquefac2": 0.01,
    "liquefac3": 1.0,
    # optional
    "modulus_reduction_curve":
        [
            1e-6, 0.999, 3e-6, 0.995, 1e-5, 0.99, 3e-5, 0.96,
            1e-4, 0.85, 3e-4, 0.64, 1e-3, 0.37, 3e-3, 0.18,
            1e-2, 0.08, 3e-2, 0.03, 1e-1, 0.01
        ],
    "e": 0.7,
    "cs1": 0.9,
    "cs2": 0.02,
    "cs3": 0.7,
    "pa": 101,
    "c": 0.3,
}

paramsPDMY02 = {
    "matTag": 4,
    "ndm": 2,
    "rho": 1.85,
    "gRef": 6.0e4,
    "kRef": 2.2e5,
    "frictionAng": 32.0,
    "peakShearStra": 0.1,
    "refPress": 80,
    "pressDependCoe": 0.5,
    "phaseTransformAng": 26,
    "contract1": 0.05,
    "contract3": 0.5,
    "dilate1": 0.3,
    "dilate3": 3.0,
    # optional
    "modulus_reduction_curve":
        [
            1e-6, 0.999, 3e-6, 0.995, 1e-5, 0.99, 3e-5, 0.96,
            1e-4, 0.85, 3e-4, 0.64, 1e-3, 0.37, 3e-3, 0.18,
            1e-2, 0.08, 3e-2, 0.03, 1e-1, 0.01
        ],
    "contract2": 5,
    "dilate2": 3,
    "liquefac1": 1,
    "liquefac2": 0,
    "e": 0.6,
    "cs1": 0.9,
    "cs2": 0.02,
    "cs3": 0.7,
    "pa": 101,
    "c": 0.1,
}

paramsPDMY03 = {
    "matTag": 5,
    "ndm": 2,
    "rho": 1.85,
    "gRef": 6.0e4,
    "kRef": 2.2e5,
    "frictionAng": 32.0,
    "peakShearStra": 0.1,
    "refPress": 80,
    "pressDependCoe": 0.5,
    "phaseTransformAng": 26,
    "mType": 0,
    "ca": 0.02, "cb": 0.04, "cc": 0.08, "cd": 0.1, "ce": 0.2,
    "da": 0.01, "db": 0.02, "dc": 0.03,
    # optional
    "modulus_reduction_curve":
        [
            1e-6, 0.999, 3e-6, 0.995, 1e-5, 0.99, 3e-5, 0.96,
            1e-4, 0.85, 3e-4, 0.64, 1e-3, 0.37, 3e-3, 0.18,
            1e-2, 0.08, 3e-2, 0.03, 1e-1, 0.01
        ],
    "liquefac1": 1.0,
    "liquefac2": 0.0,
    "pa": 101.0,
    "s0": 1.73,
}

paramsFSP = {
    "matTag": 10,
    "ndm": 2,
    "soilMatTag": 5,  # this should correspond to your PDMY03 tag
    "combinedBulkModul": 2.2e6 / 0.3,  # for example, Bf/n (if porosity = 0.3)
    # optional
    "pa": 101.0,
}

paramsElastic = {
    "matTag": 20,
    "E": 3.0e7,   # Elastic modulus (Pa)
    "v": 0.3,     # Poisson's ratio
    "rho": 2.0e3  # Density (optional)
}


def writeMaterials(materials, registry):
    """
    Write one or more material definitions to file(s).

    Args:
        materials (dict | tuple | list):
            The material(s) to write. Accepts:
              - A single tuple: ("MaterialKey", params_dict)
              - A dict: {"MaterialKey": params_dict, ...}
              - A list of tuples: [("MaterialKey", params_dict), ...]

        registry (dict):
            The material registry (e.g., MATERIAL_TPL) that maps material keys
            to their template definitions, required, and optional parameters.

    Returns:
        None
            Writes .tcl material definition files to disk. Prints success messages
            or errors to stderr.
    """
    SHORT_NAMES = {
        "PressureIndependMultiYield": "matPIMY",
        "PressureDependMultiYield": "matPDMY",
        "PressureDependMultiYield02": "matPDMY02",
        "PressureDependMultiYield03": "matPDMY03",
        "FluidSolidPorousMaterial": "matFSP",
        "ElasticIsotropic": "matELAS",
    }

    if not materials:
        print("No materials provided.", file=sys.stderr)
        return

    # normalize input
    if isinstance(materials, tuple):
        materials = [materials]
    elif isinstance(materials, dict):
        materials = list(materials.items())

    for key, params in materials:
        short = SHORT_NAMES.get(key, key[:6])  # fallback if not in dict
        # outName = f"material_{key.lower()}_test.tcl"
        outName = f"{short}.tcl"
        with open(outName, "w") as f:
            write_material_def(key, params, f, registry)
        print(f"Wrote {outName} successfully.")


# ============================================================
# APPLICATIONS
# ============================================================

# gRefExX = EexX / (2 * (1 + nuExX))
# kRefExX = EexX / (3 * (1 - 2 * nuExX))

rhoEx1 = 2.0
Eex1 = 9.0e4
nuEx1 = 0.40
gRefEx1 = Eex1 / (2 * (1 + nuEx1))
kRefEx1 = Eex1 / (3 * (1 - 2 * nuEx1))
cohesionEx1 = 30
gammaPeakEx1 = 0.1

paramsPIMYex1 = {
    "matTag": 1,
    "ndm": 2,
    "rho": rhoEx1,
    "gRef": gRefEx1,
    "kRef": kRefEx1,
    "cohesion": cohesionEx1,
    "peakShearStra": gammaPeakEx1,
}

VsSoil = 230.9
rhoSoil = 1755
nuSoil = 0.0
ESoil = 2 * rhoSoil * (VsSoil ** 2) * (1 + nuSoil)

paramsElastic1 = {
    "matTag": 1,
    "E": ESoil,   # Elastic modulus (Pa)
    "v": nuSoil,     # Poisson's ratio
    "rho": rhoSoil  # Density (optional)
}

writeMaterials([
    # ("PressureIndependMultiYield", paramsPIMYex1),
    # ("PressureDependMultiYield", paramsPDMY),
    # ("PressureDependMultiYield02", paramsPDMY02),
    ("ElasticIsotropic", paramsElastic1),
], MATERIAL_TPL)
