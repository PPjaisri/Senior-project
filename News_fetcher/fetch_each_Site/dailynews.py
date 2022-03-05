import re
import logging
import requests
from bs4 import BeautifulSoup
from . import tools


def dailyNews(url, reference):
    logging.debug(f'Crawing at {url}')
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    header = soup.find('h1').text
    header = re.sub(',', ' ', header)

    main = soup.find('div', class_='content-all')

    content = main.text.strip()
    content = ' '.join(content.split())
    content = re.sub(',', ' ', content)

    images = main.find_all('img')
    images = [image['src'] for image in images]

    time = soup.find('span', class_='date').text
    time = time.strip().split()
    time[2] = re.sub(time[2], tools.return_month(time[2]), time[2])
    time = ' '.join(time[1:4])
    time = tools.time_format(time)

    data = {
        "category": "ข่าวจริง",
        "header": header,
        "content": content,
        "link": url,
        "img": images,
        "reference": reference,
        "time": time
    }

    return data
