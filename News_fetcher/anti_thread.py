import logging
import os
import re
import csv
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver import Edge
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service

class anti_thread(object):
    path = os.getcwd()
    path = os.path.dirname(path)
    path = os.path.dirname(path)
    binary_location = os.path.join(path, 'msedgedriver.exe')
    binary_location = Service(binary_location)

    save_path = os.path.join(path, 'result\\Anti\\anti_thread.csv')

    def __init__(self):
        self.browser = Edge(service=self.binary_location)
        self.fetch_data = []
        self.current_page = 1
        self.finish = False
        self.last_link = ''

    def fetch_page(self, url):
        self.browser.get(url)
        self.last_link = self.read_latest_save()

        page_num = self.browser.find_elements(By.CSS_SELECTOR, 'li.paginationjs-page')
        last_page = int(page_num[-1].text)
        # last_page = 2

        while self.current_page <= last_page:
            if self.finish:
                break
            time.sleep(0.5)
            self.crawl_page()
            self.change_page()

        self.finished_crawl()

    def change_page(self):
        next_page = self.browser.find_element(
            By.CSS_SELECTOR, 'li.paginationjs-next')
        next_page = next_page.find_element(By.CSS_SELECTOR, 'a')
        self.browser.execute_script("arguments[0].click();", next_page)

    def read_latest_save(self):
        try:
            data = pd.read_csv(self.save_path, encoding='utf-8')
            last_link = data.iloc[-1]['link']
            return last_link
        except:
            return ''

    def finished_crawl(self):
        with open(self.save_path, 'a', encoding='utf-8', newline='') as file:
            fieldnames = ['category', 'header', 'link', 'time']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if self.last_link != '':
                writer.writerows(self.fetch_data)
            else:
                writer.writeheader()
                writer.writerows(self.fetch_data)

        self.browser.close()
        logging.info('finished crawling')

    def crawl_page(self):
        response = self.browser.page_source
        soup = BeautifulSoup(response, 'html.parser')
        
        blogs = soup.find_all('div', class_='blog-container')
        for blog in blogs:
            blog_content = blog.find_all('div', class_='blog-content')
            for element in blog_content:
                link = element.find_all('a', href=True)[0]['href']
                link = re.sub(' ', '', link)
                time = element.find_all('div', class_='blog-datetime')[0].text
                header = element.find_all('div', class_='blog-title')[0].text
                header = re.sub(',', '', header)

                if element.find_all('div', class_='tag-status'):
                    status = element.find_all('div', class_='tag-status')[0].text.strip()
                else:
                    status = None

            data = {
                'category': status,
                'header': header,
                'link': link,
                'time': time
            }
            
            if link == self.last_link:
                self.finish = True
                return

            self.fetch_data.insert(0, data)

        self.current_page += 1

if __name__ == '__main__':
    url = 'https://www.antifakenewscenter.com/allcontent/'
    anti = anti_thread()
    anti.fetch_page(url)