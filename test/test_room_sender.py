#import gevent
#from gevent import monkey
#monkey.patch_all()
import httplib
import json
import time

username = "ragnarok"
password = "123"
site = "localhost"
port = 8000

auth = (username + ":" + password).encode("base64")
header = {"Authorization": "Basic %s" % auth}
login_url = "/user/login/"
join_room_url = "/chatroom/join_room/1/"
send_message_url = "/chatroom/send_message/1/"


def test(method, url, data=None):
    conn = httplib.HTTPConnection(site, port)
    if data:
        conn.request(method, url, body=data, headers=header)
        res = conn.getresponse()
        print res.read()
    else:
        conn.request(method, url, headers=header)
        res = conn.getresponse()
        print res.read()

if __name__ == '__main__':
    print "login"
    data = json.dumps({'username_or_mail': username, 'password': password})
    test("POST", login_url, data)

    print "join room"
    test("POST", join_room_url)

    for x in xrange(30):
        print "send message"
        data = json.dumps({'message': 'message'})
        test("POST", send_message_url, data)
        time.sleep(5)
