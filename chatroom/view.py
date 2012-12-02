import json

from flask import Blueprint
from flask import jsonify, request, Response
from flask import g

from Athena.chatroom.models import ChatRoom, ChatRoomRecord
from Athena.chatroom.room_suck import room_manager
from Athena.basicauth.auth import require_auth
from Athena.util import get_json_post_data, no_post_data, room_not_exist_by_id, room_not_exist_by_name
from Athena.database import db


app = Blueprint("chatroom", __name__)

#TODO
# create a chat room
# join a chat room
# send message in a room
# broadcast a message when someone join a chat room
# exit a chatroom
# a long polling update message interface
# get room's online users number
# get room's online users list
# get room's info


@app.route("/create_room/", methods=("POST", ))
@require_auth
def create_room():
    """
    Create Room function
        POST json format:
            {"room_name": room_name}
        Response json format:
            {"room_name": room_name, "room_id": room_id}
        If the room for name is already exist, return 406
    """
    creator = g.user
    info = get_json_post_data()
    if info is None:
        return no_post_data
    name = info.get('room_name', None)
    if name is None:
        return Response(status=406)
    room_list = ChatRoom.query.filter_by(title=name).all()
    if len(room_list) > 0:
        return Response("room %s was existed" % name, 406)
    # create the room
    room = ChatRoom(name, creator.id)
    db.session.add(room)
    db.session.commit()

    # and let creator join this room
    room_manager.join_room(room.id, creator.id)
    return jsonify(room_name=room.title, room_id=room.id)


@app.route("/join_room/<int:room_id>", methods=("POST", ))
@require_auth
def join_room(room_id):
    """
    Join room function:
        POST:
            no data
        Response 200 if success
        If the room is not exist, return 400
    """
    join_user = g.user
    room = ChatRoom.query.get(room_id)
    if room is None:
        return room_not_exist_by_id(room_id)
    room_manager.join_room(room_id, join_user.id)

    # broadcast a message to all user
    room_manager.send_message(room_id, "%s join room!" % join_user.username)
    return Response("successful join room %s" % room.title, 200)


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


@app.route("/get_room_user_num/<int:room_id>", methods=("GET", ))
@require_auth
def get_room_user_num(room_id):
    pass


@app.route("/get_room_users/<int:room_id>", methods=("GET", ))
@require_auth
def get_room_users(room_id):
    pass


@app.route("/get_room_info/<int:room_id>", methods=("GET", ))
@require_auth
def get_room_info(room_id):
    pass
