import scrapy
import json
import os
# -*- coding: utf-8 -*-

class cofact_subLink(scrapy.Spider):
    name = 'cofact_subLink'
    path = os.getcwd()
    file_path = os.path.join(path, "spiders\\fetch file\\cofact_getLink.json")
    save_path = os.path.join(path, "spiders\\fetch file\\cofact_detail.json")
    output = []
    amount = 0
    count = 0
    text = 0

    # COUNT_MAX = 30

    # custom_settings = {
    #     'CLOSESPIDER_PAGECOUNT': COUNT_MAX
    # }

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(cofact_subLink, cls).from_crawler(
            crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed,
                                signal=scrapy.signals.spider_closed)
        return spider

    def start_requests(self):
        urls = []
        with open(self.file_path, 'r', encoding = 'utf-8') as fp:
            data = json.load(fp)
            self.amount = data[0]

            for data_dict in data[1:]:
                urls.append(data_dict['link'])
        
        for url in urls:
            self.text += 1
            print(self.text)
            yield scrapy.Request(url, callback=self.parse)

    def spider_closed(self, spider):
        json_object = json.dumps(self.output, indent=4, ensure_ascii=False)

        with open(self.save_path, 'a', encoding='utf-8') as f:
            f.write(json_object)
        spider.logger.info('Spider closed: %s', spider.name)

    def parse(self, response):
        self.count += 1
        reference = []
        # Thread content
        link = response.url
        title = response.css('div.item-title::text').get()
        content = response.css('article.content').css('div::text').get()

        # Comment content
        reference = []
        refer_link = ''
        for comment in response.css('div.root.card'):
            label = comment.css('strong::attr("title")').get()
            comment_content = comment.css('div.bubble').css('div::text').get()
            
            for refer in comment.css('div.bubble').css('section.links'):
                refer_link = refer.css('a::attr("href")').getall()

            reference_data = {
                "category": label,
                "content": comment_content,
                "ref-link": refer_link
            }

            reference.append(reference_data)

        data = {
            'header': title,
            'content': content,
            'link': link,
            'reference': reference,
        }

        print(self.count)

        self.output.append(data)
        if self.count == self.amount:
            yield self.spider_closed()
