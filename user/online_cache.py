

# store the online user in the list
# only store user id
class UserListCache(object):
    def __init__(self):
        """
        online users cache dict
        {'user_id': ip_addr}
        """
        self.user_dict = {}

    def add_user(self, ip, user):
        if user.id not in self.user_dict:
            self.user_dict[user.id] = ip

    def delete_user(self, user):
        try:
            del self.user_dict[user.id]
        except KeyError:
            pass

    def get_online_users(self):
        return self.user_dict.keys()

    def is_online(self, user):
        if user in self.user_dict.keys():
            return True
        else:
            return False

    def get_online_friends(self, user):
        print 'online user list %s' % self.user_dict
        friends = user.get_friends()
        result = {}
        for _id, ip in self.user_dict.items():
            if _id in friends:
                result[ip] = _id
        return result

    def get_online_user_ip(self, user):
        try:
            return self.user_dict[user.id]
        except:
            return None


online_users = UserListCache()
