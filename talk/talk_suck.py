from gevent.event import Event
from gevent import monkey
monkey.patch_all()

import time

from Athena.user.online_cache import online_users


class TalkSuck(object):
    """
    God Damn Talk Suck
    """
    def __init__(self):
        self.events = {}
        self.talk_affairs = {}

    def new_talk(self, sender_id, receiver_id):
        """
        sender want to talk to receiver
        """
        print sender_id
        try:
            if self.talk_affairs.get(receiver_id, None) is None:
                self.talk_affairs[receiver_id] = []
            self.talk_affairs[receiver_id].append(sender_id)
            self.events[receiver_id].set()
            self.events[receiver_id].clear()
        except:
            pass

    def tell_to_talk(self, user_id):
        self.events[user_id].wait()
        time.sleep(0.1)
        try:
            initiator_list = self.talk_affairs[user_id]
            del self.talk_affairs[user_id]
            return initiator_list
        except:
            return None

    def add_user(self, user):
        self.events[user.id] = Event()

    def delete_user(self, user_id):
        try:
            del self.events[user_id]
            del self.talk_affairs[user_id]
        except:
            pass

talk_manager = TalkSuck()
