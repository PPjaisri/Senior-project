import scrapy
import json
import os

class anti_news(scrapy.Spider):
    name = 'anti_news'
    count = -1
    index = -1
    add = False

    path = os.getcwd()
    file_path = os.path.join(
        path, 'spiders\\fetch file\\antifakenews_getLink.json')
    save_path = os.path.join(
        path, 'spiders\\fetch file\\antifakenews_detail.json')

    start_urls = [
        'https://www.antifakenewscenter.com'
    ]

    fetch_urls = []
    fetch_data = []

    def fetch(self):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            for obj in data[1:]:
                self.fetch_urls.append(obj['link'])

    def parse(self, response):
        if not self.add:
            self.fetch()
            self.add = True

        self.index += 1

        for item in response.css('div.-detail'):
            category = item.css('p').css('span').css('strong::text').get()
            category2 = item.css('p').css('span').css('b::text').get()
            detail = item.css('p::text').getall()
            detail2 = item.css('p').css('span::text').getall()

            if category:
                if len(detail) != 0:
                    self.fetch_data.append({
                        'category': category,
                        'detail': detail,
                        'link': response.url
                    })
                else:
                    self.fetch_data.append({
                        'category': category,
                        'detail': detail2,
                        'link': response.url
                    })
            else:
                if len(detail) != 0:
                    self.fetch_data.append({
                        'category': category2,
                        'detail': detail,
                        'link': response.url
                    })
                else:
                    self.fetch_data.append({
                        'category': category2,
                        'detail': detail2,
                        'link': response.url
                    })
        
        print(self.index, len(self.fetch_urls))
        if self.index < len(self.fetch_urls) - 1:
            next_page = self.fetch_urls[self.index]
            yield response.follow(next_page, callback=self.parse)
        elif self.index >= len(self.fetch_urls) - 1:
            json_data = json.dumps(
                self.fetch_data, indent=4, ensure_ascii=False)
            with open(self.save_path, 'a', encoding='utf-8') as fp:
                fp.write(json_data)
