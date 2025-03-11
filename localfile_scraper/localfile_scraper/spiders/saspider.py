import scrapy
from scrapy.http import HtmlResponse
import os

class SaSpider(scrapy.Spider):
    name = 'saspider'
    start_urls = [
        'file://./income_statement.html'
    ]

    def parse(self, response):
        # 在这里提取页面中的数据
        heading = response.xpath('//h1/text()').get()
        theader = response.xpath('//*[@id="main-table"]/thead/tr[1]/th')

        # Iterate over the extracted <th> elements and print their text
        for th in theader:
            text = th.xpath('.//text()').get()  # Extract text content from <th>
            print(text)

