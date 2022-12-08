from paths import INPUTS_DIR, DATA_DIR
from os.path import join
from os.path import isfile
from os import makedirs
import pandas as pd
from IPython import embed
import requests
import shutil
from tqdm import tqdm

urls = join(INPUTS_DIR, "elevation.csv")
if not isfile(urls):
    raise FileNotFoundError(urls)

dataframe = pd.read_csv(urls, header=None)
# print(dataframe)
elevation_dir = join(DATA_DIR, "elevation")
makedirs(elevation_dir, exist_ok=True)
for url in tqdm(list(dataframe[0])):
    response = requests.get(url, stream=True)
    file = join(elevation_dir, url.split("/")[-1])
    if response.status_code == 200:
        with open(file, 'wb') as f:
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, f) 
