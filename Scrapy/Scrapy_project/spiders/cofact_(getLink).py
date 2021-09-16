import scrapy
# -*- coding: utf-8 -*-

class cofact_link(scrapy.Spider):
    name = 'cofact'

    start_urls = [
        "https://cofact.org/articles?replyRequestCount=1&before=&after=&filter=solved"
    ]

    def parse(self, response):
        domain = response.url[0:18]
        article = response.url[0:27]
        amount = response.css('div.text-muted::text').get()

        for box in response.css('ul.article-list').css('li'):
            
            link = box.css('a::attr("href")').get()
            text = box.css('a').css('div.item-text::text').get()
            img = box.css('a').css('img::attr("src")').get()

            if text != None:
                yield {
                    'text': text,
                    'img': None,
                    'link': domain + link
                }
            else:
                yield {
                    'text': None,
                    'img': img,
                    'link': domain + link
                }

        next_link = response.css(
            'div.wrapper-pager').css('a.ml-auto::attr("href")').get()
        if next_link is not None:
            next_page = article + next_link
            yield response.follow(next_page, callback=self.parse)
        else:
            yield { "amount": amount }