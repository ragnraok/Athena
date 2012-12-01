import json

from flask import Blueprint
from flask import jsonify, request, Response

from Athena.chatroom.models import ChatRoom, ChatRoomRecord
from Athena.basicauth.auth import require_auth


app = Blueprint("chatroom", __name__)

#TODO
# create a chat room
# join a chat room
# send message in a room
# broadcast a message when someone join a chat room
# exit a chatroom
# a long polling update message interface


@app.route("/create_room/", methods=("POST", ))
@require_auth
def create_room():
    pass


@app.route("/join_room/<int:room_id>", methods=("POST", ))
@require_auth
def join_room(room_id):
    pass


@app.route("/send_message/<int:room_id>", methods=("POST", ))
@require_auth
def send_message(room_id):
    pass


@app.route("/exit_room/<int:room_id>", methods=("POST", ))
@require_auth
def exit_room(room_id):
    pass


@app.route("/update_message/<int:room_id>", methods=("POST", ))
@require_auth
def update_message(room_id):
    pass
