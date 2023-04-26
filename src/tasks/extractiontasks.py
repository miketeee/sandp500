import http.server
import socketserver
import threading
from scrapy.crawler import CrawlerProcess
from src.tasks.wikipediascraper.wikipediascraper.spiders import sandpwikipediascraper
from prefect import task
import requests
from datetime import datetime
from src.tasks import s3_tasks

@task(name='Clear all folder sub folders of folder filestoproces')
def clear_sub_folders():
    pass



@task(name='Make GET Request')
def make_get_request(webpage_url):
    response_obj = requests.get(url=webpage_url)
    if not isinstance(response_obj, requests.models.Response):
        raise ValueError
    else:
        return response_obj


@task(name='Determine response Status Code')
def get_status_code(response_obj: requests.models.Response):
    if response_obj.status_code == 200:
        return response_obj
    else:
        return response_obj.status_code


@task(name='Determine response Content Type')
def get_content_type(response_obj: requests.models.Response):

    if response_obj.headers['Content-Type'].__contains__("html"):
        return response_obj
    else:
        return response_obj.headers['Content-Type']


@task(name='Download response html file')
def download_html_file(request_obj: requests.models.Response, client):
    current_utc_date = datetime.utcnow()
    utc_to_str = datetime.strftime(current_utc_date, '%Y_%m_%d')
    new_file_location = f'src/filestoprocess/downloadedhtml/sp500_{utc_to_str}.html'
    s3_tasks.add_obj_to_s3.fn('sandp', new_file_location, request_obj.text, client)

    return new_file_location, request_obj.text

@task(name='Set up file server')
def set_up_file_server():
    class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
        pass

    handler = http.server.SimpleHTTPRequestHandler
    host, port = "localhost", 8000

    threaded_server = ThreadedTCPServer((host, port), handler)

    return threaded_server


@task(name='Scrapy spider process')
def run_scraper():
    process = CrawlerProcess()
    process.crawl(sandpwikipediascraper.SandpwikipediascraperSpider)
    process.start()


@task(name="File serving and data scraping",
      description="This task serves as a place holder for the"
                  "task start_file_server_and_scrape_data. The task"
                  "has to be called directly from the flow due to"
                  "threading issue risk. Tasks that are called directly"
                  "do not show up in the Prefect flow run logs.")
def file_serving_and_data_scraping_tracker():
    return True


@task(name='Start fileserver and scrape html data', task_run_name="threaded_server")
def start_file_server_and_scrape_data(file_server, scraper_task, tracker):
    with file_server:
        # Start a thread with the server -- that thread will then start one
        # more thread for each request
        server_thread = threading.Thread(target=file_server.serve_forever)
        # Exit the server thread when the main thread terminates
        server_thread.daemon = True
        server_thread.start()
        scraping_output = scraper_task

        file_server.shutdown()





