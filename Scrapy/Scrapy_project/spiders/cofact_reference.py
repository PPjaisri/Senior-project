import scrapy
import json
import os
import re


class cofact_reference(scrapy.Spider):
    name = 'cofact_refer'

    path = os.getcwd()
    file_path = os.path.join(path, 'Scrapy_project\\spiders\\fetch file\\cofact_detail.json')
    save_path = os.path.join(path, 'Scrapy_project\\spiders\\fetch file\\cofact_refer.json')
    test_path = os.path.join(path, 'Scrapy_project\\spiders\\fetch file\\cofact_refer_test.json')

    fetch_data = []
    refer_link = ''
    count = 0
    size = 0

    def start_requests(self):
        with open(self.file_path, 'r', encoding='utf_8') as fp:
            data = json.load(fp)

        web = [(website['link'], website['reference']) for website in data]
        
        urls = []
        for (link, refer) in web:
            for each_url in refer:
                if each_url != None:
                    urls.append((link, each_url))

        self.size = len(urls[:15]) - 1
        for url in urls[:15]:
            self.refer_link = url[0]
            yield scrapy.Request(url[1], callback=self.parse)

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

    # def parse_bangkokbiznews(self, response): # 403 forbidden
    #     link = response.url

    #     # data = {
    #     #     "category": "ข่าวจริง",
    #     #     "header": header,
    #     #     "content": content,
    #     #     "link": link,
    #     #     "img": image
    #     # }

    #     # return data

    def parse_thairath(self, response, refer_link):
        link = response.url

        header = response.css('h1::text').get()
        content = response.css('div[itemprop]').css(
            'div').css('div').css('p::text').getall()

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
        for paragraph in response.css('div.fr-view').css('div'):
            p = paragraph.css('p').css('span::text').get()

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

    def parse_mgronline(self, response, refer_link):
        link = response.url
        header = response.css('article').css('h1::text').get()

        content = []
        for paragraph in response.css('div.detail::text').getall():
            text = paragraph.strip()
            content.append(text)

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
        for paragraph in response.css('article'):
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
        for element in response.css('div.-detail'):
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


    def parse(self, response):
        self.count += 1
        print('1', 'count: ', self.count, 'size', self.size, self.count == self.size)
        # status = response.status
        link = self.check_domain(response.url)
        refer_link = self.refer_link
        # print(link)

        if link == 'prachachat.net':
            # print('prachachat.net')
            res = self.fetch_data.append(self.parse_prachachat(response, refer_link))
            if res != None:
                self.fetch_data.append(res)
        elif link == 'matichon.co.th':
            # print('matichon.co.th')
            res = self.fetch_data.append(self.parse_matichon(response, refer_link)) # some 502 bad gateway and som 200 success
            if res != None:
                self.fetch_data.append(res)
        elif link == 'thansettakij.com':
            # print('thansetthakij')
            res = self.fetch_data.append(self.parse_thansettakij(response, refer_link))
            if res != None:
                self.fetch_data.append(res)
        # elif link == 'bangkokbiznews.com':
        #     res = self.fetch_data.append(self.parse_bangkokbiznews(response, refer_link)) # 403 forbidden
            #if res != None:      
            # self.fetch_data.append(res)
        elif link == 'thairath.co.th':
            # print('thairath.co.th')
            res = self.fetch_data.append(self.parse_thairath(response, refer_link))
            if res != None:
                self.fetch_data.append(res)
        elif link == 'tnnthailand.com':
            # print('tnnthailand.com')
            res = self.fetch_data.append(self.parse_tnn(response, refer_link))
            if res != None:
                self.fetch_data.append(res)
        elif link == 'mgronline.com':
            # print('mgronline.com')
            res = self.fetch_data.append(self.parse_mgronline(response, refer_link))
            if res != None:
                self.fetch_data.append(res)
        elif link == 'news.thaipbs.or.th':
            # print('news.thaipbs.ro.th')
            res = self.fetch_data.append(self.parse_thaipbs(response, refer_link))
            if res != None:
                self.fetch_data.append(res)
        elif link == 'antifakenewscenter.com':
            # print('antifakenewscenter.com')
            res = self.fetch_data.append(self.parse_antifakenews(response, refer_link))
            if res != None:
                self.fetch_data.append(res)

        print('2', 'count: ', self.count, 'size', self.size, self.count == self.size)
        if self.count == self.size:
            # print('Finish')
            with open(self.test_path, 'a', encoding='utf-8') as fp:
                data = json.dumps(self.fetch_data, indent=4, ensure_ascii=False)
                fp.write(data)
