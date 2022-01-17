from scrapy.exceptions import CloseSpider
from scrapy import signals, Spider
import pandas as pd
import csv
import os


# -*- coding: utf-8 -*-
class cofact_thread(Spider):
    name = 'cofact_thread'
    path = os.getcwd()
    path = os.path.dirname(path)
    path = os.path.dirname(path)
    save_path = os.path.join(
        path, 'result\\Cofact\\cofact_thread.csv')

    start_urls = [
        "https://cofact.org/articles?replyRequestCount=1&before=&after=&filter=solved"
    ]

    fetch_data = []
    last_link = ''
    add = False

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(cofact_thread, cls).from_crawler(
            crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed,
                                signal=signals.spider_closed)
        return spider

    def read_latest_save(self):
        try:
            data = pd.read_csv(self.save_path, encoding='utf-8')
            last_link = data.iloc[-1]['link']
            return last_link
        except:
            return ''

    def parse(self, response):
        if not self.add:
            self.last_link = self.read_latest_save()
            self.add = True

        domain = response.url[0:18]
        article = response.url[0:27]
        self.amount = response.css('div.text-muted::text').get()
        li = response.css('ul.article-list').css('li')

        for element in li:
            header = element.css(
                'div.item-title::text, div.item-text::text').get()
            link = element.css('a::attr("href")').get()
            status_set = element.css('div.meter-tag').css('div::text').getall()
            if len(status_set) > 0:
                status = status_set[1]
            else:
                status = None

            data = {
                "category": status,
                "header": [header],
                "link": domain + link,
            }

            self.fetch_data.insert(0, data)

            if (domain + link) == self.last_link:
                raise CloseSpider('finished')

        next_link = response.css(
            'div.wrapper-pager').css('a.ml-auto::attr("href")').get()
        if next_link is not None:
            next_page = article + next_link
            yield response.follow(next_page, callback=self.parse)
        else:
            raise CloseSpider('finished')

    def spider_closed(self):
        fieldnames = ['category', 'header', 'link']
        with open(self.save_path, 'a+', encoding='utf-8', newline='') as fp:
            writer = csv.DictWriter(
                fp, fieldnames=fieldnames)
            print(self.last_link != '')
            if self.last_link != '':
                writer.writerows(self.fetch_data)
            else:
                writer.writeheader()
                writer.writerows(self.fetch_data)
