import re
import logging
import requests
from bs4 import BeautifulSoup


def thairath(url, reference):
    logging.debug(f'Crawing at {url}')
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    header = soup.find('h1').text
    header = re.sub(',', ' ', header)
    
    main = soup.find('div', class_='css-1x6s6w6')

    content = main.text.strip()
    content = ' '.join(content.split())
    content = re.sub(',', ' ', content)

    images = main.find_all('img')
    images = [image['src'] for image in images]
    
    time = soup.find('div', class_='css-1nkcd4z').find('p').text

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
