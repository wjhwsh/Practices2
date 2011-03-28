import re

file = open('/Users/kordan/Practices/python/re_test.txt', 'r')
content = file.read()

# href="/dictionary?hl=zh-TW&sl=en&tl=zh-TW&q= WORD"
m = re.findall(r'href=[\'""]?([^\'" >"]+)', content)

print m
