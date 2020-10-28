import re
import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = ["http://quotes.toscrape.com"]

    xpaths = {
        "quotes": '//div[@class="quote"]',
        "name": './span/small[@class="author"]/text()',
        "quote": './span[@class="text"]/text()',
        "next_page": '//li[@class="next"]/a/@href',
    }

    num_pages = 20

    def parse(self, response):
        quotes_selector = response.xpath(self.xpaths["quotes"])
        for quote_selector in quotes_selector:
            name = quote_selector.xpath(self.xpaths["name"]).get()
            quote = quote_selector.xpath(self.xpaths["quote"]).get()

            yield {"name": name, "quote": quote}

        next_page = response.xpath(self.xpaths["next_page"]).get()
        print(next_page)
        if next_page:
            match = re.search(r"/page/(\d+)/", next_page)
            if match:
                page_number = int(match.group(1))
                if page_number <= self.num_pages:
                    next_page_url = response.urljoin(next_page)
                    yield scrapy.Request(url=next_page_url, callback=self.parse)
