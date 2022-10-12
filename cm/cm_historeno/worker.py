#!/usr/bin/env python3

import logging
from datetime import datetime

import requests
import xmltodict
from BaseCM import cm_base as cm_base
from BaseCM.cm_output import validate

from form import decoder

app = cm_base.get_default_app("historeno")
schema_path = cm_base.get_default_schema_path()
input_layers_path = cm_base.get_default_input_layers_path()
wiki = "http://www.historeno.eu/"


@app.task(
    base=cm_base.CMBase,
    bind=True,
    schema_path=schema_path,
    input_layers_path=input_layers_path,
    wiki=wiki,
)
def Module_Historeno(self, selection: dict, rasters: list, params: dict):
    def post_parameters():
        """Post on calculator to create task."""
        with open(f"parms_{datetime.now()}.txt", mode="w") as file:
            file.write(str(params))
        parameters = {
            "country": decoder.get("country").get(params["Pays"]),
            "canton": decoder.get("canton").get(params["Region"]),
            "altitude": params["Altitude"],  # not found
            "meteoParam": decoder.get("meteoParam").get(params["Météo"]),
            "context": decoder.get("context").get(params["Context"]),
            "polygon": "[[0,0],[0,10],[10,10],[10,0]]",
            "typo": params["Typologie"],  # not found
            "year": params["Années de construction"],
            "category": params["Catégorie d'ouvrage"],
            "height": params["Hauteur du bâtiment"],
            "generator": decoder.get("generator").get(params["Type de chauffage"]),
            "generatorYear": params["Année d'installation du chauffage"],
            "emettors": decoder.get("emettors").get(params["Type d'émetteurs"]),
            "regulation": decoder.get("regulation").get(
                params["Régulation du chauffage"]
            ),
            "tubeInsulH": decoder.get("tubeInsulH").get(
                params["Isolation des conduites de chauffage"]
            ),
            "tubeInsulW": decoder.get("tubeInsulW").get(
                params["Isolation des conduites d'ECS"]
            ),
            "solarThermal": decoder.get("solarThermal").get(
                params["Présence d'une installation solaire thermique"]
            ),
            "solarThermalAreaAuto": "Oui",
            "nbAppart": params["Nombre de logements"],
            "devEff": decoder.get("devEff").get(
                params["Efficacité des appareils électriques"]
            ),
            "ventMeca": decoder.get("ventMeca").get(
                params["Présence d'une ventilation mécanique"]
            ),
            "elevator": decoder.get("elevator").get(params["Présence d'ascenseur"]),
            "solarPV": decoder.get("solarPV").get(
                params["Présence d'une instalaltion solaire PV"]
            ),
            "pvAreaAuto": "Oui",
            "pvBattery": decoder.get("pvBattery").get(
                params["Présence de batteries de stockage"]
            ),
            # "renoLevel": params["Niveau de rénovation souhaité pour le scénario automatique"],
            "protectionGrade": params["Note de protection du patrimoine"],
            "renoMaxCost": params["Capacité d'investissement"],
        }
        url_endpoint = "https://historeno.heig-vd.ch/tool/calcPTF.php"
        try:
            resp = requests.post(url_endpoint, data=parameters)
            logging.info(f"RESULTS: {resp.status_code}")
            return resp
        except ConnectionError as error:
            logging.error("Error during the post of the file.")
            raise ConnectionError(error)

    res = post_parameters()
    ret = dict()
    ret["graphs"] = []
    ret["geofiles"] = {}
    parser = xmltodict.parse(res.content)
    # with open(f"res_{datetime.now()}.txt", mode="w") as file:
    #     file.write(str(res.content))
    values = parser["project"]
    ret["values"] = {
        "Classe de l'enveloppe": values["bldOutput"]["classEnv"],
        "Classe énergie primaire": values["bldOutput"]["classEp"],
        "Classe émissions gaz à effet de serre": values["bldOutput"]["classCO2"],
        "Besoin en chauffage [kWh/m²a]": round(float(values["bldOutput"]["Qh"]), 2),
        "Besoin en eau chaude sanitaire (ECS) [kWh/m²a]": round(float(values["bldOutput"]["Qw"]), 2),
        # "Coût totaux [CHF/Euro]": round(values["bldOutput"]["EnergyCost"], 2),
        # "Pertes par ventilation  [kWh]": round(values["bldOutput"]["Qv"], 2),
        # "Energie primaire non renouvelable totale [kWh]": round(values["bldOutput"]["NRE"], 2),
    }
    ret["warnings"] = {}

    return validate(ret)


if __name__ == "__main__":
    cm_base.start_app(app)
