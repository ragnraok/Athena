import gevent
from gevent import monkey
monkey.patch_all()

import httplib

username = 'ragnarok'
password = '123'
site = 'localhost'
port = 8000

user_list = [('ragnarok', '123'), ('okone1288', '123'), ('okone', '123')]


def request_send(username, password):
    url = '/talk/launch_talk/2/'
    auth = (username + ":" + password).encode("base64")
    header = {'Authorization': 'Basic %s' % auth}
    conn = httplib.HTTPConnection(site, port)
    conn.request('POST', url, headers=header)
    res = conn.getresponse()
    print res.read()

jobs = [gevent.spawn(request_send, username, password) for username, password in user_list]

gevent.joinall(jobs)
