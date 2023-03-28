from prefect import flow
from src.tasks.dataextractiontasks import *


@flow(name="Extract SandP 500 Company data from wikipedia website")
def get_s_and_p_500_companies():
    successful_get_request = make_get_request("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
    request_with_status_200 = get_status_code(successful_get_request)
    request_with_content_type_html = get_content_type(request_with_status_200)
    html_content_file_location = download_html_file(request_with_content_type_html)
    new_file_server = set_up_file_server()

    # A threaded server is used to serve local files. The following task/func
    # has to be called directly by the flow if not threading issues will occur
    start_file_server_and_scrape_data.fn(new_file_server, run_scraper.fn(), file_serving_and_data_scraping_tracker())

