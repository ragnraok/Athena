import json

from flask import Response, request


def get_json_post_data():
    """
    get the post json from request.json(if exist) or request.data,
    if both not exist, return None
    """
    info = None
    if hasattr(request, 'json') and request.json is not None:
        # shit?!
        data = request.json
        if not data.endswith("\"}"):
            print 'data not complete'
            data += "\"}"
        info = json.loads(data)
        return info
    elif hasattr(request, 'data'):
        # shit?!
        data = request.data
        if not data.endswith("\"}"):
            print 'data not complete'
            data += "\"}"
        info = json.loads(data)
        return info
    else:
        return None

no_post_data = Response(status=406)


def user_not_exist_by_id(user_id):
    """
    the user for id is not exist,
    return error code 400
    """
    return Response("user for id %d is not exist" % user_id, 400)


def user_not_exist_by_name(username):
    """
    the user is not exist(by username),
    return error code 400
    """
    return Response("user %s is not exist" % username, 400)

