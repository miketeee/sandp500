from src.flows import transformationflows, extractionflows
from prefect import flow

    # FLOW ONE: Data Extraction Flow
    # Scrape S & P 500 data from wikipedia
    # add the data to a list
    # write the list to a text file
@flow(name="sandpentry")
def sandpentry():
    extractionflows.get_s_and_p_500_companies()
    transformationflows.data_cleaning()


if __name__ == '__main__':
    sandpentry()









