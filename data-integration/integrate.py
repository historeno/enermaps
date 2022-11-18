import fake_data
from legends import post_legend
from utilities import get_engine
from regbl_data import set_spatial_table 

# create engine
engine = get_engine()

# post legends
post_legend(engine=engine)

# post the data
geo_dataframe = fake_data.read_data()
fake_data.post_data(data=geo_dataframe, engine_=engine)

# regbl
# geo_dataframe = set_spatial_table()
