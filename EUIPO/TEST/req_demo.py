import requests

url = 'https://euipo.europa.eu/copla/ctmsearch/json'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3610.2 Safari/537.36',
}

cookie = {
    'JSESSIONID': '430F9B43C55D07655F1C5A1E36922158.copla3',
    'TS0159664b': '010dad8a7aad5b474bc0a8b716a1e5d684f4b48f2b9f42c98f2d0aa7b3211cee3dd56255f4a484412ef4b172c85eccc64bd6a85a3b03c062f6ef32680f7c6277e1a3741dead715dd1f7baa3ef3276a03d5734487e3',
    'TSPD_101': '0831631732ab2800d0366556974779fe928745592a65d4983b521da10a09be07c56a54ea93223ad0638c83e6f14caf43:',
    'TS0160d57f': '010dad8a7a09cf51323da27141edb0e4f4f20693095e85456cbb8ede63886d8b8d7bf0f5c9997664b4e844aa84e2f938c10046d72491c8ac05e73327e281671ecce25cc9db',
    '__utma': '106981910.1726864177.1545636763.1545636763.1545636763.1',
    '__utmc': '106981910',
    '__utmz': '106981910.1545636763.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
    '__utmb': '106981910.2.10.1545636763',
    '_pk_id.26.18ee': '179329495b1ec6d2.1545636763.1.1545636763.1545636763.',
    ' _pk_ses.26.18ee': '*',
    'TS01976a55': '010dad8a7a64b022dd34b88673ad94ab2591ca9fbd9f42c98f2d0aa7b3211cee3dd56255f496719ffd490455e35e17c1af9a30bbcf55156b01753f17a97c539f61225fd152',
    'GUEST_LANGUAGE_ID': 'en_GB',
    'COOKIE_SUPPORT': 'true',
    'TS01b54a83': '010dad8a7a0fedad2e2dfeb1de20519ad3d4094ba780182c439011e8ad3ba4240bd591804321e294604da0a906c6b374ec90d674827f2654634c836ca48d954598c977aa53830b444a037ea4b8abdd5aaa1ad7dec9ee5e44ccb1209e19a986ed27705a25a0'
}

data = {
    'start': '0',
    'rows': '100',
    'searchMode': 'basic',
    'criterion_1': 'ApplicationNumber',
    'term_1': 'apple',
    'operator_1': 'OR',
    'condition_1': 'CONTAINS',
    'criterion_2': 'MarkVerbalElementText',
    'term_2': 'apple',
    'operator_2': 'OR',
    'condition_2': 'CONTAINS',
    'criterion_3': 'OppositionIdentifier',
    'term_3': 'apple',
    'operator_3': 'OR',
    'condition_3': 'CONTAINS',
    'sortField': 'ApplicationNumber',
    'sortOrder': 'asc',
}

text = requests.post(url=url, headers=headers, json=data, cookies=cookie, ).text
print(text)
