import json

from flask import Blueprint
from flask import jsonify, request, Response
from flask import g
from sqlalchemy.sql.expression import desc

from Athena.chatroom.models import ChatRoom, ChatRoomRecord
from Athena.chatroom.room_suck import room_manager
from Athena.basicauth.auth import require_auth
from Athena.util import get_json_post_data, no_post_data,\
room_not_exist_by_id, login_first, not_in_room_by_id, add_keep_alive
from Athena.database import db
from Athena.user.online_cache import online_users
from Athena.user.models import User


app = Blueprint("chatroom", __name__)

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


@app.route("/join_room/<int:room_id>/", methods=("POST",))
@require_auth
def join_room(room_id):
    """
    Join room function:
        POST:
            no data
        Response 200 if success
        If the room is not exist, return 400
        If the user is not online now, return 406
    """
    join_user = g.user
    if not online_users.is_online(join_user):
        return login_first()
    room = ChatRoom.query.get(room_id)
    if room is None:
        return room_not_exist_by_id(room_id)
    room_manager.join_room(room_id, join_user.id)
    # broadcast a message to all user
    room_manager.send_message(join_user.id, room_id, "%s join room!" % join_user.username)
    return Response("successful join room %s" % room.title, 200)


@app.route("/send_message/<int:room_id>/", methods=("POST", ))
@require_auth
def send_message(room_id):
    """
    Send message function
        POST json format:
            {"message": message}
        Response 200 if success
        if the room is not exist, return 400
        if the is not online now, return 406
        if the user is not in this room, return 406
    """
    sender = g.user
    print "sender is %s" % sender
    if not online_users.is_online(sender):
        return login_first()
    room = ChatRoom.query.get(room_id)
    if room is None:
        return room_not_exist_by_id(room_id)
    if not room_manager.is_in_room(room_id, sender.id):
        return not_in_room_by_id(room_id)
    info = get_json_post_data()
    msg = info.get('message', None)
    if msg is None:
        return Response(status=406)
    room_manager.send_message(sender.id, room_id, msg)
    return Response("successful send message to room %s" % room.title, 200)


@app.route("/exit_room/<int:room_id>/", methods=("POST", ))
@require_auth
def exit_room(room_id):
    """
    Exit room function
        POST:
            no data
        Response 200 if success
        if the room is not exist, return 400
        if the user is not online now, return 406
        if the user is not in this room, return 406
    """
    exit_user = g.user
    if not online_users.is_online(exit_user):
        return login_first()
    room = ChatRoom.query.get(room_id)
    if room is None:
        return room_not_exist_by_id(room_id)
    if not room_manager.is_in_room(room_id, exit_user.id):
        return not_in_room_by_id(room_id)
    room_manager.exit_room(room_id, exit_user.id)

    # broadcast a message to all users in this room
    room_manager.send_message(exit_user.id, room_id, "%s exit room!" % exit_user.username)
    return Response("successful exit room %s" % room.title, 200)


@app.route("/update_message/<int:room_id>/", methods=("GET", ))
@require_auth
def update_message(room_id):
    """
    Update message function, a long polling interface,
    the user must ensure 'Keep-Alive' in 'Connection' field of
    HTTP header
        POST:
            no data
        Response json format:
            {'messages':
                [{'msg_id': msg_id,
                'sender_id': sender_id,
                'sender_name': sender_name,
                'msg': msg,
                'send_time': YYYY/MM/DD,HH:MM:SS}, ...]
            }, the lastest 40 messages(if have enough messages)
        if the room is not exist, return 400
        if the 'Keep-Alive' is not in 'Connection' field, return 406
        if the user is not in this room, return 406
    """
    connection = request.headers.get('Connection', None)
    if connection is None or connection.lower() != 'keep-alive':
        return add_keep_alive()

    room = ChatRoom.query.get(room_id)
    if room is None:
        return room_not_exist_by_id(room_id)
    update_user = g.user
    if not room_manager.is_in_room(room_id, update_user.id):
        return not_in_room_by_id(room_id)
    room_manager.update_message(room_id)
    # construct the message json
    msgs = room.records.order_by(desc(ChatRoomRecord.send_time)).all()
    if len(msgs) > 40:
        msgs = msgs[:40]
    data = []
    for m in msgs:
        sender = User.query.get(m.sender_id)
        if sender is not None:
            data.append(
                {'msg_id': m.id,
                 'sender_id': m.sender_id,
                 'sender_name': sender.username,
                 'msg': m.record,
                 'send_time': m.send_time.strftime("%Y/%m/%d,%H:%M:%S")}
            )
    return jsonify(messages=data)


@app.route("/get_room_user_num/<int:room_id>/", methods=("GET", ))
@require_auth
def get_room_user_num(room_id):
    """
    Get room online user number function
        GET:
            no data
        Response json format:
            {'user_num': user_num}
        if the room is not exist, return 400
    """
    room = ChatRoom.query.get(room_id)
    if room is None:
        return room_not_exist_by_id(room_id)
    user_num = room_manager.get_room_online_user_num(room_id)
    return jsonify(user_num=user_num)


@app.route("/get_room_users/<int:room_id>/", methods=("GET", ))
@require_auth
def get_room_users(room_id):
    """
    Get room's all online users informations function
        GET:
            no data
        Response json format:
            {'users':
                [{'user_id': user_id,
                  'username': username}, ...]
            }
        if room is not exist, return 400
    """
    room = ChatRoom.query.get(room_id)
    if room is None:
        return room_not_exist_by_id(room_id)
    user_list = room_manager.get_room_online_users(room_id)
    if user_list is None:
        return jsonify(users=[])
    data = []
    for uid in user_list:
        user = User.query.get(uid)
        data.append(
            {'user_id': user.id,
             'username': user.username}
        )
    return jsonify(users=data)


@app.route("/get_room_info/<int:room_id>/", methods=("GET", ))
@require_auth
def get_room_info(room_id):
    """
    Get room information
        GET:
            no data
        Response json format:
            {'room_id': room_id, 'room_name': room_name, 'room_launcher_id': launcher_id,
            'room_launcher_name': room_launcher_name}
        return 400 if room is not exist
    """
    room = ChatRoom.query.get(room_id)
    if room is None:
        return room_not_exist_by_id(room_id)
    launcher = User.query.get(room.launcher_id)
    return jsonify(room_id=room.id, room_name=room.title,
                  room_launcher_id=launcher.id, room_launcher_name=launcher.username)
