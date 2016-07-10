import scrapy
from scrapy.loader import ItemLoader
from HouseCrawler.items import LjSecHand
from HouseCrawler.pipelines import *
import datetime

class LianjiaSpider(scrapy.Spider):
    name = "lianjia"
#    allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://sh.lianjia.com/ershoufang"
    ]

#    logfile = name + datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

    pipeline = set([
#        MongoPipeline,
#        JsonWriterPipeline,
    ])


    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(settings.getbool('LOG_ENABLE'))

    def parse(self, response):
        for district in response.xpath('.//*[@id="filter-options"]/dl[1]/dd/div[1]/a[position()>1]/@href').extract():
#            name = district.xpath('@gahref').extract()
#            link = district.xpath('@href').extract()
            district_url = 'http://sh.lianjia.com' + district
#            print(district_url)
            yield scrapy.Request(district_url, meta = {'dont_redirect': True,'handle_httpstatus_list': [302]},  callback = self.parse_regions)

    def parse_regions(self, response):
        for region in response.xpath('.//*[@id="filter-options"]/dl[1]/dd/div[2]/a[position()>1]/@href').extract():
            region_url = 'http://sh.lianjia.com' + region
#            print(region_url, last_page)
            yield scrapy.Request(region_url, meta = {'dont_redirect': True,'handle_httpstatus_list': [302]},  callback = self.parse_houselist)

    def parse_houselist(self, response):
        print(response.url)
        total_page = response.xpath('/html/body/div[3]/div[3]/div/div[3]/a[last() - 1]/text()').extract_first(default = '1')
        for page in range(1, int(total_page) + 1):
            houselist_url = response.url + 'd' + str(page)
            yield scrapy.Request(houselist_url, meta = {'dont_redirect': True,'handle_httpstatus_list': [302]},  callback = self.parse_houseitem)


    def parse_houseitem(self, response):

        print(response.url)

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
