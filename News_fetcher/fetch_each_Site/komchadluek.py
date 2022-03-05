import re
import logging
import requests
from bs4 import BeautifulSoup
from . import tools


def komchadluek(url, reference):
    logging.debug(f'Crawing at {url}')
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    header = soup.find('h1').text.strip()
    header = re.sub(',', ' ', header)

    main = soup.find('div', class_='jAUvMO')
    another_news = main.find('div', class_='cdFDeR')
    another_news.decompose()

    content = main.text.strip()
    content = ' '.join(content.split())
    content = re.sub('แท็กที่เกี่ยวข้อง', '', content)

    images = main.find_all('picture')
    images = [image.find('img')['src'] for image in images]

    time = soup.find('div', id='date-update').text.strip().split()
    time[1] = re.sub(time[1], tools.return_month(time[1]), time[1])
    time = ' '.join(time)
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
