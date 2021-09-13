#!/usr/bin/env python3
"""
Integrate JRC PPDB DB into EnerMaps DB.
Use datapackage to check for updates.

@author: giuseppeperonato
"""

import json
import logging
import os
import sys

import frictionless
import geopandas as gpd
import numpy as np
import pandas as pd
import utilities
from pandas_datapackage_reader import read_datapackage

# Constants
logging.basicConfig(level=logging.INFO)

VALUE_VARS = ["capacity_p", "capacity_g"]
ID_VARS = ["fid", "fields"]
ID = "index"
SPATIAL_VARS = ["lat", "lon"]
UNIT = "MW"
ISRASTER = False
RESOURCE_IDX = 0
RESOURCE_NAME = "units"

DB_URL = utilities.DB_URL


def get(url: str, dp: frictionless.package.Package, force: bool = False):
    """
    Retrieve data and check update.
    Parameters
    ----------
    url : str
        URL of the Gitlab repository (raw).
    dp : frictionless.package.Package
        Datapackage against which validating the data.
    force : Boolean, optional
        If True, new data will be uploaded even if the same as in the db. The default is False.
    Returns
    -------
    DataFrame
        Data in EnerMaps format.
    frictionless.package.Package
        Pakage descring the data.
    """
    new_dp = frictionless.Package(url + "datapackage.json")

    # Make sure to read the csv file from remote
    new_dp.resources[RESOURCE_IDX]["path"] = url + new_dp.resources[0]["path"]
    new_dp.resources[RESOURCE_IDX]["scheme"] = "https"

    isChangedStats = False  # initialize check

    name = new_dp["name"]

    # Inferring and completing metadata
    logging.info("Creating datapackage for input data")

    # Logic for update
    if dp is not None:  # Existing dataset
        # check stats
        if "stats" in dp["resources"][RESOURCE_IDX].keys():
            isChangedStats = (
                dp["resources"][RESOURCE_IDX]["stats"]
                != new_dp["resources"][RESOURCE_IDX]["stats"]
            )
        else:
            isChangedStats = False
        isChangedVersion = dp["version"] != new_dp["version"]
        if (
            isChangedStats or isChangedVersion
        ):  # Data integration will continue, regardless of force argument
            logging.info("Data has changed")
            if utilities.isDPvalid(dp, new_dp):
                enermaps_data, spatial = prepare(new_dp, name)
        elif force:  # Data integration will continue, even if data has not changed
            logging.info("Forced update")
            if utilities.isDPvalid(dp, new_dp):
                enermaps_data, spatial = prepare(new_dp, name)
        else:  # Data integration will stop here, returning Nones
            logging.info("Data has not changed. Use --force if you want to reupload.")
            return None, None, None
    else:  # New dataset
        dp = new_dp  # this is just for the sake of the schema control
        if utilities.isDPvalid(dp, new_dp):
            enermaps_data, spatial = prepare(new_dp, name)

    return enermaps_data, spatial, new_dp


def prepare(dp: frictionless.package.Package, name: str):
    """

    Prepare data in EnerMaps format.

    Parameters
    ----------
    dp : frictionless.package.Package
        Valid datapackage
    name : str
        Name of the dataset (used for constructing the FID)

    Returns
    -------
    DataFrame
        Data in EnerMaps format.
    GeoDataFrame
        Spatial data in EnerMaps format.

    """
    data = read_datapackage(dp, RESOURCE_NAME)
    if ID == "index":
        data["fid"] = name + "_" + data.index.astype(str)
    else:
        data["fid"] = name + "_" + data[ID].astype(str)

    spatial = gpd.GeoDataFrame(
        data["fid"],
        columns=["fid"],
        geometry=gpd.points_from_xy(data[SPATIAL_VARS[1]], data[SPATIAL_VARS[0]]),
        crs="EPSG:4326",
    )

    # Other fields to json
    def np_encoder(object):
        """Source: https://stackoverflow.com/a/65151218."""
        if isinstance(object, np.generic):
            return object.item()

    other_cols = [
        x for x in data.columns if x not in VALUE_VARS + SPATIAL_VARS + ID_VARS
    ]

    # Int64 to int
    data.loc[:, other_cols].loc[:, data[other_cols].dtypes == "int64"] = (
        data.loc[:, other_cols].loc[:, data[other_cols].dtypes == "int64"].astype(int)
    )
    data = data.replace({np.nan: None})
    data["fields"] = data[other_cols].to_dict(orient="records")
    data["fields"] = data["fields"].apply(lambda x: json.dumps(x, default=np_encoder))

    # Unpivoting
    data = data.melt(id_vars=["fid", "fields"], value_vars=VALUE_VARS)

    # Remove nan
    data = data.dropna()

    # Conversion
    enermaps_data = utilities.ENERMAPS_DF
    enermaps_data["fid"] = data["fid"]
    enermaps_data["value"] = data["value"]
    enermaps_data["variable"] = data["variable"]
    enermaps_data["fields"] = data["fields"]
    enermaps_data["unit"] = UNIT
    enermaps_data["israster"] = ISRASTER

    return enermaps_data, spatial


if __name__ == "__main__":
    datasets = pd.read_csv("datasets.csv", index_col=[0])
    script_name = os.path.basename(sys.argv[0])
    ds_ids, isForced = utilities.parser(script_name, datasets)
    url = datasets.loc[
        datasets["di_script"] == os.path.basename(sys.argv[0]), "di_URL"
    ].values[0]
    for ds_id in ds_ids:
        dp = utilities.getDataPackage(ds_id, DB_URL)

        data, spatial, dp = get(url=url, dp=dp, force=isForced)

        if isinstance(data, pd.DataFrame):
            # Remove existing dataset
            if utilities.datasetExists(ds_id, DB_URL,):
                utilities.removeDataset(ds_id, DB_URL)
                logging.info("Removed existing dataset")

            # Create dataset table
            metadata = datasets.loc[ds_id].fillna("").to_dict()
            metadata["datapackage"] = dp
            metadata = json.dumps(metadata)
            dataset = pd.DataFrame([{"ds_id": ds_id, "metadata": metadata}])
            utilities.toPostgreSQL(
                dataset, DB_URL, schema="datasets",
            )

            # Create data table
            data["ds_id"] = ds_id
            utilities.toPostgreSQL(
                data, DB_URL, schema="data",
            )

            # Create spatial table
            spatial = spatial.to_crs("EPSG:3035")
            spatial["ds_id"] = ds_id
            utilities.toPostGIS(
                spatial, DB_URL, schema="spatial",
            )
