import os
import re
import csv
import time
import logging
import requests
import pandas as pd
from bs4 import BeautifulSoup

class sure_thread(object):
    path = os.getcwd()
    path = os.path.dirname(path)

    save_path = os.path.join(path, 'result\\Sure\\sure_thread.csv')

    logging.basicConfig(level=logging.DEBUG)

    def __init__(self):
        self.fetch_data = []
        self.finish = False
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
            fieldnames = ['header', 'link', 'time']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if self.last_link != '':
                writer.writerows(self.fetch_data)
            else:
                writer.writeheader()
                writer.writerows(self.fetch_data)

    def fetch_page(self, url):
        self.last_link = self.read_latest_save()
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        pagination = soup.find_all('a', class_='page-numbers')
        last_page = max([int(i.text) for i in pagination if i.text != ''])
        # last_page = 2
        for i in range(1, last_page + 1):
            if self.finish:
                break
            else:
                next_url = f'{url}/page/{i}'
                time.sleep(0.5)
                self.crawl_page(next_url)

        self.finished_crawl()
                

    def crawl_page(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        items = soup.find_all('article', class_='content-item')
        for item in items:
            link = item.a['href']
            header = item.h2.a.text.strip()
            header = re.sub(',', '', header)
            header = re.sub('"', '', header)
            time = item.find('div', class_='time').text.strip()
            time = ' '.join(time.split())

            data = {
                'header': header,
                'link': link,
                'time': time
            }

            if link == self.last_link:
                self.finish = True
                return

            self.fetch_data.insert(0, data)

if __name__ == '__main__':
    url = 'https://tna.mcot.net/category/sureandshare'
    sure = sure_thread()
    sure.fetch_page(url)