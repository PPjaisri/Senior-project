import scrapy
import os
import json
import re

class sure(scrapy.Spider):
    name = 'sure_thread'
    path = os.getcwd()
    save_path = os.path.join(path, 'spiders\\fetch file\\sure_fetch_thread.json')

    start_urls = [
        'https://tna.mcot.net/category/sureandshare'
    ]

    count = 1
    fetch_data = []

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(sure, cls).from_crawler(
            crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed,
                                signal=scrapy.signals.spider_closed)
        return spider

    def parse(self, response):
        last_page = int(response.css('a.page-numbers::text').getall()[-1])
        article = response.css('div.s-grid').css('article')
        for item in article:
            header = item.css('h2').css('a::text').get()
            link = item.css('h2').css('a::attr("href")').get()
            image = ''

            for i in item.css('div.pic').css('img::attr("src")').getall():
                if re.search('tna.mcot.net', i):
                    image = i

            self.fetch_data.append({
                'header': header,
                'link': link,
                'image': image
            })

        print('before fetch others')
        if self.count <= last_page:
            self.count += 1
            link = f'https://tna.mcot.net/category/sureandshare/page/{self.count}'
            print('after fetch others')
            try:
                yield scrapy.Request(link, callback=self.parse)
            except:
                pass

    def spider_closed(self, spider):

        with open(self.save_path, 'r+', encoding='utf-8') as fp:
            json_data = json.dumps(
                self.fetch_data, indent=4, ensure_ascii=False)
            fp.write(json_data)

        spider.logger.info('Spider closed: %s', spider.name)
