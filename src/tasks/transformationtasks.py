from prefect import task
from datetime import datetime, date
import ast
import json
import time
import requests
import os
import csv


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


@task(name="get balance company balance sheets")
def balance_sheet_retrieval(companies, api_key):
    ticker_attempts = 0
    while len(companies) > 0:
        ticker = companies[0][0]

        try:
            url = f"https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={ticker}&apikey={api_key}"
            r = requests.request(method='GET', url=url)
            response_json = json.dumps(r.json(), indent=4)

            with open(f"src/filestoprocess/balancesheets/{ticker}_balancesheet.json", mode='w') as output_file:
                output_file.write(response_json)
                print(r.json()['symbol'])
                print(f"{len(companies)} left")
                companies.pop(0)

        except KeyError:
            print(f"You hit your per minute limit at ticker {ticker}")
            ticker_attempts += 1
            print(f"{ticker} has been tried {ticker_attempts} time(s)")
            time.sleep(20)
            if ticker_attempts >= 2:
                companies.pop(0)
                ticker_attempts = 0

        finally:
            pass


@task(name="write sort json files into csv file")
def write_to_csvs():
    master_quarterly_reports = "./src/filestoprocess/quarterlyreports/masterquarterlyreports.csv"
    master_annual_reports = "./src/filestoprocess/annualreports/masterannualreports.csv"
    header_flags = {}

    for balancesheetpath in os.listdir("./src/filestoprocess/balancesheets"):

        with (open(f"./src/filestoprocess/balancesheets/{balancesheetpath}", mode='r', encoding='utf-8') as bs,
              open(master_quarterly_reports, mode='a', newline='', encoding='utf-8') as mqr_appender,
              open(master_annual_reports, mode='a', newline='', encoding='utf-8') as mar_appender,
              ):

            balance_sheet_dict = json.loads(bs.read())
            if len(balance_sheet_dict.items()) > 0:
                company_ticker, annual_report, quarterly_report = [key for key in balance_sheet_dict.keys()]
                report_types = [annual_report, quarterly_report]
                context_manager_writer = None

                for report_type in report_types:
                    for report_dict in balance_sheet_dict[report_type]:
                        report_dict.update({company_ticker: balance_sheet_dict[company_ticker]})
                        if report_type == 'quarterlyReports':
                            context_manager_writer = mqr_appender

                        if report_type == 'annualReports':
                            context_manager_writer = mar_appender

                        report_fieldnames = [fn for fn in report_dict.keys()]
                        report_writer = csv.DictWriter(context_manager_writer, report_fieldnames)

                        # only write header if header flag in not in the header_flag_dict
                        if report_type not in header_flags.keys():
                            report_writer.writeheader()
                            header_flags.update({report_type: True})

                        report_writer.writerow(report_dict)




