import scrapy
import json
import os

class sure_detail(scrapy.Spider):
    name = 'sure_detail'
    index = -1
    add = False
    path = os.getcwd()
    file_path = os.path.join(path, 'spiders\\fetch file\\sure_getLink.json')
    save_path = os.path.join(path, 'spiders\\fetch file\\sure_detail.json')

    start_urls = [
        'https://tna.mcot.net'
    ]

    next_urls = []
    fetch_data = []

    def fetch(self):
        with open(self.file_path, encoding='utf-8') as f:

            data = json.load(f)

            for obj in data[1:]:
                self.next_urls.append(obj['link'])

    def parse(self, response):
        if not self.add:
            self.fetch()
            self.add = True
        
        self.index += 1

        image = response.css('div.thumb').css('img::attr("src")').get()

        for item in response.css('article'):
            header = item.css('header').css('h1::text').get()

            for news in item.css('div.entry-content'):
                if len(news.css('p').css('strong::text').getall()) > 1:
                    category = news.css('p').css('strong::text').getall()[1]
                else:
                    category = None
                detail = news.css('p').getall()
                # detail2 = news.css('p').css('strong::text').get()

                self.fetch_data.append({
                    'category': category,
                    'header': header,
                    'content': detail,
                    'link': response.url,
                    'img': image
                })

        print(self.index, len(self.next_urls))
        if self.index < len(self.next_urls) - 1:
            next_page = self.next_urls[self.index]
            yield response.follow(next_page, callback=self.parse)
        elif self.index >= len(self.next_urls) - 1:
            json_data = json.dumps(
                self.fetch_data, indent=4, ensure_ascii=False)
            with open(self.save_path, 'a', encoding='utf-8') as fp:
                fp.write(json_data)
