import scrapy
from scrapy.spiders import Spider
from re import findall
from zom_scrapper.items import ZomScrapperItem
from zom_scrapper.items import RestItemLoader


class ZomSpider(Spider):
    name = 'zom_spider'

    allowed_domains = ['zomato.com']

    start_urls = [
        'https://www.zomato.com/ncr/restaurants?page=1',
    ]

    def parse(self, response):
        for rest in response.css('a.result-title'):
            url = rest.xpath('@href').extract()[0]
            yield scrapy.Request(url, callback=self.parse_restaurants)

        next_link = response.css('li.current + li.active a').xpath('@href').extract()
        print "NEXT LINK:", next_link
        for i in range(2, 947):
            url = 'https://www.zomato.com/ncr/restaurants?page={0}'.format(i)
            print("========scrapping %s==========" %url)
            yield scrapy.Request(response.urljoin(url), callback=self.parse)

    def parse_restaurants(self, response):
        rest = RestItemLoader(item=ZomScrapperItem(), response=response)

        rest.add_xpath('name', '//*[@id="mainframe"]/div[1]/div/div[1]/div[1]/div/div[2]/div[1]/div[1]/h1/a/text()')
        rest.add_xpath('id', '//*/@data-res-id')
        rest.add_xpath('type', '//*[@id="mainframe"]/div[1]/div/div[1]/div[1]/div/div[2]/div[1]/div[1]/div[1]/span[2]/a[1]/text()')
        rest.add_xpath('link', '//*[@id="mainframe"]/div[1]/div/div[1]/div[1]/div/div[2]/div[1]/div[1]/h1/a/@href')
        rest.add_value('city',  findall('\\.com\/([a-z]+)\/', response.url))
        rest.add_xpath('cost', '//*[@id="mainframe"]/div[1]/div/div[1]/div[3]/div[1]/div[1]/div[3]/div/div/span[2]/text()')
        rest.add_xpath('area', '//*[@id="mainframe"]/div[1]/div/div[1]/div[3]/div[1]/div[2]/div[3]/div[1]/div/span/span/text()')
        rest.add_xpath('rating', '//*[@id="mainframe"]/div[1]/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div/div/div/div/text()')
        rest.add_xpath('rating_votes', '//*[@id="mainframe"]/div[1]/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div/div/span[1]/span/span/text()')
        rest.add_xpath('reviews', '//*[@id="reviews-container"]/div[1]/div[3]/div[1]/div[1]/div/div[1]/div[1]/div[1]/div[2]/a[1]/div/text()')
        rest.add_xpath('photos', '//*[@id="mainframe"]/div[1]/div/div[1]/div[5]/div/div/div[1]/a/img/@src/text()')
        rest.add_xpath('cuisines', '//*[@id="mainframe"]/div[1]/div/div[1]/div[3]/div[1]/div[1]/div[2]/div/div/a[1]/text()')
        rest.add_xpath('address', '//*[@id="mainframe"]/div[1]/div/div[1]/div[3]/div[1]/div[2]/div[3]/div[1]/div/span/text()[1]')
        # rest.add_value('latitude', value=response.selector.re("\|([\d.]+),[\d.]+\|"))
        # rest.add_value('longitude', value=response.selector.re("\|[\d.]+,([\d.]+)\|"))
        rest.add_xpath('opening_hours', '//*[@id="mainframe"]/div[1]/div/div[1]/div[3]/div[1]/div[2]/div[1]/div/div/div[2]/div/div[1]/text()')
        rest.add_xpath('booking_link', '//*[@id="res_page_book_tab"]')
        rest.add_xpath('highlights', '//*[@id="mainframe"]/div[1]/div/div[1]/div[3]/div[1]/div[3]/div[1]/div/div[1]/div/text()')
        rest.add_xpath('phone_nos', '//*[@id="phoneNoString"]/span/span/span/text()')
        rest.add_xpath('latitude', '//*[@id="res-map-canvas"]/div[2]/@data-url')
        rest.add_xpath('longitude', '//*[@id="res-map-canvas"]/div[2]/@data-url')
        yield rest.load_item()

