import json
import httplib

username = 'ragnarok'
password = '123'
auth = (username + ":" + password).encode("base64")
header = {'Authorization': 'Basic %s' % auth}
site = 'localhost'
port = 8000
url = '/talk/launch_talk/2/'

conn = httplib.HTTPConnection(site, port)
conn.request('POST', url, headers=header)
res = conn.getresponse()
print res.read()
