import scrapy
import json
import os

from scrapy import signals

# -*- coding: utf-8 -*-

class cofact_link(scrapy.Spider):
    name = 'cofact'
    path = os.getcwd()
    save_path = os.path.join(path, 'spiders\\fetch file\\cofact_getLink.json')

    start_urls = [
        "https://cofact.org/articles?replyRequestCount=1&before=&after=&filter=solved"
    ]

    fetch_data = []
    amount = 0

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(cofact_link, cls).from_crawler(
            crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed,
                                signal=signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        self.fetch_data.insert(0, {'total': self.amount})
        json_data = json.dumps(
            self.fetch_data, indent=4, ensure_ascii=False)
        with open(self.save_path, 'a', encoding='utf-8') as fp:
            fp.write(json_data)

    def parse(self, response):
        domain = response.url[0:18]
        article = response.url[0:27]
        self.amount = response.css('div.text-muted::text').get()
        li = response.css('li')

        for element in li:
            header = element.css('div.item-title::text').get()
            link = element.css('a::attr("href")').get()
            content = element.css('div.item-text::text').get()
            image = element.css('img::attr("src")').get()
            print(element.css('div.meter-tag').css('div::text'))
            status = element.css('div.meter-tag').css('div::text').getall()[1]

            data = {
                "category": status,
                "header": header,
                "content": content,
                "link": domain + link,
                "img": image
            }

            self.fetch_data.append(data)

        next_link = response.css(
            'div.wrapper-pager').css('a.ml-auto::attr("href")').get()
        if next_link is not None:
            next_page = article + next_link
            yield response.follow(next_page, callback=self.parse)
