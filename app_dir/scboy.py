"""
  created by IAmFiveHigh on 2020-01-02
 """
from app_dir.app import create_app


app = create_app()


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=app.config['DEBUG'], threaded=True)

