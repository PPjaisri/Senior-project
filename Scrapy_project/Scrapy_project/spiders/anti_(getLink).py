import scrapy


class crawlFakeNews(scrapy.Spider):
    name = 'anti'
    add = False

    start_urls = [
        'https://www.antifakenewscenter.com/?s&order_by=date'
    ]

    next_urls = []
    index = -1

    def parse(self, response):
        self.index += 1
        page = response.css('div.pagination').css('a::text').getall()

        if not self.add:
            for i in range(2, int(page[len(page) - 1])):
                self.next_urls.append(
                    f'https://www.antifakenewscenter.com/page/{i}/??s&order_by=date'
                )
            self.add = True

        for item in response.css('div.col-lg-4.col-md-6.col-sm-12.-new.h-zoom'):
            category = item.css('div.-excerpt').css('a::text').get().strip()
            header = item.css('p::text').get().strip()
            link = item.css('a').attrib['href']

            yield {
                'category': category,
                'header': header,
                'link': link
            }

        if self.index <= int(page[len(page) - 1]):
            next_page = self.next_urls[self.index]
            yield response.follow(next_page, callback=self.parse)
