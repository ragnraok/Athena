

# store the online user in the list
# only store user id
class UserListCache(object):
    def __init__(self):
        self.user_list = []

    def add_user(self, user):
        if user.id not in self.user_list:
            self.user_list.append(user.id)

    def delete_user(self, user):
        try:
            self.user_list.remove(user.id)
        except KeyError:
            pass

    def get_online_users(self):
        return self.user_list

    def is_online(self, user):
        if user in self.user_list:
            return True
        else:
            return False

    def get_online_friends(self, user):
        friends = user.get_friends()
        print 'friends is %s' % str(friends)
        online_friends = filter(lambda user: user.id in self.user_list,
                                friends)
        print 'online user list is %s' % self.user_list
        return online_friends


online_users = UserListCache()
