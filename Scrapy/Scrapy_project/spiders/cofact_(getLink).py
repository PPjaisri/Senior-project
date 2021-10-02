import scrapy
import json
import os

# -*- coding: utf-8 -*-

class cofact_link(scrapy.Spider):
    name = 'cofact'
    path = os.getcwd()
    save_path = os.path.join(path, 'spiders\\fetch file\\cofact_getLink.json')

    start_urls = [
        "https://cofact.org/articles?replyRequestCount=1&before=&after=&filter=solved"
    ]

    fetch_data = []

    def parse(self, response):
        domain = response.url[0:18]
        article = response.url[0:27]
        amount = response.css('div.text-muted::text').get()

        for box in response.css('ul.article-list').css('li'):
            
            link = box.css('a::attr("href")').get()
            text = box.css('a').css('div.item-text::text').get()
            img = box.css('a').css('img::attr("src")').get()

            if text != None:
                self.fetch_data.append({
                    'text': text,
                    'img': None,
                    'link': domain + link
                })
            else:
                self.fetch_data.append({
                    'text': None,
                    'img': img,
                    'link': domain + link
                })

        next_link = response.css(
            'div.wrapper-pager').css('a.ml-auto::attr("href")').get()
        if next_link is not None:
            next_page = article + next_link
            yield response.follow(next_page, callback=self.parse)
        else:
            self.fetch_data.insert(0, {'total': amount})
            json_data = json.dumps(
                self.fetch_data, indent=4, ensure_ascii=False)
            with open(self.save_path, 'a', encoding='utf-8') as fp:
                fp.write(json_data)
