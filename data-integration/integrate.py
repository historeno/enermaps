import fake_data
from legends import post_legend
from utilities import get_engine
import ch_data_integrate 

# create engine
engine = get_engine()

# post legends
post_legend(engine=engine)

# post CH data
ch_data_integrate.post_datasets(engine_=engine)
fids = ch_data_integrate.post_data(engine_=engine)
ch_data_integrate.post_spatial(engine_=engine, ids=fids)