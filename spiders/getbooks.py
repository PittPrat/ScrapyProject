import scrapy
import csv

class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["http://books.toscrape.com/"]
    
    def __init__(self):
        self.file = open('books_data.csv', 'w', newline='', encoding='utf-8')
        self.writer = csv.writer(self.file)
        self.writer.writerow(['Title', 'Price', 'Star', 'URL', 'Availability', 'Description'])
        self.book_count = 0
        self.books_required = 1000
    
    def parse(self, response):
        books = response.xpath('//article[@class="product_pod"]')
        # Extracting data from each book and its url
        for book in books:
            if self.book_count >= self.books_required:
                break
                
            rel_url = book.xpath('.//h3/a/@href').extract_first()
            abs_url = response.urljoin(rel_url)
            yield scrapy.Request(url=abs_url, callback=self.parse_book)

        # Move to the next page    
        next_page = response.xpath('//li[@class="next"]/a/@href').extract_first()
        if next_page and self.book_count < self.books_required:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_url, callback=self.parse)
    
    def parse_book(self, response):
        self.book_count += 1
        
        # Extracting Title 
        title = response.xpath('//div[contains(@class, "product_main")]/h1/text()').extract_first()
        if not title:
            title = "Title not found"
        
        # Extracting Star Rating
        star_class = response.xpath('//p[contains(@class, "star-rating")]/@class').extract_first()
        star = star_class.split()[1] if star_class else "Unknown"
        
        url = response.url
        
        # Extracting Price from the table in product page - row "Price (Incl. tax)" and get its value
        price = response.xpath('//th[contains(text(), "Price (excl. tax)")]/following-sibling::td/text()').extract_first()
        if price:
            price = price.strip().replace('£', '')
        else:
            price = "Price not found"
        
        # Extracting availability
        availability = response.xpath('//th[contains(text(), "Availability")]/following-sibling::td/text()').extract_first()
        if not availability:
            availability = "Availability not found"
        
        # Extracting description
        description = response.xpath('//div[@id="product_description"]/following-sibling::p/text()').extract_first()
        if not description:
            description = "No description available"
        else:
            description = description.strip()
        
        # Printing extraction results for debugging
        # print(f"Book #{self.book_count}: {title}")
        # print(f"  URL: {url}")
        # print(f"  Price: {price}")
        # print(f"  Star: {star}")
        # print(f"  Availability: {availability}")
        # print(f"  Description: {description[:50]}..." if len(description) > 50 else f"  Description: {description}")
        
        # Writing the extracted data to the CSV file
        self.writer.writerow([title, price, star, url, availability, description])
        
        yield {
            'Title': title,
            'Price': price,
            'Star': star,
            'URL': url,
            'Availability': availability,
            'Description': description
        }
    
    def closed(self, reason):
        self.file.close()
        print(f"Spider closed: {reason}. Total books scraped: {self.book_count}")