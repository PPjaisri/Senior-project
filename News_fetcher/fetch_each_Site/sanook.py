import re
import logging
import requests
from . import tools
from bs4 import BeautifulSoup


def sanook(url, reference):
    logging.debug(f'Crawing at {url}')
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    header = soup.find('h1').text
    header = re.sub(',', '', header)

    time = soup.find('time')['datetime']
    time = tools.tools.time_format(time)

    content = soup.find('div', id='EntryReader_0').text.strip()
    content = ' '.join(content.split())
    content = re.sub(',', ' ', content)

    div = soup.find('div', class_='jsx-2954975791')
    image = div.find('img')['src']

    data = {
        "category": "ข่าวจริง",
        "header": header,
        "content": content,
        "link": url,
        "img": image,
        "reference": reference,
        "time": time
    }

    return data
