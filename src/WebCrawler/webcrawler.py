import requests
import re
import webbrowser
from time import sleep
import os, sys, q
import cookieparse
import json
import random
import logging
from progressbar import ProgressBar
from datetime import datetime

headers = {
    # 'connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:59.0) Gecko/20100101 Firefox/59.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

invalid_chars = ('<', '>', ':', '\"', '/', '\\', '|', '?', '*')

# q(invalid_chars)
processed = 0
increment = 0
total = 1000


def main():
    global total, increment, processed

    with open(sys.argv[1], 'r', encoding='utf-8') as jsonconfig:
        config = json.load(jsonconfig)
        # q(config)

    cookies = cookieparse.parse(config['cookies'])
    # q(cookies)
    total = config.get('total', 1000)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(config['logger'], mode='a', encoding='utf-8')
    fh.setFormatter(logging.Formatter(
        "%(asctime)s: %(levelname)s %(message)s", datefmt='%Y-%m-%d %H:%M:%S'))
    logger.addHandler(fh)

    ne, _, de = config.get('pattern', '1/1').partition('/')
    ne, de = int(ne), int(de)
    total /= de
    errorCnt = 0

    logger.debug("You should see this message")

    with open(config['list'], 'r', encoding='utf-8') as l:
        for idx, name in enumerate(ProgressBar(l.readlines())):
            if idx % de != ne - 1:
                continue

            name = name.strip()

            processed += 1
            url = config['url'] % name
            output_file = '/'.join((config['output_dir'], name + '.html'))
            # q(output_file)
            if os.path.exists(output_file):
                continue

            if idx % 50 == 0:
                sleep(60 * 10)

            if any(a in name for a in invalid_chars):
                logger.error("Invalid name to create file: %s" % name)
                continue

            sleep(abs(random.normalvariate(config['period'], 5)))
            for i in range(13):
                try:
                    response = requests.get(
                        url, cookies=cookies, headers=headers)
                except requests.HTTPError as e:
                    logger.error("Connection Error: %s when query %s" %
                                 (e.code, name))
                    exit(-1)

                content = response.content.decode('utf-8')

                if '<!DOCTYPE html> <html lang="en"> <head> <meta charset="utf-8">' in content:
                    with open(output_file, 'w', encoding='utf-8') as output:
                        output.write(content)
                        increment += 1
                    break
                else:
                    match = re.search(r"location.href='([^']*)'", content)
                    if match:
                        webbrowser.open(match.group(1))
                        errorCnt += 1
                        logger.debug("{}".format(idx / errorCnt))
                    else:
                        logger.debug(content[:80])
                    sleep(10 * (2 ** i))


try:
    main()
finally:
    # q(total)
    print('\n\n{::^62}'.format('scrawl.py'))
    print('|{:^60}|'.format(datetime.now().strftime('%y-%M-%d %H:%m')))
    print('|{:^60}|'.format('total items: %s' % total))
    print('|{:^60}|'.format('processed items: %s' % processed))
    print('{::^62}'.format(''))
