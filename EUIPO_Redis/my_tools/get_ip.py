import requests

text = requests.get('http://39.107.59.59/get').text.replace('\\', '').split('["')[1].split('"]')[0]
print(text)
ip_ls = text.split('",')
ips = []
for ip in ip_ls:
    ip_dict = eval(ip.replace('"{', '{'))
    ips.append((ip_dict['ip'], str(ip_dict['port'])))
pass
