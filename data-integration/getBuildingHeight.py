#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prepare the Building Height dataset for EnerMaps.

Note that the  files must be downloaded from Copernicus (requires log-in)
and extracted in the data/31 directory.
This script expects that the original zip file from Copernicus is extracted
in multiple zip files.
Created on Wed June 02 12:50:00 2021

@author: giuseppeperonato
"""

import glob
import json
import logging
import os
import pathlib
import shutil
import sys

import geopandas as gpd
import pandas as pd
import utilities
from osgeo import gdal, osr
from pyproj import CRS
from shapely.geometry import box

N_FILES = 38
ISRASTER = True
logging.basicConfig(level=logging.INFO)

DB_URL = utilities.DB_URL


def getExtentBox(ds):
    """Return shapely box of corner coordinates from a gdal Dataset."""
    xmin, xpixel, _, ymax, _, ypixel = ds.GetGeoTransform()
    width, height = ds.RasterXSize, ds.RasterYSize
    xmax = xmin + width * xpixel
    ymin = ymax + height * ypixel

    return box(xmin, ymin, xmax, ymax)


def convertZip(directory: str):
    """Convert files downloaded from Copernicus."""
    files_list = glob.glob(os.path.join(directory, "*.zip"))
    if len(files_list) > 0:
        logging.info("Extracting zip files")
        for zipfile in files_list:
            extract_dir = os.path.join(
                os.path.dirname(zipfile), pathlib.Path(zipfile).stem
            )
            extracted = utilities.extractZip(zipfile, extract_dir)
            source_file = [x for x in extracted if x.endswith("tif")][0]

            logging.info(source_file)

            dest_file = os.path.join(
                os.path.dirname(extract_dir), os.path.basename(extract_dir) + ".tif",
            )
            os.system(
                "gdal_translate {source_file} {dest_file}  -a_srs EPSG:3035 -of GTIFF --config GDAL_PAM_ENABLED NO -co COMPRESS=DEFLATE -co BIGTIFF=YES".format(
                    source_file=source_file, dest_file=dest_file
                )
            )
            shutil.rmtree(extract_dir)
            os.remove(zipfile)
    else:
        logging.info("There are no zip files to extract")


def get(directory):
    """Prepare df and gdf from rasters."""
    files_list = glob.glob(os.path.join(directory, "*.tif"))
    fids = []
    extents = []
    for file in files_list:
        logging.info(file)
        src_ds = gdal.Open(file)
        prj = src_ds.GetProjection()
        srs = osr.SpatialReference(wkt=prj)
        source_crs = CRS.from_epsg(srs.GetAttrValue("authority", 1))

        try:
            assert source_crs.to_string() == "EPSG:3035"
        except AssertionError:
            logging.error("Input files must be in EPSG:3035")

        extentBox = getExtentBox(src_ds)
        fids.append(os.path.basename(file))
        extents.append(extentBox)

    enermaps_data = pd.DataFrame(
        columns=[
            "start_at",
            "fields",
            "variable",
            "value",
            "ds_id",
            "fid",
            "dt",
            "z",
            "israster",
            "unit",
        ]
    )
    enermaps_data["fid"] = fids

    spatial = gpd.GeoDataFrame(geometry=extents, crs="EPSG:3035",)
    spatial["fid"] = fids

    return enermaps_data, spatial


if __name__ == "__main__":
    argv = sys.argv
    datasets = pd.read_csv("datasets.csv", engine="python", index_col=[0])
    ds_id = int(
        datasets[datasets["di_script"] == os.path.basename(argv[0])].index.values[0]
    )
    url = datasets.loc[
        datasets["di_script"] == os.path.basename(argv[0]), "di_URL"
    ].values[0]

    if "--force" in argv:
        isForced = True
    else:
        isForced = False

    directory = "./data/{}".format(ds_id)

    if (
        os.path.exists(directory)
        and os.path.isdir(directory)
        and len(os.listdir(directory)) == N_FILES
    ):
        # Dezip
        convertZip(directory)

        data, spatial = get(directory)

        # Remove existing dataset
        if utilities.datasetExists(ds_id, DB_URL) and not isForced:
            raise FileExistsError("Use --force to replace the existing dataset.")
        elif utilities.datasetExists(ds_id, DB_URL) and isForced:
            utilities.removeDataset(ds_id, DB_URL)
            logging.info("Removed existing dataset")
        else:
            pass

        # Create dataset table
        metadata = datasets.loc[ds_id].fillna("").to_dict()
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
        spatial["ds_id"] = ds_id
        utilities.toPostGIS(
            spatial, DB_URL, schema="spatial",
        )
    else:
        logging.error(
            "The {} directory must exist and contain {} files from Copernicus.".format(
                directory, N_FILES
            )
        )
