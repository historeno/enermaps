decoder = {
    "country": {"Suisse": "CH", "France": "FR"},
    "canton": {
        "Valais": "VS",
        "Vaud": "VD",
        "Fribourg": "FR",
        "Bern": "BE",
        "Neuchâtel": "NE",
        "Jura-CH": "JU",
        "Genève": "GE",
        "Haute-Savoie": "74",
        "Ain": "01",
        "Jura-FR": "39",
        "Territoire de Belfort": "90",
    },
    # "altitude" / get from the form
    "meteoParam": {
        "Jura": "jura",
        "Préalpes": "preAlpes",
        "Dégagé vers le sud": "sud",
        "Bouché vers le sud": "norSud",
    },
    "context": {
        "Rural": "rural",
        "Urban": "urban",
        "Suburban": "suburban",
    },
    # empreinte / get from the form
    # typologie / get from the form
    # année de constr / get from the form
    # catégorie d'ouvrage / get from the form
    # hauteur / get from the form
    "generator": {
        "Mazout": "genTypOil",
        "Gas naturel": "genTypGas",
        "Pellets": "genTypWoodPellets",
        "Büches bois": "genTypWoodLogs",
        "Vopeaux bois": "genTypWoodChpis",
        "PAC air-eau": "genTypHeatPumpAW",
        "PAC sol-eau": "genTypHeatPumpGW",
        "Électrique direct": "genTypElecDirect",
        "Chauffage à distance": "genTypCAD",
    },
    # "generatorYear" / get from the form
    "emettors": {
        "Radiateurs": "emRadWall",
        "Radiateurs devant fenêtres": "emRadWin",
        "Plancher(s) chaffant(s)": "emHeatedFloor",
        "Murs chauffants": "emHeatedWall",
        "Aucun (élec direct)": "emNone",
    },
    "regulation": {
        "Sondes de temp. par pièce ou vannes thermostatiques sur radiateurs (+0°C)": 0,
        "Sonde de température dans une pièce de référence (par ex séjour)  (+1°C)": 1,
        "autre (+2°C)": 2,
    },
    "tubeInsulH": {
        "Non": 0,
        "Oui": 1,
    },
    "tubeInsulW": {
        "Non isolées": "notInsulated",
        "Partiellement isolées": "partiallyInsulated",
        "Complètement isolées": "fullyInsulated",
    },
    "solarThermal": {
        "Non": 0,
        "Oui": 1,
    },
    "solarThermalAreaAuto": {
        "Non": 0,
        "Oui": 1,
    },
    # "solarThermalArea": 10,
    "nbAppart": 0,
    "devEff": {
        "Meilleurs appareils": "best",
        "Appareils neufs courants": "new",
        "Anciens appareils (env. 5 ans)": "old5",
        "Très anciens appareils (>10 ans)": "old10",
    },
    "ventMeca": {
        "Aucune": "none",
        "Double flux": "df",
        "Simple flux": "sf",
    },
    "elevator": {
        "Non": 0,
        "Oui": 1,
    },
    "solarPV": {
        "Non": 0,
        "Oui": 1,
    },
    "pvAreaAuto": {
        "Non": 0,
        "Oui": 1,
    },
    "pvArea": 5.0,
    "pvOri": 7.0,
    "pvBattery": {
        "Non": 0,
        "Oui": 1,
    },
    # "protectionGrade": 0,
    "heatingWood": {
        "Non": 0,
        "Oui": 1,
    },
    "heatingProbes": {
        "Non": 0,
        "Oui": 1,
    },
    "solarRoof": {
        "Non": 0,
        "Oui": 1,
    },
}
