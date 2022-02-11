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
        self.start_url = 'https://www.facebook.com/'
        self.browser = Edge(service=self.binary_location)

        self.username = 'ppjaisri@gmail.com'
        self.password = '@Pp045403'

    def fetch_page(self):
        self.browser.get(self.url)

        # email = self.browser.find_element(By.NAME, 'email')
        # password = self.browser.find_element(By.NAME, 'pass')
        # login = self.browser.find_element(By.NAME, 'login')

        # email.send_keys(self.username)
        # password.send_keys(self.password)

        self.crawl_page()
        self.finished_crawl()

    def crawl_page(self):
        self.browser.get(self.url)
        response = self.browser.page_source
        soup = BeautifulSoup(response, 'lxml')

        header = soup.find('span', class_='fwb')
        # header = header.text
        print(header)
        with open('test.html', 'w', encoding='utf-8') as file:
            file.write(soup.text)

    def finished_crawl(self):
        self.browser.close()

if __name__ == '__main__':
    link = r'https://www.facebook.com/sheapgamer/posts/1090517985062860'
    face = facebook(link)
    face.fetch_page()