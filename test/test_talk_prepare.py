import json
import httplib

login_json_1 = json.dumps({"password": "123", "username_or_mail": "ragnarok"})
login_json_2 = json.dumps({"username_or_mail": "okone", "password": "123"})
login_json_3 = json.dumps({"username_or_mail": "okone1288", "password": "123"})

site = "localhost"
port = 8000
header = {'Content-Type': 'application/json'}
url = "/user/login/"

# login the first user
conn1 = httplib.HTTPConnection(site, port)
conn1.request('POST', url, unicode(login_json_1))
res1 = conn1.getresponse()
print res1.read()

print '\n'

# login the second user
conn2 = httplib.HTTPConnection(site, port)
conn2.request('POST', url, unicode(login_json_2))
res2 = conn2.getresponse()
print res2.read()

# login the third user
conn3 = httplib.HTTPConnection(site, port)
conn3.request('POST', url, unicode(login_json_3))
res3 = conn3.getresponse()
print res3.read()
