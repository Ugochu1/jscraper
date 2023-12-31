# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


# class JumiascraperSpiderMiddleware:
#     # Not all methods need to be defined. If a method is not defined,
#     # scrapy acts as if the spider middleware does not modify the
#     # passed objects.

#     @classmethod
#     def from_crawler(cls, crawler):
#         # This method is used by Scrapy to create your spiders.
#         s = cls()
#         crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
#         return s

#     def process_spider_input(self, response, spider):
#         # Called for each response that goes through the spider
#         # middleware and into the spider.

#         # Should return None or raise an exception.
#         return None

#     def process_spider_output(self, response, result, spider):
#         # Called with the results returned from the Spider, after
#         # it has processed the response.

#         # Must return an iterable of Request, or item objects.
#         for i in result:
#             yield i

#     def process_spider_exception(self, response, exception, spider):
#         # Called when a spider or process_spider_input() method
#         # (from other spider middleware) raises an exception.

#         # Should return either None or an iterable of Request or item objects.
#         pass

#     def process_start_requests(self, start_requests, spider):
#         # Called with the start requests of the spider, and works
#         # similarly to the process_spider_output() method, except
#         # that it doesn’t have a response associated.

#         # Must return only requests (not items).
#         for r in start_requests:
#             yield r

#     def spider_opened(self, spider):
# spider.logger.info("Spider opened: %s" % spider.name)

# for making API calls
import requests
import random
from urllib.parse import urlencode


class JumiascraperDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls(crawler.settings)
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def __init__(self, settings):
        # the initialize your settings and get all headers
        self.scrapeops_api_key = settings.get("SCRAPEOPS_API_KEY")
        self.scrapeops_header_endpoint = settings.get("SCRAPEOPS_HEADER_ENDPOINT")
        self.scrapeops_num_headers = settings.get("SCRAPEOPS_NUM_HEADERS")
        self.header_list = []

        self._get_header_list()

    def _get_header_list(self):
        # make the API call to get the headers
        params = {"api_key": self.scrapeops_api_key}

        if self.scrapeops_num_headers is not None:
            params["num_headers"] = self.scrapeops_num_headers
        response = requests.get(
            self.scrapeops_header_endpoint, params=urlencode(params)
        )

        json_response = response.json()
        self.header_list = json_response.get("result", [])

    def _get_random_header(self):
        random_index = random.randint(0, len(self.header_list) - 1)
        return self.header_list[random_index]

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        header = self._get_random_header()

        request.headers["upgrade-insecure-requests"] = header["upgrade-insecure-requests"]
        request.headers["user-agent"] = header["user-agent"]
        request.headers["accept"] = header["accept"]
        request.headers["sec-ch-ua"] = header["sec-ch-ua"]
        request.headers["sec-ch-ua-mobile"] = header["sec-ch-ua-mobile"]
        request.headers["sec-ch-ua-platform"] = header["sec-ch-ua-platform"]
        request.headers["sec-fetch-site"] = header["sec-fetch-site"]
        request.headers["sec-fetch-mod"] = header["sec-fetch-mod"]
        request.headers["sec-fetch-user"] = header["sec-fetch-user"]
        request.headers["accept-encoding"] = header["accept-encoding"]
        request.headers["accept-language"] = header["accept-language"]
        
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)
