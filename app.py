from flask import Flask
from gevent.wsgi import WSGIServer

from Athena.database import db

app = Flask(__name__)
app.config.from_pyfile("config.py")


def register(blueprint):
    _view = __import__('Athena.%s' % blueprint, None, None, ['view'], 0)
    view = getattr(_view, 'view', '')
    app.register_blueprint(view.app, url_prefix="/%s" % blueprint)


def prepare_run():
    app.config.from_pyfile('config.py')
    register('user')

db.init_app(app)
db.app = app

if __name__ == '__main__':
    print 'Serving at http://127.0.0.1:8080/'
    prepare_run()
    WSGIServer(("localhost", 8000), app.wsgi_app).serve_forever()
    #app.run()
