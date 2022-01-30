import os
import requests
from bs4 import BeautifulSoup

class anti_specific_page(object):
    path = os.getcwd()
    path = os.path.dirname(path)

    def __init__(self, url):
        self.fetch_data = []
        self.last_link = ''
        self.count = 0
        self.url = url

    def fetch_page(self, reference):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')

        header = soup.h1.text.strip()
        time = soup.time.text.strip()
        category = soup.find_all('div', class_='blog-tag')[0].text.strip()
        content_blog = soup.select('div.tdb-block-inner p')
        content = [i.text for i in content_blog]
        image_list = soup.select('div.tdb-block-inner p img')
        image = [i['src'] for i in image_list]

        data = {
            'category': category,
            'header': header,
            'content': content,
            'link': self.url,
            'image': image,
            'reference': reference,
            'time': time
        }

        return data
