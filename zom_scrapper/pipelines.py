# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv
from items import ZomScrapperItem


class ZomScrapperPipeline(object):
    def __init__(self):
        names = ZomScrapperItem().fields
        self.csv_file = open('res.csv', 'wb')
        self.file = csv.DictWriter(self.csv_file, fieldnames=names)
        self.file.writeheader()

    def process_item(self, item, spider):
        self.file.writerow(item)

    def close_spider(self, spider):
        self.csv_file.close()
