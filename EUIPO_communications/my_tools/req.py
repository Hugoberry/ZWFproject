import requests

url = "https://euipo.europa.eu/copla/communications/menu/CTM/000000001"
cookies = {
    "TS0160d57f": "010dad8a7a53a16bb5e0d9f06ee9ae1a0619ba667182b5d5cc56f98142ecddaa430fee5bca0861b9f447b3be8e0b69d7013e36d215",
    "TSPD_101": "0831631732ab2800b9534728383ff6c0d700b9b52280fc5e4f26c2d3711f0ce566f616dddd869d3b3ab717408a77612d:",
    "TS01976a55": "010dad8a7a3eb853bb3d0a21a92eb824e05b2e27040327a03a859f27afade9b55a71d4cdfaccdb5cfc659fe532ec30302260b19bdc",
    "__utma": "106981910.1511186174.1558340210.1558340210.1558340210.1", "__utmc": "106981910",
    "__utmb": "106981910.1.10.1558340210",
    "__utmz": "106981910.1558340210.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)", "__utmt": "1"}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
}

res = requests.get(url=url, headers=headers, cookies=cookies)
print(res)
