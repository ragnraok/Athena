import httplib
import json

site = "localhost"
port = 8000
url = "/chatroom/update_message/1/"

username = "ragnarok"
password = "123"
auth = (username + ":" + password).encode("base64")
header = {'Authorization': 'Basic %s' % auth, 'Connection': 'Keep-Alive'}

print "login"
login_url = "/user/login/"
data = json.dumps({'username_or_mail': 'ragnarok', 'password': '123'})
conn = httplib.HTTPConnection(site, port)
conn.request("POST", url=login_url, body=data)
res = conn.getresponse()
print res.read()

print "join room"
join_room_url = "/chatroom/join_room/1/"
conn = httplib.HTTPConnection(site, port)
conn.request("POST", url=join_room_url, headers={"Authorization": "Basic %s" % auth})
res = conn.getresponse()
print res.read()


conn = httplib.HTTPConnection(site, port)
conn.request("GET", url=url, headers=header)


while True:
    res = conn.getresponse()
    print res.read()
    conn.request("GET", url=url, headers=header)
