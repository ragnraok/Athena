import json

from flask import Blueprint
from flask import jsonify, request, Response
from flask import g

from Athena.user.online_cache import online_users
from Athena.user.models import User
from Athena.basicauth.auth import require_auth
from Athena.util import user_not_exist_by_id, get_json_post_data, no_post_data
from Athena.talk.talk_suck import talk_manager
from Athena.user.online_cache import online_users


##TODO
# launch a talk, if A want to talk to B,
# A tell server, server tell B, and let B
# listen in a specific port(provide in protocol)
# use gevent

app = Blueprint('talk', __name__)


@app.route('/launch_talk/<int:talk_to_user_id>/', methods=('POST', ))
@require_auth
def launch_talk(talk_to_user_id):
    """
    Launch a new talk function,
    for current logined user want to talk to user for _user_id
        POST:
            no data
        Response json format:
            {'success': 'true'}
        If the user is not exist return error code 400
        If the user is not both online, return 406
    """
    user = g.user
    if user is None:
        pass
    talk_to_user = User.query.get(talk_to_user_id)
    if talk_to_user is None:
        return user_not_exist_by_id(talk_to_user_id)
    if user.id not in online_users.get_online_users():
        return Response("User %s is not online now" % user.username, 406)
    if talk_to_user_id not in online_users.get_online_users():
        return Response("User %s is not online now" % talk_to_user.username, 406)
    talk_manager.new_talk(user.id, talk_to_user_id)
    return jsonify(success='true')


@app.route('/check_new_talk/', methods=('GET', ))
@require_auth
def check_new_talk():
    """
    Check new talk function, check if someone want to
    talk to you, please ensure 'Connection:Keep-Alive' for this
    connection
        GET:
            no data
        Response:
            if someone want to talk to you, return
            {'user_id': user_id, 'username': username,
            'user_ip': user_ip}
        If the user is not exist, return 400
        If 'Keep-Alive' is not in the 'Connection' field, return 406
        If the user is not online, return 406
    """
    connection = request.headers.get('Connection', None)
    if connection is None or connection != 'Keep-Alive':
        return Response("You should put \'Keep-Alive\' in \'Connection\' field", 406)
    user = g.user
    if user is None:
        pass
    if user.id not in online_users.get_online_users():
        return Response("User %s is not online now" % user.username, 406)
    initiator_id = talk_manager.tell_to_talk(user.id)
    if initiator_id is not None:
        initiator = User.query.get(initiator_id)
        initiator_ip = online_users.get_online_user_ip(initiator)
        return jsonify(user_id=initiator_id, username=initiator.username,
                      user_ip=initiator_ip)
