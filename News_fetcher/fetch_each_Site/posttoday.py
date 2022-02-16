import re
import logging
import requests
from bs4 import BeautifulSoup
from . import tools


def postToday(url, reference):
    logging.debug(f'Crawing at {url}')
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    head = soup.find('div', class_='article-headline')
    header = head.find('h2').text.strip()
    header = re.sub(',', ' ', header)

    time = head.find('div').text.strip()
    time = time.split()
    time[2] = re.sub(time[2], tools.tools.return_month(time[2]), time[2])
    time = ' '.join(time[1:4])
    time = tools.tools.time_format(time)

    content = soup.find('div', class_='article-content').text.strip()
    content = ' '.join(content.split())
    content = re.sub(',', ' ', content)

    image_block = soup.find('picture', class_='img-full')
    images = soup.find_all('img', class_='img-f')
    images = [image['data-src'] for image in images if image.has_attr('data-src') is True]

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
