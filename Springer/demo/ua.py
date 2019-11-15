from fake_useragent import FakeUserAgent

a = FakeUserAgent()
for x in range(100):
    b = a.random
    if ('And' or 'phone') in b:
        print(b)
    else:
        pass

pass
