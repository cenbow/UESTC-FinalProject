# -*- coding: utf-8 -*-
import requests
from time import sleep
import datetime as dt
from random import uniform, random
import logging
import argparse
import q, os, sys
from cookieparse import cookiesParse

from urllib.parse import urlencode

HOME_URL = 'http://www.qichacha.com/'
QUERY_URL = 'http://www.qichacha.com/search'

headers = {
    # 'connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:59.0) Gecko/20100101 Firefox/59.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

# preparing for cookie

# response = requests.get(HOME_URL, headers=headers)

# cookies = response.cookies
cookies = cookiesParse("cookies.txt")

# r = requests.get(QUERY_URL + '?' + "key=ofo", cookies=cookies, headers=headers)

# print('status code: {}'.format(r.status_code))
# print('content:{}'.format(r.content.decode('utf-8')))


parse = argparse.ArgumentParser(
    description="Query company information from QICHACHA")
parse.add_argument('filename')
parse.add_argument('-o', '--output-dir',
                   help="destination directory", default='output')
parse.add_argument('-l', '--logger', help='log file name',
                   default='scrawl.log')

args = parse.parse_args()

if not os.path.exists(args.output_dir):
    os.mkdir(args.output_dir)

logging.basicConfig(filename=args.logger, level=logging.WARNING)
logging.debug('This message should go to the log file')
logging.info('So should this')
logging.warning('And this, too')

totalcnt = 0
with open(args.filename, 'r', encoding='utf-8') as temp:
    totalcnt = len(temp.readlines())


idle_cnt = 0
newItemCnt = 0
with open(args.filename, 'r', encoding='utf-8') as name_list:
    processor = 0
    for name in reversed(name_list.readlines()):
        processor += 1

        if '/' in name:
            continue

        # processor bar
        percentage = processor / totalcnt
        processorbar = "|{}{}|".format(
            '█' * int(80 * percentage), ' ' * (80 - int(80 * percentage)))
        sys.stdout.write('\r{:3d}% {}:{}'.format(
            int(percentage * 100), processorbar, name))
        sys.stdout.flush()

        name = name.strip()
        offset_time = 10
        output_file = args.output_dir + '/' + name + '.html'
        if os.path.exists(output_file):
            continue
        suffix = urlencode({'key': name})
        try:
            response = requests.get(
                QUERY_URL + '?' + suffix, cookies=cookies, headers=headers)
            content = response.content.decode('utf-8')
            q(content[:80])

            if 'index_verify' in content or '504 Gateway Time-out' in content:
                logging.warning("{}: Scrawller found by server".format(
                    dt.datetime.now().time()))
                sleep(offset_time)
                offset_time *= 2
                continue
            else:
                offset_time = 10

            with open(args.output_dir + '/' + name + '.html', 'w', encoding='utf-8') as htmlfile:
                htmlfile.write(content)
                newItemCnt += 1

        except requests.HTTPError as e:
            logging.error(
                "Error {} found when scrawl {}".format(e.errno, name))
        except FileNotFoundError:
            logging.error("Can't create file :  {}".format(name))
        except:
            with open('log.txt', 'a') as log:
                log.write("END with {name} at {time}\n".format(name=name, time=dt.datetime.now().time()))
                log.write("GET {} items totally".format(newItemCnt))
        finally:
            sleep(uniform(20, 30))
            idle_cnt += 1
            if idle_cnt > 100:
                idle_cnt = 0
                sleep(60 * 15)
