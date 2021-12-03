from scrapy import signals, Spider
import csv
import os

# -*- coding: utf-8 -*-
class cofact_link(Spider):
    name = 'cofact_thread'
    path = os.getcwd()
    save_path = os.path.join(
        path, 'spiders\\results\\cofact\\cofact_thread.csv')

    start_urls = [
        "https://cofact.org/articles?replyRequestCount=1&before=&after=&filter=solved"
    ]

    fetch_data = []

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(cofact_link, cls).from_crawler(
            crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed,
                                signal=signals.spider_closed)
        return spider

    def parse(self, response):
        domain = response.url[0:18]
        article = response.url[0:27]
        self.amount = response.css('div.text-muted::text').get()
        li = response.css('ul.article-list').css('li')

        for element in li:
            header = element.css('div.item-title::text').get()
            link = element.css('a::attr("href")').get()
            status_set = element.css('div.meter-tag').css('div::text').getall()
            if len(status_set) > 0:
                status = status_set[1]
            else:
                status = None

            data = {
                "category": status,
                "header": header,
                "link": domain + link,
            }

            self.fetch_data.append(data)

        next_link = response.css(
            'div.wrapper-pager').css('a.ml-auto::attr("href")').get()
        if next_link is not None:
            next_page = article + next_link
            yield response.follow(next_page, callback=self.parse)

    def spider_closed(self):
        fieldnames = ['category', 'header', 'link']
        with open(self.save_path, 'a+', encoding='utf-8', newline='') as fp:
            writer = csv.DictWriter(
                fp, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.fetch_data)
