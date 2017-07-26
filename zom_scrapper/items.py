# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class ZomScrapperItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Name = Field()
    Address = Field()
    Area = Field()
    Phone = Field()
    Rating = Field()
    RatingVotes = Field()
    Reviews = Field()
    Cuisines = Field()
    Categories = Field()
    Hours = Field()
    Price = Field()
    Range = Field()
    Image = Field()
    URL = Field()
    Listing = Field()


