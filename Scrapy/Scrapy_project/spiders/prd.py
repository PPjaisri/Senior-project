import scrapy

class nnt(scrapy.Spider):
    name = 'nnt'

    start_urls = [
        'https://thainews.prd.go.th/th/news/category/7'
    ]

    def parse(self, response):
        category = 'foreign'

        for item in response.css('div.tab-pane.fade.in.active.col-xs-12.nopadding'):
            for news in item.css('div.col-xs-12.col-sm-4.boxItem.nopadmobile'):
                header = news.css('p::text').get()
                link = news.css('a').attrib['href']
                date = news.css('a').css('h4::text').get()

                yield {
                    'category': category,
                    'header': header,
                    'link': link,
                    'date': date
                }
