from paths import CH_DATA_DIR, DATA_DIR
import pandas as pd
import geopandas as gpd
from os.path import join, isfile, dirname, abspath, isdir
from os import listdir
# from IPython import embed
import sqlalchemy
import json
from tqdm import tqdm

NROWS = None

# CURRENT_DIR = dirname(abspath(__file__))
# DATA_DIR = join(CURRENT_DIR, "data")
# CH_DATA_DIR = join(DATA_DIR, "ch_data")
def post_data(
    engine_: sqlalchemy.engine.Engine,
    **kwargs,
):
    file = join(CH_DATA_DIR, "sub_data.csv")
    if not isdir(CH_DATA_DIR):
        msg = f"{listdir(DATA_DIR)}"
        raise ValueError(msg)
    # sub_data = pd.read_csv(file, nrows=NROWS, index_col=0)
    sub_data = pd.read_csv(file, nrows=10000, index_col=0)
    # if ids is not None:
    #     sub_data = sub_data[sub_data["fid"].isin(ids)]
    sub_data.to_sql(
        "data",
        engine_,
        if_exists="append",
        index=False,
        **kwargs,
    )
    # sql = text('SELECT * FROM public.data LIMI 10')
    # res = engine_.execute(sql)
    # print(res)
    print("post_data done")
    return list(set(sub_data["fid"]))


def post_spatial(
    engine_: sqlalchemy.engine.Engine,
    ids: list = None,
    **kwargs,
):
    file = join(CH_DATA_DIR, "spatial.shp")
    if not isdir(CH_DATA_DIR):
        msg = f"{listdir(CH_DATA_DIR)}"
        raise ValueError(msg)
    # spatial = gpd.read_file(file, rows=NROWS) 
    spatial = gpd.read_file(file) 
    spatial.to_crs(epsg=3035, inplace=True)
    spatial.drop_duplicates(subset=['fid'], inplace=True)
    if ids is not None:
        spatial = spatial[ spatial["fid"].isin(ids)]
    # from IPython import embed; embed(); exit()
    n = 1000  #chunk row size
    list_df = [spatial[i:i+n] for i in range(0, spatial.shape[0],n)]
    for dataframe_spatial in tqdm(list_df):
        dataframe_spatial.to_postgis(
        "spatial",
        engine_,
        if_exists="append",
        index=False,
        chunksize=1000,
        **kwargs,
    )
    # spatial.to_postgis(
    #     "spatial",
    #     engine_,
    #     if_exists="append",
    #     index=False,
    #     chunksize=1000,
    #     **kwargs,
    # )
    # sql = text('SELECT * FROM public.spatial LIMI 10')
    # res = engine_.execute(sql)
    # print(res)
    print("post_spatial done")
    return list(spatial.fid)


def post_datasets(    
    engine_: sqlalchemy.engine.Engine,
    **kwargs,):

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
    # sql = text('SELECT * FROM public.datasets LIMI 10')
    # res = engine_.execute(sql)
    # print(res)
    print("post_datasets done")

# if __name__ == "__main__" :

#     file = join(CH_DATA_DIR, "sub_data.csv")
#     if not isdir(CH_DATA_DIR):
#         msg = f"{listdir(DATA_DIR)}"
#         raise ValueError(msg)
#     sub_data = pd.read_csv(file, nrows=NROWS, index_col=0)

#     NROWS = 5000
#     file = join(CH_DATA_DIR, "spatial.shp")
#     if not isdir(CH_DATA_DIR):
#         msg = f"{listdir(CH_DATA_DIR)}"
#         raise ValueError(msg)
#     spatial = gpd.read_file(file, rows=NROWS) 
#     spatial.to_crs(epsg=3035, inplace=True)
#     spatial.drop_duplicates(subset=['fid'], inplace=True)

#     from IPython import embed; embed(); exit()
#     fids = list(spatial.fid)
#     sub_data.loc[ sub_data["fid"] == fids]