import scrapy

class NewsSpider(scrapy.Spider):
    name = "news_liputan6"
    start_urls = [
        'https://www.liputan6.com/tag/korupsi?page=',
    ]

    def parse(self, response):
        for i in range(15):
            next_page = response.url + str(i)
            yield scrapy.Request(next_page, self.parse_links)

    def parse_links(self, response):
        links = response.xpath('//a[contains(@class, "articles--iridescent-list--text-item__title")]/@href').getall()
 
        for link in links:
            yield scrapy.Request(link, self.parse_contents)

    def parse_contents(self, response):
        yield {
            'title' : response.xpath('//title/text()').get(),
            'contents' : response.xpath('//p//text()[normalize-space()]').getall(),
        }
