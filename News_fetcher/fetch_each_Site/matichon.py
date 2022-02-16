import re
import logging
import requests
from bs4 import BeautifulSoup

from .tools import tools

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 Edg/97.0.1072.76'
}


def matichon(url, reference):
    logging.debug(f'Crawing at {url}')
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')

    header = soup.find('h1').text
    header = re.sub(',', ' ', header)

    main = soup.find('div', class_='td-post-content')
    
    content = main.text.strip()
    content = ' '.join(content.split())
    content = re.sub(',', ' ', content)
    
    images = main.find_all('img')
    images = [image['src'] for image in images]

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
