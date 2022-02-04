import re
import logging
import requests
from bs4 import BeautifulSoup


def pptv(url, reference):
    logging.debug(f'Crawing at {url}')
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    header = soup.find('h1').text
    header = re.sub(',', ' ', header)

    article = soup.find('article', class_='pptv-container')
    section = article.find('header')
    section.decompose()
    
    content = article.text.strip()
    content = ' '.join(content.split())
    content = re.sub(header, '', content)
    content = re.sub(',', ' ', content)
    
    images = article.find_all('picture', class_='')
    images = [image.find('img')['src'] for image in images if re.search(
        'img.', image.find('img')['src'])]

    time = soup.find('time')['datetime']
    
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
