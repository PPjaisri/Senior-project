from scrapy import signals, Spider, Request
import json
import os
import re

class cofact_reference(Spider):
    name = 'cofact_refer'

    path = os.getcwd()
    file_path = os.path.join(path, 'spiders\\fetch file\\cofact_detail.json')
    save_path = os.path.join(path, 'spiders\\fetch file\\cofact_refer.json')
    test_path = os.path.join(path, 'spiders\\fetch file\\cofact_refer_test.json')

    fetch_data = []
    refer_link = ''

    count1, count2 = 0, 0

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(cofact_reference, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed,
                                signal=signals.spider_closed)
        return spider

    def start_requests(self):
        with open(self.file_path, 'r', encoding='utf_8') as fp:
            data = json.load(fp)

        urls = []
        for i in data:
            link = i['link']
            for reference in i['reference']:
                refer = reference['ref-link']
            urls.append((link, refer))
        
        # urls = []
        # for (link, refer) in web:
        #     for each_url in refer:
        #         if each_url != None:
        #             urls.append((link, each_url))
        
        for url in urls:
            self.count1 += 1
            print('count1 =', self.count1)
            for ref in url[1]:
                yield Request(ref, meta={'reference': url[0]}, callback=self.parse)

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

    def parse_prachachat(self, response, refer_link):
        link = response.url

        header = response.css('h1::text').get()
        content = response.css('div.td-post-content').css('p::text').getall()
        image = response.css(
            'div.td-post-content').css('img::attr("src")').get()

        data = {
            "category": "ข่าวจริง",
            "header": header,
            "content": content,
            "link": link,
            "img": image,
            "reference": refer_link
        }

        return data

    def parse_matichon(self, response, refer_link): # some 502 bad gateway and some 200 success
        link = response.url

        header = response.css('h1::text').get()
        content = []

        for element in response.css('div.td-post-content'):
            paragraph = element.css('p::text').get()
            content.append(paragraph)

        image = response.css(
            'div.td-post-content').css('img::attr("src")').get()

        data = {
            "category": "ข่าวจริง",
            "header": header,
            "content": content,
            "link": link,
            "img": image,
            "reference": refer_link
        }

        return data

    def parse_thansettakij(self, response, refer_link):
        link = response.url
        content_path = response.css('div#contents').xpath(
            '//div[re:test(@id, "section-")]')

        header = response.css('h1::text').get()
        content = content_path.css('p::text').getall()
        image = content_path.css('picture').css('img::attr("src")').getall()

        data = {
            "category": "ข่าวจริง",
            "header": header,
            "content": content,
            "link": link,
            "img": image,
            "reference": refer_link
        }

        return data

    def parse_thairath(self, response, refer_link):
        link = response.url

        header = response.css('h1::text').get()
        content = response.css('div[itemprop]').css('p::text').getall()

        image = response.css('picture').css('img::attr("src")').get()

        data = {
            "category": "ข่าวจริง",
            "header": header,
            "content": content,
            "link": link,
            "img": image,
            "reference": refer_link
        }

        return data

    def parse_tnn(self, response, refer_link):
        link = response.url
        header = response.css('article').css('h1::text').get()
        image = response.css(
            'picture.tnn--thumbnail').css('img::attr("src")').get()

        content = []
        for paragraph in response.css('div.tnn--article__textwrap').css('p'):
            p = paragraph.css('p::text').get()

            if p == None:
                p = paragraph.css('p').css('span::text').get()
            else:
                content.append(p)

        data = {
            "category": "ข่าวจริง",
            "header": header,
            "content": content,
            "link": link,
            "img": image,
            "reference": refer_link
        }

        return data

    def parse_mgronline(self, response, refer_link):
        link = response.url
        header = response.css('article').css('h1::text').get()

        content = response.css('div.detail').css(
            'div::text, span::text, strong::text').getall()

        image =  response.css('div.photo-gallery').css('img::attr("src")').getall()

        data = {
            "category": "ข่าวจริง",
            "header": header,
            "content": content,
            "link": link,
            "img": image,
            "reference": refer_link
        }

        return data

    def parse_thaipbs(self, response, refer_link):
        link = response.url
        header = response.css('h1::text').get()
        image = response.css('article').css('img::attr("src")').get()

        content = []
        for paragraph in response.css('article').css('p'):
            p = paragraph.css('p::text').get()

            if p != None:
                content.append(p)

        data = {
            "category": "ข่าวจริง",
            "header": header,
            "content": content,
            "link": link,
            "img": image,
            "reference": refer_link
        }

        return data

    def parse_antifakenews(self, response, refer_link):
        link = response.url

        header = response.css('div.title-post-news').css('p::text').get()
        content = []
        for element in response.css('div.-detail').css('p'):
            paragraph = element.css('p::text').get()

            if paragraph == None:
                paragraph = element.css('p').css('strong::text').get()

            content.append(paragraph)

        image = response.css('div.-detail').css('img::attr("src")').get()

        data = {
            "category": "ข่าวจริง",
            "header": header,
            "content": content,
            "link": link,
            "img": image,
            "reference": refer_link
        }

        return data

    def spider_closed(self, spider):
        with open(self.save_path, 'a', encoding='utf-8') as fp:
            data = json.dumps(self.fetch_data, indent=4, ensure_ascii=False)
            fp.write(data)
        spider.logger.info('Spider closed: %s', spider.name)

    def parse(self, response):
        link = self.check_domain(response.url)
        refer_link = response.meta['reference']
        self.count2 += 1
        print('count2 =', self.count2)

        if link == 'prachachat.net':
            res = self.parse_prachachat(response, refer_link)
            if res != None:
                self.fetch_data.append(res)
        elif link == 'matichon.co.th':
            res = self.parse_matichon(response, refer_link) # some 502 bad gateway and som 200 success
            if res != None:
                self.fetch_data.append(res)
        elif link == 'thansettakij.com':
            res = self.parse_thansettakij(response, refer_link)
            if res != None:
                self.fetch_data.append(res)
        elif link == 'thairath.co.th':
            res = self.parse_thairath(response, refer_link)
            if res != None:
                self.fetch_data.append(res)
        elif link == 'tnnthailand.com':
            res = self.parse_tnn(response, refer_link)
            if res != None:
                self.fetch_data.append(res)
        elif link == 'mgronline.com':
            res = self.parse_mgronline(response, refer_link)
            if res != None:
                self.fetch_data.append(res)
        elif link == 'news.thaipbs.or.th':
            res = self.parse_thaipbs(response, refer_link)
            if res != None:
                self.fetch_data.append(res)
        elif link == 'antifakenewscenter.com':
            res = self.parse_antifakenews(response, refer_link)
            if res != None:
                self.fetch_data.append(res)
        else:
            return
