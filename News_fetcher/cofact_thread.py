import logging
import os
import re
import csv
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver import Edge
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service

# -*- coding: utf-8 -*-

class cofact_thread(object):
    path = os.getcwd()
    path = os.path.dirname(path)
    binary_location = os.path.join(path, 'msedgedriver.exe')
    binary_location = Service(binary_location)
    save_path = os.path.join(
        path, 'result\\Cofact\\cofact_thread.csv')

    logging.basicConfig(level=logging.DEBUG)

    def __init__(self):
        self.browser = Edge(service=self.binary_location)
        self.fetch_data = []
        self.last_link = ''
        self.finish = False
        self.next = 0
        self.count = 0

    def read_latest_save(self):
        try:
            data = pd.read_csv(self.save_path, encoding='utf-8')
            last_link = data.iloc[-1]['link']
            return last_link
        except:
            return ''

    def finished_crawl(self):
        logging.info(f'Crawled {self.count} pages')
        with open(self.save_path, 'a', encoding='utf-8', newline='') as file:
            fieldnames = ['category', 'header', 'link']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if self.last_link != '':
                writer.writerows(self.fetch_data)
            else:
                writer.writeheader()
                writer.writerows(self.fetch_data)

        self.browser.close()
        logging.info('finished crawling')

    def change_page(self):
        next_page = self.browser.find_element(
            By.CSS_SELECTOR, 'div.wrapper-pager')
        time.sleep(0.5)
        next_page = next_page.find_elements(By.CSS_SELECTOR, 'a')

        if len(next_page) > self.next:
            self.next = len(next_page)
        if len(next_page) >= self.next:
            self.browser.execute_script("arguments[0].click();", next_page[-1])
        else:
            self.finish = True

    def fetch_page(self, url):
        self.browser.get(url)
        self.last_link = self.read_latest_save()

        while not self.finish:
            time.sleep(0.5)
            self.crawl_page()
            self.count += 1
            try:
                self.change_page()
            except:
                continue
                            
        self.finished_crawl()
        
    def crawl_page(self):
        response = self.browser.page_source
        soup = BeautifulSoup(response, 'lxml')
        news_list = soup.find_all('li', class_='card')

        for news in news_list:
            try:
                category = news.find('div', class_='meter-tag').text
                category = re.sub('meter: ', '', category)
            except:
                category = None
            header = news.find('div', class_='item-text').text
            header = re.sub(',', '', header)
            header = ' '.join(header.split())
            link = news.a['href']

            data = {
                'category': category,
                'header': header,
                'link': f'https://cofact.org{link}'
            }

            if f'https://cofact.org{link}' == self.last_link:
                self.finish = True
                return

            self.fetch_data.insert(0, data)

if __name__ == '__main__':
    url = 'https://cofact.org/articles?replyRequestCount=1&before=&after=&filter=solved'
    cofact = cofact_thread()
    cofact.fetch_page(url)