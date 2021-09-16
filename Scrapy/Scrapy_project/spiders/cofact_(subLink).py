import scrapy
import json
# -*- coding: utf-8 -*-

class cofact_subLink(scrapy.Spider):
    name = 'cofact_subLink'
    path = 'C:/Coding/Senior project/Scrapy/result_json/Cofact/cofact.json'

    def start_requests(self):
        urls = []
        with open(self.path, encoding = 'utf-8') as fp:
            data = fp.read()
            data_list = json.loads(data)

            for data_dict in data_list[:len(data_list) - 1]:
                urls.append(data_dict['link'])
        
        for url in urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        reference = []
        link = response.url

        for element in response.css('div.wrapper-main'):
            title = element.css('div.item-title::text').get()
            content = element.css('article.content').css('div::text').get()
            img = element.css('article.content').css('img::attr("src")').get()
            label = element.css('section').css('strong::text').get()

            for section in element.css('div.wrapper').css('div.root'):
                reference.append(section.css('div.bubble').css('a::attr("href")').get())

            yield {
                'label': label,
                'link': link,
                'title': title,
                'img': img,
                'content': content,
                'reference': reference,
            }
