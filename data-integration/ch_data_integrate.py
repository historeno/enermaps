import json
from os import listdir
from os.path import isdir, join

import geopandas as gpd
import pandas as pd
import sqlalchemy
from tqdm import tqdm

from paths import CH_FINAL_RESULTS_DATA_DIR

NROWS = None


def post_data(
    engine_: sqlalchemy.engine.Engine,
    **kwargs,
):
    file = join(CH_FINAL_RESULTS_DATA_DIR, "sub_data.csv")
    if not isdir(CH_FINAL_RESULTS_DATA_DIR):
        msg = f"This directory does not exist : {CH_FINAL_RESULTS_DATA_DIR}"
        raise NotADirectoryError(msg)
    # sub_data = pd.read_csv(file, nrows=NROWS, index_col=0)
    sub_data = pd.read_csv(file, nrows=10000, index_col=0)
    sub_data.to_sql(
        "data",
        engine_,
        if_exists="append",
        index=False,
        **kwargs,
    )
    print("post_data done")
    return list(set(sub_data["fid"]))


def post_spatial(
    engine_: sqlalchemy.engine.Engine,
    ids: list = None,
    **kwargs,
):
    file = join(CH_FINAL_RESULTS_DATA_DIR, "spatial.shp")
    if not isdir(CH_FINAL_RESULTS_DATA_DIR):
        msg = f"This directory does not exist : {CH_FINAL_RESULTS_DATA_DIR}"
        raise NotADirectoryError(msg)
    # spatial = gpd.read_file(file, rows=NROWS)
    spatial = gpd.read_file(file)
    spatial.to_crs(epsg=3035, inplace=True)
    spatial.drop_duplicates(subset=["fid"], inplace=True)
    spatial = spatial[spatial["fid"].isin(ids)]
    n = 1000  # chunk row size
    list_df = [spatial[i : i + n] for i in range(0, spatial.shape[0], n)]
    for dataframe_spatial in tqdm(list_df):
        dataframe_spatial.to_postgis(
            "spatial",
            engine_,
            if_exists="append",
            index=False,
            chunksize=1000,
            **kwargs,
        )
    print("post_spatial done")
    return list(spatial.fid)


def post_datasets(
    engine_: sqlalchemy.engine.Engine,
    **kwargs,
):

    ds_id = 1

    # DATASETS TABLE
    data = {
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
    datasets = pd.DataFrame(data=data)
    datasets["metadata"] = datasets["metadata"].apply(json.dumps)
    datasets.to_sql(
        "datasets",
        engine_,
        if_exists="append",
        index=False,
        **kwargs,
    )
    print("post_datasets done")
