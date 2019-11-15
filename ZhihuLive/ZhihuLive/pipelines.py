# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ZhihulivePipeline(object):

    def open_spider(self, spider):
        self.file = open('./info.txt', 'w+', encoding='utf-8')

    def process_item(self, item, spider):
        aim = dict(item)
        zh_id = str(aim['zh_id'])
        content = aim['kw'] + 'ÿ' + aim['title'] + 'ÿ' + aim['target_url'] + 'ÿ' + aim['speakers_name'] + 'ÿ'\
                  + str(aim['taken']) + 'ÿ' + str(aim['estimation']) + 'ÿ' + zh_id + 'ÿ' + aim['description'] + '\n'
        self.file.write(content)
        self.file.flush()
        return item

    def close_spider(self, spider):
        self.file.close()
