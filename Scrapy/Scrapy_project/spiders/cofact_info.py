from scrapy import Spider, signals, Request
from scrapy.exceptions import CloseSpider
import pandas as pd
import csv
import os


# -*- coding: utf-8 -*-
class cofact_info(Spider):
    name = 'cofact_info'

    path = os.getcwd()
    file_path = os.path.join(path, 'spiders\\results\\cofact\\cofact_thread.csv')
    save_path = os.path.join(path, 'spiders\\results\\cofact\\cofact_info.csv')
    save_path_ref = os.path.join(path, 'spiders\\results\\cofact\\cofact_info_ref.csv')

    fetch_data = []
    fetch_data_ref = []
    text = 0
    last_link = ''
    add = False

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(cofact_info, cls).from_crawler(
            crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed,
                                signal=signals.spider_closed)
        return spider

    def start_requests(self):
        urls = []
        with open(self.file_path, 'r', encoding = 'utf-8') as fp:
            data = fp.readlines()

        for data_dict in data:
            urls.append(data_dict.split(',')[2])

        new_urls = []
        for url in range(len(urls) - 1, -1, -1):
            new_urls.append(urls[url])
        
        for url in new_urls[1:]:
            self.text += 1
            try:
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
        fieldnames = ['header', 'content', 'image', 'link']
        fieldnames_ref = ['category', 'content', 'link', 'ref-link']

        with open(self.save_path, 'a+', encoding='utf-8', newline='') as fp:
            writer = csv.DictWriter(fp, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.fetch_data)

        with open(self.save_path_ref, 'a+', encoding='utf-8', newline='') as fp:
            writer = csv.DictWriter(fp, fieldnames=fieldnames_ref)
            writer.writeheader()
            writer.writerows(self.fetch_data_ref)

    def parse(self, response):
        if not self.add:
            self.last_link = self.read_latest_save()
            self.add = True
        
        # Thread content
        link = response.url
        title = response.css('div.item-title::text').get()
        content = response.css('article.content').css('div::text').get()
        image = response.css('img.image-content::attr("src")').get()

        # Comment content
        refer_link = ''
        for comment in response.css('div.root.card'):
            label = comment.css('strong::attr("title")').get()
            comment_content = comment.css('div.bubble').css('div::text').get()
            
            for refer in comment.css('div.bubble').css('section.links'):
                refer_link = refer.css('a::attr("href")').getall()

            refer_link = [ref for ref in refer_link if ref != '']

            reference_data = {
                'category': label,
                'content': comment_content,
                'link': link,
                'ref-link': refer_link
            }

            self.fetch_data_ref.insert(0, reference_data)

        data = {
            'header': title,
            'content': content,
            'image': image,
            'link': link,
        }

        if self.last_link == link:
            raise CloseSpider('finished')

        self.fetch_data.insert(0, data)
