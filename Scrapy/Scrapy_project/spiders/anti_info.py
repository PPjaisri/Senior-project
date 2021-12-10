from scrapy import Spider, Request, signals
from scrapy.exceptions import CloseSpider
import pandas as pd
import csv
import os
import time

class anti_news(Spider):
    name = 'anti_info'

    path = os.getcwd()
    input_path = os.path.join(
        path, 'spiders\\results\\anti\\anti_thread.csv')
    save_path = os.path.join(
        path, 'spiders\\results\\anti\\anti_info.csv')

    fetch_data = []
    add = False
    last_link = ''

    custom_settings = {
        'DOWNLOAD_DELAY': 3
    }

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(anti_news, cls).from_crawler(
            crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed,
                                signal=signals.spider_closed)
        return spider

    def start_requests(self):
        urls = []

        with open(self.input_path, 'r', encoding='utf-8') as fp:
            data = fp.readlines()

            for obj in data:
                if obj != '\n':
                    obj = obj.split(',')
                    urls.append(obj[2])

        new_urls = []
        for url in range(len(urls) - 1, 0, -1):
            new_urls.append(urls[url])

        for url in new_urls:
            try:
                time.sleep(1)
                yield Request(url, callback=self.parse)
            except:
                continue

    def read_latest_save(self):
        try:
            data = pd.read_csv(self.save_path, encoding='utf-8')
            last_link = data.iloc[-1]['link']
            return last_link
        except:
            return ''

    def spider_closed(self):

        with open(self.save_path, 'a+', encoding='utf-8', newline='') as fp:
            fieldnames = ['category', 'header', 'content', 'link', 'image']
            writer = csv.DictWriter(fp, fieldnames=fieldnames)
            if self.last_link != '':
                writer.writerows(self.fetch_data)
            else:
                writer.writeheader()
                writer.writerows(self.fetch_data)

        # Spider.logger.info('Spider closed: %s', Spider.name)

    def parse(self, response):
        if not self.add:
            self.last_link = self.read_latest_save()
            self.add = True

        if response.url == self.last_link:
            print(True)
            raise CloseSpider('finished')

        header = response.css('div.title-post-news').css('p::text').get()

        image = response.css(
            'div.-detail, div.gray-image').css('img::attr("src")').getall()

        category = response.css(
            'div.-detail').css('span').css('strong *::text, b *::text').get()

        content = []
        for element in response.css('div.-detail').css('p'):
            paragraph = element.css('p *::text').get()

            if paragraph != None:
                content.append(paragraph)

        data = {
            'category': category,
            'header': header,
            'content': content,
            'link': response.url,
            'image': image
        }

        self.fetch_data.insert(0, data)
