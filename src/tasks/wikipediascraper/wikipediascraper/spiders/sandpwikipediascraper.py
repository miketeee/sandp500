import scrapy
from bs4 import BeautifulSoup
from datetime import datetime
from src.tasks import s3_tasks

current_utc_date = datetime.utcnow()
utc_to_str = datetime.strftime(current_utc_date, '%Y_%m_%d')

class SandpwikipediascraperSpider(scrapy.Spider):
    name = "sandpwikipediascraper"
    allowed_domains = ["localhost"]

    def start_requests(self):
        yield scrapy.Request('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')

    def parse(self, response):
        all_rows = []

        table_rows = response.xpath('//table[@id="constituents"]//tbody//tr//td')
        client = s3_tasks.get_client()
        key = f'src/filestoprocess/dataextractedfromhtml/extracteddata{utc_to_str}.txt'

        for row in table_rows:
            text = row.get()
            soup = BeautifulSoup(text).td

            if soup.contents:
                all_rows.append(soup.contents[0].string.strip())
            else:
                pass

        s3_tasks.add_obj_to_s3('sandp', key, str(all_rows), client)


