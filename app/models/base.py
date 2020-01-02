"""
  created by IAmFiveHigh on 2020-01-02
 """
from sqlalchemy import Column, DateTime, Integer, String, SmallInteger
from flask_sqlalchemy import SQLAlchemy as sq, BaseQuery
from contextlib import contextmanager
from datetime import datetime



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


class TL(db.Model):
    age = Column(Integer)
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20))
