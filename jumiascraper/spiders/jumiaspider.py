import scrapy


class JumiaspiderSpider(scrapy.Spider):
    name = "jumiaspider"
    allowed_domains = ["jumia.com.ng"]
    start_urls = ["https://jumia.com.ng"]

    def parse(self, response):
        pass
