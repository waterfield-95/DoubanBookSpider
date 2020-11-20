# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from fake_useragent import UserAgent
import base64
import random

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class AbuyunProxyMiddleware(object):
    proxyServer = ""
    proxyUser = ""
    proxyPass = ""
    encoded_user_pass = proxyUser + ":" + proxyPass
    proxyAuth = 'Basic' + base64.urlsafe_b64encode(encoded_user_pass.encode()).decode()

    def process_request(self, request, spider):
        request.meta['proxy'] = self.proxyServer
        request.headers['Proxy-Authorization'] = self.proxyAuth
        return None


class CookieMiddleware():
    def process_request(self, request, spider):
        cookies = {
            'll': '118282',
            'bid': 'L010R6yyi8w',
            'gr_user_id': '03cce2dc-e927-40c3-b2c7-3fc248abfcaa',
            '__yadk_uid': '1aNqBAtqGXDn2KEdNtqlHFnbKTG8hNuX',
            '_vwo_uuid_v2': 'D793FAC9C56B44E1AE5F33F751BA726EC|a196d126463d7740bd898895127d6fef',
            'douban-fav-remind': '1',
            '__utmc': '30149280',
            'Hm_lvt_cfafef0aa0076ffb1a7838fd772f844d': '1605604815',
            'Hm_lpvt_cfafef0aa0076ffb1a7838fd772f844d': '1605604815',
            '_ga': 'GA1.2.171069040.1604371207',
            '_gid': 'GA1.2.1044574779.1605610240',
            '__utmz': '30149280.1605616497.27.16.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)',
            '__gads': 'ID=a0f79d81392a0297-220298e5ecc400fd:T=1605670025:RT=1605670025:S=ALNI_MYdGaZXhQmpFfsd4ZmaeoS0h7egmw',
            'viewed': '34876209_35188551_35230260_35217846_34834201_34995553_1002299_3910853_25891307_6533645',
            'ct': 'y',
            '_pk_ref.100001.3ac3': '%5B%22%22%2C%22%22%2C1605678920%2C%22https%3A%2F%2Fwww.google.com%2F%22%5D',
            'ap_v': '0,6.0',
            '__utma': '30149280.171069040.1604371207.1605670025.1605678924.30',
            '_pk_id.100001.3ac3': '2406857cae7303bc.1604371247.29.1605679634.1605671324.',
            '__utmb': '30149280.3.10.1605678924',
        }
        cookies['__utmb'] = '30149280.{}.10.1603168583'.format(random.choice([i for i in range(1, 10)]))
        return None


class DoubanBookSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class DoubanBookDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        ua = UserAgent()
        request.headers['User-Agent'] = ua.random
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
        spider.logger.info('Spider opened: %s' % spider.name)



