import geopandas as gpd
from paths import FOOTPRINT_DATA_DIR, INPUTS_DIR
from os.path import join
from IPython import embed
import time
import random
from legends import LEGENDS_UUID
import pandas as pd

import requests
import xmltodict
import math

from tqdm import tqdm
tqdm.pandas()

tic = time.perf_counter()

geopackage = join(FOOTPRINT_DATA_DIR, "merged_data_v2.gpkg")

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
all_data = gpd.read_file(geopackage, rows=10)


# DATASETS

# SPATIAL
ds_id = 1
spatial = all_data[["geometry", "egid", "canton"]].copy()
spatial["ds_id"] = ds_id
spatial["fid"] = spatial["canton"] + spatial["egid"].astype(str)
spatial.drop(["canton", "egid"], axis=1, inplace=True)
# TODO : missing empty field
spatial.to_pickle("spatial.pkl") 



# DATA
# translate function
def get_region(canton: str):
    return "Jura-FR"


def get_altitude():
    return 837


def get_meteo():
    return "Jura"


def get_context():
    return "Urban"


def get_footprint(geometry):
    geometries = list(geometry.geoms)
    if len(geometries) > 1:
        raise NotImplemented
    polygon = geometries[0]
    x, y = polygon.exterior.coords.xy
    coordinates = [list(element) for element in list(zip(x, y))]
    return f"{coordinates}"


def get_mitoyennete(geometry):
    geometries = list(geometry.geoms)
    if len(geometries) >= 2:
        raise NotImplemented
    polygon = geometries[0]
    x, y = polygon.exterior.coords.xy
    mitoyennete = [0 for _ in list(zip(x, y))]
    return f"{mitoyennete}"


def get_typology():
    url = "https://historeno.heig-vd.ch/tool/typo/typologies.xml"
    response = requests.get(url)
    dict_data = xmltodict.parse(response.content)
    data = dict_data["typologies"]["typo"]
    length = len(data)
    _max = max(1, length)
    return random.randint(0, _max)


def get_construction_year(construction_year):
    if not math.isnan(construction_year):
        return int(construction_year)
    else:
        return 1900


def get_category(category):
    file = join(INPUTS_DIR, "code_category.csv")
    data = pd.read_csv(file, sep=";")
    # embed()
    index =  data.loc[data["code regbl"] == int(category), "catégorie sia"].index[0]
    return data.loc[data["code regbl"] == int(category), "catégorie sia"][index]

def get_heigth(regbl_levels):
    if not math.isnan(regbl_levels):
        return int(regbl_levels) * 2.9
    else:
        return 3 * 2.9

def get_heating_systen(regbl_hot_water_source1):
    file = join(INPUTS_DIR, "code_heating_system.csv")
    data = pd.read_csv(file, sep=";")
    if regbl_hot_water_source1 is None:
        return "Mazout"
    else:
        index = data.loc[data["code regbl"] == int(regbl_hot_water_source1), "type de chauffage"].index[0]
        return data.loc[data["code regbl"] == int(regbl_hot_water_source1), "type de chauffage"][index]


def get_heating_systen_construction_year():
    return random.randint(1950, 2000)


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


def get_n_flat(category):
    file = join(INPUTS_DIR, "code_category.csv")
    data = pd.read_csv(file, sep=";")
    # embed()
    index = data.loc[data["code regbl"] == int(category), "nombre de logement"].index[0]
    number_of_flats = data.loc[data["code regbl"] == int(category), "nombre de logement"][index]
    if isinstance(number_of_flats, int) or isinstance(number_of_flats, float):
        return int(number_of_flats)
    else:
        return 1
    # return data.loc[data["code regbl"] == int(category), "nombre de logement"][0]


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
    return random.randint(1, 5)


# processing
all_data["ds_id"] = ds_id
all_data["fid"] = all_data["canton"] + all_data["egid"].astype(str)
# all_data["fields"] = all_data.apply(
all_data["fields"] = all_data.progress_apply(
    lambda row: {
        "Pays": "Suisse",
        "Region": get_region(canton=row["canton"]),
        "Altitude": get_altitude(),
        "Météo": get_meteo(),
        "Context": get_context(),
        "Empreinte au sol": get_footprint(geometry=row["geometry"]),
        "Mitoyenneté": get_mitoyennete(geometry=row["geometry"]),
        "Typologie": get_typology(),
        "Années de construction": get_construction_year(construction_year=row["construction_year"]),
        "Catégorie d'ouvrage": get_category(category=row["class"]),
        "Hauteur du bâtiment": get_heigth(regbl_levels=row["regbl_levels"]),
        "Type de chauffage": get_heating_systen(regbl_hot_water_source1=row["regbl_hot_water_source1"]),
        "Année d'installation du chauffage": get_heating_systen_construction_year(),
        "Type d'émetteurs": get_heating_emission_system(),
        "Régulation du chauffage": get_heating_emission_regulation_system(),
        "Isolation des conduites de chauffage": get_heating_pipes_insulated(),
        "Isolation des conduites d'ECS": get_dhw_pipes_insulated(),
        "Présence d'une installation solaire thermique": get_solar_thermal(regbl_heat_generator1=row["regbl_heat_generator1"]),
        "Surface de capteurs solaires thermiques automatique": "Oui",
        "Surface de capteurs solaires thermiques": "0",
        "Nombre de logements": get_n_flat(category=row["class"]),
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
all_data["value"] = 99999999999  # variable value
all_data["unit"] = "[-]"  # variable unit
all_data["start_at"] = "2022-06-30 12:00:00"
all_data["dt"] = None
all_data["z"] = None
all_data["israster"] = False
all_data["vis_id"] = LEGENDS_UUID[0]
sub_data = all_data[[
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
    "vis_id"
]]
sub_data.to_pickle("sub_data.pkl") 

# blocker
toc = time.perf_counter()
header = f"Downloaded the tutorial in {toc - tic:0.4f} seconds"
embed(header=header)
