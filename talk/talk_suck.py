from gevent.event import Event
from gevent import monkey
monkey.patch_all()

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
        try:
            self.talk_affairs[receiver_id] = sender_id
            self.events[receiver_id].set()
            self.events[receiver_id].clear()
        except:
            pass

    def tell_to_talk(self, user_id):
        self.events[user_id].wait()
        try:
            initiator_id = self.talk_affairs[user_id]
            return initiator_id
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
