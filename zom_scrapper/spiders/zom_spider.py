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
        # if next_link:
        #     yield scrapy.Request(response.urljoin(next_link[0]), callback=self.parse)

    def parse_restaurants(self, response):
        rest = RestItemLoader(item=ZomScrapperItem(), response=response)

        rest.add_xpath('name', '//*[@id="mainframe"]/div[1]/div/div[1]/div[1]/div/div[2]/div[1]/div[1]/h1/a/text()')
        rest.add_xpath('id', '//*/@data-res-id')
        rest.add_css('type', 'div.res-info-estabs > a::text')
        rest.add_value('link', response.url)
        rest.add_value('city',  findall('\\.com\/([a-z]+)\/', response.url))
        rest.add_css('cost', 'span[itemprop="priceRange"]::text')
        rest.add_xpath('area', '//*[@id="mainframe"]/div[1]/div/div[1]/div[3]/div[1]/div[2]/div[3]/div[1]/div/span/span/text()')
        rest.add_xpath('rating', '//*[@id="mainframe"]/div[1]/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div/div/div/div/text()')
        rest.add_xpath('rating_votes', '//*[@id="mainframe"]/div[1]/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div/div/span[1]/span/span/text()')
        rest.add_xpath('reviews', '//*[@id="reviews-container"]/div[1]/div[3]/div[1]/div[1]/div/div[1]/div[1]/div[1]/div[2]/a[1]/div/text()')
        # rest.add_xpath('photos', '//*[@id="progressive_image"]/div[1]/@style::background-image')
        rest.add_css('bookmarks', "div#wtt_count::text")
        rest.add_css('checkins', "div#bt_count::text")
        rest.add_xpath('cuisines', '//*[@id="mainframe"]/div[1]/div/div[1]/div[3]/div[1]/div[1]/div[2]/div/div/a[1]/text()')
        rest.add_css('collections', "span.res-page-collection-text > a::text")
        rest.add_xpath('address', '//*[@id="mainframe"]/div[1]/div/div[1]/div[3]/div[1]/div[2]/div[3]/div[1]/div/span/text()[1]')
        rest.add_value('latitude', value=response.selector.re("\|([\d.]+),[\d.]+\|"))
        rest.add_value('longitude', value=response.selector.re("\|[\d.]+,([\d.]+)\|"))
        rest.add_xpath('opening_hours', '//*[@id="mainframe"]/div[1]/div/div[1]/div[3]/div[1]/div[2]/div[1]/div/div/div[2]/div/div[1]/text()')
        rest.add_xpath('booking_link', '//*[@id="res_page_book_tab"]')
        rest.add_xpath('highlights', '//*[@id="mainframe"]/div[1]/div/div[1]/div[3]/div[1]/div[3]/div[1]/div/div[1]/div/text()')
        yield rest.load_item()

