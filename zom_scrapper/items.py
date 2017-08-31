# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
from scrapy.loader.processors import TakeFirst, MapCompose, Identity, Join
from scrapy.loader import ItemLoader
import re
import unicodedata


class ZomScrapperItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = Field()
    id = Field()
    type = Field()
    address = Field()
    city = Field()
    link = Field()
    cost = Field()
    area = Field()
    rating = Field()
    rating_votes = Field()
    reviews = Field()
    photos = Field()
    cuisines = Field()
    collections = Field()
    latitude = Field()
    longitude = Field()
    opening_hours = Field()
    booking_link = Field()
    highlights = Field()
    phone_nos = Field()


def int_convert(x):
    try:
        return int(x)
    except ValueError:
        return None


def float_convert(x):
    try:
        return float(x)
    except ValueError:
        return None


def unicode_convert(s):
    return unicodedata.normalize('NFKD', s).encode('ascii', 'ignore')


def strip_newline(s):
    try:
        return strip_blank_spaces(s.strip('\n'))
    except Exception:
        return strip_blank_spaces(s)


def strip_blank_spaces(s):
    try:
        return s.strip(' ')
    except Exception:
        return s


def get_latitude(s):
    try:
        result = re.search('%s(.*)%s' % ('markers=', ',pin_res'), s).group(1)
        return result.split(',')[0]
    except:
        return None


def get_longitude(s):
    try:
        print("============Raw lat long data===========")
        print(s)
        result = re.search('%s(.*)%s' % ('markers=', ',pin_res'), s).group(1)
        print("=============long lat data============")
        print(result)
        return result.split(',')[1]
    except:
        return None


class RestItemLoader(ItemLoader):
    default_input_processor = MapCompose(unicode_convert)
    default_output_processor = TakeFirst()

    id_in = MapCompose(int_convert)

    name_in = MapCompose(strip_newline)

    link_in = Identity()

    city_in = MapCompose(str.capitalize)

    cost_in = MapCompose(lambda x: re.sub('[^0-9]+', '', x), int_convert)

    rating_in = MapCompose(unicode.strip, float_convert)

    rating_votes_in = MapCompose(int_convert)
    reviews_in = MapCompose(unicode.strip)
    # photos_in = MapCompose()
    bookmarks_in = MapCompose(int_convert)
    checkins_in = MapCompose(int_convert)

    cuisines_out = Identity()
    collections_out = Identity()

    address_in = MapCompose(unicode.strip)
    address_out = Join()

    latitude_in = MapCompose(get_latitude)
    longitude_in = MapCompose(get_longitude)
    opening_hours_out = Identity()
