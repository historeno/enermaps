from os.path import abspath, dirname, join

CURRENT_DIR = dirname(abspath(__file__))

DATA_DIR = join(CURRENT_DIR, "data")
FAKE_DATA_DIR = join(DATA_DIR, "fake_data")
REGBL_DATA_DIR = join(DATA_DIR, "regbl_data")

INPUTS_DIR = join(CURRENT_DIR, "inputs")
