import re
import requests
from bs4 import BeautifulSoup

def sanook(url, refer_link):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    header = soup.find('h1').text
    header = re.sub(',', '', header)
    # time = response.css('time::text').get()
    # time = re.sub('(|)', '', time)

    # content = []
    # for paragraph in response.css('div#EntryReader_0').css('p *::text'):
    #     res = paragraph.get().strip()
    #     if res != '':
    #         content.append(res)

    # image = response.css('div.EntryContent').css(
    #     'div.thumbnail').css('img::attr("src")').getall()

    # data = {
    #     "category": "ข่าวจริง",
    #     "header": header,
    #     "content": content,
    #     "link": url,
    #     "img": image,
    #     "reference": refer_link,
    #     "time": time
    # }

    # return data


url = 'https://www.sanook.com/health/10505/'

sanook(url, 'a')