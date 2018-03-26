import sys

raw_cookie = input("please type cookies:")

items = raw_cookie.split(';')
d = {}
for item in items:
    item = item.strip()
    if item:
        key_, _, val = item.partition('=')
        d[key_] = val

print(repr(d))
