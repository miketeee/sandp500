import scrapy
from bs4 import BeautifulSoup
from datetime import datetime

current_utc_date = datetime.utcnow()
utc_to_str = datetime.strftime(current_utc_date, '%Y_%m_%d')

class SandpwikipediascraperSpider(scrapy.Spider):
    name = "sandpwikipediascraper"
    allowed_domains = ["localhost"]
    start_urls = ["https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"]

    def parse(self, response):
        all_rows = []

        table_rows = response.xpath('//table[@id="constituents"]//tbody//tr//td')
        with open(f'src/filestoprocess/dataextractedfromhtml/extracteddata{utc_to_str}.txt', mode='w', encoding='utf-8') as pt:

            for row in table_rows:
                text = row.get()

                soup = BeautifulSoup(text).td

                if soup.contents:
                    all_rows.append(soup.contents[0].string.strip())
                else:
                    pass

            pt.write(str(all_rows))