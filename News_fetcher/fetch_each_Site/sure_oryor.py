import re
import logging
import requests
from bs4 import BeautifulSoup


def sureOryor(url, reference):
    logging.debug(f'Crawing at {url}')
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    header = soup.find('h3', class_='ci').text.strip()
    header = re.sub(',', ' ', header)
    
    main = soup.find('div', class_='content-detail')

    div = main.find('div', class_='wrap-btm-social-btn')
    div.decompose()

    content = main.text.strip()
    content = ' '.join(content.split())
    content = re.sub(',', ' ', content)
    
    images_tag = main.find_all('img')
    images = [iamge['src'] for iamge in images_tag]
    
    time = soup.find('h6', class_='ci').text.strip()
    time = ' '.join(time.split())
    time = time.split()[:3]
    
    data = {
        "category": "ข่าวจริง",
        "header": header,
        "content": content,
        "link": url.strip(),
        "img": images,
        "reference": reference,
        "time": ' '.join(time)
    }

    return data
    