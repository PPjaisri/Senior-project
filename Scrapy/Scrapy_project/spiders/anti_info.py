from scrapy import Spider, Request, signals
import json
import os


class anti_news(Spider):
    name = 'anti_info'

    path = os.getcwd()
    input_path = os.path.join(
        path, 'spiders\\fetch file\\anti_fetch_thread.json')
    save_path = os.path.join(
        path, 'spiders\\fetch file\\anti_info.json')

    fetch_data = []

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(anti_news, cls).from_crawler(
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
            try:
                yield Request(url, callback=self.parse)
            except:
                pass

    def parse(self, response):
        header = response.css('div.title-post-news').css('p::text').get()

        image = response.css(
            'div.-detail, div.gray-image').css('img::attr("src")').getall()

        category = response.css(
            'div.-detail').css('span').css('strong *::text, b *::text').get()

        content = []
        for element in response.css('div.-detail').css('p'):
            paragraph = element.css('p *::text').get()

            if paragraph != None:
                content.append(paragraph)

        data = {
            'category': category,
            'header': header,
            'content': content,
            'link': response.url,
            'image': image
        }

        self.fetch_data.append(data)

    def spider_closed(self, spider):

        with open(self.save_path, 'r+', encoding='utf-8') as fp:
            json_data = json.dumps(
                self.fetch_data, indent=4, ensure_ascii=False)
            fp.write(json_data)

        spider.logger.info('Spider closed: %s', spider.name)
