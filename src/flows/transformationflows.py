from prefect import flow
from src.tasks.transformationtasks import *
from dotenv import dotenv_values
from src.tasks import s3_tasks
from prefect.blocks.system import Secret

secret_block = Secret.load("apikey")

# Access the stored secret
api_key = secret_block.get()

# api_key = dotenv_values()['API_KEY']

@flow(name="Data cleaning flow")
def data_cleaning():
    s3_client = s3_tasks.get_client()
    data_that_exists = verify_raw_data_file_exists(s3_client)
    restructured_data = restructure_data(data_that_exists)
    balance_sheet_retrieval(restructured_data, api_key)
    write_to_csvs()
    master_quarterly_reports = "src/filestoprocess/quarterlyreports/masterquarterlyreports.csv"
    master_annual_reports = "src/filestoprocess/annualreports/masterannualreports.csv"
    write_csv_to_s3(master_annual_reports, s3_client)
    write_csv_to_s3(master_quarterly_reports, s3_client)
    clean_up_folders()





