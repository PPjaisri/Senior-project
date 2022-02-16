import re
import logging
import requests
from bs4 import BeautifulSoup
from . import tools


def thanSettakij(url, reference):
    logging.debug(f'Crawing at {url}')
    response = requests.get(url, timeout=60)
    soup = BeautifulSoup(response.text, 'lxml')

    header = soup.find('h1').text.strip()
    header = re.sub(',', ' ', header)
    header = ' '.join(header.split())
    
    main = soup.find('div', id='contents')
    time_raw = main.find('div', class_='info').text
    time = time_raw.split('|')[1]
    time = time.split()[:3]
    time[1] = re.sub(time[1], tools.tools.return_month(time[1]), time[1])
    time = ' '.join(time)
    time = tools.tools.time_format(time)

    div = main.find('div', class_='content-related')
    div.decompose()

    content = main.text.strip()
    content = re.sub(time_raw, '', content)
    content = ' '.join(content.split())
    
    images = main.find_all('img')
    images = [image['src'] for image in images]
    
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
    
