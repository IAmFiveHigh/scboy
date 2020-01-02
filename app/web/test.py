"""
  created by IAmFiveHigh on 2020-01-02
 """

from . import web
from app.models.topic import Test
from app.models.base import db


@web.route('/test')
def test():
    test11 = Test.query.filter_by(id=2).all()

    return "<h1>test</h1>"
