import re
import logging
import requests
from bs4 import BeautifulSoup


def oryor(url, reference):
    logging.debug(f'Crawing at {url}')
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    header = soup.find('h3', class_='ci').text.strip()
    header = re.sub(',', ' ', header)

    main = soup.find('div', class_='content-detail')

    ul = main.find('div', class_='new-tag')
    ul.decompose()

    content = main.text.strip()
    content = ' '.join(content.split())
    content = re.sub(',', ' ', content)
    
    category = main.find('strong').text.strip()
    
    images_a = soup.find_all('a', id='contect_picture')
    images = [a['href'] for a in images_a]
    
    time = soup.find('h6', class_='ci').text.strip()
    time = ' '.join(time.split())
    time = time.split()[:3]

    data = {
        "category": category,
        "header": header,
        "content": content,
        "link": url.strip(),
        "img": images,
        "reference": reference,
        "time": ' '.join(time)
    }

    return data
