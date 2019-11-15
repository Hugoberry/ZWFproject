import happybase


async def get_hbase(page):
    connect = happybase.Connection("40.73.36.79", 9090)
    student_table = connect.table('zhihuLiveData')
    page = int(page)
    scanner = student_table.scan(limit=100, batch_size=10, row_start="%d" % (page * 100), row_stop="%d" % ((page + 1) * 100))
    kvd = dict()
    for k, v in scanner:
        kvd1 = dict()
        for k1, v1 in v.items():
            kvd1[str(k1, encoding="utf-8")] = str(v1, encoding="utf-8").replace(
                '<div class="ztext SearchItem-description Highlight">', "").replace('</div>', '').replace(
                '<span class="Highlight">', '').replace('</span>', '')
        kvd[str(k, encoding="utf-8")] = kvd1
    return kvd
