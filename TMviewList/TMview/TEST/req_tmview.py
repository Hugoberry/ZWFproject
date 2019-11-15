import requests

# url = 'https://www.tmdn.org/tmview/search-tmv?_search=false&nd=1548657310485&rows=100&page=1&sidx=tm&sord=asc&q=tm%3Aapple&fq=%5B%5D&pageSize=100&facetQueryType=2&selectedRowRefNumber=null&providerList=null&expandedOffices=null'
url = 'https://www.tmdn.org/tmview/get-detail?st13=US500000072024748'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Referer': 'https://www.tmdn.org/tmview/welcome',
    'Cookie': 'JSESSIONID=72A82C548847BF9F8625CCE471F20205.tmdsview1; TS01cf9d9b=01601e1d32ffe1ddfc4bd1c0f9fde70c3fc88a0d60fa59898ca7b8e9b01e6f1dd72b819f2ccd9c1fc6774c072ead8b386dcd0d6b120b376c92837a9552d264a8d1d5fd8c12; font_size_cookie=12; actual_step=0; tmvSearchTermsHistory=tm%3Aapple; lastExecutedQuery=tm%3Aapple; TS0137cd0e=01601e1d32a6507ba450ed8b8146f0cb0650f3c8925d7a3c97d916bc0cc8de2e056d372d2c1cbf4566712e2802dcc2b0a4bf8bbf3e; TSPD_101=0827db1318ab28009407239c0f864d137129dc8dc472b75631dda0a19f06bc522b1a76e9a5df54ded7a526d751486063:; TS01e836b1=01601e1d3218696343572fd2d15256183e3f70e3b3fa59898ca7b8e9b01e6f1dd72b819f2cd188fb65adb6e220de7f04fffce165e4; TS01e836b1_28=01edc21ef0a64636d491933ad3b0adf62192db18bf0d96c45dd580f60f3a4168b03e70567be21400dcf1e0414541f83ef920bbeff4; cookieconsent_status=dismiss; TS0137cd0e_77=0827db1318ab280010f2b76c43323c811091805fc0a36c491d49f278d1ed16d074fca5d8091a2bf9c4842b3b6f729e7208d428b0be823800724c0910415201d14d6d2e2c95a14eb3968bdb30d9b137578b4cd7923eda1a11728489d89411595ca980bae61932aeb99778d017fc4cae09; _pk_ses.18.9586=*; _pk_id.18.9586=a640cdd1d8bb4829.1548657272.1.1548657287.1548657272.; TS01c9251e=01601e1d3250660e33f22e3ea0f82ce484cd729e4e44190c89696a96fd288faeabcb06ab75343be0df1864f592f8cfcbf82cfe3e3a; TS01e836b1_77=0827db1318ab2800d636e2a89823f722050f62e3a794a6f45b5344aa3bcb09b95297b580ab0422e6dc828d1707e27586081703f6d182380098468a22b28baa2a9d082888da13df818578a84605c439d7d28d56ff58d9d0ad86bfc11f8645e91b1bf4f7eddf3352e39f4a9c0ce796b908'
}

req = requests.get(url, headers=headers)
pass
