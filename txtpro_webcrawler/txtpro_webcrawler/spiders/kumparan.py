import scrapy, time, chromedriver_binary
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
class NewsSpider(scrapy.Spider):
    name = "news_kumparan"
    start_urls = [
        'https://kumparan.com/topic/korupsi/',
    ]

    def parse(self, response):
        SCROLL_PAUSE_TIME = 5
        driver = webdriver.Chrome(ChromeDriverManager().install())
        last_height = driver.execute_script("return document.body.scrollHeight")
        driver.get(response.url)
        
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height:
                break

            last_height = new_height

        links = driver.find_elements_by_xpath('//a[contains(@class, "LabelLinkweb-njxxwb-0 izuxWI CardContentweb__CustomLabelLink-sc-1wr516g-2 gCqqNi")]')

        for link in links:
            news_url = response.urljoin(link.get_attribute('href'))
            yield scrapy.Request(news_url, self.parse_contents)

    def parse_contents(self, response):
        yield {
            'title' : response.xpath('//title/text()').get(),
            'contents' : response.xpath('//span[contains(@class, "Textweb__StyledText-sc-2upo8d-0 bHnXqU components__InlineTableText-zjjpg2-0 dWDCSS")]//span//text()[normalize-space()]').getall(),
        }
