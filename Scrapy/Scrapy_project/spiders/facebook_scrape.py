from scrapy import Spider
from scrapy_selenium import SeleniumRequest

class FacebookScrapeSpider(Spider):
    name = 'facebook_scrape'
    url = 'https://www.facebook.com/sheapgamer/posts/1063757677738891'

    def start_requests(self):
        yield SeleniumRequest(
            url=self.url,
            wait_time=2,
            callback=self.parse,
            dont_filter=True
        )

    def parse(self, response):
        page_name = response.xpath('//*[@id="jsc_c_3a9"]/span/a/strong/span').get()

        yield {
            'page name': page_name
        }
