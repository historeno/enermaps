d = {
    "project": {
        "formData": {
            "country": "FR",
            "canton": "VS",
            "altitude": "100",
            "meteoParam": "jura",
            "context": "rural",
            "polygon": "[[0,0],[0,10],[10,10],[10,0]]",
            "adjoining": "[0,0,0.5,0]",
            "typo": "1",
            "year": "1900",
            "category": "1",
            "height": "5",
            "generator": "genTypOil",
            "generatorYear": "1900",
            "emettors": "emRadWall",
            "regulation": "0",
            "tubeInsulH": "notInsulated",
            "tubeInsulW": "notInsulated",
            "solarThermal": "0",
            "solarThermalAreaAuto": "0",
            "solarThermalArea": "Non",
            "nbAppart": "0",
            "devEff": "best",
            "ventMeca": "none",
            "elevator": "0",
            "solarPV": "0",
            "pvAreaAuto": "0",
            "pvArea": "0",
            "pvOri": "0",
            "protectionGrade": "1",
            "heatingWood": "0",
            "heatingProbes": "0",
            "solarRoof": "0",
        },
        "bldOutput": {
            "Qh": "39.222067477738",
            "Qt": {
                "total": "25.3200095082543",
                "wall": "0.000393493843468899",
                "roof": "0",
                "floor": "25.3189649999999",
                "window": "0.000651014410932324",
                "tb": "0",
            },
            "Qv": "28.93596",
            "Qs": "0.000879970414355701",
            "Qi": "27.265",
            "fUtil": "0.551383291241563",
            "Qw": "75.6",
            "Qhli": "21.4466392191405",
            "Ath": "615467221176.291",
            "Efp": "16404.1524968219",
            "CED": "20177.4475710916",
            "NRE": "20013.191046123",
            "GWP": "4888.20894405249",
            "Cost": "0.106000000203448",
            "heating": {
                "gen": {"EF": "5603.15249681972", "vector": "oil"},
                "Efp": "5603.15249681972",
                "CED": "6891.87757108825",
                "NRE": "6835.84604612005",
                "GWP": "1669.73944405228",
                "Cost": "0",
            },
            "dhw": {
                "gen": {"EF": "10800.0000000003", "vector": "oil"},
                "Efp": "10800.0000000003",
                "CED": "13284.0000000003",
                "NRE": "13176.0000000003",
                "GWP": "3218.40000000008",
                "Cost": "0",
            },
            "aux": {
                "gen": {"EF": "0.5", "vector": "electricity"},
                "Efp": "1",
                "CED": "1.57",
                "NRE": "1.345",
                "GWP": "0.0695",
                "Cost": "0.106",
            },
            "devices": {
                "gen": {"EF": "9.59658350945514E-10", "vector": "electricity"},
                "Efp": "1.91931670189103E-9",
                "CED": "3.01332722196891E-9",
                "NRE": "2.58148096404343E-9",
                "GWP": "1.33392510781426E-10",
                "Cost": "2.03447570400449E-10",
            },
            "classEnv": "D",
            "classEp": "G",
            "classCO2": "G",
            "Xsw": "0",
            "Xsh": "0",
            "pvCover": "0",
            "Qls_H": "0",
            "Qls_W": "1.87583245777735E-12",
        },
        "bldInput": {
            "calcmode": "opti",
            "calcversion": "2016",
            "building": {
                "ID": "03b1ee1d-ee61-4820-9725-500cb9d32be1",
                "tbFactor": None,
                "name": "Building",
                "altitude": "100",
                "worktype": "new",
                "meteo": "60EE1731-5854-4084-889C-BF35C57A49C6",
                "zones": {
                    "zone": {
                        "id": "5741a9e3-9424-4bc4-af0c-d0a83b8cf560",
                        "name": "zone1",
                        "category": "1",
                        "Ae": "984725448456.66",
                        "Tint": "20",
                        "regulation": "0",
                        "airflow": "1",
                        "capa": None,
                        "envelopes": {
                            "walls": {
                                "wall": [
                                    {
                                        "type": "envWall",
                                        "name": "WALL_EXT1A",
                                        "id": "2ab29366-1486-482c-8efc-e0ae21da619e",
                                        "against": "ext",
                                        "bfact": "1",
                                        "ori": "90",
                                        "incline": "90",
                                        "uval": "0.44",
                                        "nb": "1",
                                        "isHeated": None,
                                        "heatedTMax": "0",
                                        "areaNet": "0",
                                        "areaBrut": "5086416.5442",
                                    },
                                    {
                                        "type": "envWall",
                                        "name": "WALL_EXT2A",
                                        "id": "b44dba84-d125-4bf8-b97b-3a41ae23efa0",
                                        "against": "ext",
                                        "bfact": "1",
                                        "ori": "180",
                                        "incline": "90",
                                        "uval": "0.44",
                                        "nb": "1",
                                        "isHeated": None,
                                        "heatedTMax": "0",
                                        "areaNet": "0",
                                        "areaBrut": "5120695.068",
                                    },
                                    {
                                        "type": "envWall",
                                        "name": "WALL_EXT3A",
                                        "id": "d7996be6-eb34-4d75-9408-e53a2a62e1e5",
                                        "against": "ext",
                                        "bfact": "1",
                                        "ori": "315",
                                        "incline": "90",
                                        "uval": "0.44",
                                        "nb": "1",
                                        "isHeated": None,
                                        "heatedTMax": "0",
                                        "areaNet": "0",
                                        "areaBrut": "3608779.2686915",
                                    },
                                ]
                            },
                            "floors": {
                                "floor": {
                                    "type": "envFloor",
                                    "name": "FLOOR_NHA",
                                    "id": "9afa148a-8940-4432-8523-8b97101a39c0",
                                    "against": "znh",
                                    "bfact": "0.7",
                                    "ori": "-1",
                                    "incline": "0",
                                    "uval": "0.67",
                                    "nb": "1",
                                    "isHeated": None,
                                    "heatedTMax": "0",
                                    "areaNet": "0",
                                    "areaBrut": "615453405285.41",
                                }
                            },
                            "roofs": None,
                            "windows": {
                                "win": [
                                    {
                                        "id": "3cf43caa-98c7-4e9d-8aa8-2e6c2899634e",
                                        "parent": "2ab29366-1486-482c-8efc-e0ae21da619e",
                                        "name": "Fen%C3%AAtres+E",
                                        "against": ["ext", "ext"],
                                        "type": "window",
                                        "ori": "90",
                                        "incline": "90",
                                        "nb": "1",
                                        "areaNet": "1047801.8081052",
                                        "uval": "2.05",
                                        "bfact": "1",
                                        "gp": "0.63",
                                        "frmPercent": "0.25",
                                        "FS": "0.288",
                                    },
                                    {
                                        "id": "7eda0327-5897-40a1-a656-5d859d7e3063",
                                        "parent": "b44dba84-d125-4bf8-b97b-3a41ae23efa0",
                                        "name": "Fen%C3%AAtres+S",
                                        "against": ["ext", "ext"],
                                        "type": "window",
                                        "ori": "180",
                                        "incline": "90",
                                        "nb": "1",
                                        "areaNet": "1776881.188596",
                                        "uval": "2.05",
                                        "bfact": "1",
                                        "gp": "0.63",
                                        "frmPercent": "0.25",
                                        "FS": "0.355",
                                    },
                                    {
                                        "id": "0e49b5df-ecaf-40a2-ae60-fe91cd866538",
                                        "parent": "d7996be6-eb34-4d75-9408-e53a2a62e1e5",
                                        "name": "Fen%C3%AAtres+NO",
                                        "against": ["ext", "ext"],
                                        "type": "window",
                                        "ori": "315",
                                        "incline": "90",
                                        "nb": "1",
                                        "areaNet": "795735.82874648",
                                        "uval": "2.05",
                                        "bfact": "1",
                                        "gp": "0.63",
                                        "frmPercent": "0.25",
                                        "FS": "0.243",
                                    },
                                ]
                            },
                        },
                        "thermalbridges": {"linear": None, "pt": None},
                    }
                },
                "generators": {
                    "generator": {
                        "type": "oil_boiler",
                        "vector": "oil",
                        "mode": "HW",
                        "effH": "0.007",
                        "effW": "0.007",
                        "coverH": "1",
                        "coverW": "1",
                    }
                },
                "solarThermal": {"area": "0", "mode": "W"},
                "dist": {
                    "genSupply": None,
                    "genPos": "outsideEnv",
                    "tempInOut": "70_55",
                    "surdim": "1.5",
                    "tubeInsulH": "notInsulated",
                    "tubeInsulW": "notInsulated",
                    "TubeInsulThickH": "0.02",
                    "TubeInsulThickW": "0.02",
                    "tempMaintenance": "0",
                    "stockVol": None,
                },
                "pv": {
                    "area": "0",
                    "incline": "30",
                    "ori": "180",
                    "techno": "mono",
                    "isBattery": "0",
                },
                "electricity": {
                    "nbAppart": "0",
                    "nbGasCook": "0",
                    "devEff": "best",
                    "devLevel": "std",
                    "ventil": "none",
                    "isElevator": "0",
                    "isJacuzzi": "0",
                    "isSauna": "0",
                    "isAquarium": "0",
                    "isWaterbed": "0",
                },
            },
        },
        "renoOutput": {
            "Qh": "39.222067477738",
            "Qt": {
                "total": "25.3200095082543",
                "wall": "0.000393493843468899",
                "roof": "0",
                "floor": "25.3189649999999",
                "window": "0.000651014410932324",
                "tb": "0",
            },
            "Qv": "28.93596",
            "Qs": "0.000879970414355701",
            "Qi": "27.265",
            "fUtil": "0.551383291241563",
            "Qw": "75.6",
            "Qhli": "21.4466392191405",
            "Ath": "615467221176.291",
            "Efp": "16404.1524968219",
            "CED": "20177.4475710916",
            "NRE": "20013.191046123",
            "GWP": "4888.20894405249",
            "Cost": "0.106000000203448",
            "heating": {
                "gen": {"EF": "5603.15249681972", "vector": "oil"},
                "Efp": "5603.15249681972",
                "CED": "6891.87757108825",
                "NRE": "6835.84604612005",
                "GWP": "1669.73944405228",
                "Cost": "0",
            },
            "dhw": {
                "gen": {"EF": "10800.0000000003", "vector": "oil"},
                "Efp": "10800.0000000003",
                "CED": "13284.0000000003",
                "NRE": "13176.0000000003",
                "GWP": "3218.40000000008",
                "Cost": "0",
            },
            "aux": {
                "gen": {"EF": "0.5", "vector": "electricity"},
                "Efp": "1",
                "CED": "1.57",
                "NRE": "1.345",
                "GWP": "0.0695",
                "Cost": "0.106",
            },
            "devices": {
                "gen": {"EF": "9.59658350945514E-10", "vector": "electricity"},
                "Efp": "1.91931670189103E-9",
                "CED": "3.01332722196891E-9",
                "NRE": "2.58148096404343E-9",
                "GWP": "1.33392510781426E-10",
                "Cost": "2.03447570400449E-10",
            },
            "classEnv": "D",
            "classEp": "G",
            "classCO2": "G",
            "Xsw": "0",
            "Xsh": "0",
            "pvCover": "0",
            "Qls_H": "0",
            "Qls_W": "1.87583245777735E-12",
        },
        "renoInput": {
            "calcmode": "opti",
            "calcversion": "2016",
            "building": {
                "ID": "03b1ee1d-ee61-4820-9725-500cb9d32be1",
                "tbFactor": None,
                "name": "Building",
                "altitude": "100",
                "worktype": "new",
                "meteo": "60EE1731-5854-4084-889C-BF35C57A49C6",
                "zones": {
                    "zone": {
                        "id": "5741a9e3-9424-4bc4-af0c-d0a83b8cf560",
                        "name": "zone1",
                        "category": "1",
                        "Ae": "984725448456.66",
                        "Tint": "20",
                        "regulation": "0",
                        "airflow": "1",
                        "capa": None,
                        "envelopes": {
                            "walls": {
                                "wall": [
                                    {
                                        "type": "envWall",
                                        "name": "WALL_EXT1A",
                                        "id": "2ab29366-1486-482c-8efc-e0ae21da619e",
                                        "against": "ext",
                                        "bfact": "1",
                                        "ori": "90",
                                        "incline": "90",
                                        "uval": "0.44",
                                        "nb": "1",
                                        "isHeated": None,
                                        "heatedTMax": "0",
                                        "areaNet": "0",
                                        "areaBrut": "5086416.5442",
                                    },
                                    {
                                        "type": "envWall",
                                        "name": "WALL_EXT2A",
                                        "id": "b44dba84-d125-4bf8-b97b-3a41ae23efa0",
                                        "against": "ext",
                                        "bfact": "1",
                                        "ori": "180",
                                        "incline": "90",
                                        "uval": "0.44",
                                        "nb": "1",
                                        "isHeated": None,
                                        "heatedTMax": "0",
                                        "areaNet": "0",
                                        "areaBrut": "5120695.068",
                                    },
                                    {
                                        "type": "envWall",
                                        "name": "WALL_EXT3A",
                                        "id": "d7996be6-eb34-4d75-9408-e53a2a62e1e5",
                                        "against": "ext",
                                        "bfact": "1",
                                        "ori": "315",
                                        "incline": "90",
                                        "uval": "0.44",
                                        "nb": "1",
                                        "isHeated": None,
                                        "heatedTMax": "0",
                                        "areaNet": "0",
                                        "areaBrut": "3608779.2686915",
                                    },
                                ]
                            },
                            "floors": {
                                "floor": {
                                    "type": "envFloor",
                                    "name": "FLOOR_NHA",
                                    "id": "9afa148a-8940-4432-8523-8b97101a39c0",
                                    "against": "znh",
                                    "bfact": "0.7",
                                    "ori": "-1",
                                    "incline": "0",
                                    "uval": "0.67",
                                    "nb": "1",
                                    "isHeated": None,
                                    "heatedTMax": "0",
                                    "areaNet": "0",
                                    "areaBrut": "615453405285.41",
                                }
                            },
                            "roofs": None,
                            "windows": {
                                "win": [
                                    {
                                        "id": "3cf43caa-98c7-4e9d-8aa8-2e6c2899634e",
                                        "parent": "2ab29366-1486-482c-8efc-e0ae21da619e",
                                        "name": "Fen%C3%AAtres+E",
                                        "against": ["ext", "ext"],
                                        "type": "window",
                                        "ori": "90",
                                        "incline": "90",
                                        "nb": "1",
                                        "areaNet": "1047801.8081052",
                                        "uval": "2.05",
                                        "bfact": "1",
                                        "gp": "0.63",
                                        "frmPercent": "0.25",
                                        "FS": "0.288",
                                    },
                                    {
                                        "id": "7eda0327-5897-40a1-a656-5d859d7e3063",
                                        "parent": "b44dba84-d125-4bf8-b97b-3a41ae23efa0",
                                        "name": "Fen%C3%AAtres+S",
                                        "against": ["ext", "ext"],
                                        "type": "window",
                                        "ori": "180",
                                        "incline": "90",
                                        "nb": "1",
                                        "areaNet": "1776881.188596",
                                        "uval": "2.05",
                                        "bfact": "1",
                                        "gp": "0.63",
                                        "frmPercent": "0.25",
                                        "FS": "0.355",
                                    },
                                    {
                                        "id": "0e49b5df-ecaf-40a2-ae60-fe91cd866538",
                                        "parent": "d7996be6-eb34-4d75-9408-e53a2a62e1e5",
                                        "name": "Fen%C3%AAtres+NO",
                                        "against": ["ext", "ext"],
                                        "type": "window",
                                        "ori": "315",
                                        "incline": "90",
                                        "nb": "1",
                                        "areaNet": "795735.82874648",
                                        "uval": "2.05",
                                        "bfact": "1",
                                        "gp": "0.63",
                                        "frmPercent": "0.25",
                                        "FS": "0.243",
                                    },
                                ]
                            },
                        },
                        "thermalbridges": {"linear": None, "pt": None},
                    }
                },
                "generators": {
                    "generator": {
                        "type": "oil_boiler",
                        "vector": "oil",
                        "mode": "HW",
                        "effH": "0.007",
                        "effW": "0.007",
                        "coverH": "1",
                        "coverW": "1",
                    }
                },
                "solarThermal": {"area": "0", "mode": "W"},
                "dist": {
                    "genSupply": None,
                    "genPos": "outsideEnv",
                    "tempInOut": "70_55",
                    "surdim": "1.5",
                    "tubeInsulH": "notInsulated",
                    "tubeInsulW": "notInsulated",
                    "TubeInsulThickH": "0.02",
                    "TubeInsulThickW": "0.02",
                    "tempMaintenance": "0",
                    "stockVol": None,
                },
                "pv": {
                    "area": "0",
                    "incline": "30",
                    "ori": "180",
                    "techno": "mono",
                    "isBattery": "0",
                },
                "electricity": {
                    "nbAppart": "0",
                    "nbGasCook": "0",
                    "devEff": "best",
                    "devLevel": "std",
                    "ventil": "none",
                    "isElevator": "0",
                    "isJacuzzi": "0",
                    "isSauna": "0",
                    "isAquarium": "0",
                    "isWaterbed": "0",
                },
            },
        },
    }
}
