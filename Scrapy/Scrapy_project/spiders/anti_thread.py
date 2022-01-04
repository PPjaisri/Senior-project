import os
import csv
import pandas as pd
from scrapy import Spider, signals
from scrapy.exceptions import CloseSpider
from selenium.webdriver import Edge
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class anti_thread(Spider):
    name = 'anti_thread'

    path = os.getcwd()
    save_path = os.path.join(
        path, 'spiders\\results\\anti\\anti_thread.csv')

    binary_location = os.path.join(path, 'msedgedriver.exe')
    start_urls = [
        'https://www.antifakenewscenter.com/allcontent/'
    ]

    def __init__(self):
        self.browser = Edge(self.binary_location)

    # @classmethod
    # def from_crawler(cls, crawler, *args, **kwargs):
    #     spider = super(anti_thread, cls).from_crawler(
    #         crawler, *args, **kwargs)
    #     crawler.signals.connect(spider.spider_closed,
    #                             signal=signals.spider_closed)
    #     return spider

    # def spider_closed(self):
    #     fieldnames = ['category', 'header', 'link']
    #     with open(self.save_path, 'a', encoding='utf-8', newline='') as fp:
    #         writer = csv.DictWriter(fp, fieldnames=fieldnames)
    #         if len(self.last_link) > 0:
    #             writer.writerows(self.fetch_data)
    #         else:
    #             writer.writeheader()
    #             writer.writerows(self.fetch_data)

    # def read_latest_save(self):
    #     try:
    #         data = pd.read_csv(self.save_path, encoding='utf-8')
    #         last_link = data.iloc[-1]['link']
    #         return last_link
    #     except:
    #         return ''

    def nextPage(self):
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        next_page_button = self.browser.find_element_by_class_name('paginationjs-next')
        next_page_button.click()
        
        return

    # def getContentBlock(self):

    def parse(self, response):
        self.browser.get(response.url)

        blog_container = response.css('div.blog-container')

        for blog in blog_container:
            blog_content = blog.css('div.blog-content')
            category = blog.css('div.blog-tag::text').getall()[0].strip()
            for content in blog_content:
                header = content.css('div.blog-title::text').get()
                link = content.css('a::attr("href")').get()

            data = {
                'category': category,
                'header': header,
                'link': link
            }

            yield data
            self.nextPage()

        yield self.parse()
