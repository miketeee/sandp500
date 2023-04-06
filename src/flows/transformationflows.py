from prefect import flow
from src.tasks.transformationtasks import *
from dotenv import dotenv_values


api_key = dotenv_values()['API_KEY']

@flow(name="Data cleaning flow")
def data_cleaning():
    data_that_exists = verify_raw_data_file_exists()
    restructured_data = restructure_data(data_that_exists)
    balance_sheet_retrieval(restructured_data, api_key)
    write_to_csvs()





