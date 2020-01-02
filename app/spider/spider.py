# create date: 2020/1/2 17:41
# author: IAmFiveHigh

import re

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

    author_id = li.css('div>a>img::attr(uid)').extract_first()

    title = li.css('div:nth-child(2)>div>a>span::text').extract_first()
    if title == None:
        title = li.css('div:nth-child(2)>div>a::text').extract_first()

    tag = li.css('div:nth-child(2)>div>a.badge-pill::text').extract_first()

    author_time_original = li.css('div:nth-child(2)>div:nth-child(2)>div>span.date::text').extract_first()

    # print(f'topic_id: {data_tid}, image_src: {image}, author_id: {author_id}, title: {title}, tag: {tag} ')
    print(author_time_original)


def operator(time_text:str):


get_main()