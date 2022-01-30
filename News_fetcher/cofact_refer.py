import os
import re
import csv
import logging
import requests
import pandas as pd
from bs4 import BeautifulSoup

class cofact_refer(object):
    path = os.getcwd()
    path = os.path.dirname(path)
    file_path = os.path.join(path, 'result\\Cofact\\cofact_info_ref.csv')
    save_path = os.path.join(path, 'result\\Cofact\\cofact_refer.csv')

    def __init__(self):
        self.fetch_data = []
        self.last_link = ''
        self.count = 0
        self.add = False

    def read_latest_save(self):
        try:
            data = pd.read_csv(self.file_path, encoding='utf-8')
            last_link = data.iloc[-1]['link']
            return last_link
        except:
            return ''

    def finished_crawl(self):
        logging.info(f'Crawled {self.count} pages')
        fieldnames = ['category', 'header',
                      'content', 'link', 'img', 'reference', 'time']

        with open(self.save_path, 'a', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if self.last_link != '':
                writer.writerows(self.fetch_data)
            else:
                writer.writeheader()
                writer.writerows(self.fetch_data)

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

    def checkDuplicate(self, refer_link):
        result = False
        refer_data = self.saved_data['reference'].array
        if refer_link in refer_data:
            result = True
        return result

    def fetch_page(self):
        self.last_link = self.read_latest_save()
        urls = []
        with open(self.file_path, 'r', encoding='utf-8') as fp:
            data = fp.readlines()

        for data_dict in data:
            urls.append(data_dict.split(',')[-1])

        new_urls = []
        for url in range(len(urls) - 1, 0, -1):
            new_urls.append(urls[url])

        for url in new_urls:
            for url_ref in url[1]:
                self.count += 1
                ref = url[0]
                try:
                    if self.last_link == url_ref.strip():
                        break
                    self.crawl_page(url_ref, ref)
                except:
                    continue

        self.finished_crawl()

    def crawl_page(self, url, reference):
        link = self.check_domain(url)
        isDuplicate = self.checkDuplicate(reference)

        if isDuplicate:
            return

        if link == 'sanook.com':
            res = self.parse_sanook(url, refer_link)
            if res != None:
                self.fetch_data.insert(0, res)
        # elif link == 'bbc.com':
        #     res = self.parse_bbc(url, refer_link)
        #     if res != None:
        #         self.fetch_data.insert(0, res)
        # elif link == 'pptvhd36.com':
        #     res = self.parse_pptv(url, refer_link)
        #     if res != None:
        #         self.fetch_data.insert(0, res)
        # elif link == 'dailynews.co.th':
        #     res = self.parse_dailynews(url, refer_link)
        #     if res != None:
        #         self.fetch_data.insert(0, res)
        # elif link == 'komchadluek.net':
        #     res = self.parse_komchadluek(url, refer_link)
        #     if res != None:
        #         self.fetch_data.insert(0, res)
        # elif link == 'oryor.com':
        #     res = self.parse_oryor(url, refer_link)
        #     if res != None:
        #         self.fetch_data.insert(0, res)
        # elif link == 'sure.oryor.com':
        #     res = self.parse_sure_oryor(url, refer_link)
        #     if res != None:
        #         self.fetch_data.insert(0, res)
        # elif link == 'prachachat.net':
        #     res = self.parse_prachachat(url, refer_link)
        #     if res != None:
        #         self.fetch_data.insert(0, res)
        # elif link == 'matichon.co.th':
        #     res = self.parse_matichon(url, refer_link)
        #     if res != None:
        #         self.fetch_data.insert(0, res)
        # elif link == 'thansettakij.com':
        #     res = self.parse_thansettakij(url, refer_link)
        #     if res != None:
        #         self.fetch_data.insert(0, res)
        # elif link == 'thairath.co.th':
        #     res = self.parse_thairath(url, refer_link)
        #     if res != None:
        #         self.fetch_data.insert(0, res)
        # elif link == 'tnnthailand.com':
        #     res = self.parse_tnn(url, refer_link)
        #     if res != None:
        #         self.fetch_data.insert(0, res)
        # elif link == 'mgronline.com':
        #     res = self.parse_mgronline(url, refer_link)
        #     if res != None:
        #         self.fetch_data.insert(0, res)
        # elif link == 'news.thaipbs.or.th':
        #     res = self.parse_thaipbs(url, refer_link)
        #     if res != None:
        #         self.fetch_data.insert(0, res)
        # elif link == 'antifakenewscenter.com':
        #     res = self.parse_antifakenews(url, refer_link)
        #     if res != None:
        #         self.fetch_data.insert(0, res)
        else:
            return


if __name__ == '__main__':
    cofact = cofact_refer()
    cofact.fetch_page()
