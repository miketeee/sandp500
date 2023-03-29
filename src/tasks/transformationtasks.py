from prefect import task
from datetime import datetime, date
import ast


@task(name="Check to see if raw data file exists")
def verify_raw_data_file_exists():
    current_utc_date = datetime.utcnow()
    utc_to_str = datetime.strftime(current_utc_date, '%Y_%m_%d')

    with open(f'src/'
              f'filestoprocess'
              f'/dataextractedfromhtml'
              f'/extracteddata{utc_to_str}.txt', mode='r', encoding='utf-8') as raw_data:

        rawdata = ast.literal_eval(raw_data.read())

    return rawdata


@task(name="Restructure data into table")
def restructure_data(data_to_restructure):
    all_companies = []

    for i, x in enumerate(data_to_restructure):

        # find the column representing the central index key
        # this column will be the anchor to find columns
        # that should appear before and after it
        if x[:2] == '00':

            symbol = data_to_restructure[i-5]
            security = data_to_restructure[i-4]
            sector = data_to_restructure[i-3]
            sub_industry = data_to_restructure[i-2]
            headquarters = data_to_restructure[i - 1]
            cik = data_to_restructure[i]
            founded = data_to_restructure[i + 1]
            date_added = 'Null'

            if (len(data_to_restructure[i-1]) > 5 and str.isdigit(data_to_restructure[i-1][:4])) or data_to_restructure[i-1].__contains__('?'):
                symbol = data_to_restructure[i-6]
                security = data_to_restructure[i-5]
                sector = data_to_restructure[i-4]
                sub_industry = data_to_restructure[i-3]
                headquarters = data_to_restructure[i-2]
                date_added = data_to_restructure[i - 1]

                company_data = [symbol, security, sector, sub_industry, headquarters, date_added, cik, founded]
                all_companies.append(company_data)

            else:
                company_data = [symbol, security, sector, sub_industry, headquarters, date_added, cik, founded]
                all_companies.append(company_data)

    return all_companies




