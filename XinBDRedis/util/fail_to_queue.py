"""把失败的公司名重新入队列"""
from util.db import get_redis_cli

if __name__ == '__main__':
    cli = get_redis_cli()
    i = 0
    while True:
        company_name = cli.spop("fail_queue")
        if not company_name:
            break
        else:
            company_name = company_name.decode("utf-8")
        cli.lpush("company_queue", company_name)
        print("insert %d ok" % i)
        i += 1


