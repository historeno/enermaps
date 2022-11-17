import json
import random
import sys
import zipfile
from os import chdir, makedirs, remove, system, listdir
from os.path import exists, join

import fiona
import geopandas as gpd

# import matplotlib.pyplot as plt
import pandas as pd
import requests
from clint.textui import progress

# from IPython import embed
from shapely.ops import cascaded_union

from legends import LEGENDS_UUID
from paths import REGBL_DATA_DIR, FOOTPRINT_DATA_DIR, CANTON_FOOTPRINT_CSVS_DIR
from tqdm import tqdm
import fiona
import geopandas as gpd
from tqdm import tqdm
import os

VALID_CANTON_ALIAS = ["be", "ge", "ju", "ne", "vd", "vs"]


def unzip(extraction_dir: str, zip_file: str, remove_orphans: bool = True) -> None:
    if not exists(extraction_dir):
        with zipfile.ZipFile(zip_file, mode="r") as file:
            file.extractall(extraction_dir)
        print("Extraction is done")
    print("Extraction is already done")
    if exists(zip_file) and remove_orphans:
        remove(zip_file)


# DATA TABLE
def download_regbl(NROWS: int = 100) -> pd.DataFrame:  # TODO : limiter
    print("start dowload regbl")

    def get_regbl_commands() -> str:
        """Find the command based on the OS."""
        commands = dict()
        for alias in VALID_CANTON_ALIAS:
            BASE_URL = f"https://public.madd.bfs.admin.ch/{alias}.zip"
            ZIP_FILE = alias + ".zip"

            if sys.platform.startswith(
                "linux"
            ):  # could be "linux", "linux2", "linux3", ...
                # linux
                command = f'curl -J -O -o "{ZIP_FILE}" "{BASE_URL}"'
            elif sys.platform == "win32":
                # Windows (either 32-bit or 64-bit)
                command = f'powershell Invoke-WebRequest -Uri "{BASE_URL}" -OutFile "{ZIP_FILE}"'
            else:
                raise OSError("This OS is not supported.")
            commands[ZIP_FILE] = command
        return commands

    def read_regbl_data(extraction_dir: str, nrows: int = NROWS) -> pd.DataFrame:
        """Reads building CSV."""
        building_file = join(extraction_dir, "gebaeude_batiment_edificio.csv")
        building = pd.read_csv(building_file, nrows=nrows, sep="\t")
        return building

    # change dir
    makedirs(REGBL_DATA_DIR, exist_ok=True)
    chdir(REGBL_DATA_DIR)

    # parse commands
    dataframes = list()
    commands = get_regbl_commands()
    for regbl_zip_file, command in tqdm(commands.items()):
        zip_path = join(REGBL_DATA_DIR, regbl_zip_file)
        zip_extraction_dir = zip_path.replace(".zip", "")
        if not exists(zip_extraction_dir):
            system(command=command)
            unzip(extraction_dir=zip_extraction_dir, zip_file=zip_path)
            print("Download is done")
        print("Download is already done")
        dataframe = read_regbl_data(extraction_dir=zip_extraction_dir)
        dataframes.append(dataframe)
    return pd.concat(dataframes, ignore_index=True)


def set_data_table(regbl: pd.DataFrame) -> pd.DataFrame:
    print("start settng data table")

    def set_fields(row: pd.Series) -> str:
        def heating_system(code: float):
            if code == 7530:
                return "mazout"
            elif code == 7520:
                return "Gas naturel"
            elif code == 7542:
                return "pellets"
            elif code == 7541:
                return "büches bois"
            elif code == 7543:
                return "copeaux bois"
            elif code in [7501]:
                return "PAC air-eau"
            elif code in [7510, 7511, 7511, 7513]:
                return "PAC sol-eau"
            elif code == None:  # no information in REGBL
                return "électrique direct"
            elif code in [7580, 7581, 7582]:
                return "chauffage à distance"
            elif code == 7500:
                return "Aucun"
            elif code == 7599:
                return "Autre"
            else:
                return None

        def region(code: float):
            ## TODO : maybe need to be updated
            if code == None:
                return None
            else:
                return code

        def altitude():
            return random.randint(800, 1980)

        def weather(code: float):
            if code == "VD":
                return "Jura"  # "Préalpes"
            elif code == "VS":
                return "dégagé vers le sud"  # bouché vers le sud
            else:
                return None

        def context():
            return random.choice(["rural", "urban", "suburban"])

        def category(code: float):
            """
            data from the REGBL:

            1273	GKLAS	Monument historique ou classé
            1274	GKLAS	Autre bâtiment non classé ailleur
            """
            if code in [1121, 1122, 1130, 1211, 1212, 1275]:
                return 1  # h. collectif
            if code == 1110:
                return 2  # h. indv.
            if code == 1220:
                return 3  # administration
            if code == 1263:
                return 4  # école
            if code == 1230:
                return 5  # commerce
            if code == 1231:
                return 6  # restaurant
            if code in [1261, 1262, 1272]:
                return 7  # lieux de rassemblement
            if code == 1264:
                return 8  # hopitaux
            if code == 1251:
                return 9  # industrie
            if code in [1241, 1242, 1252, 1271, 1276, 1277, 1278]:
                return 10  # dépôts
            if code == 1265:
                return 11  # installation sportive
            if code == None:  # not define in REGBL
                return 12  # piscine couverte
            else:
                return None

        def protection_level():
            return random.randint(0, 4)

        fields = {}
        fields["Pays"] = "Suisse"
        fields["Region"] = region(code=row.GDEKT)
        fields["Altitude"] = altitude()
        fields["Météo"] = weather(code=row.GDEKT)
        fields["Context"] = context()
        fields["Empreinte au sol"] = ""  # come from footprint
        fields["Mitoyenneté"] = ""  # come from foot print
        fields["Typologie"] = ""  # see harmonization
        fields["Années de construction"] = row.GBAUJ
        fields["Catégorie d'ouvrage"] = category(code=row.GKLAS)
        fields["Hauteur du bâtiment"] = random.randint(1950, 1980)
        fields["Type de chauffage"] = heating_system(code=row.GENH1)
        fields["Année d'installation du chauffage"] = 1900  # not in the REGBL
        fields["Type d'émetteurs"] = "Radiateurs"
        fields["Régulation du chauffage"] = "autre (+2°C)"
        fields["Isolation des conduites de chauffage"] = "Non"
        fields["Isolation des conduites d'ECS"] = "Non isolées"
        fields["Présence d'une installation solaire thermique"] = "Non"
        fields["Surface de capteurs solaires thermiques automatique"] = "Oui"
        fields["Surface de capteurs solaires thermiques"] = "Oui"
        fields["Nombre de logements"] = 1
        fields["Efficacité des appareils électriques"] = "Meilleurs appareils"
        fields["Présence d'une ventilation mécanique"] = "Aucune"
        fields["Présence d'ascenseur"] = "Non"
        fields["Présence d'une instalaltion solaire PV"] = "Non"
        fields["Surface PV automatique"] = "Oui"
        fields["Présence de batteries de stockage"] = "None"
        fields["Note de protection du patrimoine"] = protection_level()
        fields["Capacité d'investissement"] = 0
        return json.dumps(fields)

    data_dataframe = pd.DataFrame()
    data_dataframe["index"] = regbl["EGID"]
    data_dataframe["ds_id"] = 1
    data_dataframe["fid"] = regbl.apply(
        lambda row: row.GDEKT + str(row.EGID),
        axis=1,
    )
    data_dataframe["variable"] = "Niveau de protection"
    data_dataframe["value"] = ""  # note patrimoniale
    data_dataframe["unit"] = "[-]"
    data_dataframe["start_at"] = "2022-06-30 12:00:00"
    # data_dataframe["fields"] = "" # create fields
    data_dataframe["fields"] = regbl.apply(
        lambda row: set_fields(row=row),
        axis=1,
    )
    data_dataframe["dt"] = None
    data_dataframe["z"] = None
    data_dataframe["israster"] = False
    data_dataframe["vis_id"] = str(LEGENDS_UUID[0])
    return data_dataframe


# SPATIAL TABLE
def get_zipped_fooprint_data(
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
        total_length = int(response.headers.get("content-length"))
        for chunk in progress.bar(
            response.iter_content(chunk_size=chunksize),
            expected_size=(total_length / chunksize) + 1,
        ):
            if chunk:
                file.write(chunk)
                file.flush()


def dowload_footprint_data(force_download: bool = False):
    """Dowload the GDB files."""
    for alias in VALID_CANTON_ALIAS:
        csv_file = join(CANTON_FOOTPRINT_CSVS_DIR, f"{alias}.csv")
        dataframe = pd.read_csv(csv_file, header=None)
        nrows, _ = dataframe.shape
        for row in range(nrows):
            url = dataframe[0].iloc[row]
            zip_filename = url.split("/")[-1]
            save_path = join(FOOTPRINT_DATA_DIR, f"{alias}")
            makedirs(save_path, exist_ok=True)
            zip_path = join(save_path, zip_filename)
            extraction_dir = zip_path.replace(".zip", "")
            if exists(extraction_dir) or force_download:
                break
            get_zipped_fooprint_data(
                url=url,
                zip_path=zip_path,
            )

            unzip(
                extraction_dir=extraction_dir,
                zip_file=zip_path,
                remove_orphans=True,
            )

            # TODO : BREAKER
            # TODO : BREAKER
            # TODO : BREAKER
            break


def lsit_gdb_files() -> list:
    """List GDB files."""
    _gdb_files = list()
    for canton_footprint_dir in listdir(FOOTPRINT_DATA_DIR):
        cantondir_dir = join(FOOTPRINT_DATA_DIR, canton_footprint_dir)
        for first_gdb_dir in listdir(cantondir_dir):
            second_gdb_dir = join(
                FOOTPRINT_DATA_DIR, canton_footprint_dir, first_gdb_dir
            )
            for file in listdir(second_gdb_dir):
                _file = join(second_gdb_dir, file)
                _gdb_files.append(_file)
    return _gdb_files


def read_footprint_data(gdb_directory, layer: str = None) -> gpd.GeoDataFrame:
    """Turn GDB directory into GeoDataFrame (for a specific layer)."""
    layers = fiona.listlayers(gdb_directory)
    if layer in layers or layer is None:
        features = [feature for feature in fiona.open(gdb_directory, layer=layer)]
    else:
        raise NotImplemented
    return gpd.GeoDataFrame.from_features(features)


def extract_polygon(
    dataframe: gpd.GeoDataFrame,
) -> gpd.GeoDataFrame:
    """Convert multipolygon into polygon."""
    dataframe.geometry = dataframe.geometry.apply(
        lambda multipolygon: cascaded_union(multipolygon)
    )
    return dataframe.geometry


def clean_column_names(dataframe: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
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


def to_database(dataframe: gpd.GeoDataFrame) -> None:
    from utilities import get_engine

    # create engine
    engine = get_engine()

    # table
    table_name = "footprint"
    primary_key = "UUID"

    dataframe.to_postgis(
        name=table_name,
        con=engine.connect(),
        if_exists="append",
        index=False,
    )

    # with engine.connect() as con:
    #     con.execute('ALTER TABLE `example_table` ADD PRIMARY KEY (`ID_column`);')
    pass


def spatial_join(footprint: gpd.GeoDataFrame, regbl: gpd.GeoDataFrame, prefix_fd: str):
    regbl = regbl.drop(
        [
            # "EGID",
            "GDEKT",
            "GGDENR",
            "GGDENAME",
            "EGRID",
            "LGBKR",
            "LPARZ",
            "LPARZSX",
            "LTYP",
            "GEBNR",
            "GBEZ",
            "GKSCE",
            "GSTAT",
            "GKAT",
            "GKLAS",
            "GBAUJ",
            "GBAUM",
            "GBAUP",
            "GABBJ",
            "GAREA",
            "GVOL",
            "GVOLNORM",
            "GVOLSCE",
            "GASTW",
            "GANZWHG",
            "GAZZI",
            "GSCHUTZR",
            "GEBF",
            "GWAERZH1",
            "GENH1",
            "GWAERSCEH1",
            "GWAERDATH1",
            "GWAERZH2",
            "GENH2",
            "GWAERSCEH2",
            "GWAERDATH2",
            "GWAERZW1",
            "GENW1",
            "GWAERSCEW1",
            "GWAERDATW1",
            "GWAERZW2",
            "GENW2",
            "GWAERSCEW2",
            "GWAERDATW2",
            "GEXPDAT",
        ],
        axis=1,
    )
    regbl = regbl.rename(
        columns={
            "GKODE": "x",
            "GKODN": "y",
        }
    )
    geometry = gpd.points_from_xy(regbl.x, regbl.y, crs="EPSG:2056")
    regbl = gpd.GeoDataFrame(
        regbl, 
        geometry=geometry
    )
    regbl.to_crs(3035, inplace=True)
    spatial = footprint.sjoin(regbl, how="left").drop_duplicates(subset=['UUID'])
    # spatial.EGID = 1
    # from IPython import embed
    # embed()
    # exit()
    spatial = spatial[spatial['EGID'].notna()]
    spatial.ds_id = 1
    spatial.EGID = spatial.EGID.apply(lambda egid: prefix_fd + str(egid)) 
    spatial.drop(
        [
            "category",
            "name",
            "usage",
            "index_right",
            "x",
            "y",
            "modification_date",
            "UUID",
            # "EGID"
        ],
        axis=1,
        inplace=True,
    )
    spatial.rename(
        columns={
            "EGID": "fid"
        },
        inplace=True,
    )
    # from IPython import embed
    # embed()
    # exit()
    return spatial


def main():
    dowload_footprint_data()
    gdb_files = lsit_gdb_files()
    for gdb_file in gdb_files:
        dataframe = read_footprint_data(gdb_directory=gdb_file, layer="Floor")
        dataframe = clean_column_names(dataframe=dataframe)
        dataframe.geometry = extract_polygon(dataframe=dataframe)
        dataframe.set_crs(epsg=3035, inplace=True)
        for alias in VALID_CANTON_ALIAS:
            if alias in gdb_file.split(os.sep):
                PREFIX_FID = alias.upper()
        spatial = spatial_join(footprint=dataframe, regbl=download_regbl(NROWS=None), prefix_fd=PREFIX_FID)
        from IPython import embed
        embed()
        exit()
        exit()
        to_database(dataframe=dataframe)


# def set_spatial_table(footprint: pd.DataFrame) -> pd.DataFrame:
#     print("start setting spatial table")
#     spatial_dataframe = pd.DataFrame()
#     spatial_dataframe["geometry"] = footprint["geometry"]
#     spatial_dataframe["ds_id"] = 1
#     spatial_dataframe["fid"] = ""
#     spatial_dataframe["levl_code"] = "geometry"
#     spatial_dataframe["cntr_code"] = None
#     spatial_dataframe["name_engl"] = None
#     spatial_dataframe["name"] = None

if __name__ == "__main__":
    main()
    # download regbl
    # regbl = download_regbl()

    # DATASETS
    # Have been already added

    # DATA
    # data = set_data_table(regbl=regbl)

    # SPATIAL
    pass
