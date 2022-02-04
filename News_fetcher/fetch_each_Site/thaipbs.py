import re
import logging
import requests
from bs4 import BeautifulSoup


def thaipbs(url, reference):
    logging.debug(f'Crawing at {url}')
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    header = soup.find('h1').text.strip()
    header = re.sub(',', ' ', header)

    main = soup.find('article', class_='entry-content')

    content = main.text.strip()
    content = ' '.join(content.split())
    content = re.sub(',', ' ', content)

    images = main.find_all('img')
    images = [image['src'] for image in images]

    time = soup.find('div', class_='content-meta').text.strip()
    time = ' '.join(time.split()[:-3]).strip()

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
