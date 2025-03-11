# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.http import HtmlResponse
from urllib.parse import urlparse
import os

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class LocalfileScraperSpiderMiddleware:
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


class LocalfileScraperDownloaderMiddleware:
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
        # Check if the request URL is a file:// URL
        if request.url.startswith('file://'):
            # Extract the local file path from the URL
            file_path = self.get_local_file_path(request.url)
            
            # Check if the file exists on the local file system
            if os.path.exists(file_path):
                with open(file_path, 'rb') as f:
                    body = f.read()
                
                # Return an HtmlResponse (or Response for non-HTML files) with the file content
                return HtmlResponse(url=request.url, body=body, encoding='utf-8')
        
        # If the file doesn't exist, continue the request processing (fall back to HTTP download)
        return None

    def get_local_file_path(self, url):
        # Extract the local file path from the file URL
        parsed_url = urlparse(url)
        
        # We assume that the file URL uses 'file:///' or 'file://' scheme
        file_path = parsed_url.netloc + parsed_url.path
        
        # Convert the file path to the correct system path (on Unix, no need to remove '/')
        return file_path

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
