import scrapy

class national(scrapy.Spider):
    name = 'national'

    start_urls = [
        'https://thainews.prd.go.th/th/home/index'
    ]

    def parse(self, response):
        for a in response.css('ul.dropdown-menu').css('li'):
            pre = a.css('a::text').get().strip().split(' ')
            link = a.css('a::attr("href")').get()

            title = [word for word in pre if word != '']

            yield {
                'title': title,
                'link': link
            }
