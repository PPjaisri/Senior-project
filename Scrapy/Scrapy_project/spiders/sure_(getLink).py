import scrapy
import os
import json

class sure(scrapy.Spider):
    name = 'sure'
    path = os.getcwd()
    save_path = os.path.join(path, 'spiders\\fetch file\\sure_getLink.json')

    start_urls = [
        'https://tna.mcot.net/category/sureandshare'
    ]

    fetch_data = []
    def parse(self, response):
        for item in response.css('div.s-grid.-m1.-d4'):
            for article in item.css('article'):
                header = article.css('a').attrib['title']
                link = article.css('a').attrib['href']
                image = article.css('a').css(
                    'div.pic').css('img').attrib['src']

                self.fetch_data.append({
                    'header': header,
                    'link': link,
                    'image': image
                })

        next_button = response.css('a.next.page-numbers').get()
        if next_button is not None:
            next_page = response.css('a.next.page-numbers').attrib['href']
            yield response.follow(next_page, callback=self.parse)
        else:
            count = len(self.fetch_data)
            self.fetch_data.insert(0, {'total': count})
            json_data = json.dumps(
                self.fetch_data, indent=4, ensure_ascii=False)
            with open(self.save_path, 'a', encoding='utf-8') as fp:
                fp.write(json_data)
