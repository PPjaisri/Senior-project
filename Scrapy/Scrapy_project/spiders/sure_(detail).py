import scrapy
import json

class sure_detail(scrapy.Spider):
    name = 'sure_detail'
    index = -1
    path = 'C:\Coding\Senior project\Scrapy_project\sure.json'

    start_urls = [
        'https://tna.mcot.net'
    ]

    next_urls = []

    def fetch(self):
        temp = []
        with open(self.path, encoding='utf-8') as f:
            # f.read()

            # for i in f:
            #     self.next_urls.append(i)

            data = json.load(f)

            for obj in data:
                temp.append(list(obj.values()))
            for item in temp:
                self.next_urls.append(item[1])

    def parse(self, response):
        self.fetch()
        self.index += 1
        for item in response.css('article'):
            header = item.css('header').css('h1::text').get()

            for news in item.css('div.entry-content'):
                if len(news.css('p').css('strong::text').getall()) > 1:
                    category = news.css('p').css('strong::text').getall()[1]
                else:
                    category = None
                detail = news.css('p').getall()
                # detail2 = news.css('p').css('strong::text').get()

                yield {
                    'category': category,
                    'header': header,
                    'detail': detail,
                    'link': response.url
                }

        if self.index <= len(self.next_urls) - 1:
            next_page = self.next_urls[self.index]
            yield response.follow(next_page, callback=self.parse)
