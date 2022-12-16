import json
import random
from os.path import isfile, join

import geopandas as gpd
import pandas as pd
import shapely
import sqlalchemy

from legends import LEGENDS_UUID
from paths import FAKE_DATA_DIR


def read_data() -> gpd.GeoDataFrame:
    file = join(FAKE_DATA_DIR, "datasets.shp")
    if not isfile(file):
        raise FileExistsError(file)
    dataframe = gpd.read_file(filename=file)
    return dataframe


def post_data(
    data: gpd.GeoDataFrame,
    engine_: sqlalchemy.engine.Engine,
    **kwargs,
) -> None:
    ds_id = 1

    # DATASETS TABLE
    d = {
        "ds_id": [ds_id],
        "metadata": [
            {
                "Group": "Bâtiment",
                "Title": "Bâtiments existants",
                "parameters": {
                    "end_at": "2015-12-31 23:00",
                    "fields": [],
                    "levels": [],  # mandatory
                    "is_raster": False,
                    "start_at": "2021-06-30 12:00:00",
                    "is_tiled": False,
                    "variables": ["Niveau de protection"],  # mandatory
                    "time_periods": [],  # mandatory
                    "temporal_granularity": "hour",
                },
            }
        ],
    }
    datasets = pd.DataFrame(data=d)
    datasets["metadata"] = datasets["metadata"].apply(json.dumps)
    datasets.to_sql(
        "datasets",
        engine_,
        if_exists="append",
        index=False,
        **kwargs,
    )

    # SPATIAL TABLE
    spatial_data = data.copy(deep=True)
    spatial_data = spatial_data[["geometry"]]
    spatial_data["geometry"] = spatial_data["geometry"].apply(
        lambda shape: shapely.ops.transform(lambda x, y, z: (x, y), shape)
    )
    spatial_data["ds_id"] = [ds_id for _ in range(spatial_data.shape[0])]
    spatial_data["fid"] = [f"FR_{fid}" for fid in range(spatial_data.shape[0])]
    spatial_data["levl_code"] = ["geometry" for fid in range(spatial_data.shape[0])]
    spatial_data["cntr_code"] = [None for _ in range(spatial_data.shape[0])]
    spatial_data["name_engl"] = [None for _ in range(spatial_data.shape[0])]
    spatial_data["name"] = [None for _ in range(spatial_data.shape[0])]

    spatial_data.to_postgis(
        "spatial",
        engine_,
        if_exists="append",
        index=False,
        **kwargs,
    )

    # DATA TABLE
    rows = spatial_data.shape[0]
    fields = [
        {
            "Besoin": str(sre) + " kWh",
            "Demande": str(sre) + " kWh",
            "Pays": "France",
            "Region": "Jura-FR",
            "Altitude": 837,
            "Météo": "Jura",
            "Context": "Urban",
            "Empreinte au sol": "[[6.6366674,46.5174068],[6.6367499,46.5173885],"
            "[6.6367136,46.5173010],[6.6368834,46.5172600],"
            "[6.6369874,46.5174985],[6.6367287,46.5175586],"
            "[6.6366674,46.5174068]]",
            "Mitoyenneté": "[0,0,0.5,0]",
            "Typologie": random.randint(1, 2),
            "Années de construction": random.randint(1950, 1980),
            "Catégorie d'ouvrage": random.randint(1, 12),
            "Hauteur du bâtiment": random.randint(3, 12),
            "Type de chauffage": "Mazout",
            "Année d'installation du chauffage": random.randint(1950, 2000),
            "Type d'émetteurs": "Murs chauffants",
            "Régulation du chauffage": "autre (+2°C)",
            "Isolation des conduites de chauffage": "Non",
            "Isolation des conduites d'ECS": "Non isolées",
            "Présence d'une installation solaire thermique": random.choice(
                ["Oui", "Non"]
            ),
            "Surface de capteurs solaires thermiques automatique": "Oui",
            "Surface de capteurs solaires thermiques": "Oui",
            "Nombre de logements": random.randint(1, 4),
            "Efficacité des appareils électriques": "Meilleurs appareils",
            "Présence d'une ventilation mécanique": "Aucune",
            "Présence d'ascenseur": random.choice(["Oui", "Non"]),
            "Présence d'une instalaltion solaire PV": "Non",
            "Surface PV automatique": "Oui",
            "Présence de batteries de stockage": "Non",
            "Note de protection du patrimoine": random.randint(1, 5),
            "Capacité d'investissement": 0,
        }
        for sre in range(rows)
    ]

    d = {
        "index": [index for index in range(rows)],
        "ds_id": [ds_id for _ in range(rows)],
        "fid": [f"FR_{fid}" for fid in range(rows)],
        "variable": ["Niveau de protection" for _ in range(rows)],  # variable name
        "value": [
            building["Note de protection du patrimoine"] for building in fields
        ],  # variable value
        "unit": ["[-]" for _ in range(rows)],  # variable unit
        "start_at": ["2022-06-30 12:00:00" for _ in range(rows)],
        "fields": fields,
        "dt": [None for _ in range(rows)],
        "z": [None for _ in range(rows)],
        "israster": [False for _ in range(rows)],
        "vis_id": [LEGENDS_UUID for _ in range(rows)],
    }
    data_data = pd.DataFrame(data=d)
    data_data["fields"] = data_data["fields"].apply(json.dumps)

    data_data.to_sql(
        "data",
        engine_,
        if_exists="append",
        index=False,
        **kwargs,
    )
    print("FAKE DATA POST")