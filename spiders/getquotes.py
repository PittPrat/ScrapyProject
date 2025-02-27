import scrapy


class GetquotesSpider(scrapy.Spider):
    name = "getquotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/page/1"]

    def parse(self, response):
        # authors = response.xpath('//small[@class="author"]/text()').extract()
        # for author in authors:
        #     yield {
        #         'author': author
        #     }
        #next_page
        # quotes = response.xpath('//span[@class="text"]/text()').extract()
        # for i in range(len(authors)):
        #     yield {
        #         'author': authors[i],
        #         'quote': quotes[i]
        #     }
        # next_page = response.xpath('//li[@class="next"]/a/@href').extract_first()
        # if next_page is not None:
        #     next_page_link = response.urljoin(next_page)
        #     yield scrapy.Request(url=next_page_link, callback=self.parse)
        quotes = response.xpath('//div[@class="quote"]')
        for quote in quotes:
            author = quote.xpath('span/small[@class="author"]/text()').extract_first()
            text = quote.xpath('span[@class="text"]/text()').extract_first()[1:-1]
            tag = quote.xpath('div[@class="tags"]/meta/@content').extract_first()
            rel_url = quote.xpath('span/a/@href').extract_first()
            abs_url = response.urljoin(rel_url)
            yield {'Author': author, 'Text': text, 'Tag': tag, 'URL': abs_url}

        next_page = response.xpath('//li[@class="next"]/a/@href').extract_first()
        next_page_url = response.urljoin(next_page)
        yield scrapy.Request(url=next_page_url, callback=self.parse)