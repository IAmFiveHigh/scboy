# create date: 2020/1/2 17:41
# author: IAmFiveHigh

import re
from datetime import datetime, timedelta
from queue import Queue
from threading import Thread

import requests
from scrapy import Selector
from flask import current_app

from app.models.base import Topic, db

url_test = 'https://www.scboy.com/?forum-1-1.htm&orderby=last_date&digest=0'
topic_detail_prefix_url = 'https://www.scboy.com/?thread-'

topic_list = Queue()


def get_main():


    res_text = requests.get(url_test).text
    sel = Selector(text=res_text)
    li_list = sel.css('.list-unstyled>li')
    # for li in li_list:
    #     topic_list.put(li)

    for i in range(2):
        topic_list.put(li_list[i])
    topic_thread = Parse_topic()
    topic_thread.start()


class Parse_topic(Thread):

    def run(self):
        while 1:
            if not topic_list.empty():
                li = topic_list.get()
                data_tid = li.css('::attr(data-tid)').extract_first()

                aid = li.css('div>a>img::attr(uid)').extract_first()

                title_a = li.css('div.media-body>div.subject>a.xs-thread-a')
                if title_a.css('span').extract_first() is None:
                    title = title_a.css('::text').extract_first()
                else:
                    title = title_a.css('span::text').extract_first()

                tag = li.css('div:nth-child(2)>div>a.badge-pill::text').extract_first()

                detail_url = topic_detail_prefix_url + data_tid + '.htm'

                if data_tid is None:
                    return
                with current_app.app_context:
                    print(current_app.__name__)
                    with db.auto_commit():
                        topic = Topic()
                        topic.id = int(data_tid)
                        # topic.aid = int(aid)
                        topic.title = title
                        topic.tag = tag

                        db.session.add(topic)


def parse_topic_detail(url, data_tid):
    res_test = requests.get(url).text
    sel = Selector(text=res_test)

    # 发布时间
    public_date = sel.css('.card-thread>.card-body>.media>.media-body>div>div>.date::text').extract_first()

    # 浏览数
    eye_nums = sel.css('.card-thread>.card-body>.media>.media-body>div>div>span:nth-child(3)::text').extract_first()

    # 点赞量
    thumbs_up_nums = sel.css('.haya-post-like-thread-user-count::text').extract_first()

    # 收藏量
    collect_nums = sel.css('.js-haya-favorite-show-users>span::text').extract_first()

    # 内容
    content = sel.css('.card-thread>.card-body>.message>p::text').extract_first()

    with db.auto_commit():
        topic = Topic.query.filter_by(id=data_tid).first()
        topic.author_time = transform_date(public_date)
        topic.eye_nums = eye_nums
        topic.thumbs_up_nums = thumbs_up_nums
        topic.collect_nums = collect_nums
        topic.content = content


# def operator(time_text:str):
#     r = re.match('(\d+)([\u4e00-\u9fa5]*)前', time_text)
#
#     number = r.group(1)
#     unit = r.group(2)
#     now = datetime.now()
#     if unit == '年':
#         create_time = now - timedelta(days=float(365 * number))
#     elif unit == '月':
#         create_time = now - timedelta(weeks=float(4 * number))
#     elif unit == '天':
#         create_time = now - timedelta(days=float(number))
#     elif unit == '小时':
#         create_time = now - timedelta(hours=float(number))
#     elif unit == '分钟':
#         create_time = now - timedelta(minutes=float(number))
#     else:
#         create_time = now
#
#     return create_time


def transform_date(date: str):
    return datetime.strptime(date, '%Y-%m-d %H:%m')


if __name__ == '__main__':
    get_main()

    topic_thread = Parse_topic()
    topic_thread.start()


