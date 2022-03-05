import logging
import requests
from bs4 import BeautifulSoup
from . import tools


def antifakenews(url, reference):
    logging.debug(f'Crawing at {url}')
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    header = soup.h1.text.strip()
    time = soup.time['datetime']
    time = tools.time_format(time)
    category = soup.find_all('div', class_='blog-tag')[0].text.strip()
    content_blog = soup.select('div.tdb-block-inner p')
    content = [i.text for i in content_blog]
    image_list = soup.select('div.tdb-block-inner p img')
    image = [i['src'] for i in image_list]

    data = {
        'category': category,
        'header': header,
        'content': content,
        'link': url,
        'img': image,
        'reference': reference,
        'time': time
    }

    return data
