import json
import httplib
import time

username = 'ragnarok'
password = '123'
auth = (username + ":" + password).encode("base64")
header = {'Authorization': 'Basic %s' % auth, 'Connection': 'Keep-Alive'}
site = 'localhost'
port = 8000
url = '/talk/check_new_talk/'

conn = httplib.HTTPConnection(site, port)
conn.request('GET', url, headers=header)

while True:
    res = conn.getresponse()
    print res.read()
    conn.request('GET', url, headers=header)
