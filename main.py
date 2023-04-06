from src.flows import transformationflows, extractionflows

if __name__ == '__main__':

    # FLOW ONE: Data Extraction Flow
    # Scrape S & P 500 data from wikipedia
    # add the data to a list
    # write the list to a text file

    extractionflows.get_s_and_p_500_companies()
    transformationflows.data_cleaning()











