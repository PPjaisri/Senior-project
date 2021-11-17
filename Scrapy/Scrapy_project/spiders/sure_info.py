from scrapy import Spider, Request, signals
import json
import os
import re

class sure_info(Spider):
    name = 'sure_info'

    path = os.getcwd()
    input_path = os.path.join(path, 'spiders\\fetch file\\sure_fetch_thread.json')
    save_path = os.path.join(path, 'spiders\\fetch file\\sure_info.json')

    fetch_data = []

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(sure_info, cls).from_crawler(
            crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed,
                                signal=signals.spider_closed)
        return spider

    def start_requests(self):
        urls = []

        with open(self.input_path, 'r', encoding='utf-8') as fp:
            data = json.load(fp)

            for obj in data[1:]:
                urls.append(obj['link'])

        for url in urls:
            yield Request(url, callback=self.parse)

    def spider_closed(self, spider):

        with open(self.save_path, 'r+', encoding='utf-8') as fp:
            json_data = json.dumps(
                self.fetch_data, indent=4, ensure_ascii=False)
            fp.write(json_data)

        spider.logger.info('Spider closed: %s', spider.name)

    def parse(self, response, **kwargs):
        header = response.css('h1::text').get()
        link_id = response.url.split('-')[-1]
        category = response.xpath(
            f'//*[@id="post-{link_id}"]/div/p[2]/strong/text()').get()
        image = []

        img = response.css('div.thumb, figure').css('img::attr("src")').getall()
        for i in img:
            if re.search("tna.mcot.net", i):
                image.append(i)

        content = response.css(
            'div.entry-content').css('p *::text, ol *::text').getall()

        data = {
            'category': category,
            'header': header,
            'content': content,
            'link': response.url,
            'img': image
        }

        self.fetch_data.append(data)
