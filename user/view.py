import json

from flask import Blueprint
from flask import jsonify, request, Response
from sqlalchemy import or_

from Athena.user.models import User
from Athena.app import db
from Athena.user.online_cache import online_users
from Athena.basicauth.auth import require_auth
from Athena.util import get_json_post_data, no_post_data, user_not_exist_by_id, user_not_exist_by_name


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
    name = info['username']
    pwd = info['password']
    mail = info['email']

    # determine the user if exist
    u = User.query.filter_by(username=name).all()
    if u is not None:
        return Response(status=406)
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
    info = json.loads(request.data)
    name_or_mail = info['username_or_mail']
    pwd = info['password']
    user_list = User.query.filter(or_(User.username == name_or_mail,
                                      User.email == name_or_mail))
    user = user_list.first()
    if user is None or not user.check_password(pwd):
        return user_not_exist_by_name(name_or_mail)
    else:
        online_users.add_user(user)
        return jsonify(user_id=user.id)


@app.route('/heartbeat/<int:user_id>', methods=('GET', ))
@require_auth
def heartbeat(user_id):
    """
    Hearbeat function, used to check the user whether
    connect normally
    GET:
        no data
    Response json format:
        {'connect': 'normal'}
    If the user_id correspond user is not exist, return 400
    """
    user = User.query.get(user_id)
    if user is None:
        return user_not_exist_by_id(user_id)
    else:
        return jsonify(connect='normal')


@app.route('/get_online_friends/<int:user_id>', methods=('GET', ))
@require_auth
def get_online_friends(user_id):
    """
    Get online friends function
    GET:
        no data
    Response json format:
        {'online_friends':
            [{'user_id': user_id,
              'username': username}, ....]
            }
    If the user is not exist, return error code 400
    """
    user = User.query.get(user_id)
    if user is None:
        return user_not_exist_by_id(user_id)
    else:
        online_list = online_users.get_online_friends(user)
        # construct the return json
        return_json = []
        for _id in online_list:
            user = User.query.get(_id)
            if user is not None:
                return_json.append(
                    {'user_id': _id,
                     'username': user.username}
                )
        return jsonify(online_friends=return_json)


@app.route('/add_friend/<int:user_id>', methods=('POST', ))
@require_auth
def add_friend(user_id):
    """
    Add friend function
        POST json format:
            {'friend_id': friend_id}
        Response 200 if success
        If the user is not exist, return error code 406
    """
    from_user = User.query.get(user_id)
    if from_user is None:
        return user_not_exist_by_id(user_id)
    info = get_json_post_data()
    if info is None:
        return no_post_data
    to_user_id = info['friend_id']
    to_user = User.query.get(to_user_id)
    if to_user is None:
        return user_not_exist_by_id(to_user_id)

    # add friend
    from_user.add_friend(to_user)
    return Response("Success add friend", status=200)


@app.route('/get_user_info/<int:user_id>', methods=('GET', ))
@require_auth
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
