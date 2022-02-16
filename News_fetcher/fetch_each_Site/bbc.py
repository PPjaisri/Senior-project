import re
import logging
import requests
from bs4 import BeautifulSoup
from tools import tools


def bbc(url, reference):
    logging.debug(f'Crawing at {url}')
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    header = soup.find('h1').text
    header = re.sub(',', ' ', header)

    main = soup.find('main')

    content = main.text.strip()
    content = ' '.join(content.split())
    content = re.sub(',', ' ', content)
    content = re.sub('Getty Images', '', content)
    content = re.sub(header, '', content)

    images = main.find_all('img')
    images = [image['src'] for image in images if image != '']

    time = soup.find('time')['datetime']
    time = tools.time_format(time)

    data = {
        "category": "ข่าวจริง",
        "header": header,
        "content": content,
        "link": url.strip(),
        "img": images,
        "reference": reference,
        "time": time
    }

    return data
