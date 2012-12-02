import json

from flask import Blueprint
from flask import jsonify, request, Response
from flask import g
from sqlalchemy import or_

from Athena.user.models import User
from Athena.app import db
from Athena.user.online_cache import online_users
from Athena.basicauth.auth import require_auth
from Athena.util import get_json_post_data, no_post_data, user_not_exist_by_id, user_not_exist_by_name
from Athena.talk.talk_suck import talk_manager
from Athena.chatroom.room_suck import room_manager



# contains login, logout
# register
# get online friends
# heartbeat packages
# Authentication: BasicAuth

app = Blueprint('user', __name__)


# register must be refined, current implementation is unsafe
@app.route('/register/', methods=('POST',))
def register():
    """
    Register function
        POST json format:
            {'username': username, 'password': password, 'email': email}
        Response json format:
            {'user_id': user_id}
        If the user was already existed, return error code 406
    """
    info = get_json_post_data()
    if info is None:
        return no_post_data
    name = info.get('username', None)
    pwd = info.get('password', None)
    mail = info.get('email', None)

    if name is None or pwd is None or mail is None:
        return Response(status=406)

    # determine the user if exist
    u = User.query.filter_by(username=name).all()
    if len(u) > 0:
        return Response("user %s has already existed" % name, status=406)
    else:
        new_user = User(username=name, email=mail, password=pwd)
        db.session.add(new_user)
        db.session.commit()
        return jsonify(user_id=new_user.id)


# like register, current implementation is unsafe
@app.route('/login/', methods=('POST', ))
def login():
    """
    Login function
        POST json format:
            {'username_or_mail': username_or_mail, 'password': password}
        Response json format:
            {'user_id': user_id}
        If password is wrong or the user is not exist, return error code 400
    """
    info = get_json_post_data()
    if info is None:
        return no_post_data
    name_or_mail = info.get('username_or_mail', None)
    pwd = info.get('password', None)
    if name_or_mail is None or pwd is None:
        return Response(status=406)
    user_list = User.query.filter(or_(User.username == name_or_mail,
                                      User.email == name_or_mail))
    user = user_list.first()
    ip = request.remote_addr
    if user is None or not user.check_password(pwd):
        return user_not_exist_by_name(name_or_mail)
    else:
        online_users.add_user(ip, user)
        talk_manager.add_user(user)
        #g.user = user  # store the logined user in g
        return jsonify(user_id=user.id)


@app.route('/logout/', methods=('POST', ))
@require_auth
def logout():
    """
    Logout function
        POST:
            no data
        Response 200 if success
        If user is not exist, return 400
        If user is not online, return 406
    """
    user = g.user
    if user.id not in online_users.get_online_users():
        return Response("user %s is not online now" % user.username, 406)
    # delete user in online list, talk_manager
    del g.user
    online_users.delete_user(user)
    talk_manager.delete_user(user.id)
    room_manager.exit_all_room(user.id)
    return Response("logout success", 200)


@app.route('/heartbeat/', methods=('GET', ))
@require_auth
def heartbeat():
    """
    Hearbeat function, used to check the user whether
    connect normally
    GET:
        no data
    Response json format:
        {'connect': 'normal'}
    If the user_id correspond user is not exist, return 400
    """
    user = g.user
    if user is None:
        pass
    else:
        return jsonify(connect='normal')


@app.route('/get_online_friends/', methods=('GET', ))
@require_auth
def get_online_friends():
    """
    Get online friends function
    GET:
        no data
    Response json format:
        {'online_friends':
            [{'user_id': user_id,
              'username': username,
              'ip_addr': ip_addr}, ....]
            }
    If the user is not exist, return error code 400
    """
    user = g.user
    if user is None:
        pass
    else:
        online_list = online_users.get_online_friends(user)
        # construct the return json
        return_json = []
        for ip, _id in online_list.items():
            _user = User.query.get(_id)
            if user is not None:
                return_json.append(
                    {'user_id': _id,
                     'username': _user.username,
                     'ip_addr': ip}
                )
        return jsonify(online_friends=return_json)


@app.route('/get_friends/', methods=('GET', ))
@require_auth
def get_friends():
    """
    Get your friends list function
        GET:
            no data
        Response json format:
            {'friends':
                [{'user_id': user_id,
                'username': username,
                'ip_addr': ip_addr}, ....]
             }
             ip_addr is None when user is not online now
        return 400 if user is not exist
    """
    user = g.user
    if user is None:
        pass
    friend_list = user.get_friends()
    data_list = []
    for friend_id in friend_list:
        friend = User.query.get(friend_id)
        if friend is not None:
            ip_addr = online_users.get_online_user_ip(friend)
            data_list.append(
                {'user_id': friend_id, 'username': friend.username,
                 'ip_addr': ip_addr or ""}
            )
    return jsonify(friends=data_list)


@app.route('/add_friend/<int:user_id>/', methods=('POST', ))
@require_auth
def add_friend(user_id):
    """
    Add friend function
        POST:
            no data
        Response 200 if success
        If the user is not exist, return error code 406
    """
    from_user = g.user
    if from_user is None:
        pass
    to_user = User.query.get(user_id)
    if to_user is None:
        return user_not_exist_by_id(user_id)

    # add friend
    from_user.add_friend(to_user)
    return Response("add friend %s" % to_user.username, status=200)


@app.route('/get_user_info/<int:user_id>/', methods=('GET', ))
def get_user_info(user_id):
    """
    Get user info function
        GET:
            no data
        Response json format:
            {'username': username, 'email': email}
        If the user is not exist, return error code 400
    """
    user = User.query.get(user_id)
    if user is None:
        return user_not_exist_by_id(user_id)
    return jsonify(username=user.username, email=user.email)
