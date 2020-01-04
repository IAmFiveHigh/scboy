"""
  created by IAmFiveHigh on 2020-01-02
 """
from sqlalchemy import Column, DateTime, Integer, String, SmallInteger, ForeignKey
from flask_sqlalchemy import SQLAlchemy as sq, BaseQuery
from contextlib import contextmanager
from datetime import datetime
from sqlalchemy.orm import relationship


class SQLAlchemy(sq):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e


class Query(BaseQuery):
    def filter_by(self, **kwargs):
        if 'status' not in kwargs.keys():
            kwargs['status'] = 1
        return super(Query, self).filter_by(**kwargs)


db = SQLAlchemy(query_class=Query)


class Base(db.Model):
    __abstract__ = True
    create_time = Column('create_time', DateTime)
    status = Column(SmallInteger, default=1)

    def __init__(self):
        self.create_time = datetime.now()


class Test(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    age = Column(Integer)
    name = Column(String(20))


class Topic(Base):
    id = Column(Integer, primary_key=True)
    title = Column(String(200), default='')
    tag = Column(String(20))
    content = Column(String(1000))
    author = relationship('Author')
    aid = Column(Integer, ForeignKey('author.id'), nullable=False)
    author_time = Column(DateTime)
    eye_nums = Column(Integer, default=0)
    comment_nums = Column(Integer, default=0)
    thumbs_up_nums = Column(Integer, default=0)
    collect_nums = Column(Integer, default=0)


class Author(Base):
    id = Column(Integer, primary_key=True)
    image = Column(String(50), default='')
    first_login_time = Column(DateTime)
    last_login_time = Column(DateTime)


class Comment(Base):
    id = Column(Integer, primary_key=True)
    author = relationship('Author')
    aid = Column(Integer, ForeignKey('author.id'), nullable=False)
    content = Column(String(1000))
    comment_time = Column(DateTime, nullable=False)
    thumbs_up_nums = Column(Integer, default=0)
    reply_comment = relationship('Comment')
    reply_comment_id = Column(Integer, ForeignKey('comment.id'), nullable=True)
