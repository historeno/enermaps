from os.path import abspath, dirname, join
from os import makedirs

CURRENT_DIR = dirname(abspath(__file__))

DATA_DIR = join(CURRENT_DIR, "data")
CH_DATA_DIR = join(DATA_DIR, "ch_data")
FAKE_DATA_DIR = join(DATA_DIR, "fake_data")
REGBL_DATA_DIR = join(DATA_DIR, "regbl_data")
FOOTPRINT_DATA_DIR = join(DATA_DIR, "footprint_data")
ALL_CANTON_FOOTPRINT_DIR = join(FOOTPRINT_DATA_DIR, "all_canton")
makedirs(ALL_CANTON_FOOTPRINT_DIR, exist_ok=True)

INPUTS_DIR = join(CURRENT_DIR, "inputs")
CANTON_FOOTPRINT_CSV_DIR = join(INPUTS_DIR, "canton_footprint")
