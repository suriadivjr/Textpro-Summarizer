import scrapy

class NewsSpider(scrapy.Spider):
    name = "news_detik"
    start_urls = [
        'https://www.detik.com/search/searchnews?query=korupsi&sortby=time&page=',
    ]

    def parse(self, response):
        for i in range(1,1115):
            next_page = response.url + str(i)
            yield scrapy.Request(next_page, self.parse_links)

    def parse_links(self, response):
        links = response.xpath('//div[contains(@class, "list media_rows list-berita")]/article/a/@href').getall()

        for link in links:
            yield scrapy.Request(link, self.parse_contents)        

    def parse_contents(self, response):
        yield {
            'title' : response.xpath('//title/text()').get(),
            'contents' : response.xpath('//p//text()[normalize-space()]').getall(),
        }
