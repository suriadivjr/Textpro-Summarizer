import scrapy

class NewsSpider(scrapy.Spider):
    name = "news_cnnindo"
    start_urls = [
        'https://www.cnnindonesia.com/tag/korupsi/',
    ]

    def parse(self, response):
        for i in range(1, 1500):
            next_page = response.url + str(i)
            yield scrapy.Request(next_page, self.parse_links)

    def parse_links(self, response):
        links = response.xpath('//div[contains(@class, "list media_rows middle")]/article/a/@href').getall()

        for link in links:
            yield scrapy.Request(link, self.parse_contents)

    def parse_contents(self, response):
        yield {
            'title' : response.xpath('normalize-space(//h1[contains(@class, "title")]/text())').get(),
            'contents' : response.xpath('//div[contains(@class, "detail_text")]//text()[not (ancestor-or-self::script or ancestor-or-self::noscript or ancestor-or-self::style)]').getall(),
        }
