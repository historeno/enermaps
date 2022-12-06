from os.path import join, isdir, exists, isfile, basename 
from os import listdir, makedirs, remove
from paths import FOOTPRINT_DATA_DIR, CANTON_FOOTPRINT_CSV_DIR, ALL_CANTON_FOOTPRINT_DIR
from tqdm import tqdm
import fiona 
import geopandas as gpd
from shapely.ops import unary_union
import shapely
import requests
import pandas as pd
from zipfile import ZipFile


VALID_CANTON_ALIAS = ["be", "ge", "ju", "ne", "fr", "vd", "vs"]

def get_zipfile(
    url: str,
    zip_path: str,
    chunksize: int = 1024,
) -> str:
    """Fetch zip data from url."""
    response = requests.get(url, stream=True)
    with open(
        file=zip_path,
        mode="wb",
    ) as file:
        # total_length = int(response.headers.get("content-length"))
        # for chunk in progress.bar(
        #     response.iter_content(chunk_size=chunksize),
        #     expected_size=(total_length / chunksize) + 1,
        # ):
        for chunk in response.iter_content(chunk_size=chunksize):
            if chunk:
                file.write(chunk)
                file.flush()

def unzip(extraction_dir: str, zip_file: str, remove_orphans: bool = True) -> None:
    if not exists(extraction_dir):
        with ZipFile(zip_file, mode="r") as file:
            file.extractall(extraction_dir)
        # print("Extraction is done")
    # print("Extraction is already done")
    if exists(zip_file) and remove_orphans:
        remove(zip_file)

def dowload_footprint_data(force_download: bool = False):
    """
    Dowload the GDB files.
    Each file is saved in canton specific directory.
    Example : data/footprint_data/vs/*gdb/
    """
    for alias in VALID_CANTON_ALIAS:
        save_path = join(FOOTPRINT_DATA_DIR, f"{alias}")
        makedirs(save_path, exist_ok=True)
        msg = f"Downloading GDB files : {alias.upper()}"
        print(msg)
        csv_file = join(CANTON_FOOTPRINT_CSV_DIR, f"{alias}.csv")
        if not isfile(csv_file):
            msg = f"This file does not exist : {csv_file}."
            raise FileNotFoundError(msg)
        dataframe = pd.read_csv(csv_file, header=None)
        nrows, _ = dataframe.shape
        for row in range(nrows):
            url = dataframe[0].iloc[row]
            zip_filename = url.split("/")[-1]
            zip_path = join(save_path, zip_filename)
            extraction_dir = zip_path.replace(".zip", "")
            if exists(extraction_dir) or force_download:
                continue
            get_zipfile(
                url=url,
                zip_path=zip_path,
            )

            unzip(
                extraction_dir=extraction_dir,
                zip_file=zip_path,
                remove_orphans=True,
            )

def list_gdb_files() -> list:
    """List GDB files in data/footprint_data directory."""
    files = list()
    for canton in VALID_CANTON_ALIAS:
        # for canton_footprint_dir in listdir(FOOTPRINT_DATA_DIR):
        canton_dir = join(FOOTPRINT_DATA_DIR, canton)
        if not isdir(canton_dir):
            msg = f"This directory does not exist : {canton_dir}"
            raise DirectoryNotFound(msg)
        for first_gdb_file in listdir(canton_dir):
            first_gdb_dir = join(canton_dir, first_gdb_file)
            for second_gdb_file in listdir(first_gdb_dir):
                second_gdb_dir = join(first_gdb_dir, second_gdb_file) 
                files.append(second_gdb_dir)
    return files

def clean_column_names(dataframe: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """Change colunums name and reshape de geodataframe."""
    dataframe.drop(
        [
            "GRUND_AENDERUNG",
            "HERKUNFT",
            "HERKUNFT_MONAT",
            "HERKUNFT_JAHR",
            "ORIGINAL_HERKUNFT",
            "ERSTELLUNG_MONAT",
            "ERSTELLUNG_JAHR",
            "REVISION_JAHR",
            "REVISION_MONAT",
            "DATUM_ERSTELLUNG",
            # "modification_date",
            "GELAENDEPUNKT",
            "GESAMTHOEHE",
            "EGID",
        ],
        axis=1,
        inplace=True,
    )
    dataframe.rename(
        columns={
            "OBJEKTART": "category",
            "DATUM_AENDERUNG": "modification_date",
            "GEBAEUDE_NUTZUNG": "usage",
            # "OBJEKTART": "type",
            "NAME_KOMPLETT": "name",
        },
        inplace=True,
    )
    return dataframe

def extract_polygon(dataframe: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """Convert multipolygon into polygon and remove the z value of the coordinates."""
    dataframe.geometry = dataframe.geometry.apply(
        lambda multipolygon: unary_union(multipolygon)
    )
    dataframe.geometry = dataframe.geometry.apply(
        lambda shape: shapely.ops.transform(lambda x, y, z: (x, y), shape)
    )
    return dataframe.geometry

if __name__ == "__main__":
    dowload_footprint_data()
    gdb_files = list_gdb_files()
    for gdb_file in tqdm(gdb_files):
        if not isdir(gdb_file):
            msg = f"This directory does not exist : {gdb_file}"
            raise DirectoryNotFound(msg)
        gpkg_filename = basename(gdb_file).replace(".gdb", ".gpkg")
        filename = join(ALL_CANTON_FOOTPRINT_DIR, gpkg_filename)
        if isfile(filename):
            continue
        
        layers = fiona.listlayers(gdb_file)
        if "Floor" not in layers:
            continue
        features = [feature for feature in fiona.open(gdb_file, layer="Floor")]
        footprint_dataframe = gpd.GeoDataFrame.from_features(features)
        if footprint_dataframe is None:
            continue
        footprint_dataframe = clean_column_names(dataframe=footprint_dataframe)
        footprint_dataframe.geometry = extract_polygon(dataframe=footprint_dataframe)
        footprint_dataframe.set_crs(epsg=3035, inplace=True)        
        footprint_dataframe.to_file(filename, driver='GPKG', layer='Floor')  
