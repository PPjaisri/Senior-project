from scrapy import signals
from scrapy import Spider


class DmozSpider(Spider):
    name = "scrapy_test"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "https://www.antifakenewscenter.com/%e0%b8%82%e0%b9%88%e0%b8%b2%e0%b8%a7%e0%b8%9b%e0%b8%a5%e0%b8%ad%e0%b8%a1-%e0%b8%ad%e0%b8%a2%e0%b9%88%e0%b8%b2%e0%b9%81%e0%b8%8a%e0%b8%a3%e0%b9%8c-%e0%b8%95%e0%b8%b3%e0%b8%a3%e0%b8%a7%e0%b8%88%e0%b8%9b%e0%b8%8f%e0%b8%b4%e0%b9%80%e0%b8%aa%e0%b8%98%e0%b8%81%e0%b8%b2%e0%b8%a3%e0%b8%a3%e0%b8%b1%e0%b8%9a%e0%b9%81%e0%b8%88%e0%b9%89%e0%b8%87%e0%b8%84%e0%b8%a7%e0%b8%b2%e0%b8%a1-%e0%b8%88%e0%b8%b2%e0%b8%81%e0%b9%80%e0%b8%ab%e0%b8%95%e0%b8%b8%e0%b8%81%e0%b8%b2%e0%b8%a3%e0%b8%93%e0%b9%8c%e0%b8%97%e0%b8%b5%e0%b9%88%e0%b8%8a%e0%b8%b2%e0%b8%a7%e0%b8%95%e0%b9%88%e0%b8%b2%e0%b8%87%e0%b8%8a%e0%b8%b2%e0%b8%95%e0%b8%b4%e0%b8%9e%e0%b8%a5%e0%b8%b1%e0%b8%94%e0%b8%95%e0%b8%81%e0%b8%9a%e0%b9%88%e0%b8%ad%e0%b8%99%e0%b9%89%e0%b8%b3%e0%b8%9e%e0%b8%b8%e0%b8%a3%e0%b9%89%e0%b8%ad%e0%b8%99/"
    ]

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(DmozSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed,
                                signal=signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        # spider.logger.info('Spider closed: %s', spider.name)
        print(spider.name)

    def parse(self, response):
        pass