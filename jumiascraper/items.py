# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JumiascraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class ProductItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    brand = scrapy.Field()
    brand_url = scrapy.Field()
    price = scrapy.Field()
    rating = scrapy.Field()
    number_of_ratings = scrapy.Field()
    product_details = scrapy.Field()
    categories = scrapy.Field()
