"""
  created by IAmFiveHigh on 2020-01-02
 """

from flask import Flask
from app.models.base import db


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.secure')
    app.config.from_object('app.setting')

    db.init_app(app)
    db.create_all(app=app)

    register_blueprint(app)
    return app


def register_blueprint(app):
    from app.web import web
    app.register_blueprint(web)