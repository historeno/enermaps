from app.data_integration import data_endpoints, enermaps_server
from app.models.geofile import create


def init_enermaps_datasets():

    # Get NUTS and LAU datasets
    # nuts_and_lau_datasets = ["country", "NUTS1", "NUTS2", "NUTS3", "LAU"]
    # for dataset_name in nuts_and_lau_datasets:
    #     try:
    #         file_upload = enermaps_server.get_nuts_and_lau_dataset(dataset_name)
    #         if file_upload is not None:
    #             create(file_upload)
    #     except Exception as e:
    #         print("Error creating dataset {}".format(dataset_name))
    #         print(e)

    # Get the ids of the datasets that we want to load
    datasets_ids = data_endpoints.get_ds_ids()
    # To download only a subset of the datasets (!datasets ids must be in the config file!)
    # datasets_ids = [1,2,3,4,5,6]
    datasets_ids = [1, 2, 14]
    # Check that the datasets that we want to load are in the enermaps DB
    for dataset_id in datasets_ids:
        try:
            file_upload = enermaps_server.get_dataset(dataset_id)
            if file_upload is not None:
                create(file_upload)
        except Exception as e:
            print("Error creating dataset {}".format(dataset_id))
            print(e)
