"""
  created by IAmFiveHigh on 2020-01-02
 """

from flask import Blueprint


web = Blueprint('web', __name__)


from app.web import test