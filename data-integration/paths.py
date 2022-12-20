from os.path import abspath, dirname, join
from os import makedirs

CURRENT_DIR = dirname(abspath(__file__))

DATA_DIR = join(CURRENT_DIR, "data")

CH_DATA_DIR = join(DATA_DIR, "suisse")
CH_DEM_DATA_DIR = join(CH_DATA_DIR, "digital elevation model")
CH_FOOTPRINT_DATA_DIR = join(CH_DATA_DIR, "footprint")
CH_FINAL_RESULTS_DATA_DIR = join(CH_DATA_DIR, "final_results")

INPUTS_DIR = join(CURRENT_DIR, "inputs")

CH_INPUTS_DIR = join(INPUTS_DIR, "suisse")
CH_DEM_INPUTS_DIR = join(CH_INPUTS_DIR, "digital elevation model")
CH_FOOTPRINT_INPUTS_DIR = join(CH_INPUTS_DIR, "footprint")
CH_REGBL_INPUTS_DIR = join(CH_INPUTS_DIR, "regbl")
