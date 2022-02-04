import re
import logging
import requests
from bs4 import BeautifulSoup


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
    
    time = soup.find('div', class_='iRAivw').text.strip()
    
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
