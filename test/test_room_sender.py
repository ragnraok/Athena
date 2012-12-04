import gevent
from gevent import monkey
monkey.patch_all()
import httplib
import json
import time

site = "localhost"
port = 8000

login_url = "/user/login/"
join_room_url = "/chatroom/join_room/1/"
send_message_url = "/chatroom/send_message/1/"


def test(method, url, header, data=None):
    conn = httplib.HTTPConnection(site, port)
    if data:
        conn.request(method, url, body=data, headers=header)
        res = conn.getresponse()
        print res.read()
    else:
        conn.request(method, url, headers=header)
        res = conn.getresponse()
        print res.read()


def test_sender(username, password):
    auth = (username + ":" + password).encode("base64")
    header = {"Authorization": "Basic %s" % auth}

    print "login"
    data = json.dumps({'username_or_mail': username, 'password': password})
    test("POST", login_url, header, data)

    print "join room"
    test("POST", join_room_url, header)

    for x in xrange(30):
        print "send message"
        data = json.dumps({'message': 'message'})
        test("POST", send_message_url, header, data)
        time.sleep(5)


if __name__ == '__main__':
    username_1 = 'ragnarok'
    password_1 = '123'

    username_2 = 'okone'
    password_2 = '123'

    params = [(username_1, password_1), (username_2, password_2)]

    jobs = [gevent.spawn(test_sender, username, password) for username, password in params]

    gevent.joinall(jobs)
