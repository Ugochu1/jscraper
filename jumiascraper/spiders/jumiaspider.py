import scrapy
from jumiascraper.items import ProductItem


class JumiaspiderSpider(scrapy.Spider):
    name = "jumiaspider"
    allowed_domains = ["jumia.com.ng"]
    start_urls = ["https://jumia.com.ng"]
    domain = "https://www.jumia.com.ng"

    def parse(self, response):
        categories = response.css("div.flyout a")  # get all the categories
        for category in categories:
            next_category_link = category.attrib.get("href", None)
            if next_category_link is not None:
                if self.domain not in next_category_link:
                    next_category_link = self.domain + next_category_link
                # move to the next page
                yield scrapy.Request(next_category_link, self.getProducts)

    def getProducts(self, response):
        products = response.xpath(
            "//div[@class='-paxs row _no-g _4cl-3cm-shs']/article"
        )
        for product in products:
            next_product_link = product.css("a").attrib.get("href", None)
            if next_product_link is None:
                continue
            # if it exists
            if self.domain not in next_product_link:
                next_product_link = self.domain + next_product_link

            yield scrapy.Request(next_product_link, self.parseProductData)

    def parseProductData(self, response):
        base_brand_url = response.xpath(
            "//div[@class='row card _no-g -fg1 -pas']//div[@class='-phs']//a"
        )[0].attrib[
            "href"
        ]  # get the base url
        product = ProductItem()

        product["name"] = response.xpath(
            "//div[@class='row card _no-g -fg1 -pas']//div[@class='-df -j-bet']//h1/text()"
        ).get()
        product["url"] = response.url
        product["brand"] = response.xpath(
            "//div[@class='row card _no-g -fg1 -pas']//div[@class='-phs']//a[@class='_more']/text()"
        )[0].get()
        product["brand_url"] = (
            base_brand_url
            if self.domain in base_brand_url
            else self.domain + base_brand_url
        )
        product["price"] = response.xpath(
            "//div[@class='row card _no-g -fg1 -pas']//div[@class='-phs']//div[@class='df -i-ctr -fw-w']/span/text()"
        ).get()
        product["rating"] = response.xpath(
            "//div[@class='row card _no-g -fg1 -pas']//div[@class='-phs']//div[@class='stars _m _al']/text()"
        ).get()
        product["number_of_ratings"] = response.xpath(
            "//div[@class='row card _no-g -fg1 -pas']//div[@class='-phs']//div[@class='stars _m _al']/following-sibling::a/text()"
        ).get()
        product["product_details"] = response.xpath(
            "//div[@class='row']//div[@class='card aim -mtm']//div[@class='markup -mhm -pvl -oxa -sc']/text()"
        ).get()
        product["categories"] = self.getCategories(response)

        yield product

    def getCategories(self, response):
        category_list = []

        for category in response.xpath("//div[@class='brcbs col16 -pts -pbm']/a"):
            value = category.css("::text").get()
            if value != "Home":
                category_list.append(value)

        return category_list
