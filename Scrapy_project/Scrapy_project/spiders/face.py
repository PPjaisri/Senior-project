import scrapy

class face(scrapy.Spider):
    name = 'face'

    start_urls = [
        'https://www.facebook.com/AntiFakeNewsCenter'
    ]

    def parse(self, response):
        for item in response.css('span.nc684nl6'):
            page = item.css('strong')

            
