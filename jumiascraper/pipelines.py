# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class JumiascraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # clean the price
        if adapter.get("price"):
            price = adapter.get("price").split(" ")[1].replace(",", "")
            adapter["price"] = int(price)

        # clean the rating
        if adapter.get("rating"):
            adapter["rating"] = round(float(adapter.get("rating").split(" ")[0]), 2)

        # clean the number of ratings
        if adapter.get("number_of_ratings"):
            adapter["number_of_ratings"] = int(
                adapter.get("number_of_ratings")[1:].split(" ")[0]
            )

        # clean the product details
        if adapter.get("product_details"):
            adapter["product_details"] = (
                adapter.get("product_details")
                if "\n" not in adapter.get("product_details")
                else None
            )

        return item
