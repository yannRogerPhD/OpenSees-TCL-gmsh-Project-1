!!!!!!!!!!!!! Testing G1 functions !!!!!!!!!!!!!

1. G18: parseELMTsFromGMSH
    WE WANT TO EXTRACT ELEMENTS ON WHICH TO APPLY MATERIAL PROPS (beam, plate, shells, soil, etc...)
    --> -TEST all elements inside gmshType (for these tests we shall limit ourselves to lines, quadangles, and hexahedron; this is simply because these are the main elements we shal use for future simulations)
        -lines for beam elements
        -quads for 2D soil elements
        -hexahedron for 3D soil elements
    --> see nomenclature below (elementLabels)
    --> more:
        - G18-1 (lines)
        - G18-3-1 (quads WITHOUT structural elements)
        - G18-3-2 (quads WITH structural 2D elements)
        - G18-5-1 (hexahedron WITHOUT structural elements)
        - G18-5-2 (hexahedron WITH 3D structural elements)

elementLabels = {
    # for structural elements:
    1: "elasticBeamColumn2D",
    101: "elasticBeamColumn3D",
    201: "dispBeamColumn2D",
    202: "dispBeamColumn3D",

    # 2D soil
    3: "quad (plain 2D)",
    10: "quad9 (plain 2D)",
    103: "bbarQuadUP",
    1003: "quadUP",

    10031: "ASD2D_B",
    10032: "ASD2D_L",
    10033: "ASD2D_R",
    10034: "ASD2D_BL",
    10035: "ASD2D_BR",

    # 3D soil
    5: "brick (plain 3D)",
    105: "bbarBrickUP",
    1005: "SSPbrickUP",
    1055: "SSPbrick",

    10051: "ASD3D_B",
    10052: "ASD3D_L",
    10053: "ASD3D_R",
    10054: "ASD3D_F",
    10055: "ASD3D_K",
    10056: "ASD3D_BL",
    10057: "ASD3D_BR",
    10058: "ASD3D_BF",
    10059: "ASD3D_BK",
    10060: "ASD3D_LF",
    10061: "ASD3D_LK",
    10062: "ASD3D_RF",
    10063: "ASD3D_RK",
    10064: "ASD3D_BLF",
    10065: "ASD3D_BLK",
    10066: "ASD3D_BRF",
    10067: "ASD3D_BRK",

    17: "20_8_BrickUP",
}

