# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class Search360Pipeline(object):

    def open_spider(self, spider):
        self.file = open('./search_info.txt', 'w+', encoding='utf-8')

    def process_item(self, item, spider):
        print(item['news_nums'])
        self.file.write(item['kw'] + 'ÿ' + item['news_nums'] + '\n')
        self.file.flush()
        return item

    def close_spider(self, spider):
        self.file.close()
