# Data integration for Historeno

This service retrieves the different sources to be integrated into the database.

## Required directories/files

### Inputs directory

inputs
 ┗ suisse
 ┃ ┣ digital elevation model
 ┃ ┃ ┣ elevation.csv
 ┃ ┃ ┗ elevation.py
 ┃ ┣ footprint
 ┃ ┃ ┣ be.csv
 ┃ ┃ ┣ ch_data_integrate.py
 ┃ ┃ ┣ fr.csv
 ┃ ┃ ┣ ge.csv
 ┃ ┃ ┣ ju.csv
 ┃ ┃ ┣ ne.csv
 ┃ ┃ ┣ swissBUILDINGS3D 2.0_Produktinfo_fr_2021_bf.pdf
 ┃ ┃ ┣ vd.csv
 ┃ ┃ ┗ vs.csv
 ┃ ┗ regbl
 ┃ ┃ ┣ code_category.csv
 ┃ ┃ ┣ code_heating_system.csv
 ┃ ┃ ┗ commands.sql

### Data directory

data
 ┗ suisse
 ┃ ┣ digital elevation model
 ┃ ┃ ┣ elevation.zip
 ┃ ┃ ┣ swissalti3d_2019_2501-1120_2_2056_5728.tif
 ┃ ┃ ┣ swissalti3d_2019_2501-1121_2_2056_5728.tif
 ┃ ┃ ┣ ...
 ┃ ┃ ┗ swissalti3d_2022_2732-1114_2_2056_5728.tif
 ┃ ┣ final_results
 ┃ ┗ footprint
 ┃ ┃ ┣ footprint_gpkg
 ┃ ┃ ┣ README.md
 ┃ ┃ ┗ merged_data_v2.gpkg