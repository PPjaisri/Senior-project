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
    length = 0
    count = 1

    def start_requests(self):
        urls = []
        with open(self.file_path, 'r', encoding = 'utf-8') as fp:
            data = fp.read()
            data_list = json.loads(data)

            for data_dict in data_list[1:len(data_list) - 1]:
                urls.append(data_dict['link'])

        self.length = len(urls)
        
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

            data = {
                'label': label,
                'link': link,
                'title': title,
                'img': img,
                'content': content,
                'reference': reference,
            }

            self.output.append(data)

        if self.count == self.length:
            json_object = json.dumps(self.output, indent=4, ensure_ascii=False)

            with open(self.save_path, 'a', encoding='utf-8') as f:
                f.write(json_object)

        self.count += 1
