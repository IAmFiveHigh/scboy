"""
  created by IAmFiveHigh on 2020-01-02
 """

from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.secure')
    app.config.from_object('app.setting')
    return app