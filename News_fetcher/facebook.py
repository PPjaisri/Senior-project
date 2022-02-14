import os
import re
import logging
from bs4 import BeautifulSoup
from selenium.webdriver import Edge
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service


class facebook(object):
    path = os.getcwd()
    path = os.path.dirname(path)
    binary_location = os.path.join(path, 'msedgedriver.exe')
    binary_location = Service(binary_location)

    def __init__(self, url) -> None:
        self.url = url
        self.browser = Edge(service=self.binary_location)
    def fetch_page(self):
        self.browser.get(self.url)

        self.crawl_page()
        self.finished_crawl()

    def crawl_page(self):
        self.browser.get(self.url)
        response = self.browser.page_source
        soup = BeautifulSoup(response, 'lxml')

        main = soup.find('div', class_='_1dwg _1w_m _q7o')

        poster = main.find('span', class_='fwb').text.strip()
        poster = re.sub(',', ' ', poster)
        content = main.find('div', class_='userContent').text.strip()
        content = ' '.join(content.split())
        content = re.sub(',', ' ', content)
        images = main.find_all('img', class_='scaledImageFitHeight')
        images = [image['src'] for image in images]
        
        data = {
            "poster": poster,
            "content": content,
            "link": self.url.strip(),
            "img": images
        }

        return data

    def finished_crawl(self):
        self.browser.close()
