from scrapy import Spider, signals
from scrapy.exceptions import CloseSpider
import csv
import os
import pandas as pd

class anti_thread_old(Spider):
    name = 'anti_thread_old'
    add = False
    skip = False

    path = os.getcwd()
    save_path = os.path.join(
        path, 'spiders\\results\\anti\\anti_thread.csv')

    start_urls = [
        'https://www.antifakenewscenter.com/allcontent/'
    ]

    next_urls = []
    fetch_data = []
    page_size = 0
    index = 0
    last_link = ''

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(anti_thread_old, cls).from_crawler(
            crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed,
                                signal=signals.spider_closed)
        return spider
    def spider_closed(self):
        fieldnames = ['category', 'header', 'link']
        with open(self.save_path, 'a', encoding='utf-8', newline='') as fp:
            writer = csv.DictWriter(fp, fieldnames=fieldnames)
            if len(self.last_link) > 0:
                writer.writerows(self.fetch_data)
            else:
                writer.writeheader()
                writer.writerows(self.fetch_data)

    def fetch_page(self, page_size):
        for i in range(2, page_size):
            link = f'https://www.antifakenewscenter.com/page/{i}/??s&order_by=date'
            self.next_urls.append(link)

    def read_latest_save(self):
        try:
            data = pd.read_csv(self.save_path, encoding='utf-8')
            last_link = data.iloc[-1]['link']
            return last_link
        except:
            return ''

    def parse(self, response):
        self.index += 1
        page = response.css('div.pagination').css('a::text').getall()
        print('page: ', page)
        self.page_size = int(page[len(page) - 1])

        # print(response.url.split('/'))
        if not self.skip:
            if len(response.url.split('/')) > 4:
                page_num = int(response.url.split('/')[4])
                if page_num > self.page_size - 5:
                    self.skip = True
                    return

        if not self.add:
            self.last_link = self.read_latest_save()
            self.fetch_page(self.page_size)
            self.add = True

        for item in response.css('div.h-zoom'):
            category = item.css('div.-excerpt').css('a::text').get().strip()
            header = item.css('p::text').get().strip()
            link = item.css('a').attrib['href']

            if link == self.last_link:
                raise CloseSpider('finished')

            data = {
                'category': category,
                'header': header,
                'link': link
            }

            self.fetch_data.insert(0, data)
            
        if self.index < self.page_size:
            next_page = self.next_urls[self.index - 2]
            yield response.follow(next_page, callback=self.parse)
        else:
            raise CloseSpider('finished')
