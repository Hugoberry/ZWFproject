import xlrd
from util.db import get_redis_cli
import re

redis_cli = get_redis_cli()


def csv_to_db():
    """从excel文件中获取商标名、商标申请号存放到 redis 数据库中"""

    # filename = "商标交易数据列表.xlsx"
    filename = "企业名称.xlsx"
    workbook = xlrd.open_workbook(filename)
    booksheet = workbook.sheet_by_index(0)
    # 获取商品名称列表
    name_list = booksheet.col_values(0, 1)
    # 获取申请号列表
    # reg_no_list = booksheet.col_values(1, 1)
    # 统计编号数量
    dupefilter = set()
    for index, name in enumerate(name_list):
        if name not in dupefilter:
            dupefilter.add(name)
            # redis_cli.rpush("keyword_queue", name)
            redis_cli.rpush("company_queue", name)
        print("当前是第 {} 次存取".format(index + 1))
    print("共有 {} 个唯一值".format(len(dupefilter)))


def txt_to_db(file_name, redis_key):
    """从文本文件中获取数据"""
    pattern = re.compile(r"\((.*?),1\)$")
    with open(file_name, "r", encoding="gb2312", errors="ignore") as f:
        results = f.readlines()
        for i in results:
            name = pattern.match(i).group(1)
            redis_cli.lpush(redis_key, name)
    print("save ok!")


if __name__ == '__main__':
    # txt_to_db(file_name=r"C:\Users\EDZ\Desktop\code\西瓜数据\shangbiao.txt", redis_key="tm_name")
    csv_to_db()
