import scrapy
from scrapy.loader import ItemLoader
from HouseCrawler.items import LjSecHand
from HouseCrawler.pipelines import *
import datetime

class LjtestSpider(scrapy.Spider):
    name = "ljtest"
#    allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://sh.lianjia.com/ershoufang/beicai"
    ]

    custom_settings = {
        'LOG_ENABLED': False,
        'LOG_FILE': 'log',
    }

    pipeline = set([
        MongoPipeline,
#        JsonWriterPipeline,
    ])

    def parse(self, response):

        print(response.url)
#        print("Existing settings: %s" % self.settings.attributes.keys())

        for house in response.xpath('.//*[@id="house-lst"]/li'):
            loader = ItemLoader(LjSecHand(), house)
            loader.add_value('source', '链家')
            loader.add_value('category', 'secendhand')
            loader.add_value('date', datetime.datetime.today())
            loader.add_xpath('title', 'div[2]/h2/a/@title')
            loader.add_value('url', 'http://sh.lianjia.com')
            loader.add_xpath('url', 'div[2]/h2/a/@href')
            loader.add_xpath('district', 'div[2]/div[1]/div[2]/div/a[1]/text()')
            loader.add_xpath('region', 'div[2]/div[1]/div[2]/div/a[2]/text()')
            loader.add_xpath('total_price', 'div[2]/div[2]/div[1]/span/text()')
            loader.add_xpath('layout', 'div[2]/div[1]/div[1]/span[1]/text()')
            loader.add_xpath('area', 'div[2]/div[1]/div[1]/span[2]/text()')
            loader.add_xpath('unit_price', 'div[2]/div[2]/div[2]/text()')
#            loader.add_xpath('floor', )
#            loader.add_xpath('build_time', )
#            loader.add_xpath('direction', )
            loader.add_xpath('location', 'div[2]/div[1]/div[1]/a/span/text()')
            loader.add_xpath('subway', 'div[2]/div[1]/div[3]/div/div/span[@class="fang-subway-ex"]/span/text()')
            loader.add_xpath('taxfree', 'div[2]/div[1]/div[3]/div/div/span[@class="taxfree-ex"]/span/text()')
            loader.add_xpath('haskey', 'div[2]/div[1]/div[3]/div/div/span[@class="haskey-ex"]/span/text()')
            yield loader.load_item()
