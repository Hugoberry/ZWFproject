# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ZhihutopicPipeline(object):

    def open_spider(self, spider):
        self.file = open('./info.txt', 'w+', encoding='utf-8')

    def process_item(self, item, spider):
        aim = dict(item)
        self.file.write(aim['kw'] + 'ÿ' + aim['title'] + 'ÿ' + aim['description'] + 'ÿ' + str(aim['id_no']) + 'ÿ'
                        + str(aim['followers_count']) + 'ÿ' + str(aim['questions_count']) + 'ÿ'
                        + str(aim['top_answer_count']) + 'ÿ' + aim['avatar_url'] + 'ÿ' + aim['topic_url'] + '\n')
        self.file.flush()
        return item

    def close_spider(self, spider):
        self.file.close()
