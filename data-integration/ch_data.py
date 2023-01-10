"""
Module that create the files to be integrated.
"""

import json
import math
import random
import time
from os import remove
from os.path import isfile, join

import geopandas as gpd
import pandas as pd
import requests
import xmltodict
from IPython import embed
from tqdm import tqdm

from legends import LEGENDS_UUID
from paths import (CH_FINAL_RESULTS_DATA_DIR, CH_FOOTPRINT_DATA_DIR,
                   CH_REGBL_INPUTS_DIR)

tqdm.pandas()

error_file = "get_footprint_error.txt"
if isfile(error_file):
    remove(error_file)
error_file = "get_mitoyennete_error.txt"
if isfile(error_file):
    remove(error_file)

tic = time.perf_counter()

geopackage = join(CH_FOOTPRINT_DATA_DIR, "merged_data_v2.gpkg")

columns = [
    "egid",
    "canton",
    "commune",
    "building_type",
    "regbl_soruce",
    "category",
    "class",
    "construction_year",
    "regbl_surface",
    "regbl_volume",
    "regbl_levels",
    "regbl_sre",
    "regbl_heat_generator1",
    "regbl_heat_source1",
    "regbl_heat_generator2",
    "regbl_heat_source2",
    "regbl_hot_water_generator1",
    "regbl_hot_water_source1",
    "regbl_hot_water_generator2",
    "regbl_hot_water_source2",
    "geometry",
]
all_data = gpd.read_file(geopackage, rows=None)
all_data.drop_duplicates(["egid"], inplace=True)
all_data.dropna(subset=["class"], inplace=True)

# SPATIAL
ds_id = 1
spatial = all_data[["geometry", "egid", "canton"]].copy()
spatial["ds_id"] = ds_id
spatial["fid"] = spatial["canton"] + spatial["egid"].astype(str)
spatial.drop_duplicates(subset=["fid"], inplace=True)
spatial.drop(["canton", "egid"], axis=1, inplace=True)

save_file = join(CH_FINAL_RESULTS_DATA_DIR, "spatial.pkl")
spatial.to_pickle(save_file)

save_file = join(CH_FINAL_RESULTS_DATA_DIR, "spatial.shp")
spatial.to_file(save_file)

# DATA
def get_region(canton: str):
    return canton


def get_altitude():
    # TODO : get data from the DEM
    return 1700


# TODO : create a script based on spatial join
# def get_meteo():
#     return "Jura"


def get_context():
    # TODO : analyse the surrounding buildings
    return "suburban"


def get_footprint(geometry):
    geometries = list(geometry.geoms)

    if len(geometries) != 1:
        with open("get_footprint_error.txt", "a") as file:
            file.write("\n")
            file.write(f"geometries")
    polygon = geometries[0]
    x, y = polygon.exterior.coords.xy
    coordinates = [list(element) for element in list(zip(x, y))]
    return f"{coordinates}"


def get_mitoyennete(geometry):
    geometries = list(geometry.geoms)
    if len(geometries) != 1:
        with open("get_mitoyennete_error.txt", "a") as file:
            file.write("\n")
            file.write(f"geometries")
    polygon = geometries[0]
    x, y = polygon.exterior.coords.xy
    mitoyennete = [0 for _ in list(zip(x, y))]
    return f"{mitoyennete}"


def get_typology():
    # TODO : NOT DEFAULT VALUE, modifcation of the form (name - year)
    # try:
    #     url = "https://historeno.heig-vd.ch/tool/typo/typologies.xml"
    #     response = requests.get(url)
    #     dict_data = xmltodict.parse(response.content)
    #     data = dict_data["typologies"]["typo"]
    #     length = len(data)
    #     _max = max(1, length)
    #     return random.randint(1, _max)
    # except:
    #     return 1
    return 1


def get_construction_year(construction_year):
    if not math.isnan(construction_year):
        return int(construction_year)
    else:
        return 1900


def get_category(category, s):
    file = join(CH_REGBL_INPUTS_DIR, "code_category.csv")
    data = pd.read_csv(file, sep=";")
    try:
        index = data.loc[data["code regbl"] == int(category), "catégorie sia"].index[0]
    except:
        embed(header="get category")
    return data.loc[data["code regbl"] == int(category), "catégorie sia"][index]


def get_heigth(regbl_levels):
    if not math.isnan(regbl_levels):
        return int(regbl_levels) * 2.9
    else:
        return 3 * 2.9


def get_heating_systen(regbl_hot_water_source1):
    file = join(CH_REGBL_INPUTS_DIR, "code_heating_system.csv")
    data = pd.read_csv(file, sep=";")
    if regbl_hot_water_source1 is None:
        return "Mazout"
    else:
        index = data.loc[
            data["code regbl"] == int(regbl_hot_water_source1), "type de chauffage"
        ].index[0]
        return data.loc[
            data["code regbl"] == int(regbl_hot_water_source1), "type de chauffage"
        ][index]


def get_heating_systen_construction_year():
    return 2000


def get_heating_emission_system():
    return "Radiateurs"


def get_heating_emission_regulation_system():
    return "autre (+2°C)"


def get_heating_pipes_insulated():
    return "Non"


def get_dhw_pipes_insulated():
    return "Non isolées"


def get_solar_thermal(regbl_heat_generator1):
    if math.isnan(regbl_heat_generator1):
        return "Non"
    elif int(regbl_heat_generator1) == 7420 or int(regbl_heat_generator1) == 7421:
        return "Oui"
    else:
        return "Non"


def get_n_flat(category, sre):
    if isinstance(sre, float):
        return sre / 100
    file = join(CH_REGBL_INPUTS_DIR, "code_category.csv")
    data = pd.read_csv(file, sep=";")
    index = data.loc[data["code regbl"] == int(category), "nombre de logement"].index[0]
    number_of_flats = data.loc[
        data["code regbl"] == int(category), "nombre de logement"
    ][index]
    if isinstance(number_of_flats, int) or isinstance(number_of_flats, float):
        return int(number_of_flats)
    else:
        return 1


def get_eletric_device_efficiency():
    return "Très anciens appareils"


def get_mecanic_ventilation():
    return "Aucune"


def get_elevator():
    return "Non"


def get_pv():
    return "Non"


def get_electricity_battery():
    return "Non"


def get_protection_level():
    # TODO: add data from cantonal GIS web
    # application, empty in the front end for the moment
    # return random.randint(1, 5)
    return 1  # high protection level by default


all_data["ds_id"] = ds_id
all_data["fid"] = all_data["canton"] + all_data["egid"].astype(str)
all_data["fields"] = all_data.progress_apply(
    lambda row: {
        "Pays": "Suisse",
        "Region": get_region(canton=row["canton"]),  # TODO : 1ST PRIORITY
        "Altitude": get_altitude(),
        # "Météo": get_meteo(), # NOT NEEDED
        "Context": get_context(),
        "Empreinte au sol": get_footprint(geometry=row["geometry"]),
        "Mitoyenneté": get_mitoyennete(geometry=row["geometry"]),  # TODO : 2ND PRIORITY
        "Typologie": get_typology(),
        "Années de construction": get_construction_year(
            construction_year=row["construction_year"]
        ),
        "Catégorie d'ouvrage": get_category(category=row["class"], s=row["fid"]),
        "Hauteur du bâtiment": get_heigth(regbl_levels=row["regbl_levels"]),
        "Type de chauffage": get_heating_systen(
            regbl_hot_water_source1=row["regbl_hot_water_source1"]
        ),
        "Année d'installation du chauffage": get_heating_systen_construction_year(),
        "Type d'émetteurs": get_heating_emission_system(),
        "Régulation du chauffage": get_heating_emission_regulation_system(),
        "Isolation des conduites de chauffage": get_heating_pipes_insulated(),
        "Isolation des conduites d'ECS": get_dhw_pipes_insulated(),
        "Présence d'une installation solaire thermique": get_solar_thermal(
            regbl_heat_generator1=row["regbl_heat_generator1"]
        ),
        "Surface de capteurs solaires thermiques automatique": "Oui",
        "Surface de capteurs solaires thermiques": "0",
        "Nombre de logements": get_n_flat(category=row["class"], sre=row["regbl_sre"]),
        "Efficacité des appareils électriques": get_eletric_device_efficiency(),
        "Présence d'une ventilation mécanique": get_mecanic_ventilation(),
        "Présence d'ascenseur": get_elevator(),
        "Présence d'une instalaltion solaire PV": get_pv(),
        "Surface PV automatique": "Oui",
        "Présence de batteries de stockage": get_electricity_battery(),
        "Note de protection du patrimoine": get_protection_level(),
        "Capacité d'investissement": 0,
    },
    axis=1,
)
all_data["variable"] = "Niveau de protection"  # variable name
all_data["value"] = 0  # variable value
all_data["unit"] = "[-]"  # variable unit
all_data["start_at"] = "2022-06-30 12:00:00"
all_data["dt"] = None
all_data["z"] = None
all_data["israster"] = False
all_data["vis_id"] = LEGENDS_UUID[0]
sub_data = all_data[
    [
        "ds_id",
        "fid",
        "fields",
        "variable",
        "value",
        "unit",
        "start_at",
        "dt",
        "z",
        "israster",
        "vis_id",
    ]
]
save_file = join(CH_FINAL_RESULTS_DATA_DIR, "sub_data.pkl")
sub_data.to_pickle(save_file)

save_file = join(CH_FINAL_RESULTS_DATA_DIR, "sub_data.csv")
sub_data.to_csv(save_file)

# blocker
toc = time.perf_counter()
header = f"Downloaded the tutorial in {toc - tic:0.4f} seconds"
# embed(header=header)
print(header)
