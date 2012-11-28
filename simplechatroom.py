from gevent import monkey
from gevent.event import Event
from gevent.wsgi import WSGIServer

from flask import Flask, jsonify, request, Response

import json

monkey.patch_socket()


app = Flask(__name__)
app.config.from_object(__name__)


class ChatRoom(object):

    def __init__(self):
        self.msg = []
        self.event = Event()

    def new_message(self, message):
        self.msg.append(message)
        self.event.set()
        self.event.clear()

    def wait(self):
        self.event.wait()

    def get_messages(self):
        return self.msg

room = ChatRoom()


@app.route("/")
def index():
    return "hello world"


@app.route("/new_message/", methods=("POST", ))
def new_message():
    resp = Response()
    # set the request header field 'Content-Type' to be
    # 'text/plain' or 'application/json'
    # accept json
    if hasattr(request, "data"):
        new_msg = json.loads(request.data)['message']
        room.new_message(new_msg)
        resp.status_code = 200
    else:
        resp.status_code = 400

    return resp


@app.route("/update/", methods=("GET",))
def update_message():
    room.wait()
    return jsonify(messages=room.get_messages())


if __name__ == '__main__':
    WSGIServer(("localhost", 8080), app.wsgi_app).serve_forever()
