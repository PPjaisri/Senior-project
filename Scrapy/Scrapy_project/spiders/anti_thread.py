import scrapy
import csv
import os


class crawlFakeNews(scrapy.Spider):
    name = 'anti_thread'
    add = False

    path = os.getcwd()
    save_path = os.path.join(
        path, 'spiders\\results\\anti\\anti_thread.csv')

    start_urls = [
        'https://www.antifakenewscenter.com/?s&order_by=date'
    ]

    next_urls = []
    fetch_data = []
    index = 0

    def parse(self, response):
        self.index += 1
        page = response.css('div.pagination').css('a::text').getall()

        if not self.add:
            for i in range(2, int(page[len(page) - 1])):
                self.next_urls.append(
                    f'https://www.antifakenewscenter.com/page/{i}/??s&order_by=date'
                )
            self.add = True

        for item in response.css('div.h-zoom'):
            category = item.css('div.-excerpt').css('a::text').get().strip()
            header = item.css('p::text').get().strip()
            link = item.css('a').attrib['href']

            data = {
                'category': category,
                'header': header,
                'link': link
            }

            self.fetch_data.append(data)

        if self.index < int(page[len(page) - 1]):
            next_page = self.next_urls[self.index - 2]
            yield response.follow(next_page, callback=self.parse)
        if self.index >= int(page[len(page) - 1]):
            fieldnames = ['category', 'header', 'link']
            with open(self.save_path, 'a', encoding='utf-8', newline='') as fp:
                writer = csv.DictWriter(fp, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.fetch_data)
