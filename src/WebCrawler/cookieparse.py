import sys, os, q
def __init__(self):
    pass
def parse(s):
    res = {}
    s.strip()
    cookies = s.split(':')
    cookies = [cookie.strip() for cookie in cookies if cookie.strip()]
    for cookie in cookies:
        key, _, val = cookie.partition('=')
        res[key.strip()] = val.strip()
    return res

def cookiesParse(fn):
    with open(fn, mode='r') as fn:
        return parse(fn.read())
