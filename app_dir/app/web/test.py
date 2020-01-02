"""
  created by IAmFiveHigh on 2020-01-02
 """

from . import web


@web.route('/test')
def test():
    return "<h1>test</h1>"
