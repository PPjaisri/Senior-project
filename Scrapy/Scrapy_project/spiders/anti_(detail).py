import scrapy
import json

class anti_news(scrapy.Spider):
    name = 'anti_news'
    count = -1
    index = -1
    path = 'C:/Coding/Senior project/Scrapy_project/Scrapy_project/result_json/anti.json'

    start_urls = [
        'https://www.antifakenewscenter.com'
    ]

    fetch_urls = []

    def fetch(self):
        f = open(self.path, encoding='utf-8',)
        data = json.load(f)
        
        for obj in data:
            self.fetch_urls.append(list(obj.values())[2])

        f.close()

    def parse(self, response):
        self.fetch()
        self.index += 1
        for item in response.css('div.-detail'):
            category = item.css('p').css('span').css('strong::text').get()
            category2 = item.css('p').css('span').css('b::text').get()
            detail = item.css('p::text').getall()
            detail2 = item.css('p').css('span::text').getall()

            if category:
                if len(detail) != 0:
                    yield {
                        'category': category,
                        'detail': detail,
                        'link': response.url
                    }
                else:
                    yield {
                        'category': category,
                        'detail': detail2,
                        'link': response.url
                    }
            else:
                if len(detail) != 0:
                    yield {
                        'category': category2,
                        'detail': detail,
                        'link': response.url
                    }
                else:
                    yield {
                        'category': category2,
                        'detail': detail2,
                        'link': response.url
                    }
                
        if self.index <= len(self.fetch_urls) - 1:
            next_page = self.fetch_urls[self.index]
            yield response.follow(next_page, callback=self.parse)
