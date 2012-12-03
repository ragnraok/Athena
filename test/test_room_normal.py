import json
import httplib

site = "localhost"
port = 8000

create_room_url = "/chatroom/create_room/"
join_room_url = "/chatroom/join_room/"
exit_room_url = "/chatroom/exit_room/"
get_room_user_num_url = "/chatroom/get_room_user_num/"
get_room_users_url = "/chatroom/get_room_users/"
get_room_info_url = "/chatroom/get_room_info/"

login_url = "/user/login/"

username = "ragnarok"
password = "123"
auth = (username + ":" + password).encode("base64")

header = {"Authorization": "Basic %s" % auth}


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
    deli = "===========================\n"

    print "first login"
    data = json.dumps({'username_or_mail': 'ragnarok', 'password': '123'})
    test("POST", login_url, data)

    print "test create room"
    data = json.dumps({'room_name': "ragnarok_room_2"})
    test("POST", create_room_url, data)

    print deli

    print "test join room"
    test("POST", join_room_url + "1/")

    print deli

    print "test get room user num"
    test("GET", get_room_user_num_url + "1/")

    print deli

    print "test get room users"
    test("GET", get_room_users_url + "1/")

    print deli

    print "test get room info"
    test("GET", get_room_info_url + "1/")

    print deli
    print "test exit room"
    test("POST", exit_room_url + "3/")
