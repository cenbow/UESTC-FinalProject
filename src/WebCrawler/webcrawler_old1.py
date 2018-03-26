import sys, os
from urllib import request, parse, error
from http import cookiejar
from keepalive import keepalive


HOME_URL = 'http://www.qichacha.com/'
QUERY_URL = 'http://www.qichacha.com/search'

headers = {
    'connection': 'keep-alive',
    'upgrade-insecure-requests': 1,
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3355.4 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate',
    'accept-language': 'zh-CN,zh;q=0.9',
}


def query(keyword):
    kaHandler = keepalive.HTTPHandler()

    # cookie = cookiejar.MozillaCookieJar()
    # if os.path.exists('cookies.txt'):
    #     cookie.load('cookies.txt')
    # else:
    cookie = cookiejar.MozillaCookieJar('cookies.txt')

    cjHandler = request.HTTPCookieProcessor(cookie)
    opener = request.build_opener(kaHandler, cjHandler)
    # opener_with_cookie.addheaders = [('User-Agent', user_agent)]
    request.install_opener(opener)
    # request.urlopen(HOME_URL)
    first_req = request.Request(HOME_URL, headers=headers)
    response = request.urlopen(first_req)
    tcookie = response.info()['Set-Cookie']
    print(tcookie)
    cookie.save(ignore_discard=True, ignore_expires=True)

    data = {'key': 'ofo'}
    url_with_paras = QUERY_URL + '?' + parse.urlencode(data)
    print('+++++++++++' + url_with_paras + '+++++++++++')
    req = request.Request(url_with_paras, headers=headers)
    # req.remove_header('Cookie')
    req.add_header('Referer', HOME_URL)
    # req.add_header('Cookie', tcookie)
    try:
        response = request.urlopen(req)
        html = response.read()
        with open('temp.html', 'w') as f:
            f.write(html)
    except error.HTTPError as e:
        print(e.code)


if __name__ == "__main__":
    query('ofo')
