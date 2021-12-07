from scrapy import signals, Spider, Request
from scrapy.exceptions import CloseSpider
from ast import literal_eval
import pandas as pd
import csv
import os
import re


class cofact_reference(Spider):
    name = 'cofact_refer'

    path = os.getcwd()
    file_path = os.path.join(path, 'spiders\\results\\cofact\\cofact_info_ref.csv')
    save_path = os.path.join(path, 'spiders\\results\\cofact\\cofact_refer.csv')

    fetch_data = []
    last_link = ''
    add = False

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(cofact_reference, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed,
                                signal=signals.spider_closed)
        return spider

    def start_requests(self):
        with open(self.file_path, 'r', encoding='utf_8') as fp:
            csv_reader = csv.reader(fp, delimiter=',')
            data = list(csv_reader)

        urls = []
        for item in data[1:]:
            link = item[2]
            refer = item[3]
            refer_link = literal_eval(refer)
            urls.append((link, refer_link))
        
        new_urls = []
        for url in range(len(urls) - 1, -1, -1):
            new_urls.append(urls[url])

        for url in new_urls:
            for ref in url[1]:
                try:
                    yield Request(ref, meta={'reference': url[0]}, dont_filter=True, callback=self.parse)
                except:
                    continue

    def read_latest_save(self):
        try:
            data = pd.read_csv(self.save_path, encoding='utf-8')
            last_link = data.iloc[-1]['link']
            return last_link
        except:
            return ''


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

    def parse_pptv(self, response, refer_link):
        link = response.url
        header = response.css('h1::text').get()

        content = []
        for paragraph in response.css('section[class^="content-"]').css('p::text, strong::text'):
            res = paragraph.get().strip()
            if res != "":
                content.append(res)

        image = response.css('a[itemprop="contentUrl"]').css(
            'img::attr("src")').getall()

        data = {
            "category": "ข่าวจริง",
            "header": header,
            "content": content,
            "link": link,
            "img": image,
            "reference": refer_link
        }

        return data
    
    def parse_dailynews(self, response, refer_link):
        link = response.url
        header = response.css('h1::text').get()

        content = []
        for paragraph in response.css('div.elementor-widget-container').css('p::text'):
            res = paragraph.get().strip()
            if res != "":
                content.append(res)

        image = []
        for url in response.css('div.elementor-widget-container').css('img.attachment-full::attr("src")').getall():
            if re.search('dailynews', url) != None:
                image.append(url)

        data = {
            "category": "ข่าวจริง",
            "header": header,
            "content": content,
            "link": link,
            "img": image,
            "reference": refer_link
        }

        return data

    def parse_komchadluek(self, response, refer_link):
        link = response.url
        header = response.css('h1::text').getall()[1]

        content = []
        for paragraph in response.css('div.jAUvMO').css('div[id^="section-"]').css('p::text'):
            res = paragraph.get().strip()
            if res != "":
                content.append(res)

        image = []
        for url in response.css('img::attr("src")').getall():
            if re.search('media.komchadluek.net', url) != None:
                image.append(url)

        data = {
            "category": "ข่าวจริง",
            "header": header,
            "content": content,
            "link": link,
            "img": image,
            "reference": refer_link
        }

        return data

    def parse_oryor(self, response, refer_link):
        link = response.url
        header = response.css('div.col-sm-9').css('h3::text').get()

        content = []
        for paragraph in response.css('div.content-detail').css('p::text'):
            content.append(paragraph.get().strip())

        image = []
        for url in response.css('img::attr("src")').getall():
            if re.search('db.oryor.com', url) != None:
                image.append(url)

        data = {
            "category": "ข่าวจริง",
            "header": header,
            "content": content,
            "link": link,
            "img": image,
            "reference": refer_link
        }

        return data

    def parse_sure_oryor(self, response, refer_link):
        link = response.url

        header = response.css('h3::text').get()

        content = []
        for detail in response.css('div.content-detail'):
            content.append(detail.css('p::text').get().strip())

        image = []
        for url in response.css('img::attr("src")').getall():
            if re.search('db.oryor.com', url) != None:
                image.append(url)

        data = {
            "category": "ข่าวจริง",
            "header": header,
            "content": content,
            "link": link,
            "img": image,
            "reference": refer_link
        }

        return data

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

    def parse_matichon(self, response, refer_link):
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

        content = []
        for paragraph in response.css('div.detail').css(
            'div::text, span::text, strong::text').getall():
            temp = paragraph.strip()
            if temp != '':
                content.append(temp)

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
        fieldnames = ['category', 'header', 'content', 'link', 'img', 'reference']
        print(len(self.fetch_data))
        with open(self.save_path, 'a+', encoding='utf-8', newline='') as fp:
            writer = csv.DictWriter(fp, fieldnames=fieldnames)
            if self.last_link != '':
                writer.writerows(self.fetch_data)
            else:
                writer.writeheader()
                writer.writerows(self.fetch_data)
        spider.logger.info('Spider closed: %s', spider.name)

    def parse(self, response):
        link = self.check_domain(response.url)
        refer_link = response.meta['reference']

        if not self.add:
            self.last_link = self.read_latest_save()
            self.add = True

        if link == 'pptvhd36.com':
            res = self.parse_pptv(response, refer_link)
            if res != None:
                self.fetch_data.insert(0, res)
        elif link == 'dailynews.co.th':
            res = self.parse_dailynews(response, refer_link)
            if res != None:
                self.fetch_data.insert(0, res)
        elif link == 'komchadluek.net':
            res = self.parse_komchadluek(response, refer_link)
            if res != None:
                self.fetch_data.insert(0, res)
        elif link == 'oryor.com':
            res = self.parse_oryor(response, refer_link)
            if res != None:
                self.fetch_data.insert(0, res)
        elif link == 'sure.oryor.com':
            res = self.parse_sure_oryor(response, refer_link)
            if res != None:
                self.fetch_data.insert(0, res)
        elif link == 'prachachat.net':
            res = self.parse_prachachat(response, refer_link)
            if res != None:
                self.fetch_data.insert(0, res)
        elif link == 'matichon.co.th':
            res = self.parse_matichon(response, refer_link)
            if res != None:
                self.fetch_data.insert(0, res)
        elif link == 'thansettakij.com':
            res = self.parse_thansettakij(response, refer_link)
            if res != None:
                self.fetch_data.insert(0, res)
        elif link == 'thairath.co.th':
            res = self.parse_thairath(response, refer_link)
            if res != None:
                self.fetch_data.insert(0, res)
        elif link == 'tnnthailand.com':
            res = self.parse_tnn(response, refer_link)
            if res != None:
                self.fetch_data.insert(0, res)
        elif link == 'mgronline.com':
            res = self.parse_mgronline(response, refer_link)
            if res != None:
                self.fetch_data.insert(0, res)
        elif link == 'news.thaipbs.or.th':
            res = self.parse_thaipbs(response, refer_link)
            if res != None:
                self.fetch_data.insert(0, res)
        elif link == 'antifakenewscenter.com':
            res = self.parse_antifakenews(response, refer_link)
            if res != None:
                self.fetch_data.insert(0, res)
        else:
            return

        if self.last_link == refer_link:
            raise CloseSpider('finished')
