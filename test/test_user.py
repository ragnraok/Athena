import httplib
import json

login_json = json.dumps({'username_or_mail': 'ragnarok', 'password': '123'})
register_json = json.dumps({'username': 'okone1288', 'password': '123', 'email': 'okone1288@gmail.com'})
dummy_json = json.dumps({'no_data': 'no_data'})

user = 'ragnarok'
password = '123'

auth = (user + ":" + password).encode('base64')
header = {'Authorization': 'Basic %s' % auth, 'Content-Type': 'application/json'}
print header

header_no_auth = {'Content-Type': 'application/json'}


site = 'localhost'
port = 8000
register_url = "/user/register/"
login_url = "/user/login/"
logout_url = "/user/logout/"
heartbeat_url = "/user/heartbeat/"
get_online_friends_url = "/user/get_online_friends/"
get_friends_url = "/user/get_friends/"
add_friend_url = "/user/add_friend/"
get_user_info_url = "/user/get_user_info/"


def test(site, port, method, url, header, data):
    conn = httplib.HTTPConnection(site, port)
    conn.request(method, url, data, header)
    print 'url is ' + url
    response = conn.getresponse()
    print response.read()


if __name__ == '__main__':
    deli = "=================\n"
    print 'test login'
    test(site, port, 'POST', login_url, header, login_json)

    #print deli
    #print 'test register'
    #test(site, port, 'POST', register_url, header, register_json)

    print deli
    print 'test heartbeat'
    test(site, port, 'GET', heartbeat_url, header, dummy_json)

    print deli
    print 'test get_online_friends'
    test(site, port, 'GET', get_online_friends_url, header, dummy_json)

    print deli
    print 'test get_friends'
    test(site, port, 'GET', get_friends_url, header, dummy_json)

    print deli
    print 'test add_friend'
    test(site, port, 'POST', add_friend_url + "3/", header, dummy_json)

    print deli
    print 'test get_user_info'
    test(site, port, 'GET', get_user_info_url + "3/", header, dummy_json)

    #print deli
    #print 'test logout'
    #test(site, port, 'POST', logout_url, header, dummy_json)
