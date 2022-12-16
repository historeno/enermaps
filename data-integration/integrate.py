import fake_data
from legends import post_legend
from utilities import get_engine
import ch_data_integrate 

# create engine
engine = get_engine()

# post legends
post_legend(engine=engine)

# post fake data
# fake_data.post_data(data=fake_data.read_data(), engine_=engine)

# post CH data
ch_data_integrate.post_datasets(engine_=engine)
print("post_datasets")
ids = ch_data_integrate.post_data(engine_=engine)
print("post_data")
ch_data_integrate.post_spatial(engine_=engine, ids=ids)
print("post_spatial")