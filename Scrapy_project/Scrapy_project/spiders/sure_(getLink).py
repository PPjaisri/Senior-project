import scrapy

class sure(scrapy.Spider):
    name = 'sure'

    start_urls = [
        'https://tna.mcot.net/category/sureandshare'
    ]

    def parse(self, response):
        for item in response.css('div.s-grid.-m1.-d4'):
            for article in item.css('article'):
                header = article.css('a').attrib['title']
                link = article.css('a').attrib['href']
                image = article.css('a').css(
                    'div.pic').css('img').attrib['src']

                yield {
                    'header': header,
                    'link': link,
                    'image': image
                }

        next_button = response.css('a.next.page-numbers').get()
        if next_button is not None:
            next_page = response.css('a.next.page-numbers').attrib['href']
            yield response.follow(next_page, callback=self.parse)