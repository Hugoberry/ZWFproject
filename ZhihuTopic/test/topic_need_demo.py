import re
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome'
                  '/70.0.3538.67 Safari/537.36'
}
html = requests.get('https://www.zhihu.com/search?q=%E5%B0%8F%E7%B1%B3&type=topic', headers=headers).text

info = '<div class="List-item"><div class="ContentItem"><div class="ContentItem-main"><div class="' \
       'ContentItem-image"><a class="TopicLink" href="(.*?)" target="_blank">' \
       '<div class="Popover"><div id="null-toggle" aria-haspopup="true" aria-expanded="false" aria-owns=' \
       '"null-content"><img class="Avatar Avatar--large TopicLink-avatar" width="60" height="60" src="' \
       '(.*?)" srcSet="(.*?) 2x" alt="(.*?)/></div></div></a></div><div class="ContentItem-head">' \
       '<h2 class="ContentItem-title"><div><a class="TopicLink" href="(.*?)" target="_blank"><div ' \
       'class="Popover"><div id="null-toggle" aria-haspopup="true" aria-expanded="false"' \
       ' aria-owns="null-content"><span class="Highlight">(.*?)</span></div></div></a></div>' \
       '</h2><div class="ContentItem-meta"><div><div class="RichText ztext SearchItem-meta Highlight">' \
       '(.*?)</div><div class="ContentItem-status"><a class="ContentItem-statusItem Search-statusLink" ' \
       'target="_blank" href="(.*?)">(.*?) 关注</a><a class="ContentItem-statusItem' \
       ' Search-statusLink" target="_blank" href="(.*?)">(.*?) 问题</a><a class=' \
       '"ContentItem-statusItem Search-statusLink" target="_blank" href="(.*?)">' \
       '(.*?) 精华内容</a>'

all_need = re.compile(info).findall(html)
for need in all_need:
    print(need)
    print(len(need))
