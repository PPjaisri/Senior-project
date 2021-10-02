import scrapy
import json
import os


class crawlFakeNews(scrapy.Spider):
    name = 'anti'
    add = False

    path = os.getcwd()
    save_path = os.path.join(
        path, 'spiders\\fetch file\\antifakenews_getLink.json')

    start_urls = [
        'https://www.antifakenewscenter.com/?s&order_by=date'
    ]

    next_urls = []
    index = 0
    fetch_data = []

    def parse(self, response):
        self.index += 1
        amount = response.css(
            'div.result-fonud').css('h3::text').get().split(' ')
        page = response.css('div.pagination').css('a::text').getall()

        if not self.add:
            self.fetch_data.append({'total': amount[0]})

        if not self.add:
            for i in range(2, int(page[len(page) - 1])):
                self.next_urls.append(
                    f'https://www.antifakenewscenter.com/page/{i}/??s&order_by=date'
                )
            self.add = True

        for item in response.css('div.col-lg-4.col-md-6.col-sm-12.-new.h-zoom'):
            category = item.css('div.-excerpt').css('a::text').get().strip()
            header = item.css('p::text').get().strip()
            link = item.css('a').attrib['href']

            data = {
                'category': category,
                'header': header,
                'link': link
            }

            self.fetch_data.append(data)

        # print(self.index)
        if self.index < int(page[len(page) - 1]):
            next_page = self.next_urls[self.index - 2]
            yield response.follow(next_page, callback=self.parse)
        if self.index >= int(page[len(page) - 1]):
            print('save !!')
            with open(self.save_path, 'a', encoding='utf-8') as fp:
                json_data = json.dumps(
                    self.fetch_data, indent=4, ensure_ascii=False)
                fp.write(json_data)
