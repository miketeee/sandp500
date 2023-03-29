from prefect import flow
from src.tasks.transformationtasks import *
from datetime import datetime
from dotenv import dotenv_values
import requests
import json
import time

api_key = dotenv_values()['API_KEY']

@flow(name="Data cleaning flow")
def data_cleaning():
    data_that_exists = verify_raw_data_file_exists()
    restructured_data = restructure_data(data_that_exists)

    def get_ticker_balancesheet_json(ticker):
        url = f"https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={ticker}&apikey={api_key}"
        r = requests.request(method='GET', url=url)

        try:
            if r.json()['symbol']:
                response_json = json.dumps(r.json(), indent=4)

                with open(f"src/filestoprocess/balancesheets/{ticker}_balancesheet.json", mode='w') as output_file:
                    output_file.write(response_json)
                    print(r.json()['symbol'])

        except KeyError:
            print("You hit your per minute limit")
            time.sleep(60)
        finally:
            pass

    for company in restructured_data:
        ticker = company[0]

        get_ticker_balancesheet_json(ticker)








