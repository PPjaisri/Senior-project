import json
import scrapy


class national_subLink(scrapy.Spider):
    name = 'national_subLink'

    def start_requests(self):
        urls = []
        with open('C:/Coding/Senior project/Scrapy/result_json/national.json', encoding='utf-8') as fp:
            data = json.load(fp)

            for obj in data:
                urls.append(obj['link'])

        # for url in urls:
        #     yield scrapy.Request(url=url, callback=self.parse)
        yield scrapy.Request(url=urls[16], callback=self.parse)

    def parse(self, response):
        links = []

        for element in response.css('ul.pagination.font_lv3.th-saraban').css('li'):
            if element.css('a::attr("rel")').get() == 'next':
                next_page = element.css('a::attr("href")').get()
        
        for element in response.css('div.tab-pane.fade.in.active.col-xs-12.nopadding').css('div'):
            link = element.css('a::attr("href")').get()
            title = element.css('a::attr("title")').get()
            if link != None:
                if title != None:
                    links.append((link, title))

        for link in links[1::]:
            yield {
                'link': link,
                'next': next_page
            }

        if next_page != None:
            yield scrapy.Request(url=next_page, callback=self.parse)
