import ch_data_integrate
from legends import post_legend
from utilities import get_engine, remove_dataset, remove_lengends

# create engine
engine = get_engine()

# post legends
# remove_lengends(engine=engine)
post_legend(engine=engine)

# post CH data
remove_dataset(ds_id=1, engine=engine)
ch_data_integrate.post_datasets(engine_=engine)
fids = ch_data_integrate.post_data(engine_=engine)
ch_data_integrate.post_spatial(engine_=engine, ids=fids)
