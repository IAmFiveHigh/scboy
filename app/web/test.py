"""
  created by IAmFiveHigh on 2020-01-02
 """

import re
from queue import Queue
from datetime import datetime
from threading import Thread

import requests
from scrapy import Selector
from . import web
from app.models.base import Topic, db
import pymysql

topic_list = Queue()
topic_detail_prefix_url = 'https://www.scboy.com/?thread-'
url_test = 'https://www.scboy.com/?forum-1-1.htm&orderby=last_date&digest=0'
detail_url_list = Queue()


def get_main():
    res_text = requests.get(url_test).text
    sel = Selector(text=res_text)
    li_list = sel.css('.list-unstyled>li')
    for li in li_list:
        topic_list.put(li)



@web.route('/test')
def test():
    # test11 = Test.query.filter_by(id=2).all()

    return "<h1>test</h1>"


@web.route('/spider')
def spider():
    get_main()

    t1 = Thread(target=parse_topic)
    t1.start()
    t2 = Thread(target=parse_topic_detail)
    t2.start()
    while 1:
        pass
    return '正在spider'


def parse_topic():
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
            detail_url_list.put(detail_url)

            if data_tid is None:
                return

            # app = current_app._get_current_object().app_context()
            # app.push()
            # with db.auto_commit():
            #     topic = Topic()
            #     topic.id = int(data_tid)
            #     # topic.aid = int(aid)
            #     topic.title = title
            #     topic.tag = tag
            #
            #     db.session.add(topic)
            # app.pop()

            # 无法用sqlalchemy操作 因为多线程里获取不到currentapp 所以只能用sql语句操作
            sql_str = f"INSERT INTO topic (id, title, tag) VALUES ({data_tid}, '{title}', '{tag}')"
            print(sql_str)
            conn = pymysql.connect(
                host='localhost',
            user = 'root', password = '123456789',
            database = 'scboy')
            cursor = conn.cursor()
            cursor.execute(sql_str)
            conn.commit()
            cursor.close()
            conn.close()


def parse_topic_detail():
    while 1:
        if not detail_url_list.empty():

            url = detail_url_list.get()
            # 获取data_tid
            data_tid = re.match('.*thread-(\d*).htm', url).group(1)

            # 根据url获取页面
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

            # with db.auto_commit():
            #     topic = Topic.query.filter_by(id=data_tid).first()
            #     topic.author_time = transform_date(public_date)
            #     topic.eye_nums = eye_nums
            #     topic.thumbs_up_nums = thumbs_up_nums
            #     topic.collect_nums = collect_nums
            #     topic.content = content


def transform_date(date: str):
    return datetime.strptime(date, '%Y-%m-d %H:%m')