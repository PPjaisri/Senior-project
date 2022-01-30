import logging
import os
import re
import csv
import time
import logging
import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver import Edge
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service

class cofact_info(object):
    path = os.getcwd()
    path = os.path.dirname(path)
    file_path = os.path.join(path, 'result\\Cofact\\cofact_thread.csv')
    save_path = os.path.join(path, 'result\\Cofact\\cofact_info.csv')
    save_path_ref = os.path.join(path, 'result\\Cofact\\cofact_info_ref.csv')

    binary_location = os.path.join(path, 'msedgedriver.exe')
    binary_location = Service(binary_location)

    def __init__(self):
        self.browser = Edge(service=self.binary_location)
        self.fetch_data = []
        self.fetch_data_ref = []
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
        fieldnames = ['category', 'header', 'content', 'image', 'link']
        fieldnames_ref = ['category', 'content', 'link', 'ref-link']

        with open(self.save_path, 'a', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if self.last_link != '':
                writer.writerows(self.fetch_data)
            else:
                writer.writeheader()
                writer.writerows(self.fetch_data)

        with open(self.save_path_ref, 'a', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames_ref)
            if self.last_link != '':
                writer.writerows(self.fetch_data_ref)
            else:
                writer.writeheader()
                writer.writerows(self.fetch_data_ref)

        self.browser.close()

    def fetch_page(self):
        self.last_link = self.read_latest_save()
        urls = []
        with open(self.file_path, 'r', encoding='utf-8') as fp:
            data = fp.readlines()

        for data_dict in data:
            urls.append(data_dict.split(',')[2])

        new_urls = []
        for url in range(len(urls) - 1, 0, -1):
            new_urls.append(urls[url])

        for url in new_urls:
            self.count += 1
            try:
                if self.last_link == url.strip():
                    break
                time.sleep(0.5)
                self.crawl_page(url)
            except:
                continue

        self.finished_crawl()

    def crawl_page(self, url):
        logging.debug(f'Crawling at {url}')
        self.browser.get(url)
        self.browser.set_page_load_timeout(1)
        self.browser.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        response = self.browser.page_source
        soup = BeautifulSoup(response, 'lxml')

        category = soup.find('div', class_='meter-tag').text
        category = re.sub('meter: ', '', category)
        try:
            header = soup.find('div', class_='item-title').text
        except:
            header = None

        thread_body = soup.find('div', class_='card-body')
        image = thread_body.find_all('img')
        if len(image) == 0:
            image = None
        
        # Thread content
        try:
            content = soup.find('article', class_='content').text
            content = ' '.join(content.split())
        except:
            content = None

        # Comment Content
        comments = self.browser.find_elements(By.CSS_SELECTOR, 'div.root.card')
        for comment in comments:
            try:
                button = comment.find_element(By.CSS_SELECTOR, 'button.more')
                button.click()
            except:
                pass
            
            content_ref = comment.find_element(By.CSS_SELECTOR, 'div.bubble').text
            content_ref = re.sub('ย่อรายละเอียด', '', content_ref)
            content_ref = ' '.join(content_ref.split())

            section = comment.find_elements(
                By.CSS_SELECTOR, 'section')
            
            refer_link = section[1].find_element(By.CSS_SELECTOR, 'a').text

            data_ref = {
                'category': category,
                'content': content_ref,
                'link': url.strip(),
                'ref-link': refer_link
            }
            
            self.fetch_data_ref.append(data_ref)

        data = {
            'category': category,
            'header': header,
            'content': content,
            'image': image,
            'link': url.strip()
        }

        self.fetch_data.insert(0, data)

if __name__ == '__main__':
    cofact = cofact_info()
    cofact.fetch_page()