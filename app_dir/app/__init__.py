"""
  created by IAmFiveHigh on 2020-01-02
 """

from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.secure')
    app.config.from_object('app.setting')

    register_blueprint(app)
    return app


def register_blueprint(app):
    from app_dir.app.web import web
    app.register_blueprint(web)