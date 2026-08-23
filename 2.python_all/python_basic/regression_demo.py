import re

res = re.match(r'^[1-9]\w{6}$', '1xiefei')
print(res)
print(res.group())  # 获取匹配的字符串