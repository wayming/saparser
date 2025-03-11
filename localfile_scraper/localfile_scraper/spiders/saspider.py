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
        
        trs = response.xpath('//*[@id="main-table"]/tbody/tr')
        for tr in trs:
            tds = tr.xpath('.//td')
            
            div = tds[0].xpath('.//div//text()').get()
            if div is not None:
                print(div)
            else:
                print(tds[0].xpath('.//a//text()').get())

            for td in tds[1:]:
                print(td.xpath('.//text()').get())

