from utilities import get_engine, post_data, read_data
from legends import post_legend

# create engine
engine = get_engine()

# set the dataframe
geo_dataframe = read_data()

# post legends
post_legend(engine=engine)

# post the data
post_data(data=geo_dataframe, engine_=engine)
