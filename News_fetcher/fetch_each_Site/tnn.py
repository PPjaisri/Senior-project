import re
import logging
import requests
from . import tools
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin


def tnn(url, reference):
    logging.debug(f'Crawing at {url}')
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')

    header = soup.find('h1').text
    header = re.sub(',', ' ', header)

    main = soup.find('div', class_='tnn--article__textwrap')
    footer = main.find('div', class_='tnn--article__footer')
    footer.decompose()

    content = main.text.strip()
    content = ' '.join(content.split())

    domain = f'{urlparse(url).scheme}://{urlparse(url).hostname}'

    images = main.find_all('img')
    images = [image['src'] for image in images]
    images = [urljoin(domain, image) for image in images]

    time = soup.find('div', class_='section--read')
    time = time.find('span').text
    time = re.sub(',', ' ', time).strip().split()
    time[1] = re.sub(time[1], tools.return_month(time[1]), time[1])
    time = ' '.join(time[:-1])
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
