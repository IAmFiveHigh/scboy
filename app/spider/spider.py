# create date: 2020/1/2 17:41
# author: IAmFiveHigh

import re
from datetime import datetime, timedelta

import requests
from scrapy import Selector


url_test = 'https://www.scboy.com/?forum-1-1.htm&orderby=last_date&digest=0'


def get_main():
    res_text = requests.get(url_test).text
    sel = Selector(text=res_text)
    # 去掉了头部 top_1 top_3的特殊帖子 弃用
    # li_list = sel.css('.list-unstyled>li:not(.top_1)')[1:]
    li_list = sel.css('.list-unstyled>li')
    for li in li_list:
        parse_topic(li)


def parse_topic(li: Selector):
    data_tid = li.css('::attr(data-tid)').extract_first()

    image = li.css('div>a>img::attr(src)').extract_first()
    if not image.startswith('http'):
       image = 'https://www.scboy.com/' + image

    aid = li.css('div>a>img::attr(uid)').extract_first()

    title = li.css('div:nth-child(2)>div>a>span::text').extract_first()
    if title is None:
        title = li.css('div:nth-child(2)>div>a::text').extract_first()

    tag = li.css('div:nth-child(2)>div>a.badge-pill::text').extract_first()


def operator(time_text:str):
    if time_text is None:
        return None

    r = re.match('(\d+)([\u4e00-\u9fa5]*)前', time_text)

    number = r.group(1)
    unit = r.group(2)
    now = datetime.now()
    if unit == '年':
        create_time = now - timedelta(days=float(365 * number))
    elif unit == '月':
        create_time = now - timedelta(weeks=float(4 * number))
    elif unit == '天':
        create_time = now - timedelta(days=float(number))
    elif unit == '小时':
        create_time = now - timedelta(hours=float(number))
    elif unit == '分钟':
        create_time = now - timedelta(minutes=float(number))
    else:
        create_time = now

    return create_time


get_main()
