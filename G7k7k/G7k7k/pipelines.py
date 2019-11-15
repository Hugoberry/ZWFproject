# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

from main import num


class G7K7KPipeline(object):

    def open_spider(self, spider):
        self.file = open('./g7k7k_%s.txt' % num, mode='a+', encoding='utf-8')

    def process_item(self, item, spider):
        self.file.write(json.dumps(dict(item), ensure_ascii=False) + '\n')
        return item

    def close_spider(self, spider):
        self.file.close()
