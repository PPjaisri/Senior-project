from scrapy import Spider, signals, Request
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
    count = 0
    text = 0

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
        
        for url in urls[1:]:
            self.text += 1
            try:
                yield Request(url, callback=self.parse)
            except:
                continue

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
        self.count += 1
        
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

            self.fetch_data_ref.append(reference_data)

        data = {
            'header': title,
            'content': content,
            'image': image,
            'link': link,
        }

        self.fetch_data.append(data)
        # if self.count == self.amount:
        #     yield self.spider_closed()
