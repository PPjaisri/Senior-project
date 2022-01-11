import os
import csv
import logging
import requests
import pandas as pd
from bs4 import BeautifulSoup

class anti_info(object):
    path = os.getcwd()
    path = os.path.dirname(path)

    input_path = os.path.join(path, 'result/Anti/anti_thread.csv')
    save_path = os.path.join(path, 'result/Anti/anti_info.csv')

    logging.basicConfig(level=logging.DEBUG)

    def __init__(self):
        self.fetch_data = []
        self.last_link = ''

    def read_latest_save(self):
        try:
            data = pd.read_csv(self.save_path, encoding='utf-8')
            last_link = data.iloc[-1]['link']
            return last_link
        except:
            return ''

    def finished_crawl(self):
        with open(self.save_path, 'a', encoding='utf-8', newline='') as file:
            fieldnames = ['category', 'header',
                          'content', 'link', 'image', 'time']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if self.last_link != '':
                writer.writerows(self.fetch_data)
            else:
                writer.writeheader()
                writer.writerows(self.fetch_data)

    def fetch_page(self):
        urls = []
        self.last_link = self.read_latest_save()

        with open(self.input_path, 'r', encoding='utf-8') as file:
            data = file.readlines()

            for obj in data:
                if obj != '\n':
                    obj = obj.split(',')
                    urls.append(obj[2])

        new_urls = []
        for url in range(len(urls) - 1, 0, -1):
            new_urls.append(urls[url])

        for url in new_urls:
            if url == self.last_link:
                self.finished_crawl()
                break
            else:
                self.crawl_page(url)

        self.finished_crawl()

    def crawl_page(self, url):
        response = requests.get(url) 
        logging.debug(f'Crawling at {response.url}')
        soup = BeautifulSoup(response.text, 'html.parser')

        header = soup.h1.text.strip()
        category = soup.find_all('div', class_='blog-tag')[0].text.strip()
        content_blog = soup.select('div.tdb-block-inner p')
        content = [i.text for i in content_blog]
        image_list = soup.select('div.tdb-block-inner p img')
        image = [i['src'] for i in image_list]

        data = {
            'category': category,
            'header': header,
            'content': content,
            'link': response.url,
            'image': image
        }

        self.fetch_data.insert(0, data)

anti = anti_info()
anti.fetch_page()