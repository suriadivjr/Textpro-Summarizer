import scrapy

class NewsSpider(scrapy.Spider):
    name = "news_kompas"
    start_urls = [
        'https://www.kompas.com/tag/korupsi?sort=desc&page=',
    ]

    def parse(self, response):
        for i in range(1, 500):
            next_page = response.url + str(i)
            yield scrapy.Request(next_page, self.parse_links)

    def parse_links(self, response):
        links = response.xpath('//div[contains(@class, "article__asset")]/a/@href').getall()
        
        for link in links:
            yield scrapy.Request(link, self.parse_contents)

    def parse_contents(self, response):
        yield {
            'title' : response.xpath('//title/text()').get(),
            'contents' : response.xpath('//p//text()[normalize-space()]').getall(),
        }
