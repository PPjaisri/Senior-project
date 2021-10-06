import scrapy
import json
import os
import re


class cofact_reference(scrapy.Spider):
    name = 'cofact_refer'

    path = os.getcwd()
    file_path = os.path.join(path, 'spiders\\fetch file\\cofact_detail.json')

    fetch_data = []

    def check_domain(self, link):
        # url start at 'https://' or 'http://'
        if len(link.split('//')) > 1:
            domain = link.split('//')[1]
            domain = domain.split('/')[0]
            domain = re.sub('www.', '', domain)
        # url start at 'www.'
        else:
            domain = link.split('/')[0]
            domain = re.sub('www.', '', domain)
        return domain

    def parse_prachachat(self, response):
        link = response.url

        # data = {
        #     "category": "ข่าวจริง",
        #     "header": header,
        #     "content": content,
        #     "link": link,
        #     "img": image
        # }

        # return data

    def parse_matichon(self, response):
        link = response.url

        # data = {
        #     "category": "ข่าวจริง",
        #     "header": header,
        #     "content": content,
        #     "link": link,
        #     "img": image
        # }

        # return data

    def parse_thansettakij(self, response):
        link = response.url

        # data = {
        #     "category": "ข่าวจริง",
        #     "header": header,
        #     "content": content,
        #     "link": link,
        #     "img": image
        # }

        # return data

    def parse_bangkokbiznews(self, response):
        link = response.url

        # data = {
        #     "category": "ข่าวจริง",
        #     "header": header,
        #     "content": content,
        #     "link": link,
        #     "img": image
        # }

        # return data

    def parse_thairath(self, response):
        link = response.url

        # data = {
        #     "category": "ข่าวจริง",
        #     "header": header,
        #     "content": content,
        #     "link": link,
        #     "img": image
        # }

        # return data

    def parse_tnn(self, response):
        link = response.url
        header = response.css('article').css('h1::text').get()
        image = response.css(
            'picture.tnn--thumbnail').css('img::attr("src")').get()

        content = []
        for paragraph in response.css('div.fr-view').css('div'):
            p = paragraph.css('p').css('span::text').get()

            if p != None:
                content.append(p)

        data = {
            "category": "ข่าวจริง",
            "header": header,
            "content": content,
            "link": link,
            "img": image
        }

        return data

    def parse_mgronline(self, response):
        link = response.url
        header = response.css('article').css('h1::text').get()

        content = response.css('div.detail').getall()
        image =  response.css('div.photo-gallery').css('img::attr("src")').getall()

        data = {
            "category": "ข่าวจริง",
            "header": header,
            "content": content,
            "link": link,
            "img": image
        }

        return data

    def parse_thaipbs(self, response):
        link = response.url
        header = response.css('h1::text').get()
        image = response.css('article').css('img::attr("src")').get()

        content = []
        for paragraph in response.css('article'):
            p = paragraph.css('p::text').get()

            if p != None:
                content.append(p)

        data = {
            "category": "ข่าวจริง",
            "header": header,
            "content": content,
            "link": link,
            "img": image
        }

        return data

    def parse_antifakenews(self, response):
        link = response.url

        # data = {
        #     "category": "ข่าวจริง",
        #     "header": header,
        #     "content": content,
        #     "link": link,
        #     "img": image
        # }

        # return data

    def start_requests(self):
        with open(self.file_path, 'r', encoding='utf_8') as fp:
            data = json.load(fp)

        # urls = [website['reference'] for website in data]
        # urls = [website for web_list in urls for website in web_list if website != None]
        urls = ['https://mgronline.com/onlinesection/detail/9640000095556']

        for url in urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        link = self.check_domain(response.url)
        # link = response.url

        if link == 'prachachat.net':
            self.fetch_data.append(self.parse_prachachat(response))
        elif link == 'matichon.co.th':
            self.fetch_data.append(self.parse_matichon(response))
        elif link == 'thansettakij.com':
            self.fetch_data.append(self.parse_thansettakij(response))
        elif link == 'bangkokbiznews.com':
            self.fetch_data.append(self.parse_bangkokbiznews(response))
        elif link == 'thairath.co.th':
            self.fetch_data.append(self.parse_thairath(response))
        elif link == 'tnnthailand.com':
            self.fetch_data.append(self.parse_tnn(response))
        elif link == 'mgronline.com':
            self.fetch_data.append(self.parse_mgronline(response))
        elif link == 'news.thaipbs.or.th':
            self.fetch_data.append(self.parse_thaipbs(response))
        elif link == 'antifakenewscenter.com':
            self.fetch_data.append(self.parse_antifakenews(response))
        else:
            pass
