# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class SearchPipeline(object):

    def open_spider(self, spider):
        self.file = open('./search_nums.txt', 'a+', encoding='utf-8')

    def process_item(self, item, spider):
        self.file.write(item['kw'] + 'ÿ' + item['search_nums'] + '\n')
        self.file.flush()
        return item

    def close_spider(self, spider):
        self.file.close()
